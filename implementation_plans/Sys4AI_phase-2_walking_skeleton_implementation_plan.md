# Sys4AI Phase 2 Walking Skeleton Implementation Plan

**Plan ID:** `SFA-P2-WALKING-SKELETON-IMPLEMENTATION-PLAN-001`
**Status:** Controlled implementation plan accepted by `RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001`
**Prepared date:** 2026-07-08
**Source PRD:** `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`
**Producing AgentJob:** `AJ-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001`
**Subject system:** Sys4AI
**Subject layer:** `framework_product`

## 1. Source PRD

This plan implements the controlled Phase 2 walking skeleton PRD:

- `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`
- RDR source: `Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md`
- Prior handoff: `Sys4AI/control_records/handoffs/HANDOFF-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml`
- Scope plan: `implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md`

The PRD authorizes planning and later bounded implementation packets. It does not authorize production runtime claims or autonomous operation claims.

## 2. Product Summary

The walking skeleton proves that Sys4AI can carry a target-system idea through an auditable artifact chain:

1. `/init` or equivalent target-system intent classification.
2. Requirements Discovery Record.
3. Product Requirements Document.
4. Implementation plan.
5. Bounded AgentJobs.
6. Structural validation evidence.
7. Package or export smoke artifact.

The demonstration is structural. It proves source trace, controlled transitions, validators, and package shape. It does not prove semantic correctness for a real target system.

## 3. Repository Context

Current repository evidence shows:

- The active product scaffold is under `Sys4AI/`.
- The active runtime skills are under `.agents/skills/`.
- The Phase 2 RDR and PRD already exist and are controlled.
- The current `Sys4AI/Makefile` exposes validation targets, but no walking-skeleton or target-package validation target exists yet.
- No `Sys4AI/sys_for_ai/walking_skeleton.py`, `Sys4AI/sys_for_ai/target_package.py`, or `Sys4AI/sys_for_ai/trace_flow.py` module exists yet.
- No `Sys4AI/examples/target_systems/` package surface exists yet.
- Generated docs under `Sys4AI/docs/generated/` remain derivative navigation surfaces.

The logical design is therefore a small deterministic CLI and validation surface, not a runtime orchestrator.

## 4. Assumptions

1. The concrete smoke scenario will be `repo_steward_agent_sample`, a read-only repository steward example.
2. The package output will be a local repository example under `Sys4AI/examples/target_systems/repo_steward_agent_package/`.
3. The first implementation slice should validate artifact connectivity before package export is added.
4. The package validator should use existing Python and registry helpers where practical.
5. All Phase 2 validation remains offline and deterministic.

## 5. Open Questions

| ID | Question | Handling |
| --- | --- | --- |
| `OPEN-P2-001` | What concrete target-system example should the walking skeleton use? | Resolved for this plan as `repo_steward_agent_sample`; later packets may refine content without claiming production utility. |
| `OPEN-P2-002` | What exact package or export artifact shape counts as smoke evidence? | Resolved as a local example package with README, manifest, RDR, PRD, plan, task packets, trace, artifact index, and validation summary. |
| `OPEN-P2-003` | Should the flow require exactly three task packets or allow more? | Use three bounded task packets for the smoke example unless validation exposes a trace gap. |

## 6. Requirement Traceability Matrix

| PRD requirement | Implementation task | Validation or deferral |
| --- | --- | --- |
| `SFA-P2-WS-FLOW-001` | AJ-20 validates the RDR to PRD to plan to AgentJob chain. AJ-21 adds the package surface. AJ-22 demonstrates the full chain. | `validate-walking-skeleton`, `validate-target-package-smoke`, and demo acceptance report. |
| `SFA-P2-WS-FLOW-002` | AJ-20, AJ-21, and AJ-22 each update receipts, handoffs, and program state through `/continue`. | `validate-control-loop` and completion receipts. |
| `SFA-P2-WS-RDR-001` | Already satisfied by WS-17. AJ-20 consumes it as required flow input. | RDR existence and source trace checked by walking-skeleton validator. |
| `SFA-P2-WS-PRD-001` | Already satisfied by WS-18. AJ-20 consumes it as required flow input. | PRD existence and trace checked by walking-skeleton validator. |
| `SFA-P2-WS-PLAN-001` | Satisfied by this implementation plan. | This plan plus AJ-19 receipt and `validate-requirement-trace`. |
| `SFA-P2-WS-AJ-001` | Satisfied by pending AJ-20, AJ-21, and AJ-22 created by this packet. | `validate-agentjob-registry` and targeted AgentJob validation. |
| `SFA-P2-WS-PACKAGE-001` | AJ-21 creates the package surface. AJ-22 validates it as part of acceptance. | `validate-target-package-smoke`; no production-readiness claim. |
| `SFA-P2-WS-TRACE-001` | AJ-20 adds flow trace checks. AJ-21 adds package trace files. AJ-22 checks end-to-end trace evidence. | `validate-requirement-trace`, flow validator, package validator, acceptance report. |
| `SFA-P2-WS-VAL-001` | AJ-20 and AJ-21 add validators. AJ-22 separates proven claims from review-only claims. | Validator outputs and `PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md`. |
| `SFA-P2-WS-NFR-001` | AJ-20 and AJ-21 register generated and example artifacts as derivative or controlled smoke evidence. | `validate-generated-derivatives` and source registry review. |
| `SFA-P2-WS-NFR-002` | All Phase 2 packets prohibit production, autonomous operation, and domain semantic correctness claims. | AgentJob forbidden actions and AJ-22 claims-not-proven section. |

## 7. Proposed Technical Approach

Use three bounded slices:

