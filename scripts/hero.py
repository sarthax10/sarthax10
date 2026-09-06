#!/usr/bin/env python3
"""Render assets/hero-{dark,light}.svg. Edit the copy/geometry constants
below and re-run:  python3 scripts/hero.py
"""
import io, pathlib

THEMES = {
    "dark": dict(
        bg="#0D1117", glowstop="#2F6BA8", glowop="0.16",
        ink="#E9E9E3", muted="#7D8A99", gold="#C99A3F",
        panel="#141C26", rule="#232C38", line="#7D8A99",
        title="#B9C4CF",
    ),
    "light": dict(
        bg="#FFFFFF", glowstop="#2F6BA8", glowop="0.07",
        ink="#16202B", muted="#5A6672", gold="#8A6516",
        panel="#F3F6F9", rule="#DCE3EA", line="#5A6672",
        title="#3C4854",
    ),
}

# --- geometry -------------------------------------------------------------
W, H = 900, 300
PAD = 48
TILES = [  # x, y, w, h, n_content_lines
    (600, 66, 118, 168, 6),
    (727, 66, 125, 80, 3),
    (727, 155, 58, 79, 2),
    (794, 155, 58, 79, 2),
]
EYEBROW = "SOFTWARE ENGINEER · BENGALURU, INDIA"
NAME = "Shreyansh Sarthak"
LEDE = "I build systems from the protocol up."
SUB = "RUST · C# · PYTHON"

NAME_LEN, LEDE_LEN, EYE_LEN, SUB_LEN = 449, 400, 335, 167
CARET_X = PAD + LEDE_LEN + 9
RULE_LEN = W - 2 * PAD

ALT = ("Shreyansh Sarthak — software engineer in Bengaluru, India. "
       "I build systems from the protocol up. Rust, C#, Python.")


def content_lines(x, y, w, h, n, t):
    """Window-content lines inside a tile: first one is a brighter 'title'."""
    out = []
    inset = 16 if w > 90 else 12
    lx = x + inset
    ly = y + inset + 8
    avail = w - inset * 2
    widths = [0.62, 0.88, 0.74, 0.93, 0.58, 0.81, 0.70, 0.86]
    for i in range(n):
        ww = round(avail * widths[i % len(widths)], 1)
        cls = "tt" if i == 0 else "tl"
        out.append(f'<rect class="{cls}" x="{lx}" y="{ly}" width="{ww}" height="4" rx="2"/>')
        ly += 14
    return "\n      ".join(out)


