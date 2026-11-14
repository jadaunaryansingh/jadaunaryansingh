"""Generate custom animated vector SVGs for Aryan Singh Jadaun's GitHub profile README.
All typography is converted to crisp SVG <path> outlines using fontTools (Unbounded + Figtree)
so every card renders identically across desktop, mobile, and GitHub's camo proxy.
"""
import html
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
FONTS = Path(__file__).resolve().parent / "fonts"


class Face:
    def __init__(self, path: Path, **axes):
        tt = TTFont(str(path))
        if axes and "fvar" in tt:
            tt = instantiateVariableFont(tt, axes, inplace=False)
        self.tt = tt
        self.upm = tt["head"].unitsPerEm
        self.cmap = tt.getBestCmap()
        self.gset = tt.getGlyphSet()
        self.hmtx = tt["hmtx"].metrics

    def width(self, text: str, size: float, track: float = 0.0) -> float:
        s = size / self.upm
        total = 0.0
        n = 0
        for c in text:
            if ord(c) in self.cmap:
                total += self.hmtx[self.cmap[ord(c)]][0] * s
                n += 1
        return total + max(0, n - 1) * track

    def text(
        self,
        text: str,
        x: float,
        y: float,
        size: float,
        fill: str = "#F8FAFC",
        track: float = 0.0,
        anchor: str = "start",
        opacity: float = 1.0,
        extra: str = "",
    ) -> str:
        s = size / self.upm
        w = self.width(text, size, track)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        pen = SVGPathPen(self.gset)
        cx = x
        for c in text:
            code = ord(c)
            if code not in self.cmap:
                continue
            gname = self.cmap[code]
            adv = self.hmtx[gname][0]
            if c != " ":
                tpen = TransformPen(pen, (s, 0, 0, -s, cx, y))
                self.gset[gname].draw(tpen)
            cx += adv * s + track
        d = pen.getCommands()
        if not d:
            return ""
        op = f' opacity="{opacity}"' if opacity < 1.0 else ""
        ex = f" {extra}" if extra else ""
        return f'<path d="{d}" fill="{fill}"{op}{ex}/>'


DISP = Face(FONTS / "Unbounded.ttf", wght=800)
DISP_M = Face(FONTS / "Unbounded.ttf", wght=600)
SANS_B = Face(FONTS / "Figtree.ttf", wght=700)
SANS_M = Face(FONTS / "Figtree.ttf", wght=600)
SANS = Face(FONTS / "Figtree.ttf", wght=500)

# High-Tech Dark Architectural Palette
BG_DEEP = "#060911"
BG_CARD = "#0A101D"
BG_PANEL = "#0E1729"
BG_GLASS = "#131F36"
BORDER = "#1E293B"
BORDER_HI = "#334155"

TEXT_WHITE = "#F8FAFC"
TEXT_LIGHT = "#CBD5E1"
TEXT_MUTED = "#94A3B8"
TEXT_DIM = "#64748B"

CYAN = "#00F0FF"
EMERALD = "#10B981"
AMBER = "#F59E0B"
VIOLET = "#A855F7"
BLUE = "#38BDF8"
ROSE = "#F43F5E"


def svg(name: str, w: int, h: int, body: str, css: str = "", title: str = ""):
    safe_title = html.escape(title or name)
    style = f"<style>{css}</style>" if css else ""
    out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="100%" role="img" aria-label="{safe_title}">'
        f"<title>{safe_title}</title>{style}{body}</svg>"
    )
    (OUT / name).write_text(out, encoding="utf-8")
    print(f"wrote {name:24s} ({len(out):>6,d} bytes)")


def wrap_lines(face: Face, text: str, size: float, max_w: float, track: float = 0.0):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if face.width(test, size, track) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def pill(
    x: float,
    y: float,
    label: str,
    accent: str = CYAN,
    bg: str = "#0D1627",
    border: str = "#1E293B",
    h: float = 30,
    dot: bool = True,
    pulse: bool = False,
):
    tw = SANS_B.width(label, 11, 0.5)
    pad_l = 24 if dot else 12
    w = int(tw + pad_l + 14)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" '
        f'fill="{bg}" stroke="{border}" stroke-width="1.2"/>'
    ]
    if dot:
        cls = ' class="pulse-dot"' if pulse else ""
        parts.append(
            f'<circle cx="{x + 13}" cy="{y + h/2:.1f}" r="4" fill="{accent}"{cls}/>'
        )
    parts.append(SANS_B.text(label, x + pad_l, y + h / 2 + 4, 11, TEXT_WHITE, 0.5))
    return "\n".join(parts), w


def corner_brackets(x: float, y: float, w: float, h: float, color: str = CYAN, s: float = 14):
    return (
        f'<g stroke="{color}" stroke-width="2" fill="none" stroke-linecap="square" opacity="0.85">'
        f'<path d="M {x},{y+s} V {y} H {x+s}"/>'
        f'<path d="M {x+w-s},{y} H {x+w} V {y+s}"/>'
        f'<path d="M {x},{y+h-s} V {y+h} H {x+s}"/>'
        f'<path d="M {x+w-s},{y+h} H {x+w} V {y+h-s}"/>'
        f"</g>"
    )


