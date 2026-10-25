"""Generates the pixel art SVGs in assets/pixel/.

Every sprite is a grid of palette keys. Run `python3 tools/pixelart.py`
after editing a sprite; the output SVGs are committed so the site needs
no build step.
"""

import math
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "pixel")

PALETTE = {
    "k": "#141229",  # outline
    "h": "#33427a",  # hood
    "H": "#46589a",  # hood light
    "s": "#c48d6a",  # skin
    "e": "#141229",  # eyes
    "c": "#1f4d38",  # cloak, Slytherin green
    "C": "#2b664b",  # cloak light
    "b": "#c9a24a",  # belt / gold
    "m": "#6b4c35",  # leather
    "M": "#82603f",  # leather light
    "y": "#ffd98a",  # lantern light
    "Y": "#fff3cf",  # lantern core
    "a": "#e3b55b",  # gold accent
    "A": "#f4d48e",  # gold light
    "g": "#8a93b8",  # steel
    "w": "#dfe4f5",  # steel light
    "d": "#262b55",  # deep blue
    "D": "#353c72",  # deep blue light
    "t": "#7fd6c2",  # arcane teal
    "T": "#c4f1e6",  # arcane teal light
    "r": "#a8463f",  # red
    "p": "#efe6cf",  # parchment
    "P": "#cbbd98",  # parchment shade
    "n": "#5a4a3a",  # ink
    # guild marks
    "x": "#e50914",  # netflix red
    "X": "#b1060f",
    "q": "#0061fe",  # dropbox blue
    "v": "#76b900",  # nvidia green
    "j": "#00a1e0",  # salesforce blue
    "J": "#4fc3ef",
    "O": "#c74634",  # oracle red
    "G": "#2a8a5a",  # serpent green
    "L": "#c3c9d4",  # silver
}


def mirror(rows):
    """Builds a symmetric sprite from its left half."""
    return [r + r[::-1] for r in rows]


def svg(rows, palette=PALETTE, before="", after=""):
    h = len(rows)
    w = max(len(r) for r in rows)
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            run = 1
            while x + run < len(row) and row[x + run] == ch:
                run += 1
            if ch in palette:
                rects.append(
                    f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{palette[ch]}"/>'
                )
            x += run
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" shape-rendering="crispEdges">'
        f'{before}{"".join(rects)}{after}</svg>\n'
    )


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# ---------------------------------------------------------------- hero

HERO = [
    "......kkkk......",
    ".....kHHhhk.....",
    "....kHHhhhhk....",
    "...kHhhhhhhhk...",
    "...khhkkkkhhk...",
    "...khksssskhk...",
    "...khkesseskhk..",
    "...khksssskhk...",
    "..kchhkkkkhhck..",
    ".kCcchhhhhhccck.",
    ".kCccbbbbbbccck.",
    "kCcccmMmmmmcccck",
    "kCccmMmmmmmmccck",
    "kCccmMmmmmmmccck",
    ".kCcmmmmmmmmcck.",
    ".kccmmmkkmmmcck.",
    "..kkmmk..kmmkk..",
    "...kmmk..kmmk...",
    "...kkkk..kkkk...",
]
HERO[6] = "...khkessekhk..."

WIZARD = [
    ".....k.....tT.",
    ".....kk....Tt.",
    "....kDk.....m.",
    "....kDdk....m.",
    "...kDddk....m.",
    "..kkDdddkk..m.",
    ".kkkkkkkkkk.m.",
    "...kssssk...m.",
    "...ksesek...m.",
    "...kwwwwk...m.",
    "..kdwwwwdkssm.",
    "..kddwwdddk.m.",
    "..kdDddddk..m.",
    "..kdDddddk..m.",
    ".kddDdddddk.m.",
    ".kddDdddddk.m.",
    ".kddddddddk.m.",
    "kddddddddddkm.",
    "kkkkkkkkkkkkm.",
]

