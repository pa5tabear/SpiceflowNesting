import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import json

import scoring
from scoring import score_listing


class DummyListing:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.beds = 1
        self.baths = 1
        self.sqft = 500
        self.price = 1000
        self.amenities = json.dumps(["dishwasher", "air", "laundry"])
        self.title = "test"


def test_distance_filter(monkeypatch):
    monkeypatch.setattr(scoring, "_sentiment", lambda text: 0.5)
    close = DummyListing(42.2808, -83.7480)
    far = DummyListing(42.31, -83.7480)
    assert score_listing(close, 1)["passed"]
    assert not score_listing(far, 1)["passed"]
