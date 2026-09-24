import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

SOURCE_URL = "https://missil.se/nyheter/"
OUTPUT_FILE = "feed.xml"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; MissilRSS/1.0)"
}

response = requests.get(SOURCE_URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

fg = FeedGenerator()
fg.title("MISSIL")
fg.link(href=SOURCE_URL, rel="alternate")
fg.description("Nyheter från MISSIL")
fg.language("sv")

seen = set()

for link in reversed(soup.find_all("a", href=True)):
    href = urljoin(SOURCE_URL, link["href"])

    if "/nyheter/" not in href:
        continue

    if href.rstrip("/") == SOURCE_URL.rstrip("/"):
        continue

    title = link.get_text(" ", strip=True)
    
    if title == "Hoppa till innehåll":
        continue

    if not title or len(title) < 10:
        continue

    if href in seen:
        continue

    seen.add(href)

    entry = fg.add_entry()
    entry.id(href)
    entry.title(title)
    entry.link(href=href)

fg.rss_file(OUTPUT_FILE, pretty=True)

print(f"Created {OUTPUT_FILE} with {len(seen)} articles.")
