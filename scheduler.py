import asyncio
import logging
from datetime import datetime
import argparse
from importlib import import_module
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from models import Source, Listing, Run
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
    db.add(Run())
    db.commit()
    await asyncio.gather(
        *(run_scraper(name, mod, db) for name, mod in SCRAPERS.items())
    )
    refresh_scores(db)
    db.close()


async def run_scraper(name, module_path, db):
    logging.info("Running %s at %s", name, datetime.utcnow())
    mod = import_module(module_path)
    existing = db.query(Source).filter_by(name=name).first()
    source = existing or Source(name=name, url=module_path)
    source = db.merge(source)
    db.flush()
    async for item in mod.fetch_raw():
        if item.get("lat") is None or item.get("lon") is None:
            coords = await geocode_address(item.get("title", ""))
            if coords:
                item["lat"], item["lon"] = coords
        existing = (
            db.query(Listing)
            .filter_by(source_id=source.id, source_uid=item["source_uid"])
            .first()
        )
        if existing:
            for k, v in item.items():
                setattr(existing, k, v)
        else:
            db.add(Listing(source_id=source.id, **item))
    db.commit()


def start_scheduler():
    sched = AsyncIOScheduler()
    sched.add_job(
        run_once,
        IntervalTrigger(hours=settings.RUN_INTERVAL_HOURS),
        max_instances=1,
    )
    sched.start()
    asyncio.get_event_loop().run_forever()


def cli(argv=None):
    parser = argparse.ArgumentParser(prog="rentbot")
    parser.add_argument("command", choices=["run-once"])
    args = parser.parse_args(argv)
    if args.command == "run-once":
        asyncio.run(run_once())


def main():
    start_scheduler()


if __name__ == "__main__":
    main()
