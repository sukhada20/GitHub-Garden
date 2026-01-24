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

def flower_svg(x, y, count):
    if count == 0:
        return ""

    petals = min(8, count + 2)
    size = min(6 + count * 1.5, 16)

    lilac = ["#E6D9F2", "#C8AEE6", "#A57BD8", "#7E57C2"]
    color = lilac[min(len(lilac)-1, count // 2)]

    petals_svg = ""
    for i in range(petals):
        angle = 2 * math.pi * i / petals
        px = x + math.cos(angle) * size
        py = y + math.sin(angle) * size
        petals_svg += f'<circle cx="{px}" cy="{py}" r="{size/2}" fill="{color}" />'

    return f"""
    <g>
      {petals_svg}
      <circle cx="{x}" cy="{y}" r="{size/3}" fill="#5E3A8C"/>
    </g>
    """

def generate_svg(days):
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="180">',
        '<rect width="100%" height="100%" fill="#F6F0FA"/>'
    ]

    x, y = 20, 30
    col = 0

    for d in days:
        svg.append(flower_svg(x + col * 18, y, d["contributionCount"]))
        col += 1
        if col == 52:
            col = 0
            y += 30

    svg.append("</svg>")
    return "\n".join(svg)

if __name__ == "__main__":
    days = fetch_contributions()
    svg = generate_svg(days)
    with open("garden.svg", "w") as f:
        f.write(svg)
