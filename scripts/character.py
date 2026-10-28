#!/usr/bin/env python3
"""Render assets/character.svg: an RPG character sheet.
Edit STATS / GEAR / PERKS below and re-run:  python3 scripts/character.py
"""
import io, pathlib
from brand import NIGHT as C, Type, pixel

W, H = 900, 470

STATS = [  # label, value out of 10, note
    ("SYSTEMS", 9, ""),
    ("WEB", 8, ""),
    ("INFRA", 8, "ci/cd, pipelines, the boring bits"),
    ("GAME DEV", 6, "+1 per night"),
    ("PIXEL ART", 5, "practising"),
    ("CURIOSITY", 10, "max"),
    ("SLEEP", 2, "debuffed"),
]
GEAR = ["Rust", "C#/.NET", "TypeScript", "Python",
        "CI/CD", "GH Actions", "Linux", "Postgres",
        "Godot 4", "Aseprite", "Figma", "Git"]
NIGHT_GEAR = {"Godot 4", "Aseprite", "Figma"}
NIGHT_STATS = {"GAME DEV", "PIXEL ART"}
PERKS = [
    ("From Scratch", "builds the dependency to find out where it breaks"),
    ("Receipts", "measures before deciding, writes the reasoning down"),
    ("Green Pipeline", "ships through CI, never by hand, never on a Friday"),
    ("Night Owl", "+30% focus after 22:00, -50% before coffee"),
]
ALT = ("Character sheet. Player 1: Shreyansh. Class: software engineer, multiclass: indie dev. "
       + ", ".join(f"{l} {v} of 10" for l, v, _ in STATS) + ". Equipped: " + ", ".join(GEAR)
       + ". Perks: " + "; ".join(f"{n}: {d}" for n, d in PERKS) + ".")


def build():
    T = Type()
    b = io.StringIO()
    w = b.write

    # frame: chunky border with gold corner studs
    w(f'  <rect width="{W}" height="{H}" fill="{C["bg"]}" rx="16"/>\n')
    w(f'  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="9" fill="none" '
      f'stroke="{C["rule"]}" stroke-width="2"/>\n')
    for cx, cy in [(10, 10), (W-18, 10), (10, H-18), (W-18, H-18)]:
        w(f'  <rect x="{cx}" y="{cy}" width="8" height="8" fill="{C["accent"]}"/>\n')

    # header
    w('  ' + pixel("Character sheet", 36, 34, 1.5, C["muted"])[0] + '\n')
    p1, pw = pixel("Player 1", 36, 56, 3, C["ink"])
    w('  ' + p1 + '\n')
    nm, nw = pixel("Shreyansh", 36 + pw + 18, 56, 3, C["accent"])
    w('  ' + nm + '\n')
    w(f'  <rect class="blink" x="{36+pw+18+nw+6}" y="74" width="12" height="3" fill="{C["accent"]}"/>\n')
    w('  ' + T.text("Body", W-36, 58, "CLASS", 11, C["muted"], "end", 'letter-spacing="2"') + '\n')
    w('  ' + T.text("DisplaySemi", W-36, 78, "Software Engineer", 15, "#FF9E64", "end") + '\n')
    w('  ' + T.text("Body", W-210, 58, "MULTICLASS", 11, C["muted"], "end", 'letter-spacing="2"') + '\n')
    w('  ' + T.text("DisplaySemi", W-210, 78, "Indie Dev", 15, C["accent2"], "end") + '\n')
    w(f'  <line x1="36" y1="100" x2="{W-36}" y2="100" stroke="{C["rule"]}" stroke-dasharray="4 4"/>\n')

    # stats
    w('  ' + pixel("Stats", 36, 120, 2, C["muted"])[0] + '\n')
    y = 152
    for i, (label, val, note) in enumerate(STATS):
        colour = C["low"] if val <= 2 else (C["accent2"] if label in NIGHT_STATS else C["accent"])
        w('  ' + pixel(label, 36, y, 2, C["ink"])[0] + '\n')
        for k in range(10):
            w(f'  <rect x="{160+k*19}" y="{y}" width="15" height="14" rx="2" fill="{C["panel"]}" '
              f'stroke="{C["rule"]}"/>\n')
        inner = "low" if val <= 2 else ""
        w(f'  <g class="bar" style="animation-delay:{.15+i*.12:.2f}s"><g class="{inner}">')
        for k in range(val):
            w(f'<rect x="{162+k*19}" y="{y+2}" width="11" height="10" rx="1" fill="{colour}"/>')
        w('</g></g>\n')
        w('  ' + pixel(str(val), 362, y, 2, C["ink"])[0] + '\n')
        if note:
            w('  ' + T.text("BodyItalic", 392, y + 11, note, 12, C["muted"]) + '\n')
        y += 26

    # equipped
    gx = 556
    w('  ' + pixel("Equipped", gx, 120, 2, C["muted"])[0] + '\n')
    for i, g in enumerate(GEAR):
        cx, cy = gx + (i % 4) * 78, 146 + (i // 4) * 46
        night = g in NIGHT_GEAR
        w(f'  <rect x="{cx}" y="{cy}" width="72" height="36" rx="6" fill="{C["panel"]}" '
          f'stroke="{C["accent2"] if night else C["rule"]}" stroke-opacity="{.55 if night else 1}"/>\n')
        w('  ' + T.text("Code", cx + 36, cy + 22, g, 10.5, C["accent2"] if night else C["ink"], "middle") + '\n')
    w('  ' + T.text("BodyItalic", gx, 298, "lilac = night-shift gear", 11, C["muted"]) + '\n')

    # perks
    w(f'  <line x1="36" y1="342" x2="{W-36}" y2="342" stroke="{C["rule"]}" stroke-dasharray="4 4"/>\n')
    w('  ' + pixel("Perks", 36, 362, 2, C["muted"])[0] + '\n')
    py = 374
    for name, desc in PERKS:
        w(f'  <rect x="160" y="{py-9}" width="8" height="8" fill="{C["accent"]}" '
          f'transform="rotate(45 164 {py-5})"/>\n')
        w('  ' + T.text("DisplaySemi", 180, py, name, 13, C["ink"]) + '\n')
        w('  ' + T.text("Body", 320, py, desc, 13, C["muted"]) + '\n')
        py += 22
    w('</svg>\n')

    s = io.StringIO()
    w = s.write
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'role="img" aria-label="{ALT}">\n  <title>{ALT}</title>\n')
    w('  <style>\n')
    w(f'    {T.css()}\n')
    # visible by default; the animation only plays the reveal, so static viewers see full bars
    w('    .bar{transform-box:fill-box;transform-origin:left;'
      'animation:fill 1.1s cubic-bezier(.22,.61,.36,1) backwards}\n')
    w('    .blink{animation:blink 1s steps(1,end) infinite}\n')
    w('    .low{animation:warn 1.6s ease-in-out infinite}\n')
    w('    @keyframes fill{from{transform:scaleX(0)}}\n')
    w('    @keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}\n')
    w('    @keyframes warn{0%,100%{opacity:1}50%{opacity:.35}}\n')
    w('    @media (prefers-reduced-motion:reduce){.bar{animation:none}.blink,.low{animation:none}}\n')
    w('  </style>\n')
    return s.getvalue() + b.getvalue()


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "character.svg"
    out.write_text(build(), encoding="utf-8")
    print(out.name, out.stat().st_size, "bytes")
