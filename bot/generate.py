"""Crée une nouvelle vidéo : choisit un format différent des derniers, cherche une partie
intéressante, rend le MP4 avec le son et écrit la légende.

Usage : python bot/generate.py [--mode war] [--out out]
"""
import argparse
import base64
import json
import os
import random
import subprocess
import time
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

from content import INSTRUMENTS, MELODIES, MODES, SECRET_WORDS, SONG_NAMES, end_cta, interesting, platform_captions

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "engine" / "index.html"
STATE = ROOT / "state.json"
FPS = 60  # 60 images/s : mouvement bien plus fluide
CHROME = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
HANDLE = os.environ.get("HANDLE", "")
# ffmpeg tout prêt fourni par le paquet imageio-ffmpeg (pas d'installation système)
FFMPEG = os.environ.get("FFMPEG") or imageio_ffmpeg.get_ffmpeg_exe()


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"history": [], "episodes": {}, "words": []}


def pick_mode(state, forced=None):
    if forced:
        return forced
    recent = state["history"][-3:]
    choices = [m for m in MODES if m not in recent and m != "battle"]
    # Les formats les moins publiés passent en priorité
    least = min(state["episodes"].get(m, 0) for m in choices)
    pool = [m for m in choices if state["episodes"].get(m, 0) <= least + 1]
    return random.choice(pool)


def pick_options(mode, state):
    m = MODES[mode]
    opts = {"hook": random.choice(m["hooks"]), "inst": random.choice(INSTRUMENTS)}
    if mode in BURST_MODES:
        opts["inst"] = "piano"  # vraies notes de piano (échantillons CC0)
    if mode in ("piano", "pendulum"):
        opts["mel"] = random.choice([x for x in MELODIES if x != "run"])
    elif mode == "glass":
        opts["inst"] = random.choice(["glass", "musicbox", "kalimba"])
        opts["mel"] = random.choice([x for x in MELODIES if x not in ("run", "canon")])
    else:
        opts["mel"] = random.choice(MELODIES)
    if mode == "reveal":
        fresh = [w for w in SECRET_WORDS if w not in state["words"][-20:]]
        opts["secret"] = random.choice(fresh or SECRET_WORDS)
    return opts


IDEAS = ROOT / "ideas.json"
BATTLES = ROOT / "battles.json"
# Identifiant affiché en fond de vidéo, différent sur chaque plateforme (vide = rien)
HANDLES = {
    "tiktok": os.environ.get("HANDLE_TIKTOK", "@subliminal.tv"),
    "instagram": os.environ.get("HANDLE_INSTAGRAM", "@subliminal_tv"),
    "youtube": os.environ.get("HANDLE_YOUTUBE", "@Subliminal_TVi"),
}


def load_battles():
    return json.loads(BATTLES.read_text()) if BATTLES.exists() else []


def due_battle(state, forced=False):
    """Battle d'actualité à publier : de 2 jours avant l'événement jusqu'au jour J, une par jour max."""
    today = time.strftime("%Y-%m-%d")
    todo = sorted([b for b in load_battles() if not b.get("used")], key=lambda b: b.get("date", ""))
    if forced:
        return todo[0] if todo else None
    if state.get("battle_day") == today:
        return None
    for b in todo:
        d = time.mktime(time.strptime(b["date"], "%Y-%m-%d"))
        t = time.mktime(time.strptime(today, "%Y-%m-%d"))
        if -2 * 86400 <= t - d <= 0:
            return b
    return None


def mark_battle_used(battle):
    bs = load_battles()
    for b in bs:
        if b == battle:
            b["used"] = True
            break
    BATTLES.write_text(json.dumps(bs, indent=2, ensure_ascii=False))


# Zones visibles de chaque appli sur une image 1080x1920 (gauche, haut, droite, bas) :
# hors des boutons à droite, du texte et de la légende en bas, des onglets en haut.
SAFE = {
    "tiktok": (60, 130, 930, 1440),
    "instagram": (65, 200, 900, 1500),
    "youtube": (48, 120, 970, 1580),
}
# Partie de l'image où se trouve tout le contenu (numéro, accroche, simulation, compteur)
CONTENT = (60, 130, 1020, 1540)


