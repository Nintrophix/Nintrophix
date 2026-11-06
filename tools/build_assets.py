"""Generates the engineering-drawing themed SVGs for the GitHub profile README.

Every asset is emitted twice (dark = blueprint, light = drafting paper) from the
same geometry, so the README can swap them with <picture> + prefers-color-scheme.

    python tools/build_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

THEMES = {
    "dark": dict(bg="#0a1a2f", grid="#10294a", grid2="#163659", line="#9fd8ff",
                 dim="#ffb454", text="#e8f2ff", muted="#6f8fb5", scan="#5eead4"),
    "light": dict(bg="#f5f1e6", grid="#ebe4d3", grid2="#ddd3bd", line="#1d2733",
                  dim="#c2410c", text="#1d2733", muted="#857a66", scan="#0f766e"),
}


def t(x, y, s, size=12, fill="text", weight=400, anchor="start", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="var(--{fill})" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>'
            f'{escape(s)}</text>')


def wrap(svg_body, w, h, c):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">
<defs>
  <pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="var(--grid)" stroke-width="1"/></pattern>
  <pattern id="G" width="100" height="100" patternUnits="userSpaceOnUse"><rect width="100" height="100" fill="url(#g)"/><path d="M100 0H0V100" fill="none" stroke="var(--grid2)" stroke-width="1"/></pattern>
  <marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 2L10 5L0 8z" fill="var(--dim)"/></marker>
</defs>
<rect width="{w}" height="{h}" rx="10" fill="var(--bg)"/>
{svg_body}
</svg>'''
    for k, v in c.items():  # inline real colors; var() in presentation attrs is unreliable
        s = s.replace(f"var(--{k})", v)
    return s


def sheet_frame(w, h, cols, rows, inset=14, band=14):
    """Outer border + zone band with reference letters/numbers, like a real drawing sheet."""
    o = [f'<rect x="{inset}" y="{inset}" width="{w-2*inset}" height="{h-2*inset}" fill="none" stroke="var(--line)" stroke-width="1"/>',
         f'<rect x="{inset+band}" y="{inset+band}" width="{w-2*inset-2*band}" height="{h-2*inset-2*band}" fill="url(#G)" stroke="var(--line)" stroke-width="1.6"/>']
    cw = (w - 2 * inset) / cols
    for i in range(cols):
        cx = inset + cw * (i + .5)
        if i:
            x = inset + cw * i
            o += [f'<path d="M{x} {inset}v{band}M{x} {h-inset-band}v{band}" stroke="var(--line)"/>']
        o += [t(cx, inset + 10.5, str(i + 1), 9, "muted", anchor="middle"),
              t(cx, h - inset - 3.5, str(i + 1), 9, "muted", anchor="middle")]
    rh = (h - 2 * inset) / rows
    for j in range(rows):
        cy = inset + rh * (j + .5) + 3
        if j:
            y = inset + rh * j
            o += [f'<path d="M{inset} {y}h{band}M{w-inset-band} {y}h{band}" stroke="var(--line)"/>']
        o += [t(inset + 7, cy, "ABCD"[j], 9, "muted", anchor="middle"),
              t(w - inset - 7, cy, "ABCD"[j], 9, "muted", anchor="middle")]
    return "\n".join(o)


# ---------------------------------------------------------------- header
def header(c):
    W, H = 1200, 440
    o = [sheet_frame(W, H, 8, 3)]

    # --- left: name block
    o += [t(70, 92, "DWG. 001 — GENERAL ARRANGEMENT", 12, "muted", ls=3),
          f'<path d="M70 104h300" stroke="var(--muted)" stroke-dasharray="2 4"/>',
          t(66, 172, "KRITHIV", 72, "text", 800, ls=6),
          t(66, 246, "SHANKAR", 72, "dim", 800, ls=6),
          t(70, 284, "B.TECH CSE · SRM IST, CHENNAI · CGPA 8.88", 14, "muted", ls=1.5),
          t(70, 316, "I build software that sees, listens & teaches.", 18, "text")]

    # --- right: the part (a mounting plate) -------------------------------
    plate = ("M700 96 H850 v18 a14 14 0 0 0 14 14 h32 a14 14 0 0 0 14 -14 v-18 H1060 "
             "a16 16 0 0 1 16 16 V262 a16 16 0 0 1 -16 16 H700 a16 16 0 0 1 -16 -16 V112 a16 16 0 0 1 16 -16 Z")
    o += [f'<path d="{plate}" fill="var(--bg)" fill-opacity=".55" stroke="var(--line)" stroke-width="2.2"/>']
    holes = [(740, 146, 12), (740, 228, 12), (1020, 146, 12), (1020, 228, 12), (880, 190, 34)]
    for x, y, r in holes:
        e = r + 12
        o += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="var(--line)" stroke-width="2"/>',
              f'<path d="M{x-e} {y}H{x+e}M{x} {y-e}V{y+e}" stroke="var(--muted)" stroke-width=".8" stroke-dasharray="10 3 2 3"/>']
    o += ['<circle cx="880" cy="190" r="22" fill="none" stroke="var(--line)" stroke-width="1" stroke-dasharray="3 3"/>']

    # dimensions
    o += [f'<path d="M684 284v32M1076 284v32M1084 96h40M1084 278h40" stroke="var(--dim)" stroke-width=".8"/>',
          f'<path d="M686 308H1074" stroke="var(--dim)" stroke-width="1" marker-start="url(#a)" marker-end="url(#a)"/>',
          f'<rect x="846" y="300" width="68" height="16" fill="var(--bg)"/>',
          t(880, 312, "392.00", 12, "dim", anchor="middle"),
          f'<path d="M1116 98V276" stroke="var(--dim)" stroke-width="1" marker-start="url(#a)" marker-end="url(#a)"/>',
          f'<rect x="1108" y="160" width="16" height="58" fill="var(--bg)"/>',
          t(1120, 189, "182.00", 12, "dim", anchor="middle", extra='transform="rotate(-90 1120 189)" dominant-baseline="middle"'),
          f'<path d="M1029 137L1064 76H1150" fill="none" stroke="var(--dim)" stroke-width=".8" marker-start="url(#a)"/>',
          t(1068, 70, "4× Ø24 THRU", 12, "dim"),
          f'<path d="M856 166L800 76H700" fill="none" stroke="var(--dim)" stroke-width=".8" marker-start="url(#a)"/>',
          t(700, 70, "Ø68 / Ø44 CBORE", 12, "dim")]

    # --- the one animation: a scan pass that "detects" each feature --------
    DUR, SWEEP, X0, X1 = 8, .42, 670, 1090
    o += [f'''<g opacity="0">
  <animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;.02;{SWEEP};{SWEEP+.04};1" values="0;1;1;0;0"/>
  <rect x="{X0-40}" y="90" width="40" height="194" fill="var(--scan)" opacity=".12">
    <animate attributeName="x" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{SWEEP};1" values="{X0-40};{X1-40};{X1-40}"/>
  </rect>
  <line x1="{X0}" x2="{X0}" y1="84" y2="290" stroke="var(--scan)" stroke-width="1.6">
    <animate attributeName="x1" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{SWEEP};1" values="{X0};{X1};{X1}"/>
    <animate attributeName="x2" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{SWEEP};1" values="{X0};{X1};{X1}"/>
  </line>
</g>''']
    for x, y, r in holes:
        f = round((x - X0) / (X1 - X0) * SWEEP, 3)
        s, k = r + 7, 7
        br = (f"M{x-s} {y-s+k}v{-k}h{k}M{x+s-k} {y-s}h{k}v{k}M{x+s} {y+s-k}v{k}h{-k}"
              f"M{x-s+k} {y+s}h{-k}v{-k}")
        o += [f'''<path d="{br}" fill="none" stroke="var(--scan)" stroke-width="2" opacity="0">
  <animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{f};{f+.015};.9;.96;1" values="0;0;1;1;0;0"/>
</path>''']
    o += [f'''<g opacity="0">
  <animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" keyTimes="0;{SWEEP+.02};{SWEEP+.05};.9;.96;1" values="0;0;1;1;0;0"/>
  {t(70, 372, "› scan complete · 5 features · σ 0.04 mm · 0 open issues", 13, "scan")}
</g>''']
    o += [t(70, 396, "github.com/Nintrophix", 12, "muted", ls=1)]

    # --- title block -------------------------------------------------------
    x0, y0, x1, y1 = 744, 334, 1172, 412
    o += [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="var(--bg)" stroke="var(--line)" stroke-width="1.6"/>',
          f'<path d="M{x0} 360H{x1}M{x0} 386H{x1}M1060 {y0}V360M876 360V{y1}M968 360V386M1060 360V{y1}M968 386V{y1}" stroke="var(--line)" stroke-width=".8"/>']

    def cell(x, y, label, val, vfill="text", vsize=11):
        return t(x + 6, y + 9, label, 7, "muted", ls=1) + t(x + 6, y + 21, val, vsize, vfill, 700)

    o += [cell(x0, y0, "TITLE", "KRITHIV SHANKAR — DEVELOPER, CS STUDENT", vsize=11),
          cell(1060, y0, "DWG NO.", "NTX-001", "dim"),
          cell(x0, 360, "DRAWN", "K. SHANKAR"),
          cell(876, 360, "SCALE", "1 : 1"),
          cell(968, 360, "UNITS", "mm"),
          cell(1060, 360, "REV", "2026.11", "dim"),
          cell(x0, 386, "MATERIAL", "PY · TS · JS · RUST"),
          cell(876, 386, "TOLERANCE", "±0 BUGS*"),
          cell(968, 386, "CHECKED", "CAFFEINE"),
          cell(1060, 386, "SHEET", "1 OF 1")]
    return wrap("\n".join(o), W, H, c)


# ---------------------------------------------------------------- project cards
GLYPHS = {
    # Friday — voice: waveform passing through a microphone capsule
    "friday": '''<rect x="455" y="58" width="44" height="78" rx="22" fill="none" stroke="var(--line)" stroke-width="2"/>
<path d="M440 112a37 37 0 0 0 74 0M477 149v22M457 171h40" fill="none" stroke="var(--line)" stroke-width="2"/>
<path d="M392 104h14l6-18 8 40 8-58 8 70 7-46 6 22h12M508 104h12l6-14 7 28 8-40 7 46 6-20h14" fill="none" stroke="var(--dim)" stroke-width="1.6"/>''',
    # Debug Odyssey — a compiler error being traced to its line
    "debug": '''<path d="M430 64l-30 42 30 42M524 64l30 42-30 42" fill="none" stroke="var(--line)" stroke-width="2.2"/>
<path d="M452 88h46M452 104h30M452 120h40" stroke="var(--line)" stroke-width="2"/>
<path d="M484 98l12 12m0-12l-12 12" stroke="var(--dim)" stroke-width="2.4"/>
<path d="M496 110l26 50h34" fill="none" stroke="var(--dim)" stroke-width=".9"/>
<text x="526" y="172" font-size="10" fill="var(--dim)">E0425</text>''',
    # Lost & Found Hub — a luggage tag with an eyelet
    "lost": '''<path d="M420 74h88l34 34-34 34h-88z" fill="none" stroke="var(--line)" stroke-width="2.2" transform="rotate(-12 470 108)"/>
<circle cx="510" cy="100" r="7" fill="none" stroke="var(--line)" stroke-width="2"/>
<path d="M517 98c22-6 30-26 22-40" fill="none" stroke="var(--line)" stroke-width="1.6" stroke-dasharray="3 3"/>
<path d="M434 110h44M438 124h28" stroke="var(--dim)" stroke-width="2" transform="rotate(-12 470 108)"/>
<path d="M430 160h18m-9-9v18" stroke="var(--dim)" stroke-width="1.6"/><circle cx="439" cy="160" r="5" fill="none" stroke="var(--dim)"/>''',
    # Metal Scanner — a part between caliper jaws
    "metal": '''<g transform="translate(-14 0)"><path d="M396 66h168v16H396zM406 82v62l12 12V82M554 82v62l-12 12V82" fill="none" stroke="var(--line)" stroke-width="2"/>
<rect x="430" y="94" width="100" height="50" rx="6" fill="none" stroke="var(--line)" stroke-width="2"/>
<circle cx="452" cy="119" r="8" fill="none" stroke="var(--line)" stroke-width="1.6"/><circle cx="508" cy="119" r="8" fill="none" stroke="var(--line)" stroke-width="1.6"/>
<path d="M432 164H528" stroke="var(--dim)" marker-start="url(#a)" marker-end="url(#a)"/>
<text x="480" y="180" font-size="10" fill="var(--dim)" text-anchor="middle">100.00 ±0.5</text></g>''',
}

PROJECTS = [
    ("debug", "A", "DEBUG ODYSSEY", ["Story-driven ed-tech platform that teaches", "beginners to read, decode & fix compiler", "errors across five languages."],
     "FastAPI · Monaco · Docker · Cloud Run", "◆ CELESTIA 2.0 FINALIST"),
    ("friday", "B", "FRIDAY", ["Voice-controlled desktop assistant —", "hands-free commands that automate", "everyday tasks on your computer."],
     "Python · LLM API · faster-whisper · PySide6", "◆ OFFLINE STT VIA VOSK"),
    ("lost", "C", "LOST & FOUND HUB", ["Campus portal to report, search, claim", "and recover items — with real-time", "private chat between students."],
     "Node · Express · Socket.io · Supabase", "◆ LIVE ON RENDER"),
    ("metal", "D", "METAL SCANNER", ["Measures metal part outlines & bolt-hole", "positions from camera frames with", "contour tracing — mm-level accuracy."],
     "TypeScript · React · Canvas · WebRTC", "◆ BUILT AT IRONTRONICS"),
]


def card(c, key, letter, name, desc, stack, badge):
    W, H = 600, 260
    o = [f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="url(#G)" stroke="var(--line)" stroke-width="1.6"/>',
         f'<path d="M10 40H{W-10}" stroke="var(--line)" stroke-width=".8"/>',
         f'<circle cx="32" cy="25" r="9" fill="none" stroke="var(--dim)" stroke-width="1.4"/>',
         t(32, 29, letter, 11, "dim", 700, "middle"),
         t(50, 29, f"DETAIL {letter}", 11, "muted", ls=2),
         t(W - 26, 29, "SCALE 2 : 1", 11, "muted", anchor="end", ls=2),
         t(30, 86, name, 28, "text", 800, ls=1.5)]
    for i, line in enumerate(desc):
        o.append(t(30, 118 + i * 21, line, 13.5, "text"))
    o += [f'<path d="M30 196H{W-30}" stroke="var(--muted)" stroke-dasharray="2 4"/>',
          t(30, 220, stack, 12, "dim", 700),
          t(30, 238, badge, 10, "muted", ls=1.5),
          f'<g transform="translate(20 6)">{GLYPHS[key]}</g>']
    return wrap("\n".join(o), W, H, c)


# ---------------------------------------------------------------- material spec (skills)
SPEC = [
    ("LANGUAGES", "Python · TypeScript · JavaScript · C · Rust · SQL · HTML/CSS"),
    ("WEB / API", "React · Node.js · Express · FastAPI · Django · Flask · Tailwind"),
    ("ML / VISION", "NumPy · Pandas · scikit-learn · XGBoost · CatBoost · OpenCV"),
    ("REAL-TIME", "Socket.io · WebSockets · WebRTC · Canvas API · ntfy"),
    ("DATA", "PostgreSQL · Supabase · SQLite · MS SQL Server · Full-Text Search"),
    ("SHIP", "Docker · Git · Vercel · Render · Netlify · Google Cloud Run · Vite"),
]


def spec(c):
    W, RH, TOP = 1200, 34, 64
    H = TOP + RH * (len(SPEC) + 1) + 26
    o = [f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="url(#G)" stroke="var(--line)" stroke-width="1.6"/>',
         t(30, 42, "MATERIAL SPECIFICATION", 14, "text", 800, ls=3),
         t(W - 30, 42, "PARTS LIST · TABLE 1", 11, "muted", anchor="end", ls=2)]
    x = [30, 90, 290, 1060, W - 30]
    y = TOP
    o.append(f'<rect x="{x[0]}" y="{y}" width="{x[-1]-x[0]}" height="{RH*(len(SPEC)+1)}" fill="var(--bg)" stroke="var(--line)" stroke-width="1.4"/>')
    for xi in x[1:-1]:
        o.append(f'<path d="M{xi} {y}v{RH*(len(SPEC)+1)}" stroke="var(--line)" stroke-width=".8"/>')
    heads = ["ITEM", "DESIGNATION", "SPECIFICATION", "QTY"]
    for i, hd in enumerate(heads):
        o.append(t(x[i] + 12, y + 22, hd, 10, "muted", 700, ls=2))
    for r, (lab, val) in enumerate(SPEC):
        yy = y + RH * (r + 1)
        o.append(f'<path d="M{x[0]} {yy}H{x[-1]}" stroke="var(--line)" stroke-width="{1.2 if r == 0 else .5}"/>')
        o += [t(x[0] + 30, yy + 22, f"{r+1:02d}", 12, "dim", 700, "middle"),
              t(x[1] + 12, yy + 22, lab, 12, "text", 700, ls=1),
              t(x[2] + 12, yy + 22, val, 13, "text"),
              t(x[3] + 12, yy + 22, str(len(val.split(" · "))), 12, "dim", 700)]
    return wrap("\n".join(o), W, H, c)


def main():
    OUT.mkdir(exist_ok=True)
    for mode, c in THEMES.items():
        (OUT / f"header-{mode}.svg").write_text(header(c), encoding="utf-8")
        (OUT / f"spec-{mode}.svg").write_text(spec(c), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f"detail-{p[0]}-{mode}.svg").write_text(card(c, *p), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "svgs to", OUT)


if __name__ == "__main__":
    main()
