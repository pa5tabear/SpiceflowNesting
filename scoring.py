import json
import statistics
from openai import OpenAI
from sqlalchemy.orm import Session
from models import Listing, Score
from config import settings
from utils.geo import haversine_miles

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def _sentiment(text: str) -> float:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Score 0-1 how luxurious and pleasant this rental sounds.",
            },
            {"role": "user", "content": text[:4000]},
        ],
        max_tokens=1,
        logprobs=True,
    )
    try:
        return float(resp.choices[0].message.content.strip())
    except Exception:
        return 0.5


def score_listing(listing: Listing, market_ppsf_25: float) -> dict:
    if listing.beds < 1 or listing.baths < 1:
        return {"passed": False}
    if not all(
        x in (listing.amenities or "") for x in ["dishwasher", "air", "laundry"]
    ):
        return {"passed": False}
    if haversine_miles(listing.lat, listing.lon) > settings.MAX_DISTANCE_MILES:
        return {"passed": False}

    subs = {}
    ppsf = listing.price / listing.sqft if listing.sqft else listing.price
    subs["price"] = max(0, min(40, 40 * (market_ppsf_25 / ppsf)))
    subs["amenities"] = min(25, 3 * len(json.loads(listing.amenities)))
    subs["distance"] = 10 if haversine_miles(listing.lat, listing.lon) < 0.5 else 5
    subs["sentiment"] = 25 * _sentiment(listing.title)

    total = round(sum(subs.values()), 1)
    subs["total"] = total
    subs["passed"] = True
    return subs


def refresh_scores(db: Session):
    prices = [
        item.price / (item.sqft or 1)
        for item in db.query(Listing).filter(Listing.sqft.isnot(None))
    ]
    p25 = statistics.quantiles(prices, n=4)[0] if prices else 1
    for lst in db.query(Listing):
        res = score_listing(lst, p25)
        if res.get("passed"):
            db.merge(
                Score(listing_id=lst.id, score=res["total"], subscores=json.dumps(res))
            )
    db.commit()
