"""Découpe, normalise et embarque les bruitages choisis (sfx_raw/) dans engine/sfx.js."""
import base64, glob, json, subprocess, imageio_ffmpeg
F = imageio_ffmpeg.get_ffmpeg_exe()
PICK = {  # nom : [(fichier, longueur max s, début s)]
    "pop": [("pop/00", .35, 0), ("pop/01", .35, 0), ("pop/04", .35, 0)],
    "bite": [("bite/04", .45, 0), ("bite/05", .40, 0), ("bite/01", .40, 0)],
    "knock": [("knock/03", .30, 0), ("knock/02", .35, 0), ("knock/00", .40, 0)],
    "plop": [("spit/05", .25, 0)],
    "thump": [("thump/01", .60, 0), ("thump/02", .60, 0)],
    "boom": [("boom/04", 3.2, 0), ("boom/06", 2.4, 0)],
    "glass": [("glass/03", .80, 0)],
    "whoosh": [("whoosh/02", .45, 0), ("whoosh/01", .48, 0)],
    "piano": [("piano/00", .44, s) for s in (0.01, .46, .93, 1.39, 1.85, 2.30, 2.77, 3.26, 3.70, 4.15, 4.62, 5.08)],
}
out, used = {}, []
credits = {c["file"].split("/", 1)[1].split("_")[0] + c["file"]: c for c in json.load(open("sfx_raw/credits.json"))}
for name, items in PICK.items():
    out[name] = []
    for pre, ln, st in items:
        src = glob.glob(f"sfx_raw/{pre}_*")[0]
        trim = "" if name == "piano" else "silenceremove=start_periods=1:start_threshold=-40dB,"
        base = f"{trim}atrim=0:{ln},afade=t=out:st={max(0, ln - .08):.2f}:d=0.08"
        vd = subprocess.run([F, "-ss", str(st), "-i", src, "-af", base + ",volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        peak = float(vd.split("max_volume:")[1].split("dB")[0])
        af = f"{base},volume={-1.5 - peak:.2f}dB,aresample=44100"
        mp3 = subprocess.run([F, "-v", "error", "-ss", str(st), "-i", src, "-af", af, "-ac", "1", "-c:a", "libmp3lame", "-b:a", "80k", "-f", "mp3", "-"],
                             capture_output=True, check=True).stdout
        out[name].append(base64.b64encode(mp3).decode())
        used.append(src)
open("engine/sfx.js", "w").write("// Bruitages CC0 d'Openverse (voir sfx_raw/credits.json)\nwindow.SFX=" + json.dumps(out) + ";\n")
cred = [c for c in json.load(open("sfx_raw/credits.json")) if c["file"] in used]
json.dump(cred, open("engine/sfx_credits.json", "w"), indent=1, ensure_ascii=False)
print({k: len(v) for k, v in out.items()}, round(sum(len(x) for v in out.values() for x in v) / 1024), "Ko")
