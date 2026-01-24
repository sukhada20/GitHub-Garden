import requests
from datetime import datetime, timedelta
import math
import os

TOKEN = os.environ["GH_TOKEN"]
USERNAME = "sukhada20"

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

def block_color(count):
    if count == 0:
        return LILAC_SCALE[0]
    elif count <= 2:
        return LILAC_SCALE[1]
    elif count <= 5:
        return LILAC_SCALE[2]
    elif count <= 9:
        return LILAC_SCALE[3]
    else:
        return LILAC_SCALE[4]

def fetch_contributions():
    r = requests.post(
        API_URL,
        json={"query": QUERY, "variables": {"login": USERNAME}},
        headers=HEADERS
    )
    data = r.json()
    days = []
    for week in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in week["contributionDays"]:
            days.append(d)
    return days

def flower_svg(cx, cy, count, delay):
    petals = min(6 + count, 10)
    radius = min(4 + count, 10)
    color = "#A57BD8"

    petals_svg = ""
    for i in range(petals):
        angle = 2 * math.pi * i / petals
        px = cx + math.cos(angle) * radius
        py = cy + math.sin(angle) * radius
        petals_svg += f'<circle cx="{px}" cy="{py}" r="3" fill="{color}" />'

    return f"""
    <g transform="scale(0)" style="transform-origin:{cx}px {cy}px">
      <animateTransform
        attributeName="transform"
        type="scale"
        from="0"
        to="1"
        begin="{delay}s"
        dur="0.6s"
        fill="freeze" />
      {petals_svg}
      <circle cx="{cx}" cy="{cy}" r="3" fill="#5E3A8C"/>
    </g>
    """

def generate_svg(days):
    block = 14
    gap = 4
    width = 53 * (block + gap)
    height = 7 * (block + gap)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#F6F0FA"/>'
    ]

    col = 0
    row = 0
    delay = 0.0

    for d in days:
        x = col * (block + gap)
        y = row * (block + gap)

        color = block_color(d["contributionCount"])

        # Block (streak indicator)
        svg.append(
            f'<rect x="{x}" y="{y}" width="{block}" height="{block}" '
            f'rx="3" ry="3" fill="{color}"/>'
        )

        # Flower bloom overlay
        if d["contributionCount"] > 0:
            cx = x + block / 2
            cy = y + block / 2
            svg.append(flower_svg(cx, cy, d["contributionCount"], delay))
            delay += 0.02

        row += 1
        if row == 7:
            row = 0
            col += 1

    svg.append("</svg>")
    return "\n".join(svg)
