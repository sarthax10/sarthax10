#!/usr/bin/env python3
"""Render assets/languages-{dark,light}.svg from the language bytes of every
public, non-fork repository on the account. Run it by hand, or let
.github/workflows/languages.yml run it weekly.

    GITHUB_TOKEN=... python3 scripts/languages.py
"""
import json, os, urllib.request, collections, pathlib

USER = "sarthax10"
TOP_N = 5
API = "https://api.github.com"

# --- design system --------------------------------------------------------
W, BAR_Y, BAR_H, GAP = 560, 16, 10, 3
COL_X = (0, 192, 384)
ROW_Y = (56, 84)

PALETTE = {                       # warm / cool alternating, brand-derived
    "dark":  ["#C99A3F", "#6E8FB8", "#B4763A", "#4E6C8E", "#7D8A99", "#39434F"],
    "light": ["#9A7222", "#4A6F9B", "#8A5626", "#35506D", "#5A6672", "#9AA7B4"],
}
INK   = {"dark": "#B9C4CF", "light": "#3C4854"}
MUTED = {"dark": "#7D8A99", "light": "#5A6672"}

MONO = ('ui-monospace,"SFMono-Regular","SF Mono","Cascadia Mono",'
        '"Roboto Mono","Liberation Mono",Menlo,Consolas,monospace')


def api(path):
    req = urllib.request.Request(API + path,
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": USER})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    totals = collections.Counter()
    page = 1
    while True:
        repos = api(f"/users/{USER}/repos?per_page=100&type=owner&page={page}")
        if not repos:
            break
        for repo in repos:
            if repo["fork"] or repo["private"]:
                continue
            totals.update(api(f"/repos/{USER}/{repo['name']}/languages"))
        page += 1
    return totals


def segments(totals):
    total = sum(totals.values())
    ranked = totals.most_common()
    head, tail = ranked[:TOP_N], ranked[TOP_N:]
    out = [(name, 100 * n / total) for name, n in head]
    if tail:
        out.append(("Other", 100 * sum(n for _, n in tail) / total))
    return out


def render(rows, theme):
    pal, ink, muted = PALETTE[theme], INK[theme], MUTED[theme]
    usable = W - GAP * (len(rows) - 1)
    label = " · ".join(f"{n} {p:.0f}%" for n, p in rows)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 100" '
         f'width="{W}" height="100" role="img" '
         f'aria-label="Language distribution across public repositories: {label}">',
         f'  <title>Language distribution across public repositories — {label}</title>',
         '  <style>',
         f'    text{{font-family:{MONO}}}',
         f'    .pct{{font-size:12px;font-weight:600;fill:{ink}}}',
         f'    .lbl{{font-size:11px;font-weight:500;fill:{ink};opacity:.72}}',
         '    .seg{transform-origin:left center;animation:grow .9s cubic-bezier(.22,.61,.36,1) backwards}',
         '    @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}',
         '    @media (prefers-reduced-motion:reduce){.seg{animation:none}}',
         '  </style>']

    x = 0
    for i, (name, pct) in enumerate(rows):
        w = usable * pct / 100
        o.append(f'  <rect class="seg" x="{x:.1f}" y="{BAR_Y}" width="{w:.1f}" '
                 f'height="{BAR_H}" rx="{BAR_H/2}" fill="{pal[i]}" '
                 f'style="animation-delay:{i*0.07:.2f}s"/>')
        x += w + GAP

    for i, (name, pct) in enumerate(rows):
        cx, cy = COL_X[i % 3], ROW_Y[i // 3]
        o.append(f'  <rect x="{cx}" y="{cy-8}" width="9" height="9" rx="2.5" fill="{pal[i]}"/>')
        o.append(f'  <text class="pct" x="{cx+17}" y="{cy}">{pct:.1f}%</text>')
        o.append(f'  <text class="lbl" x="{cx+63}" y="{cy}">{name}</text>')

    o.append('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    rows = segments(collect())
    out = pathlib.Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for theme in ("dark", "light"):
        (out / f"languages-{theme}.svg").write_text(render(rows, theme), encoding="utf-8")
    print(" · ".join(f"{n} {p:.1f}%" for n, p in rows))
