## 1 · Sprint Goal (≤25 words)
Inject user criteria into site URLs **and** automate 4×-daily deduped scraping with run logging.

## 2 · Deliverables & Acceptance Criteria
- **Criteria URL filters** – `search_criteria.yaml` parsed; `url_helpers.py` builds price/bed params for Zillow + Craigslist; integration test proves pre-filtered results pass max_rent & min_beds.
- **Interval scheduler & run log** – `scheduler.py` uses `RUN_INTERVAL_HOURS`; new `runs` table (+ migration) records each job; duplicate listings per run ≤1.
- **CLI entrypoint** – `poetry run rentbot run-once` triggers one cycle; README updated.

## 4 · Workflow
1. Think: map criteria → site params, design dedupe query.
2. Plan: write failing tests (URL builder, dupe prevention, CLI exit 0).
3. Code: implement all features (<180 LOC total) & migration.
4. Test: unit + optional `--live` integration; CI green.
5. PR: branch `sprint-07`, request review.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % on new code.
- [ ] No new deps; LOC delta ≤180.
- [ ] README documents criteria YAML and CLI.
- [ ] Commit prefix `feat(s07):`.

## 6 · Proposed Next Sprint
Implement scoring algorithm v1 (price, distance, amenities, sentiment). 