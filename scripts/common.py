"""Shared design tokens + SVG helpers for the profile artwork."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

BG = "#07070B"
INK = "#F5F5F7"
MUTED = "#A1A1AA"
DIM = "#71717A"


def esc(s: str) -> str:
    return escape(s, quote=True)


GRAIN = """
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/>
  <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .09 0"/>
</filter>"""


def svg(w, h, body, defs="", style="", title=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img">
{t}<style>
text{{font-family:{FONT};}}
.mono{{font-family:{MONO};}}
{style}
@media (prefers-reduced-motion: reduce){{*{{animation-duration:0s!important;animation-iteration-count:1!important;}}}}
</style>
<defs>{GRAIN}{defs}</defs>
{body}
</svg>
"""


def frame(x, y, w, h, a1, a2, sid="", rx=28, glow=(0.85, 0.0), strength=0.34):
    """A glass-on-black card: returns (defs, background, foreground)."""
    s = sid
    defs = f"""
<linearGradient id="stroke{s}" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity=".24"/><stop offset=".45" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity=".04"/>
</linearGradient>
<radialGradient id="glow{s}" cx="{glow[0]}" cy="{glow[1]}" r=".95">
  <stop offset="0" stop-color="{a1}" stop-opacity="{strength}"/><stop offset=".42" stop-color="{a2}" stop-opacity="{strength * .3:.3f}"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="acc{s}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
<linearGradient id="hl{s}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="surf{s}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111118"/><stop offset="1" stop-color="#09090D"/></linearGradient>
<clipPath id="clip{s}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>"""
    bg = f"""<g clip-path="url(#clip{s})">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#surf{s})"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#glow{s})"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#grain)" opacity=".55"/>
</g>"""
    fg = f"""<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{rx - .5}" stroke="url(#stroke{s})"/>
<rect x="{x + w * .18:.1f}" y="{y}" width="{w * .64:.1f}" height="1" fill="url(#hl{s})"/>"""
    return defs, bg, fg


def text_w(s, size, mono=False, spacing=0.0, weight=500):
    """Rough advance-width estimate (SF Pro / Segoe UI metrics)."""
    if mono:
        return len(s) * (size * 0.6 + spacing)
    factor = 0.56 if weight >= 600 else 0.53
    narrow = sum(1 for c in s if c in "iljtfrI.,:;'|! ")
    wide = sum(1 for c in s if c in "mwMW@")
    return (len(s) * factor + wide * 0.25 - narrow * 0.22) * size + len(s) * spacing


def chip(x, y, label, size=14, h=32, dot=None, fill=".06", stroke=".11", color="#D4D4D8"):
    pad = 14
    dot_w = 16 if dot else 0
    w = text_w(label, size) + pad * 2 + dot_w
    parts = [f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="#fff" fill-opacity="{fill}" stroke="#fff" stroke-opacity="{stroke}"/>']
    tx = x + pad
    if dot:
        parts.append(f'<circle cx="{x + pad + 4}" cy="{y + h / 2}" r="4" fill="{dot}"/>')
        tx += dot_w
    parts.append(f'<text x="{tx:.1f}" y="{y + h / 2 + size * .36:.1f}" font-size="{size}" font-weight="500" fill="{color}">{esc(label)}</text>')
    return "".join(parts), w


def write(name, content):
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8")
    print(f"  wrote assets/{name}  ({len(content.encode()) / 1024:.1f} KB)")
