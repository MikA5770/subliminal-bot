"""Textes, réglages et critères de qualité de chaque format de vidéo.

Pour ajouter une accroche ou un mot secret, il suffit de compléter les listes.
"""

INSTRUMENTS = ["musicbox", "marimba", "glass", "kalimba"]
MELODIES = ["run", "elise", "ode", "twinkle", "canon", "jingle", "frere", "mary", "greensleeves",
            "nachtmusik", "turkish", "lullaby", "minuet", "morning", "london", "auld"]
SONG_NAMES = {"elise": "Für Elise", "ode": "Ode to Joy", "twinkle": "Twinkle Twinkle", "canon": "Canon in D"}

SECRET_WORDS = [
    "PIZZA", "OCEAN", "TIGER", "GHOST", "MANGO", "ROBOT", "CANDY", "PIANO", "SPACE", "DREAM",
    "LEMON", "PANDA", "STORM", "MAGIC", "SUSHI", "HONEY", "PLANET", "COFFEE", "DRAGON", "RAINBOW",
    "CASTLE", "JUNGLE", "ROCKET", "WINTER", "COOKIE", "MONKEY", "SUNSET", "GUITAR", "BANANA", "PIRATE",
]

# hue=True : on peut décaler les couleurs de la vidéo pour varier (pas quand les couleurs ont un sens).
# min/max : durée acceptable en secondes. pick : critère de choix d'une partie « intéressante ».
MODES = {
    "rings": {
        "series": "Escape", "keyword": "Satisfying ball escape simulation",
        "hooks": ["You can't look away", "16 rings. 45 seconds. Don't blink", "Watch until the last ring"],
        "question": "Did you think it would make it?",
        "tags": ["#satisfying", "#oddlysatisfying", "#ballescape", "#hypnotic"],
        "hue": False, "min": 25, "max": 52,
    },
    "multiply": {
        "series": "Multiply", "keyword": "Satisfying bouncing balls multiplying",
        "hooks": ["Every escape becomes two", "It only gets worse from here", "Don't look away. It multiplies"],
        "question": "When did you think the ring would break?",
        "tags": ["#satisfying", "#oddlysatisfying", "#simulation", "#hypnotic"],
        "hue": False, "min": 25, "max": 55,
    },
    "grow": {
        "series": "Growth", "keyword": "Satisfying growing ball simulation",
        "hooks": ["It grows every time it touches", "Guess the final number", "It gets bigger. And bigger"],
        "question": "What was your guess for the final count?",
        "tags": ["#satisfying", "#oddlysatisfying", "#physics", "#hypnotic"],
        "hue": False, "min": 25, "max": 52,
    },
    "trail": {
        "series": "Spiral", "keyword": "Hypnotic satisfying ball spiral",
        "hooks": ["Try not to get hypnotized", "Faster every bounce. Until it breaks", "Your eyes will follow it"],
        "question": "Did it hypnotize you?",
        "tags": ["#satisfying", "#hypnotic", "#oddlysatisfying", "#physics"],
        "hue": False, "min": 15, "max": 40,
    },
    "war": {
        "series": "Color War", "keyword": "Satisfying color war ball battle",
        "hooks": ["Pick a color. Now", "Choose before it starts", "Only one color takes the ring"],
        "question": "Which color did you pick? Comment it below",
        "tags": ["#satisfying", "#colorwar", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 40, "max": 48,
    },
    "reveal": {
        "series": "Hidden Word", "keyword": "Satisfying hidden word reveal",
        "hooks": ["There is a hidden word", "Read it before it's revealed", "Your brain sees it before you do"],
        "question": "At what percent did you read it?",
        "tags": ["#satisfying", "#guesstheword", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 14, "max": 35,
    },
    "maze": {
        "series": "Maze", "keyword": "Satisfying spinning maze ball escape",
        "hooks": ["8 layers. 45 seconds. Don't blink", "Will it find the way out?", "You can't look away"],
        "question": "Escape or not, what did you say?",
        "tags": ["#satisfying", "#maze", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 25, "max": 50,
    },
    "flags": {
        "series": "Last Flag", "keyword": "Satisfying country flags ball battle",
        "hooks": ["Only one country survives", "Comment your country first", "Last flag inside wins"],
        "question": "Which country were you rooting for?",
        "tags": ["#satisfying", "#flags", "#countries", "#oddlysatisfying"],
        "hue": False, "min": 18, "max": 45,
    },
    "glass": {
        "series": "Glass", "keyword": "Satisfying glass breaking ball simulation",
        "hooks": ["One ball. Every pane is a note", "It breaks every single one", "Each pane was placed before it fell"],
        "question": "Did you hear the song?",
        "tags": ["#satisfying", "#glassbreaking", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 20, "max": 45,
    },
    "pendulum": {
        "series": "Weld", "keyword": "Satisfying double pendulum collects every block",
        "hooks": ["Every block it touches sticks", "It keeps everything it hits", "Guess how many it carries at the end"],
        "question": "How many blocks did you guess?",
        "tags": ["#satisfying", "#doublependulum", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 20, "max": 45,
    },
    "bricks": {
        "series": "Walls", "keyword": "Satisfying ball breaks every brick wall",
        "hooks": ["One bounce. One brick. Until the walls are gone", "52 bricks. One ball. No way out", "Watch the box disappear"],
        "question": "Which brick did you think would be the last?",
        "tags": ["#satisfying", "#brickbreaker", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 25, "max": 58,
    },
    "split": {
        "series": "Splinter", "keyword": "Satisfying falling bar snaps in half on every bounce",
        "hooks": ["Every bar that hits the floor snaps in half", "One bar. Guess how many pieces", "It only takes one fall"],
        "question": "How many pieces did you guess?",
        "tags": ["#satisfying", "#physics", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 12, "max": 50,
    },
    "overflow": {
        "series": "Overflow", "keyword": "1 ball becomes 262,144 balls satisfying simulation",
        "hooks": ["1 ball. It doubles every bounce. Watch the counter", "From 1 ball to 262,144", "Guess the final number before it breaks"],
        "question": "What number did you guess?",
        "tags": ["#satisfying", "#ballmultiply", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 20, "max": 58,
    },
    "crusher": {
        "series": "Crusher", "keyword": "Satisfying ball crusher simulation, every crushed ball duplicates",
        "hooks": ["Lilac or pink? Every crushed ball comes back as two", "Pick a color before it's full", "Crush one, get two. Which color fills it first?"],
        "question": "Lilac or pink, which side were you on?",
        "tags": ["#satisfying", "#hydraulicpress", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 25, "max": 50,
    },
    "battle": {
        "series": "Battle", "keyword": "Ball battle simulation",
        "hooks": ["Pick a side before it starts"],
        "question": "Who were you rooting for?",
        "tags": ["#satisfying", "#ballbattle", "#whowins", "#simulation"],
        "hue": False, "min": 26, "max": 62,
    },
    "piano": {
        "series": "Echo", "keyword": "Satisfying ball plays a song",
        "hooks": ["Listen closely", "Every touch is a note. Name it", "You know this song"],
        "question": "Which song should it play next?",
        "tags": ["#satisfying", "#guessthesong", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 15, "max": 40,
    },
}


def interesting(mode, info):
    """Renvoie un score (plus haut = meilleur) d'une partie simulée, ou None si elle est à rejeter."""
    m = MODES[mode]
    d = info["dur"]
    if d < m["min"] or d > m["max"]:
        return None
    if mode in ("rings", "maze"):
        if info["state"] == "win":
            # Victoire de justesse = suspense jusqu'à la fin
            return 10 - info["time"] if info["time"] <= 8 else 1
        left = info.get("left", 8 - info.get("lvl", 0))
        return 8 if left <= 1 else (3 if left <= 3 else None)
    if mode == "war":
        c = sorted(info["c"], reverse=True)
        gap = c[0] - c[1]
        # Pas d'égalité (le gagnant doit être clair), mais une fin serrée
        return 10 - gap if 2 <= gap <= 6 else None
    if mode == "overflow":
        return 8 if info["state"] == "break" and 26 <= d <= 56 else None
    if mode == "crusher":
        # Pas d'égalité : la couleur gagnante affichée doit être indiscutable
        if info["state"] != "full" or info["n"] < 600 or info["gap"] < 2:
            return None
        return 8 + (1 if info["gap"] <= 40 else 0)
    if mode == "bricks":
        return 8 - d / 20 if info["state"] == "clear" and info["left"] == 0 else None
    if mode == "battle":
        # Fin serrée : le gagnant termine avec peu de vie (frustration = commentaires)
        return 10 - info["hp"] / 10 if info["state"] == "win" else None
    if mode in ("pendulum", "bricks", "split"):
        if info["state"] not in ("done", "clear"):
            return None
        return 5 + min(info.get("n", 0), 2000) / 1000
    if mode == "glass":
        # Assez de vitres pour que la vidéo soit impressionnante
        return 5 + info["n"] / 20 if info["n"] >= 30 and info["state"] == "done" else None
    return 5


# ---------- Légendes par plateforme et hashtags variés ----------
import random as _r

CORE_TAGS = ["#satisfying", "#oddlysatisfying"]
GENERAL_TAGS = ["#hypnotic", "#mesmerizing", "#satisfyingvideo", "#visualasmr", "#relaxing",
                "#physics", "#simulation", "#calm", "#asmr", "#brainrelax", "#loop", "#trippy"]
MODE_TAGS = {
    "rings": ["#ballescape", "#escapechallenge", "#bouncingball", "#canitescape", "#rings"],
    "multiply": ["#bouncingballs", "#multiply", "#chaos", "#ballsimulation", "#exponential"],
    "grow": ["#growingball", "#bouncingball", "#guessthenumber", "#ballsimulation", "#bigger"],
    "trail": ["#spiral", "#hypnosis", "#bouncingball", "#speed", "#tunnel"],
    "war": ["#colorwar", "#pickacolor", "#teambattle", "#whowins", "#ballbattle"],
    "reveal": ["#guesstheword", "#hiddenword", "#wordpuzzle", "#braintest", "#reveal"],
    "maze": ["#maze", "#spinningmaze", "#ballescape", "#labyrinth", "#puzzle"],
    "flags": ["#flags", "#countries", "#countryballs", "#worldbattle", "#flagbattle"],
    "glass": ["#glassbreaking", "#ricochet", "#bouncingball", "#glass", "#oddlysatisfyingvideo"],
    "pendulum": ["#doublependulum", "#pendulum", "#chaos", "#physics", "#guessthenumber"],
    "bricks": ["#brickbreaker", "#bouncingball", "#breakout", "#ballescape", "#walls"],
    "split": ["#physics", "#breaking", "#guessthenumber", "#simulation", "#fractal"],
    "overflow": ["#ballmultiply", "#exponential", "#1ball", "#chaos", "#guessthenumber"],
    "crusher": ["#hydraulicpress", "#crusher", "#duplication", "#physics", "#asmr"],
    "battle": ["#ballbattle", "#whowins", "#pickaside", "#battle", "#simulation"],
    "piano": ["#guessthesong", "#musicball", "#piano", "#namethesong", "#melody"],
}

TIKTOK_TEMPLATES = [
    "{keyword} 🌀 {question}",
    "{keyword}. {question}",
    "{keyword} | {series} Nº{ep}. {question}",
]
INSTAGRAM_TEMPLATES = [
    "{keyword} | {series} Nº{ep}\n\n{question} 👇\n\nFollow for a new hypnotic simulation every day.",
    "{series} Nº{ep}\n{keyword}.\n\n{question}\n\nNew episode every day 🌀",
    "Try not to look away 👁️\n{keyword} | {series} Nº{ep}\n\n{question}",
]
YOUTUBE_TEMPLATES = [
    "{keyword}. Episode {ep} of the {series} series: {hook_lc}.\n\n{question}\nSubscribe for a new hypnotic simulation every day.",
    "{series} Nº{ep}: {keyword_lc} you can't stop watching.\n\n{question}\nNew Short every day on Subliminal.",
]


def _tags(mode, n_core, n_mode, n_gen):
    return (_r.sample(CORE_TAGS, n_core) + _r.sample(MODE_TAGS[mode], n_mode) + _r.sample(GENERAL_TAGS, n_gen))


def platform_captions(mode, ep, hook, override=None):
    m = dict(MODES[mode], **(override or {}))
    ctx = {"keyword": m["keyword"], "keyword_lc": m["keyword"].lower(), "series": m["series"], "ep": ep,
           "question": m["question"], "hook_lc": hook.rstrip(".").lower()}
    extra = (override or {}).get("tags", [])
    note = "\n\nSimulation, not a prediction." if mode == "battle" else ""
    tiktok = _r.choice(TIKTOK_TEMPLATES).format(**ctx) + note + "\n\n" + " ".join(extra[:2] + _tags(mode, 1, 2, 1))
    insta = _r.choice(INSTAGRAM_TEMPLATES).format(**ctx) + note + "\n\n" + " ".join(extra[:2] + _tags(mode, 2, 2, 1))
    yt_tags = ["#shorts"] + extra[:1] + _r.sample(MODE_TAGS[mode], 1) + _r.sample(CORE_TAGS, 1)
    youtube = _r.choice(YOUTUBE_TEMPLATES).format(**ctx) + note + "\n\n" + " ".join(yt_tags)
    return {"tiktok": tiktok, "instagram": insta, "youtube": youtube}


# ---------- Appels à l'action (fin de vidéo) ----------
# Pas de "like si…" (pénalisé comme engagement-bait) : on pousse le follow par la série
# et le commentaire par une question à laquelle on a envie de répondre.
CTA = {
    "follow": ["Follow for Nº{next}", "Nº{next} tomorrow"],
    "comment": ["Did you guess right?", "Suggest the next one below"],
}


def end_cta(ep):
    kind = _r.choice(["follow", "follow", "comment"])
    return _r.choice(CTA[kind]).format(next=ep + 1)
