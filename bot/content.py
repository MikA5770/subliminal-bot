"""Textes, réglages et critères de qualité de chaque format de vidéo.

Pour ajouter une accroche ou un mot secret, il suffit de compléter les listes.
"""

INSTRUMENTS = ["musicbox", "marimba", "glass", "kalimba"]
MELODIES = ["run", "elise", "ode", "twinkle", "canon"]
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
        "series": "Escape the Rings",
        "hooks": [
            "Can the ball escape all 16 rings before time runs out?",
            "16 rings. 45 seconds. Will it make it?",
            "Escape 16 rings in 45 seconds or lose. Watch till the end",
        ],
        "question": "Did you think it would make it?",
        "tags": ["#satisfying", "#physics", "#oddlysatisfying", "#ballescape"],
        "hue": True, "min": 25, "max": 52,
    },
    "multiply": {
        "series": "+2 Every Escape",
        "hooks": [
            "Every escape = 2 new balls. Can the ring hold 512?",
            "Each ball that escapes becomes two. When does it break?",
        ],
        "question": "How long did you think the ring would last?",
        "tags": ["#satisfying", "#physics", "#simulation", "#oddlysatisfying"],
        "hue": True, "min": 25, "max": 55,
    },
    "grow": {
        "series": "It Grows Every Bounce",
        "hooks": [
            "It grows every bounce. Guess the final count!",
            "Bigger with every bounce. How many until it pops?",
        ],
        "question": "What was your guess for the final count?",
        "tags": ["#satisfying", "#physics", "#oddlysatisfying", "#asmr"],
        "hue": True, "min": 25, "max": 52,
    },
    "trail": {
        "series": "Speed Tube",
        "hooks": [
            "It speeds up every bounce... until it breaks free",
            "Faster every bounce. Watch the ending",
        ],
        "question": "Which color was your favorite?",
        "tags": ["#satisfying", "#physics", "#rainbow", "#oddlysatisfying"],
        "hue": False, "min": 15, "max": 40,
    },
    "war": {
        "series": "Color War",
        "hooks": [
            "Pick a color before it starts! Who takes the ring?",
            "Choose your color now. Comment it below!",
        ],
        "question": "Which color did you pick?",
        "tags": ["#satisfying", "#colorwar", "#physics", "#oddlysatisfying"],
        "hue": False, "min": 40, "max": 48,
    },
    "reveal": {
        "series": "Mystery Word",
        "hooks": [
            "Guess the word before it is fully revealed!",
            "Can you read the hidden word before 50%?",
        ],
        "question": "At what percent did you guess it?",
        "tags": ["#satisfying", "#guesstheword", "#physics", "#oddlysatisfying"],
        "hue": False, "min": 14, "max": 35,
    },
    "maze": {
        "series": "Spinning Maze",
        "hooks": [
            "Can it escape the spinning maze in 45 seconds?",
            "8 layers. 45 seconds. Escape or not?",
        ],
        "question": "Escape or no escape, what did you say?",
        "tags": ["#satisfying", "#maze", "#physics", "#oddlysatisfying"],
        "hue": True, "min": 25, "max": 50,
    },
    "flags": {
        "series": "Last Flag Standing",
        "hooks": [
            "Comment your country! The last flag inside wins",
            "8 countries, 1 ring. Who survives?",
        ],
        "question": "Which country were you rooting for?",
        "tags": ["#satisfying", "#flags", "#countries", "#physics"],
        "hue": False, "min": 18, "max": 45,
    },
    "piano": {
        "series": "Name the Song",
        "hooks": [
            "Every bounce plays the next note. Name the song!",
            "Each bounce is a note. Can you name this song?",
        ],
        "question": "Which song should the ball play next?",
        "tags": ["#satisfying", "#guessthesong", "#piano", "#physics"],
        "hue": True, "min": 15, "max": 40,
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
    return 5
