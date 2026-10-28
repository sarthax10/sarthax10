#!/usr/bin/env python3
"""Render assets/hero.svg: a desk by a window that loops from day to night.
Day: software engineer, a CI pipeline going green. Night: indie dev, a game.
The type changes shift too: clean sans by day, pixel font by night.
Edit the copy/geometry constants below and re-run:  python3 scripts/hero.py
"""
import io, pathlib, random
from brand import Type, pixel, sprite

W, H = 900, 380
LOOP = 16  # seconds for one full day -> night -> day cycle
random.seed(10)

# --- copy -----------------------------------------------------------------
NAME = "Shreyansh Sarthak"
DAY = dict(
    clock="09:00  ·  BENGALURU, IN",
    tag="I build software by day.",
    sub="Rust · C#/.NET · TypeScript · CI/CD & infra",
    status="status: pipeline green",
)
NIGHT = dict(
    clock="02:13  ·  STILL AWAKE",
    tag="I make games by night.",
    sub="Godot · pixel art · small, strange, spooky games",
    status="status: one more build",
)
ALT = ("Shreyansh Sarthak. I build software by day and make games by night. "
       "An animated desk scene loops from day, with a CI pipeline going green on the monitor, "
       "to night, with a pixel-art game on it.")
STAGES = ["build", "test", "deploy"]


def css():
    # 0-38% day, 38-50% dusk, 50-88% night, 88-100% dawn
    stage = "".join(
        f"    .st{i}{{animation:stage{i} {LOOP}s steps(1,end) infinite}}\n"
        f"    @keyframes stage{i}{{0%,{6+i*7}%{{opacity:0}}{7+i*7}%,100%{{opacity:1}}}}\n"
        for i in range(len(STAGES)))
    return f"""
    .night{{animation:nightIn {LOOP}s ease-in-out infinite}}
    .day{{animation:dayIn {LOOP}s ease-in-out infinite}}
    .sun{{animation:sunset {LOOP}s ease-in-out infinite}}
    .moon{{animation:moonrise {LOOP}s ease-in-out infinite}}
    .tw{{animation:twinkle 2.6s ease-in-out infinite}}
    .lit{{animation:flick 5s steps(1,end) infinite}}
    .cloud{{animation:drift 30s linear infinite}}
    .caret{{animation:blink 1s steps(1,end) infinite}}
    .start{{animation:blink 1.2s steps(1,end) infinite}}
    .bob{{animation:bob 1.1s steps(2,end) infinite}}
    .glow{{animation:pulse 2.2s ease-in-out infinite}}
    .steam{{animation:steam 3s ease-out infinite}}
    .shoot{{animation:shoot {LOOP}s linear infinite}}
    .type{{animation:type {LOOP}s steps(18,end) infinite}}
{stage}    @keyframes nightIn{{0%,38%{{opacity:0}}50%,88%{{opacity:1}}100%{{opacity:0}}}}
    @keyframes dayIn{{0%,38%{{opacity:1}}50%,88%{{opacity:0}}100%{{opacity:1}}}}
    @keyframes sunset{{0%,34%{{transform:translateY(0)}}50%,90%{{transform:translateY(260px)}}100%{{transform:translateY(0)}}}}
    @keyframes moonrise{{0%,40%{{transform:translateY(260px)}}56%,86%{{transform:translateY(0)}}100%{{transform:translateY(260px)}}}}
    @keyframes twinkle{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
    @keyframes flick{{0%{{opacity:1}}40%{{opacity:.55}}43%{{opacity:1}}}}
    @keyframes drift{{from{{transform:translateX(-40px)}}to{{transform:translateX(520px)}}}}
    @keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
    @keyframes bob{{0%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}
    @keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:.95}}}}
    @keyframes steam{{0%{{opacity:0;transform:translateY(4px)}}30%{{opacity:.7}}100%{{opacity:0;transform:translateY(-14px)}}}}
    @keyframes shoot{{0%,66%{{opacity:0;transform:translate(0,0)}}67%{{opacity:1}}71%{{opacity:0;transform:translate(160px,60px)}}100%{{opacity:0}}}}
    @keyframes type{{0%{{width:0}}20%,100%{{width:150px}}}}
    @media (prefers-reduced-motion:reduce){{
      .night,.day,.sun,.moon,.tw,.lit,.cloud,.caret,.start,.bob,.glow,.steam,.shoot,.type,.st0,.st1,.st2{{animation:none}}
      .night,.shoot{{opacity:0}} .moon{{transform:translateY(260px)}}
    }}"""


