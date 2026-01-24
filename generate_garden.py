import os
import math
import requests
from datetime import datetime

# ===================== CONFIG =====================

USERNAME = "sukhada20" 
TOKEN = os.environ["GH_TOKEN"]

BLOCK_SIZE = 14
GAP = 4
WEEKS = 53
DAYS = 7

BACKGROUND = "#F6F0FA"
BORDER_COLOR = "#D2C2E6"

LILAC_SCALE = [
    "#F6F0FA",  # 0
    "#E6D9F2",  # 1–2
    "#C8AEE6",  # 3–5
    "#A57BD8",  # 6–9
    "#7E57C2",  # 10+
]

FLOWER_PETAL = "#B79AD9"
FLOWER_CENTER = "#5E3A8C"

# ===================== GITHUB QUERY =====================

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

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# ===================== DATA =====================

def fetch_contributions():
    r = requests.post(
        API_URL,
        json={"query": QUERY, "variables": {"login": USERNAME}},
        headers=HEADERS,
        timeout=30
    )
    r.raise_for_status()

    weeks = r.json()["data"]["user"]["contributionsCollection"][
        "contributionCalendar"
    ]["weeks"]

    days = []
    for w in weeks:
        for d in w["contributionDays"]:
            days.append(d)

    return days[-(WEEKS * DAYS):]

# ===================== VISUAL LOGIC =====================

def block_color(count):
    if count == 0:
        return LILAC_SCALE[0]
    if count <= 2:
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
            f'<circle cx="{px}" cy="{py}" r="2.6" fill="{FLOWER_PETAL}" />'
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
      <circle cx="{cx}" cy="{cy}" r="2.8" fill="{FLOWER_CENTER}" />
    </g>
    """

# ===================== SVG GENERATION WITH MONTH LABELS =====================

def generate_svg(days):
    width = WEEKS * (BLOCK_SIZE + GAP)
    height = DAYS * (BLOCK_SIZE + GAP) + 20  # extra space for month labels

    svg = [
        f"<!-- regenerated at {datetime.utcnow().isoformat()} -->",
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{BACKGROUND}" />'
    ]

    col = 0
    row = 0
    delay = 0.0
    last_month = None
    month_drawn = set()

    for d in days:
        x = col * (BLOCK_SIZE + GAP)
        y = row * (BLOCK_SIZE + GAP) + 20  # offset for month labels

        count = d["contributionCount"]
        date_str = d["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        color = block_color(count)

        tooltip = f"{date_str} — {count} contribution{'s' if count != 1 else ''}"

        # Month separator & label (only draw once per month)
        if date_obj.month != last_month:
            if date_obj.month not in month_drawn:
                # Vertical dashed line for month
                svg.append(
                    f'<line x1="{x-2}" y1="20" x2="{x-2}" y2="{height}" '
                    f'stroke="#8e44ad" stroke-width="1" stroke-dasharray="2,2" />'
                )
                # Month label
                month_label = date_obj.strftime("%b")
                svg.append(
                    f'<text x="{x}" y="14" font-size="10" fill="#5E3A8C" font-family="sans-serif">{month_label}</text>'
                )
                month_drawn.add(date_obj.month)
            last_month = date_obj.month

        # Group block + tooltip + flower
        svg.append(f'<g>')
        svg.append(f'<title>{tooltip}</title>')

        # Day block with border
        svg.append(
            f'<rect x="{x}" y="{y}" '
            f'width="{BLOCK_SIZE}" height="{BLOCK_SIZE}" '
            f'rx="3" ry="3" '
            f'fill="{color}" '
            f'stroke="{BORDER_COLOR}" stroke-width="0.8" />'
        )

        # Flower overlay
        if count > 0:
            cx = x + BLOCK_SIZE / 2
            cy = y + BLOCK_SIZE / 2
            svg.append(flower_svg(cx, cy, count, delay))
            delay += 0.03

        svg.append('</g>')

        row += 1
        if row == DAYS:
            row = 0
            col += 1

    svg.append("</svg>")
    return "\n".join(svg)

# ===================== MAIN =====================

if __name__ == "__main__":
    days = fetch_contributions()
    svg = generate_svg(days)

    with open("garden.svg", "w", encoding="utf-8") as f:
        f.write(svg)