# a sentry at the castle gate, drawn small because it stands far off
KNIGHT = [
    "......w",
    "..kk..g",
    ".kggk.m",
    ".kgkk.m",
    ".kggk.m",
    "kdrdrkm",
    "kdrrdsm",
    "kdrdrkm",
    ".kddk.m",
    ".kk.kkm",
    ".kk.kk.",
]

# a distant dragon circling the far peaks
DRAGON = [
    ".......8........",
    "........88......",
    ".........888....",
    "....8....8888...",
    "...88...88888...",
    "88..8888888888.8",
    ".888888888888888",
    "....88.....88.8.",
]

# an owl keeping watch from the left tower
OWL = [
    "k...k",
    "kkkkk",
    "kokok",
    "kkkkk",
    ".kkk.",
    ".k.k.",
]

LANTERN = [
    "..k..",
    ".kkk.",
    "kyYyk",
    "kYYYk",
    "kyYyk",
    ".kkk.",
]

MOON = []
for y in range(22):
    row = ""
    for x in range(22):
        dx, dy = x - 10.5, y - 10.5
        r = math.hypot(dx, dy)
        if r > 10.6:
            row += "."
            continue
        # crescent: carve a second circle out of the upper right
        if math.hypot(x - 15, y - 7) < 8.2:
            row += "."
            continue
        shade = "p"
        if (x - 6) ** 2 + (y - 13) ** 2 < 4 or (x - 9) ** 2 + (y - 18) ** 2 < 2:
            shade = "P"
        if r > 9.6:
            shade = "P"
        row += shade
    MOON.append(row)


# ---------------------------------------------------------------- scene

W, H = 320, 96
SKY = "."
FAR, MID, NEAR = "1", "2", "3"
SCENE_PALETTE = dict(PALETTE)
SCENE_PALETTE.update(
    {
        "1": "#262c5e",
        "!": "#2e3570",  # far ridge highlight
        "2": "#191d43",
        "3": "#0e1029",
        "4": "#0b0c20",  # castle
        "5": "#151838",  # castle light side
        "o": "#f0c36a",  # lit window
        "f": "#2a8a5a",  # flag, green and silver
        "F": "#c3c9d4",
        "z": "#5d5644",  # great tree, far and faint
        "Z": "#7d704c",
        "u": "#4f4a45",  # great tree trunk
        "8": "#363d7a",  # distant dragon
    }
)


