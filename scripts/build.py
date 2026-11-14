"""Bespoke High-Tech Vector Profile Generator for Aryan Singh Jadaun.
Aesthetic: Dark Architectural Obsidian (#070E1B), Electric Cyan (#00F0FF), Matrix Mint (#00E599), Solar Gold (#FFB800).
Zero cartoon graphics. 100% self-contained vector artwork with embedded CSS animations.
"""
import os
import sys
import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, "fonts")
OUT = os.path.join(SCRIPT_DIR, "..", "assets")

FONT_UNBOUNDED = os.path.join(FONTS_DIR, "Unbounded.ttf")
FONT_FIGTREE = os.path.join(FONTS_DIR, "Figtree.ttf")

# Palette: High-Contrast Dark Architectural Tech
BG = "#070E1B"          # Deep Midnight Obsidian
CARD = "#0C172B"        # Deep Cyan-Navy Slate
CARD_ALT = "#101F38"    # Lighter Slate Layer
INK = "#03060C"         # Solid Dark Structural Outline
WHITE = "#FFFFFF"       # Crisp Text
TEAL = "#00F0FF"        # Electric Cyan Accent
MINT = "#00E599"        # Matrix Emerald Mint
GOLD = "#FFB800"        # Solar Gold (SIH Winner)
BLUE = "#2D68FF"        # Deep Tech Royal Blue
RED = "#FF3B30"         # Gauge / Alert Red
MUTED = "#8EA3C4"       # Secondary Subtitle

SW = 4
O = f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"'


class Face:
    def __init__(self, path, wght):
        self.f = instantiateVariableFont(TTFont(path), {"wght": wght})
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.hmtx = self.f["hmtx"]

    def width(self, t, size, ls=0):
        w = sum(self.hmtx[self.cmap[ord(c)]][0] for c in t if ord(c) in self.cmap) * size / self.upm
        return w + ls * max(len(t) - 1, 0)

    def fit(self, t, maxw, maxsize, ls=0):
        w = self.width(t, maxsize, ls)
        if w <= 0: return maxsize
        return min(maxsize, maxsize * maxw / w)

    def text(self, t, x, y, size, fill=WHITE, anchor="start", ls=0, extra=""):
        w = self.width(t, size, ls)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        sc = size / self.upm
        pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.1f}")
        for c in t:
            if ord(c) not in self.cmap:
                continue
            g = self.cmap[ord(c)]
            self.gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, y)))
            x += self.hmtx[g][0] * sc + ls
        return f'<path d="{pen.getCommands()}" fill="{fill}" {extra}/>'

    def wrap(self, t, size, maxw):
        lines, cur = [], ""
        for word in t.split():
            trial = (cur + " " + word).strip()
            if self.width(trial, size) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


D = Face(FONT_UNBOUNDED, 900)   # Display font
B = Face(FONT_FIGTREE, 700)     # Body font
BX = Face(FONT_FIGTREE, 800)    # Label font

MOTION_OFF = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def svg(name, w, h, body, css="", title=""):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
         f"<title>{title}</title><style>{css}{MOTION_OFF}</style>{body}</svg>")
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(s)
    print(f"{name:24s} {len(s)/1024:6.1f} KB")


def st(stroke, extra):
    if not stroke:
        return extra
    o = O.replace(f'stroke-width="{SW}" ', "") if "stroke-width" in extra else O
    return f"{o} {extra}"