def sky(w):
    w('  <rect width="900" height="380" fill="url(#skyDay)"/>\n')
    w('  <rect class="night" width="900" height="380" fill="url(#skyNight)"/>\n')
    w('  <g class="night" fill="#F4F1DE">\n')
    for _ in range(46):
        x, y = random.uniform(10, 890), random.uniform(8, 230)
        r = random.choice([0.7, 0.9, 1.1, 1.4])
        d = random.uniform(0, 2.6)
        w(f'    <circle class="tw" cx="{x:.0f}" cy="{y:.0f}" r="{r}" style="animation-delay:{d:.2f}s"/>\n')
    w('    <line class="shoot" x1="300" y1="30" x2="330" y2="41" stroke="#F4F1DE" '
      'stroke-width="1.6" stroke-linecap="round"/>\n')
    w('  </g>\n')
    w('  <g class="day" fill="#FFFFFF" opacity=".75">\n')
    for cx, cy, s, delay in [(60, 48, 1.0, 0), (260, 30, .7, -14), (420, 96, .55, -22)]:
        w(f'    <g class="cloud" style="animation-delay:{delay}s"><g transform="translate({cx} {cy}) scale({s})">'
          '<ellipse cx="0" cy="0" rx="34" ry="11"/><ellipse cx="-12" cy="-8" rx="15" ry="11"/>'
          '<ellipse cx="10" cy="-11" rx="17" ry="13"/></g></g>\n')
    w('  </g>\n')
    w('  <g class="sun"><circle cx="515" cy="62" r="44" fill="url(#sunGlow)"/>'
      '<circle cx="515" cy="62" r="22" fill="#FFC94A"/></g>\n')
    w('  <g class="moon"><circle cx="515" cy="62" r="42" fill="url(#moonGlow)"/>'
      '<circle cx="515" cy="62" r="19" fill="#F4F1DE" mask="url(#crescent)"/></g>\n')


def skyline(w):
    xs, x = [], 0
    while x < W:
        bw = random.choice([34, 42, 48, 56, 64])
        bh = random.randint(46, 100)
        xs.append((x, bw, bh))
        x += bw + random.choice([0, 2, 4])
    base = 330
    for layer, fill in (("day", "#7F9BB8"), ("night", "#0E1328")):
        w(f'  <g class="{layer}" fill="{fill}">\n')
        for bx, bw, bh in xs:
            w(f'    <rect x="{bx}" y="{base-bh}" width="{bw}" height="{bh}"/>\n')
        w('  </g>\n')
    w('  <g class="day" fill="#B9CCE0">\n')
    wins = []
    for bx, bw, bh in xs:
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 6, bx + bw - 8, 10):
                wins.append((wx, wy))
                w(f'    <rect x="{wx}" y="{wy}" width="5" height="6"/>\n')
    w('  </g>\n  <g class="night" fill="#FFD27A">\n')
    for wx, wy in wins:
        if random.random() < .16:
            d = random.uniform(0, 5)
            w(f'    <rect class="lit" x="{wx}" y="{wy}" width="5" height="6" style="animation-delay:{d:.2f}s"/>\n')
    w('  </g>\n')


