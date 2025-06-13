import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import scheduler
from models import Base, Listing, Score


def setup(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    monkeypatch.setattr(scheduler, "Session", Session)
    monkeypatch.setattr(scheduler, "SCRAPERS", {})
    async def noop(*_):
        pass
    monkeypatch.setattr(scheduler, "run_scraper", noop)
    monkeypatch.setattr(scheduler, "refresh_scores", lambda *_: None)
    return Session


def test_digest_trigger(monkeypatch):
    Session = setup(monkeypatch)
    called = {}

    async def fake_send(lst):
        called["x"] = lst

    monkeypatch.setattr(scheduler, "send_digest", fake_send)
    db = Session()
    lst = Listing(source_id=1, source_uid="1", url="u", title="t")
    db.add(lst)
    db.flush()
    db.add(Score(listing_id=lst.id, score=90))
    db.commit()
    db.close()
    asyncio.run(scheduler.run_once())
    assert called.get("x")