def scene():
    rnd = random.Random(7)
    g = [[SKY] * W for _ in range(H)]

    def fill_col(x, top, ch):
        for y in range(max(0, top), H):
            g[y][x] = ch

    # a great golden tree on the horizon, far behind the mountains
    blobs = [(50, 28, 9, 5), (39, 32, 9, 4), (61, 32, 9, 4), (30, 36, 7, 3),
             (70, 36, 7, 3), (44, 36, 7, 3), (56, 36, 7, 3)]
    for y in range(20, 42):
        for x in range(18, 84):
            for cx, cy, rx, ry in blobs:
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d < 1 and not (d > 0.7 and rnd.random() < 0.3):
                    g[y][x] = "Z" if (y < cy - 1 and rnd.random() < 0.7) else "z"
                    break
    for (x1, y1) in [(36, 35), (64, 35), (50, 29), (43, 32), (57, 32)]:
        for i in range(13):
            t = i / 12
            g[round(42 + (y1 - 42) * t)][round(50 + (x1 - 50) * t)] = "u"
    for y in range(40, 60):
        spread = (y - 40) // 9
        for x in range(49 - spread, 52 + spread):
            g[y][x] = "u"

    # far mountains: jagged ridgeline
    peaks = [(0, 52), (30, 40), (55, 50), (85, 34), (120, 48), (150, 38), (178, 50),
             (205, 30), (240, 46), (270, 36), (300, 48), (320, 42)]
    for x in range(W):
        for (x0, y0), (x1, y1) in zip(peaks, peaks[1:]):
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                top = round(y0 + (y1 - y0) * t + rnd.choice([0, 0, 1]))
                fill_col(x, top, FAR)
                if y1 < y0 and t > 0.15:  # light catches the left-facing slopes
                    g[top][x] = "!"
                break

    # mid hills: smooth rolling
    def mid_top(x):
        return round(66 - 5 * math.sin(x / 38) - 3 * math.sin(x / 13 + 1) - 10 * math.exp(-((x - 223) / 28) ** 2))

    for x in range(W):
        fill_col(x, mid_top(x), MID)

    # castle on the mid hill
    def block(x0, x1, top, ch="4"):
        for x in range(x0, x1):
            fill_col(x, top, ch)

    def crenel(x0, x1, top):
        for x in range(x0, x1):
            if (x - x0) % 2 == 0:
                g[top - 1][x] = "4"

    block(208, 238, 46)               # curtain wall + keep
    crenel(208, 238, 46)
    block(203, 210, 38)               # left tower
    crenel(203, 210, 38)
    block(236, 243, 36)               # right tower
    crenel(236, 243, 36)
    block(219, 227, 28)               # central spire
    for i in range(6):                # spire roof
        for x in range(219 + i, 227 - i):
            g[27 - i][x] = "4"
    for y in range(17, 22):           # flagpole
        g[y][223] = "4"
    g[17][224] = g[17][225] = "f"
    g[18][224] = g[18][225] = "F"
    for x in (204, 237, 220):         # lit sides
        for y in range(39 if x == 204 else 37 if x == 237 else 29, H):
            if g[y][x] == "4":
                g[y][x] = "5"
    for (x, y) in [(205, 42), (207, 42), (239, 40), (241, 40), (222, 32), (224, 32),
                   (213, 50), (232, 50), (222, 38)]:
        g[y][x] = "o"
        g[y + 1][x] = "o"
    for y in range(52, 56):           # gate
        for x in range(221, 225):
            g[y][x] = "o" if y > 52 or x in (222, 223) else g[y][x]

    # near hill: where the hero stands
    def near_top(x):
        return round(80 - 5 * math.sin(x / 47 + 0.4) - 2 * math.sin(x / 11) + (4 if x > 150 else 0) * math.sin((x - 150) / 60))

    flat = range(118, 138)
    stand = near_top(128)
    wflat = range(100, 118)
    wstand = near_top(109)
    for x in range(W):
        top = stand if x in flat else wstand if x in wflat else near_top(x)
        fill_col(x, top, NEAR)

    # pines along the near hill
    for x0 in [12, 26, 34, 70, 82, 160, 172, 181, 266, 280, 292, 306]:
        base = near_top(x0) + 1
        hgt = rnd.randint(10, 16)
        for i in range(hgt):
            half = (i * 4) // hgt + (1 if i % 3 == 2 else 0)
            y = base - hgt + i
            for x in range(x0 - half, x0 + half + 1):
                if 0 <= x < W and 0 <= y < H:
                    g[y][x] = NEAR

    # hero + lantern
    def stamp(sprite, x0, y0):
        for dy, row in enumerate(sprite):
            for dx, ch in enumerate(row):
                if ch != ".":
                    g[y0 + dy][x0 + dx] = ch

    hx = 120
    stamp(HERO, hx, stand - len(HERO))
    stamp(WIZARD, 102, wstand - len(WIZARD))
    stamp(KNIGHT, 193, mid_top(196) - len(KNIGHT))
    stamp(DRAGON, 150, 20)
    stamp(OWL, 204, 37 - len(OWL))
    stamp(LANTERN, hx + 15, stand - len(HERO) + 9)

    lx, ly = hx + 17.5, stand - len(HERO) + 12
    defs = (
        '<defs><radialGradient id="glow"><stop offset="0" stop-color="#ffd98a" stop-opacity=".45"/>'
        '<stop offset=".45" stop-color="#ffd98a" stop-opacity=".12"/>'
        '<stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="tree"><stop offset="0" stop-color="#f4d48e" stop-opacity=".22"/>'
        '<stop offset="1" stop-color="#f4d48e" stop-opacity="0"/></radialGradient></defs>'
        '<ellipse cx="50" cy="36" rx="44" ry="24" fill="url(#tree)"/>'
    )
    lantern_glow = f'<circle class="glow" cx="{lx}" cy="{ly}" r="18" fill="url(#glow)"/>'
    out = svg(["".join(r) for r in g], SCENE_PALETTE, defs, lantern_glow)
    return out.replace('width="320" height="96" ', 'preserveAspectRatio="xMidYMax slice" ')