# ============================================================================
# 1. HERO BANNER (1200 x 540)
# ============================================================================
def build_hero():
    W, H = 1200, 540
    css = """
    @keyframes pulseDot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.35; transform: scale(1.35); }
    }
    @keyframes flowPacket {
      0% { stroke-dashoffset: 160; }
      100% { stroke-dashoffset: 0; }
    }
    @keyframes flowPacketRev {
      0% { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: 160; }
    }
    @keyframes spinCW {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    @keyframes spinCCW {
      from { transform: rotate(360deg); }
      to { transform: rotate(0deg); }
    }
    @keyframes barWave {
      0%, 100% { transform: scaleY(0.45); opacity: 0.65; }
      50% { transform: scaleY(1); opacity: 1; }
    }
    @keyframes scanLine {
      0% { transform: translateY(0px); opacity: 0.0; }
      15% { opacity: 0.45; }
      85% { opacity: 0.45; }
      100% { transform: translateY(410px); opacity: 0.0; }
    }
    .pulse-dot { animation: pulseDot 2.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
    .packet-1 { stroke-dasharray: 14 146; animation: flowPacket 2.6s linear infinite; }
    .packet-2 { stroke-dasharray: 14 146; animation: flowPacket 3.1s linear infinite 0.7s; }
    .packet-3 { stroke-dasharray: 14 146; animation: flowPacket 2.3s linear infinite 1.3s; }
    .packet-out { stroke-dasharray: 10 150; animation: flowPacketRev 2.8s linear infinite; }
    .ring-cw { animation: spinCW 22s linear infinite; transform-origin: 734px 298px; }
    .ring-ccw { animation: spinCCW 15s linear infinite; transform-origin: 734px 298px; }
    .scan-beam { animation: scanLine 6s linear infinite; }
    .tbar-1 { animation: barWave 1.4s ease-in-out infinite 0.0s; transform-box: fill-box; transform-origin: bottom; }
    .tbar-2 { animation: barWave 1.4s ease-in-out infinite 0.2s; transform-box: fill-box; transform-origin: bottom; }
    .tbar-3 { animation: barWave 1.4s ease-in-out infinite 0.4s; transform-box: fill-box; transform-origin: bottom; }
    .tbar-4 { animation: barWave 1.4s ease-in-out infinite 0.6s; transform-box: fill-box; transform-origin: bottom; }
    .tbar-5 { animation: barWave 1.4s ease-in-out infinite 0.8s; transform-box: fill-box; transform-origin: bottom; }
    """

    p = [
        f"""<defs>
          <pattern id="archGrid" width="32" height="32" patternUnits="userSpaceOnUse">
            <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#1E293B" stroke-width="0.7" opacity="0.45"/>
          </pattern>
          <radialGradient id="glowCyan" cx="78%" cy="28%" r="48%">
            <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.14"/>
            <stop offset="100%" stop-color="{BG_DEEP}" stop-opacity="0"/>
          </radialGradient>
          <radialGradient id="glowEmerald" cx="18%" cy="82%" r="45%">
            <stop offset="0%" stop-color="{EMERALD}" stop-opacity="0.11"/>
            <stop offset="100%" stop-color="{BG_DEEP}" stop-opacity="0"/>
          </radialGradient>
          <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="{CYAN}"/>
            <stop offset="50%" stop-color="{EMERALD}"/>
            <stop offset="100%" stop-color="{AMBER}"/>
          </linearGradient>
          <linearGradient id="coreGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0F1B33"/>
            <stop offset="100%" stop-color="#091020"/>
          </linearGradient>
        </defs>""",
        # Outer frame
        f'<rect width="{W}" height="{H}" rx="20" fill="{BG_DEEP}"/>',
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#archGrid)"/>',
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#glowCyan)"/>',
        f'<rect width="{W}" height="{H}" rx="20" fill="url(#glowEmerald)"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="19" fill="none" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<rect x="44" y="1" width="320" height="3" fill="url(#accentGrad)"/>',
        corner_brackets(14, 14, W - 28, H - 28, CYAN, 16),
    ]

    # Top Telemetry Header Bar
    p.append(
        f'<rect x="44" y="28" width="445" height="28" rx="14" fill="#0B1324" stroke="{BORDER}" stroke-width="1"/>'
        f'<circle cx="60" cy="42" r="4.5" fill="{EMERALD}" class="pulse-dot"/>'
    )
    p.append(
        SANS_B.text(
            "SYS.ONLINE  //  INDIA  //  AI & DISTRIBUTED SYSTEMS",
            74,
            46,
            10.5,
            TEXT_LIGHT,
            0.8,
        )
    )
    p.append(
        SANS_M.text(
            "CLUSTER: ASJ-PROD-26   ·   SLA: 99.98%   ·   LATENCY: 14ms",
            1156,
            46,
            10.5,
            TEXT_MUTED,
            0.6,
            anchor="end",
        )
    )

    # Left Column: Architectural Typography
    p.append(f'<rect x="44" y="80" width="22" height="3" rx="1.5" fill="{CYAN}"/>')
    p.append(
        SANS_B.text(
            "AI SYSTEMS ARCHITECT  ·  BACKEND LEAD  ·  CO-FOUNDER",
            74,
            85,
            11.5,
            CYAN,
            1.2,
        )
    )

    # Display Name
    p.append(DISP.text("ARYAN SINGH", 44, 146, 50, TEXT_WHITE, 0.5))
    # Subtle offset shadow + cyan display text for JADAUN.
    p.append(DISP.text("JADAUN.", 47, 209, 50, "#003B46", 0.5))
    p.append(DISP.text("JADAUN.", 44, 206, 50, CYAN, 0.5))
    # Accent block next to JADAUN
    j_w = DISP.width("JADAUN.", 50, 0.5)
    p.append(
        f'<rect x="{44 + j_w + 14:.1f}" y="168" width="120" height="36" rx="8" fill="#0B192C" stroke="{CYAN}" stroke-width="1.2"/>'
    )
    p.append(
        SANS_B.text(
            "B.TECH AI & ML '28",
            44 + j_w + 74,
            190,
            10.5,
            CYAN,
            0.6,
            anchor="middle",
        )
    )

    # Tagline
    p.append(
        SANS_M.text(
            "I don't build fragile demos or weekend prototypes.",
            44,
            248,
            18,
            TEXT_MUTED,
        )
    )
    p.append(
        SANS_B.text(
            "I architect & ship production systems that stay up.",
            44,
            276,
            19,
            TEXT_WHITE,
        )
    )
    tag_w = SANS_B.width("I architect & ship production systems that ", 19)
    stay_w = SANS_B.width("stay up.", 19)
    p.append(
        f'<rect x="{44 + tag_w:.1f}" y="281" width="{stay_w:.1f}" height="3" rx="1.5" fill="{EMERALD}"/>'
    )

    # 2x2 Status Badges (Carefully spaced so zero overlap)
    b1, w1 = pill(44, 306, "SIH 2026 WINNER · 1ST PRIZE", AMBER, "#14120B", "#42300E", 32, True, True)
    b2, w2 = pill(44 + w1 + 10, 306, "BACKEND LEAD @ PROCKSI & KRUGERX", CYAN, "#091826", "#133B54", 32, True, False)
    b3, w3 = pill(44, 348, "ZORVYN FINTECH · ₹40K/MO INTERN", EMERALD, "#091B18", "#124235", 32, True, False)
    b4, w4 = pill(44 + w3 + 10, 348, "CO-FOUNDER & CTO @ CAB-I-NET", VIOLET, "#151026", "#38205E", 32, True, False)
    p.extend([b1, b2, b3, b4])

    # Bottom Live KPI Strip (x=44, y=404, w=564, h=100)
    kx, ky, kw, kh = 44, 404, 564, 100
    p.append(
        f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="14" fill="{BG_CARD}" stroke="{BORDER}" stroke-width="1.2"/>'
        f'<rect x="{kx+16}" y="{ky}" width="{kw-32}" height="2" fill="url(#accentGrad)"/>'
    )
    kpis = [
        ("1,089+", "COMMITS / YEAR", CYAN, "ACTIVE DAILY"),
        ("40+", "PUBLIC REPOS", EMERALD, "OPEN SOURCE"),
        ("5 LIVE", "PROD PLATFORMS", AMBER, "SHIPPED TO USERS"),
        ("2x AZURE", "AI-900 & AZ-900", VIOLET, "+ NPTEL ELITE"),
    ]
    col_w = kw / 4
    for i, (val, lbl, col, sub) in enumerate(kpis):
        cx = kx + i * col_w
        if i > 0:
            p.append(
                f'<line x1="{cx:.1f}" y1="{ky+16}" x2="{cx:.1f}" y2="{ky+kh-16}" stroke="{BORDER}" stroke-width="1"/>'
            )
        p.append(DISP.text(val, cx + col_w / 2, ky + 42, 20, col, 0.2, anchor="middle"))
        p.append(
            SANS_B.text(
                lbl, cx + col_w / 2, ky + 64, 10, TEXT_WHITE, 0.6, anchor="middle"
            )
        )
        p.append(
            SANS.text(
                sub, cx + col_w / 2, ky + 82, 9.5, TEXT_MUTED, 0.4, anchor="middle"
            )
        )

    # ========================================================================
    # Right Column: Original Live System Topology & Neural Command Deck
    # ========================================================================
    rx, ry, rw, rh = 632, 68, 528, 436
    p.append(
        f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="16" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.5"/>'
        # Subtle animated scanline inside command deck
        f'<line x1="{rx+4}" y1="{ry+36}" x2="{rx+rw-4}" y2="{ry+36}" stroke="{CYAN}" stroke-width="1" class="scan-beam"/>'
        # Top Window Header
        f'<path d="M {rx},{ry+16} Q {rx},{ry} {rx+16},{ry} H {rx+rw-16} Q {rx+rw},{ry} {rx+rw},{ry+16} V {ry+36} H {rx} Z" fill="#0E172A"/>'
        f'<line x1="{rx}" y1="{ry+36}" x2="{rx+rw}" y2="{ry+36}" stroke="{BORDER}" stroke-width="1"/>'
        f'<circle cx="{rx+20}" cy="{ry+18}" r="5" fill="{ROSE}"/>'
        f'<circle cx="{rx+36}" cy="{ry+18}" r="5" fill="{AMBER}"/>'
        f'<circle cx="{rx+52}" cy="{ry+18}" r="5" fill="{EMERALD}"/>'
    )
    p.append(
        SANS_B.text(
            "ARCH.TOPOLOGY // PRODUCTION-MESH.V4",
            rx + 74,
            ry + 22,
            10.5,
            TEXT_LIGHT,
            0.8,
        )
    )
    p.append(
        f'<rect x="{rx+rw-132}" y="{ry+8}" width="118" height="20" rx="10" fill="#082420" stroke="{EMERALD}" stroke-width="1"/>'
        f'<circle cx="{rx+rw-118}" cy="{ry+18}" r="3.5" fill="{EMERALD}" class="pulse-dot"/>'
    )
    p.append(
        SANS_B.text("LIVE TELEMETRY", rx + rw - 108, ry + 22, 9.5, EMERALD, 0.5)
    )

    # Layer 1: 3 Client / Edge Production Platforms (y = 118..178)
    edge_nodes = [
        (650, "KRUGERX ENGINE", "Flutter · Multi-LLM", "krugerx.tech", CYAN),
        (820, "PROCKSI PMS", "RBAC · WebSockets", "procksi.in", EMERALD),
        (990, "CARELINK MESH", "5 Portals · ICU Live", "AWS CloudFront", AMBER),
    ]
    for nx, ntitle, nsub, ndom, ncol in edge_nodes:
        ny, nw, nh = 118, 154, 62
        p.append(
            f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="10" fill="{BG_PANEL}" stroke="{BORDER_HI}" stroke-width="1.2"/>'
            f'<rect x="{nx}" y="{ny}" width="4" height="{nh}" rx="2" fill="{ncol}"/>'
            f'<circle cx="{nx+nw-14}" cy="{ny+15}" r="3.5" fill="{ncol}" class="pulse-dot"/>'
        )
        p.append(SANS_B.text(ntitle, nx + 14, ny + 21, 10.5, TEXT_WHITE, 0.5))
        p.append(SANS.text(nsub, nx + 14, ny + 38, 10, TEXT_MUTED, 0.2))
        p.append(SANS_B.text(ndom, nx + 14, ny + 53, 9.5, ncol, 0.3))

    # Animated Circuit Bus Traces from Layer 1 -> Central Core (y = 180..232)
    traces_top = [
        ("M 727,180 V 206 H 820 V 232", CYAN, "packet-1"),
        ("M 897,180 V 232", EMERALD, "packet-2"),
        ("M 1067,180 V 206 H 974 V 232", AMBER, "packet-3"),
    ]
    for path_d, col, cls in traces_top:
        p.append(
            f'<path d="{path_d}" fill="none" stroke="#1E293B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{path_d}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="{cls}"/>'
        )

    # Layer 2: Central AI & Async Compute Core (x=650, y=230, w=492, h=140)
    cx_box, cy_box, cw_box, ch_box = 650, 230, 492, 140
    p.append(
        f'<rect x="{cx_box}" y="{cy_box}" width="{cw_box}" height="{ch_box}" rx="14" fill="url(#coreGrad)" stroke="{CYAN}" stroke-width="1.4" stroke-opacity="0.65"/>'
    )

    # Left inside Core: Rotating Orbital Telemetry Reactor (center = 734, 300)
    rcx, rcy = 734, 300
    p.append(
        f'<circle cx="{rcx}" cy="{rcy}" r="54" fill="#060B16" stroke="{BORDER_HI}" stroke-width="1"/>'
        f'<g class="ring-cw">'
        f'<circle cx="{rcx}" cy="{rcy}" r="45" fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="18 10 6 10" opacity="0.8"/>'
        f'<circle cx="{rcx}" cy="{rcy-45}" r="3" fill="{CYAN}"/>'
        f'<circle cx="{rcx}" cy="{rcy+45}" r="3" fill="{EMERALD}"/>'
        f"</g>"
        f'<g class="ring-ccw">'
        f'<circle cx="{rcx}" cy="{rcy}" r="32" fill="none" stroke="{EMERALD}" stroke-width="1.5" stroke-dasharray="12 8" opacity="0.85"/>'
        f"</g>"
        f'<circle cx="{rcx}" cy="{rcy}" r="19" fill="#0D1F33" stroke="{CYAN}" stroke-width="1.5"/>'
    )
    p.append(DISP.text("AI", rcx, rcy + 5, 13, CYAN, 0.5, anchor="middle"))

    # Right inside Core: FastAPI + Groq LPU + Live Telemetry Equalizer
    tx = 808
    p.append(
        SANS_B.text(
            "FASTAPI ASYNC GATEWAY & GROQ LPU STREAM",
            tx,
            cy_box + 26,
            12,
            TEXT_WHITE,
            0.5,
        )
    )
    p.append(
        SANS_M.text(
            "SSE Streaming  ·  RBAC Auth  ·  Celery Queues  ·  WebSockets",
            tx,
            cy_box + 45,
            10.2,
            CYAN,
            0.2,
        )
    )

    # Telemetry Equalizer Box (x=808, y=286, w=316, h=68)
    ex, ey, ew, eh = 808, 286, 316, 68
    p.append(
        f'<rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" rx="8" fill="#060A14" stroke="{BORDER}" stroke-width="1"/>'
    )
    # 16 animated equalizer bars on the left of the telemetry box
    bar_heights = [24, 38, 18, 42, 30, 44, 22, 36, 40, 26, 44, 32, 20, 38, 28, 42]
    for i, bh in enumerate(bar_heights):
        bx = ex + 12 + i * 9
        by = ey + 56 - bh
        bcol = CYAN if i % 2 == 0 else EMERALD
        bcls = f"tbar-{(i % 5) + 1}"
        p.append(
            f'<rect x="{bx}" y="{by}" width="5" height="{bh}" rx="2" fill="{bcol}" class="{bcls}"/>'
        )

    # Right of bars: Hard live metrics
    mx = ex + 168
    p.append(SANS_B.text("TTFT: 38ms", mx, ey + 24, 11, EMERALD, 0.4))
    p.append(SANS_B.text("STREAM: 480 tok/s", mx, ey + 41, 11, CYAN, 0.4))
    p.append(SANS_M.text("TESTS: 72 PASSING", mx, ey + 57, 10, AMBER, 0.4))

    # Animated Traces from Central Core -> Layer 3 Infrastructure Pods (y = 370..406)
    pod_centers = [706, 833, 960, 1086]
    for idx, pcx in enumerate(pod_centers):
        col = [CYAN, EMERALD, AMBER, VIOLET][idx]
        p.append(
            f'<line x1="{pcx}" y1="370" x2="{pcx}" y2="406" stroke="#1E293B" stroke-width="2"/>'
            f'<line x1="{pcx}" y1="370" x2="{pcx}" y2="406" stroke="{col}" stroke-width="2.5" class="packet-out"/>'
        )

    # Layer 3: 4 Persistence & Cloud Infrastructure Pods (y = 406..484)
    pods = [
        (650, "POSTGRESQL", "Supabase · RLS", CYAN),
        (777, "REDIS + CELERY", "Pub/Sub · Queues", EMERALD),
        (904, "AWS CLOUD", "EC2 · CloudFront", AMBER),
        (1030, "LLM ROUTER", "Groq · OpenAI", VIOLET),
    ]
    for px, ptitle, psub, pcol in pods:
        py, pw, ph = 406, 112, 76
        p.append(
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{BG_PANEL}" stroke="{BORDER}" stroke-width="1.2"/>'
            f'<rect x="{px+16}" y="{py}" width="{pw-32}" height="2.5" fill="{pcol}"/>'
        )
        p.append(
            SANS_B.text(
                ptitle, px + pw / 2, py + 32, 10.5, TEXT_WHITE, 0.5, anchor="middle"
            )
        )
        p.append(
            SANS.text(
                psub, px + pw / 2, py + 52, 9.5, TEXT_MUTED, 0.2, anchor="middle"
            )
        )

    svg(
        "hero.svg",
        W,
        H,
        "\n".join(p),
        css=css,
        title="Aryan Singh Jadaun — AI Systems Architect, Distributed Backend Lead & Startup Co-Founder",
    )