def platform_version(page, src, handle, dst, plat):
    """Recadre la vidéo pour que le contenu soit centré dans la zone visible de l'appli, puis ajoute l'identifiant."""
    l, t, r, b = SAFE[plat]
    cl, ct, cr, cb = CONTENT
    s = min(1.0, (r - l) / (cr - cl), (b - t) / (cb - ct))
    ox = round((l + r) / 2 - s * (cl + cr) / 2)
    oy = round((t + b) / 2 - s * (ct + cb) / 2)
    sw, sh = round(1080 * s / 2) * 2, round(1920 * s / 2) * 2
    # bords de l'image réduite fondus dans le noir : aucune cassure visible
    mask = dst.with_name(dst.stem + "_mask.png")
    from PIL import Image, ImageFilter
    m = Image.new("L", (sw, sh), 0)
    m.paste(255, (70, 70, sw - 70, sh - 70))
    m.filter(ImageFilter.GaussianBlur(28)).save(mask)
    inputs = [FFMPEG, "-loglevel", "error", "-y", "-i", str(src), "-loop", "1", "-i", str(mask),
              "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}"]
    filt = (f"[0]scale={sw}:{sh},format=rgba[c];[1]format=gray[m];[c][m]alphamerge[v];"
            f"[2][v]overlay={ox}:{oy}:shortest=1[b]")
    png = None
    if handle:
        png = dst.with_suffix(".png")
        png.write_bytes(base64.b64decode(page.evaluate("t=>__exp.handlePng(t)", handle).split(",")[1]))
        inputs += ["-loop", "1", "-i", str(png)]
        wx, wy = round((l + r) / 2 - 540), round((t + b) / 2 - 1010)
        filt += f";[3]format=rgba[w];[b][w]overlay={wx}:{wy}:shortest=1[o]"
    else:
        filt += ";[b]null[o]"
    subprocess.run(inputs + ["-filter_complex", filt, "-map", "[o]", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(dst)], check=True)
    if png:
        png.unlink()
    mask.unlink()


TEASERS = ["WAIT FOR IT", "WATCH THE END", "IT ENDS LIKE THIS", "DON'T SCROLL"]
TEASER_LEN = 0.9
BURST_MODES = ("stamps", "twin", "blender", "hunters", "spinners", "chompers")


def add_teaser(page, mp4, at):
    """Accroche : une seconde du moment le plus fort, avec un texte, puis coupe franche vers le début."""
    png = mp4.with_name(mp4.stem + "_teaser.png")
    png.write_bytes(base64.b64decode(page.evaluate("t=>__exp.teaserPng(t)", random.choice(TEASERS)).split(",")[1]))
    out = mp4.with_name(mp4.stem + "_hook.mp4")
    # l'extrait est lu à part (2e entrée) : pas besoin de garder toute la vidéo en mémoire
    filt = (f"[2:v]setpts=PTS-STARTPTS,eq=brightness=0.04:contrast=1.08[tv];[tv][1]overlay=0:0:shortest=1[tvo];"
            f"[2:a]asetpts=PTS-STARTPTS,afade=t=out:st={TEASER_LEN-0.15:.2f}:d=0.15[ta];"
            f"[tvo][ta][0:v][0:a]concat=n=2:v=1:a=1[v][au]")
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(mp4), "-loop", "1", "-i", str(png),
                    "-ss", f"{at:.3f}", "-t", f"{TEASER_LEN:.3f}", "-i", str(mp4), "-filter_complex", filt,
                    "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    png.unlink()
    out.replace(mp4)