# ---------------------------------------------------------------- storybook scene
# A winter dusk where three realms meet: a lamppost and a faun in a snowy wood,
# a round green door in a hillside, misty peaks, and a many-spired castle above
# a lake, lit by floating candles.

FAUN = [
    "...++++++...",
    ".++++++++++.",
    "++++++++++++",
    "........k...",
    "..nnnn..k...",
    ".nssssn.k...",
    "..sese..k...",
    "..ssss..k...",
    ".rrrrrr.k...",
    ".rssssrsk...",
    ".ssssss.k...",
    ".mmmmmm.k...",
    ".mmmmmm.....",
    ".mm..mm.....",
    ".mm..mm.....",
    "..m...m.....",
    ".kk..kk.....",
]

LAMPPOST = [
    ".###.",
    "#yYy#",
    "#YYY#",
    "#yYy#",
    ".###.",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    ".###.",
    "#####",
]

CANDLE = ["y", "Y", "p", "p", "P"]

STORY_PALETTE = dict(PALETTE)
STORY_PALETTE.update(
    {
        "1": "#3b5079",  # far peaks
        "!": "#d9e3f0",  # snow caps
        "2": "#20324f",  # forest
        "@": "#8fa6c2",  # snow on boughs
        "3": "#1a2843",  # cliff
        "4": "#121b31",  # castle
        "5": "#1d2a47",  # castle light side
        "o": "#f0c36a",  # lit window
        "6": "#28456c",  # lake
        "~": "#e9c27a",  # lake glints
        "7": "#7d94b3",  # far snow
        "8": "#a9bdd6",  # snow
        "9": "#7f97b8",  # snow shade
        "#": "#232637",  # lamppost iron
        "%": "#3f7d4a",  # round door
        "&": "#7a5a3a",  # door frame
        "+": "#262a3c",  # umbrella
    }
)


