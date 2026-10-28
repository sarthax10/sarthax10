#!/usr/bin/env python3
"""Render assets/languages-{dark,light}.svg from the language bytes of every
public, non-fork repository on the account. Run it by hand, or let
.github/workflows/languages.yml run it weekly.

    GITHUB_TOKEN=... python3 scripts/languages.py
"""
import json, os, sys, urllib.request, collections, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

USER = "sarthax10"
TOP_N = 5
API = "https://api.github.com"

# --- design system --------------------------------------------------------
# Pixel font only (drawn in brand.py), so CI needs no font files.
from brand import DAY, NIGHT, pixel, pixel_width

W, H, PAD = 900, 168, 32
BLOCKS = 60  # the bar is drawn as chunky XP blocks
THEME = {"dark": NIGHT, "light": DAY}
PALETTE = {
    "dark":  ["#FFD27A", "#B79CFF", "#FF9E64", "#7FD1B9", "#82AAFF", "#5A5078"],
    "light": ["#D9542B", "#2C6FBB", "#C7891A", "#2E9478", "#7A4FC4", "#B7A88F"],
}


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
    C, pal = THEME[theme], PALETTE[theme]
    label = " · ".join(f"{n} {p:.0f}%" for n, p in rows)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="XP by language across public repositories: {label}">',
         f'  <title>XP by language across public repositories: {label}</title>',
         '  <style>',
         '    .blk{animation:pop .2s steps(1,end) backwards}',
         '    @keyframes pop{from{opacity:0}}',
         '    @media (prefers-reduced-motion:reduce){.blk{animation:none}}',
         '  </style>',
         f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{C["bg"]}" stroke="{C["rule"]}" stroke-width="1.5"/>',
         '  ' + pixel("XP by language", PAD, 28, 2, C["muted"])[0],
         '  ' + pixel("all public repos", W - PAD, 28, 2, C["muted"], "end")[0]]

    # allot blocks by largest remainder so they always sum to BLOCKS
    raw = [p * BLOCKS / 100 for _, p in rows]
    n = [int(r) for r in raw]
    for i in sorted(range(len(rows)), key=lambda i: raw[i] - n[i], reverse=True)[:BLOCKS - sum(n)]:
        n[i] += 1
    bw = (W - 2 * PAD) / BLOCKS
    x, k = PAD, 0
    for i, cnt in enumerate(n):
        for _ in range(cnt):
            o.append(f'  <rect class="blk" style="animation-delay:{k*0.018:.3f}s" x="{x+1:.1f}" y="54" '
                     f'width="{bw-3:.1f}" height="22" rx="2" fill="{pal[i]}"/>')
            x += bw
            k += 1

    colw = (W - 2 * PAD) / 3
    for i, (name, pct) in enumerate(rows):
        cx, cy = PAD + (i % 3) * colw, 100 + (i // 3) * 30
        o.append(f'  <rect x="{cx:.1f}" y="{cy}" width="14" height="14" rx="3" fill="{pal[i]}"/>')
        nm, nw = pixel(name, cx + 26, cy, 2, C["ink"])
        o.append('  ' + nm)
        o.append('  ' + pixel(f"{pct:.1f}%", cx + colw - 24, cy, 2, C["muted"], "end")[0])

    o.append('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    rows = segments(collect())
    out = pathlib.Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for theme in ("dark", "light"):
        (out / f"languages-{theme}.svg").write_text(render(rows, theme), encoding="utf-8")
    print(" · ".join(f"{n} {p:.1f}%" for n, p in rows))
