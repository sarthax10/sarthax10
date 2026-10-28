#!/usr/bin/env python3
"""Render the rest of the page: section banners, project cards, the Watchnight
feature, the quest log and the "Continue?" footer, all into assets/.
Edit the data below and re-run:  python3 scripts/cards.py
"""
import io, pathlib
from brand import DAY, NIGHT, Type, esc, pixel, pixel_width, sprite, wrap

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

# --- data -------------------------------------------------------------------
BANNERS = {  # file: (theme, eyebrow, title, subtitle, shift hours or None)
    "day-shift": ("day", "09:00 — 18:00", "The day shift", "systems, tools, and the pipelines that ship them", (9, 18)),
    "night-shift": ("night", "22:00 — 02:00", "The night shift", "games, and the tools I build to make them", (22, 26)),
    "character": ("night", "SAVE FILE 01", "Character", "stats, gear, and one alarming weakness", None),
    "quests": ("night", "IN PROGRESS", "Quest log", "what's on the bench right now", None),
}

ICONS = {
    "layers": ["..AAAAAA..", ".AAAAAAAA.", "..AAAAAA..", "..........", "..BBBBBB..",
               ".BBBBBBBB.", "..BBBBBB..", "..........", "..CCCCCC..", ".CCCCCCCC."],
    "tiles": ["AAAAA.BBBB", "AAAAA.BBBB", "AAAAA.BBBB", "AAAAA.....", "AAAAA.CCCC",
              "AAAAA.CCCC", "AAAAA.CCCC", "..........", "DDDDDDDDDD", "DDDDDDDDDD"],
    "mosaic": ["AA.BB.CC.A", "AA.BB.CC.A", "..........", "B.CC.AA.BB", "B.CC.AA.BB",
               "..........", "CC.A.BB.CC", "CC.A.BB.CC", "..........", "A.BB.CC.AA"],
    "wave": ["....A.....", "....A...A.", "..A.A...A.", "..A.A.A.A.", "A.A.A.A.A.",
             "A.A.A.A.A.", "..A.A.A.A.", "..A.A...A.", "....A...A.", "....A....."],
    "house": ["....AA....", "...AAAA...", "..AAAAAA..", ".AAAAAAAA.", "AAAAAAAAAA",
              ".BBBBBBBB.", ".BBCCBBDB.", ".BBCCBBBB.", ".BBCCBBBB.", ".BBCCBBBB."],
    "hourglass": ["AAAAAAAAAA", ".BBBBBBBB.", "..BBBBBB..", "...BBBB...", "....BB....",
                  "....CC....", "...C..C...", "..C.CC.C..", ".CCCCCCCC.", "AAAAAAAAAA"],
    "hammer": [".AAAAA....", "AAAAAAA...", "AAAAAAA...", ".AAAAA....", "...BB.....",
               "....BB....", ".....BB...", "......BB..", ".......BB.", "........BB"],
    "film": ["AAAAAAAAAA", "A.A.A.A.AA", "AAAAAAAAAA", "AAABAAAAAA", "AAABBBAAAA",
             "AAABBBBBAA", "AAABBBAAAA", "AAABAAAAAA", "AAAAAAAAAA", "A.A.A.A.AA"],
}

DAY_PROJECTS = [  # repo, icon, tags, blurb
    ("strata", "layers", "TypeScript · Windows",
     "A Windows dev environment where the terminal, a Claude Code agent, the editor, a preview and Git are all views of one project."),
    ("rackwm", "tiles", "Rust · Win32",
     "A native, Hyprland-inspired tiling window manager for Windows. Event-driven, no polling loop, config that hot-reloads."),
    ("tessera", "mosaic", "C# · .NET 10",
     "A real-time collaborative canvas on a from-scratch CRDT merge engine. Convergence is tested as a property, not by example."),
    ("juno-assistant", "wave", "Python · QML",
     "An offline wake-word voice assistant. Whisper stays asleep until you actually say its name."),
    ("urbanConnect", "house", "C# · JavaScript",
     "Home-services booking where two customers can never be sold the same hour."),
    ("antiquary", "hourglass", "Python · Ollama",
     "Short, fact-checked videos about surprising true history, with a review desk that approves every story."),
]
NIGHT_PROJECTS = [
    ("gamesmith", "hammer", "TypeScript · React",
     "The workshop at night: a local-first school I built to learn game dev from zero. Code, pixel art, chiptune, levels."),
    ("schematic", "film", "Python · HTML/JS",
     "Animated, narrated engineering explainers made end to end: script, human review, storyboard, frame-exact render."),
]

