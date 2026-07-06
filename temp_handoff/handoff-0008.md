# Handoff 0008: Phase 7 Boundary and Diff Validators

Date: 2026-07-06
Plan: `implementation_plans/sys-for-ai-dev_memory_continue_self_hosting_implementation_plan.md`
Completed phase: Phase 7 - Boundary and diff validators

## Latest prior handoff check

Before Phase 7 began, the latest handoff was `temp_handoff/handoff-0007.md`. It recommended implementing boundary and diff validators for changed artifacts, generated derivative promotion blocking, stale memory evidence, and runtime-skill drift.

## Work completed

- Added `sys_for_ai.control_loop.boundaries`.
- Added Git diff collection for:
  - `git diff --name-only`
  - `git diff --cached --name-only`
  - `git ls-files --others --exclude-standard`
- Added AgentJob boundary validation against:
  - `allowed_writes`
  - `generated_paths`
  - `forbidden_paths`
  - generated derivative registry paths
  - generated derivative source-authority inversion checks
- Added support for running boundary validation from either repository root or `sys-for-ai/` root.
- Added CLI commands:
  - `validate-agentjob-boundaries --agentjob <id> --git`
  - `validate-check-diff --agentjob <id>`
- Added Makefile targets:
  - `validate-agentjob-boundaries`
  - `validate-check-diff`
- Added `validate-check-diff` to the default `make validate` chain.
- Formalized the Phase 7 AgentJob:
  - `sys-for-ai/control_records/agentjobs/AJ-P1-BOUNDARY-VALIDATORS-001.yaml`
- Registered the Phase 7 AgentJob and new boundary validator sources in:
  - `registries/agentjob_registry.csv`
  - `registries/control_record_registry.csv`
  - `registries/source_registry.csv`
- Updated the continue packet test so the latest Phase 6 handoff now routes to `AJ-P1-BOUNDARY-VALIDATORS-001`.
- Added `tests/test_agentjob_boundaries.py` coverage for allowed paths, outside-allowlist paths, forbidden paths, generated derivative authorization, untracked file collection, repo-root operation, and current-diff validation.

## Validation evidence

The following commands passed:

- `cd sys-for-ai && make validate-agentjob-boundaries validate-check-diff`
- `cd sys-for-ai && .venv/bin/python -m unittest discover -s tests`
- `PYTHONPATH=sys-for-ai sys-for-ai/.venv/bin/python -m sys_for_ai.cli validate-check-diff --agentjob AJ-P1-BOUNDARY-VALIDATORS-001 --json`
- `cd sys-for-ai && make validate`
- `git diff --check`

Observed behavior:

- `validate-agentjob-boundaries --git` allowed all current Phase 7 changed paths and reported no violations.
- `validate-check-diff` reported no violations.
- The boundary tests fail explicit unauthorized paths in unit coverage.
- The boundary tests fail forbidden `LICENSE` changes in unit coverage.
- The boundary tests fail generated derivative changes without `generated_paths` authorization in unit coverage.
- The untracked-file test uses a temporary Git repository and confirms untracked paths are collected.
- `continue-packet` now selects `AJ-P1-BOUNDARY-VALIDATORS-001` through the latest handoff route.

## Remaining uncertainty

Phase 7 blocks generated derivative edits unless an AgentJob declares `generated_paths`, but the generated derivative files are still stub-maintained. The next phase should replace or supplement those stubs with deterministic generators.

The validator implements the generated-derivative canonical-source inversion check through registry rows. It does not inspect arbitrary natural-language claims inside generated pages beyond existing generated derivative validation.

## Next logical step

Implement Phase 8: generated derivative generators for the Configuration and Control Wiki and Validation Contracts Catalog.