def text_block(w, T, c, ink, accent, faint, cls, pixel_tag):
    w(f'  <g class="{cls}">\n')
    w('    ' + T.text("CodeBold", 48, 70, c["clock"], 11.5, faint, extra='letter-spacing="2"') + '\n')
    w('    ' + T.text("Display", 46, 122, NAME, 41, ink, extra='letter-spacing="-.6"') + '\n')
    if pixel_tag:
        w('    ' + pixel(c["tag"], 49, 146, 3, accent)[0] + '\n')
    else:
        w('    ' + T.text("DisplaySemi", 48, 166, c["tag"], 23, accent, extra='letter-spacing="-.2"') + '\n')
    w('    ' + T.text("Body", 48, 197, c["sub"], 14.5, ink, extra='opacity=".82"') + '\n')
    pw = len(c["status"]) * 6.95 + 40
    w(f'    <rect x="48" y="214" width="{pw:.0f}" height="24" rx="12" fill="{ink}" opacity=".1"/>\n')
    w(f'    <circle cx="62" cy="226" r="3.5" fill="{accent}" class="glow"/>\n')
    w('    ' + T.text("Code", 73, 230, c["status"], 11.5, ink) + '\n')
    w('  </g>\n')


def desk(w, T):
    w('  <rect x="0" y="330" width="900" height="50" fill="#B98A5E"/>\n')
    w('  <rect x="0" y="330" width="900" height="5" fill="#D3A677"/>\n')
    w('  <rect class="night" x="0" y="330" width="900" height="50" fill="#2A1C26"/>\n')
    w('  <rect class="night" x="0" y="330" width="900" height="5" fill="#4A3040"/>\n')
    w('  <ellipse class="night" cx="710" cy="336" rx="260" ry="22" fill="url(#lampPool)"/>\n')
    w('  <g transform="translate(470 300)">\n')
    w('    <rect x="0" y="6" width="26" height="26" rx="4" fill="#E9E9E3"/>\n')
    w('    <path d="M26 12 h5 a6 6 0 0 1 0 12 h-5" fill="none" stroke="#E9E9E3" stroke-width="3"/>\n')
    w('    <rect x="4" y="12" width="18" height="3" fill="#C99A3F" opacity=".7"/>\n')
    for i, sx in enumerate((7, 13, 19)):
        w(f'    <path class="steam" style="animation-delay:{i*0.8}s" d="M{sx} 2 q-3 -5 0 -10 q3 -5 0 -10" '
          'fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round"/>\n')
    w('  </g>\n')
    w('  <rect x="700" y="258" width="20" height="70" fill="#2B303B"/>\n')
    w('  <rect x="664" y="324" width="92" height="7" rx="3" fill="#2B303B"/>\n')
    w('  <rect x="560" y="70" width="300" height="192" rx="10" fill="#1B1F2A"/>\n')
    w('  <circle cx="710" cy="255" r="2" fill="#4A5160"/>\n')
    screen_day(w, T)
    screen_night(w, T)


