"""Simplified fan-art figures of Cartoon Network characters, drawn as plain SVG.

Each function returns an SVG fragment with its origin at the character's feet
(centre bottom), facing the viewer, about 120 units tall. Callers translate and
scale them into place.
"""

INK = "#111111"
SKIN = "#ffd9b8"


def _limb(x1, y1, x2, y2, fill, w=7):
    """Outlined cartoon limb: fat ink stroke under a thinner coloured stroke."""
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="{w + 5}" stroke-linecap="round"/>'
            f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{fill}" stroke-width="{w}" stroke-linecap="round"/>')


def _bob(inner, dy=3, dur=2.2):
    return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 -{dy};0 0" dur="{dur}s" repeatCount="indefinite"/></g>')


S = f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"'


def dexter():
    """Boy genius: flat orange hair, big glasses, lab coat, purple gloves, black boots."""
    hair, glove = "#ff6a13", "#8b4dff"
    o = [
        f'<rect x="-21" y="-12" width="17" height="12" rx="5" fill="{INK}"/>',
        f'<rect x="4" y="-12" width="17" height="12" rx="5" fill="{INK}"/>',
        _limb(-16, -58, -30, -32, "#ffffff", 8),
        f'<circle cx="-31" cy="-29" r="6.5" fill="{glove}" {S}/>',
        f'<path d="M-17 -64 L-27 -10 H27 L17 -64 Z" fill="#ffffff" {S}/>',
        f'<path d="M0 -60 V-12 M-6 -64 L0 -54 L6 -64" stroke="{INK}" stroke-width="2.2" fill="none"/>',
        # raised arm, pointing like he's calling out to Computer
        '<g>' + _limb(16, -58, 34, -80, "#ffffff", 8)
        + f'<circle cx="36" cy="-83" r="6.5" fill="{glove}" {S}/>'
        '<animateTransform attributeName="transform" type="rotate" values="0 16 -58;-8 16 -58;0 16 -58" dur="1.4s" repeatCount="indefinite"/></g>',
        f'<ellipse cx="-28" cy="-84" rx="4" ry="5" fill="{SKIN}" {S}/>',
        f'<ellipse cx="28" cy="-84" rx="4" ry="5" fill="{SKIN}" {S}/>',
        f'<ellipse cx="0" cy="-84" rx="28" ry="21" fill="{SKIN}" {S}/>',
        f'<path d="M-29 -86 Q-31 -112 0 -112 Q31 -112 29 -86 Q22 -97 0 -97 Q-22 -97 -29 -86 Z" fill="{hair}" {S}/>',
        f'<rect x="-25" y="-92" width="22" height="14" rx="3" fill="#e4f4ff" {S}/>',
        f'<rect x="3" y="-92" width="22" height="14" rx="3" fill="#e4f4ff" {S}/>',
        f'<path d="M-3 -86 H3" stroke="{INK}" stroke-width="3"/>',
        f'<path d="M-8 -71 Q0 -67 8 -71" stroke="{INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
        f'<g fill="{INK}">'
        '<text x="44" y="-98" font-family="\'Arial Black\',Impact,sans-serif" font-size="13" font-weight="900">'
        'COMPUTER!<animate attributeName="opacity" values="0;1;1;0" dur="2.8s" repeatCount="indefinite"/></text></g>',
    ]
    return "".join(o)