def take_idea(mode):
    """Idée de la communauté pour ce format (ideas.json), créditée dans la vidéo et la légende."""
    if not IDEAS.exists():
        return None
    ideas = json.loads(IDEAS.read_text())
    for it in ideas:
        if not it.get("used") and it.get("mode") == mode and it.get("by"):
            return it
    return None


def mark_idea_used(idea):
    ideas = json.loads(IDEAS.read_text())
    for it in ideas:
        if it == idea:
            it["used"] = True
            break
    IDEAS.write_text(json.dumps(ideas, indent=2, ensure_ascii=False))


def find_seed(page, mode, opts, tries=40):
    best, best_score = None, -1
    seeds = random.sample(range(1, 100000), tries)
    for i, s in enumerate(seeds):
        info = page.evaluate("([m,s,o])=>__exp.stats(m,s,90,o)", [mode, s, opts])
        score = interesting(mode, info)
        if score is not None and score > best_score:
            best, best_score = (s, info), score
        if best_score >= 7 and i >= 7:
            break
    if best is None:
        raise RuntimeError(f"Aucune partie valable trouvée pour {mode}")
    return best


def render(page, mode, seed, opts, out_mp4, hue_shift):
    page.evaluate("([m,s,o])=>__exp.start(m,s,o)", [mode, seed, opts])
    tmp_v = out_mp4.with_suffix(".v.mp4")
    vf = ["-vf", f"hue=h={hue_shift}"] if hue_shift else []
    ff = subprocess.Popen(
        [FFMPEG, "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
         "-i", "-", *vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", str(tmp_v)],
        stdin=subprocess.PIPE)
    n = 0
    while True:
        r = page.evaluate(f"__exp.frame({FPS})")
        ff.stdin.write(base64.b64decode(r["img"].split(",")[1]))
        n += 1
        if r["done"] or n > FPS * 75:
            break
    ff.stdin.close()
    ff.wait()
    dur = n / FPS
    wav = out_mp4.with_suffix(".wav")
    wav.write_bytes(base64.b64decode(page.evaluate(f"__exp.audio({dur})")))
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(tmp_v), "-i", str(wav), "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out_mp4)], check=True)
    tmp_v.unlink()
    wav.unlink()
    return dur


def captions(mode, ep, opts, info, override=None):
    # Une battle d'actualité remplace le mot-clé, la question et les hashtags (noms des combattants)
    m = dict(MODES[mode], **(override or {}))
    question = m["question"]
    tags = list(dict.fromkeys((override or {}).get("tags", []) + MODES[mode]["tags"]))
    # Les mots-clés recherchés en première ligne (référencement), puis la série et la question
    caption = f"{m['keyword']} | {m['series']} Nº{ep}\n\n{question}\n\n" + " ".join(tags)
    title = f"{m['keyword']} | {m['series']} Nº{ep}"
    return caption, title[:92] + " #shorts"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=list(MODES))
    ap.add_argument("--out", default=str(ROOT / "out"))
    ap.add_argument("--no-state", action="store_true", help="ne pas mettre à jour state.json (essai)")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    state = load_state()
    # Les battles passent uniquement par battles.json : une idée « battle » n'a pas de combattants
    pending = [it for it in (json.loads(IDEAS.read_text()) if IDEAS.exists() else [])
               if not it.get("used") and it.get("mode") in MODES and it.get("mode") != "battle" and it.get("by")]
    battle = None if a.mode and a.mode != "battle" else due_battle(state, forced=a.mode == "battle")
    forced = a.mode or ("battle" if battle else None) or next((it["mode"] for it in pending if it["mode"] not in state["history"][-1:]), None)
    mode = pick_mode(state, forced)
    if mode == "battle":
        if not battle:
            raise SystemExit("Aucune battle à publier dans battles.json (toutes utilisées ou fichier vide)")
        names = [str(f.get("name", "")).strip() for f in battle.get("fighters", [])]
        if not 2 <= len(names) <= 6 or not all(names):
            raise SystemExit(f"Battle « {battle.get('title', '')} » : il faut de 2 à 6 combattants, chacun avec un nom")
    opts = pick_options(mode, state)
    ep = state["episodes"].get(mode, 0) + 1
    opts.update({"ep": ep, "handle": HANDLE, "cta": end_cta(ep, mode)})
    override = None
    if mode == "battle":
        opts["battle"] = {"title": battle.get("title", ""), "fighters": battle["fighters"]}
        opts["hook"] = battle.get("hook") or f"{' vs '.join(names)}. Pick a side before it starts"
        # Appel à l'action propre aux battles (posé après celui par défaut pour ne pas être écrasé)
        opts["cta"] = random.choice(["Who were you rooting for?", "Rematch? Comment below", "Was it fair? Comment"])
        override = {"keyword": battle.get("keyword") or f"{' vs '.join(names)} ball battle simulation",
                    "question": battle.get("question", "Who were you rooting for?"),
                    "tags": battle.get("tags", [])}
    idea = None if mode == "battle" else take_idea(mode)
    if idea:
        by = str(idea["by"]).strip()
        by = by if by.startswith("@") else "@" + by
        opts["credit"] = f"Idea by {by}"
        if idea.get("hook"):
            opts["hook"] = idea["hook"]
    t0 = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": 500, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(ENGINE.as_uri())
        page.evaluate("document.fonts.load('300 40px \"Montserrat\"')")
        page.wait_for_function("document.fonts.check('300 40px \"Montserrat\"')", timeout=20000)
        seed, info = find_seed(page, mode, opts, tries=8 if mode == "overflow" else 40)
        hue = random.choice([0, 40, 80, 140, 200, 260]) if MODES[mode]["hue"] else 0
        stamp = time.strftime("%Y%m%d-%H%M")
        mp4 = out / f"subliminal_{stamp}_{mode}_{ep}.mp4"
        # moment montré en accroche : juste avant la fin (le plus spectaculaire), pris dans la durée connue
        teaser_at = round(max(3.0, float(info.get("dur", 20)) * 0.8), 2)
        if mode in BURST_MODES:
            # le teaser montre l'explosion finale
            teaser_at = round(float(info["dur"]) - 4.15, 2)
        opts["teaserAt"] = teaser_at
        dur = render(page, mode, seed, opts, mp4, hue)
        if teaser_at + TEASER_LEN < dur - 1:
            add_teaser(page, mp4, teaser_at)
            dur += TEASER_LEN
        files = {}
        for plat, h in HANDLES.items():
            dst = mp4.with_name(f"{mp4.stem}_{plat}.mp4")
            platform_version(page, mp4, h, dst, plat)
            files[plat] = dst.name
        browser.close()
        if errors:
            raise RuntimeError("Erreurs dans le moteur : " + "; ".join(errors))

    caption, title = captions(mode, ep, opts, info, override)
    post = {"mode": mode, "episode": ep, "seed": seed, "options": opts, "hue": hue, "duration": round(dur, 1),
            "result": info, "file": mp4.name, "caption": caption, "title": title,
            "files": files, "captions": platform_captions(mode, ep, opts["hook"], override)}
    if idea:
        for k in post["captions"]:
            post["captions"][k] = post["captions"][k].replace("\n\n", f"\n\n{opts['credit']} 💜 Drop yours in the comments.\n\n", 1)
    (out / "post.json").write_text(json.dumps(post, indent=2, ensure_ascii=False))

    if not a.no_state:
        if idea:
            mark_idea_used(idea)
        if mode == "battle" and battle:
            mark_battle_used(battle)
            state["battle_day"] = time.strftime("%Y-%m-%d")
        state["history"] = (state["history"] + [mode])[-30:]
        state["episodes"][mode] = ep
        if mode == "reveal":
            state["words"] = (state["words"] + [opts["secret"]])[-40:]
        STATE.write_text(json.dumps(state, indent=2))
    print(json.dumps({k: post[k] for k in ("mode", "episode", "duration", "file", "result")}, ensure_ascii=False))
    print(f"Terminé en {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
