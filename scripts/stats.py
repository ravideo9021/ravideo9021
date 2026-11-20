#!/usr/bin/env python3
"""Generates assets/activity.svg from live GitHub data.

Runs daily in .github/workflows/activity.yml. Locally:
    GITHUB_TOKEN=$(gh auth token) python3 scripts/stats.py
"""
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

from common import DIM, INK, MUTED, esc, frame, svg, write

USER = os.environ.get("GH_USER", "ravideo9021")
EXCLUDE_LANGS = {"Jupyter Notebook", "HTML", "Makefile", "Dockerfile", "Shell", "Mermaid"}
LANG_COLORS = {"TypeScript": "#0A84FF", "Python": "#FFD60A", "JavaScript": "#FF9F0A", "C++": "#FF375F",
               "C": "#BF5AF2", "CSS": "#64D2FF", "Go": "#30D158", "Rust": "#FF6B3D"}
FALLBACK = ["#30D158", "#5E5CE6", "#FF6482", "#40C8E0"]
LEVELS = ["#FFFFFF10", "#15456F", "#1F74C6", "#3D9BFF", "#7FDBFF"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t:
        return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json", "User-Agent": "profile-activity-card"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
    except urllib.error.URLError:  # e.g. a local Python without CA certs — fall back to the gh CLI
        out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={USER}"],
                             capture_output=True, text=True, check=True).stdout
        data = json.loads(out)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if counts and counts[i] == 0:  # today not yet counted — don't break the streak
        i -= 1
    while i >= 0 and counts[i]:
        cur += 1
        i -= 1
    return cur, longest


