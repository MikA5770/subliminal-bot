"""Télécharge des bruitages CC0 depuis l'API Openverse (lancé par GitHub Actions)."""
import json, os, pathlib, urllib.parse, urllib.request

QUERIES = {
    "pop": ["bubble pop", "pop mouth", "cork pop"],
    "bite": ["bite crunch", "chomp", "eating crunch", "apple bite"],
    "knock": ["marble click", "wood knock", "billiard ball", "pebble tap"],
    "boom": ["explosion", "big boom", "impact explosion"],
    "thump": ["heartbeat", "bass thump", "low thud"],
    "glass": ["glass shatter", "glass break"],
    "whoosh": ["whoosh", "swoosh"],
    "piano": ["piano note c4", "piano single note", "grand piano key"],
    "spit": ["spit", "plop", "water drop"],
}
OUT = pathlib.Path("sfx_raw")
UA = {"User-Agent": "subliminal-bot/1.0 (github.com/MikA5770/subliminal-bot)"}
credits = []
for cat, qs in QUERIES.items():
    seen, n = set(), 0
    for q in qs:
        url = "https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode({"q": q, "license": "cc0", "page_size": 20})
        try:
            data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
        except Exception as e:
            print("recherche impossible", q, e); continue
        for r in data.get("results", []):
            if r["id"] in seen or n >= 8:
                continue
            d = r.get("duration") or 0
            if not (100 <= d <= (9000 if cat in ("boom", "piano") else 4000)):
                continue
            src = r.get("url")
            ext = (r.get("filetype") or src.rsplit(".", 1)[-1])[:4]
            dst = OUT / cat / f"{n:02d}_{r['id'][:8]}.{ext}"
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                dst.write_bytes(urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=60).read())
            except Exception as e:
                print("téléchargement raté", src, e); continue
            seen.add(r["id"]); n += 1
            credits.append({"file": str(dst), "title": r.get("title"), "creator": r.get("creator"), "license": r.get("license"),
                            "license_version": r.get("license_version"), "source": r.get("foreign_landing_url"), "duration": d, "query": q})
            print(cat, dst.name, r.get("title"), d)
(OUT / "credits.json").write_text(json.dumps(credits, indent=1, ensure_ascii=False))
print(len(credits), "sons")