def scene_storybook():
    rnd = random.Random(11)
    g = [[SKY] * W for _ in range(H)]

    def fill_col(x, top, ch):
        for y in range(max(0, top), H):
            g[y][x] = ch

    def stamp(sprite, x0, y0):
        for dy, row in enumerate(sprite):
            for dx, ch in enumerate(row):
                if ch != "." and 0 <= x0 + dx < W and 0 <= y0 + dy < H:
                    g[y0 + dy][x0 + dx] = ch

    # misty peaks with snow caps
    peaks = [(0, 50), (24, 34), (46, 48), (70, 28), (96, 46), (124, 36), (150, 50),
             (176, 32), (204, 46), (236, 30), (268, 46), (296, 36), (320, 48)]
    for x in range(W):
        for (x0, y0), (x1, y1) in zip(peaks, peaks[1:]):
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                top = round(y0 + (y1 - y0) * t)
                fill_col(x, top, "1")
                peak_y = min(y0, y1)
                for y in range(top, min(top + 3, H)):
                    if y < peak_y + 6:
                        g[y][x] = "!"
                break

    # lake across the right half, with candlelight glinting on it
    for y in range(60, H):
        for x in range(162, W):
            g[y][x] = "6"
    for _ in range(26):
        x, y = rnd.randint(166, 290), rnd.randint(62, 86)
        for dx in range(rnd.randint(1, 3)):
            if x + dx < W:
                g[y][x + dx] = "~"

    # cliff rising from the lake
    def cliff_top(x):
        return round(56 - 8 * math.exp(-((x - 228) / 26) ** 2))

    for x in range(188, 272):
        top = cliff_top(x)
        if x < 196 or x > 262:
            top += abs(x - 229) // 6 - 4
        fill_col(x, max(top, 40), "3")

    # castle of many spires
    def tower(x0, x1, top, roof=True):
        for x in range(x0, x1):
            fill_col(x, top, "4")
        if roof:
            w = x1 - x0
            for i in range(w // 2 + 2):
                for x in range(x0 - 1 + i, x1 + 1 - i):
                    if 0 <= top - 1 - i * 2 < H:
                        g[top - 1 - i * 2][x] = "4"
                        if top - 2 - i * 2 >= 0:
                            g[top - 2 - i * 2][x] = "4"

    tower(204, 252, 44, roof=False)       # great hall
    tower(200, 205, 34)
    tower(211, 216, 30)
    tower(222, 228, 22)                   # tallest spire
    tower(234, 239, 28)
    tower(245, 250, 32)
    tower(255, 259, 40)
    for x in (201, 212, 223, 235, 246):
        for y in range(H):
            if g[y][x] == "4":
                g[y][x] = "5"
    for (x, y) in [(202, 38), (213, 34), (224, 27), (225, 33), (236, 32), (247, 36),
                   (208, 47), (211, 47), (217, 47), (230, 47), (240, 47), (243, 47), (256, 43)]:
        g[y][x] = "o"
        g[y + 1][x] = "o"

    # snowy wood behind the near hill
    for x0 in [6, 18, 30, 52, 64, 82, 96, 112, 136, 300, 312]:
        base = (70 if x0 < 150 else 68) + rnd.randint(-2, 2)
        hgt = rnd.randint(12, 18)
        for i in range(hgt):
            half = (i * 4) // hgt + (1 if i % 3 == 2 else 0)
            y = base - hgt + i
            for x in range(x0 - half, x0 + half + 1):
                if 0 <= x < W and 0 <= y < H:
                    g[y][x] = "@" if (i % 3 == 2 and x <= x0) else "2"

    # near snowfield
    def near_top(x):
        top = round(80 - 4 * math.sin(x / 41 + 0.6) - 2 * math.sin(x / 13))
        if x >= 162:                       # the shore drops away to the lake
            top = max(top, round(80 + min(x - 162, 8)))
        if x >= 278:                       # far bank where the last pines stand
            top = min(top, max(70, round(88 - (x - 278) * 0.9)))
        return top

    flat = range(100, 162)
    stand = near_top(120)
    mound = lambda x: round(stand - 11 * math.sqrt(max(0, 1 - ((x - 58) / 24) ** 2)))
    for x in range(W):
        top = stand if x in flat else near_top(x)
        if 34 <= x <= 82:
            top = min(top, mound(x))
        fill_col(x, top, "9")
        g[top][x] = "8"
        if top + 1 < H:
            g[top + 1][x] = "8"

    # round door in the hillside
    cx, cy, r = 58, stand - 4, 5
    for y in range(cy - r - 1, stand + 1):
        for x in range(cx - r - 1, cx + r + 2):
            d = math.hypot(x - cx, (y - cy) * 1.0)
            if y > cy and abs(x - cx) <= r:
                g[y][x] = "%" if abs(x - cx) < r else "&"
            elif d <= r - 0.5:
                g[y][x] = "%"
            elif d <= r + 0.7:
                g[y][x] = "&"
    g[cy + 1][cx] = "a"                        # brass knob
    for (x, y) in [(47, cy), (48, cy), (47, cy + 1), (48, cy + 1), (68, cy), (69, cy), (68, cy + 1), (69, cy + 1)]:
        g[y][x] = "o"                          # round windows either side

    # lamppost, faun and the wanderer
    stamp(LAMPPOST, 156, stand - len(LAMPPOST))
    stamp(FAUN, 142, stand - len(FAUN))
    hx = 120
    stamp(HERO, hx, stand - len(HERO))
    stamp(LANTERN, hx + 15, stand - len(HERO) + 9)

    # floating candles
    candles = [(20, 30), (112, 34), (150, 24), (166, 30), (182, 22), (290, 26), (304, 20), (314, 32)]
    for (x, y) in candles:
        stamp(CANDLE, x, y)

    glows = "".join(
        f'<circle cx="{x + 0.5}" cy="{y + 1}" r="5" fill="url(#cglow)"/>' for (x, y) in candles
    )
    defs = (
        '<defs><radialGradient id="glow"><stop offset="0" stop-color="#ffd98a" stop-opacity=".45"/>'
        '<stop offset=".45" stop-color="#ffd98a" stop-opacity=".12"/>'
        '<stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="cglow"><stop offset="0" stop-color="#ffd98a" stop-opacity=".5"/>'
        '<stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e1029" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#0e1029" stop-opacity=".85"/></linearGradient></defs>'
    )
    after = (
        glows
        + f'<circle cx="158.5" cy="{stand - len(LAMPPOST) + 2}" r="16" fill="url(#glow)"/>'
        + f'<circle cx="{hx + 17.5}" cy="{stand - len(HERO) + 12}" r="14" fill="url(#glow)"/>'
        + f'<rect x="0" y="{stand + 2}" width="{W}" height="{H - stand - 2}" fill="url(#fade)"/>'
    )
    out = svg(["".join(r) for r in g], STORY_PALETTE, defs, after)
    return out.replace(f'width="{W}" height="{H}" ', 'preserveAspectRatio="xMidYMax slice" ')


# ---------------------------------------------------------------- icons

ICONS = {
    # application security
    "shield": mirror([
        ".kkkkk",
        "kwgggg",
        "kgdddd",
        "kgddaa",
        "kgddaa",
        "kgddda",
        "kgddda",
        ".kgdda",
        ".kgddd",
        "..kgdd",
        "...kgg",
        "....kk",
    ]),
    # penetration testing
    "sword": [
        "..........kk",
        ".........kwk",
        "........kwgk",
        ".......kwgk.",
        "......kwgk..",
        "..k..kwgk...",
        "..kakwgk....",
        "...kagk.....",
        "...kmak.....",
        "..kmk.kk....",
        ".kak........",
        ".kk.........",
    ],
    # realm toggle
    "ring": [
        "..kkkk..",
        ".kAAAak.",
        "kAk..kak",
        "kAk..kak",
        "kak..kak",
        "kak..kak",
        ".kaaaak.",
        "..kkkk..",
    ],
    # threat modeling
    "map": [
        "kkkkkkkkkkkk",
        "kppppppppPpk",
        "kpnppppppPpk",
        "kppppppppPpk",
        "kppnppppPppk",
        "kpppppnpPppk",
        "kppppppppppk",
        "kpppppppnppk",
        "kPppppprprpk",
        "kPpppppprppk",
        "kPppppprprpk",
        "kkkkkkkkkkkk",
    ],
    # agentic / AI security
    "orb": mirror([
        "...kkk",
        "..kttt",
        ".kttTT",
        "kttTTT",
        "kttTTT",
        "ktttTT",
        ".ktttt",
        "..kttt",
        "..kkkk",
        ".kaaaa",
        "kaAAAA",
        "kkkkkk",
    ]),
    # bug bounty
    "coin": mirror([
        "...kkk",
        "..kaaa",
        ".kaAAA",
        "kaAAak",
        "kaAkaA",
        "kaAkaA",
        "kaAkaA",
        "kaAAak",
        ".kaAAA",
        "..kaaa",
        "...kkk",
    ]),
    # cryptography / auth
    "key": [
        ".kkkk.......",
        "kaAAak......",
        "kAkkAk......",
        "kAk.kak.....",
        "kaAAaAak....",
        ".kkkkaAak...",
        "......kaAak.",
        ".......kaAak",
        "......kaakk.",
        ".......kak..",
        "........k...",
        "............",
    ],
    # cloud / infrastructure
    "chip": [
        "..k.k.k.k...",
        ".kkkkkkkkk..",
        "kkdddddddkk.",
        ".kdDDDDDdk..",
        "kkdDttTDdkk.",
        ".kdDtTtDdk..",
        "kkdDDDDDdkk.",
        ".kdddddddk..",
        "kkkkkkkkkkk.",
        "..k.k.k.k...",
    ],
    # kernels / storage
    "scroll": [
        ".kkkkkkkkk..",
        "kPppppppppk.",
        "kPkkkkkkkPk.",
        ".kpnnnnnpk..",
        ".kpppppppk..",
        ".kpnnnnpk...",
        ".kpppppppk..",
        ".kpnnnnnpk..",
        "kPkkkkkkkPk.",
        "kPppppppppk.",
        ".kkkkkkkkk..",
    ],
    # education
    "book": [
        "kkkkkk.kkkkk",
        "kpppppkpppppk"[:12],
        "kpnnppkppnnk",
        "kpppppkpppppk"[:12],
        "kpnnnpkpnnnk",
        "kpppppkpppppk"[:12],
        "kpnnppkppnnk",
        "kpppppkpppppk"[:12],
        "kkkkkkkkkkkk",
        ".kddddkddddk",
        "..kkkkkkkkk.",
    ],
    # contact
    "letter": [
        "kkkkkkkkkkkk",
        "kpkppppppkpk",
        "kppkppppkppk",
        "kpppkppkpppk",
        "kppppkkppppk",
        "kpppprrppppk",
        "kpppprrppppk",
        "kppppppppppk",
        "kkkkkkkkkkkk",
    ],
}


GUILDS = {
    "netflix": [
        "xx....xx",
        "xxx...xx",
        "xXx...xx",
        "xX.x..xx",
        "xX.xx.Xx",
        "xX..x.Xx",
        "xX..xxXx",
        "xx...xXx",
        "xx...xxx",
        "xx....xx",
    ],
    "dropbox": [
        "..q......q..",
        ".qqq....qqq.",
        "qqqqq..qqqqq",
        ".qqq....qqq.",
        "..q......q..",
        ".qqq....qqq.",
        "qqqqq..qqqqq",
        ".qqq....qqq.",
        "..q......q..",
        ".....qq.....",
        "....qqqq....",
        ".....qq.....",
    ],
    "nvidia": [
        "vvvvvvvvvv",
        "vv....vvvv",
        "v.vvvv.vvv",
        ".vv..vv.vv",
        ".vv..vv.vv",
        "v.vvvv.vvv",
        "vv....vvvv",
        "vvvvvvvvvv",
    ],
    "salesforce": [
        "...JJ.......",
        "..jjjj.jj...",
        ".jjjjjjjjjj.",
        "jjjjjjjjjjj.",
        "jjjjjjjjjjjj",
        "jjjjjjjjjjjj",
        ".jjjjjjjjjj.",
    ],
    "oracle": [
        "..OOOOOOOO..",
        ".OO......OO.",
        "OO........OO",
        "OO........OO",
        ".OO......OO.",
        "..OOOOOOOO..",
    ],
}


SERPENT = [
    "..GGGGL.",
    ".GG...GG",
    ".GG.....",
    "..GGG...",
    "....GG..",
    ".....GG.",
    "G....GG.",
    "GG..GG..",
    ".GGGG...",
]


def main():
    os.makedirs(OUT, exist_ok=True)
    write("scene.svg", scene())
    write("scene-storybook.svg", scene_storybook())
    write("moon.svg", svg(MOON))
    write("hero.svg", svg(HERO))
    write("serpent.svg", svg(SERPENT))
    for name, rows in GUILDS.items():
        write(f"guild-{name}.svg", svg(rows))
    for name, rows in ICONS.items():
        width = max(len(r) for r in rows)
        write(f"{name}.svg", svg([r.ljust(width, ".") for r in rows]))


if __name__ == "__main__":
    main()
