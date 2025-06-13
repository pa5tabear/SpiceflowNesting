from __future__ import annotations
import json
from bs4 import BeautifulSoup
import httpx

BASE = "https://annarbor.craigslist.org"
SEARCH_PATH = "/search/apa"


async def fetch_raw():
    url = f"{BASE}{SEARCH_PATH}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select("ol.cl-static-search-results li.cl-static-search-result")
    meta = json.loads(soup.find("script", id="ld_searchpage_results").string)[
        "itemListElement"
    ]
    for li, js in zip(items, meta):
        title = li.find("div", class_="title").get_text(strip=True)
        href = li.find("a")["href"]
        price_el = li.find("div", class_="price")
        price = (
            int(price_el.get_text(strip=True).strip("$").replace(",", ""))
            if price_el
            else None
        )
        yield {
            "source_uid": js.get("position"),
            "url": href,
            "title": title,
            "price": price,
            "beds": js["item"].get("numberOfBedrooms"),
            "baths": js["item"].get("numberOfBathroomsTotal"),
            "sqft": None,
            "lat": js["item"].get("latitude"),
            "lon": js["item"].get("longitude"),
            "amenities": "[]",
        }
