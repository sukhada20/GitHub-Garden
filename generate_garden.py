import os
import math
import requests
from datetime import datetime

USERNAME = "sukhada20" 
TOKEN = os.environ["GH_TOKEN"]

BLOCK = 14
GAP = 4
LEFT_LABEL_SPACE = 34
TOP_LABEL_SPACE = 22

WEEKS = 53
DAYS = 7

BACKGROUND = "#F6F0FA"
BORDER_COLOR = "#D2C2E6"
TEXT_COLOR = "#5E3A8C"

LILAC_SCALE = [
    "#F6F0FA",
    "#E6D9F2",
    "#C8AEE6",
    "#A57BD8",
    "#7E57C2",
]

FLOWER_PETAL = "#B79AD9"
FLOWER_CENTER = "#5E3A8C"

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

DAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}

API_URL = "https://api.github.com/graphql"

QUERY = """
query ($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def fetch_contributions():
    r = requests.post(
        API_URL,
        json={"query": QUERY, "variables": {"login": USERNAME}},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()

    weeks = r.json()["data"]["user"]["contributionsCollection"][
        "contributionCalendar"]["weeks"]

    days = []
    for w in weeks:
        days.extend(w["contributionDays"])

    return days[-(WEEKS * DAYS):]


def block_color(count):
    if count == 0:
        return LILAC_SCALE[0]
    if count <= 1:
        return LILAC_SCALE[1]
    if count <= 5:
        return LILAC_SCALE[2]
    if count <= 9:
        return LILAC_SCALE[3]
    return LILAC_SCALE[4]


def flower_svg(cx, cy, count, delay):
    petals = min(6 + count, 10)
    radius = min(3 + count, 8)

    petals_svg = []
    for i in range(petals):
        angle = 2 * math.pi * i / petals
        px = cx + math.cos(angle) * radius
        py = cy + math.sin(angle) * radius
        petals_svg.append(
            f'<circle cx="{px}" cy="{py}" r="2.4" fill="{FLOWER_PETAL}"/>'
        )

    return f"""
    <g transform="scale(0)" style="transform-origin:{cx}px {cy}px">
      <animateTransform
        attributeName="transform"
        type="scale"
        from="0"
        to="1"
        begin="{delay:.2f}s; bloom.end+4s"
        dur="0.6s"
        fill="freeze"
        id="bloom"/>
      {''.join(petals_svg)}
      <circle cx="{cx}" cy="{cy}" r="2.6" fill="{FLOWER_CENTER}"/>
    </g>
    """


def generate_svg(days):
    width = LEFT_LABEL_SPACE + WEEKS * (BLOCK + GAP)
    height = TOP_LABEL_SPACE + DAYS * (BLOCK + GAP)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{BACKGROUND}"/>'
    ]

    # Day labels
    for row, label in DAY_LABELS.items():
        y = TOP_LABEL_SPACE + row * (BLOCK + GAP) + BLOCK - 2
        svg.append(
            f'<text x="2" y="{y}" font-size="10" fill="{TEXT_COLOR}" '
            f'font-family="monospace">{label}</text>'
        )

    col = 0
    row = 0
    delay = 0.0

    for d in days:
        date_obj = datetime.strptime(d["date"], "%Y-%m-%d")

        x = LEFT_LABEL_SPACE + col * (BLOCK + GAP)
        y = TOP_LABEL_SPACE + row * (BLOCK + GAP)

        # Month label only on first day of month
        if date_obj.day == 1:
            svg.append(
                f'<text x="{x}" y="12" font-size="10" fill="{TEXT_COLOR}" '
                f'font-family="monospace">{MONTH_NAMES[date_obj.month - 1]}</text>'
            )

        count = d["contributionCount"]
        tooltip = f"{d['date']} — {count} contribution{'s' if count != 1 else ''}"

        # Rect with tooltip INSIDE rect (GitHub-safe)
        svg.append(
            f'<rect x="{x}" y="{y}" width="{BLOCK}" height="{BLOCK}" '
            f'rx="3" ry="3" fill="{block_color(count)}" '
            f'stroke="{BORDER_COLOR}" stroke-width="0.8">'
            f'<title>{tooltip}</title>'
            f'</rect>'
        )

        if count > 0:
            cx = x + BLOCK / 2
            cy = y + BLOCK / 2
            svg.append(flower_svg(cx, cy, count, delay))
            delay += 0.03

        row += 1
        if row == DAYS:
            row = 0
            col += 1

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    days = fetch_contributions()
    svg = generate_svg(days)
    with open("garden.svg", "w", encoding="utf-8") as f:
        f.write(svg)