QUESTS = [  # column title, colour key, [(name, text, done)]
    ("☀ Day quests", "day", [
        ("strata", "make the agent pane feel like part of the terminal, not a guest in it", False),
        ("juno-assistant", "get false wakes down without raising the miss rate", False),
        ("tessera", "the TypeScript client, then Postgres instead of in-memory storage", False),
    ]),
    ("☾ Night quests", "night", [
        ("Watchnight", "the next playable build, and more ways to lie convincingly", False),
        ("gamesmith", "keep working through the curriculum; draw something every night", False),
    ]),
    ("★ Side quests", "side", [
        ("rackwm", "a real keybinding table, so the chords stop being hardcoded", False),
        ("Reading", "distributed systems verification", False),
        ("Sleep", "get a full eight hours", True),
    ]),
]
LAST_SAVED = "LAST SAVED · OCT 2026"


# --- helpers ----------------------------------------------------------------
def svg(w, h, alt, T, body, style=""):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(alt)}">\n  <title>{esc(alt)}</title>\n'
            f'  <style>\n    {T.css()}\n    {style}\n  </style>\n')
    return head + body + "</svg>\n"


def save(name, text):
    p = OUT / f"{name}.svg"
    p.write_text(text, encoding="utf-8")
    print(f"{p.name:24} {p.stat().st_size:>7} bytes")


BLINK = ("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}} .blink{animation:blink 1.1s steps(1,end) infinite}"
         " @media (prefers-reduced-motion:reduce){.blink{animation:none}}")


