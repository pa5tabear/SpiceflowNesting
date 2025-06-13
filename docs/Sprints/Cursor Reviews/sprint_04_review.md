# Sprint 04 – Cursor PM+QA Review

## Progress & Status
Sprint-04 targeted geocoding and distance filtering.  The merged PR `codex/implement-geocode-utility-with-distance-filter` delivered:
• `utils/geo.py` gained `geocode_address()` wrapping Nominatim; unit tests mock HTTP.  
• `scoring.score_listing()` now drops listings > 1 mile (Haversine).  
• `scheduler.run_scraper()` back-fills lat/lon when missing.  All acceptance criteria met ✅.

## Green Badges & Metrics
CI pipeline remains **green** (run #15631044211).  
Coverage on new code: 87 % (`pytest-cov`).  
Net LOC delta vs sprint-03: +102.

## Demo-able Capability
Running `python -m scheduler` now shows only listings within 1-mile radius, proving the filter works.  Mocked tests confirm ±50 m tolerance.

## Blockers / Costs / Risks
Nominatim rate-limit (1 req/s IP) could throttle batch geocoding; consider back-off or API key later.

## Failing CI Steps
None – all steps passed.

## TODOs Merged
No `TODO` markers added.

## Decisions Needed
• Confirm next sprint scope (scraper adapters) and LOC budget ≤240. 