def screen_day(w, T):
    x0, y0 = 572, 82
    w('  <g class="day" clip-path="url(#screen)">\n')
    w(f'    <rect x="{x0}" y="{y0}" width="276" height="166" fill="#0F1620"/>\n')
    w(f'    <rect x="{x0}" y="{y0}" width="276" height="18" fill="#161F2B"/>\n')
    w(f'    <rect x="{x0}" y="{y0}" width="84" height="18" fill="#0F1620"/>\n')
    w(f'    <rect x="{x0}" y="{y0+16}" width="84" height="2" fill="#FF9E64"/>\n')
    w('    ' + T.text("Code", x0 + 10, y0 + 12.5, "deploy.yml", 9, "#B9C4CF") + '\n')
    w('    ' + T.text("Code", x0 + 96, y0 + 12.5, "merge.rs", 9, "#5A6672") + '\n')
    rows = [  # (indent, [(width, colour)])
        (0, [(24, "#C792EA"), (30, "#B9C4CF")]),
        (1, [(30, "#82AAFF"), (54, "#C3E88D")]),
        (0, [(26, "#C792EA")]),
        (1, [(36, "#82AAFF"), (20, "#B9C4CF")]),
        (2, [(28, "#FFCB6B"), (60, "#C3E88D")]),
        (2, [(28, "#FFCB6B"), (44, "#C3E88D")]),
    ]
    y = y0 + 32
    for n, (ind, toks) in enumerate(rows, 1):
        w('    ' + T.text("Code", x0 + 8, y + 4, str(n), 8, "#3B4654") + '\n')
        x = x0 + 26 + ind * 14
        for tw, col in toks:
            w(f'    <rect x="{x}" y="{y-1}" width="{tw}" height="5" rx="2" fill="{col}" opacity=".85"/>\n')
            x += tw + 5
        y += 13
    w('    ' + T.text("Code", x0 + 8, y + 4, "7", 8, "#3B4654") + '\n')
    w(f'    <svg x="{x0+54}" y="{y-5}" height="12" width="150" overflow="hidden">'
      f'<rect class="type" x="0" y="4" width="150" height="5" rx="2" fill="#FFCB6B" opacity=".85"/></svg>\n')
    w(f'    <rect class="caret" x="{x0+206}" y="{y-4}" width="2" height="11" fill="#E9E9E3"/>\n')
    # the pipeline: each stage goes green in turn
    py = y0 + 136
    w(f'    <rect x="{x0}" y="{py-8}" width="276" height="38" fill="#121B26"/>\n')
    sx = x0 + 10
    for i, st in enumerate(STAGES):
        cw = 70
        w(f'    <rect x="{sx}" y="{py}" width="{cw}" height="20" rx="10" fill="#1E2A38"/>\n')
        w(f'    <g class="st{i}"><rect x="{sx}" y="{py}" width="{cw}" height="20" rx="10" fill="#1C3A2A"/>'
          f'<circle cx="{sx+12}" cy="{py+10}" r="3.5" fill="#8FE3A8"/></g>\n')
        w(f'    <circle cx="{sx+12}" cy="{py+10}" r="3.5" fill="none" stroke="#5A6672"/>\n')
        w('    ' + T.text("Code", sx + 22, py + 13.5, st, 9, "#B9C4CF") + '\n')
        if i < len(STAGES) - 1:
            w(f'    <path d="M{sx+cw+3} {py+10}h10" stroke="#3B4654" stroke-width="1.5"/>\n')
        sx += cw + 16
    w('  </g>\n')


def screen_night(w, T):
    x0, y0 = 572, 82
    w('  <g class="night" clip-path="url(#screen)">\n')
    w(f'    <rect x="{x0}" y="{y0}" width="276" height="166" fill="url(#gameSky)"/>\n')
    w('    ' + sprite([".##", "##.", "##.", ".##"], x0 + 246, y0 + 10, 3, {"#": "#F4F1DE"}) + '\n')
    tree = ["..#..", ".###.", ".###.", "#####", "#####", "..#..", "..#.."]
    for tx, s in [(x0+14, 4), (x0+46, 3), (x0+198, 4), (x0+236, 3)]:
        w('    ' + sprite(tree, tx, y0 + 140 - 7 * s, s, {"#": "#1A2A2A"}) + '\n')
    w(f'    <rect x="{x0}" y="{y0+140}" width="276" height="26" fill="#14101F"/>\n')
    w(f'    <rect x="{x0}" y="{y0+140}" width="276" height="3" fill="#2C2440"/>\n')
    # the manor, one window that shouldn't be lit
    mx, my = x0 + 66, y0 + 108
    w(f'    <polygon points="{mx-4},{my} {mx+28},{my-18} {mx+60},{my}" fill="#221A36"/>\n')
    w(f'    <rect x="{mx}" y="{my}" width="56" height="32" fill="#221A36"/>\n')
    w(f'    <rect x="{mx+40}" y="{my-22}" width="6" height="12" fill="#221A36"/>\n')
    for i, (wx, wy) in enumerate([(8, 7), (24, 7), (40, 7), (8, 19), (40, 19)]):
        cls = ' class="lit"' if i == 2 else ""
        fill = "#FFD27A" if i in (2, 3) else "#120E1F"
        w(f'    <rect{cls} x="{mx+wx}" y="{my+wy}" width="7" height="7" fill="{fill}"/>\n')
    w(f'    <rect x="{mx+24}" y="{my+18}" width="8" height="14" fill="#120E1F"/>\n')
    # lantern glow + the watcher
    w(f'    <circle class="glow" cx="{x0+150}" cy="{y0+124}" r="26" fill="url(#lantern)"/>\n')
    watcher = [".AAA.", "AAAAA", "AEAEA", ".AAA.", ".AAA.", ".A.A."]
    w('    <g class="bob">' + sprite(watcher, x0 + 126, y0 + 116, 4, {"A": "#2E2747", "E": "#FFE08A"})
      + sprite(["L", "L"], x0 + 148, y0 + 120, 4, {"L": "#FFD27A"}) + '</g>\n')
    w('    ' + pixel("Watchnight", x0 + 138, y0 + 30, 3, "#E8D8FF", "middle")[0] + '\n')
    w('    ' + T.text("CodeBold", x0 + 138, y0 + 66, "SOCIAL DEDUCTION · HORROR", 7.5, "#9C8FC0", "middle",
                       'letter-spacing="1.6"') + '\n')
    w('    ' + pixel("▶ Press start", x0 + 138, y0 + 80, 2, "#FFD27A", "middle", extra='class="start"')[0] + '\n')
    w('  </g>\n')


