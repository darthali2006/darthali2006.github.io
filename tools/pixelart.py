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
    "c": "#4a2f5e",  # cloak
    "C": "#5e3d75",  # cloak light
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
        "f": "#a8463f",  # flag
        "z": "#5d5644",  # great tree, far and faint
        "Z": "#7d704c",
        "u": "#4f4a45",  # great tree trunk
    }
)


def scene():
    rnd = random.Random(7)
    g = [[SKY] * W for _ in range(H)]

    def fill_col(x, top, ch):
        for y in range(max(0, top), H):
            g[y][x] = ch

    # a great golden tree on the horizon, far behind the mountains
    blobs = [(50, 20, 9, 5), (39, 24, 9, 4), (61, 24, 9, 4), (30, 28, 7, 3),
             (70, 28, 7, 3), (44, 28, 7, 3), (56, 28, 7, 3)]
    for y in range(12, 34):
        for x in range(18, 84):
            for cx, cy, rx, ry in blobs:
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d < 1 and not (d > 0.7 and rnd.random() < 0.3):
                    g[y][x] = "Z" if (y < cy - 1 and rnd.random() < 0.7) else "z"
                    break
    for (x1, y1) in [(36, 27), (64, 27), (50, 21), (43, 24), (57, 24)]:
        for i in range(13):
            t = i / 12
            g[round(34 + (y1 - 34) * t)][round(50 + (x1 - 50) * t)] = "u"
    for y in range(32, 56):
        spread = (y - 32) // 9
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
    g[17][224] = g[17][225] = g[18][224] = "f"
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
    for x in range(W):
        fill_col(x, stand if x in flat else near_top(x), NEAR)

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
    stamp(LANTERN, hx + 15, stand - len(HERO) + 9)

    lx, ly = hx + 17.5, stand - len(HERO) + 12
    defs = (
        '<defs><radialGradient id="glow"><stop offset="0" stop-color="#ffd98a" stop-opacity=".45"/>'
        '<stop offset=".45" stop-color="#ffd98a" stop-opacity=".12"/>'
        '<stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="tree"><stop offset="0" stop-color="#f4d48e" stop-opacity=".22"/>'
        '<stop offset="1" stop-color="#f4d48e" stop-opacity="0"/></radialGradient></defs>'
        '<ellipse cx="50" cy="28" rx="44" ry="24" fill="url(#tree)"/>'
    )
    lantern_glow = f'<circle class="glow" cx="{lx}" cy="{ly}" r="18" fill="url(#glow)"/>'
    out = svg(["".join(r) for r in g], SCENE_PALETTE, defs, lantern_glow)
    return out.replace('width="320" height="96" ', 'preserveAspectRatio="xMidYMax slice" ')


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


def main():
    os.makedirs(OUT, exist_ok=True)
    write("scene.svg", scene())
    write("moon.svg", svg(MOON))
    write("hero.svg", svg(HERO))
    for name, rows in ICONS.items():
        width = max(len(r) for r in rows)
        write(f"{name}.svg", svg([r.ljust(width, ".") for r in rows]))


if __name__ == "__main__":
    main()