def courage():
    """Pink dog with black droopy ears, trembling, paws on his cheeks."""
    pink = "#f2a2c4"
    o = [
        _limb(-6, -26, -9, -4, pink, 4), _limb(6, -26, 9, -4, pink, 4),
        f'<ellipse cx="-11" cy="-3" rx="7" ry="3.5" fill="{pink}" {S}/>',
        f'<ellipse cx="11" cy="-3" rx="7" ry="3.5" fill="{pink}" {S}/>',
        f'<path d="M10 -26 Q26 -24 24 -10" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>',
        f'<ellipse cx="0" cy="-40" rx="13" ry="19" fill="{pink}" {S}/>',
        _limb(-9, -50, -22, -70, pink, 4), _limb(9, -50, 22, -70, pink, 4),
        f'<path d="M-18 -92 Q-42 -98 -36 -64 Q-28 -78 -16 -84 Z" fill="{INK}"/>',
        f'<path d="M18 -92 Q42 -98 36 -64 Q28 -78 16 -84 Z" fill="{INK}"/>',
        f'<ellipse cx="0" cy="-82" rx="23" ry="17" fill="{pink}" {S}/>',
        f'<circle cx="-22" cy="-73" r="5" fill="{pink}" {S}/>',
        f'<circle cx="22" cy="-73" r="5" fill="{pink}" {S}/>',
        f'<circle cx="-8" cy="-87" r="8" fill="#ffffff" {S}/>',
        f'<circle cx="8" cy="-87" r="8" fill="#ffffff" {S}/>',
        f'<circle cx="-8" cy="-87" r="2.4" fill="{INK}"/><circle cx="8" cy="-87" r="2.4" fill="{INK}"/>',
        f'<ellipse cx="0" cy="-77" rx="4.5" ry="3" fill="{INK}"/>',
        f'<path d="M-10 -69 L-6 -72 L-2 -69 L2 -72 L6 -69 L10 -72" stroke="{INK}" stroke-width="2" fill="none"/>',
        '<path d="M26 -96 Q30 -88 26 -84 Q22 -88 26 -96 Z" fill="#7fd0ff" stroke="#111" stroke-width="1.5">'
        '<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></path>',
    ]
    return (f'<g>{"".join(o)}<animateTransform attributeName="transform" type="translate" '
            'values="0 0;-1.6 0;1.6 0;0 0" dur=".18s" repeatCount="indefinite"/></g>')


def edd():
    """Double D: black sock hat with white side stripes, orange-red shirt, purple shorts, red socks."""
    shirt, shorts, socks = "#ff5a36", "#6a4c9c", "#e23b3b"
    o = [
        f'<ellipse cx="-9" cy="-4" rx="9" ry="4.5" fill="{INK}"/>',
        f'<ellipse cx="9" cy="-4" rx="9" ry="4.5" fill="{INK}"/>',
        _limb(-7, -8, -7, -26, socks, 6), _limb(7, -8, 7, -26, socks, 6),
        _limb(-7, -28, -7, -38, SKIN, 4), _limb(7, -28, 7, -38, SKIN, 4),
        f'<rect x="-15" y="-48" width="30" height="13" rx="3" fill="{shorts}" {S}/>',
        _limb(-13, -74, -24, -50, SKIN, 4),
        f'<rect x="-15" y="-80" width="30" height="34" rx="6" fill="{shirt}" {S}/>',
        f'<path d="M-8 -80 L0 -72 L8 -80" stroke="{INK}" stroke-width="2.5" fill="none"/>',
        # right arm holding out a label tag
        _limb(13, -74, 28, -62, SKIN, 4),
        f'<g transform="translate(30 -66) rotate(-12)"><rect x="0" y="-9" width="40" height="18" rx="3" fill="#ffffff" {S}/>'
        f'<circle cx="6" cy="0" r="2.4" fill="{INK}"/>'
        '<text x="24" y="4" font-family="Verdana,sans-serif" font-size="9" font-weight="700" text-anchor="middle" fill="#111">LOST</text></g>',
        f'<ellipse cx="0" cy="-98" rx="15" ry="18" fill="{SKIN}" {S}/>',
        f'<path d="M-18 -93 C-21 -131 21 -131 18 -93 Q0 -101 -18 -93 Z" fill="{INK}" {S}/>',
        '<path d="M-12 -97 V-109 M12 -97 V-109" stroke="#ffffff" stroke-width="2.5" fill="none"/>',
        f'<circle cx="-5" cy="-93" r="2.2" fill="{INK}"/><circle cx="5" cy="-93" r="2.2" fill="{INK}"/>',
        f'<path d="M-6 -86 Q0 -82 6 -86" stroke="{INK}" stroke-width="2" fill="#ffffff"/>',
        f'<path d="M0 -85.5 V-83" stroke="{INK}" stroke-width="1.5"/>',
    ]
    return _bob("".join(o))


