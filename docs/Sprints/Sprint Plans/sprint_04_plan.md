## 1 · Sprint Goal (≤25 words)
Accurately geocode listings and apply 1-mile distance filter to enable location-aware scoring and alerts.

## 2 · Deliverables & Acceptance Criteria
- **Implement geocoder utility** – `utils/geo.py: geocode_address()` calls Nominatim via httpx; returns lat/lon; unit test mocks API and passes.
- **Integrate distance filter** – Update `scoring.score_listing()` to skip listings >1 mile; add test fixture asserting ±50 m tolerance.
- **Back-fill missing coords** – Scheduler populates lat/lon via geocoder when scraper lacks them; `pytest -k test_scheduler_geo` green.

## 4 · Workflow
1. Think: define function signature, error handling, mock strategy.
2. Plan: draft failing tests for geocoder + distance filter.
3. Code: implement utility, scoring change, scheduler hook (<120 LOC).
4. Test: run `pytest`, `ruff check .`, `black --check .` locally.
5. PR: push branch `sprint-04`, ensure CI green.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % for changed files.
- [ ] No new Python dependencies; HTTP requests mocked in tests.
- [ ] LOC delta ≤120; functions typed & documented.
- [ ] Commit message starts with `feat(s04):`.

## 6 · Proposed Next Sprint
Build natural-language geosearch CLI leveraging new geocoder. 