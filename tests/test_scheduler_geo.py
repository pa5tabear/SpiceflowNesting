import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import sys
from pathlib import Path
import types
import asyncio

sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Listing
import scheduler


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(bind=engine)


async def dummy_fetch_raw():
    yield {"source_uid": "1", "url": "u", "title": "addr"}


def test_scheduler_geo(monkeypatch):
    db = setup_db()
    mod = types.SimpleNamespace(fetch_raw=dummy_fetch_raw)
    monkeypatch.setattr(scheduler, "import_module", lambda _: mod)
    monkeypatch.setattr(scheduler, "geocode_address", lambda addr: (1.0, 2.0))
    asyncio.run(scheduler.run_scraper("dummy", "dummy", db))
    lst = db.query(Listing).first()
    assert (lst.lat, lst.lon) == (1.0, 2.0)
