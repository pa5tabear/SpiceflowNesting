import json
import statistics
from openai import OpenAI
from sqlalchemy.orm import Session
from scrapers.url_helpers import load_criteria
from models import Listing, Score
from config import settings
from utils.geo import haversine_miles

client = OpenAI(api_key=settings.OPENAI_API_KEY)
CRITERIA = load_criteria()


def _sentiment(text: str) -> float:
    """Return sentiment score 0-1 via OpenAI; fallback to neutral on error."""
    try:
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
        return float(resp.choices[0].message.content.strip())
    except Exception:
        return 0.5


def score_listing(listing: Listing, market_ppsf_25: float) -> dict:
    """Return weighted subscores; ensure listing meets YAML criteria."""
    if CRITERIA.get("min_beds") and (listing.beds or 0) < CRITERIA["min_beds"]:
        return {"passed": False}
    if (
        CRITERIA.get("max_rent")
        and listing.price
        and listing.price > CRITERIA["max_rent"]
    ):
        return {"passed": False}
    req = CRITERIA.get("required_amenities") or []
    if not all(x in (listing.amenities or "") for x in req):
        return {"passed": False}
    if listing.lat is None or listing.lon is None:
        return {"passed": False}
    radius = CRITERIA.get("radius_miles", settings.MAX_DISTANCE_MILES)
    if haversine_miles(listing.lat, listing.lon) > radius:
        return {"passed": False}

    subs = {}
    ppsf = (listing.price or 0) / (listing.sqft or 1)
    subs["price"] = max(0, min(40, 40 * (market_ppsf_25 / max(ppsf, 1))))
    subs["amenities"] = min(25, 3 * len(json.loads(listing.amenities or "[]")))
    subs["distance"] = 10 if haversine_miles(listing.lat, listing.lon) < 0.5 else 5
    subs["sentiment"] = 25 * _sentiment(listing.title or "")

    total = round(sum(subs.values()), 1)
    subs["total"] = total
    subs["passed"] = True
    return subs


def get_market_ppsf_percentile(db: Session, pct: float = 0.25) -> float:
    """Return price-per-sqft percentile for current listings."""
    prices = [
        item.price / (item.sqft or 1)
        for item in db.query(Listing).filter(Listing.sqft.isnot(None))
    ]
    if not prices:
        return 1.0
    return statistics.quantiles(prices, n=4)[0]


def refresh_scores(db: Session):
    p25 = get_market_ppsf_percentile(db)
    for lst in db.query(Listing):
        res = score_listing(lst, p25)
        if res.get("passed"):
            db.merge(
                Score(listing_id=lst.id, score=res["total"], subscores=json.dumps(res))
            )
    db.commit()
