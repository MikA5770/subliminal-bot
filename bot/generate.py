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

from content import INSTRUMENTS, MELODIES, MODES, SECRET_WORDS, SONG_NAMES, interesting, platform_captions

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
    choices = [m for m in MODES if m not in recent]
    # Les formats les moins publiés passent en priorité
    least = min(state["episodes"].get(m, 0) for m in choices)
    pool = [m for m in choices if state["episodes"].get(m, 0) <= least + 1]
    return random.choice(pool)


def pick_options(mode, state):
    m = MODES[mode]
    opts = {"hook": random.choice(m["hooks"]), "inst": random.choice(INSTRUMENTS)}
    if mode == "piano":
        opts["mel"] = random.choice([x for x in MELODIES if x != "run"])
    else:
        opts["mel"] = random.choice(MELODIES)
    if mode == "reveal":
        fresh = [w for w in SECRET_WORDS if w not in state["words"][-20:]]
        opts["secret"] = random.choice(fresh or SECRET_WORDS)
    return opts


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
    mode = pick_mode(state, a.mode)
    opts = pick_options(mode, state)
    ep = state["episodes"].get(mode, 0) + 1
    opts.update({"ep": ep, "handle": HANDLE})
    t0 = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": 500, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(ENGINE.as_uri())
        page.evaluate("document.fonts.load('300 40px \"Montserrat\"')")
        page.wait_for_function("document.fonts.check('300 40px \"Montserrat\"')", timeout=20000)
        seed, info = find_seed(page, mode, opts)
        hue = random.choice([0, 40, 80, 140, 200, 260]) if MODES[mode]["hue"] else 0
        stamp = time.strftime("%Y%m%d-%H%M")
        mp4 = out / f"subliminal_{stamp}_{mode}_{ep}.mp4"
        dur = render(page, mode, seed, opts, mp4, hue)
        browser.close()
        if errors:
            raise RuntimeError("Erreurs dans le moteur : " + "; ".join(errors))

    caption, title = captions(mode, ep, opts, info)
    post = {"mode": mode, "episode": ep, "seed": seed, "options": opts, "hue": hue, "duration": round(dur, 1),
            "result": info, "file": mp4.name, "caption": caption, "title": title,
            "captions": platform_captions(mode, ep, opts["hook"])}
    (out / "post.json").write_text(json.dumps(post, indent=2, ensure_ascii=False))

    if not a.no_state:
        state["history"] = (state["history"] + [mode])[-30:]
        state["episodes"][mode] = ep
        if mode == "reveal":
            state["words"] = (state["words"] + [opts["secret"]])[-40:]
        STATE.write_text(json.dumps(state, indent=2))
    print(json.dumps({k: post[k] for k in ("mode", "episode", "duration", "file", "result")}, ensure_ascii=False))
    print(f"Terminé en {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