def jack():
    """Samurai in a white gi with a topknot, katana raised over his head."""
    gi = "#f6f2e4"
    o = [
        f'<path d="M-12 -2 H-2 M2 -2 H12" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
        f'<path d="M-15 -76 L-23 -6 H23 L15 -76 Z" fill="{gi}" {S}/>',
        f'<path d="M-9 -76 L0 -60 L9 -76" stroke="{INK}" stroke-width="2.5" fill="none"/>',
        f'<path d="M-15 -74 L-30 -44 L-19 -40 L-11 -62 Z" fill="{gi}" {S}/>',
        f'<circle cx="-26" cy="-40" r="5" fill="{SKIN}" {S}/>',
        # katana: blade glints
        f'<path d="M28 -88 L-12 -126" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
        '<path d="M28 -88 L-12 -126" stroke="#e8eef4" stroke-width="3.5" stroke-linecap="round"/>',
        '<path d="M20 -96 L6 -109" stroke="#ffffff" stroke-width="2" stroke-linecap="round">'
        '<animate attributeName="opacity" values="0;1;0" dur="1.6s" repeatCount="indefinite"/></path>',
        f'<path d="M40 -76 L30 -86" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>',
        f'<ellipse cx="29" cy="-87" rx="6" ry="3" fill="#d4a017" {S} transform="rotate(45 29 -87)"/>',
        f'<path d="M15 -74 L34 -84 L38 -76 L19 -64 Z" fill="{gi}" {S}/>',
        f'<circle cx="37" cy="-80" r="5" fill="{SKIN}" {S}/>',
        f'<ellipse cx="0" cy="-92" rx="13" ry="16" fill="{SKIN}" {S}/>',
        f'<path d="M-13 -95 Q-14 -110 0 -110 Q14 -110 13 -95 Q6 -102 0 -101 Q-6 -102 -13 -95 Z" fill="{INK}"/>',
        f'<circle cx="0" cy="-114" r="5.5" fill="{INK}"/>',
        f'<path d="M-9 -95 L-2 -93 M9 -95 L2 -93" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>',
        f'<path d="M-6 -89 H-3 M3 -89 H6" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>',
        f'<path d="M-4 -82 H4" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>',
    ]
    return "".join(o)


def ben():
    """Kid hero: brown hair, white tee with a black stripe, green cargo pants, glowing watch."""
    pants = "#3f8f3f"
    o = [
        f'<ellipse cx="-9" cy="-4" rx="9" ry="5" fill="#ffffff" {S}/>',
        f'<ellipse cx="9" cy="-4" rx="9" ry="5" fill="#ffffff" {S}/>',
        f'<rect x="-14" y="-40" width="13" height="34" rx="3" fill="{pants}" {S}/>',
        f'<rect x="1" y="-40" width="13" height="34" rx="3" fill="{pants}" {S}/>',
        _limb(-14, -70, -24, -44, SKIN, 5),
        f'<rect x="-16" y="-76" width="32" height="38" rx="5" fill="#ffffff" {S}/>',
        f'<rect x="-4" y="-75" width="8" height="36" fill="{INK}"/>',
        _limb(14, -70, 32, -82, SKIN, 5),
        f'<rect x="26" y="-90" width="15" height="13" rx="3" fill="#2b2b2b" {S}/>',
        f'<circle cx="33.5" cy="-83.5" r="4.5" fill="#39ff6a"><animate attributeName="r" values="3.5;6;3.5" dur="1s" repeatCount="indefinite"/></circle>',
        f'<ellipse cx="0" cy="-92" rx="15" ry="16" fill="{SKIN}" {S}/>',
        f'<path d="M-17 -92 Q-19 -114 2 -112 Q19 -112 17 -92 Q12 -101 5 -99 Q0 -106 -7 -99 Q-12 -102 -17 -92 Z" fill="#7a4a24" {S}/>',
        '<circle cx="-5" cy="-90" r="2.6" fill="#2d9b45"/><circle cx="5" cy="-90" r="2.6" fill="#2d9b45"/>',
        f'<path d="M-4 -83 Q2 -80 6 -84" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>',
    ]
    return _bob("".join(o), 2, 1.8)


