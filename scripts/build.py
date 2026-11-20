#!/usr/bin/env python3
"""Builds the static artwork for the profile README.

    python3 scripts/build.py

Edit the content blocks below (PROJECTS, STACK, ...) and re-run.
The activity card is generated separately by scripts/stats.py (daily, via Actions).
"""
from common import BG, DIM, INK, MONO, MUTED, chip, esc, frame, svg, text_w, write

# ───────────────────────────── content ─────────────────────────────

NAME = "Ravi Deo"
EYEBROW = "AI ENGINEER · CS · GREATER NOIDA, IN"
TAGLINE = ["Building intelligent systems that see,", "reason and act — from on-device vision to agents."]
NOW = [
    "Soma — an AI digital twin for your lifestyle",
    "SignSpeak — real-time ASL, fully on-device",
    "ResLand — learning to land drones on moving decks",
]

PROJECTS = [
    dict(slug="soma", repo="ai-digital-twin-lifestyle", kicker="HEALTH AI", title="Soma",
         desc=["A living digital twin of you — predicts sleep,", "nutrition, activity & stress issues early."],
         tags=["TypeScript", "React 19", "Predictive ML"], a1="#30D158", a2="#64D2FF", motif="pulse"),
    dict(slug="signspeak", repo="signspeak", kicker="COMPUTER VISION", title="SignSpeak",
         desc=["ASL word signs + fingerspelling from your camera,", "recognised in the browser. Nothing leaves device."],
         tags=["Next.js", "MediaPipe", "PyTorch TCN"], a1="#BF5AF2", a2="#FF6482", motif="hand"),
    dict(slug="resland", repo="uav-residual-control", kicker="RESEARCH · ROBOTICS", title="ResLand",
         desc=["Residual compensation for UAV landing on moving", "platforms under ground-effect disturbance."],
         tags=["Python", "Control", "Simulation"], a1="#FFD60A", a2="#FF9F0A", motif="drone"),
    dict(slug="rag", repo="Multilingual-RAG-System", kicker="RETRIEVAL · NLP", title="Multilingual RAG",
         desc=["Hindi ⇄ English cross-lingual retrieval with", "streaming generation. Hinglish welcome."],
         tags=["FastAPI", "FAISS", "LLMs"], a1="#0A84FF", a2="#5E5CE6", motif="rag"),
    dict(slug="analyst", repo="Autonomous-Data-Analyst-LLM-Powered-Agentic-System", kicker="AGENTIC AI", title="Autonomous Analyst",
         desc=["Plans, writes and runs its own analysis code —", "sandboxed, self-correcting, streamed."],
         tags=["Python", "Agents", "Docker"], a1="#FF375F", a2="#FF9F0A", motif="orbit"),
    dict(slug="forecast", repo="sales-forecasting-inventory-ml", kicker="APPLIED ML", title="Demand Forecasting",
         desc=["XGBoost sales forecasting + inventory", "optimisation, in a 6-page Streamlit app."],
         tags=["XGBoost", "pandas", "Streamlit"], a1="#64D2FF", a2="#0A84FF", motif="bars"),
]

STACK = [
    ("LANGUAGES", "#64D2FF", ["Python", "TypeScript", "JavaScript", "C++", "C", "SQL"]),
    ("AI · ML", "#BF5AF2", ["PyTorch", "TensorFlow", "scikit-learn", "XGBoost", "MediaPipe", "FAISS", "LLM Agents", "RAG"]),
    ("PRODUCT", "#30D158", ["Next.js", "React", "Tailwind CSS", "FastAPI", "Streamlit", "Node.js"]),
    ("TOOLING", "#FF9F0A", ["Docker", "Git", "GitHub Actions", "Jupyter", "Vercel", "Linux"]),
]
DOTS = {"Python": "#FFD60A", "TypeScript": "#0A84FF", "JavaScript": "#FFD60A", "C++": "#FF375F", "C": "#8E8E93",
        "SQL": "#64D2FF", "PyTorch": "#FF6B3D", "TensorFlow": "#FF9F0A", "scikit-learn": "#64D2FF",
        "XGBoost": "#30D158", "MediaPipe": "#0A84FF", "OpenCV": "#30D158", "FAISS": "#5E5CE6",
        "LLM Agents": "#BF5AF2", "RAG": "#FF6482", "Next.js": "#F5F5F7", "React": "#64D2FF",
        "Tailwind CSS": "#40C8E0", "FastAPI": "#30D158", "Streamlit": "#FF375F", "Node.js": "#30D158",
        "Docker": "#0A84FF", "Git": "#FF6B3D", "GitHub Actions": "#0A84FF", "Jupyter": "#FF9F0A",
        "Vercel": "#F5F5F7", "Linux": "#FFD60A"}