def rect(x, y, w, h, fill, rx=0, stroke=True, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {st(stroke, extra)}/>'


def circ(x, y, r, fill, stroke=True, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {st(stroke, extra)}/>'


def path(d, fill="none", extra="", stroke=True):
    return f'<path d="{d}" fill="{fill}" {st(stroke, extra)}/>'


def tri(x, y, s, fill=INK, left=False):
    k = -1 if left else 1
    return f'<path d="M{x} {y - s}L{x + k * s * 1.5} {y}L{x} {y + s}Z" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def pipe(d, fill, w=18):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * SW}" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')


def gear(cx, cy, r, fill, cls=""):
    teeth = "".join(
        f'<rect x="{-r * 0.2:.1f}" y="{-r * 1.3:.1f}" width="{r * 0.4:.1f}" height="{r * 2.6:.1f}" rx="3" fill="{fill}" {O} transform="rotate({a})"/>'
        for a in (0, 45, 90, 135))
    return (f'<g transform="translate({cx} {cy})"><g class="{cls}">{teeth}'
            f'<circle r="{r}" fill="{fill}" {O}/><circle r="{r * 0.35:.1f}" fill="{INK}"/></g></g>')


def spark(x, y, s, fill):
    return path(f"M{x} {y - s}Q{x} {y} {x + s} {y}Q{x} {y} {x} {y + s}Q{x} {y} {x - s} {y}Q{x} {y} {x} {y - s}Z", fill,
                extra='stroke-width="3"')


def pill(cx, cy, label, fill, face=BX, size=15, padx=18, h=36, ls=0.6, ink=INK):
    w = face.width(label, size, ls) + padx * 2
    return (rect(cx - w / 2, cy - h / 2, w, h, fill, rx=h / 2, extra='stroke-width="4"')
            + face.text(label, cx, cy + size * 0.36, size, ink, "middle", ls)), w


# ---------------------------------------------------------------- 1. HERO (HIGH-TECH DISTRIBUTED WORKBENCH)
def hero():
    W, H = 1200, 520
    b = [rect(0, 0, W, H, BG, stroke=False)]

    # Corner brackets / Structural Frame
    b += [
        path(f"M 24 60 V 24 H 60", extra='stroke-width="5"'),
        path(f"M {W-24} 60 V 24 H {W-60}", extra='stroke-width="5"'),
        path(f"M 24 {H-60} V {H-24} H 60", extra='stroke-width="5"'),
        path(f"M {W-24} {H-60} V {H-24} H {W-60}", extra='stroke-width="5"'),
    ]

    # Name Sign Plaque
    b += [
        rect(96, 0, 14, 62, INK, stroke=False),
        rect(486, 0, 14, 62, INK, stroke=False),
        rect(58, 68, 500, 150, INK, rx=12, stroke=False),
        rect(48, 58, 500, 150, CARD, rx=12),
        rect(66, 76, 464, 114, BLUE, rx=6),
    ]
    # Screws
    for x, y in ((57, 67), (539, 67), (57, 199), (539, 199)):
        b.append(circ(x, y, 3.5, TEAL, stroke=False))

    size = D.fit("ARYAN", 420, 80)
    b.append(D.text("ARYAN", 298, 132 + size * 0.02, min(size, 62), WHITE, "middle"))
    b.append(D.text("SINGH JADAUN", 298, 174, 25, GOLD, "middle", ls=7))

    # Main Taglines
    b.append(D.text("Ideas in.", 48, 278, 38, WHITE))
    b.append(D.text("Distributed systems out.", 48, 326, 36, TEAL))

    # 4 Status Pills
    pills_data = [
        ("SIH '26 WINNER (1ST PRIZE)", GOLD, INK),
        ("AI & BACKEND LEAD", TEAL, INK),
        ("STARTUP CO-FOUNDER", MINT, INK),
        ("1,089+ COMMITS", WHITE, INK),
    ]
    x = 48
    for i, (lab, bg_col, text_col) in enumerate(pills_data):
        if i == 2:
            x, y = 48, 438
        else:
            y = 388
        w = BX.width(lab, 14, 0.6) + 32
        p, _ = pill(x + w / 2, y, lab, bg_col, size=14, ink=text_col)
        b.append(p)
        x += w + 12

    # ---------------- RIGHT SIDE: ARCHITECTURAL TELEMETRY CLUSTER ----------------
    # High-Throughput Server Tower
    b += [
        rect(634, 330, 82, 24, INK, rx=6),
        rect(640, 96, 70, 240, CARD, rx=35),
        rect(634, 122, 82, 18, TEAL, rx=6),
        rect(634, 296, 82, 18, TEAL, rx=6),
    ]
    # Status LED stack
    for i, col in enumerate((TEAL, MINT, GOLD)):
        b.append(circ(675, 172 + i * 48, 17, col, extra=f'class="lamp l{i}"'))

    # Conduit Bus Pipe
    b.append(pipe("M712 218H768V300H830", TEAL))

    # Data Stream Tower & Exhaust Nodes
    b += [
        rect(1100, 128, 40, 92, CARD),
        rect(1091, 116, 58, 20, MINT, rx=5),
    ]
    for i, (dx, r) in enumerate(((0, 16), (10, 20), (-6, 24))):
        b.append(f'<g class="puff p{i}">{circ(1120 + dx, 96, r, TEAL)}</g>')

    # Base Chassis
    b += [
        path("M1120 250L1160 214V424L1120 462Z", INK),
        path("M820 250L860 214H1160L1120 250Z", CARD_ALT),
        rect(820, 250, 300, 212, CARD, rx=6),
        rect(798, 384, 36, 64, INK, rx=7, stroke=False),
    ]

    # AI Hex Dome & Precision Gears
    b += [
        path("M900 214A90 90 0 0 1 1080 214Z", BLUE),
        gear(990, 176, 22, TEAL, "spin"),
        path("M926 190A66 66 0 0 1 962 146", extra=f'stroke="{WHITE}" stroke-width="7"', stroke=False).replace('fill="none"', f'fill="none" stroke-linecap="round"'),
        rect(888, 208, 204, 14, INK, rx=7),
    ]

    # Analog Telemetry Dial & Swinging Needle
    b += [circ(904, 336, 50, CARD_ALT), circ(904, 336, 50, "none")]
    for a in range(-60, 61, 30):
        b.append(f'<path d="M904 298V306" stroke="{WHITE}" stroke-width="4" stroke-linecap="round" transform="rotate({a} 904 336)"/>')
    b.append(f'<g transform="translate(904 336)"><path class="needle" d="M0 4V-34" stroke="{RED}" stroke-width="6" stroke-linecap="round"/></g>')
    b.append(circ(904, 336, 7, TEAL, stroke=False))

    # Signal Indicator Lamps
    for i, col in enumerate((RED, MINT, TEAL)):
        b.append(circ(1000 + i * 40, 290, 12, col, extra=f'class="lamp l{i}"'))

    # Cooling Vents
    for i in range(3):
        b.append(f'<path d="M984 {332 + i * 16}H1096" stroke="{TEAL}" stroke-width="5" stroke-linecap="round"/>')

    # Unit Plate
    b.append(rect(984, 394, 112, 40, INK, rx=6))
    b.append(D.text("ASJ-01", 1040, 422, 19, TEAL, "middle"))

    # Electric Circuit Sparks
    b += [spark(770, 96, 16, TEAL), spark(1178, 300, 12, GOLD), spark(604, 250, 11, WHITE), spark(850, 150, 9, MINT)]

    css = (
        ".puff{transform-box:fill-box;transform-origin:center;animation:rise 4.5s linear infinite}"
        ".p1{animation-delay:-1.5s}.p2{animation-delay:-3s}"
        "@keyframes rise{0%{transform:translateY(24px) scale(.5);opacity:0}20%{opacity:1}100%{transform:translateY(-78px) scale(1.15);opacity:0}}"
        ".spin{animation:spin 8s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
        ".needle{animation:swing 3.2s cubic-bezier(.45,0,.2,1) infinite alternate}"
        "@keyframes swing{from{transform:rotate(-52deg)}to{transform:rotate(48deg)}}"
        ".lamp{animation:blink 2.4s steps(1) infinite}.l1{animation-delay:-.8s}.l2{animation-delay:-1.6s}"
        "@keyframes blink{0%,70%{opacity:1}71%,100%{opacity:.35}}"
    )
    svg("hero.svg", W, H, "".join(b), css, "Aryan Singh Jadaun — Ideas in, distributed systems out.")


# ---------------------------------------------------------------- 2. STRIP (TICKER)
def ticker_units(labels, size, y, fill, tri_fill, span):
    unit, x = [], 0
    for lab in labels:
        unit.append(D.text(lab, x, y, size, fill))
        x += D.width(lab, size) + 22
        unit.append(tri(x, y - size * 0.36, size * 0.42, tri_fill))
        x += size * 0.63 + 22
    n = int(span / x) + 2
    g = "".join(f'<g transform="translate({i * x:.1f} 0)">{"".join(unit)}</g>' for i in range(n))
    return g, x


def strip():
    W, H = 1200, 52
    items = ["ARYAN SINGH JADAUN", "SIH 2026 WINNER (1ST PRIZE)", "KRUGERX.TECH", "PROCKSI.IN", "CARELINK HEALTHCARE", "1,089+ COMMITS", "DISTRIBUTED SYSTEMS"]
    g, uw = ticker_units(items, 15, 32, TEAL, GOLD, W)
    body = (rect(0, 0, W, H, BG, stroke=False) + f'<g class="t">{g}</g>'
            + rect(0, 0, W, 4, TEAL, stroke=False) + rect(0, H - 4, W, 4, TEAL, stroke=False))
    css = f".t{{animation:t 18s linear infinite}}@keyframes t{{to{{transform:translateX(-{uw:.1f}px)}}}}"
    svg("strip.svg", W, H, body, css, "Aryan Singh Jadaun: Telemetry Ticker")


# ---------------------------------------------------------------- 3. SECTION HEADERS
def header(name, title):
    W, H = 1200, 84
    g, uw = ticker_units(["ARYAN SINGH JADAUN"], 14, 47, WHITE, TEAL, 360)
    body = (rect(0, 0, W, H, BLUE, stroke=False)
            + '<clipPath id="l"><rect x="0" y="0" width="330" height="84"/></clipPath>'
            + '<clipPath id="r"><rect x="870" y="0" width="330" height="84"/></clipPath>'
            + f'<g clip-path="url(#l)"><g class="t">{g}</g></g>'
            + f'<g clip-path="url(#r)"><g transform="translate(870 0)"><g class="t">{g}</g></g></g>'
            + tri(338, 42, 9, TEAL) + tri(862, 42, 9, TEAL, left=True)
            + rect(374, 16, 460, 56, INK, rx=28, stroke=False)
            + rect(370, 12, 460, 56, CARD, rx=28, extra=f'stroke="{TEAL}" stroke-width="4"')
            + D.text(title, 600, 50, 24, WHITE, "middle", ls=2)
            + rect(0, 0, W, 4, TEAL, stroke=False) + rect(0, H - 4, W, 4, TEAL, stroke=False))
    css = f".t{{animation:t 12s linear infinite}}@keyframes t{{to{{transform:translateX(-{uw:.1f}px)}}}}"
    svg(name, W, H, body, css, title.title())


# ---------------------------------------------------------------- 4. ABOUT CARD
def about():
    W, H = 1200, 480
    lines = [
        "Architects production AI and distributed systems end to end, from model to interface.",
        "1st Prize Winner @ Smart India Hackathon (SIH) 2026. B.Tech AIML @ GLA University.",
        "Co-Founder @ Cab-I-Net · Backend Lead @ Procksi & KrugerX Browser.",
        "FastAPI, Python 3.13, Supabase, Redis, Docker, Celery, AWS EC2, Flutter, React 19.",
    ]
    b = [
        rect(0, 0, W, H, CARD, stroke=False),
        path("M220 400V76A46 46 0 0 1 266 30H934A46 46 0 0 1 980 76V400Z", BLUE),
        rect(246, 60, 708, 310, CARD_ALT, rx=8, extra=f'stroke="{TEAL}" stroke-width="3"'),
    ]
    y = 112
    for l in lines:
        for w in B.wrap(l, 23, 676):
            b.append(B.text(w, 600, y, 23, WHITE, "middle"))
            y += 32
        y += 14

    b += [
        rect(196, 406, 808, 52, INK, rx=10, stroke=False),
        rect(196, 396, 808, 52, BG, rx=10, extra=f'stroke="{TEAL}" stroke-width="3"'),
    ]
    for i, x in enumerate((226, 276)):
        b.append(rect(x, 406, 34, 32, BLUE, rx=5))
        b.append(tri(x + (22 if i == 0 else 12), 422, 7, WHITE, left=(i == 0)))

    b += [
        circ(952, 424, 20, INK, stroke=False), circ(952, 420, 20, TEAL),
        D.text("GO", 952, 426, 13, INK, "middle"),
        gear(1090, 110, 26, WHITE, "spin"), gear(1136, 160, 16, TEAL, "spin2"),
        spark(110, 120, 20, GOLD), spark(160, 200, 11, TEAL),
    ]
    css = (".spin{animation:s 9s linear infinite}.spin2{animation:s 5.6s linear infinite reverse}"
           "@keyframes s{to{transform:rotate(360deg)}}")
    svg("about.svg", W, H, "".join(b), css, "About Aryan Singh Jadaun")


# ---------------------------------------------------------------- 5. PROJECT CARDS (6 CARDS)
def ic(body):
    return f'<g transform="translate(130 112)" {O}>{body}</g>'


ICONS = {
    "krugerx": ic(f'<circle r="26" fill="{BLUE}"/>'
                  f'<circle r="14" fill="{WHITE}"/>'
                  f'<path d="M-26 0H26M0 -26V26" fill="none" stroke="{WHITE}" stroke-width="4"/>'
                  f'<circle r="6" fill="{TEAL}"/>'),
    "procksi": ic(f'<rect x="-24" y="-30" width="48" height="60" rx="7" fill="{WHITE}"/>'
                  f'<rect x="-14" y="-20" width="28" height="6" rx="3" fill="{TEAL}"/>'
                  f'<path d="M-14 -4l6 6 12-12M-14 16l6 6 12-12" fill="none" stroke="{BLUE}" stroke-width="4"/>'),
    "carelink": ic(f'<circle r="28" fill="{WHITE}"/>'
                   f'<path d="M-9 -20H9V-9H20V9H9V20H-9V9H-20V-9H-9Z" fill="{RED}"/>'
                   f'<path d="M-28 6H-14L-8 -6L-2 16L4 2L10 6H28" fill="none" stroke="{BLUE}" stroke-width="3.5"/>'),
    "neuralflow": ic(f'<rect x="-26" y="-26" width="52" height="52" rx="8" fill="{BLUE}"/>'
                     f'<path d="M-4 -20L-14 2H2L-2 20L14 -2H-2Z" fill="{GOLD}"/>'),
    "cabinet": ic(f'<rect x="-28" y="-12" width="56" height="28" rx="6" fill="{GOLD}"/>'
                  f'<path d="M-18 -12L-12 -24H12L18 -12Z" fill="{BLUE}"/>'
                  f'<circle cx="-16" cy="16" r="7" fill="{INK}"/><circle cx="16" cy="16" r="7" fill="{INK}"/>'
                  f'<rect x="-8" y="-29" width="16" height="5" rx="2" fill="{WHITE}"/>'),
    "portfolio": ic(f'<rect x="-26" y="-30" width="52" height="60" rx="4" fill="{WHITE}"/>'
                    f'<rect x="-18" y="-22" width="36" height="10" fill="{INK}"/>'
                    f'<path d="M-18 -6H18M-18 2H18M-18 10H8M-18 18H18" fill="none" stroke="{INK}" stroke-width="3"/>'),
}

PROJECTS = [
    ("krugerx", "KrugerX Browser", "AI-powered browser ecosystem. Flutter client, async FastAPI, Redis & 5 LLM providers.", "FLUTTER · FASTAPI"),
    ("procksi", "Procksi PMS", "Enterprise task engine with RBAC, multi-tenant workspaces, WebSockets & Celery workers.", "FASTAPI · REDIS"),
    ("carelink", "CareLink Healthcare", "National healthcare platform across 5 portals with emergency routing on AWS Cloud.", "REACT 19 · AWS"),
    ("neuralflow", "NeuralFlow AI", "Hyper-speed Groq LPU studio with sub-ms SSE streaming & DeepSeek-R1 reasoning.", "GROQ · FASTAPI"),
    ("cabinet", "CAB-I-NET", "Real-time cab fare comparison across Uber, Ola & Rapido with ML surge forecasting.", "AI · FLUTTER"),
    ("portfolio", "The Developer Daily", "Cinematic 1930s living newspaper portfolio with 3D paper physics & live Git wire.", "NEXT.JS 16 · TS"),
]


def card(key, name, desc, lang):
    W, H = 600, 290
    b = [
        rect(0, 0, W, H, CARD, stroke=False),
        f'<ellipse cx="130" cy="246" rx="74" ry="10" fill="{CARD_ALT}"/>',
        path("M58 168H202V196A44 44 0 0 1 158 240H102A44 44 0 0 1 58 196Z", BLUE),
        path("M58 168V112A72 72 0 0 1 202 112V168Z", TEAL),
        f'<path d="M76 118A54 54 0 0 1 104 66" fill="none" stroke="{WHITE}" stroke-width="7" stroke-linecap="round"/>',
        ICONS[key],
        rect(46, 160, 168, 18, INK, rx=9),
    ]
    b.append(D.text(name, 244, 90, D.fit(name, 320, 28), WHITE))
    y = 126
    for l in B.wrap(desc, 18, 322):
        b.append(B.text(l, 244, y, 18, MUTED))
        y += 25
    p, w = pill(244 + (BX.width(lang, 12, 0.8) + 28) / 2, 232, lang, TEAL, size=12, padx=14, h=30, ls=0.8, ink=INK)
    b.append(p)
    b += [
        circ(548, 232, 19, INK, stroke=False),
        f'<path d="M539 232H556M549 224l8 8-8 8" fill="none" stroke="{TEAL}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
    ]
    svg(f"card-{key}.svg", W, H, "".join(b), "", f"{name}: {desc}")


# ---------------------------------------------------------------- 6. CREDENTIALS CARD
def credentials():
    W, H = 1200, 370
    items = [
        ("SIH 2026 WINNER", "Smart India Hackathon 1st Prize · MoE & GLA Internal", "1ST PRIZE", GOLD),
        ("AZURE AI (AI-900)", "Microsoft Certified: Azure AI Fundamentals", "MICROSOFT", TEAL),
        ("AZURE CLOUD (AZ-900)", "Microsoft Certified: Azure Fundamentals", "MICROSOFT", BLUE),
        ("NPTEL ELITE MIS", "Management Information System · IIT/IISc 12-Week", "ELITE 80%", MINT),
    ]
    b = [rect(0, 0, W, H, BG, stroke=False), pipe("M-20 196H1220", BLUE, 22)]
    for i, (tag, title, badge, col) in enumerate(items):
        x = 50 + i * 280
        b += [rect(x + 8, 55, 260, 275, INK, rx=10, stroke=False), rect(x, 45, 260, 275, CARD, rx=10, extra=f'stroke="{col}" stroke-width="3"')]
        p, _ = pill(x + 130, 45, badge, col, face=D, size=13, padx=18, h=36, ls=1.2, ink=INK)
        b.append(p)
        b.append(D.text(tag, x + 130, 115, D.fit(tag, 230, 18), WHITE, "middle", ls=1))
        y = 155
        for l in B.wrap(title, 16, 220):
            b.append(B.text(l, x + 130, y, 16, MUTED, "middle"))
            y += 24
        b += [
            rect(x + 20, 265, 220, 36, INK, rx=18, stroke=False),
            BX.text("VERIFIED CREDENTIAL", x + 130, 288, 12, col, "middle", ls=0.8),
        ]
    svg("credentials.svg", W, H, "".join(b), "", "Verified Honors & Credentials")


# ---------------------------------------------------------------- 7. TECH STACK
def stack():
    W, H = 1200, 370
    cols = [
        ("LANGUAGES & DB", ["Python 3.13", "TypeScript", "PostgreSQL", "Redis Cache"]),
        ("BACKEND & CLOUD", ["FastAPI Microservices", "Docker Containers", "Celery & WebSockets", "AWS (EC2, S3, CloudFront)"]),
        ("AI & AGENTIC", ["LangGraph & LangChain", "Groq LPU Inference", "DeepSeek-R1 & OpenAI", "RAG & Vector Pipelines"]),
    ]
    b = [rect(0, 0, W, H, BG, stroke=False), pipe("M-20 196H1220", TEAL, 22)]
    for i, (title, items) in enumerate(cols):
        x = 90 + i * 360
        b += [rect(x + 10, 60, 300, 268, INK, rx=10, stroke=False), rect(x, 50, 300, 268, CARD, rx=10, extra=f'stroke="{TEAL}" stroke-width="3"')]
        p, _ = pill(x + 150, 50, title, TEAL, face=D, size=14, padx=20, h=40, ls=1.5, ink=INK)
        b.append(p)
        for j, it in enumerate(items):
            y = 92 + j * 52
            b.append(rect(x + 24, y, 252, 38, CARD_ALT, rx=19, extra=f'stroke="{INK}" stroke-width="3"'))
            b.append(BX.text(it, x + 150, y + 25, 15, WHITE, "middle"))
        if i < 2:
            b += [rect(x + 318, 178, 24, 36, TEAL, rx=5)]
    svg("stack.svg", W, H, "".join(b), "", "Tech Arsenal Stack")


# ---------------------------------------------------------------- 8. CONTACT BUTTONS
def button(name, label, fill):
    W, H = 300, 92
    body = (rect(14, 16, 276, 64, INK, rx=32, stroke=False) + rect(6, 8, 276, 64, fill, rx=32, extra=f'stroke="{INK}" stroke-width="4"')
            + D.text(label, 130, 48, D.fit(label, 170, 19), INK, "middle", ls=1)
            + circ(246, 40, 17, INK, stroke=False)
            + f'<path d="M238 40H253M247 33l7 7-7 7" fill="none" stroke="{WHITE}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    svg(name, W, H, body, "", label.title())


os.makedirs(OUT, exist_ok=True)
hero()
strip()
header("head-about.svg", "SYSTEM PROFILE")
about()
header("head-projects.svg", "SHIPPED ARCHITECTURES")
for p in PROJECTS:
    card(*p)
header("head-credentials.svg", "HONORS & CREDENTIALS")
credentials()
header("head-stack.svg", "TECH ARSENAL")
stack()
header("head-contact.svg", "SAY HELLO")
button("btn-linkedin.svg", "LINKEDIN", TEAL)
button("btn-email.svg", "EMAIL", MINT)
button("btn-portfolio.svg", "PORTFOLIO", GOLD)
