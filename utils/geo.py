"""Geospatial helpers."""

from math import radians, cos, sin, asin, sqrt
from typing import Optional, Tuple

import httpx

from config import settings


def haversine_miles(lat1, lon1, lat2=settings.DOWNTOWN_LAT, lon2=settings.DOWNTOWN_LON):
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    miles = 3958.8 * 2 * asin(sqrt(a))
    return miles


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """Return latitude and longitude for an address using Nominatim."""

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    r = httpx.get(
        url, params=params, headers={"User-Agent": "spiceflownesting"}, timeout=10
    )
    r.raise_for_status()
    data = r.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])
