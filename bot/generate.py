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
FPS = 30
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
    "tiktok": os.environ.get("HANDLE_TIKTOK", "@subliminal239"),
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


def add_handle(page, src, handle, dst, dur):
    """Identifiant en fond, qui suit le fondu au noir de la fin."""
    png = dst.with_suffix(".png")
    png.write_bytes(base64.b64decode(page.evaluate("t=>__exp.handlePng(t)", handle).split(",")[1]))
    st = max(0, dur - 0.5)
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(src), "-loop", "1", "-t", f"{dur:.2f}", "-i", str(png),
                    "-filter_complex", f"[1]format=rgba,fade=t=out:st={st:.2f}:d=0.45:alpha=1[w];[0][w]overlay=shortest=1",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", str(dst)], check=True)
    png.unlink()


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


def captions(mode, ep, opts, info):
    m = MODES[mode]
    question = m["question"]
    if mode == "war":
        question = "Which color did you pick? Comment it below"
    # Les mots-clés recherchés en première ligne (référencement), puis la série et la question
    caption = f"{m['keyword']} | {m['series']} Nº{ep}\n\n{question}\n\n" + " ".join(m["tags"])
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
    pending = [it for it in (json.loads(IDEAS.read_text()) if IDEAS.exists() else [])
               if not it.get("used") and it.get("mode") in MODES and it.get("by")]
    battle = None if a.mode and a.mode != "battle" else due_battle(state, forced=a.mode == "battle")
    forced = a.mode or ("battle" if battle else None) or next((it["mode"] for it in pending if it["mode"] not in state["history"][-1:]), None)
    mode = pick_mode(state, forced)
    opts = pick_options(mode, state)
    override = None
    if mode == "battle" and battle:
        names = [f["name"] for f in battle["fighters"]]
        opts["battle"] = {"title": battle.get("title", ""), "fighters": battle["fighters"]}
        opts["hook"] = battle.get("hook") or f"{' vs '.join(names)}. Pick a side before it starts"
        opts["cta"] = random.choice(["Who were you rooting for?", "Rematch? Comment below", "Was it fair? Comment"])
        override = {"keyword": battle.get("keyword") or f"{' vs '.join(names)} ball battle simulation",
                    "question": battle.get("question", "Who were you rooting for?"),
                    "tags": battle.get("tags", [])}
    ep = state["episodes"].get(mode, 0) + 1
    opts.update({"ep": ep, "handle": HANDLE, "cta": end_cta(ep)})
    idea = None if mode == "battle" else take_idea(mode)
    if idea:
        opts["credit"] = f"Idea by {idea['by']}"
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
        dur = render(page, mode, seed, opts, mp4, hue)
        files = {}
        for plat, h in HANDLES.items():
            if h:
                dst = mp4.with_name(f"{mp4.stem}_{plat}.mp4")
                add_handle(page, mp4, h, dst, dur)
                files[plat] = dst.name
            else:
                files[plat] = mp4.name
        browser.close()
        if errors:
            raise RuntimeError("Erreurs dans le moteur : " + "; ".join(errors))

    caption, title = captions(mode, ep, opts, info)
    post = {"mode": mode, "episode": ep, "seed": seed, "options": opts, "hue": hue, "duration": round(dur, 1),
            "result": info, "file": mp4.name, "caption": caption, "title": title,
            "files": files, "captions": platform_captions(mode, ep, opts["hook"], override)}
    if idea:
        for k in post["captions"]:
            post["captions"][k] = post["captions"][k].replace("\n\n", f"\n\nIdea by {idea['by']} 💜 Drop yours in the comments.\n\n", 1)
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
