from bs4 import BeautifulSoup
import httpx
import json


BASE = "https://www.zillow.com"


async def fetch_raw():
    url = f"{BASE}/homes/for_rent/Ann-Arbor-MI_rb/"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    json_blob = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(json_blob.string)
    cards = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"][
        "listResults"
    ]
    for c in cards:
        yield {
            "source_uid": c["zpid"],
            "url": c["detailUrl"],
            "title": c["address"],
            "price": c.get("price"),
            "beds": c.get("beds"),
            "baths": c.get("baths"),
            "sqft": c.get("area"),
            "lat": c["latLong"]["latitude"],
            "lon": c["latLong"]["longitude"],
            "amenities": json.dumps(
                c.get("hdpData", {}).get("homeInfo", {}).get("homeFacts", [])
            ),
        }
