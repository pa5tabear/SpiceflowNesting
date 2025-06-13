# Sprint 05 – Cursor PM+QA Review

## Progress & Status
Goal was to add two production-ready scrapers. PR `codex/add-zillow-and-craigslist-scrapers` merged and delivered:
• `scrapers/zillow.py` – emits ≥15 live listings; selectors resilient to missing fields.  
• `scrapers/craigslist.py` – parses HTML to yield ≥20 listings in integration test.  
• `tests/test_integration_scrapers.py` with `--live` marker; mocked unit tests run in CI.  All Sprint-05 acceptance criteria met.

## Green Badges & Metrics
CI run #15633117781: **✔︎ success**.  
Coverage overall 86 % (+3 %).  
LOC delta vs sprint-04: +198 (under 240 budget).

## Demo-able Capability
Running `python -m scheduler` now ingests real Zillow & Craigslist data; database shows ~35 downtown listings after first run.

## Blockers / Costs / Risks
• Craigslist sometimes serves geo-obscured posts; ~10 % fail distance filter – acceptable for now.  
• Zillow paging beyond first 40 results not yet implemented.

## Failing CI Steps
N/A – all jobs passed.

## TODOs Merged
No new `TODO` tags found.

## Decisions Needed
• Approve Sprint-06 scope: interval scheduler, CLI trigger, run log table; LOC budget ≤120. 