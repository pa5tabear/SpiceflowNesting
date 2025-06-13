## 1 · Sprint Goal (≤25 words)
Automate scraping 4× daily with deduplicated runs and a one-shot CLI entrypoint.

## 2 · Deliverables & Acceptance Criteria
- **Interval scheduler** – `scheduler.py` uses `RUN_INTERVAL_HOURS` to schedule jobs; two consecutive runs add ≤1 duplicate listing (constraint enforced).
- **Run log table** – new SQLAlchemy model `Run(id, started_at)` + Alembic migration; each job inserts a row.
- **CLI command** – `poetry run rentbot run-once` triggers a single scrape + score cycle; README updated.

## 4 · Workflow
1. Think: design dedupe query & run logging.  
2. Plan: write failing tests for duplicate prevention and CLI exit code.  
3. Code: implement features (<120 LOC) and migration.  
4. Test: `pytest`; ensure CI green.  
5. PR: branch `sprint-06`, request review.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % on new lines.  
- [ ] LOC delta ≤120; no new dependencies.  
- [ ] `README.md` showcases CLI usage.  
- [ ] Commit message prefix `feat(s06):`.

## 6 · Proposed Next Sprint
Implement deterministic scoring algorithm v1. 