# Sprint 08 – Cursor PM+QA Review

## Progress & Status
Sprint-08 targeted the first full scoring algorithm.  PR `codex/implement-scoring-system-and-sentiment-stub` merged and delivered:
• Nightly 25-percentile price-per-sqft calculation added to `scoring.refresh_scores()`.  
• `scoring.score_listing()` now returns subscores: price (40 %), amenities (25 %), distance (10 %), sentiment (25 %); total 0-100.  
• Sentiment stub calls OpenAI when key set, otherwise returns 0.5; unit tests mock the call.  All deliverables met ✅.

## Green Badges & Metrics
CI run #15636110055: **✔︎ success**.  
Coverage overall 88 % (+3 %).  
LOC delta +115 (within 120 budget).

## Demo-able Capability
Running `poetry run rentbot run-once` now prints a Top-10 list with scores and subscores in JSON; listings below 60 are dropped.  Database `scores` table populated with first batch.

## Blockers / Costs / Risks
• Sentiment relies on OpenAI; exceeding free quota will drop to default 0.5 score.  
• Market percentile function runs in-process; consider nightly cron if dataset grows large.

## Failing CI Steps
N/A – all steps passed.

## TODOs Merged
`TODO` note added in `scoring.py` about later learning from thumbs-up/-down feedback.

## Decisions Needed
• Approve Sprint-09 scope: email notifier via SendGrid; LOC budget ≤120. 