import asyncio
import logging
from datetime import datetime
from importlib import import_module
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Source, Listing
from config import settings
from scoring import refresh_scores
from utils.geo import geocode_address

engine = create_engine(settings.DATABASE_URL, future=True, echo=False)
Session = sessionmaker(engine)

SCRAPERS = {
    "zillow": "scrapers.zillow",
    "craigslist": "scrapers.craigslist",
}


async def run_once():
    db = Session()
    await asyncio.gather(
        *(run_scraper(name, mod, db) for name, mod in SCRAPERS.items())
    )
    refresh_scores(db)
    db.close()


async def run_scraper(name, module_path, db):
    logging.info("Running %s at %s", name, datetime.utcnow())
    mod = import_module(module_path)
    source = db.query(Source).filter_by(name=name).first() or Source(
        name=name, url=module_path
    )
    db.merge(source)
    db.flush()
    async for item in mod.fetch_raw():
        if item.get("lat") is None or item.get("lon") is None:
            coords = await geocode_address(item.get("title", ""))
            if coords:
                item["lat"], item["lon"] = coords
        lst = Listing(source_id=source.id, **item)
        db.merge(lst)
    db.commit()


def main():
    scheduler = asyncio.get_event_loop()
    scheduler.run_until_complete(run_once())


if __name__ == "__main__":
    main()
