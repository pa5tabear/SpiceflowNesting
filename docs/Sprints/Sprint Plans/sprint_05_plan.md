## 1 · Sprint Goal (≤25 words)
Add two working website scrapers to ingest real listings into the database.

## 2 · Deliverables & Acceptance Criteria
- **Zillow scraper** – `scrapers/zillow.py` returns ≥10 Ann Arbor listings in integration test; CI green.
- **Craigslist scraper** – `scrapers/craigslist.py` returns ≥10 listings; HTTP mocked in unit tests.
- **Integration test suite** – `pytest -k test_integration_scrapers` passes with live call flag.

## 4 · Workflow
1. Think: outline HTML selectors & error handling.
2. Plan: write failing integration tests with `--live` marker.
3. Code: implement scrapers (<240 LOC total) & register in `SCRAPERS` dict.
4. Test: run `pytest` (unit) then `pytest -m live` locally; CI runs unit only.
5. PR: open `sprint-05` branch; ensure CI green.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % on new modules.
- [ ] No new Python deps; requests mocked in default test run.
- [ ] LOC delta ≤240; commit prefix `feat(s05):`.

## 6 · Proposed Next Sprint
Enhance scheduler for 4× daily runs and add deduplication. 