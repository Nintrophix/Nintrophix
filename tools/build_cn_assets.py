"""Generates the Cartoon-Network-themed SVGs for the GitHub profile README.

Everything is original vector art in a Saturday-morning cartoon style: thick
black outlines, offset drop shadows, checkerboard bumpers. Characters are
referenced by name only (no copyrighted character art is reproduced).
Every card carries its own solid background, so one file works in GitHub's
light and dark themes.

    python tools/build_cn_assets.py
"""
from pathlib import Path
from textwrap import wrap as twrap
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "cn"
DISPLAY = "'Arial Black','Arial Bold',Impact,'Helvetica Neue',sans-serif"
BODY = "Verdana,'DejaVu Sans',Geneva,sans-serif"
INK = "#111111"


def T(x, y, s, size=14, fill=INK, weight=400, anchor="start", family=BODY, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def outlined(x, y, s, size, fill, anchor="start", stroke=INK, sw=6, shadow=True):
    """Cartoon title text: offset shadow + fat outline + fill."""
    o = []
    common = f'x="{x}" y="{y}" font-family="{DISPLAY}" font-size="{size}" font-weight="900" text-anchor="{anchor}"'
    if shadow:
        o.append(f'<text {common} transform="translate(4 4)" fill="{INK}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round">{escape(s)}</text>')
    o.append(f'<text {common} fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke">{escape(s)}</text>')
    return "".join(o)


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{body}</svg>')


def checker(x, y, cols, rows, size, a="#ffffff", b=INK):
    o = []
    for r in range(rows):
        for c in range(cols):
            o.append(f'<rect x="{x + c * size}" y="{y + r * size}" width="{size}" height="{size}" fill="{a if (r + c) % 2 == 0 else b}"/>')
    return "".join(o)


def chip_w(s, size=12):
    return int(len(s) * size * 0.66) + 18


def chips(items, x0, y0, maxw, size=12, fill="#ffffff", gap=8, row_h=28):
    """Flowing pill chips. Returns (svg, bottom_y)."""
    o, x, y = [], x0, y0
    for s in items:
        w = chip_w(s, size)
        if x + w > x0 + maxw and x > x0:
            x, y = x0, y + row_h
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{row_h - 7}" rx="{(row_h - 7) / 2}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>')
        o.append(T(x + w / 2, y + row_h - 13, s, size, INK, 700, "middle"))
        x += w + gap
    return "".join(o), y + row_h


# ----------------------------------------------------------------------------- header
def header():
    w, h = 1000, 330
    dots = ('<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse">'
            '<circle cx="9" cy="9" r="3.2" fill="#ffb800"/></pattern>'
            '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
            '<rect width="4" height="2" fill="#000" opacity=".06"/></pattern>')
    o = [f'<rect width="{w}" height="{h}" rx="22" fill="#ffd400"/>',
         f'<rect width="{w}" height="{h}" rx="22" fill="url(#dots)"/>']
    # sunburst behind the logo
    rays = []
    for i in range(16):
        rays.append(f'<path d="M0 0 L420 -40 L420 40 Z" fill="#fff3a0" opacity=".55" transform="rotate({i * 22.5})"/>')
    o.append(f'<g transform="translate(170 165)"><g>{"".join(rays)}'
             '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="60s" repeatCount="indefinite"/></g></g>')
    # checkerboard "KS" channel logo (original letters, CN-bumper style)
    lx, ly, s = 60, 70, 110
    o.append(f'<rect x="{lx + 8}" y="{ly + 8}" width="{s * 2}" height="{s * 2}" fill="{INK}"/>')
    o.append(checker(lx, ly, 2, 2, s))
    o.append(f'<rect x="{lx}" y="{ly}" width="{s * 2}" height="{s * 2}" fill="none" stroke="{INK}" stroke-width="6"/>')
    for (cx, cy, ch, col) in [(0, 0, "K", "#111"), (1, 0, "S", "#fff"), (0, 1, "<", "#fff"), (1, 1, "/>", "#111")]:
        fs = 92 if len(ch) == 1 else 64
        o.append(T(lx + cx * s + s / 2, ly + cy * s + s / 2 + fs * 0.36, ch, fs, col, 900, "middle", DISPLAY))
    # title block
    o.append(T(330, 92, "NOW SHOWING ON CHANNEL NINTROPHIX", 15, INK, 900, family=DISPLAY, extra='letter-spacing="2"'))
    o.append(outlined(326, 166, "KRITHIV", 72, "#ffffff"))
    o.append(outlined(326, 238, "SHANKAR", 72, "#ff3ea5"))
    o.append(f'<rect x="330" y="258" width="600" height="38" rx="19" fill="#ffffff" stroke="{INK}" stroke-width="3.5"/>')
    o.append(T(630, 283, "B.Tech CSE @ SRM IST  ·  Intern @ Irontronics  ·  Logic Play", 14, INK, 700, "middle"))
    # ON AIR light
    o.append(f'<g transform="translate(838 52)"><rect width="112" height="38" rx="8" fill="{INK}"/>'
             f'<circle cx="20" cy="19" r="8" fill="#ff2a2a"><animate attributeName="opacity" values="1;.15;1" dur="1.2s" repeatCount="indefinite"/></circle>'
             + T(68, 26, "ON AIR", 16, "#ffffff", 900, "middle", DISPLAY) + '</g>')
    # scrolling checker band along the bottom
    band = checker(0, 0, 70, 1, 16)
    o.append(f'<clipPath id="hc"><rect width="{w}" height="{h}" rx="22"/></clipPath>')
    o.append(f'<g clip-path="url(#hc)"><g transform="translate(0 {h - 16})"><g>{band}{checker(1120, 0, 70, 1, 16)}'
             '<animateTransform attributeName="transform" type="translate" from="0 0" to="-32 0" dur="1.2s" repeatCount="indefinite"/></g></g>'
             f'<rect width="{w}" height="{h}" fill="url(#scan)"/></g>')
    o.append(f'<rect x="3" y="3" width="{w - 6}" height="{h - 6}" rx="20" fill="none" stroke="{INK}" stroke-width="6"/>')
    return svg(w, h, "".join(o), dots)


# ----------------------------------------------------------------------------- motifs
def motif_flask():  # Friday — Dexter's Lab
    bubbles = "".join(
        f'<circle cx="{cx}" cy="0" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2">'
        f'<animate attributeName="cy" values="40;-60" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for cx, r, d, b in [(-8, 6, 2.2, 0), (10, 4, 1.8, .6), (0, 5, 2.6, 1.2)])
    bars = "".join(
        f'<rect x="{-56 + i * 16}" y="-8" width="9" height="16" rx="4" fill="{INK}">'
        f'<animate attributeName="height" values="8;{20 + (i * 7) % 26};8" dur="{0.7 + (i % 3) * .2}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="-4;{-(10 + (i * 7) % 26 / 2)};-4" dur="{0.7 + (i % 3) * .2}s" repeatCount="indefinite"/></rect>'
        for i in range(8))
    return (f'<g>{bubbles}</g>'
            f'<path d="M-16 -30 V0 L-48 52 Q-52 62 -40 62 H40 Q52 62 48 52 L16 0 V-30 Z" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-30 22 L-46 52 Q-49 58 -40 58 H40 Q49 58 46 52 L30 22 Z" fill="#39d353"/>'
            f'<rect x="-22" y="-38" width="44" height="10" rx="3" fill="#ffffff" stroke="{INK}" stroke-width="4"/>')


def motif_plate():  # Irontronics — Samurai Jack
    holes = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#2b2b2b" stroke="{INK}" stroke-width="3"/>'
                    for x, y in [(-38, -30), (38, -30), (-38, 30), (38, 30)])
    return (f'<rect x="-62" y="-52" width="124" height="104" rx="10" fill="#c9d1d9" stroke="{INK}" stroke-width="4"/>'
            f'{holes}<circle r="16" fill="#2b2b2b" stroke="{INK}" stroke-width="3"/>'
            f'<line x1="-62" x2="62" y1="0" y2="0" stroke="#ff2a2a" stroke-width="3">'
            f'<animate attributeName="y1" values="-52;52;-52" dur="3s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="-52;52;-52" dur="3s" repeatCount="indefinite"/></line>'
            f'<path d="M-62 74 H62" stroke="{INK}" stroke-width="2.5"/><path d="M-62 66 V82 M62 66 V82" stroke="{INK}" stroke-width="2.5"/>'
            + T(0, 96, "± mm", 13, INK, 900, "middle", DISPLAY))


def motif_dial():  # Logic Play — Ben 10
    ticks = "".join(f'<rect x="-3" y="-60" width="6" height="12" fill="{INK}" transform="rotate({i * 45})"/>' for i in range(8))
    return (f'<rect x="-70" y="-22" width="140" height="44" rx="10" fill="#2b2b2b" stroke="{INK}" stroke-width="4"/>'
            f'<circle r="56" fill="#1e1e1e" stroke="{INK}" stroke-width="4"/>'
            f'<g>{ticks}<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/></g>'
            f'<circle r="38" fill="#39ff6a" stroke="{INK}" stroke-width="4"><animate attributeName="fill" values="#39ff6a;#b6ffc8;#39ff6a" dur="1.6s" repeatCount="indefinite"/></circle>'
            + T(0, 9, "{ }", 26, INK, 900, "middle", DISPLAY))


def motif_house():  # Debug Odyssey — Courage the Cowardly Dog
    return (f'<circle cx="34" cy="-44" r="30" fill="#fff6c9" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-80 54 Q0 2 80 54 Z" fill="#6b3fa0" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-30 34 V2 L-6 -18 L18 2 V34 Z" fill="#f2e6c9" stroke="{INK}" stroke-width="3.5"/>'
            f'<rect x="-16" y="10" width="10" height="10" fill="#ffd400" stroke="{INK}" stroke-width="2"><animate attributeName="fill" values="#ffd400;#5a4a00;#ffd400" dur="2.4s" repeatCount="indefinite"/></rect>'
            f'<path d="M30 34 V-6" stroke="{INK}" stroke-width="3"/><g transform="translate(30 -6)"><g>'
            f'<path d="M0 0 L0 -18 M0 0 L16 8 M0 0 L-16 8" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/></g></g>'
            f'<g opacity=".95"><g>' + T(-44, -40, "SyntaxError", 12, "#ff3ea5", 900, "middle", DISPLAY)
            + '<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="2s" repeatCount="indefinite"/></g></g>')


def motif_search():  # Lost & Found Hub — Ed, Edd n Eddy
    return (f'<rect x="-58" y="-30" width="76" height="70" rx="6" fill="#d9a066" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-58 -10 H18" stroke="{INK}" stroke-width="3"/>'
            + T(-20, 30, "?", 40, "#ffffff", 900, "middle", DISPLAY,
                'stroke="#111" stroke-width="3" paint-order="stroke"')
            + f'<g><circle cx="34" cy="10" r="24" fill="#bdf2ff" fill-opacity=".7" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M51 27 L70 46" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            '<animateTransform attributeName="transform" type="translate" values="0 0;-10 -6;0 0" dur="2.6s" repeatCount="indefinite"/></g>'
            f'<g transform="translate(-30 -62)"><path d="M0 0 H56 Q64 0 64 8 V26 Q64 34 56 34 H18 L6 44 L8 34 H0 Q-8 34 -8 26 V8 Q-8 0 0 0 Z" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
            + "".join(f'<circle cx="{12 + i * 16}" cy="17" r="4" fill="{INK}"><animate attributeName="opacity" values=".2;1;.2" dur="1.2s" begin="{i * .3}s" repeatCount="indefinite"/></circle>' for i in range(3))
            + '</g>')


# ----------------------------------------------------------------------------- episode cards
def card(ep, when, title, vibe, body, stack, bg, accent, motif, title_fill="#ffffff"):
    w = 480
    lines = []
    for para in body:
        lines += twrap(para, 36)
    y_body = 152
    text_end = y_body + 20 * (len(lines) - 1)
    chip_svg, chip_end = chips(stack, 26, max(text_end + 20, 234), w - 52, 11, row_h=26)
    h = chip_end + 22
    o = [f'<rect x="10" y="10" width="{w - 16}" height="{h - 16}" rx="20" fill="{INK}"/>',
         f'<rect x="3" y="3" width="{w - 16}" height="{h - 16}" rx="18" fill="{bg}" stroke="{INK}" stroke-width="5"/>',
         f'<clipPath id="top"><rect x="3" y="3" width="{w - 16}" height="{h - 16}" rx="18"/></clipPath>',
         f'<g clip-path="url(#top)"><rect x="0" y="0" width="{w}" height="46" fill="{accent}"/>'
         f'<path d="M0 46 H{w}" stroke="{INK}" stroke-width="4"/></g>',
         T(24, 31, f"EP. {ep}", 16, "#ffffff", 900, family=DISPLAY, extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke"'),
         T(100, 30, when, 12, "#ffffff", 700, extra=f'stroke="{INK}" stroke-width="2.5" paint-order="stroke"'),
         checker(w - 66, 13, 2, 1, 20),
         f'<rect x="{w - 66}" y="13" width="40" height="20" fill="none" stroke="{INK}" stroke-width="2.5"/>',
         outlined(22, 96, title, 30, title_fill, sw=5, shadow=True),
         T(24, 122, vibe, 12.5, INK, 700, extra='font-style="italic"')]
    o += [T(24, y_body + i * 20, ln, 13, INK) for i, ln in enumerate(lines)]
    o.append(f'<g transform="translate(376 {178 if len(lines) < 5 else 186}) scale(.82)">{motif}</g>')
    o.append(chip_svg)
    return svg(w, h, "".join(o))


CARDS = {
    "ep-irontronics": dict(
        ep="01", when="MAY 2026 – NOW", title="Irontronics",
        vibe="Intern · Samurai Jack-grade precision",
        body=["Scans metal part outlines and bolt-hole positions from camera frames with contour tracing and binary segmentation, hitting millimetre-level accuracy via pixel-to-mm calibration."],
        stack=["Python", "JavaScript", "TypeScript", "React", "Canvas API", "WebRTC", "Blob API", "HTML", "CSS3"],
        bg="#ffe1e1", accent="#e0242f", motif=motif_plate()),
    "ep-logicplay": dict(
        ep="02", when="NOV 2026 – NOW", title="Logic Play",
        vibe="Core Member · it's hero time (Ben 10)",
        body=["Builds and optimises interactive features, algorithms and logic systems for club projects and event platforms.",
              "Debugs, tests and deploys with cross-functional teams."],
        stack=["Algorithms", "Logic systems", "Testing", "Deployment"],
        bg="#dcffe4", accent="#1a9e3f", motif=motif_dial()),
    "ep-friday": dict(
        ep="03", when="AUG 2026", title="Friday",
        vibe="“Computer!” — very Dexter's Lab",
        body=["A voice-controlled desktop assistant, inspired by Iron Man, that automates everyday computer tasks through hands-free commands."],
        stack=["Python", "LLM API", "VOSK", "faster-whisper", "PySide6", "PyQt", "pyttsx3"],
        bg="#e3f1ff", accent="#1f6fd1", motif=motif_flask()),
    "ep-debugodyssey": dict(
        ep="04", when="SEP 2026", title="Debug Odyssey",
        vibe="Errors so scary, Courage would bolt",
        body=["A story-driven full-stack Ed-Tech platform that teaches beginners to read, decode and fix compiler errors across five languages."],
        stack=["FastAPI", "Monaco Editor", "Python", "JS", "Java", "C++", "Docker", "Vercel", "Cloud Run"],
        bg="#efe3ff", accent="#7a3fc2", motif=motif_house()),
    "ep-lostfound": dict(
        ep="05", when="NOV 2026", title="Lost & Found",
        vibe="Everything labelled, Double D-style",
        body=["A full-stack campus portal where students report, search, claim and recover items, with real-time private chat."],
        stack=["Node.js", "Express", "Socket.io", "PostgreSQL", "Supabase", "Tailwind", "EJS", "bcrypt", "Helmet", "Sharp", "Render"],
        bg="#fff6c9", accent="#e08a00", motif=motif_search()),
}


# ----------------------------------------------------------------------------- skills: the Powerpuff formula
def beaker(cx, cy, color, label):
    return (f'<g transform="translate({cx} {cy})">'
            f'<path d="M-30 -42 V18 Q-30 40 0 40 Q30 40 30 18 V-42" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-27 -6 V18 Q-27 37 0 37 Q27 37 27 18 V-6 Z" fill="{color}">'
            f'<animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="'
            f'M-27 -6 Q0 -14 27 -6 V18 Q27 37 0 37 Q-27 37 -27 18 Z;M-27 -10 Q0 0 27 -10 V18 Q27 37 0 37 Q-27 37 -27 18 Z;M-27 -6 Q0 -14 27 -6 V18 Q27 37 0 37 Q-27 37 -27 18 Z"/></path>'
            f'<rect x="-36" y="-48" width="72" height="9" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="4"/></g>'
            + T(cx + 46, cy - 4, label, 20, INK, 900, family=DISPLAY))


def skills():
    w = 1000
    cols = [
        ("#ff6fb5", "#ffe0ef", "LANGUAGES", "Blossom-pink", ["Python", "C", "JavaScript", "Rust", "SQL", "HTML", "CSS"]),
        ("#57b8ff", "#e0f1ff", "FRAMEWORKS", "Bubbles-blue", ["Django", "Flask", "FastAPI", "Streamlit", "Node.js", "Express.js", "Tailwind CSS"]),
        ("#5fd068", "#e2f8e3", "LIBRARIES", "Buttercup-green", ["React", "NumPy", "Pandas", "Scikit-learn", "XGBoost", "CatBoost", "OpenCV", "Socket.io"]),
    ]
    o, bottoms = [], []
    colw = 300
    for i, (c, soft, label, sub, items) in enumerate(cols):
        x = 30 + i * (colw + 15)
        o.append(f'<rect x="{x}" y="128" width="{colw}" height="__H__" rx="16" fill="{soft}" stroke="{INK}" stroke-width="3.5"/>')
        o.append(beaker(x + 46, 190, c, label))
        o.append(T(x + 92, 214, sub, 12, INK, 700, extra='font-style="italic"'))
        ch, b = chips(items, x + 16, 252, colw - 32, 12, row_h=30)
        o.append(ch)
        bottoms.append(b)
    col_bottom = max(bottoms) + 10
    o = [s.replace("__H__", str(col_bottom - 128)) for s in o]
    # Chemical X band
    y = col_bottom + 28
    tech = ["REST APIs", "Machine Learning", "Agentic AI", "WebSockets", "Full-Text Search", "Authentication",
            "Web Security", "Version Control", "ntfy", "Docker", "Git", "GitHub", "VS Code", "Antigravity",
            "Render", "Vercel", "Netlify", "Supabase", "PostgreSQL", "SQLite", "MS SQL Server", "Vite",
            "Jupyter", "Google Colab", "Figma"]
    ch, b = chips(tech, 200, y + 22, w - 240, 12, fill="#ffffff", row_h=30)
    band_h = b - y + 14
    o.append(f'<rect x="30" y="{y}" width="{w - 60}" height="{band_h}" rx="16" fill="#2a2a2a" stroke="{INK}" stroke-width="3.5"/>')
    o.append(f'<g transform="translate(110 {y + band_h / 2})">'
             f'<rect x="-44" y="-34" width="88" height="70" rx="10" fill="{INK}" stroke="#ffffff" stroke-width="3"/>'
             + T(0, 4, "X", 44, "#ffffff", 900, "middle", DISPLAY)
             + f'<circle cx="0" cy="-8" r="46" fill="none" stroke="#ff3ea5" stroke-width="3" opacity=".8">'
             '<animate attributeName="r" values="40;58;40" dur="2s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".9;0;.9" dur="2s" repeatCount="indefinite"/></circle>'
             + T(0, 56, "CHEMICAL X", 13, "#ffffff", 900, "middle", DISPLAY) + '</g>')
    o.append(ch)
    h = y + band_h + 26
    head = [f'<rect x="10" y="10" width="{w - 16}" height="{h - 16}" rx="22" fill="{INK}"/>',
            f'<rect x="3" y="3" width="{w - 16}" height="{h - 16}" rx="20" fill="#fff8fc" stroke="{INK}" stroke-width="5"/>',
            outlined(36, 76, "THE POWERPUFF FORMULA", 40, "#ff6fb5", sw=6),
            T(40, 108, "Sugar (languages) + spice (frameworks) + everything nice (libraries) + a dash of Chemical X (tools & tech)", 13, INK, 700)]
    return svg(w, h, "".join(head + o))


# ----------------------------------------------------------------------------- footer bumper
def footer():
    w, h = 1000, 150
    o = [f'<rect width="{w}" height="{h}" rx="22" fill="{INK}"/>',
         f'<clipPath id="fc"><rect width="{w}" height="{h}" rx="22"/></clipPath>',
         f'<g clip-path="url(#fc)"><g>{checker(0, 0, 66, 1, 16)}{checker(1056, 0, 66, 1, 16)}'
         '<animateTransform attributeName="transform" type="translate" from="0 0" to="32 0" dur="1.2s" repeatCount="indefinite"/></g>'
         f'<g transform="translate(0 {h - 16})"><g>{checker(-1056, 0, 132, 1, 16)}'
         '<animateTransform attributeName="transform" type="translate" from="0 0" to="-32 0" dur="1.2s" repeatCount="indefinite"/></g></g></g>',
         outlined(500, 86, "WE'LL BE RIGHT BACK", 40, "#ffd400", "middle", stroke="#ffffff", sw=5, shadow=False),
         T(500, 116, "after these messages from the portfolio, LinkedIn and inbox below", 13, "#ffffff", 700, "middle")]
    return svg(w, h, "".join(o))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"header.svg": header(), "skills.svg": skills(), "footer.svg": footer()}
    for name, kw in CARDS.items():
        files[f"{name}.svg"] = card(**kw)
    for name, s in files.items():
        (OUT / name).write_text(s, encoding="utf-8")
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
