"""Shared look for every generated SVG: palette, embedded type, a pixel font.

SVGs on GitHub are served as images, so they can't fetch web fonts. Each
render subsets the fonts it uses down to the glyphs it actually draws and
embeds them as base64 WOFF2 (all three faces are SIL OFL).

The pixel font is hand-drawn here, so anything that only uses it (the
language chart, which CI regenerates) needs no font files at all.
"""
import base64, functools, io, logging, os, pathlib

logging.getLogger("fontTools").setLevel(logging.ERROR)

# --- palette ----------------------------------------------------------------
DAY = dict(bg="#FFF6E9", panel="#FFFFFF", rule="#EBDCC6", ink="#1A2236", muted="#6B6F7E",
           accent="#D9542B", accent2="#2C6FBB", sun="#FFC94A")
NIGHT = dict(bg="#120E1F", panel="#1B1530", rule="#3A2F5C", ink="#EDE8FF", muted="#9C8FC0",
             accent="#FFD27A", accent2="#B79CFF", low="#FF6B81")

# --- embedded type ----------------------------------------------------------
_USER_FONTS = pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Windows/Fonts"
FONT_DIRS = [pathlib.Path(p) for p in os.environ.get("FONT_DIRS", "").split(os.pathsep) if p] + [
    _USER_FONTS, pathlib.Path("C:/Windows/Fonts"), pathlib.Path.home() / ".fonts",
    pathlib.Path("/usr/share/fonts")]

FACES = {  # css family -> (file, weight instance for variable fonts)
    "Display": ("Montserrat-VariableFont_wght.ttf", 800),
    "DisplaySemi": ("Montserrat-VariableFont_wght.ttf", 600),
    "Body": ("Lato-Regular.ttf", None),
    "BodyBold": ("Lato-Bold.ttf", None),
    "BodyItalic": ("Lato-Italic.ttf", None),
    "Code": ("FiraCodeNerdFontMono-Regular.ttf", None),
    "CodeBold": ("FiraCodeNerdFontMono-SemiBold.ttf", None),
}
STACK = {
    "Display": "Display,Montserrat,'Segoe UI',system-ui,sans-serif",
    "DisplaySemi": "DisplaySemi,Montserrat,'Segoe UI',system-ui,sans-serif",
    "Body": "Body,Lato,'Segoe UI',system-ui,sans-serif",
    "BodyBold": "BodyBold,Lato,'Segoe UI',system-ui,sans-serif",
    "BodyItalic": "BodyItalic,Lato,'Segoe UI',system-ui,sans-serif",
    "Code": "Code,'Fira Code',ui-monospace,'Cascadia Mono',Consolas,monospace",
    "CodeBold": "CodeBold,'Fira Code',ui-monospace,'Cascadia Mono',Consolas,monospace",
}


def _find(name):
    for d in FONT_DIRS:
        for p in (d / name, *d.rglob(name)) if d.is_dir() else ():
            if p.is_file():
                return p
    raise FileNotFoundError(f"{name} not found; set FONT_DIRS to the folder that has it")


