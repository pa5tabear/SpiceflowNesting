import sys
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.geo import haversine_miles, geocode_address


def test_haversine():
    # Distance from Liberty & Main to itself should be ~0
    assert haversine_miles(42.2808, -83.7480) < 0.01


@pytest.fixture
def one_mile_north():
    return 42.2808 + 1 / 69, -83.7480


def test_haversine_tolerance(one_mile_north):
    d = haversine_miles(*one_mile_north)
    assert abs(d - 1.0) < 0.031


def test_geocode_address(monkeypatch):
    def fake_get(*args, **kwargs):
        return SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: [{"lat": "42.0", "lon": "-83.0"}],
        )

    monkeypatch.setattr(httpx, "get", fake_get)
    assert geocode_address("addr") == (42.0, -83.0)
