## 1 · Sprint Goal (≤25 words)
Run the bot 4× daily with duplicate-safe scheduling and a manual CLI trigger.

## 2 · Deliverables & Acceptance Criteria
- **Interval scheduler** – `scheduler.py` reads `RUN_INTERVAL_HOURS`; two runs 6 h apart insert ≤1 duplicate listing.
- **Run log table** – SQLAlchemy `Run(id, started_at)` + Alembic migration; each job row inserted and visible in tests.
- **CLI entrypoint** – `poetry run rentbot run-once` executes one full cycle and exits 0; README updated.

## 4 · Workflow
1. Think: design dedupe query & logging schema.
2. Plan: write failing tests for duplicate prevention and CLI exit code.
3. Code: implement (<120 LOC) plus migration.
4. Test: pytest; CI green.
5. PR: branch `sprint-07`, request review.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % on new code.
- [ ] LOC ≤120; no new deps.
- [ ] README documents CLI usage.
- [ ] Commit prefix `feat(s07):`.

## 6 · Proposed Next Sprint
Implement scoring algorithm v1. 