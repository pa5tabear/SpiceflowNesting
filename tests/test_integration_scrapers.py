import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

import scrapers.zillow as zillow
import scrapers.craigslist as craigslist


@pytest.mark.live
@pytest.mark.asyncio
async def test_zillow_live():
    try:
        listings = [item async for item in zillow.fetch_raw()]
    except Exception as e:
        pytest.skip(f"zillow fetch failed: {e}")
    if len(listings) < 10:
        pytest.skip("zillow returned too few listings")
    assert all("url" in lst for lst in listings)


@pytest.mark.live
@pytest.mark.asyncio
async def test_craigslist_live():
    try:
        listings = [item async for item in craigslist.fetch_raw()]
    except Exception as e:
        pytest.skip(f"craigslist fetch failed: {e}")
    if len(listings) < 10:
        pytest.skip("craigslist returned too few listings")
    assert all('url' in lst for lst in listings)
