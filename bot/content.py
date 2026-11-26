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
        "hooks": ["Every bar that hits the floor snaps in half. They never stop coming", "Guess how many pieces before it bursts", "The box fills up. Then it bursts"],
        "question": "How many pieces did you guess before it burst?",
        "tags": ["#satisfying", "#physics", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 35, "max": 70,
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
    "press": {
        "series": "Press", "keyword": "Satisfying hydraulic press crushes balls into rainbow colors",
        "hooks": ["Every ball it crushes explodes into 3", "Hydraulic press vs 3 balls. Watch the colors take over", "Guess how many before it can't press anymore"],
        "question": "How many balls did you think it would take?",
        "tags": ["#satisfying", "#hydraulicpress", "#oddlysatisfying", "#asmr"],
        "hue": False, "min": 25, "max": 60,
    },
    "stamps": {
        "series": "Stamps", "keyword": "Satisfying 4 hydraulic presses multiply rainbow balls until the box bursts",
        "hooks": ["This box holds 250 balls. It starts with 4", "4 presses. 1 rhythm. The box won't survive", "Every stamp doubles them. Wait for the end"],
        "question": "At what number did you think it would burst?",
        "tags": ["#satisfying", "#hydraulicpress", "#oddlysatisfying", "#asmr"],
        "hue": False, "min": 28, "max": 80,
    },
    "twin": {
        "series": "Twin Press", "keyword": "Two walls crush balls into 3 until the box explodes, satisfying simulation",
        "hooks": ["3 balls vs 2 walls. The box won't survive", "Every ball caught becomes 3. Don't scroll", "Guess the count when it explodes"],
        "question": "What count did you guess before it exploded?",
        "tags": ["#satisfying", "#hydraulicpress", "#oddlysatisfying", "#asmr"],
        "hue": False, "min": 25, "max": 80,
    },
    "blender": {
        "series": "Blender", "keyword": "2 balls in a blender, every hit splits them in 2 until it bursts",
        "hooks": ["2 balls in a blender. Every hit makes 2", "Don't blink. This blender is about to burst", "Every ball the blade touches splits in 2"],
        "question": "Would you have stopped the blender before it burst?",
        "tags": ["#satisfying", "#blender", "#oddlysatisfying", "#asmr"],
        "hue": False, "min": 28, "max": 80,
    },
    "hunters": {
        "series": "Hunters", "keyword": "Gears roam free and multiply every ball they pin until it bursts",
        "hooks": ["3 gears roam free. Every ball they pin becomes 2", "The gears are hunting. Nothing escapes", "Guess the count when it explodes"],
        "question": "What number did you guess before it exploded?",
        "tags": ["#satisfying", "#gears", "#oddlysatisfying", "#asmr"],
        "hue": False, "min": 28, "max": 80,
    },
    "spinners": {
        "series": "Spinners", "keyword": "Spinning bars drift and split every pinned ball in 2 until it bursts",
        "hooks": ["2 spinning bars. Every ball they pin splits in 2", "They drift. They spin. They multiply", "Don't scroll. This circle is about to burst"],
        "question": "Which bar do you think did the most damage?",
        "tags": ["#satisfying", "#physics", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 28, "max": 80,
    },
    "chompers": {
        "series": "Chompers", "keyword": "Chompers eat 1 ball and spit out 2 until the circle bursts",
        "hooks": ["They eat 1 ball and spit out 2", "2 chompers. 8 balls. This ends badly", "Feed them long enough and this happens"],
        "question": "How many balls did you think they could eat?",
        "tags": ["#satisfying", "#oddlysatisfying", "#asmr", "#hypnotic"],
        "hue": False, "min": 24, "max": 80,
    },
    "oval": {
        "series": "Oval", "keyword": "Satisfying bouncing balls multiply through the hole in the oval",
        "hooks": ["Every ball through the hole becomes 2", "1 ball. 1 hole. Can the oval hold them?", "Guess how many before the oval breaks"],
        "question": "How many balls did you guess before it broke?",
        "tags": ["#satisfying", "#ballmultiply", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 25, "max": 55,
    },
    "portal": {
        "series": "Portal", "keyword": "Satisfying bouncing balls multiply through the holes of the oval",
        "hooks": ["Every ball through the hole comes back as 2", "1 ball. 2 holes. Can the oval hold them?", "Guess how many before the oval breaks"],
        "question": "How many balls did you guess before it broke?",
        "tags": ["#satisfying", "#ballmultiply", "#oddlysatisfying", "#hypnotic"],
        "hue": False, "min": 25, "max": 55,
    },
    "grinder": {
        "series": "Grinder", "keyword": "Satisfying ball grinder, every ball through the gears becomes 3",
        "hooks": ["Every ball through the gears comes out as 3", "2 balls. Flip. Flip. Flip. Count them", "How many flips before it's full?"],
        "question": "How many flips did you guess?",
        "tags": ["#satisfying", "#gears", "#oddlysatisfying", "#asmr"],
        "hue": False, "min": 22, "max": 50,
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
    if mode in ("oval", "portal"):
        # Ovale qui casse vite : la vidéo reste nerveuse
        return 10 - d / 10 if info["state"] == "break" and info["n"] >= 1000 else None
    if mode in ("press", "stamps", "twin", "blender", "hunters", "spinners", "chompers"):
        return 8 if info["state"] == "full" and info["n"] >= 180 else None
    if mode == "grinder":
        return 8 if info["state"] == "full" and info["n"] >= 450 else None
    if mode == "crusher":
        # Pas d'égalité : la couleur gagnante affichée doit être indiscutable
        if info["state"] != "full" or info["n"] < 250 or info["gap"] < 2:
            return None
        return 8 + (1 if info["gap"] <= 40 else 0)
    if mode == "bricks":
        return 8 - d / 20 if info["state"] == "clear" and info["left"] == 0 else None
    if mode == "battle":
        # Fin serrée : le gagnant termine avec peu de vie (frustration = commentaires),
        # sans duel qui s'éternise (au-delà de 40 s le score baisse)
        return 10 - info["hp"] / 10 - max(0, d - 40) / 5 if info["state"] == "win" else None
    if mode == "split":
        return 5 + info["n"] / 1000 if info["state"] == "boom" else None
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
    "stamps": ["#hydraulicpress", "#crusher", "#duplication", "#physics", "#asmr"],
    "twin": ["#hydraulicpress", "#crusher", "#explosion", "#physics", "#asmr"],
    "blender": ["#blender", "#crusher", "#duplication", "#physics", "#asmr"],
    "hunters": ["#gears", "#crusher", "#duplication", "#physics", "#hypnotic"],
    "spinners": ["#crusher", "#duplication", "#physics", "#hypnotic", "#asmr"],
    "chompers": ["#crusher", "#duplication", "#physics", "#asmr", "#explosion"],
    "crusher": ["#hydraulicpress", "#crusher", "#duplication", "#physics", "#asmr"],
    "press": ["#hydraulicpress", "#crushing", "#rainbow", "#duplication", "#physics"],
    "oval": ["#bouncingballs", "#multiply", "#exponential", "#ballsimulation", "#escape"],
    "portal": ["#portal", "#bouncingballs", "#multiply", "#exponential", "#ballsimulation"],
    "grinder": ["#gears", "#hourglass", "#duplication", "#rainbow", "#physics"],
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
    "comment": ["Suggest the next one below"],
}
# Question de fin qui colle à ce que la vidéo a demandé (« Did you guess right? » n'a pas de sens
# après une vidéo où l'on n'a rien deviné, comme Multiply ou Trail)
CTA_COMMENT = {
    "grow": "Did you guess right?", "split": "Did you guess right?", "overflow": "Did you guess right?",
    "pendulum": "Did you guess right?", "reveal": "At what % did you read it?", "piano": "Did you name it in time?",
    "war": "Did your color win?", "crusher": "Did your color win?", "flags": "Did your country win?",
    "rings": "Did you think it would make it?", "maze": "Did you think it would make it?",
}


def end_cta(ep, mode=None):
    kind = _r.choice(["follow", "follow", "comment"])
    options = CTA[kind] + ([CTA_COMMENT[mode]] if kind == "comment" and mode in CTA_COMMENT else [])
    return _r.choice(options).format(next=ep + 1)
