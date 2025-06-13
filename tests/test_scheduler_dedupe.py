import asyncio
import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import scheduler
from models import Base, Listing, Run


async def fake_fetch_raw():
    yield {
        "source_uid": "1",
        "url": "u",
        "title": "t",
        "beds": 1,
        "baths": 1,
        "amenities": "[]",
    }


def test_dedupe(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    monkeypatch.setattr(scheduler, "Session", Session)
    mod = types.ModuleType("m")
    mod.fetch_raw = fake_fetch_raw
    monkeypatch.setattr(scheduler, "import_module", lambda *_: mod)
    monkeypatch.setattr(scheduler, "SCRAPERS", {"fake": "m"})

    async def g(*_):
        return 1.0, 2.0

    monkeypatch.setattr(scheduler, "geocode_address", g)
    asyncio.run(scheduler.run_once())
    asyncio.run(scheduler.run_once())
    db = Session()
    assert db.query(Listing).count() == 1
    assert db.query(Run).count() == 2