@functools.lru_cache(None)
def _base(face):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    file, wght = FACES[face]
    font = TTFont(_find(file))
    if wght and "fvar" in font:
        font = instancer.instantiateVariableFont(font, {"wght": wght})
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def font_css(usage):
    """usage: {face: text drawn in it} -> @font-face rules, subset to that text."""
    from fontTools import subset
    from fontTools.ttLib import TTFont
    rules = []
    for face, text in usage.items():
        font = TTFont(io.BytesIO(_base(face)))
        opts = subset.Options()
        opts.flavor, opts.layout_features, opts.name_IDs, opts.hinting = "woff2", ["kern", "liga"], [], False
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(set(text + " "))))
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(f"@font-face{{font-family:{face};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "\n    ".join(rules)


class Type:
    """Collects text per face while an SVG is built, then emits the fonts it needs."""

    def __init__(self):
        self.used = {}

    def t(self, face, s):
        self.used[face] = self.used.get(face, "") + s
        return s

    def text(self, face, x, y, s, size, fill, anchor="start", extra=""):
        self.t(face, s)
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        return (f'<text x="{x}" y="{y}" font-family="{STACK[face]}" font-size="{size}" '
                f'fill="{fill}"{a} {extra}>{esc(s)}</text>')

    def css(self):
        return font_css(self.used) if self.used else ""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- pixel font (5x7, drawn for this profile) --------------------------------
_G = """
A .###. #...# #...# ##### #...# #...# #...#
B ####. #...# #...# ####. #...# #...# ####.
C .###. #...# #.... #.... #.... #...# .###.
D ####. #...# #...# #...# #...# #...# ####.
E ##### #.... #.... ####. #.... #.... #####
F ##### #.... #.... ####. #.... #.... #....
G .###. #...# #.... #.### #...# #...# .####
H #...# #...# #...# ##### #...# #...# #...#
I .###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.
J ..### ...#. ...#. ...#. #..#. #..#. .##..
K #...# #..#. #.#.. ##... #.#.. #..#. #...#
L #.... #.... #.... #.... #.... #.... #####
M #...# ##.## #.#.# #.#.# #...# #...# #...#
N #...# #...# ##..# #.#.# #..## #...# #...#
O .###. #...# #...# #...# #...# #...# .###.
P ####. #...# #...# ####. #.... #.... #....
Q .###. #...# #...# #...# #.#.# #..#. .##.#
R ####. #...# #...# ####. #.#.. #..#. #...#
S .#### #.... #.... .###. ....# ....# ####.
T ##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..
U #...# #...# #...# #...# #...# #...# .###.
V #...# #...# #...# #...# #...# .#.#. ..#..
W #...# #...# #...# #.#.# #.#.# #.#.# .#.#.
X #...# #...# .#.#. ..#.. .#.#. #...# #...#
Y #...# #...# .#.#. ..#.. ..#.. ..#.. ..#..
Z ##### ....# ...#. ..#.. .#... #.... #####
0 .###. #...# #..## #.#.# ##..# #...# .###.
1 ..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.
2 .###. #...# ....# ...#. ..#.. .#... #####
3 ####. ....# ....# .###. ....# ....# ####.
4 ...#. ..##. .#.#. #..#. ##### ...#. ...#.
5 ##### #.... ####. ....# ....# #...# .###.
6 .###. #.... #.... ####. #...# #...# .###.
7 ##### ....# ...#. ..#.. .#... .#... .#...
8 .###. #...# #...# .###. #...# #...# .###.
9 .###. #...# #...# .#### ....# ....# .###.
. . . . . . . #
: . # . . . # .
· . . . # . . .
- ... ... ... ### ... ... ...
_ ##### ..... ..... ..... ..... ..... #####
/ ..# ..# .#. .#. .#. #.. #..
! # # # # # . #
? .###. #...# ....# ...#. ..#.. ..... ..#..
' # # . . . . .
, . . . . . # #
% ##..# ##..# ...#. ..#.. .#... #..## #..##
+ ..... ..#.. ..#.. ##### ..#.. ..#.. .....
# .#.#. .#.#. ##### .#.#. ##### .#.#. .#.#.
( .# #. #. #. #. #. .#
) #. .# .# .# .# .# #.
> #... ##.. ###. #### ###. ##.. #...
* ...#... .#...#. ..###.. #.###.# ..###.. .#...#. ...#...
@ ..#.. ..#.. ##### .###. .###. .#.#. #...#
~ ..###. .##... ###... ###... ###... .##... ..###.
= ....... ......# .....## #...##. ##.##.. .###... ..#....
"""
GLYPHS = {}
for line in _G.strip().splitlines():
    ch, *rows = line.split(" ")
    GLYPHS[ch] = rows
GLYPHS[" "] = ["..."] * 7
# readable aliases: ▶ play, ☀ sun, ☾ moon, ✓ check, ★ star
ALIAS = {"▶": ">", "☀": "*", "☾": "~", "✓": "=", "★": "@"}


def pixel(s, x, y, scale=2, fill="#000", anchor="start", spacing=1, extra=""):
    """Return (svg path, width). y is the top of the 7-row cap height."""
    s = s.upper()
    w = pixel_width(s, scale, spacing)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    d, cx = [], x
    for ch in s:
        g = GLYPHS[ALIAS.get(ch, ch)] if ALIAS.get(ch, ch) in GLYPHS else GLYPHS[" "]
        for r, row in enumerate(g):
            c = 0
            while c < len(row):
                if row[c] == "#":
                    run = c
                    while run < len(row) and row[run] == "#":
                        run += 1

                    d.append(f"M{cx + c*scale:g} {y + r*scale:g}h{(run-c)*scale:g}v{scale:g}h{-(run-c)*scale:g}z")
                    c = run
                else:
                    c += 1
        cx += (len(g[0]) + spacing) * scale
    return f'<path d="{"".join(d)}" fill="{fill}" {extra}/>', w


def pixel_width(s, scale=2, spacing=1):
    s = s.upper()
    total = 0
    for ch in s:
        k = ALIAS.get(ch, ch)
        total += (len(GLYPHS.get(k, GLYPHS[" "])[0]) + spacing) * scale
    return total - spacing * scale


def sprite(rows, x, y, scale, palette):
    """Draw a multi-colour pixel sprite. rows: strings; palette: char -> colour."""
    out = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in palette:
                out.append(f'<rect x="{x+c*scale:g}" y="{y+r*scale:g}" width="{scale}" height="{scale}" fill="{palette[ch]}"/>')
    return "".join(out)


@functools.lru_cache(None)
def _metrics(face):
    from fontTools.ttLib import TTFont
    f = TTFont(io.BytesIO(_base(face)))
    return f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm


def measure(face, s, size):
    cmap, hmtx, upm = _metrics(face)
    return sum(hmtx[cmap.get(ord(ch), cmap[32])][0] for ch in s) * size / upm


def wrap(face, s, size, width):
    lines, cur = [], ""
    for word in s.split():
        test = f"{cur} {word}".strip()
        if cur and measure(face, test, size) > width:
            lines.append(cur)
            cur = word
        else:
            cur = test
    return lines + ([cur] if cur else [])