def build(theme_name):
    t = THEMES[theme_name]
    s = io.StringIO()
    w = s.write

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'role="img" aria-label="{ALT}">\n')
    w(f'  <title>{ALT}</title>\n')

    # defs
    w('  <defs>\n')
    w('    <radialGradient id="halo" cx="0.82" cy="0.38" r="0.62">\n')
    w(f'      <stop offset="0" stop-color="{t["glowstop"]}" stop-opacity="{t["glowop"]}"/>\n')
    w(f'      <stop offset="1" stop-color="{t["glowstop"]}" stop-opacity="0"/>\n')
    w('    </radialGradient>\n')
    w('    <filter id="focusglow" x="-60%" y="-60%" width="220%" height="220%">\n')
    w(f'      <feDropShadow dx="0" dy="0" stdDeviation="4.5" flood-color="{t["gold"]}" flood-opacity="0.5"/>\n')
    w('    </filter>\n')
    w('  </defs>\n')

    # styles
    w('  <style>\n')
    w('    .m{font-family:ui-monospace,"SFMono-Regular","SF Mono","Cascadia Mono",'
      '"Roboto Mono","Liberation Mono",Menlo,Consolas,monospace}\n')
    w(f'    .eyebrow{{font-size:11.5px;letter-spacing:2.4px;font-weight:500;fill:{t["muted"]}}}\n')
    w(f'    .name{{font-size:44px;font-weight:600;fill:{t["ink"]}}}\n')
    w(f'    .lede{{font-size:18px;font-weight:500;fill:{t["gold"]}}}\n')
    w(f'    .sub{{font-size:11.5px;letter-spacing:2.4px;font-weight:500;fill:{t["title"]}}}\n')
    w(f'    .tile{{fill:{t["panel"]};stroke:{t["rule"]};stroke-width:1}}\n')
    w(f'    .tl{{fill:{t["line"]};opacity:.26}}\n')
    w(f'    .tt{{fill:{t["title"]};opacity:.55}}\n')
    w(f'    .lit{{fill:{t["gold"]};opacity:0}}\n')
    w(f'    .ring{{fill:none;stroke:{t["gold"]};stroke-width:1.5;opacity:0;filter:url(#focusglow)}}\n')
    w(f'    .caret{{fill:{t["gold"]};animation:blink 1.15s steps(1,end) infinite}}\n')
    w(f'    .rule{{stroke:{t["gold"]};stroke-width:1;opacity:.34;stroke-dasharray:{RULE_LEN};'
      f'stroke-dashoffset:{RULE_LEN};animation:draw 1.5s .25s cubic-bezier(.22,.61,.36,1) forwards}}\n')
    w('    .ring,.lit{animation:focus 13s ease-in-out infinite}\n')
    w('    .lit{animation-name:focusfill}\n')
    for i in range(4):
        w(f'    #r{i+1},#l{i+1}{{animation-delay:{i*3.25:.2f}s}}\n')
    w('    @keyframes draw{to{stroke-dashoffset:0}}\n')
    w('    @keyframes blink{0%,48%{opacity:1}52%,100%{opacity:0}}\n')
    w('    @keyframes focus{0%{opacity:0}3%{opacity:1}22%{opacity:1}25%{opacity:0}100%{opacity:0}}\n')
    w('    @keyframes focusfill{0%{opacity:0}3%{opacity:.07}22%{opacity:.07}25%{opacity:0}100%{opacity:0}}\n')
    w('    @media (prefers-reduced-motion:reduce){\n')
    w('      .caret,.ring,.lit,.rule{animation:none}\n')
    w(f'      .caret{{opacity:1}} .rule{{stroke-dashoffset:0}}\n')
    w('      #r1{opacity:1} #l1{opacity:.07}\n')
    w('    }\n')
    w('  </style>\n\n')

    # ground
    w(f'  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>\n')
    w(f'  <rect width="{W}" height="{H}" fill="url(#halo)"/>\n\n')

    # tiles
    w('  <g aria-hidden="true">\n')
    for i, (x, y, tw, th, n) in enumerate(TILES, 1):
        w(f'    <g>\n')
        w(f'      <rect class="tile" x="{x}" y="{y}" width="{tw}" height="{th}" rx="5"/>\n')
        w(f'      {content_lines(x, y, tw, th, n, t)}\n')
        w(f'      <rect id="l{i}" class="lit" x="{x}" y="{y}" width="{tw}" height="{th}" rx="5"/>\n')
        w(f'      <rect id="r{i}" class="ring" x="{x+0.75}" y="{y+0.75}" '
          f'width="{tw-1.5}" height="{th-1.5}" rx="4.5"/>\n')
        w(f'    </g>\n')
    w('  </g>\n\n')

    # text
    w(f'  <text class="m eyebrow" x="{PAD}" y="86" textLength="{EYE_LEN}" '
      f'lengthAdjust="spacing">{EYEBROW}</text>\n')
    w(f'  <text class="m name" x="{PAD}" y="140" textLength="{NAME_LEN}" '
      f'lengthAdjust="spacing">{NAME}</text>\n')
    w(f'  <text class="m lede" x="{PAD}" y="180" textLength="{LEDE_LEN}" '
      f'lengthAdjust="spacing">{LEDE}</text>\n')
    w(f'  <rect class="caret" x="{CARET_X}" y="166" width="9" height="18" rx="1"/>\n')
    w(f'  <text class="m sub" x="{PAD}" y="210" textLength="{SUB_LEN}" '
      f'lengthAdjust="spacing">{SUB}</text>\n\n')

    # rule
    w(f'  <line class="rule" x1="{PAD}" y1="252" x2="{W-PAD}" y2="252"/>\n')
    w('</svg>\n')
    return s.getvalue()


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name in THEMES:
        f = out / f"hero-{name}.svg"
        f.write_text(build(name), encoding="utf-8")
        print(f, f.stat().st_size, "bytes")
