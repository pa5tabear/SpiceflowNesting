# SpiceflowNesting

This repository contains a reference scaffold for a rental-listing monitor and agent. It includes a 10‑sprint project plan and minimal runnable code skeleton. Supply your API keys in `.env` and expand each scraper to start experimenting.

## 10‑Sprint Project Plan

| # | Sprint Theme | Goals & Acceptance Criteria | Key Tasks | Primary Deliverables |
|---|--------------|----------------------------|-----------|----------------------|
|1|Repo & DevOps foundation|Public repo, CI pipeline runs, `.env.example`|Create repo, set up Poetry, Black, Ruff, GitHub Actions, Docker compose|`README.md`, green CI|
|2|Data‑model + Storage|Normalized schema for Listing, Source, Run, Score|Draft ERD, implement SQLAlchemy models and Alembic|`models.py`, migration scripts|
|3|Geocoder & distance filter|Haversine distance < 1 mi to Liberty & Main|Build `utils.geo`, add geocoder API|`utils/geo.py`, tests|
|4|Scraper framework|Abstract base scraper|Use Playwright/BeautifulSoup|`scrapers/base.py`, `core/http.py`|
|5|Website adapters (MVP set)|Working scrapers for Zillow, etc.|Site-specific parsers, save HTML|`scrapers/zillow.py` … |
|6|Scheduler (4×/day)|APScheduler job table, CLI|Asyncio app, dedupe runs|`scheduler.py`, docs|
|7|Scoring algorithms v1|Deterministic score 0–100|Market stats, amenities, sentiment|`scoring.py`, tests|
|8|Agentic layer|Reflex-style loop|LangChain or CrewAI|`agent.py`, architecture doc|
|9|Notification & Feedback|Daily email and Slack pings|Jinja templates, webhook feedback|`notifier.py`, `feedback.py`|
|10|Observability & Launch|End‑to‑end test, prod deployment guide|Structured logging, Docker Compose|`DEPLOYMENT.md`, release tag|

## Quick‑start

```bash
git clone <repo>
cd <repo>
cp .env.example .env  # add your keys
poetry install
poetry run python -m scheduler
```