# ============================================================================
# 2. ANIMATED TELEMETRY TICKER STRIP (1200 x 52)
# ============================================================================
def build_strip():
    W, H = 1200, 52
    items = [
        ("SIH 2026 NATIONAL WINNER", AMBER),
        ("ZORVYN FINTECH · ₹40K/MO INTERN", EMERALD),
        ("KRUGERX AI BROWSER", CYAN),
        ("PROCKSI ENTERPRISE PMS", BLUE),
        ("CARELINK 5-PORTAL HEALTH MESH", ROSE),
        ("NEURALFLOW GROQ LPU STUDIO", VIOLET),
        ("CAB-I-NET CO-FOUNDER & CTO", AMBER),
        ("MICROSOFT AZURE AI-900 & AZ-900", CYAN),
        ("NPTEL IIT/IISC ELITE (80%)", EMERALD),
    ]

    # Build one segment and measure exact width
    seg_parts = []
    cx = 0
    for label, col in items:
        seg_parts.append(f'<circle cx="{cx + 12}" cy="26" r="4" fill="{col}"/>')
        seg_parts.append(SANS_B.text(label, cx + 26, 30, 11.5, TEXT_WHITE, 1.0))
        tw = SANS_B.width(label, 11.5, 1.0)
        cx += int(tw + 48)
        seg_parts.append(
            f'<path d="M {cx-14},19 L {cx-6},26 L {cx-14},33" fill="none" stroke="{BORDER_HI}" stroke-width="1.5"/>'
        )

    seg_w = cx
    seg_svg = "\n".join(seg_parts)

    css = f"""
    @keyframes tickerMove {{
      0% {{ transform: translateX(0px); }}
      100% {{ transform: translateX(-{seg_w}px); }}
    }}
    .ticker-track {{ animation: tickerMove 34s linear infinite; }}
    """

    body = f"""
    <defs>
      <linearGradient id="stripLine" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="{CYAN}"/>
        <stop offset="50%" stop-color="{EMERALD}"/>
        <stop offset="100%" stop-color="{AMBER}"/>
      </linearGradient>
      <linearGradient id="fadeEdgeL" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="{BG_DEEP}" stop-opacity="1"/>
        <stop offset="100%" stop-color="{BG_DEEP}" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="fadeEdgeR" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="{BG_DEEP}" stop-opacity="0"/>
        <stop offset="100%" stop-color="{BG_DEEP}" stop-opacity="1"/>
      </linearGradient>
      <clipPath id="stripClip">
        <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12"/>
      </clipPath>
    </defs>
    <rect width="{W}" height="{H}" rx="12" fill="{BG_CARD}" stroke="{BORDER}" stroke-width="1.2"/>
    <rect x="24" y="0" width="{W-48}" height="2" fill="url(#stripLine)"/>
    <g clip-path="url(#stripClip)">
      <g class="ticker-track">
        <g transform="translate(0,0)">{seg_svg}</g>
        <g transform="translate({seg_w},0)">{seg_svg}</g>
      </g>
      <rect x="0" y="0" width="64" height="{H}" fill="url(#fadeEdgeL)"/>
      <rect x="{W-64}" y="0" width="64" height="{H}" fill="url(#fadeEdgeR)"/>
    </g>
    """
    svg("strip.svg", W, H, body, css=css, title="Live Engineering & Achievement Ticker")


