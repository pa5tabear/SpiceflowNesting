# Sprint 02 – Cursor PM+QA Review

## Progress & Status
Sprint-02 aimed to deliver data-model + migrations + green CI.  A PR (`codex/define-sqlalchemy-schema--migrations`) was merged adding:
• `models.py` rewritten with type-hints and docstrings.  
• Alembic scaffold (`alembic.ini`, `migrations/…`).  
• SQLite-backed unit tests (`tests/test_models.py`).  
• GitHub Actions `ci.yml` workflow.  

Migrations exist but are **empty** (no revision file generated).  CI pipeline is red ‑ failing at the Ruff lint step, so acceptance criteria "green CI badge" not met.

## Green Badges & Metrics
*CI* status: **❌ failure** (ruff step).  
Coverage step did not run due to earlier failure.  
Net LOC delta since sprint-01: ≈ +350 (models + tests + CI files).

## Demo-able Capability
Developers can now run `pytest` locally and see CRUD tests passing against an in-memory SQLite DB.  No automated migration yet for Postgres.

## Blockers / Costs / Risks
• Ruff invocation incorrect (`ruff .`), halting CI.  
• No Alembic revision file – migrations cannot be applied.  
• Risk of broken main until CI fixed; merge-queue guard-rail not yet enforced.

## Failing CI Steps
Job **CI / test / Run ruff .** ➜ `error: unrecognized subcommand '.'` (Ruff ≥0.4 expects `ruff check .`).

## TODOs Merged
No `TODO` comments introduced in this sprint.

## Decisions Needed
• Approve a hot-fix commit to change CI command to `ruff check .` and add initial Alembic revision.  
• Decide if failing run blocks start of Sprint-03 or is tackled as Sprint-02 remediation. 