def build(u):
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    cur, longest = streaks(days)
    active = sum(1 for d in days if d["contributionCount"])
    busiest = max(days, key=lambda d: d["contributionCount"])

    sizes = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            n = e["node"]["name"]
            if n not in EXCLUDE_LANGS:
                sizes[n] = sizes.get(n, 0) + e["size"]
    total = sum(sizes.values()) or 1
    langs = sorted(sizes.items(), key=lambda kv: -kv[1])
    top = langs[:5]
    other = sum(v for _, v in langs[5:])
    if other:
        top.append(("Other", other))

    W, H = 1200, 540
    P = 48
    defs, bg, fg = frame(0, 0, W, H, "#30D158", "#0A84FF", rx=28, glow=(0, 0), strength=.22)
    defs += """<linearGradient id="num" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#B4B4C4"/></linearGradient>
<clipPath id="barClip"><rect x="48" y="434" width="1104" height="12" rx="6"/></clipPath>"""

    # stat tiles
    tiles = [
        ("CONTRIBUTIONS", f"{cal['totalContributions']:,}", "in the last year", "#30D158"),
        ("CURRENT STREAK", f"{cur}", "day" + ("" if cur == 1 else "s") + " in a row", "#64D2FF"),
        ("LONGEST STREAK", f"{longest}", "days · best run", "#BF5AF2"),
        ("ACTIVE DAYS", f"{active}", f"busiest: {busiest['contributionCount']} on {dt.date.fromisoformat(busiest['date']):%b %d}", "#FF9F0A"),
    ]
    tw = (W - 2 * P - 3 * 16) / 4
    body = bg
    for i, (lab, val, cap, col) in enumerate(tiles):
        x = P + i * (tw + 16)
        body += (f'<rect x="{x:.1f}" y="44" width="{tw:.1f}" height="132" rx="20" fill="#fff" fill-opacity=".035" stroke="#fff" stroke-opacity=".08"/>'
                 f'<circle cx="{x + 24:.1f}" cy="72" r="4" fill="{col}"/>'
                 f'<text x="{x + 38:.1f}" y="76.5" class="mono" font-size="11.5" letter-spacing="2" fill="{col}">{lab}</text>'
                 f'<text x="{x + 22:.1f}" y="136" font-size="50" font-weight="700" letter-spacing="-2" fill="url(#num)">{esc(val)}</text>'
                 f'<text x="{x + 24:.1f}" y="160" font-size="14" fill="{DIM}">{esc(cap)}</text>')

    # heatmap
    cell, gap = 16, 4.8
    n = len(weeks)
    grid_w = n * (cell + gap) - gap
    gx = (W - grid_w) / 2
    gy = 236
    body += f'<text x="{P}" y="218" class="mono" font-size="11.5" letter-spacing="2" fill="{MUTED}">CONTRIBUTION GRAPH</text>'
    body += f'<text x="{P + 186}" y="218" class="mono" font-size="11.5" fill="{DIM}">· updated {dt.date.today():%b %d, %Y}</text>'
    lvl = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
    last_month = None
    cells = []
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            date = dt.date.fromisoformat(d["date"])
            wd = (date.weekday() + 1) % 7  # Sunday = 0
            L = lvl.get(d["contributionLevel"], 0)
            x, y = gx + wi * (cell + gap), gy + wd * (cell + gap)
            delay = f' style="animation-delay:{wi * 0.018:.3f}s"'
            cells.append(f'<rect class="c"{delay} x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="4.5" fill="{LEVELS[L]}"/>')
        first = dt.date.fromisoformat(w["contributionDays"][0]["date"])
        if first.month != last_month and first.day <= 7 and wi < n - 1:
            cells.append(f'<text x="{gx + wi * (cell + gap):.1f}" y="{gy + 7 * (cell + gap) + 14:.1f}" class="mono" font-size="11" fill="{DIM}">{first:%b}</text>')
            last_month = first.month
    body += "".join(cells)
    lx = W - P - 5 * 16 - 34
    body += f'<text x="{lx - 10}" y="218" text-anchor="end" class="mono" font-size="11" fill="{DIM}">less</text>'
    for i, c in enumerate(LEVELS):
        body += f'<rect x="{lx + i * 16}" y="207.5" width="12" height="12" rx="3.5" fill="{c}"/>'
    body += f'<text x="{lx + 5 * 16 + 4}" y="218" class="mono" font-size="11" fill="{DIM}">more</text>'

    # language bar
    body += f'<text x="{P}" y="418" class="mono" font-size="11.5" letter-spacing="2" fill="{MUTED}">LANGUAGES</text>'
    body += f'<text x="{W - P}" y="418" text-anchor="end" class="mono" font-size="11.5" fill="{DIM}">{u["repositories"]["totalCount"]} public repos</text>'
    body += '<g clip-path="url(#barClip)" class="bar"><rect x="48" y="434" width="1104" height="12" fill="#fff" fill-opacity=".06"/>'
    x = 48.0
    fb = iter(FALLBACK)
    colors = {}
    for name, size in top:
        colors[name] = "#636366" if name == "Other" else LANG_COLORS.get(name) or next(fb, "#8E8E93")
        w = 1104 * size / total
        body += f'<rect x="{x:.1f}" y="434" width="{max(w - 2, 1):.1f}" height="12" fill="{colors[name]}"/>'
        x += w
    body += "</g>"
    lx = P
    for name, size in top:
        pct = f"{100 * size / total:.1f}%"
        body += (f'<circle cx="{lx + 5}" cy="{482}" r="5" fill="{colors[name]}"/>'
                 f'<text x="{lx + 18}" y="487" font-size="15" font-weight="600" fill="{INK}">{esc(name)}</text>'
                 f'<text x="{lx + 18 + len(name) * 8.6 + 8:.0f}" y="487" class="mono" font-size="12.5" fill="{DIM}">{pct}</text>')
        lx += 18 + len(name) * 8.6 + 8 + len(pct) * 7.6 + 34
    body += fg

    style = """
.c{animation:pop .6s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:center;}
@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
.bar{animation:bar 1.4s .4s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:left;}
@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}
"""
    return svg(W, H, body, defs, style, title=f"{cal['totalContributions']} contributions in the last year; current streak {cur} days; longest {longest} days")


if __name__ == "__main__":
    write("activity.svg", build(fetch()))
