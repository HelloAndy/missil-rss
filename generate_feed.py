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

cards = soup.select(".post-card")

# Feedgen lägger senast tillagda posten först,
# därför går vi igenom korten baklänges.
for card in reversed(cards):
    link = card.select_one(".post-card__title a")
    description = card.select_one(".post-card__subtitle")
    image = card.select_one(".post-card__image")

    if not link:
        continue

    title = link.get_text(" ", strip=True)
    href = urljoin(SOURCE_URL, link["href"])

    entry = fg.add_entry()
    entry.id(href)
    entry.title(title)
    entry.link(href=href)

    if description:
        entry.description(description.get_text(" ", strip=True))

    if image and image.get("src"):
        entry.enclosure(
            image["src"],
            0,
            "image/jpeg"
        )

fg.rss_file(OUTPUT_FILE, pretty=True)

print(f"Created {OUTPUT_FILE} with {len(cards)} articles.")