def ppg(kind):
    """One of the three superpowered girls: big head, huge eyes, stubby body, colour trail."""
    color, hair = {"blossom": ("#ff6fb5", "#ff8a3d"), "bubbles": ("#57b8ff", "#ffd84d"),
                   "buttercup": ("#5fd068", "#1b1b1b")}[kind]
    back, front = "", ""
    if kind == "blossom":
        back = f'<path d="M-25 -46 Q-32 -6 -14 4 H14 Q32 -6 25 -46 Z" fill="{hair}" {S}/>'
        front = (f'<path d="M-24 -44 Q-22 -63 0 -63 Q22 -63 24 -44 Q12 -54 0 -50 Q-12 -54 -24 -44 Z" fill="{hair}" {S}/>'
                 f'<path d="M0 -64 L-16 -74 L-14 -58 Z M0 -64 L16 -74 L14 -58 Z" fill="#e3243b" {S}/>'
                 f'<circle cx="0" cy="-64" r="4" fill="#e3243b" {S}/>')
    elif kind == "bubbles":
        back = (f'<ellipse cx="-29" cy="-48" rx="8" ry="13" fill="{hair}" {S}/>'
                f'<ellipse cx="29" cy="-48" rx="8" ry="13" fill="{hair}" {S}/>')
        front = f'<path d="M-24 -44 Q-22 -63 0 -63 Q22 -63 24 -44 Q14 -52 4 -48 Q-6 -55 -24 -44 Z" fill="{hair}" {S}/>'
    else:
        front = (f'<path d="M-25 -38 Q-28 -64 0 -63 Q28 -64 25 -38 Q31 -34 34 -40 Q32 -28 22 -34 '
                 f'Q12 -50 0 -50 Q-12 -50 -22 -34 Q-32 -28 -34 -40 Q-31 -34 -25 -38 Z" fill="{hair}" {S}/>')
    trail = (f'<path d="M-6 -30 L-64 -42 L-64 -18 Z" fill="{color}" opacity=".45"/>'
             f'<path d="M-6 -30 L-42 -37 L-42 -23 Z" fill="{color}" opacity=".6"/>')
    eye = lambda x: (f'<ellipse cx="{x}" cy="-40" rx="8.5" ry="10" fill="#ffffff" stroke="{INK}" stroke-width="2"/>'
                     f'<ellipse cx="{x + 1.5}" cy="-39" rx="6" ry="7.5" fill="{color}"/>'
                     f'<circle cx="{x + 2}" cy="-38.5" r="3.4" fill="{INK}"/>'
                     f'<circle cx="{x + 3.5}" cy="-42" r="1.6" fill="#ffffff"/>')
    o = [trail, back,
         _limb(-5, -12, -8, -2, "#ffffff", 4), _limb(5, -12, 8, -2, "#ffffff", 4),
         f'<ellipse cx="-8" cy="-1" rx="5" ry="3" fill="{INK}"/><ellipse cx="8" cy="-1" rx="5" ry="3" fill="{INK}"/>',
         f'<path d="M-9 -22 L-13 -8 H13 L9 -22 Z" fill="{color}" {S}/>',
         f'<path d="M-12 -13 H12" stroke="{INK}" stroke-width="3"/>',
         _limb(-9, -20, -18, -12, SKIN, 3.5), _limb(9, -20, 18, -28, SKIN, 3.5),
         f'<ellipse cx="0" cy="-40" rx="25" ry="21" fill="{SKIN}" {S}/>',
         eye(-10), eye(10),
         f'<path d="M-4 -26 Q0 -23 4 -26" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/>',
         front]
    return "".join(o)


