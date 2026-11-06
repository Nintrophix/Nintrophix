"""Adventure Time themed, animated contribution graph for the profile README.

Finn and Jake walk across the Land of Ooo below the last year's contribution
grid; every day with contributions hops as they pass, and the busiest days
sparkle like treasure.

Data comes from the GraphQL API when GITHUB_TOKEN is set (the GitHub Action),
otherwise from the public contributions page (handy for local runs).

    python tools/build_contrib.py [login]
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cn_characters import INK, finn, jake  # noqa: E402

LOGIN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PROFILE_LOGIN", "Nintrophix")
OUT = Path(__file__).resolve().parent.parent / "assets" / "cn" / "contributions.svg"
DISPLAY = "'Arial Black','Arial Bold',Impact,'Helvetica Neue',sans-serif"
BODY = "Verdana,'DejaVu Sans',Geneva,sans-serif"
LEVELS = ["#f3e7cf", "#c6e88a", "#8fd16a", "#4fae3c", "#2f7d2a"]
GQL_LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


# ----------------------------------------------------------------------------- data
def fetch_graphql(token):
    q = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
           totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": q, "variables": {"login": LOGIN}}).encode(),
                                 headers={"Authorization": f"bearer {token}", "User-Agent": "profile-contrib-builder"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"], GQL_LEVEL[d["contributionLevel"]])
            for w in cal["weeks"] for d in w["contributionDays"]]
    return days, cal["totalContributions"]


def fetch_html():
    req = urllib.request.Request(f"https://github.com/users/{LOGIN}/contributions",
                                 headers={"User-Agent": "profile-contrib-builder"})
    html = urllib.request.urlopen(req).read().decode()
    counts = {}
    for cid, text in re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        m = re.match(r"\s*(\d+) contribution", text)
        counts[cid] = int(m.group(1)) if m else 0
    days = []
    for td in re.findall(r"<td[^>]*ContributionCalendar-day[^>]*>", html):
        date = re.search(r'data-date="([^"]+)"', td)
        level = re.search(r'data-level="(\d)"', td)
        cid = re.search(r'id="([^"]+)"', td)
        if date and level:
            days.append((date.group(1), counts.get(cid.group(1) if cid else "", 0), int(level.group(1))))
    days.sort()
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    total = int(m.group(1).replace(",", "")) if m else sum(c for _, c, _ in days)
    return days, total


def longest_streak(days):
    best = cur = 0
    for _, c, _ in days:
        cur = cur + 1 if c > 0 else 0
        best = max(best, cur)
    return best


# ----------------------------------------------------------------------------- drawing
def T(x, y, s, size=14, fill=INK, weight=400, anchor="start", family=BODY, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def build(days, total):
    W, H = 1000, 408
    cell, gap = 13, 3
    x0, y0 = 80, 130
    loop, start, span = 18.0, -140, 1280      # walkers travel from x=-140 to x=1140 every 18s
    lead = 46                                  # point between Finn and Jake that "touches" a column

    first = dt.date.fromisoformat(days[0][0])
    first_sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    cols = 0
    cells, sparkles = [], []
    months, last_month = [], None
    for date_s, count, level in days:
        d = dt.date.fromisoformat(date_s)
        col, row = (d - first_sunday).days // 7, (d.weekday() + 1) % 7
        cols = max(cols, col + 1)
        x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
        if row == 0 and d.month != last_month:
            months.append((x, d.strftime("%b")))
            last_month = d.month
        rect = (f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[level]}" '
                f'stroke="{INK}" stroke-opacity="{.55 if level else .18}" stroke-width="1.2"')
        if count <= 0:
            cells.append(rect + "/>")
            continue
        f = (x + cell / 2 - lead - start) / span
        kt = f"0;{f:.4f};{f + .012:.4f};{f + .026:.4f};1"
        cells.append(rect + f'><title>{count} contribution{"s" if count != 1 else ""} on {date_s}</title>'
                     f'<animateTransform attributeName="transform" type="translate" dur="{loop}s" repeatCount="indefinite" '
                     f'keyTimes="{kt}" values="0 0;0 0;0 -{3 + level * 1.5};0 0;0 0"/></rect>')
        if level == 4:
            cx, cy = x + cell / 2, y + cell / 2
            sparkles.append(
                f'<path d="M{cx} {cy - 9} L{cx + 2.5} {cy - 2.5} L{cx + 9} {cy} L{cx + 2.5} {cy + 2.5} L{cx} {cy + 9} '
                f'L{cx - 2.5} {cy + 2.5} L{cx - 9} {cy} L{cx - 2.5} {cy - 2.5} Z" fill="#fff6a8" stroke="{INK}" stroke-width="1" opacity="0">'
                f'<animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" '
                f'keyTimes="{kt}" values="0;0;1;0;0"/></path>')

    grid_w = cols * (cell + gap) - gap
    clouds = "".join(
        f'<g opacity=".9"><g fill="#fff" stroke="{INK}" stroke-width="2.5">'
        f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="13"/><ellipse cx="{cx - 14}" cy="{cy - 9}" rx="16" ry="12"/>'
        f'<ellipse cx="{cx + 12}" cy="{cy - 12}" rx="18" ry="14"/></g>'
        f'<g fill="#fff"><ellipse cx="{cx}" cy="{cy}" rx="32" ry="11"/></g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} 0;0 0" dur="{d}s" repeatCount="indefinite"/></g>'
        for cx, cy, dx, d in [(250, 40, 40, 30), (660, 30, -50, 36), (930, 70, -30, 26)])

    walkers = (f'<g><g transform="translate(0 {H - 30})">'
               f'<g transform="scale(1.0)">{finn()}</g>'
               f'<g transform="translate(78 0) scale(1.1)">{jake()}</g>'
               f'<g transform="translate(30 -120)"><g opacity="0">'
               f'<path d="M0 0 H108 Q116 0 116 8 V22 Q116 30 108 30 H22 L10 40 L14 30 H0 Q-8 30 -8 22 V8 Q-8 0 0 0 Z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
               + T(54, 20, "MATHEMATICAL!", 11, INK, 900, "middle", DISPLAY)
               + f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.45;.5;.62;.67;1" dur="{loop}s" repeatCount="indefinite"/></g></g>'
               f'<animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 -3;0 0" dur=".25s" repeatCount="indefinite"/></g>'
               f'<animateTransform attributeName="transform" type="translate" from="{start} 0" to="{start + span} 0" dur="{loop}s" repeatCount="indefinite"/></g>')

    o = [
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#ff8f8f"/><stop offset=".55" stop-color="#ffb98a"/><stop offset="1" stop-color="#ffd9a0"/></linearGradient>'
        f'<clipPath id="frame"><rect x="3" y="3" width="{W - 16}" height="{H - 16}" rx="20"/></clipPath></defs>',
        f'<rect x="10" y="10" width="{W - 16}" height="{H - 16}" rx="22" fill="{INK}"/>',
        f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="url(#sky)"/>{clouds}'
        f'<path d="M0 {H - 120} Q160 {H - 190} 330 {H - 120} T660 {H - 130} T1000 {H - 110} V{H} H0 Z" fill="#9bd67a" stroke="{INK}" stroke-width="3"/>'
        f'<path d="M0 {H - 70} Q220 {H - 120} 480 {H - 72} T1000 {H - 76} V{H} H0 Z" fill="#6cbf4a" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="0" y="{H - 34}" width="{W}" height="40" fill="#c99a5b" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="{x0 - 46}" y="{y0 - 30}" width="{grid_w + 66}" height="{7 * (cell + gap) + 40}" rx="14" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>',
        *[T(x, y0 - 10, m, 10, INK, 700) for x, m in months if x < x0 + grid_w - 20],
        *[T(x0 - 10, y0 + r * (cell + gap) + 10, n, 9, INK, 700, "end") for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri"))],
        *cells, *sparkles,
        f'<text x="34" y="58" font-family="{DISPLAY}" font-size="30" font-weight="900" fill="#ffe14d" stroke="{INK}" stroke-width="6" paint-order="stroke" stroke-linejoin="round">ADVENTURE LOG</text>',
        T(36, 86, f"{total} contributions in the last year  ·  longest streak {longest_streak(days)} days",
          13, "#ffffff", 900, extra=f'stroke="{INK}" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round"'),
        walkers, '</g>',
        f'<rect x="3" y="3" width="{W - 16}" height="{H - 16}" rx="20" fill="none" stroke="{INK}" stroke-width="5"/>',
    ]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<title>{escape(LOGIN)} contribution graph, Adventure Time style</title>{"".join(o)}</svg>')


def main():
    token = os.environ.get("GITHUB_TOKEN")
    try:
        days, total = fetch_graphql(token) if token else fetch_html()
    except Exception as e:  # GraphQL can refuse the Actions token; the public page still works
        print(f"primary source failed ({e}); falling back to the contributions page")
        days, total = fetch_html()
    if not days:
        sys.exit("no contribution data found")
    OUT.write_text(build(days, total), encoding="utf-8")
    print(f"wrote {OUT} ({len(days)} days, {total} contributions)")


if __name__ == "__main__":
    main()
