import asyncio
from pathlib import Path
import pytest

import scrapers.craigslist as craigslist
import scrapers.zillow as zillow
import scrapers.url_helpers as u


class FakeAsyncClient:
    def __init__(self, text):
        self.text = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, *_, **__):
        class R:
            def __init__(self, text):
                self.text = text

        return R(self.text)


def _patch_http(monkeypatch, module, text):
    monkeypatch.setattr(
        module.httpx, "AsyncClient", lambda *a, **k: FakeAsyncClient(text)
    )


async def _zillow_html():
    return (
        "<html><script id='__NEXT_DATA__' type='application/json'>"
        '{"props":{"pageProps":{"searchPageState":{"cat1":{"searchResults":{"listResults":['
        '{"zpid":1,"detailUrl":"u","address":"addr","price":1900,"beds":1,"baths":1,"area":500,"latLong":{"latitude":1,"longitude":2},"hdpData":{"homeInfo":{"homeFacts":[]}}}'
        "]}}}}}</script></html>"
    )


async def _craig_html():
    return Path("tests/data/craig_sample.html").read_text()


async def _check_all(listings, max_rent, min_beds):
    assert all(l.get("price") is None or l["price"] <= max_rent for l in listings)
    assert all(l.get("beds") is None or l["beds"] >= min_beds for l in listings)


@pytest.mark.asyncio
async def test_filtered_results(monkeypatch):
    html_c = await _craig_html()
    html_z = await _zillow_html()
    _patch_http(monkeypatch, craigslist, html_c)
    _patch_http(monkeypatch, zillow, html_z)
    monkeypatch.setattr(u, "CRITERIA", {"max_rent": 3000, "min_beds": 1})
    listings = [item async for item in craigslist.fetch_raw()]
    await _check_all(listings, 3000, 1)
    listings = [item async for item in zillow.fetch_raw()]
    await _check_all(listings, 3000, 1)
