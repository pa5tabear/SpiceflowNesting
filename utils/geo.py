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


async def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """Return latitude and longitude for an address via Nominatim."""

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": address, "format": "json", "limit": 1},
            headers={"User-Agent": "spiceflownesting/0.1"},
        )
        r.raise_for_status()
    data = r.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])
