## 1 · Sprint Goal (≤25 words)
Automate 4×/day scraping with dedup logic and run logging, using the new criteria-aware scrapers.

## 2 · Deliverables & Acceptance Criteria
- **Interval scheduler** – `scheduler.py` obeys `RUN_INTERVAL_HOURS`; two runs 6 h apart insert ≤1 duplicate listing.
- **Run log table** – SQLAlchemy `Run(id, started_at)` + Alembic migration; each job row inserted and visible in tests.
- **CLI command** – `poetry run rentbot run-once` executes one full cycle and exits 0; README updated.

## 4 · Workflow
1. Think: design dedupe query & logging schema.  
2. Plan: write failing tests for duplicate prevention and CLI exit code.  
3. Code: implement (<120 LOC) plus migration.  
4. Test: pytest; CI green.  
5. PR: branch `sprint-07`, request review.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % new lines.  
- [ ] LOC ≤120; no new deps.  
- [ ] README documents CLI.  
- [ ] Commit prefix `feat(s07):`.

## 6 · Proposed Next Sprint
Implement scoring algorithm v1 (price, distance, amenities, sentiment). 