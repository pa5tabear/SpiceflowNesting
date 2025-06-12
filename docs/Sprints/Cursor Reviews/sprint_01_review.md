# Sprint 01 – Cursor PM+QA Review

## Progress & Status
The repository skeleton has been initialised in Git, the `pyproject.toml` with Black + Ruff tooling is in place, and the core package structure (`config.py`, `models.py`, `scheduler.py`, etc.) is committed. A working `docker-compose.yml` for Postgres is **still missing** and no CI workflow file has been added, so only ~80 % of the original Sprint-01 goals are met.

## Green Badges & Metrics
*CI pipeline not yet configured – no status badge available.*  
Unit-test suite is empty; code-coverage tooling is absent.  
Total LOC (Python): ≈ 750 lines across 11 files (--).

## Demo-able Capability
Developers can:
1. `poetry install` and run `python -m scheduler` locally (though it errors without a DB).  
2. Inspect placeholder scrapers (e.g. `scrapers/zillow.py`) as examples.

## Blockers / Costs / Risks
* Major risk: lack of automated CI means future PRs may break the build invisibly.  
* Postgres container & Alembic migrations are not in place ➞ runtime errors.  
* No `.env.example` file yet – onboarding friction.

## Failing CI Steps
_(N/A – CI not configured)_

## TODOs Merged
No in-code `TODO` markers were found in the current commit range.

## Decisions Needed
• Confirm whether SQLite or Dockerised Postgres should back unit tests in Sprint 02.  
• Approve LOC budget (≤ 120) and coverage target (≥ 85 %) for upcoming data-model work. 