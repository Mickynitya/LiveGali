import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

URL = "https://satta-king-fast.com"

today = datetime.now().strftime("%Y-%m-%d")

html = requests.get(URL, timeout=15).text
soup = BeautifulSoup(html, "html.parser")

results = {}

for game in soup.select("tr.game-result"):
    name = game.select_one(".game-name")
    num  = game.select_one(".today-number h3")

    if not name or not num:
        continue

    value = num.text.strip()
    if value in ("--", "XX"):
        continue

    results[name.text.strip()] = value

data = {
    "date": today,
    "results": results
}

# Netlify public folder
os.makedirs("public", exist_ok=True)

with open("public/today.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("JSON generated for Netlify")
