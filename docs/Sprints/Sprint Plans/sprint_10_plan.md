## 1 · Sprint Goal (≤25 words)
Close the feedback loop and prepare production launch with basic observability and release docs.

## 2 · Deliverables & Acceptance Criteria
- **Feedback endpoint** – `feedback.py` exposes `/feedback` FastAPI route; thumbs-up/down updates `scores.feedback` column; unit test posts JSON and asserts DB updated.
- **Observability** – Integrate `loguru` structured logging; add Prometheus counter for runs and email sends; CI asserts log lines present.
- **Release docs** – `DEPLOYMENT.md` gives Docker Compose + systemd instructions; includes TLS and environment setup; merged PR tagged `v1.0`.

## 4 · Workflow
1. Think: define DB schema change and API route spec.  
2. Plan: write failing tests for feedback route and log presence.  
3. Code: add Alembic migration, API module, logging integration (<180 LOC total).  
4. Test: pytest; CI green.  
5. PR: branch `sprint-10`, review, tag `v1.0` after merge.

## 5 · Self-Review Rubric
- [ ] CI green; coverage ≥85 % new lines.  
- [ ] LOC delta ≤180; no new deps beyond `fastapi`, `uvicorn` (already allowed).  
- [ ] `DEPLOYMENT.md` validated via shell snippet.  
- [ ] Commit prefix `feat(s10):`.

## 6 · Proposed Next Sprint
Project maintenance mode; backlog triage and stretch goals (multi-city support). 