SECTIONS = [
    ("work", "01", "WORK", "Selected work.", "Things I've built and shipped", "#64D2FF"),
    ("toolkit", "02", "TOOLKIT", "The toolkit.", "What I reach for", "#BF5AF2"),
    ("activity", "03", "ACTIVITY", "In motion.", "Refreshed daily by GitHub Actions", "#30D158"),
]

X_HANDLE = "ravideo9021"
GH_HANDLE = "ravideo9021"

# ───────────────────────────── hero ─────────────────────────────


def hero():
    W, H = 1200, 480
    # perspective floor
    vx, vy, hz = 600, 330, 402
    floor = []
    for i in range(-12, 13):
        xb = 600 + i * 120
        x1 = vx + (xb - vx) * (hz - vy) / (H - vy)
        floor.append(f'<line x1="{x1:.1f}" y1="{hz}" x2="{xb}" y2="{H}"/>')
    yy, step = hz, 3.0
    while yy < H:
        floor.append(f'<line x1="0" y1="{yy:.1f}" x2="{W}" y2="{yy:.1f}"/>')
        step *= 1.45
        yy += step

    # neural net inside the front glass panel (panel-local coords, 340x260)
    layers = [(56, [92, 140, 188]), (170, [76, 118, 160, 202]), (284, [112, 168])]
    edges, pulses = [], []
    k = 0
    for (xa, ya), (xb, yb) in zip(layers, layers[1:]):
        for a in ya:
            for b in yb:
                edges.append(f'<line x1="{xa}" y1="{a}" x2="{xb}" y2="{b}"/>')
                if k % 3 == 0:
                    pulses.append(f'<line class="pulse" style="animation-delay:{(k * .37) % 3:.2f}s" x1="{xa}" y1="{a}" x2="{xb}" y2="{b}" pathLength="100"/>')
                k += 1
    nodes = []
    for li, (x, ys) in enumerate(layers):
        for j, y in enumerate(ys):
            active = li == 2 and j == 0
            if active:
                nodes.append(f'<circle cx="{x}" cy="{y}" r="16" fill="url(#accH)" opacity=".25" class="breathe"/>')
                nodes.append(f'<circle cx="{x}" cy="{y}" r="8" fill="url(#accH)"/>')
            else:
                nodes.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#0C0C14" stroke="#fff" stroke-opacity=".55" stroke-width="1.5"/>')

    def panel(fill_op, stroke_op):
        return (f'<rect width="340" height="260" rx="22" fill="url(#glass)" fill-opacity="{fill_op}" stroke="url(#glassStroke)" stroke-opacity="{stroke_op}"/>')

    front = f"""
    {panel(1, 1)}
    <rect x="70" y="0" width="200" height="1" fill="url(#hlH)"/>
    <circle cx="24" cy="22" r="5" fill="#FF5F57"/><circle cx="42" cy="22" r="5" fill="#FEBC2E"/><circle cx="60" cy="22" r="5" fill="#28C840"/>
    <text x="316" y="26" text-anchor="end" class="mono" font-size="12" fill="{MUTED}">model.forward(x)</text>
    <line x1="0" y1="44" x2="340" y2="44" stroke="#fff" stroke-opacity=".08"/>
    <g stroke="#fff" stroke-opacity=".13" stroke-width="1">{''.join(edges)}</g>
    <g stroke="url(#accH)" stroke-width="2.5" stroke-linecap="round">{''.join(pulses)}</g>
    {''.join(nodes)}
    <text x="284" y="146" text-anchor="middle" class="mono" font-size="11" fill="{INK}" opacity=".9">"hello"</text>
    <line x1="0" y1="222" x2="340" y2="222" stroke="#fff" stroke-opacity=".08"/>
    <text x="24" y="245" class="mono" font-size="11" fill="{DIM}">confidence</text>
    <rect x="112" y="237" width="150" height="6" rx="3" fill="#fff" fill-opacity=".08"/>
    <rect x="112" y="237" width="146" height="6" rx="3" fill="url(#accH)" class="meter"/>
    <text x="316" y="245" text-anchor="end" class="mono" font-size="11" fill="{INK}">0.97</text>"""

    # rotating "now building" lines
    now = "".join(
        f'<text class="rot" style="animation-delay:{i * 4}s" x="214" y="384" font-size="17" font-weight="500" fill="{INK}" fill-opacity=".92">{esc(t)}</text>'
        for i, t in enumerate(NOW))

    pill_w = 52 + text_w(EYEBROW, 12, mono=True, spacing=2.2)

    defs = f"""
<clipPath id="heroClip"><rect width="{W}" height="{H}" rx="32"/></clipPath>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="80"/></filter>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="34" stdDeviation="30" flood-color="#000" flood-opacity=".75"/></filter>
<linearGradient id="nameGrad" x1="0" y1="150" x2="0" y2="250" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#A9A9B8"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="260" y2="0" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-400 0;-400 0;900 0" keyTimes="0;.55;1" dur="7s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="accH" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#64D2FF"/><stop offset="1" stop-color="#BF5AF2"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>
<linearGradient id="glassStroke" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".6" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".18"/></linearGradient>
<linearGradient id="hlH" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".8"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="floorFade" x1="0" y1="{hz}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="floorMask"><rect y="{hz}" width="{W}" height="{H - hz}" fill="url(#floorFade)"/></mask>
<radialGradient id="vignette" cx=".3" cy=".45" r=".9"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".65"/></radialGradient>
<linearGradient id="leftShade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".9"/><stop offset=".55" stop-color="{BG}" stop-opacity=".35"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
<linearGradient id="horizon" x1="0" x2="1"><stop offset="0" stop-color="#64D2FF" stop-opacity="0"/><stop offset=".5" stop-color="#64D2FF" stop-opacity=".6"/><stop offset="1" stop-color="#BF5AF2" stop-opacity="0"/></linearGradient>
<linearGradient id="heroStroke" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity=".04"/></linearGradient>"""

    style = """
.b{transform-box:fill-box;transform-origin:center;}
.b1{animation:d1 18s ease-in-out infinite;} .b2{animation:d2 22s ease-in-out infinite;} .b3{animation:d3 26s ease-in-out infinite;}
@keyframes d1{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-90px,50px) scale(1.15)}}
@keyframes d2{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(70px,-60px) scale(.9)}}
@keyframes d3{0%,100%{transform:translate(0,0)}50%{transform:translate(-60px,-40px)}}
.float{animation:float 7s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.floatB{animation:float 7s ease-in-out infinite;animation-delay:-.6s;}
.floatC{animation:float 7s ease-in-out infinite;animation-delay:-1.2s;}
.pulse{stroke-dasharray:14 200;stroke-dashoffset:14;animation:pulse 3s cubic-bezier(.4,0,.2,1) infinite;}
@keyframes pulse{0%{stroke-dashoffset:14}70%,100%{stroke-dashoffset:-100}}
.breathe{transform-box:fill-box;transform-origin:center;animation:breathe 2.4s ease-in-out infinite;}
@keyframes breathe{0%,100%{transform:scale(.8);opacity:.15}50%{transform:scale(1.25);opacity:.4}}
.meter{transform-box:fill-box;transform-origin:left;animation:meter 3s cubic-bezier(.2,.8,.2,1) infinite;}
@keyframes meter{0%{transform:scaleX(.2)}40%,100%{transform:scaleX(1)}}
.rot{opacity:0;animation:rot 12s cubic-bezier(.2,.8,.2,1) infinite both;}
@keyframes rot{0%{opacity:0;transform:translateY(10px)}4%,30%{opacity:1;transform:translateY(0)}34%,100%{opacity:0;transform:translateY(-10px)}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2s cubic-bezier(0,0,.2,1) infinite;}
@keyframes ping{0%{transform:scale(1);opacity:.7}100%{transform:scale(3.2);opacity:0}}
.rise{animation:rise 1.1s cubic-bezier(.2,.8,.2,1) both;}
.rise2{animation:rise 1.1s .15s cubic-bezier(.2,.8,.2,1) both;}
.rise3{animation:rise 1.1s .3s cubic-bezier(.2,.8,.2,1) both;}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@media (prefers-reduced-motion: reduce){.rot{animation:none;opacity:0}.rot:first-of-type{opacity:1}}
"""

    body = f"""
<g clip-path="url(#heroClip)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g filter="url(#blur)" opacity=".8">
    <circle class="b b1" cx="930" cy="110" r="210" fill="#5E5CE6"/>
    <circle class="b b2" cx="1120" cy="400" r="170" fill="#0A84FF"/>
    <circle class="b b3" cx="700" cy="-30" r="170" fill="#BF5AF2" opacity=".75"/>
    <circle class="b b2" cx="120" cy="520" r="160" fill="#64D2FF" opacity=".25"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#leftShade)"/>
  <g stroke="#fff" stroke-opacity=".09" mask="url(#floorMask)">{''.join(floor)}</g>
  <rect x="0" y="{hz}" width="{W}" height="1" fill="url(#horizon)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".6"/>
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="31.5" stroke="url(#heroStroke)"/>

<g class="rise">
  <rect x="72" y="88" width="{pill_w:.0f}" height="34" rx="17" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".14"/>
  <circle class="ping" cx="92" cy="105" r="4" fill="#30D158"/>
  <circle cx="92" cy="105" r="4" fill="#30D158"/>
  <text x="108" y="109.5" class="mono" font-size="12" letter-spacing="2.2" fill="#D4D4D8">{esc(EYEBROW)}</text>
</g>

<g class="rise2">
  <text x="66" y="232" font-size="108" font-weight="700" letter-spacing="-4.5" fill="url(#nameGrad)">{esc(NAME)}<tspan fill="#64D2FF">.</tspan></text>
  <text x="66" y="232" font-size="108" font-weight="700" letter-spacing="-4.5" fill="url(#sheen)" opacity=".55">{esc(NAME)}</text>
</g>

<g class="rise3">
  <text x="72" y="284" font-size="25" font-weight="500" letter-spacing="-.4" fill="{MUTED}">{esc(TAGLINE[0])}</text>
  <text x="72" y="318" font-size="25" font-weight="500" letter-spacing="-.4" fill="{MUTED}">{esc(TAGLINE[1])}</text>
  <text x="72" y="384" class="mono" font-size="12" letter-spacing="2.2" fill="#64D2FF">NOW BUILDING ›</text>
  {now}
</g>

<g class="floatC" opacity=".35"><g transform="translate(838 86) rotate(-7 170 130)">{panel(.8, .6)}</g></g>
<g class="floatB" opacity=".6"><g transform="translate(814 104) rotate(-4.5 170 130)">{panel(.9, .8)}</g></g>
<g class="float" filter="url(#shadow)"><g transform="translate(790 122) rotate(-2 170 130)">{front}</g></g>
"""
    return svg(W, H, body, defs, style, title=f"{NAME} — {' '.join(TAGLINE)}")