# ============================================================================
# 3. ARCHITECTURAL SECTION HEADERS (1200 x 72)
# ============================================================================
def build_header(fname: str, idx: str, label: str, sub: str, accent: str):
    W, H = 1200, 72
    center_w = max(360, int(DISP.width(label, 17, 1.5) + 130))
    box_x = (W - center_w) // 2

    # Flanking ticker text
    unit = f"{idx} // {sub}   ·   "
    uw = int(SANS_B.width(unit, 10.5, 1.2))
    reps = (W // uw) + 3
    stream = "".join(
        SANS_B.text(unit, i * uw, 40, 10.5, TEXT_DIM, 1.2) for i in range(reps)
    )

    css = f"""
    @keyframes headMarquee {{
      0% {{ transform: translateX(0px); }}
      100% {{ transform: translateX(-{uw}px); }}
    }}
    @keyframes pulseBeacon {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
    }}
    .h-track {{ animation: headMarquee 10s linear infinite; }}
    .h-dot {{ animation: pulseBeacon 2s ease-in-out infinite; }}
    """

    body = f"""
    <defs>
      <clipPath id="leftWing">
        <rect x="16" y="14" width="{box_x - 28}" height="44" rx="8"/>
      </clipPath>
      <clipPath id="rightWing">
        <rect x="{box_x + center_w + 12}" y="14" width="{box_x - 28}" height="44" rx="8"/>
      </clipPath>
    </defs>
    <!-- Flanking bars -->
    <rect x="16" y="16" width="{box_x - 28}" height="40" rx="8" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1"/>
    <rect x="{box_x + center_w + 12}" y="16" width="{box_x - 28}" height="40" rx="8" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1"/>
    <g clip-path="url(#leftWing)"><g class="h-track">{stream}</g></g>
    <g clip-path="url(#rightWing)"><g class="h-track">{stream}</g></g>

    <!-- Central Architectural Badge -->
    <rect x="{box_x}" y="8" width="{center_w}" height="56" rx="14" fill="{BG_CARD}" stroke="{accent}" stroke-width="1.5"/>
    <rect x="{box_x + 24}" y="8" width="{center_w - 48}" height="3" fill="{accent}"/>
    <rect x="{box_x + 16}" y="22" width="44" height="28" rx="6" fill="{BG_PANEL}" stroke="{BORDER_HI}" stroke-width="1"/>
    {DISP.text(idx, box_x + 38, 41, 13, accent, 0.5, anchor="middle")}
    {DISP.text(label, box_x + 76, 42, 16.5, TEXT_WHITE, 1.4)}
    <circle cx="{box_x + center_w - 22}" cy="36" r="4.5" fill="{accent}" class="h-dot"/>
    """
    svg(fname, W, H, body, css=css, title=f"Section {idx} - {label}")


# ============================================================================
# 4. SYSTEM MANIFEST & TELEMETRY BENTO (about.svg — 1200 x 430)
# ============================================================================
def build_about():
    W, H = 1200, 430
    css = """
    @keyframes cursorBlink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    .cursor { animation: cursorBlink 1.1s step-end infinite; }
    """
    p = [
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1.5"/>',
        # Left IDE Manifest Card (x=22, y=20, w=636, h=390)
        f'<rect x="22" y="20" width="636" height="390" rx="14" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.2"/>',
        f'<path d="M 22,34 Q 22,20 36,20 H 644 Q 658,20 658,34 V 56 H 22 Z" fill="{BG_PANEL}"/>',
        f'<line x1="22" y1="56" x2="658" y2="56" stroke="{BORDER}" stroke-width="1"/>',
        f'<circle cx="42" cy="38" r="5" fill="{ROSE}"/>',
        f'<circle cx="58" cy="38" r="5" fill="{AMBER}"/>',
        f'<circle cx="74" cy="38" r="5" fill="{EMERALD}"/>',
        SANS_B.text("aryan_jadaun.manifest.yaml  —  PRODUCTION PROFILE", 98, 42, 11, TEXT_LIGHT, 0.5),
        SANS_B.text("UTF-8 // YAML", 640, 42, 10, CYAN, 0.5, anchor="end"),
    ]

    # YAML lines inside IDE
    code_lines = [
        ("01", "engineer:", "Aryan Singh Jadaun", CYAN),
        ("02", "education:", "B.Tech in AI & ML @ GLA University (2024–2028)", TEXT_WHITE),
        ("03", "schooling:", "St. Peter's College, Agra (ICSE / ISC Alumnus)", TEXT_LIGHT),
        ("04", "current_roles:", "", TEXT_MUTED),
        ("05", "  - zorvyn_fintech:", "Backend Developer Intern (₹40,000/mo · 6 Mos)", EMERALD),
        ("06", "  - cab_i_net:", "Co-Founder & CTO · AI Mobility Aggregator", AMBER),
        ("07", "  - procksi_krugerx:", "Backend Lead · Distributed Systems & AI Engine", CYAN),
        ("08", "  - linuxworld_2025:", "Agentic AI & Cloud Intern (Mentored by Vimal Daga)", TEXT_LIGHT),
        ("09", "  - ieee_cs_council:", "Corporate Relations Secretary & Head (Led 200+)", VIOLET),
        ("10", "core_architecture:", "[FastAPI, Next.js 16, Flutter, PostgreSQL, Redis, AWS]", BLUE),
        ("11", "operating_principle:", '"Ideas in. Fault-tolerant production systems out."', EMERALD),
    ]

    y = 86
    for ln, key, val, vcol in code_lines:
        p.append(SANS.text(ln, 40, y, 12, TEXT_DIM, 0.3))
        p.append(SANS_B.text(key, 72, y, 12.5, CYAN if not key.startswith("  -") else TEXT_LIGHT, 0.2))
        kw = SANS_B.width(key, 12.5, 0.2)
        if val:
            p.append(SANS_M.text(val, 72 + kw + 10, y, 12.5, vcol, 0.1))
        y += 27

    # Bottom status bar inside IDE
    p.append(
        f'<rect x="38" y="366" width="604" height="30" rx="6" fill="#060A12" stroke="{BORDER}" stroke-width="1"/>'
        f'<rect x="48" y="375" width="8" height="12" fill="{CYAN}" class="cursor"/>'
    )
    p.append(
        SANS_B.text(
            "STATUS: READY FOR HIGH-SCALE BACKEND, AI SYSTEMS & FOUNDING ENGINEER ROLES",
            66,
            385,
            10.5,
            EMERALD,
            0.5,
        )
    )

    # Right Side: 2x3 Hard Metric Bento Grid (x=676..1178, y=20..410)
    metrics = [
        ("1ST PRIZE", "SIH 2026 WINNER", "National Smart India Hackathon Trophy", AMBER),
        ("₹40K / MO", "ZORVYN FINTECH", "6-Month Backend Engineering Internship", EMERALD),
        ("1,089+", "ANNUAL COMMITS", "Sustained Daily Production Velocity", CYAN),
        ("40+ REPOS", "OPEN SOURCE", "Full-Stack, AI Agents & Microservices", BLUE),
        ("5 LIVE", "PROD PLATFORMS", "KrugerX, Procksi, CareLink, Cab-I-Net", VIOLET),
        ("200+ TEAM", "IEEE CS COUNCIL", "Corporate Relations Secretary & Head", ROSE),
    ]

    gx0, gy0 = 676, 20
    cw, ch = 244, 122
    gap_x, gap_y = 14, 12

    for i, (big, title, desc, col) in enumerate(metrics):
        col_idx = i % 2
        row_idx = i // 2
        cx = gx0 + col_idx * (cw + gap_x)
        cy = gy0 + row_idx * (ch + gap_y)
        p.append(
            f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.2"/>'
            f'<rect x="{cx}" y="{cy+18}" width="4" height="{ch-36}" rx="2" fill="{col}"/>'
            f'<circle cx="{cx+cw-20}" cy="{cy+22}" r="4" fill="{col}"/>'
        )
        p.append(DISP.text(big, cx + 18, cy + 44, 22, col, 0.3))
        p.append(SANS_B.text(title, cx + 18, cy + 72, 11.5, TEXT_WHITE, 0.6))
        p.append(SANS.text(desc, cx + 18, cy + 94, 10.5, TEXT_MUTED, 0.1))

    svg(
        "about.svg",
        W,
        H,
        "\n".join(p),
        css=css,
        title="Aryan Singh Jadaun — Engineering Manifest & Live Metrics",
    )


# ============================================================================
# 5. FLAGSHIP PROJECT CARDS (600 x 320 each)
# ============================================================================
def project_icon(kind: str, x: float, y: float, accent: str) -> str:
    """Custom multi-layered vector artwork emblem for each flagship system."""
    box = (
        f'<rect x="{x}" y="{y}" width="58" height="58" rx="14" fill="{BG_PANEL}" '
        f'stroke="{accent}" stroke-width="1.5"/>'
    )
    if kind == "krugerx":
        # Browser window + AI neural core
        art = (
            f'<rect x="{x+10}" y="{y+12}" width="38" height="34" rx="5" fill="none" stroke="{ TEXT_WHITE }" stroke-width="1.8"/>'
            f'<line x1="{x+10}" y1="{y+20}" x2="{x+48}" y2="{y+20}" stroke="{accent}" stroke-width="1.5"/>'
            f'<circle cx="{x+29}" cy="{y+33}" r="6" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<line x1="{x+19}" y1="{y+33}" x2="{x+23}" y2="{y+33}" stroke="{accent}" stroke-width="1.5"/>'
            f'<line x1="{x+35}" y1="{y+33}" x2="{x+39}" y2="{y+33}" stroke="{accent}" stroke-width="1.5"/>'
        )
    elif kind == "procksi":
        # Multi-tenant Kanban + RBAC lock/nodes
        art = (
            f'<rect x="{x+11}" y="{y+13}" width="10" height="32" rx="2.5" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<rect x="{x+24}" y="{y+13}" width="10" height="22" rx="2.5" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.8"/>'
            f'<rect x="{x+37}" y="{y+13}" width="10" height="28" rx="2.5" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<circle cx="{x+29}" cy="{y+42}" r="3" fill="{accent}"/>'
        )
    elif kind == "carelink":
        # Connected Healthcare Cross + Pulse Wave
        art = (
            f'<path d="M {x+25},{y+12} H {x+33} V {y+24} H {x+45} V {y+32} H {x+33} V {y+44} H {x+25} V {y+32} H {x+13} V {y+24} H {x+25} Z" '
            f'fill="none" stroke="{accent}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<polyline points="{x+15},{y+28} {x+23},{y+28} {x+26},{y+21} {x+31},{y+35} {x+34},{y+28} {x+43},{y+28}" '
            f'fill="none" stroke="{TEXT_WHITE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    elif kind == "neuralflow":
        # LPU Chip + High-Speed Streaming Bolts
        art = (
            f'<rect x="{x+16}" y="{y+16}" width="26" height="26" rx="4" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.8"/>'
            f'<path d="M {x+31},{y+20} L {x+24},{y+30} H {x+30} L {x+27},{y+38} L {x+34},{y+28} H {x+28} Z" fill="{accent}"/>'
            f'<line x1="{x+22}" y1="{y+10}" x2="{x+22}" y2="{y+16}" stroke="{accent}" stroke-width="1.8"/>'
            f'<line x1="{x+36}" y1="{y+10}" x2="{x+36}" y2="{y+16}" stroke="{accent}" stroke-width="1.8"/>'
            f'<line x1="{x+22}" y1="{y+42}" x2="{x+22}" y2="{y+48}" stroke="{accent}" stroke-width="1.8"/>'
            f'<line x1="{x+36}" y1="{y+42}" x2="{x+36}" y2="{y+48}" stroke="{accent}" stroke-width="1.8"/>'
        )
    elif kind == "cabinet":
        # Route Map Pin + Surge Telemetry Graph
        art = (
            f'<path d="M {x+29},{y+11} C {x+21},{y+11} {x+15},{y+17} {x+15},{y+25} C {x+15},{y+35} {x+29},{y+46} {x+29},{y+46} C {x+29},{y+46} {x+43},{y+35} {x+43},{y+25} C {x+43},{y+17} {x+37},{y+11} {x+29},{y+11} Z" '
            f'fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<circle cx="{x+29}" cy="{y+25}" r="5" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.8"/>'
        )
    else:
        # Broadsheet Newspaper Grid
        art = (
            f'<rect x="{x+12}" y="{y+12}" width="34" height="34" rx="4" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.8"/>'
            f'<line x1="{x+16}" y1="{y+19}" x2="{x+42}" y2="{y+19}" stroke="{accent}" stroke-width="2.2"/>'
            f'<rect x="{x+16}" y="{y+24}" width="12" height="16" fill="none" stroke="{accent}" stroke-width="1.5"/>'
            f'<line x1="{x+32}" y1="{y+26}" x2="{x+42}" y2="{y+26}" stroke="{TEXT_LIGHT}" stroke-width="1.5"/>'
            f'<line x1="{x+32}" y1="{y+32}" x2="{x+42}" y2="{y+32}" stroke="{TEXT_LIGHT}" stroke-width="1.5"/>'
            f'<line x1="{x+32}" y1="{y+38}" x2="{x+42}" y2="{y+38}" stroke="{TEXT_LIGHT}" stroke-width="1.5"/>'
        )
    return box + art


def build_project_card(
    fname: str,
    kind: str,
    title: str,
    role_sub: str,
    live_badge: str,
    desc: str,
    pipeline: str,
    tags: list[str],
    accent: str,
):
    W, H = 600, 320
    css = """
    @keyframes dotPulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.35; }
    }
    .p-dot { animation: dotPulse 2s ease-in-out infinite; }
    """
    p = [
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.5"/>',
        f'<rect x="28" y="0" width="180" height="3" fill="{accent}"/>',
        project_icon(kind, 26, 26, accent),
        DISP.text(title, 98, 50, 19, TEXT_WHITE, 0.4),
        SANS_B.text(role_sub, 98, 72, 11.5, accent, 0.5),
    ]

    # Top-right live badge
    bw = int(SANS_B.width(live_badge, 10.5, 0.5) + 32)
    bx = W - 24 - bw
    p.append(
        f'<rect x="{bx}" y="26" width="{bw}" height="28" rx="14" fill="{BG_PANEL}" stroke="{accent}" stroke-width="1.2"/>'
        f'<circle cx="{bx+13}" cy="40" r="4" fill="{accent}" class="p-dot"/>'
    )
    p.append(SANS_B.text(live_badge, bx + 24, 44, 10.5, TEXT_WHITE, 0.5))

    # Divider
    p.append(f'<line x1="26" y1="98" x2="{W-26}" y2="98" stroke="{BORDER}" stroke-width="1"/>')

    # Wrapped description (max 3 lines)
    lines = wrap_lines(SANS, desc, 13.5, W - 52)
    y = 124
    for ln in lines[:3]:
        p.append(SANS.text(ln, 26, y, 13.5, TEXT_LIGHT, 0.1))
        y += 22

    # Architecture Flow Bar (y = 198)
    p.append(
        f'<rect x="26" y="198" width="{W-52}" height="34" rx="8" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1"/>'
        f'<rect x="26" y="198" width="4" height="34" rx="2" fill="{accent}"/>'
    )
    p.append(SANS_B.text("ARCH:", 40, 219, 10.5, accent, 0.6))
    p.append(SANS_M.text(pipeline, 86, 219, 11, TEXT_WHITE, 0.3))

    # Bottom Tech Pills + Action CTA (y = 254)
    tx = 26
    for t in tags:
        tw = int(SANS_B.width(t, 10.5, 0.4) + 20)
        if tx + tw > W - 140:
            break
        p.append(
            f'<rect x="{tx}" y="256" width="{tw}" height="28" rx="8" fill="{BG_PANEL}" stroke="{BORDER_HI}" stroke-width="1"/>'
        )
        p.append(SANS_B.text(t, tx + 10, 274, 10.5, TEXT_LIGHT, 0.4))
        tx += tw + 8

    # Right CTA button
    p.append(
        f'<rect x="{W-132}" y="254" width="106" height="32" rx="10" fill="{BG_PANEL}" stroke="{accent}" stroke-width="1.2"/>'
    )
    p.append(SANS_B.text("LAUNCH", W - 92, 274, 11, accent, 0.8, anchor="middle"))
    p.append(
        f'<path d="M {W-54},274 L {W-44},264 M {W-52},264 H {W-44} V 272" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    svg(fname, W, H, "\n".join(p), css=css, title=f"{title} — {role_sub}")


# ============================================================================
# 6. HONORS & VERIFIED CREDENTIALS (credentials.svg — 1200 x 300)
# ============================================================================
def build_credentials():
    W, H = 1200, 300
    p = [
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1.5"/>'
    ]

    cards = [
        (
            "NATIONAL WINNER",
            "SMART INDIA HACKATHON",
            "SIH 2026 · 1ST PRIZE",
            "Won 1st Place nationally with ₹10,000 prize cheque & official trophy for shipping an end-to-end production solution.",
            "GOVT OF INDIA  ·  2026",
            AMBER,
            "trophy",
        ),
        (
            "MICROSOFT CERTIFIED",
            "AZURE AI FUNDAMENTALS",
            "EXAM AI-900 · VERIFIED",
            "Certified in Azure AI workloads, Machine Learning pipelines, Computer Vision, NLP & Generative AI architecture.",
            "MICROSOFT  ·  AI-900",
            CYAN,
            "ms_ai",
        ),
        (
            "MICROSOFT CERTIFIED",
            "AZURE FUNDAMENTALS",
            "EXAM AZ-900 · VERIFIED",
            "Certified in Cloud infrastructure, Core Azure compute/storage, Zero-Trust IAM security, governance & SLAs.",
            "MICROSOFT  ·  AZ-900",
            BLUE,
            "ms_az",
        ),
        (
            "IIT / IISC NPTEL ELITE",
            "MANAGEMENT INFO SYS",
            "ELITE SCORE: 80% (2026)",
            "12-Week IIT/IISc curriculum in enterprise information systems. Proctored Final: 55.5/75 + Assignments: 24.38/25.",
            "NPTEL  ·  NOC26-MG129",
            EMERALD,
            "nptel",
        ),
    ]

    cw, ch = 276, 260
    gap = 18
    x0, y0 = 21, 20

    for i, (badge, title, sub, desc, foot, col, ic) in enumerate(cards):
        cx = x0 + i * (cw + gap)
        cy = y0
        p.append(
            f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.2"/>'
            f'<rect x="{cx+20}" y="{cy}" width="{cw-40}" height="3" fill="{col}"/>'
        )
        # Badge pill
        p.append(
            f'<rect x="{cx+18}" y="{cy+18}" width="170" height="24" rx="12" fill="{BG_PANEL}" stroke="{col}" stroke-width="1"/>'
        )
        p.append(SANS_B.text(badge, cx + 30, cy + 34, 9.5, col, 0.7))

        # Vector icon in top-right of card
        ix, iy = cx + cw - 52, cy + 16
        p.append(
            f'<rect x="{ix}" y="{iy}" width="34" height="34" rx="8" fill="{BG_PANEL}" stroke="{BORDER_HI}" stroke-width="1"/>'
        )
        if ic == "trophy":
            p.append(
                f'<path d="M {ix+11},{iy+10} H {ix+23} V {iy+17} C {ix+23},{iy+21} {ix+11},{iy+21} {ix+11},{iy+17} Z M {ix+17},{iy+20} V {iy+25} M {ix+12},{iy+25} H {ix+22}" '
                f'fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round"/>'
            )
        elif ic.startswith("ms"):
            p.append(
                f'<rect x="{ix+10}" y="{iy+10}" width="6" height="6" fill="{col}"/>'
                f'<rect x="{ix+18}" y="{iy+10}" width="6" height="6" fill="{TEXT_WHITE}"/>'
                f'<rect x="{ix+10}" y="{iy+18}" width="6" height="6" fill="{TEXT_WHITE}"/>'
                f'<rect x="{ix+18}" y="{iy+18}" width="6" height="6" fill="{col}"/>'
            )
        else:
            p.append(
                f'<circle cx="{ix+17}" cy="{iy+17}" r="8" fill="none" stroke="{col}" stroke-width="1.8"/>'
                f'<polyline points="{ix+13},{iy+17} {ix+16},{iy+20} {ix+22},{iy+14}" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.8" stroke-linecap="round"/>'
            )

        p.append(DISP.text(title, cx + 18, cy + 74, 12.8, TEXT_WHITE, 0.2))
        p.append(SANS_B.text(sub, cx + 18, cy + 96, 11, col, 0.4))
        p.append(
            f'<line x1="{cx+18}" y1="{cy+112}" x2="{cx+cw-18}" y2="{cy+112}" stroke="{BORDER}" stroke-width="1"/>'
        )

        dlines = wrap_lines(SANS, desc, 12, cw - 36)
        dy = cy + 134
        for ln in dlines[:4]:
            p.append(SANS.text(ln, cx + 18, dy, 12, TEXT_LIGHT, 0.1))
            dy += 19

        p.append(
            f'<rect x="{cx+18}" y="{cy+ch-42}" width="{cw-36}" height="26" rx="6" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1"/>'
        )
        p.append(
            SANS_B.text(
                foot, cx + cw / 2, cy + ch - 25, 10, TEXT_MUTED, 0.6, anchor="middle"
            )
        )

    svg(
        "credentials.svg",
        W,
        H,
        "\n".join(p),
        title="Honors, Hackathons & Verified Cloud Certifications",
    )


# ============================================================================
# 7. PRODUCTION TECH MATRIX (stack.svg — 1200 x 350)
# ============================================================================
def build_stack():
    W, H = 1200, 350
    p = [
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1.5"/>'
    ]

    cols = [
        (
            "01 // BACKEND & CORE",
            CYAN,
            [
                ("Python 3.12+", "PRIMARY"),
                ("FastAPI (Async)", "PRODUCTION"),
                ("Node.js & Express", "PRODUCTION"),
                ("REST & WebSockets", "REAL-TIME"),
                ("Celery & Task Queues", "DISTRIBUTED"),
                ("RBAC & JWT Auth", "SECURITY"),
            ],
        ),
        (
            "02 // AI, LLM & ML OPS",
            VIOLET,
            [
                ("OpenAI / Claude / Gemini", "MULTI-LLM"),
                ("Groq LPU & SSE Stream", "SUB-MS"),
                ("LangChain & RAG", "AGENTIC AI"),
                ("DeepSeek-R1 & Ollama", "REASONING"),
                ("PyTorch & Scikit-Learn", "ML / DL"),
                ("Computer Vision & CNN", "INFERENCE"),
            ],
        ),
        (
            "03 // DATA, CLOUD & INFRA",
            EMERALD,
            [
                ("PostgreSQL & Supabase", "PRIMARY DB"),
                ("Redis Pub/Sub & Cache", "LOW LATENCY"),
                ("MongoDB & MySQL", "POLYGLOT"),
                ("AWS EC2, S3 & CloudFront", "CLOUD"),
                ("Docker & GitHub CI/CD", "CONTAINERS"),
                ("Microsoft Azure Cloud", "2x CERT"),
            ],
        ),
        (
            "04 // CLIENT & INTERFACES",
            AMBER,
            [
                ("Next.js 16 (App Router)", "FULL-STACK"),
                ("React 19 & TypeScript", "STRICT UI"),
                ("Flutter & Dart", "MULTI-OS"),
                ("Tailwind CSS & GSAP", "MOTION"),
                ("Framer Motion", "INTERACTIVE"),
                ("Live Telemetry UI", "OBSERVABILITY"),
            ],
        ),
    ]

    cw, ch = 276, 310
    gap = 18
    x0, y0 = 21, 20

    for i, (head, col, rows) in enumerate(cols):
        cx = x0 + i * (cw + gap)
        cy = y0
        p.append(
            f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.2"/>'
            f'<rect x="{cx}" y="{cy}" width="{cw}" height="44" rx="14" fill="{BG_PANEL}"/>'
            f'<rect x="{cx+16}" y="{cy}" width="{cw-32}" height="3" fill="{col}"/>'
        )
        p.append(SANS_B.text(head, cx + 18, cy + 27, 11.5, col, 0.8))

        ry = cy + 60
        for name, tag in rows:
            p.append(
                f'<rect x="{cx+14}" y="{ry}" width="{cw-28}" height="34" rx="8" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1"/>'
                f'<circle cx="{cx+28}" cy="{ry+17}" r="3.5" fill="{col}"/>'
            )
            p.append(SANS_B.text(name, cx + 40, ry + 21, 11.5, TEXT_WHITE, 0.2))
            p.append(
                SANS_B.text(
                    tag, cx + cw - 24, ry + 21, 9, col, 0.5, anchor="end"
                )
            )
            ry += 40

    svg("stack.svg", W, H, "\n".join(p), title="Production Tech Stack & Architecture Matrix")


# ============================================================================
# 8. CTA COMMAND BUTTONS (380 x 84 each)
# ============================================================================
def build_button(fname: str, label: str, sub: str, accent: str, icon_kind: str):
    W, H = 380, 84
    p = [
        f'<rect width="{W}" height="{H}" rx="16" fill="{BG_CARD}" stroke="{accent}" stroke-width="1.5"/>',
        f'<rect x="24" y="0" width="120" height="3" fill="{accent}"/>',
        f'<rect x="18" y="18" width="48" height="48" rx="12" fill="{BG_PANEL}" stroke="{BORDER_HI}" stroke-width="1.2"/>',
    ]
    if icon_kind == "web":
        p.append(
            f'<circle cx="42" cy="42" r="13" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<ellipse cx="42" cy="42" rx="6" ry="13" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.4"/>'
            f'<line x1="29" y1="42" x2="55" y2="42" stroke="{accent}" stroke-width="1.4"/>'
        )
    elif icon_kind == "in":
        p.append(DISP.text("in", 42, 49, 20, accent, 0.2, anchor="middle"))
    else:
        p.append(
            f'<rect x="29" y="32" width="26" height="20" rx="3" fill="none" stroke="{accent}" stroke-width="1.8"/>'
            f'<polyline points="30,34 42,43 54,34" fill="none" stroke="{TEXT_WHITE}" stroke-width="1.6"/>'
        )

    p.append(DISP.text(label, 80, 40, 15, TEXT_WHITE, 0.5))
    p.append(SANS_B.text(sub, 80, 60, 11.5, accent, 0.3))
    p.append(
        f'<circle cx="{W-32}" cy="42" r="16" fill="{BG_PANEL}" stroke="{BORDER_HI}" stroke-width="1"/>'
        f'<path d="M {W-37},47 L {W-27},37 M {W-35},37 H {W-27} V 45" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    svg(fname, W, H, "\n".join(p), title=f"{label} — {sub}")


def build_footer():
    W, H = 1200, 96
    css = """
    @keyframes pulseFooter {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.35; }
    }
    .f-dot { animation: pulseFooter 2.2s ease-in-out infinite; }
    """
    p = [
        f"""<defs>
          <linearGradient id="footGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="{CYAN}"/>
            <stop offset="50%" stop-color="{EMERALD}"/>
            <stop offset="100%" stop-color="{AMBER}"/>
          </linearGradient>
        </defs>""",
        f'<rect width="{W}" height="{H}" rx="16" fill="{BG_DEEP}" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<rect x="60" y="0" width="{W-120}" height="2.5" fill="url(#footGrad)"/>',
        corner_brackets(12, 12, W - 24, H - 24, CYAN, 12),
        f'<circle cx="48" cy="48" r="5" fill="{EMERALD}" class="f-dot"/>',
        DISP.text("IDEAS IN. FAULT-TOLERANT PRODUCTION SYSTEMS OUT.", 68, 44, 14, TEXT_WHITE, 0.8),
        SANS_M.text(
            "Architected & Engineered by Aryan Singh Jadaun  ·  Agra / Mathura, India  ·  All Systems Operational",
            68,
            66,
            11.5,
            TEXT_MUTED,
            0.3,
        ),
        f'<rect x="{W-230}" y="28" width="194" height="40" rx="10" fill="{BG_CARD}" stroke="{BORDER_HI}" stroke-width="1.2"/>',
        SANS_B.text("SYS.VER // 2026.4", W - 133, 52, 11, CYAN, 0.8, anchor="middle"),
    ]
    svg("footer.svg", W, H, "\n".join(p), css=css, title="Aryan Singh Jadaun — Closing Telemetry Banner")


if __name__ == "__main__":
    build_hero()
    build_strip()

    build_header("head-about.svg", "01", "SYSTEM TELEMETRY", "ENGINEERING PROFILE", CYAN)
    build_about()

    build_header("head-projects.svg", "02", "SHIPPED PRODUCTION SYSTEMS", "LIVE ARCHITECTURE", EMERALD)
    build_project_card(
        "card-krugerx.svg",
        "krugerx",
        "KRUGERX BROWSER",
        "AI-POWERED MULTI-PLATFORM BROWSER ENGINE",
        "LIVE · krugerx.tech",
        "Privacy-first cross-platform browser & neural search workspace orchestrating multi-LLM synthesis, real-time web scraping, and background task queues.",
        "Flutter  ->  FastAPI Async  ->  Redis + Celery  ->  Multi-LLM",
        ["FLUTTER", "FASTAPI", "SUPABASE", "REDIS", "MULTI-LLM"],
        CYAN,
    )
    build_project_card(
        "card-procksi.svg",
        "procksi",
        "PROCKSI PMS",
        "BACKEND LEAD · ENTERPRISE PROJECT PLATFORM",
        "LIVE · procksi.in",
        "High-concurrency multi-tenant workspace engine with granular RBAC permissions, automated sprint workflows, Celery background workers & live WebSockets.",
        "Client UI  ->  FastAPI RBAC  ->  PostgreSQL + Redis  ->  WebSockets",
        ["FASTAPI", "POSTGRESQL", "REDIS", "CELERY", "WEBSOCKETS"],
        EMERALD,
    )
    build_project_card(
        "card-carelink.svg",
        "carelink",
        "CARELINK INDIA",
        "5-PORTAL CONNECTED HEALTHCARE MESH",
        "5 PORTALS · AWS LIVE",
        "Unified healthcare ecosystem connecting Govt, Hospital, Doctor, Patient & Creator portals with live ICU bed telemetry, emergency routing & 72 automated tests.",
        "React 19 + Flutter  ->  FastAPI  ->  Supabase RLS  ->  AWS CloudFront",
        ["FASTAPI", "REACT 19", "FLUTTER", "SUPABASE", "AWS"],
        ROSE,
    )
    build_project_card(
        "card-neuralflow.svg",
        "neuralflow",
        "NEURALFLOW AI",
        "GROQ LPU HYPER-SPEED STREAMING STUDIO",
        "SUB-MS · GROQ LPU",
        "Ultra-low-latency AI developer studio streaming tokens via Server-Sent Events with live TTFT/throughput telemetry, DeepSeek-R1 reasoning & code sandbox.",
        "React Studio  ->  SSE Stream  ->  Groq LPU API  ->  Live Telemetry",
        ["GROQ LPU", "SSE STREAM", "DEEPSEEK-R1", "REACT", "VITE"],
        VIOLET,
    )
    build_project_card(
        "card-cabinet.svg",
        "cabinet",
        "CAB-I-NET",
        "CO-FOUNDER & CTO · AI MOBILITY AGGREGATOR",
        "LIVE · cab-i-net",
        "Real-time cab fare & ETA comparison engine across Uber, Ola & Rapido powered by ML surge-pricing prediction models, Google Maps routing & Razorpay.",
        "React PWA  ->  Node + FastAPI  ->  ML Surge Engine  ->  Maps + Razorpay",
        ["NODE.JS", "PYTHON ML", "REACT", "GOOGLE MAPS", "RAZORPAY"],
        AMBER,
    )
    build_project_card(
        "card-newspaper.svg",
        "newspaper",
        "THE DEVELOPER DAILY",
        "LIVING 1930s BROADSHEET ENGINEERING PORTFOLIO",
        "LIVE · .engineer",
        "Interactive vintage broadsheet portfolio featuring 8 route-synced editions, custom SVG architectural illustrations, AI voice assistant & live GitHub API telemetry.",
        "Next.js 16 App Router  ->  GSAP + Framer  ->  GitHub GraphQL API",
        ["NEXT.JS 16", "REACT 19", "TYPESCRIPT", "GSAP", "TAILWIND"],
        BLUE,
    )

    build_header("head-credentials.svg", "03", "HONORS & CREDENTIALS", "VERIFIED EXCELLENCE", AMBER)
    build_credentials()

    build_header("head-stack.svg", "04", "ARCHITECTURE MATRIX", "PRODUCTION STACK", VIOLET)
    build_stack()

    build_header("head-cadence.svg", "05", "COMMIT TELEMETRY", "CONTRIBUTION CADENCE", EMERALD)
    build_header("head-connect.svg", "06", "DIRECT CHANNELS", "INITIATE CONNECTION", CYAN)

    build_button("btn-portfolio.svg", "PORTFOLIO", "portfolioaryanjadaun.engineer", CYAN, "web")
    build_button("btn-linkedin.svg", "LINKEDIN", "in/aryansinghjadaun", BLUE, "in")
    build_button("btn-email.svg", "DIRECT EMAIL", "aryansinghjadaun@gmail.com", EMERALD, "mail")
    build_footer()
