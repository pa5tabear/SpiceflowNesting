import sys
from pathlib import Path
import asyncio

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

import scrapers.craigslist as craigslist


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


@pytest.mark.asyncio
async def test_craigslist_parse(monkeypatch):
    html = Path(__file__).with_name('data').joinpath('craig_sample.html').read_text()
    monkeypatch.setattr(craigslist.httpx, 'AsyncClient', lambda *a, **k: FakeAsyncClient(html))
    listings = [item async for item in craigslist.fetch_raw()]
    assert len(listings) >= 10
    assert all('title' in l for l in listings)