# ───────────────────────────── about (bento) ─────────────────────────────


def about():
    W, H = 1200, 440
    tiles = [  # x, y, w, h, a1, a2, glow
        (0, 0, 700, 440, "#5E5CE6", "#64D2FF", (.95, .05)),
        (720, 0, 480, 210, "#BF5AF2", "#FF6482", (1, 0)),
        (720, 230, 230, 210, "#30D158", "#64D2FF", (1, 0)),
        (970, 230, 230, 210, "#FF9F0A", "#FF375F", (1, 0)),
    ]
    defs, bgs, fgs = "", "", ""
    for i, (x, y, w, h, a1, a2, g) in enumerate(tiles):
        d, b, f = frame(x, y, w, h, a1, a2, sid=str(i), rx=26, glow=g, strength=.30)
        defs += d; bgs += b; fgs += f
    defs += """<linearGradient id="hGrad" x1="0" y1="90" x2="0" y2="190" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#B4B4C4"/></linearGradient>"""

    para = [
        "Final-year CS student who likes turning research ideas",
        "into software that actually runs — sign language read",
        "straight from a webcam, a digital twin that forecasts",
        "your week, and controllers that land drones on decks",
        "that won't sit still.",
    ]
    para_svg = "".join(f'<text x="48" y="{246 + i * 29}" font-size="18" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(para))

    focus = [("#64D2FF", "Computer vision", "on-device perception"),
             ("#BF5AF2", "Agentic AI & RAG", "LLMs that use tools"),
             ("#FFD60A", "Control & robotics", "learning-aided UAV control")]
    focus_svg = ""
    for i, (c, t, s) in enumerate(focus):
        y = 92 + i * 40
        focus_svg += (f'<circle cx="{768}" cy="{y - 6}" r="5" fill="{c}"/><circle cx="768" cy="{y - 6}" r="10" fill="{c}" opacity=".18"/>'
                      f'<text x="788" y="{y}" font-size="17" font-weight="600" fill="{INK}">{esc(t)}</text>'
                      f'<text x="1156" y="{y}" text-anchor="end" class="mono" font-size="12" fill="{DIM}">{esc(s)}</text>')
        if i < 2:
            focus_svg += f'<line x1="768" y1="{y + 15}" x2="1156" y2="{y + 15}" stroke="#fff" stroke-opacity=".06"/>'

    style = """
.ring{transform-box:fill-box;transform-origin:center;animation:ring 3.6s cubic-bezier(0,0,.2,1) infinite;}
@keyframes ring{0%{transform:scale(.3);opacity:.8}100%{transform:scale(1.6);opacity:0}}
.spark{transform-box:fill-box;transform-origin:center;animation:spark 6s ease-in-out infinite;}
@keyframes spark{0%,100%{transform:rotate(0) scale(1)}50%{transform:rotate(45deg) scale(.85)}}
"""
    body = f"""{bgs}
<!-- big tile -->
<text x="48" y="66" class="mono" font-size="12" letter-spacing="2.6" fill="#64D2FF">ABOUT</text>
<text x="46" y="134" font-size="44" font-weight="700" letter-spacing="-1.6" fill="url(#hGrad)">Engineer at the edge of</text>
<text x="46" y="186" font-size="44" font-weight="700" letter-spacing="-1.6" fill="url(#hGrad)">AI, vision &amp; control.</text>
{para_svg}
<line x1="48" y1="388" x2="652" y2="388" stroke="#fff" stroke-opacity=".07"/>
<text x="48" y="414" class="mono" font-size="12" fill="{DIM}">› python · typescript · c++</text>
<text x="652" y="414" text-anchor="end" class="mono" font-size="12" fill="{DIM}">B.Tech CSE · research co-author</text>

<!-- focus -->
<text x="768" y="50" class="mono" font-size="12" letter-spacing="2.6" fill="#BF5AF2">FOCUS</text>
{focus_svg}

<!-- based in -->
<g transform="translate(888 290)">
  <circle r="34" class="ring" stroke="#30D158" stroke-width="1.5"/>
  <circle r="34" class="ring" style="animation-delay:1.2s" stroke="#30D158" stroke-width="1.5"/>
  <circle r="34" class="ring" style="animation-delay:2.4s" stroke="#30D158" stroke-width="1.5"/>
  <circle r="5" fill="#30D158"/>
</g>
<text x="766" y="280" class="mono" font-size="12" letter-spacing="2.6" fill="#30D158">BASED IN</text>
<text x="766" y="384" font-size="26" font-weight="700" letter-spacing="-.6" fill="{INK}">Greater Noida</text>
<text x="766" y="410" class="mono" font-size="12" fill="{DIM}">India · UTC+5:30</text>

<!-- open to -->
<text x="1016" y="280" class="mono" font-size="12" letter-spacing="2.6" fill="#FF9F0A">OPEN TO</text>
<g transform="translate(1150 286)"><path class="spark" d="M0 -18 C2 -4 4 -2 18 0 C4 2 2 4 0 18 C-2 4 -4 2 -18 0 C-4 -2 -2 -4 0 -18Z" fill="url(#acc3)"/></g>
<text x="1016" y="356" font-size="26" font-weight="700" letter-spacing="-.6" fill="{INK}">Collabs &amp;</text>
<text x="1016" y="386" font-size="26" font-weight="700" letter-spacing="-.6" fill="{INK}">research</text>
<text x="1016" y="410" class="mono" font-size="12" fill="{DIM}">DMs open on X</text>
{fgs}"""
    return svg(W, H, body, defs, style, title="About Ravi Deo")


# ───────────────────────────── project cards ─────────────────────────────


def motif(kind):
    """Small animated illustration in a 170x150 box."""
    if kind == "pulse":
        return """
<circle cx="96" cy="72" r="30" stroke="url(#acc)" stroke-opacity=".5"/>
<circle cx="96" cy="72" r="52" stroke="url(#acc)" stroke-opacity=".25"/>
<circle cx="96" cy="72" r="74" stroke="url(#acc)" stroke-opacity=".1"/>
<path class="draw" pathLength="100" d="M0 76 H46 L56 76 L64 40 L76 112 L88 54 L96 76 H170" stroke="url(#acc)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="64" cy="40" r="4" fill="#fff" class="blink"/>"""
    if kind == "hand":
        pts = {"w": (86, 146), "t1": (62, 130), "t2": (44, 112), "t3": (32, 95), "t4": (22, 80),
               "i1": (64, 92), "i2": (58, 64), "i3": (55, 44), "i4": (53, 26),
               "m1": (85, 88), "m2": (85, 57), "m3": (85, 36), "m4": (85, 16),
               "r1": (104, 92), "r2": (108, 64), "r3": (110, 46), "r4": (112, 30),
               "p1": (120, 100), "p2": (128, 80), "p3": (133, 65), "p4": (137, 52)}
        bones = [("w", "t1"), ("t1", "t2"), ("t2", "t3"), ("t3", "t4"), ("w", "i1"), ("i1", "i2"), ("i2", "i3"), ("i3", "i4"),
                 ("i1", "m1"), ("m1", "m2"), ("m2", "m3"), ("m3", "m4"), ("m1", "r1"), ("r1", "r2"), ("r2", "r3"), ("r3", "r4"),
                 ("r1", "p1"), ("w", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4")]
        lines = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}"/>' for a, b in bones)
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="{4 if k.endswith("4") else 3}" fill="{"url(#acc)" if k.endswith("4") else "#fff"}"/>' for k, (x, y) in pts.items())
        c = 'stroke="url(#acc)" stroke-width="2.5" stroke-linecap="round"'
        return f"""
<g class="sway"><g stroke="#fff" stroke-opacity=".45" stroke-width="1.6">{lines}</g>{dots}</g>
<path d="M8 22 V6 H24" {c}/><path d="M146 6 H162 V22" {c}/><path d="M8 136 V152 H24" {c}/><path d="M146 152 H162 V136" {c}/>
<rect class="scan" x="8" y="6" width="154" height="2" fill="url(#acc)" opacity=".8"/>"""
    if kind == "drone":
        return """
<path d="M14 18 C 70 18, 100 50, 96 116" stroke="#fff" stroke-opacity=".25" stroke-dasharray="3 6" stroke-width="1.5"/>
<g stroke="#fff" stroke-opacity=".3" stroke-width="1.5" stroke-linecap="round"><path d="M18 134 H38"/><path d="M8 142 H30"/><path d="M152 134 H164"/></g>
<rect x="48" y="128" width="96" height="9" rx="4.5" fill="url(#acc)"/>
<path d="M82 128 l14 -9 l14 9" stroke="url(#acc)" stroke-width="2" fill="none" opacity=".5"/>
<g>
  <animateMotion dur="4.5s" repeatCount="indefinite" path="M14 18 C 70 18, 100 50, 96 112" keyPoints="0;1;1" keyTimes="0;.75;1" calcMode="spline" keySplines=".4 0 .2 1;0 0 1 1"/>
  <g stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M-14 -8 L14 8"/><path d="M-14 8 L14 -8"/></g>
  <ellipse cx="-14" cy="-8" rx="9" ry="2.5" fill="url(#acc)" class="prop"/><ellipse cx="14" cy="-8" rx="9" ry="2.5" fill="url(#acc)" class="prop"/>
  <ellipse cx="-14" cy="8" rx="9" ry="2.5" fill="url(#acc)" class="prop"/><ellipse cx="14" cy="8" rx="9" ry="2.5" fill="url(#acc)" class="prop"/>
  <rect x="-6" y="-5" width="12" height="10" rx="3" fill="#fff"/>
</g>"""
    if kind == "rag":
        return """
<g class="sway2"><circle cx="58" cy="74" r="50" fill="url(#acc)" fill-opacity=".14" stroke="url(#acc)" stroke-width="1.5"/></g>
<g class="sway3"><circle cx="114" cy="74" r="50" fill="url(#acc)" fill-opacity=".14" stroke="url(#acc)" stroke-width="1.5"/></g>
<text x="40" y="88" font-size="38" font-weight="600" fill="#fff" font-family="'Kohinoor Devanagari','Nirmala UI','Noto Sans Devanagari',sans-serif">अ</text>
<text x="114" y="88" font-size="38" font-weight="600" fill="#fff">A</text>
<g class="blink"><path d="M86 62 C87 70 88 71 96 72 C88 73 87 74 86 82 C85 74 84 73 76 72 C84 71 85 70 86 62Z" fill="#fff"/></g>"""
    if kind == "orbit":
        return """
<g transform="translate(86 76)">
  <ellipse rx="76" ry="26" stroke="#fff" stroke-opacity=".18" stroke-dasharray="2 5"/>
  <ellipse rx="76" ry="26" transform="rotate(60)" stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 5"/>
  <ellipse rx="76" ry="26" transform="rotate(-60)" stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 5"/>
  <circle r="26" fill="url(#acc)" opacity=".18" class="breathe"/>
  <circle r="15" fill="url(#acc)"/>
  <circle r="5" fill="#fff"><animateMotion dur="5s" repeatCount="indefinite" path="M76 0 A76 26 0 1 1 -76 0 A76 26 0 1 1 76 0"/></circle>
  <g transform="rotate(60)"><circle r="4" fill="#fff" opacity=".8"><animateMotion dur="7s" repeatCount="indefinite" path="M-76 0 A76 26 0 1 1 76 0 A76 26 0 1 1 -76 0"/></circle></g>
  <g transform="rotate(-60)"><circle r="4" fill="#fff" opacity=".6"><animateMotion dur="9s" repeatCount="indefinite" path="M76 0 A76 26 0 1 0 -76 0 A76 26 0 1 0 76 0"/></circle></g>
</g>"""
    if kind == "bars":
        hs = [34, 46, 40, 58, 52, 70, 64, 82]
        bars = "".join(f'<rect class="grow" style="animation-delay:{i * .08:.2f}s" x="{4 + i * 15}" y="{140 - h}" width="10" height="{h}" rx="3" fill="#fff" fill-opacity="{.10 + i * .03:.2f}"/>' for i, h in enumerate(hs))
        return f"""
{bars}
<path d="M124 46 L140 38 L156 30 L168 22 L168 40 L156 50 L140 58 L124 62 Z" fill="url(#acc)" fill-opacity=".18"/>
<path d="M9 110 L24 98 L39 104 L54 86 L69 92 L84 74 L99 80 L114 62 L124 54" stroke="url(#acc)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M124 54 L140 48 L156 40 L168 31" stroke="url(#acc)" stroke-width="2.5" stroke-dasharray="4 5" stroke-linecap="round"/>
<circle cx="168" cy="31" r="4" fill="#fff" class="blink"/>"""
    return ""


CARD_STYLE = """
.draw{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 3.2s cubic-bezier(.6,0,.2,1) infinite;}
@keyframes draw{0%{stroke-dashoffset:100}55%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-100}}
.blink{animation:blink 2s ease-in-out infinite;} @keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
.scan{animation:scan 3s ease-in-out infinite alternate;} @keyframes scan{from{transform:translateY(0)}to{transform:translateY(144px)}}
.sway{transform-box:fill-box;transform-origin:50% 100%;animation:sway 5s ease-in-out infinite;} @keyframes sway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
.sway2{animation:s2 4s ease-in-out infinite;} @keyframes s2{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
.sway3{animation:s3 4s ease-in-out infinite;} @keyframes s3{0%,100%{transform:translateX(0)}50%{transform:translateX(-6px)}}
.prop{transform-box:fill-box;transform-origin:center;animation:prop .25s linear infinite;} @keyframes prop{50%{transform:scaleX(.35)}}
.breathe{transform-box:fill-box;transform-origin:center;animation:br 2.6s ease-in-out infinite;} @keyframes br{0%,100%{transform:scale(.85);opacity:.12}50%{transform:scale(1.3);opacity:.35}}
.grow{transform-box:fill-box;transform-origin:bottom;animation:grow 4s cubic-bezier(.2,.8,.2,1) infinite;} @keyframes grow{0%{transform:scaleY(.1)}30%,100%{transform:scaleY(1)}}
"""


def card(i, p):
    W, H = 600, 340
    defs, bg, fg = frame(0, 0, W, H, p["a1"], p["a2"], rx=28, glow=(.92, .02), strength=.36)
    x = 40
    tags, cx = "", x
    for t in p["tags"]:
        s, w = chip(cx, 274, t, size=13, h=30)
        tags += s; cx += w + 8
    desc = "".join(f'<text x="{x}" y="{226 + j * 26}" font-size="16.5" fill="{MUTED}">{esc(l)}</text>' for j, l in enumerate(p["desc"]))
    body = f"""{bg}
<text x="{x}" y="58" class="mono" font-size="12" letter-spacing="2.4" fill="url(#acc)">{i + 1:02d} — {esc(p["kicker"])}</text>
<g transform="translate(398 30)">{motif(p["motif"])}</g>
<text x="{x - 2}" y="190" font-size="36" font-weight="700" letter-spacing="-1.2" fill="{INK}">{esc(p["title"])}</text>
{desc}
{tags}
<g transform="translate({W - 60} 289)">
  <circle r="21" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".16"/>
  <path d="M-5.5 5.5 L5.5 -5.5 M-3 -5.5 H5.5 V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</g>
{fg}"""
    return svg(W, H, body, defs, CARD_STYLE, title=f'{p["title"]} — {" ".join(p["desc"])}')


# ───────────────────────────── section headers ─────────────────────────────


def header(num, kicker, title, aside, accent, dark):
    W, H = 1200, 110
    ink = INK if dark else "#1D1D1F"
    sub = "#8E8E93" if dark else "#6E6E73"
    line = "#fff" if dark else "#000"
    body = f"""
<text x="2" y="34" class="mono" font-size="13" letter-spacing="3" fill="{accent}">{num} — {esc(kicker)}</text>
<text x="0" y="84" font-size="44" font-weight="700" letter-spacing="-1.6" fill="{ink}">{esc(title)}</text>
<text x="{W}" y="84" text-anchor="end" class="mono" font-size="13" fill="{sub}">{esc(aside)}</text>
<rect x="0" y="{H - 1}" width="{W}" height="1" fill="url(#hdrLine)"/>"""
    defs = f"""<linearGradient id="hdrLine" x1="0" x2="1"><stop offset="0" stop-color="{accent}" stop-opacity=".9"/><stop offset=".25" stop-color="{line}" stop-opacity=".14"/><stop offset="1" stop-color="{line}" stop-opacity=".04"/></linearGradient>"""
    return svg(W, H, body, defs, title=title)


# ───────────────────────────── stack ─────────────────────────────


def stack():
    W = 1200
    left, right, top, row_gap, chip_h, gap = 212, 1156, 56, 30, 40, 9
    rows, y = [], top
    for label, color, items in STACK:
        cx, cy, parts = left, y, []
        for it in items:
            w = text_w(it, 15) + 28 + 18
            if cx + w > right:
                cx, cy = left, cy + chip_h + 10
            s, w = chip(cx, cy, it, size=15, h=chip_h, dot=DOTS.get(it, "#8E8E93"))
            parts.append(s); cx += w + gap
        rows.append((label, color, y, cy + chip_h, "".join(parts)))
        y = cy + chip_h + row_gap * 2
    H = y - row_gap * 2 + top
    defs, bg, fg = frame(0, 0, W, H, "#BF5AF2", "#5E5CE6", rx=28, glow=(1, 0), strength=.28)
    body = bg
    for k, (label, color, ry, rb, parts) in enumerate(rows):
        body += f'<circle cx="54" cy="{ry + 20}" r="4" fill="{color}"/><text x="70" y="{ry + 24.5}" class="mono" font-size="12" letter-spacing="2.4" fill="{color}">{esc(label)}</text>'
        body += parts
        if k < len(rows) - 1:
            body += f'<line x1="48" y1="{rb + row_gap}" x2="{W - 48}" y2="{rb + row_gap}" stroke="#fff" stroke-opacity=".06"/>'
    body += fg
    return svg(W, H, body, defs, title="Toolkit: " + "; ".join(f"{l.title()}: {', '.join(i)}" for l, _, i in STACK))


# ───────────────────────────── footer + buttons ─────────────────────────────


def footer():
    W, H = 1200, 320
    defs, bg, fg = frame(0, 0, W, H, "#0A84FF", "#BF5AF2", rx=32, glow=(.5, 1.15), strength=.55)
    defs += """<linearGradient id="fGrad" x1="0" y1="120" x2="0" y2="190" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#B4B4C4"/></linearGradient>"""
    body = f"""{bg}
<text x="600" y="84" text-anchor="middle" class="mono" font-size="13" letter-spacing="3" fill="#64D2FF">04 — CONTACT</text>
<text x="600" y="168" text-anchor="middle" font-size="64" font-weight="700" letter-spacing="-2.6" fill="url(#fGrad)">Let’s build what’s next.</text>
<text x="600" y="214" text-anchor="middle" font-size="20" fill="{MUTED}">Open to collaborations in AI, computer vision and robotics.</text>
<text x="600" y="262" text-anchor="middle" class="mono" font-size="13" fill="{DIM}">x.com/{X_HANDLE}   ·   github.com/{GH_HANDLE}</text>
{fg}"""
    return svg(W, H, body, defs, title="Let's build what's next. Open to collaborations in AI, computer vision and robotics.")


X_LOGO = "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"
GH_LOGO = ("M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.68-1.28-1.68"
           "-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.28"
           " 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19"
           " 1.83 1.19 3.09 0 4.42-2.69 5.4-5.25 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z")


def button(label, logo, a1, a2):
    W, H = 260, 64
    defs, bg, fg = frame(0, 0, W, H, a1, a2, rx=32, glow=(.5, 1.2), strength=.6)
    tw = text_w(label, 17, weight=600)
    total = 22 + 12 + tw
    x0 = (W - total) / 2
    body = f"""{bg}
<g transform="translate({x0:.1f} 21) scale(.92)"><path d="{logo}" fill="#fff"/></g>
<text x="{x0 + 34:.1f}" y="38" font-size="17" font-weight="600" letter-spacing="-.2" fill="{INK}">{esc(label)}</text>
{fg}"""
    return svg(W, H, body, defs, title=label)


# ───────────────────────────── build ─────────────────────────────

if __name__ == "__main__":
    print("Building profile artwork…")
    write("hero.svg", hero())
    write("about.svg", about())
    for i, p in enumerate(PROJECTS):
        write(f"card-{p['slug']}.svg", card(i, p))
    for slug, num, kicker, title, aside, accent in SECTIONS:
        write(f"h-{slug}-dark.svg", header(num, kicker, title, aside, accent, True))
        write(f"h-{slug}-light.svg", header(num, kicker, title, aside, accent, False))
    write("stack.svg", stack())
    write("footer.svg", footer())
    write("btn-x.svg", button("Follow on X", X_LOGO, "#8E8E93", "#3A3A3C"))
    write("btn-github.svg", button("Follow on GitHub", GH_LOGO, "#5E5CE6", "#0A84FF"))
    print("Done.")
