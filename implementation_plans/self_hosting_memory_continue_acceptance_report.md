# Self-Hosting Memory and Continue Acceptance Report

Date: 2026-07-06
Plan: `implementation_plans/sys-for-ai-dev_memory_continue_self_hosting_implementation_plan.md`
Acceptance AgentJob: `AJ-P1-SELFHOST-ACCEPTANCE-001`
Completion receipt: `RECEIPT-P1-SELFHOST-ACCEPTANCE-001`
Handoff: `HANDOFF-P1-SELFHOST-ACCEPTANCE-001`

## Scope

This report closes Phase 10 of the self-hosting memory and `/continue` implementation plan. It verifies the file-backed Phase 1 implementation that now exists in `sys-for-ai/` inside the `sys-for-ai-dev` development workspace.

This acceptance does not claim production autonomous development, a vector-memory service, a multi-service runtime, or generated derivative authority. It accepts the deterministic offline kernel requested by the plan: source-first memory navigation, one-AgentJob continuation packets, receipts, handoffs, boundary validation, generated derivative checks, and active runtime skill surfaces.

## Acceptance Checklist

| ID | Criterion | Evidence | Result |
| --- | --- | --- | --- |
| SFA-ACCEPT-001 | Self-hosting boundary policy exists and is registered. | `implementation_plans/self_hosting_boundary_decision_record.md`; `sys-for-ai/docs/self_hosting_boundary_policy.md`; `sys-for-ai/registries/source_registry.csv` | PASS |
| SFA-ACCEPT-002 | Program state exists validates and is registered. | `sys-for-ai/control_records/program_state.yaml`; `sys-for-ai/registries/control_record_registry.csv`; `make validate-program-state` | PASS |
| SFA-ACCEPT-003 | Director decision records exist validate and are registered. | `sys-for-ai/control_records/director_decisions/DDR-P1-SELFHOST-001.yaml`; `sys-for-ai/registries/director_decision_registry.csv`; `make validate-director-decisions` | PASS |
| SFA-ACCEPT-004 | Operational AgentJob v0.2 contract exists and validates. | `sys-for-ai/schemas/contracts/agentjob_v0_2.schema.json`; `make validate-agentjobs` | PASS |
| SFA-ACCEPT-005 | Handoff v0.2 and completion receipt v0.2 contracts exist and validate. | `sys-for-ai/schemas/contracts/handoff_v0_2.schema.json`; `sys-for-ai/schemas/contracts/completion_receipt_v0_2.schema.json`; `make validate-handoffs`; `make validate-completion-receipts` | PASS |
| SFA-ACCEPT-006 | Memory preflight receipt contract exists and validates. | `sys-for-ai/schemas/contracts/memory_preflight_receipt.schema.json`; `sys-for-ai/control_records/memory_preflights/MEMPREFLIGHT-P1-SELFHOST-ACCEPTANCE-001.yaml`; `make validate-memory-preflight` | PASS |
| SFA-ACCEPT-007 | Operational registry files exist with expected headers. | `sys-for-ai/registries/*.csv`; `make bootstrap-memory`; `make validate-registry-graph` | PASS |
| SFA-ACCEPT-008 | Memory status lookup search and preflight commands work. | `sys-for-ai/sys_for_ai/memory/`; `sys-for-ai/sys_for_ai/cli.py`; unit tests; `make validate` | PASS |
| SFA-ACCEPT-009 | `/continue` status preflight select and packet commands work. | `sys-for-ai/sys_for_ai/control_loop/`; `make validate-control-loop`; `make validate` | PASS |
| SFA-ACCEPT-010 | `/continue` selects at most one AgentJob. | `sys-for-ai/sys_for_ai/control_loop/job_selection.py`; `sys-for-ai/sys_for_ai/control_loop/validators.py`; `make validate-one-active-agentjob` | PASS |
| SFA-ACCEPT-011 | Missing route produces a Director Decision Required packet. | `sys-for-ai/tests/test_continue_packet.py`; `make validate-control-loop`; terminal program state has no active Director decision | PASS |
| SFA-ACCEPT-012 | Multiple active AgentJobs produce a stop packet. | `sys-for-ai/tests/test_continue_packet.py`; `sys-for-ai/sys_for_ai/control_loop/job_selection.py` | PASS |
| SFA-ACCEPT-013 | Generated derivatives remain noncanonical. | `sys-for-ai/registries/derivative_registry.csv`; `sys-for-ai/docs/generated/`; `make validate-generated-derivatives` | PASS |
| SFA-ACCEPT-014 | Diff-to-allowlist validator blocks unauthorized changed paths. | `sys-for-ai/sys_for_ai/control_loop/boundaries.py`; `sys-for-ai/tests/test_agentjob_boundaries.py`; `make validate-check-diff` | PASS |
| SFA-ACCEPT-015 | Active `.agents` skills exist. | `.agents/skills/continue/`; `.agents/skills/source-first-memory/`; `sys-for-ai/tests/test_skill_surfaces.py` | PASS |
| SFA-ACCEPT-016 | `.codex` skill files are compatibility shims. | `.codex/skills/continue/SKILL.md`; `.codex/skills/source-first-memory/SKILL.md`; `sys-for-ai/tests/test_skill_surfaces.py` | PASS |
| SFA-ACCEPT-017 | Product scaffold skills are generic and not Codex-locked. | `sys-for-ai/skills/core/continue/`; `sys-for-ai/skills/core/source-first-memory/`; `make validate-skills` | PASS |
| SFA-ACCEPT-018 | Generated derivative pages include authority notices and metadata blocks. | `sys-for-ai/docs/generated/configuration_control/`; `sys-for-ai/docs/generated/validation_contracts/`; `make validate-generated-derivatives` | PASS |
| SFA-ACCEPT-019 | Requirement trace registry is updated for newly covered Phase 0 and Phase 1 requirements. | `sys-for-ai/registries/requirement_trace_registry.csv`; `make validate-requirement-trace` | PASS |
| SFA-ACCEPT-020 | `make validate` passes. | Project-local `.venv`; `cd sys-for-ai && make validate` | PASS |

## Validation Commands

The Phase 10 acceptance chain is the command list in section 20.3 of the implementation plan:

```bash
cd sys-for-ai
make doctor
make validate-agentjobs
make validate-skills
make validate-format-profiles
make validate-config-sources
make validate-control-records
make validate-validation-contract-registry
make validate-toml-config
make validate-jsonschema-contracts
make validate-registry-graph
make validate-requirement-trace
make validate-program-state
make validate-control-loop
make validate-memory-preflight
make validate-handoffs
make validate-completion-receipts
make validate-generated-derivatives
make validate
```

## Conclusion

Conclusion: Accepted.

The implementation satisfies the Phase 10 acceptance criteria for the deterministic Phase 1 self-hosting memory and `/continue` kernel. Future work should start from a new plan or Director decision, inspect `HANDOFF-P1-SELFHOST-ACCEPTANCE-001`, and preserve the boundary between canonical sources, controlled records, and generated derivatives.

## References

sys-for-ai-dev. (2026). *sys-for-ai-dev self-hosting memory and `/continue` implementation plan* [Implementation plan]. `implementation_plans/sys-for-ai-dev_memory_continue_self_hosting_implementation_plan.md`.

sys-for-ai-dev. (2026). *sys-for-ai Phase 0 product and system design PRD* [Product requirements document]. `PRDs/sys-for-ai_phase-0_product_system_design_prd.md`.
