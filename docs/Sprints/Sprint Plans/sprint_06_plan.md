## 1 · Sprint Goal (≤25 words)
Scrape only listings that already satisfy user-defined rent, beds, and amenity criteria by injecting filters into site URLs.

## 2 · Deliverables & Acceptance Criteria
- **Criteria config** – New `search_criteria.yaml` parsed by `config.py`; includes `max_rent`, `min_beds`, `radius_miles`, `required_amenities`.
- **URL builders** – `scrapers/url_helpers.py` converts criteria → filter params for Zillow & Craigslist; unit tests compare expected URLs.
- **Scraper integration** – `scrapers/zillow.py` & `scrapers/craigslist.py` use helpers; live integration test proves returned listings all pass max_rent & min_beds before local scoring.

## 4 · Workflow
1. Think: map generic criteria to each site's query syntax.
2. Plan: write failing unit tests for URL construction and rent/bed filters.
3. Code: implement YAML load, helpers (<120 LOC total), update scrapers.
4. Test: unit + integration (`--live`); CI runs unit only; badge green.
5. PR: branch `sprint-06`, request review.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % for new code.
- [ ] No new Python dependencies (use PyYAML from stdlib `yaml`).
- [ ] LOC delta ≤120; commit prefix `feat(s06):`.

## 6 · Proposed Next Sprint
Add interval scheduler and deduped run logging. 