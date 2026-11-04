#!/usr/bin/env python3
"""Render assets/languages.svg from the language bytes of every public, non-fork
repository on the account. Run it by hand, or let .github/workflows/languages.yml
run it weekly.

    GITHUB_TOKEN=... python3 scripts/languages.py

It uses only the standard library and system fonts, so CI needs nothing installed.
"""
import collections, json, os, pathlib, urllib.request
from xml.sax.saxutils import escape

USER = "sarthax10"
TOP_N = 5
API = "https://api.github.com"

W, PAD = 900, 44
INK, RED, PAPER, WHITE = "#141216", "#CC1126", "#F3EDE1", "#FFFFFF"
COLORS = [RED, INK, "#8F0B1B", "#5A5560", "#B5A88F", "#E0D4BC"]
DISPLAY = "'Arial Black','Segoe UI Black',Impact,system-ui,sans-serif"
TEXT = "'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"


def api(path):
    req = urllib.request.Request(API + path, headers={"Accept": "application/vnd.github+json", "User-Agent": USER})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    totals = collections.Counter()
    page = 1
    while True:
        repos = api(f"/users/{USER}/repos?per_page=100&type=owner&page={page}")
        if not repos:
            return totals
        for repo in repos:
            if not repo["fork"] and not repo["private"]:
                totals.update(api(f"/repos/{USER}/{repo['name']}/languages"))
        page += 1


def segments(totals):
    total = sum(totals.values())
    ranked = totals.most_common()
    head, tail = ranked[:TOP_N], ranked[TOP_N:]
    rows = [(name, 100 * n / total) for name, n in head]
    if tail:
        rows.append(("Other", 100 * sum(n for _, n in tail) / total))
    return rows


def render(rows):
    bar_x, bar_y, bar_w, bar_h = PAD, 118, W - 2 * PAD, 40
    label = ", ".join(f"{n} {p:.0f}%" for n, p in rows)
    row_count = (len(rows) + 2) // 3
    H = 186 + row_count * 38 + 30
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Languages across my public repositories: {escape(label)}">',
         f'<title>Languages across my public repositories: {escape(label)}</title>',
         f'<g transform="rotate(-.5 {W/2} {H/2})">',
         f'<rect x="20" y="24" width="{W-40}" height="{H-48}" fill="#14121633" transform="translate(5 7)"/>',
         f'<rect x="20" y="24" width="{W-40}" height="{H-48}" fill="{PAPER}"/>',
         f'<rect x="{W/2-52}" y="10" width="104" height="30" fill="#E9D79A" fill-opacity=".8" transform="rotate(-3 {W/2} 25)"/>',
         f'<text x="{PAD}" y="88" fill="{INK}" font-family="{DISPLAY}" font-size="31" font-weight="900">What my repos are made of</text>']
    x = bar_x
    for i, (name, pct) in enumerate(rows):
        w = bar_w * pct / 100
        o.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{max(w - 3, 1):.1f}" height="{bar_h}" fill="{COLORS[i % 6]}"/>')
        x += w
    col = bar_w / 3
    for i, (name, pct) in enumerate(rows):
        cx, cy = PAD + (i % 3) * col, 184 + (i // 3) * 38
        o.append(f'<rect x="{cx:.1f}" y="{cy}" width="18" height="18" fill="{COLORS[i % 6]}" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<text x="{cx + 28:.1f}" y="{cy + 15}" fill="{INK}" font-family="{TEXT}" font-size="19" font-weight="700">{escape(name)} <tspan font-weight="400">{pct:.1f}%</tspan></text>')
    o += ['</g>', '</svg>']
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    data = segments(collect())
    out = pathlib.Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    (out / "languages.svg").write_text(render(data), encoding="utf-8")
    print(", ".join(f"{n} {p:.1f}%" for n, p in data))
