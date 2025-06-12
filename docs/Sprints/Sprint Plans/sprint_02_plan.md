## 1 · Sprint Goal (≤25 words)
Establish reliable Postgres-backed data model with migrations, unit tests, and green CI pipeline to unblock future feature development.

## 2 · Deliverables & Acceptance Criteria (max 3 tasks)
- **Define SQLAlchemy schema & migrations** – `models.py` declares Source, Listing, Score; Alembic `revision --autogenerate` runs cleanly against Postgres & SQLite.
- **Unit-test CRUD & constraints** – `pytest -k test_models` passes on CI; covers unique index & FK relationships; ≥85 % coverage for models module.
- **Bootstrap CI workflow** – `.github/workflows/ci.yml` runs Ruff lint, Black check, and pytest in <3 min; badge added to README.

## 4 · Workflow
1. Think: outline model classes, constraints, test matrix.
2. Plan: draft Alembic upgrade + downgrade scripts.
3. Code: implement models & migration within 120 LOC budget.
4. Test: write failing tests first, then satisfy them locally; ensure CI script passes.
5. PR: open `sprint-02` branch, request review.

## 5 · Self-Review Rubric
- [ ] All tests & CI green locally.
- [ ] No new Python dependencies; LOC delta ≤120.
- [ ] `models.py` and migration scripts fully type-annotated & doc-stringed.
- [ ] README updated with DB quick-start.
- [ ] Commit message starts with `feat(s02):`.

## 6 · Proposed Next Sprint
Implement geocoder utility and distance filter leveraging the new database schema. 