def gumball():
    """Blue cat kid in a grey sweater and dark trousers, tail curled up."""
    blue = "#5ab7f2"
    o = [
        f'<path d="M14 -30 Q38 -30 34 -56 Q32 -66 26 -60" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>',
        f'<path d="M14 -30 Q38 -30 34 -56 Q32 -66 26 -60" stroke="{blue}" stroke-width="4" fill="none" stroke-linecap="round"/>',
        f'<ellipse cx="-9" cy="-4" rx="9" ry="4.5" fill="{INK}"/><ellipse cx="9" cy="-4" rx="9" ry="4.5" fill="{INK}"/>',
        f'<rect x="-13" y="-30" width="12" height="25" rx="3" fill="#4a3b33" {S}/>',
        f'<rect x="1" y="-30" width="12" height="25" rx="3" fill="#4a3b33" {S}/>',
        _limb(-14, -56, -24, -32, blue, 5), _limb(14, -56, 24, -32, blue, 5),
        f'<rect x="-16" y="-62" width="32" height="34" rx="7" fill="#a7a9ad" {S}/>',
        f'<path d="M-15 -66 L-22 -100 L-4 -88 Z" fill="{blue}" {S}/>',
        f'<path d="M15 -66 L22 -100 L4 -88 Z" fill="{blue}" {S}/>',
        f'<ellipse cx="0" cy="-76" rx="22" ry="17" fill="{blue}" {S}/>',
        f'<ellipse cx="-6.5" cy="-80" rx="7" ry="8.5" fill="#ffffff" {S}/>',
        f'<ellipse cx="6.5" cy="-80" rx="7" ry="8.5" fill="#ffffff" {S}/>',
        f'<circle cx="-5" cy="-79" r="2.4" fill="{INK}"/><circle cx="5" cy="-79" r="2.4" fill="{INK}"/>',
        f'<path d="M-8 -68 Q0 -62 8 -68" stroke="{INK}" stroke-width="2.2" fill="#ffffff"/>',
        f'<path d="M-14 -72 L-28 -74 M-14 -69 L-28 -67 M14 -72 L28 -74 M14 -69 L28 -67" stroke="{INK}" stroke-width="1.5"/>',
    ]
    return _bob("".join(o), 2, 1.6)


def darwin():
    """Orange goldfish on legs, wearing sneakers."""
    orange = "#ff8c1a"
    o = [
        _limb(-7, -28, -9, -8, orange, 3), _limb(7, -28, 9, -8, orange, 3),
        f'<path d="M-18 -8 Q-18 -14 -8 -14 Q-2 -14 -2 -6 Z" fill="#ffffff" {S}/>',
        f'<path d="M18 -8 Q18 -14 8 -14 Q2 -14 2 -6 Z" fill="#ffffff" {S}/>',
        f'<path d="M-18 -7 H-2 M2 -7 H18" stroke="#e23b3b" stroke-width="3"/>',
        f'<path d="M-20 -42 L-34 -54 L-34 -30 Z" fill="{orange}" {S}/>',
        f'<ellipse cx="0" cy="-42" rx="20" ry="17" fill="{orange}" {S}/>',
        f'<ellipse cx="-6" cy="-62" rx="7" ry="9" fill="#ffffff" {S}/>',
        f'<ellipse cx="7" cy="-62" rx="7" ry="9" fill="#ffffff" {S}/>',
        f'<circle cx="-5" cy="-61" r="2.4" fill="{INK}"/><circle cx="6" cy="-61" r="2.4" fill="{INK}"/>',
        f'<ellipse cx="2" cy="-40" rx="6" ry="4" fill="#ff6a8a" {S}/>',
    ]
    return _bob("".join(o), 3, 1.3)


def _swing(inner, pivot, amp=18, dur=.5, phase=0.0):
    """Leg/arm swing around a pivot for a walk cycle."""
    px, py = pivot
    vals = f"{-amp} {px} {py};{amp} {px} {py};{-amp} {px} {py}"
    return (f'<g>{inner}<animateTransform attributeName="transform" type="rotate" values="{vals}" '
            f'dur="{dur}s" begin="-{phase * dur}s" repeatCount="indefinite"/></g>')