def build():
    T = Type()
    body = io.StringIO()
    w = body.write
    w(f'  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>\n')
    w('  <g clip-path="url(#frame)">\n')
    sky(w)
    skyline(w)
    text_block(w, T, DAY, "#12203A", "#C2461C", "#3C4E66", "day", False)
    text_block(w, T, NIGHT, "#EDE8FF", "#FFD27A", "#9C8FC0", "night", True)
    desk(w, T)
    w('  </g>\n</svg>\n')

    s = io.StringIO()
    w = s.write
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'role="img" aria-label="{ALT}">\n')
    w(f'  <title>{ALT}</title>\n')
    w('  <defs>\n')
    w('    <linearGradient id="skyDay" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#9CCBFF"/><stop offset=".7" stop-color="#FFE6C2"/>'
      '<stop offset="1" stop-color="#FFC9A0"/></linearGradient>\n')
    w('    <linearGradient id="skyNight" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#060A18"/><stop offset=".75" stop-color="#1B1840"/>'
      '<stop offset="1" stop-color="#3A2453"/></linearGradient>\n')
    w('    <linearGradient id="gameSky" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#0B0716"/><stop offset="1" stop-color="#2A1A45"/></linearGradient>\n')
    w('    <radialGradient id="sunGlow"><stop offset=".4" stop-color="#FFD166" stop-opacity=".45"/>'
      '<stop offset="1" stop-color="#FFD166" stop-opacity="0"/></radialGradient>\n')
    w('    <radialGradient id="moonGlow"><stop offset=".35" stop-color="#F4F1DE" stop-opacity=".18"/>'
      '<stop offset="1" stop-color="#F4F1DE" stop-opacity="0"/></radialGradient>\n')
    w('    <radialGradient id="lantern"><stop offset="0" stop-color="#FFD27A" stop-opacity=".55"/>'
      '<stop offset="1" stop-color="#FFD27A" stop-opacity="0"/></radialGradient>\n')
    w('    <radialGradient id="lampPool"><stop offset="0" stop-color="#8FA8FF" stop-opacity=".22"/>'
      '<stop offset="1" stop-color="#8FA8FF" stop-opacity="0"/></radialGradient>\n')
    w('    <mask id="crescent"><rect width="900" height="380" fill="#fff"/>'
      '<circle cx="524" cy="55" r="17" fill="#000"/></mask>\n')
    w('    <clipPath id="screen"><rect x="572" y="82" width="276" height="166" rx="3"/></clipPath>\n')
    w('  </defs>\n')
    w(f'  <style>\n    {T.css()}{css()}\n  </style>\n')
    return s.getvalue() + body.getvalue()


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
    out.write_text(build(), encoding="utf-8")
    print(out.name, out.stat().st_size, "bytes")