# --- banners ----------------------------------------------------------------
def banner(name, theme, eyebrow, title, sub, hours):
    T, C = Type(), (DAY if theme == "day" else NIGHT)
    W, H = 900, 100 if hours else 84
    o = [f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{C["bg"]}" stroke="{C["rule"]}" stroke-width="1.5"/>']
    icon = "☀" if theme == "day" else ("☾" if name == "night-shift" else ">")
    o.append('  ' + pixel(icon, 28, 28, 4, C["accent"] if theme == "night" else C["accent"])[0])
    o.append('  ' + T.text("CodeBold", 80, 36, eyebrow, 10.5, C["muted"], extra='letter-spacing="2"'))
    if theme == "day":
        o.append('  ' + T.text("Display", 79, 64, title, 25, C["ink"], extra='letter-spacing="-.4"'))
    else:
        o.append('  ' + pixel(title, 80, 44, 3, C["ink"])[0])
    o.append('  ' + T.text("BodyItalic", W - 28, 58, sub, 14, C["muted"], "end"))
    if hours:  # a 24h track with the shift lit up
        x0, x1, y = 80, W - 28, 82
        span = (x1 - x0) / 24
        o.append(f'  <rect x="{x0}" y="{y}" width="{x1-x0}" height="4" rx="2" fill="{C["rule"]}"/>')
        a, b = hours
        for s, e in ([(a, b)] if b <= 24 else [(a, 24), (0, b - 24)]):
            o.append(f'  <rect x="{x0+s*span:.1f}" y="{y}" width="{(e-s)*span:.1f}" height="4" rx="2" fill="{C["accent"]}"/>')
        for hr in range(0, 25, 6):
            o.append('  ' + T.text("Code", x0 + hr * span, y + 14, f"{hr:02d}", 8.5, C["muted"], "middle"))
    alt = f"{title}: {sub}" + (f" ({eyebrow})" if hours else "")
    return svg(W, H, alt, T, "\n".join(o) + "\n")


# --- project cards ----------------------------------------------------------
def card(idx, repo, icon, tags, blurb, theme):
    T, C = Type(), (DAY if theme == "day" else NIGHT)
    W, H = 440, 184
    pal = {"A": C["accent"], "B": C["accent2"], "C": C["ink"], "D": C["muted"]}
    o = [f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{C["bg"] if theme == "night" else C["panel"]}" '
         f'stroke="{C["rule"]}" stroke-width="1.5"/>',
         f'  <rect x="24" y="24" width="52" height="52" rx="12" fill="{C["accent"]}" fill-opacity=".14"/>',
         '  ' + sprite(ICONS[icon], 30, 30, 4, pal)]
    if theme == "day":
        o.append('  ' + T.text("Display", 92, 50, repo, 20, C["ink"], extra='letter-spacing="-.3"'))
    else:
        o.append('  ' + pixel(repo, 92, 33, 3, C["ink"])[0])
    label = f"{'DAY' if theme == 'day' else 'NIGHT'} {idx:02d}  ·  {tags.upper()}"
    o.append('  ' + T.text("CodeBold", 92, 70, label, 9.5, C["muted"], extra='letter-spacing="1.4"'))
    y = 108
    for line in wrap("Body", blurb, 14, W - 48)[:3]:
        o.append('  ' + T.text("Body", 24, y, line, 14, C["ink"], extra='opacity=".86"'))
        y += 20
    o.append('  ' + T.text("CodeBold", W - 24, H - 20, "open repo →", 10.5, C["accent2"] if theme == "day" else C["accent"], "end"))
    return svg(W, H, f"{repo} ({tags}): {blurb}", T, "\n".join(o) + "\n")


# --- the Watchnight feature -------------------------------------------------
def watchnight():
    T, C = Type(), NIGHT
    W, H = 900, 260
    o = ['  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B0716"/>'
         '<stop offset="1" stop-color="#2A1A45"/></linearGradient>'
         '<radialGradient id="lan"><stop offset="0" stop-color="#FFD27A" stop-opacity=".5"/>'
         '<stop offset="1" stop-color="#FFD27A" stop-opacity="0"/></radialGradient>'
         f'<clipPath id="f"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath></defs>',
         '  <g clip-path="url(#f)">',
         f'  <rect width="{W}" height="{H}" fill="url(#g)"/>']
    # scene on the right, drawn in 6px pixels
    s, sx, ground = 6, 520, 212
    o.append('  ' + sprite([".###", "##..", "##..", "##..", ".###"], 820, 30, 5, {"#": "#F4F1DE"}))
    for i, (x, y) in enumerate([(560, 40), (610, 80), (700, 30), (760, 96), (860, 120), (540, 120), (650, 140)]):
        o.append(f'  <rect class="tw" style="animation-delay:{i*0.4:.1f}s" x="{x}" y="{y}" width="3" height="3" fill="#F4F1DE"/>')
    manor = [
        "..........RR..............",
        "......RRRRRRRRRR..........",
        ".....RRRRRRRRRRRR.........",
        "....RRRRRRRRRRRRRR........",
        "...RRRRRRRRRRRRRRRR.......",
        "...WWWWWWWWWWWWWWWW.......",
        "...WW.WW.WW.WW.WWWW.......",
        "...WWLWWDWWDWWDWWWW.......",
        "...WWWWWWWWWWWWWWWW.......",
        "...WWDWWLWWDWWDWWWW.......",
        "...WWWWWWWDDWWWWWWW.......",
        "...WWWWWWWDDWWWWWWW.......",
    ]
    o.append('  ' + sprite(manor, sx, ground - len(manor) * s, s,
                           {"R": "#2A2042", "W": "#221A36", "D": "#120E1F", "L": "#FFD27A"}))
    tree = ["..#..", ".###.", ".###.", "#####", "#####", "..#..", "..#.."]
    for tx, ts in [(sx - 10, 5), (sx + 150, 4), (sx + 300, 6), (sx + 340, 4)]:
        o.append('  ' + sprite(tree, tx, ground - 7 * ts, ts, {"#": "#18242A"}))
    o.append(f'  <rect x="0" y="{ground}" width="{W}" height="{H-ground}" fill="#14101F"/>')
    o.append(f'  <rect x="0" y="{ground}" width="{W}" height="3" fill="#2C2440"/>')
    o.append('  <circle class="glow" cx="752" cy="190" r="40" fill="url(#lan)"/>')
    watcher = [".AAA.", "AAAAA", "AEAEA", ".AAA.", ".AAA.", ".A.A."]
    o.append('  <g class="bob">' + sprite(watcher, 722, ground - 36, s, {"A": "#3A3160", "E": "#FFE08A"})
             + sprite(["L", "L"], 756, ground - 30, s, {"L": "#FFD27A"}) + '</g>')
    o.append('  <rect class="fog" x="-200" y="196" width="1300" height="22" fill="#B79CFF" opacity=".08" rx="11"/>')
    # copy on the left
    o.append('  ' + T.text("CodeBold", 36, 46, "NIGHT 00  ·  NOW PLAYABLE", 10.5, C["muted"], extra='letter-spacing="2"'))
    o.append('  ' + pixel("Watchnight", 36, 62, 5, C["ink"])[0])
    y = 128
    for line in ["By day, the coziest house you have ever stayed in.", "After dark, it shows you what it is."]:
        o.append('  ' + T.text("BodyItalic", 36, y, line, 16, C["ink"], extra='opacity=".9"'))
        y += 22
    o.append('  ' + T.text("Code", 36, 186, "social deduction · horror · 1–8 players · windows", 11, C["muted"]))
    btn = "▶ Free playtest on itch.io"
    bw = pixel_width(btn, 2) + 32
    o.append(f'  <rect x="36" y="204" width="{bw}" height="34" rx="8" fill="{C["accent"]}"/>')
    o.append('  ' + pixel(btn, 52, 214, 2, "#1B1530")[0])
    o.append('  </g>')
    o.append(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{C["rule"]}" stroke-width="1.5"/>')
    style = ("@keyframes tw{0%,100%{opacity:1}50%{opacity:.2}} .tw{animation:tw 2.4s ease-in-out infinite}"
             " @keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}} .glow{animation:pulse 2.2s ease-in-out infinite}"
             " @keyframes bob{0%{transform:translateY(0)}50%{transform:translateY(-3px)}} .bob{animation:bob 1.1s steps(2,end) infinite}"
             " @keyframes fog{from{transform:translateX(0)}to{transform:translateX(200px)}} .fog{animation:fog 9s ease-in-out infinite alternate}"
             " @media (prefers-reduced-motion:reduce){.tw,.glow,.bob,.fog{animation:none}}")
    alt = ("Watchnight, a social deduction horror game for 1 to 8 players on Windows. By day, the coziest house "
           "you have ever stayed in. After dark, it shows you what it is. Free playtest on itch.io.")
    return svg(W, H, alt, T, "\n".join(o) + "\n", style)


# --- quest log --------------------------------------------------------------
def quests():
    T, C = Type(), NIGHT
    W, colw, top = 900, 260, 40
    colour = {"day": "#FF9E64", "night": C["accent2"], "side": C["accent"]}
    cols, heights = [], []
    for ci, (title, key, items) in enumerate(QUESTS):
        x = 36 + ci * (colw + 24)
        o = ['  ' + pixel(title, x, top, 2, colour[key])[0]]
        y = top + 40
        for name, text, done in items:
            o.append(f'  <rect x="{x}" y="{y-12}" width="14" height="14" rx="3" fill="none" stroke="{C["muted"]}" stroke-width="1.5"/>')
            if done:
                o.append(f'  <path d="M{x+3} {y-9}l8 8m0 -8l-8 8" stroke="{C["low"]}" stroke-width="2"/>')
            o.append('  ' + T.text("BodyBold", x + 24, y, name, 14, C["ink"], extra='opacity=".55"' if done else ""))
            lines = wrap("Body", text, 13, colw - 24)
            ly = y + 19
            for line in lines:
                o.append('  ' + T.text("Body", x + 24, ly, line, 13, C["muted"]))
                ly += 18
            if done:
                o.append(f'  <line x1="{x+24}" y1="{y+14}" x2="{x+colw-20}" y2="{y+14}" stroke="{C["low"]}" stroke-width="1.5"/>')
                o.append(f'  <rect x="{x+24}" y="{ly-8}" width="{pixel_width("Quest abandoned", 1.5)+12}" height="17" rx="4" '
                         f'fill="{C["low"]}" fill-opacity=".15"/>')
                o.append('  ' + pixel("Quest abandoned", x + 30, ly - 3, 1.5, C["low"], extra='class="blink"')[0])
                ly += 18
            y = ly + 16
        cols.append(o)
        heights.append(y)
    H = max(heights) + 30
    o = [f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{C["bg"]}" stroke="{C["rule"]}" stroke-width="1.5"/>']
    for c in cols:
        o += c
    o.append('  ' + T.text("CodeBold", W - 32, H - 22, LAST_SAVED, 10, C["muted"], "end", 'letter-spacing="1.6"'))
    alt = "Quest log. " + " ".join(
        f"{t.strip('☀☾★ ')}: " + "; ".join(f"{n}: {x}{' (abandoned)' if d else ''}" for n, x, d in items) + "."
        for t, _, items in QUESTS)
    return svg(W, H, alt, T, "\n".join(o) + "\n", BLINK)


# --- continue? footer -------------------------------------------------------
def footer():
    T, C = Type(), NIGHT
    W, H = 900, 190
    o = [f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{C["bg"]}" stroke="{C["rule"]}" stroke-width="1.5"/>']
    title_w = pixel_width("Continue?", 6)
    digit_w = pixel_width("9", 6)
    x = (W - title_w - 30 - digit_w) / 2
    o.append('  ' + pixel("Continue?", x, 40, 6, C["ink"])[0])
    for i, d in enumerate("9876543210"):
        o.append(f'  <g class="cd" style="animation-delay:{i}s">' +
                 pixel(d, x + title_w + 30, 40, 6, C["accent"])[0] + '</g>')
    yes, no = "▶ Yes", "No"
    yw = pixel_width(yes, 3)
    o.append('  ' + pixel(yes, W / 2 - 40 - yw, 108, 3, C["accent"], extra='class="blink"')[0])
    o.append('  ' + pixel(no, W / 2 + 40, 108, 3, C["muted"])[0])
    floppy = ["AAAAAAAAA.", "AABBBBBAAA", "AABBBCBAAA", "AABBBBBAAA", "AAAAAAAAAA",
              "AADDDDDDAA", "AADDDDDDAA", "AADDDDDDAA", "AAAAAAAAAA"]
    o.append('  ' + sprite(floppy, W / 2 - 98, 150, 2, {"A": C["accent2"], "B": "#D8CCFF", "C": C["bg"], "D": "#2E2747"}))
    o.append('  ' + T.text("CodeBold", W / 2 - 72, 165, "PROGRESS SAVED · SEE YOU AFTER DARK", 10, C["muted"],
                           extra='letter-spacing="1.6"'))
    style = (BLINK + " @keyframes cd{0%,9.99%{opacity:1}10%,100%{opacity:0}}"
             " .cd{opacity:0;animation:cd 10s steps(1,end) infinite}"
             " @media (prefers-reduced-motion:reduce){.cd{animation:none}.cd:first-of-type{opacity:1}}")
    return svg(W, H, "Continue? Yes. Progress saved, see you after dark.", T, "\n".join(o) + "\n", style)


if __name__ == "__main__":
    for name, args in BANNERS.items():
        save(f"banner-{name}", banner(name, *args))
    for i, p in enumerate(DAY_PROJECTS, 1):
        save(f"card-{p[0].lower()}", card(i, *p, "day"))
    for i, p in enumerate(NIGHT_PROJECTS, 1):
        save(f"card-{p[0].lower()}", card(i, *p, "night"))
    save("watchnight", watchnight())
    save("quests", quests())
    save("continue", footer())