def finn(walking=True):
    """Hero kid: white bear-eared hat, light blue tee, dark blue shorts, green backpack."""
    shirt, shorts, pack = "#3fa9f5", "#1f4fa8", "#6cc04a"
    legs = [_limb(-6, -26, -6, -6, SKIN, 4), _limb(6, -26, 6, -6, SKIN, 4)]
    feet = [f'<ellipse cx="-7" cy="-3" rx="6" ry="3.5" fill="{INK}"/>', f'<ellipse cx="7" cy="-3" rx="6" ry="3.5" fill="{INK}"/>']
    if walking:
        leg_l = _swing(legs[0] + feet[0], (-6, -26), 20, .5, 0)
        leg_r = _swing(legs[1] + feet[1], (6, -26), 20, .5, .5)
        arm_l = _swing(_limb(-13, -54, -22, -30, SKIN, 3.5), (-13, -54), 22, .5, .5)
        arm_r = _swing(_limb(13, -54, 22, -30, SKIN, 3.5), (13, -54), 22, .5, 0)
    else:
        leg_l, leg_r = legs[0] + feet[0], legs[1] + feet[1]
        arm_l, arm_r = _limb(-13, -54, -22, -30, SKIN, 3.5), _limb(13, -54, 22, -30, SKIN, 3.5)
    o = [
        f'<rect x="-22" y="-58" width="12" height="26" rx="5" fill="{pack}" {S}/>',
        leg_l, leg_r,
        f'<rect x="-13" y="-34" width="26" height="12" rx="3" fill="{shorts}" {S}/>',
        arm_l,
        f'<rect x="-14" y="-58" width="28" height="26" rx="5" fill="{shirt}" {S}/>',
        f'<path d="M-12 -57 L-4 -40 M12 -57 L4 -40" stroke="#4f8f2f" stroke-width="3"/>',
        arm_r,
        f'<circle cx="-14" cy="-102" r="6" fill="#ffffff" {S}/><circle cx="14" cy="-102" r="6" fill="#ffffff" {S}/>',
        f'<rect x="-21" y="-104" width="42" height="46" rx="18" fill="#ffffff" {S}/>',
        f'<ellipse cx="0" cy="-80" rx="14" ry="11.5" fill="{SKIN}" {S}/>',
        f'<circle cx="-5" cy="-83" r="2" fill="{INK}"/><circle cx="5" cy="-83" r="2" fill="{INK}"/>',
        f'<path d="M-6 -77 Q0 -69 6 -77 Z" fill="#7a1f1f" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>',
        '<path d="M-3 -77 H3" stroke="#ffffff" stroke-width="1.6"/>',
    ]
    return "".join(o)


def jake(walking=True):
    """Yellow dog: wide bean body, big shiny eyes, droopy jowls, stubby legs."""
    gold, shade = "#f7b928", "#d9951a"
    legs = []
    for i, x in enumerate((-16, -6, 8, 18)):
        leg = _limb(x, -14, x, -3, gold, 4)
        legs.append(_swing(leg, (x, -14), 22, .5, i % 2 * .5) if walking else leg)
    o = [
        f'<path d="M-30 -24 Q-44 -30 -42 -42" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>',
        f'<path d="M-30 -24 Q-44 -30 -42 -42" stroke="{gold}" stroke-width="4" fill="none" stroke-linecap="round"/>',
        *legs,
        f'<path d="M-32 -16 Q-34 -38 -8 -40 H14 Q32 -40 30 -16 Q30 -10 22 -10 H-24 Q-32 -10 -32 -16 Z" fill="{gold}" {S}/>',
        f'<path d="M4 -40 Q2 -66 22 -66 Q42 -66 40 -44 Q40 -32 22 -32 Q6 -32 4 -40 Z" fill="{gold}" {S}/>',
        f'<path d="M10 -60 Q4 -58 6 -50 M36 -60 Q42 -58 40 -50" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        f'<circle cx="15" cy="-52" r="7.5" fill="#ffffff" {S}/><circle cx="30" cy="-52" r="7.5" fill="#ffffff" {S}/>',
        f'<circle cx="16" cy="-51" r="3.4" fill="{INK}"/><circle cx="31" cy="-51" r="3.4" fill="{INK}"/>',
        '<circle cx="17.5" cy="-53" r="1.3" fill="#fff"/><circle cx="32.5" cy="-53" r="1.3" fill="#fff"/>',
        f'<path d="M14 -42 Q18 -34 23 -38 Q28 -34 32 -42" fill="{shade}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>',
        f'<ellipse cx="23" cy="-43" rx="4" ry="2.6" fill="{INK}"/>',
    ]
    return "".join(o)
