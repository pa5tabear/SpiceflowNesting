## 1 · Sprint Goal (≤25 words)
Restore green CI by correcting Ruff invocation and committing the first Alembic migration aligned with current models.

## 2 · Deliverables & Acceptance Criteria
- **Fix Ruff step in CI** – Update `.github/workflows/ci.yml` to `ruff check .`; workflow passes lint stage.
- **Generate initial migration** – `alembic revision --autogenerate -m "baseline"` creates `migrations/versions/<hash>_baseline.py`; `alembic upgrade head` succeeds locally and in CI.
- **CI green badge** – All jobs in `CI` workflow succeed on PR; coverage ≥85 % unchanged.

## 4 · Workflow
1. Think: reproduce CI failure locally, outline fixes.
2. Plan: draft change to CI YAML and run Alembic autogenerate.
3. Code: implement changes within 60 LOC.
4. Test: run `ruff check .`, `pytest`, and `alembic upgrade head` locally; push branch.
5. PR: open `sprint-03` branch; ensure GitHub Actions passes.

## 5 · Self-Review Rubric
- [ ] `CI` workflow green on branch.
- [ ] No new dependencies; LOC delta ≤60.
- [ ] Migration script has reversible `downgrade()`.
- [ ] Commit message starts with `fix(s03):`.
- [ ] README badge reflects passing status once merged.

## 6 · Proposed Next Sprint
Add geocoder utility and distance filter leveraging the stable database schema. 