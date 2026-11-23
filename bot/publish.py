"""Envoie la vidéo générée à TikTok, Instagram (Reel) et YouTube (Short) via l'API gratuite de Buffer.

Variables d'environnement :
  BUFFER_API_KEY  clé créée sur https://publish.buffer.com/settings/api
  VIDEO_URL       adresse publique et directe du MP4
  DRY_RUN=1       affiche les requêtes sans rien publier
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

API = "https://api.buffer.com"
ROOT = Path(__file__).resolve().parent.parent
SERVICES = ("tiktok", "instagram", "youtube")


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["BUFFER_API_KEY"],
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data["data"]


def enum_values(name):
    if not os.environ.get("BUFFER_API_KEY"):
        return []
    d = gql("query($n:String!){__type(name:$n){enumValues{name}}}", {"n": name})
    t = d.get("__type") or {}
    return [v["name"] for v in t.get("enumValues") or []]


def pick(values, wanted, default):
    for v in values:
        if v.lower() == wanted:
            return v
    for v in values:
        if wanted in v.lower():
            return v
    return default


def build_input(service, channel_id, post, url, due):
    # Une description différente par plateforme (repli sur la légende générale)
    text = post.get("captions", {}).get(service, post["caption"])
    meta = {}
    if service == "instagram":
        meta = {"instagram": {"type": pick(enum_values("PostType"), "reel", "reel"), "shouldShareToFeed": True}}
    elif service == "youtube":
        meta = {"youtube": {
            "title": post["title"][:100],
            "categoryId": "24",  # Divertissement
            "privacy": pick(enum_values("YoutubePrivacy"), "public", "public"),
            "madeForKids": False,
            "notifySubscribers": True,
            "isAiGenerated": False,
        }}
    elif service == "tiktok":
        meta = {"tiktok": {"title": post["title"].replace(" #shorts", "")[:90], "isAiGenerated": False}}
    return {
        "text": text,
        "channelId": channel_id,
        "schedulingType": "automatic",
        "mode": "shareNow",
        "assets": [{"video": {"url": url, "metadata": {"thumbnailOffset": 1500}}}],
        "metadata": meta,
    }


CREATE = """mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id dueAt } }
    ... on MutationError { message }
  }
}"""


def main():
    post = json.loads((ROOT / "out" / "post.json").read_text())
    url = os.environ["VIDEO_URL"]
    urls = json.loads(os.environ.get("VIDEO_URLS") or "{}")
    dry = os.environ.get("DRY_RUN") == "1"
    draft = os.environ.get("DRAFT") == "1"
    due = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if dry and not os.environ.get("BUFFER_API_KEY"):
        for s in SERVICES:
            print(f"[TEST sans clé] {s}:", json.dumps(build_input(s, "CHANNEL_ID", post, urls.get(s, url), due), ensure_ascii=False))
        return

    orgs = gql("query{account{organizations{id name}}}")["account"]["organizations"]
    channels = []
    for o in orgs:
        channels += gql("query($id:OrganizationId!){channels(input:{organizationId:$id}){id name service}}", {"id": o["id"]})["channels"]
    targets = {}
    for c in channels:
        s = str(c["service"]).lower()
        if s in SERVICES and s not in targets:
            targets[s] = c
    missing = [s for s in SERVICES if s not in targets]
    if missing:
        print("Réseaux non connectés dans Buffer :", ", ".join(missing))

    failures = 0
    for s, c in targets.items():
        inp = build_input(s, c["id"], post, urls.get(s, url), due)
        if draft:
            inp.update({"mode": "addToQueue", "saveToDraft": True})
        if dry:
            print(f"[TEST] {s} ({c['name']}):", json.dumps(inp, ensure_ascii=False))
            continue
        try:
            res = gql(CREATE, {"input": inp})["createPost"]
        except RuntimeError as e:
            res = {"message": str(e)}
        if not res.get("post") and draft:
            failures += 1
            print(f"ÉCHEC brouillon {s} ({c['name']}) : {res.get('message')}")
            continue
        if not (res.get("post")):
            # Plan B : programmation dans 1 minute si la publication immédiate est refusée
            print(f"Publication immédiate refusée pour {s} ({res.get('message')}), programmation dans 1 minute")
            inp.update({"mode": "customScheduled", "dueAt": due})
            res = gql(CREATE, {"input": inp})["createPost"]
        if "post" in res and res["post"]:
            if draft:
                print(f"OK {s} ({c['name']}) : brouillon créé dans Buffer")
            else:
                print(f"OK {s} ({c['name']}) : envoyé, publication {res['post']['dueAt'] or 'immédiate'}")
        else:
            failures += 1
            print(f"ÉCHEC {s} ({c['name']}) : {res.get('message')}")
    if failures or not targets:
        sys.exit(1)


if __name__ == "__main__":
    main()
