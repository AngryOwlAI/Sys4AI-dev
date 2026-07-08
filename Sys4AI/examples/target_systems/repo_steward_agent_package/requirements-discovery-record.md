# Requirements Discovery Record

Discovery ID: `RDR-REPO-STEWARD-SMOKE-001`
Target system ID: `repo_steward_agent_sample`
Status: derivative draft smoke example
Subject layer: `target_system_instance`

## User Intent

The sample target system inspects a repository in read-only mode and produces a governed next-action plan.

## Constraints

- The package is a smoke example and derivative draft.
- It is not a production target system.
- The example performs no external service calls.
- The example does not claim repository semantic correctness.

## Candidate Requirements

- `RSS-FR-001`: Inspect repository files in read-only mode.
- `RSS-FR-002`: Summarize current repository state.
- `RSS-FR-003`: Produce a governed next-action plan with validation notes.
- `RSS-NFR-001`: Keep all package artifacts structurally traceable.
- `RSS-NFR-002`: Preserve the target-system instance boundary.