1. **Flow validator:** Add `walking_skeleton.py` and `trace_flow.py` plus CLI commands that verify required artifact presence and trace relationships.
2. **Package smoke surface:** Add `target_package.py`, templates or example package content, and a validator for the local package shape.
3. **Demonstration and acceptance:** Run the validators, produce an acceptance report, and state what is proven versus not proven.

The first two slices may update `Sys4AI/Makefile` with stable deterministic targets:

```bash
cd Sys4AI
.venv/bin/python -m sys_for_ai.cli walking-skeleton validate-flow --json
.venv/bin/python -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
```

The aggregate `make validate` should include the new targets only after each target is deterministic and covered by tests.

## 8. Implementation Phases

| Phase | AgentJob | Main output | Stop condition |
| --- | --- | --- | --- |
| 1 | `AJ-SFADEV-20-WALKING-SKELETON-FLOW-001` | Flow validator, trace helper, CLI command, tests, derivative flow report. | Stop if the flow cannot be validated offline from controlled sources. |
| 2 | `AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001` | Package validator, sample package, tests, package source and derivative rows. | Stop if the package surface cannot avoid framework authority confusion. |
| 3 | `AJ-SFADEV-22-WALKING-SKELETON-DEMO-001` | Acceptance report, validation transcript, closeout receipt and handoff. | Stop if any required Phase 2 artifact is missing or aggregate validation fails. |

## 9. Codex/AgentJob Task Packets

### AJ-20: Walking Skeleton Flow

Objective: implement a deterministic walking-skeleton flow validator connecting RDR, PRD, implementation plan, AgentJobs, and package outputs.

Primary writes:

- `Sys4AI/sys_for_ai/walking_skeleton.py`
- `Sys4AI/sys_for_ai/trace_flow.py`
- `Sys4AI/sys_for_ai/cli.py`
- `Sys4AI/Makefile`
- `Sys4AI/tests/test_walking_skeleton.py`
- `Sys4AI/docs/generated/governance/walking-skeleton-flow.md`

### AJ-21: Target Package Smoke

Objective: add a sample target-system package smoke surface and validator.

Primary writes:

- `Sys4AI/sys_for_ai/target_package.py`
- `Sys4AI/sys_for_ai/cli.py`
- `Sys4AI/Makefile`
- `Sys4AI/tests/test_target_package.py`
- `Sys4AI/examples/target_systems/repo_steward_agent_package/**`

### AJ-22: Walking Skeleton Demo

Objective: run the Phase 2 walking skeleton demonstration and produce acceptance evidence.

Primary writes:

- `implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md`
- `Sys4AI/control_records/completions/RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml`
- `Sys4AI/control_records/handoffs/HANDOFF-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml`

## 10. Validation Plan

Each packet must run its targeted validators and then aggregate validation.

AJ-20 validators:

- `cd Sys4AI && make doctor`
- `cd Sys4AI && .venv/bin/python -m unittest discover -s tests`
- `cd Sys4AI && make validate-walking-skeleton`
- `cd Sys4AI && make validate`

AJ-21 validators:

- `cd Sys4AI && make validate-target-package-smoke`
- `cd Sys4AI && .venv/bin/python -m unittest discover -s tests`
- `cd Sys4AI && make validate`

AJ-22 validators:

- `cd Sys4AI && make validate-walking-skeleton`
- `cd Sys4AI && make validate-target-package-smoke`
- `cd Sys4AI && make validate-requirement-trace`
- `cd Sys4AI && make validate-generated-derivatives`
- `cd Sys4AI && make validate`
- `make validate`

## 11. Security, Privacy, And Reliability Notes

- All validators must run offline.
- No external service calls are required or permitted.
- No secret material should be introduced into templates, examples, manifests, or receipts.
- Sample package artifacts must be marked as smoke evidence or derivative draft evidence.
- Validation must distinguish structural proof from semantic proof.
- The sample target package must not claim production readiness, autonomous operation readiness, or real-domain correctness.

## 12. Rollout And Rollback Plan

Rollout is one `/continue` packet at a time:

1. Complete AJ-20 and stop.
2. Complete AJ-21 and stop.
3. Complete AJ-22 and stop.

Rollback is source-control based. If a packet fails validation before commit, revert only that packet's new changes. If a committed packet is later found invalid, create a new Director Decision and superseding AgentJob rather than mutating completed control records in place.

## 13. Out Of Scope

- Production runtime orchestration.
- Hosted services.
- Vector database memory.
- Domain-specific semantic acceptance.
- Autonomous target-system execution.
- Promoting generated derivatives to canonical authority.
- Implementing PRD decomposition before Phase 2 walking-skeleton acceptance.

## 14. Final Review Checklist

- [x] Source PRD is named.
- [x] Product summary is stated.
- [x] Repository context is grounded in current files.
- [x] Assumptions are explicit.
- [x] Open questions are resolved or routed.
- [x] Every Phase 2 PRD requirement maps to a task, validator, or deferral.
- [x] Technical approach is deterministic and offline.
- [x] Implementation phases are bounded.
- [x] AgentJob packets are created.
- [x] Validation plan names executable commands or future commands created by the relevant AgentJob.
- [x] Security, privacy, and reliability limits are stated.
- [x] Rollout and rollback are controlled.
- [x] Out-of-scope claims are explicit.

## References

AngryOwlAI. (2026a). *Sys4AI Phase 2 Walking Skeleton PRD* [Repository document]. `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`.

AngryOwlAI. (2026b). *Phase 2 walking skeleton Requirements Discovery Record* [Repository control record]. `Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md`.

AngryOwlAI. (2026c). *Sys4AI-dev next-scope full implementation plan* [Repository implementation plan]. `implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md`.

AngryOwlAI. (2026d). *Self-hosting boundary decision record* [Repository decision record]. `implementation_plans/self_hosting_boundary_decision_record.md`.
