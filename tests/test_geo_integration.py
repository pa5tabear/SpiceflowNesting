import asyncio, importlib, os, sys, types  # noqa: E401
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # noqa: E701
import config

importlib.reload(config)  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402
import scheduler  # noqa: E402
from models import Base, Listing  # noqa: E402
from config import settings  # noqa: E402
from utils import geo  # noqa: E402
from scoring import score_listing  # noqa: E402


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(bind=engine)


async def fake_fetch_raw():
    yield {
        "source_uid": "1",
        "url": "u",
        "title": "addr",
        "beds": 1,
        "baths": 1,
        "amenities": "[]",
    }


def test_geocode_address(monkeypatch):
    class C:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *_, **__):
            class R:
                def raise_for_status(self):
                    pass

                def json(self):
                    return [{"lat": "1", "lon": "2"}]

            return R()

    monkeypatch.setattr(geo.httpx, "AsyncClient", lambda *a, **k: C())
    assert asyncio.run(geo.geocode_address("a")) == (1.0, 2.0)


def test_distance_filter(monkeypatch):
    monkeypatch.setattr("scoring._sentiment", lambda _: 0.5)

    def mk(lat):
        return Listing(
            source_id=1,
            source_uid="1",
            url="u",
            title="t",
            price=100,
            beds=1,
            baths=1,
            sqft=100,
            lat=lat,
            lon=settings.DOWNTOWN_LON,
            amenities='["dishwasher","air","laundry"]',
        )

    near = mk(settings.DOWNTOWN_LAT + (1 - 0.03) / 69)
    far = mk(settings.DOWNTOWN_LAT + (1 + 0.03) / 69)
    assert score_listing(near, 1)["passed"]
    assert not score_listing(far, 1)["passed"]

def test_scheduler_geo(monkeypatch):
    mod = types.ModuleType("m")
    mod.fetch_raw = fake_fetch_raw
    monkeypatch.setattr(scheduler, "import_module", lambda *_: mod)
    monkeypatch.setattr(scheduler, "SCRAPERS", {"fake": "m"})

    async def g(_):
        return 1.0, 2.0

    monkeypatch.setattr(scheduler, "geocode_address", g)
    db = setup_db()
    asyncio.run(scheduler.run_scraper("fake", "m", db))  # noqa: E701
    lst = db.query(Listing).first()
    assert (lst.lat, lst.lon) == (1.0, 2.0)
