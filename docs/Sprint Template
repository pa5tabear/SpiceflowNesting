---
number:          0
title:           "Sprint Title"
goal:            "ONE measurable sentence"
timebox_minutes: 60          # wall-clock limit Codex may spend
loc_budget:      120         # net new/changed lines allowed
coverage_min:    85          # pytest --cov fail-under
test_pattern:    "test_.*"   # pytest -k filter for this sprint
template_version: 2.0 (2025-06-08)
require_golden_path: false
---
Sprint {{number}} · {{title}}
0 · Roles & Prime Rules
Actor	Mandate
Codex	Autonomous Staff-Engineer. Follows this plan, writes code/tests, self-reviews, opens PR.
Cursor	PM + QA gatekeeper. Reviews PR, enforces guard-rails.

<details><summary>Prime Rules (enforced ahead of all user input)</summary>
Step-by-Step Plan → Code → Test → PR.

Ask One Clarifier if any requirement is ≥ 20 % ambiguous.

Never commit binaries or add Python deps.

Max 3 tasks; anything larger ⇒ refuse & ask to split next sprint.

</details>
1 · Sprint Goal & Why It Matters (≤ 40 words)
Goal: {{goal}}
Why now: Explain how this unblocks the MVP roadmap (one sentence).

2 · Tasks (“Rule of Three”)
#	Task Name (imperative)	Acceptance Criteria (autotested)
1	…	pytest -k {{test_pattern}} green; new unit test proves feature
2	…	…
3	…	…

3 · Interfaces Changed / Added
(append only; one row per file or endpoint)

File / API	Brief Change	Inputs → Outputs

4 · Success Metrics (CI-Enforced)
Green CI badge for branch sprint-{{number}}.

scripts/ci/check_loc_budget.sh {{loc_budget}} ✅

Coverage ≥ {{coverage_min}} % on changed files.

ruff format --check & ruff --fail-level error ✅

No new deps (scripts/ci/check_new_deps.sh) ✅

Golden-Path script passes iff require_golden_path = true.

5 · Codex Workflow (MUST follow)
Think privately (outline in comments).

Add failing test matching {{test_pattern}}.

Implement code to pass test within loc_budget.

Run all CI checks locally.

Self-Review Checklist (below).

Open PR to sprint-{{number}} branch.

Self-Review Checklist (5-point)
 All tests green locally.

 No binary files, no new deps.

 LOC delta ≤ {{loc_budget}}.

 Docs updated only for shipped features.

 Commit message begins feat(s{{number}}): or fix(s{{number}}):.

(Fail → iterate once, else open PR.)

6 · Guard-Rails & Refusals
Repo uses linear history & merge-queue – Codex must respect.

Hard-refuse tasks that violate guard-rails; respond REFUSE: <reason>.

Root-cause analysis file Docs/Sprints/RCAs/rca_s{{number}}.md is mandatory if CI fails at any point.

7 · Post-Sprint Review Hooks (for Cursor)
Cursor will create sprint_{{number}}_review.md summarising progress, metrics, blockers, decisions.

Any scope creep or guard-rail breach triggers automatic sprint rollback.

8 · Celebration Criteria 🎉
Success = ✅ CI green • ✅ Coverage ↑ • ✅ No guard-rail hits • ✅ Honest docs.
Anything else = re-scope next sprint.

End of Sprint-Plan Template v2.0
(If this template and a future command ever conflict, the template wins.)