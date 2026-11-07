"""scraper.py - Collect and return clean data."""
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "CS3030-Demo/1.0 (your-email@weber.edu)"}


def to_int(text):
    """'9' -> 9, and the page's dash for 'none' ('—') -> 0."""
    text = text.strip()
    return 0 if text == "—" else int(text)


def scrape_states(url):
    """Download the page and return one dictionary per state."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find_all("table", class_="wikitable")[1]   # parks-by-state table
    records = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all(["th", "td"])
        records.append({
            "state": cells[0].get_text(strip=True),
            "total": to_int(cells[1].get_text()),
        })
    return records