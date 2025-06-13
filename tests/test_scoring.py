import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import Base, Listing
import scoring


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_percentile_calc():
    db = setup_db()
    for i, p in enumerate([1000, 2000, 3000, 4000], 1):
        db.add(Listing(source_id=1, source_uid=str(i), url="u", price=p, sqft=100))
    db.commit()
    val = scoring.get_market_ppsf_percentile(db)
    assert abs(val - 12.5) < 0.01


def test_score_listing(monkeypatch):
    monkeypatch.setattr(scoring, "_sentiment", lambda *_: 0.4)
    monkeypatch.setattr(
        scoring,
        "CRITERIA",
        {
            "max_rent": 1500,
            "min_beds": 1,
            "radius_miles": 1.0,
            "required_amenities": ["dishwasher"],
        },
    )
    lst = Listing(
        source_id=1,
        source_uid="1",
        url="u",
        title="nice",
        price=1000,
        beds=1,
        baths=1,
        sqft=400,
        lat=42.2808,
        lon=-83.7480,
        amenities='["dishwasher"]',
    )
    res = scoring.score_listing(lst, 10)
    assert res["passed"]
    assert 0 <= res["total"] <= 100
    assert res["price"] == 40
