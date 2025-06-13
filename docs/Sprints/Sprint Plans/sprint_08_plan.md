## 1 · Sprint Goal (≤25 words)
Score each listing 0-100 using price, distance, amenities, and sentiment subscores.

## 2 · Deliverables & Acceptance Criteria
- **Price percentile calc** – nightly 25th-percentile price-per-sqft computed from DB; unit test with synthetic data passes.
- **Scoring implementation** – `scoring.py` returns dict with subscores (price 40 %, amenities 25 %, distance 10 %, sentiment 25 %); all criteria from `search_criteria.yaml` still enforced.
- **Sentiment stub & tests** – OpenAI call wrapped in `_sentiment()` with fallback mock; fixtures ensure total score 0-100; coverage ≥85 %.

## 4 · Workflow
1. Think: outline helper functions and test vectors.  
2. Plan: write failing tests for each sub-score.  
3. Code: implement (<120 LOC) price calc, scoring logic, sentiment stub.  
4. Test: `pytest`; CI green.  
5. PR: branch `sprint-08`, request review.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % on new code.  
- [ ] LOC delta ≤120; no new deps.  
- [ ] Docstrings explain weight tuning.  
- [ ] Commit prefix `feat(s08):`.

## 6 · Proposed Next Sprint
Add daily email digest via SendGrid with Jinja template. 