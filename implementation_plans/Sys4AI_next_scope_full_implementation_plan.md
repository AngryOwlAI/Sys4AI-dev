# Sys4AI-dev Next Scope Full Implementation Plan

**Plan ID:** `SFADEV-IMPL-PLAN-NEXT-SCOPE-001`  
**Status:** Draft for maintainer review  
**Prepared date:** 2026-07-08  
**Prepared for repository:** `AngryOwlAI/Sys4AI-dev`  
**Primary development system:** `Sys4AI-dev`  
**Framework product under development:** `Sys4AI`  
**Subject layer:** `development_system` for this plan, with explicit work packets that may affect `framework_product` sources  
**Recommended branch name:** `sfadev/next-scope-phase2-and-prd-decomposition`  
**Recommended first Director Decision:** `DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001`

---

## 0. Executive Summary

This implementation plan converts the recommendations from the latest system review into a concrete, auditable, AgentJob-based roadmap.

The current repository state says the previous all-recommendations Phase 1 implementation sequence is complete. The file named `implementation_plans/Sys4AI_PRD_decomposition_full_implementation_plan.md` is not an active PRD-decomposition plan. It is a compatibility pointer to the canonical all-recommendations plan. The canonical plan has acceptance evidence and a plan-completion audit. Therefore this new plan must not reopen or continue that completed plan.

The next work should start from a new Director Decision that selects a new scope. This plan implements all recommended next actions:

1. Preserve closure of the completed all-recommendations implementation plan.
2. Create a new scope-selection control packet.
3. Reconcile legacy pending AgentJob rows so future `/continue` runs do not select obsolete work.
4. Start a Phase 2 walking skeleton that proves `Sys4AI` can actually move a target-system idea through `/init`, discovery, RDR, PRD, implementation plan, AgentJobs, validation evidence, and a package/export surface.
5. Add a PRD decomposition strategy and then create sub-PRDs after the walking skeleton reveals the natural capability boundaries.
6. Promote or route decomposed PRDs through source-authority controls rather than treating generated sub-PRDs as canonical by default.
7. Add final acceptance evidence that proves the next-scope work is closed, traceable, and safe to build on.

This plan is intentionally ordered. Housekeeping comes before Phase 2 so stale pending rows do not become ghost steering wheels. The walking skeleton comes before PRD decomposition so the sub-PRDs are based on observed product motion, not only document taxonomy. PRD decomposition then turns the currently large canonical PRDs into a modular requirements corpus without breaking authority.

---

## 1. Source Evidence and Planning Basis

This plan is based on the following repository evidence.

| Evidence | Relevant fact used by this plan |
|---|---|
| `README.md` | The repo is the development workspace for `Sys4AI`; the product being developed lives under `Sys4AI/`; canonical current PRD sources are listed under `PRDs/`; validation is exposed through root `make validate` and product `make validate`. |
| `PRDs/Sys4AI_phase-0_product_system_design_prd.md` | Phase 0 defines product identity, lifecycle, role/artifact model, AgentJob semantics, `/continue`, source-first memory, system-layer classification, discovery gate, `/init`, skill lifecycle, and acceptance criteria. |
| `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md` | Phase 1 initializes a scaffold, validators, registries, discovery gate, role governance, skill lifecycle, `/init`, and validation commands; it does not finish the framework. |
| `PRDs/Sys4AI_phase-0_prd.md` | Superseded historical Phase 0 reference only. It must not regain authority unless a later source-authority decision promotes content. |
| `implementation_plans/Sys4AI_PRD_decomposition_full_implementation_plan.md` | Compatibility pointer. It names the canonical current plan and requires `/continue` execution with one AgentJob at a time. |
| `implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md` | Canonical prior all-recommendations plan, now completed for its current Phase 1 scope. |
| `implementation_plans/completion_receipts/CR-SFADEV-ALL-RECS-IMPLEMENTED-001.md` | Acceptance receipt for the prior all-recommendations plan. It records passing root and product validation and lists deferred later-lifecycle items. |
| `implementation_plans/completion_audits/PLAN-COMPLETION-AUDIT-SFADEV-14.md` | Confirms there is no remaining Phase 1 all-recommendations AgentJob in the current plan sequence. |
| `Sys4AI/control_records/program_state.yaml` | Current state is complete; latest task is the plan-completion audit; no active AgentJob is selected. |
| `Sys4AI/control_records/handoffs/HANDOFF-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml` | Handoff says future work should begin only from a new scope and new Director Decision. |
| `Sys4AI/registries/agentjob_registry.csv` | Contains completed all-recommendations AgentJobs and also legacy pending self-hosting rows that should be reconciled before future continuation work. |
| `.agents/skills/init/SKILL.md` | `/init` is the reversible gated front door for classification, evidence inspection, and approval before controlled artifact creation. |
| `.agents/skills/conversation-to-prd/SKILL.md` | PRD generation is available as a runtime skill, but generated PRDs remain derivative until accepted. |
| `.agents/skills/prd-to-implementation-plan/SKILL.md` | PRDs can be converted into implementation plans and task packets, with traceability and validation requirements. |
| `implementation_plans/self_hosting_boundary_decision_record.md` | `Sys4AI-dev` may self-host `Sys4AI` concepts only if authority boundaries remain explicit. |

---

## 2. Problem Statement

The repository has reached a productive but delicate point.

The project is developing `Sys4AI`, a system for developing and managing agentic systems. The development repository `Sys4AI-dev` is itself a system and is already dogfooding `Sys4AI` concepts such as AgentJobs, `/continue`, source-first memory, registries, validation contracts, skills, handoffs, completion receipts, and derivative docs.

This self-hosting loop is acceptable only if each artifact clearly declares what it governs. Without a new controlled next-scope plan, future work can easily confuse:

- The completed prior all-recommendations implementation plan.
- The compatibility pointer named as a PRD decomposition plan.
- The canonical Phase 0 and Phase 1 PRDs.
- Future sub-PRDs that do not yet exist.
- Active runtime skills under `.agents/`.
- Product-scaffold skills under `Sys4AI/skills/core/`.
- Legacy pending AgentJob registry rows.
- Future target-system instances generated by `Sys4AI`.

The immediate need is not more unbounded implementation. The immediate need is a new controlled scope packet that converts confusion into typed, validated work.

---

## 3. Goals

### 3.1 Primary Goals

1. Establish a new Director-selected scope for post-Phase-1 work.
2. Preserve the completed status of the prior all-recommendations implementation plan.
3. Prevent `/continue` from accidentally selecting obsolete legacy pending AgentJobs.
4. Build a Phase 2 walking skeleton that demonstrates end-to-end `Sys4AI` behavior.
5. Create a governed PRD decomposition strategy.
6. Produce sub-PRD drafts based on observed walking-skeleton boundaries.
7. Promote, supersede, or route sub-PRDs through a source-authority workflow.
8. Update requirement trace and registry surfaces so the new plan is auditable.
9. Provide acceptance evidence showing that the new scope is complete or intentionally deferred.

### 3.2 Secondary Goals

1. Reduce conceptual recursion by using system-layer declarations consistently.
2. Clarify which artifacts are canonical, controlled, derivative drafts, generated derivatives, scaffold references, superseded, or historical.
3. Strengthen traceability from `RDR -> PRD -> implementation plan -> AgentJobs -> validation evidence -> target-system package`.
4. Prepare the repo for later lifecycle phases: operation, improvement, maintenance, runtime execution, packaging, and target-system generation.
5. Improve maintainer usability by creating a clear next-step runway.

---

## 4. Non-Goals

This plan does not attempt to:

1. Reopen the completed all-recommendations implementation plan.
2. Treat `implementation_plans/Sys4AI_PRD_decomposition_full_implementation_plan.md` as a second canonical plan.
3. Convert generated sub-PRDs into canonical requirements without approval.
4. Build a production runtime service.
5. Add a vector database or production memory database.
6. Build a full hosted web UI.
7. Implement arbitrary domain-specific agent systems.
8. Make future target-system semantic correctness claims based only on structural validators.
9. Replace the canonical Phase 0 and Phase 1 PRDs in one uncontrolled edit.
10. Remove historical PRD references unless a source-authority decision explicitly does so.
11. Force Docker unless existing Docker trigger conditions are met.
12. Modify local `.venv`, caches, private receipts, or non-source-controlled local runtime state.

---

## 5. Authority Model

### 5.1 System Layers

All work in this plan must declare one of the following subject layers.

| Layer | Meaning | Example roots | Authority rule |
|---|---|---|---|
| `development_system` | The `Sys4AI-dev` workspace and active runtime used to develop `Sys4AI`. | repo root, `.agents/`, `.codex/`, root `Makefile`, root scripts | Active development authority for this repo. |
| `framework_product` | The `Sys4AI` framework product under development. | `Sys4AI/`, `PRDs/`, `implementation_plans/` | Product requirements, scaffold, validators, registries, and reference implementation. |
| `target_system_template` | Reusable generated scaffolds or templates emitted by `Sys4AI`. | future `Sys4AI/templates/target_systems/`, generated examples | Template authority only when declared and validated. |
| `target_system_instance` | A concrete future system created or managed using `Sys4AI`. | sample generated package, future external repo | Instance authority must not mutate core framework authority without escalation. |
| `derivative_surface` | Generated docs, catalogs, local vaults, summaries, diagrams, caches. | `Sys4AI/docs/generated/`, optional exports | Noncanonical by default. Must trace to canonical or controlled sources. |

### 5.2 Source Authority Statuses

Every new artifact introduced by this plan should use one of these statuses.

| Status | Meaning |
|---|---|
| `canonical` | Authoritative source for its declared scope. Requires explicit promotion or existing authority. |
| `controlled` | Governed source/control artifact with validation and registry trace. |
| `derivative_draft` | Draft generated from source evidence, not yet accepted as authority. |
| `generated_derivative` | Generated reader surface, catalog, index, or report. Never canonical by default. |
| `scaffold_reference` | Product scaffold or reusable template reference, not active runtime authority unless promoted. |
| `superseded` | Replaced by a later artifact. Retained for traceability. |
| `historical_reference` | Retained as background only. Not binding when it conflicts with canonical sources. |

### 5.3 Non-Negotiable Authority Rule

Generated derivatives and draft sub-PRDs must not authorize changes to PRDs, registries, control records, role catalogs, skill manifests, validation contracts, validators, or source files unless a source-authority workflow promotes them.

---

## 6. Execution Protocol

### 6.1 Required Use of `/continue`

Every implementation workstream in this plan should be executed through the active `/continue` mechanism.

Required sequence for each workstream:

1. Confirm the repo is clean or intentionally checkpointed.
2. Confirm local branch and upstream sync state.
3. Run memory preflight.
4. Inspect `Sys4AI/control_records/program_state.yaml`.
5. Inspect the latest controlled handoff.
6. Select or create at most one authorized AgentJob.
7. Execute only that AgentJob.
8. Write or update the required completion receipt.
9. Write or update the required controlled handoff.
10. Write `temp_handoff/handoff-XXXX.md` where the repo convention requires it.
11. Update registries for new or changed control records.
12. Run validators named by the AgentJob.
13. Run aggregate validation when the workstream touches cross-cutting authority surfaces.
14. Commit the bounded task.
15. Push the commit or stop and report push evidence is missing.
16. Do not start the next AgentJob while the branch is ahead of upstream without push evidence.

### 6.2 Standard Closeout Report

Each implementation AgentJob should close with a chat-visible report containing:

- Selected AgentJob ID.
- Director Decision ID, if applicable.
- Files changed.
- Controlled records created or superseded.
- Registry rows added or modified.
- Validators run and result.
- Commit hash.
- Push status.
- Open risks or unresolved questions.
- Next logical AgentJob, or `none` if complete.

### 6.3 Branch and Commit Policy

Recommended branch strategy:

```text
main
└── sfadev/next-scope-phase2-and-prd-decomposition
```

Recommended commit granularity:

- One commit per AgentJob.
- Commit message format:

```text
control: select next Sys4AI scope
control: reconcile legacy pending AgentJobs
phase2: add walking skeleton discovery packet
phase2: add target-system package smoke path
prd: add decomposition strategy
prd: add modular sub-PRD drafts
acceptance: close next-scope implementation plan
```

---

## 7. Recommended Workstream Order

| Order | Workstream | AgentJob ID | Main purpose |
|---:|---|---|---|
| 1 | WS-15 Scope Selection and Plan Adoption | `AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001` | Create the new Director Decision and adopt this plan as the active next scope. |
| 2 | WS-16 Legacy Pending AgentJob Reconciliation | `AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001` | Classify stale pending rows and prevent accidental selection. |
| 3 | WS-17 Phase 2 Discovery and RDR | `AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001` | Use `/init` and discovery governance to define the walking skeleton. |
| 4 | WS-18 Phase 2 PRD | `AJ-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001` | Generate and accept a Phase 2 walking skeleton PRD. |
| 5 | WS-19 Phase 2 Implementation Plan and AgentJobs | `AJ-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001` | Convert the Phase 2 PRD into an implementation plan and bounded AgentJobs. |
| 6 | WS-20 Walking Skeleton Implementation Slice 1 | `AJ-SFADEV-20-WALKING-SKELETON-FLOW-001` | Implement or wire the end-to-end artifact flow from idea to task packet. |
| 7 | WS-21 Walking Skeleton Implementation Slice 2 | `AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001` | Add a target-system package/export smoke surface. |
| 8 | WS-22 Walking Skeleton Validation and Demonstration | `AJ-SFADEV-22-WALKING-SKELETON-DEMO-001` | Run the demonstration, validate trace, and produce acceptance evidence. |
| 9 | WS-23 PRD Decomposition Strategy | `AJ-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001` | Define decomposition rules and authority model. |
| 10 | WS-24 Sub-PRD Draft Generation | `AJ-SFADEV-24-SUBPRD-DRAFTS-001` | Draft modular sub-PRDs as derivative drafts with trace. |
| 11 | WS-25 Sub-PRD Promotion or Routing | `AJ-SFADEV-25-SUBPRD-PROMOTION-001` | Promote, defer, or keep sub-PRDs as drafts under source-authority control. |
| 12 | WS-26 Final Acceptance and Handoff | `AJ-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001` | Prove this next-scope plan is complete, validated, and safely closed. |

---

# Part A: Scope Control and Repository Hygiene

---

## 8. WS-15: Scope Selection and Plan Adoption

### 8.1 Purpose

Create a new Director Decision that explicitly selects this next-scope plan. This prevents the completed prior plan from being treated as still active and gives future `/continue` runs a fresh, typed authority packet.

### 8.2 Subject Layer

`development_system`, with controlled effects on `framework_product` planning artifacts.

### 8.3 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001
objective: Select the next controlled scope after completion of the all-recommendations Phase 1 plan.
role: system_director
subject_system_id: Sys4AI-dev
subject_layer: development_system
authority_scope: next_scope_selection
allowed_reads:
  - README.md
  - PRDs/**
  - implementation_plans/**
  - Sys4AI/control_records/program_state.yaml
  - Sys4AI/control_records/handoffs/**
  - Sys4AI/registries/agentjob_registry.csv
allowed_writes:
  - implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md
  - Sys4AI/control_records/director_decisions/DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
  - Sys4AI/control_records/memory_preflights/MEMPREFLIGHT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
  - Sys4AI/registries/agentjob_registry.csv
  - Sys4AI/registries/director_decision_registry.csv
  - Sys4AI/registries/completion_receipt_registry.csv
  - Sys4AI/registries/handoff_registry.csv
  - Sys4AI/registries/memory_preflight_receipt_registry.csv
  - Sys4AI/registries/control_record_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/control_records/program_state.yaml
forbidden_actions:
  - Reopen the completed all-recommendations implementation plan.
  - Treat compatibility pointer files as active plan authority.
  - Create sub-PRDs before scope selection is recorded.
  - Start more than one AgentJob.
required_inputs:
  - Latest plan-completion audit.
  - Latest program state.
  - Maintainer intent to implement all next-step recommendations.
expected_outputs:
  - Director Decision selecting this plan.
  - Updated program state with active task scope.
  - Completion receipt and handoff.
validators:
  - cd Sys4AI && make validate-program-state
  - cd Sys4AI && make validate-director-decision-registry
  - cd Sys4AI && make validate-agentjob-registry
  - cd Sys4AI && make validate-control-records
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && make validate-control-loop
completion_evidence:
  - Director Decision path
  - Plan path
  - Registry rows
  - Validation transcript
stop_conditions:
  - Latest program state is not complete.
  - Another AgentJob is active.
  - Branch is ahead of upstream without push evidence.
```

### 8.4 Files to Add

```text
implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md
Sys4AI/control_records/director_decisions/DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
Sys4AI/control_records/memory_preflights/MEMPREFLIGHT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
Sys4AI/control_records/completions/RECEIPT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
Sys4AI/control_records/handoffs/HANDOFF-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
temp_handoff/handoff-0025.md
```

### 8.5 Files to Modify

```text
Sys4AI/control_records/program_state.yaml
Sys4AI/registries/agentjob_registry.csv
Sys4AI/registries/director_decision_registry.csv
Sys4AI/registries/completion_receipt_registry.csv
Sys4AI/registries/handoff_registry.csv
Sys4AI/registries/memory_preflight_receipt_registry.csv
Sys4AI/registries/control_record_registry.csv
Sys4AI/registries/source_registry.csv
Sys4AI/docs/generated/configuration_control/index.md
Sys4AI/docs/generated/configuration_control/yaml-control-records.md
Sys4AI/docs/generated/registry_catalog/index.md
```

### 8.6 Director Decision Contents

The decision should explicitly state:

1. The prior all-recommendations plan is closed.
2. The compatibility pointer remains only a pointer.
3. The next selected scope is this plan.
4. The next work order is:
   1. legacy pending row reconciliation;
   2. Phase 2 walking skeleton;
   3. PRD decomposition;
   4. final acceptance.
5. Generated sub-PRDs are derivative drafts until promoted.
6. Walking skeleton evidence should inform sub-PRD boundaries.
7. `/continue` must execute one AgentJob at a time.

### 8.7 Acceptance Criteria

- New Director Decision exists and validates.
- This plan is registered as controlled implementation-plan source evidence.
- Program state points to the new selected scope or records the completed selection task.
- Control record registries contain rows for all new control records.
- No prior completed AgentJob is reopened.
- Aggregate validation passes or documented nonblocking warnings are accepted.

---

## 9. WS-16: Legacy Pending AgentJob Reconciliation

### 9.1 Purpose

The agentjob registry contains legacy pending self-hosting rows. They are not remaining tasks for the completed prior all-recommendations plan, but they can confuse future `/continue` selection. This workstream reconciles them.

### 9.2 Target Rows

Initial rows to inspect:

```text
AJ-P1-SELFHOST-CONTINUE-KERNEL-001
AJ-P1-BOUNDARY-VALIDATORS-001
AJ-P1-DERIVATIVE-GENERATORS-001
AJ-P1-CONTINUE-SKILLS-001
```

Potential related row:

```text
AJ-P1-DISCOVERY-GATE-SMOKE-001
```

The smoke row appears superseded, but it should still be reviewed for consistency.

### 9.3 Reconciliation Classes

Each pending row must be classified into exactly one category.

| Class | Meaning | Registry action |
|---|---|---|
| `superseded_by_completed_work` | The work was completed under a later AgentJob. | Set status to `superseded`; fill `supersedes` or notes with replacement evidence. |
| `still_valid_future_work` | The work is not done but remains valuable. | Keep pending only if a new Director Decision explicitly authorizes it. |
| `duplicate_pending_row` | Another pending or completed row covers the same work. | Set status to `superseded` or `blocked` with explanation. |
| `blocked_pending_row` | Work cannot proceed without missing authority or design. | Set status to `blocked`; add blocker notes. |
| `defer_to_phase2_or_later` | Work belongs to Phase 2 or later but should not be selectable now. | Set status to `deferred`; add future-scope link. |
| `retain_for_historical_trace` | Historical only. | Set status to `historical_reference` if validator allows, otherwise `superseded` with note. |

### 9.4 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001
objective: Reconcile legacy pending AgentJob rows so future continuation selection is not ambiguous.
role: requirements_verifier
subject_system_id: Sys4AI-dev
subject_layer: development_system
authority_scope: agentjob_registry_hygiene
allowed_reads:
  - Sys4AI/registries/agentjob_registry.csv
  - Sys4AI/control_records/agentjobs/**
  - Sys4AI/control_records/completions/**
  - Sys4AI/control_records/handoffs/**
  - implementation_plans/completion_audits/**
  - implementation_plans/completion_receipts/**
allowed_writes:
  - implementation_plans/reconciliation_reports/LEGACY-PENDING-AGENTJOB-RECONCILIATION-SFADEV-16.md
  - Sys4AI/registries/agentjob_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/control_record_registry.csv
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml
forbidden_actions:
  - Delete historical AgentJob records.
  - Rewrite completed AgentJob files without supersession.
  - Select a legacy pending AgentJob for execution during this reconciliation.
  - Change product requirements.
expected_outputs:
  - Reconciliation report.
  - Updated agentjob registry statuses.
  - Completion receipt and handoff.
validators:
  - cd Sys4AI && make validate-agentjob-registry
  - cd Sys4AI && make validate-one-active-agentjob
  - cd Sys4AI && make validate-control-loop
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && make validate-control-records
completion_evidence:
  - Reconciliation table with one verdict per legacy row.
  - Registry diff.
  - Validation output.
stop_conditions:
  - Any pending row maps to active work not covered by a new Director Decision.
  - Validator rejects the chosen reconciliation status vocabulary.
```

### 9.5 Report Template

Create:

```text
implementation_plans/reconciliation_reports/LEGACY-PENDING-AGENTJOB-RECONCILIATION-SFADEV-16.md
```

Template:

```md
# Legacy Pending AgentJob Reconciliation

Reconciliation ID: LEGACY-PENDING-AGENTJOB-RECONCILIATION-SFADEV-16
Date: 2026-07-08
AgentJob: AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001
Result: PASS | WARN | FAIL

## Scope

Rows inspected:

| AgentJob ID | Prior status | Evidence inspected | Verdict | Registry action | Rationale |
|---|---|---|---|---|---|
| AJ-P1-SELFHOST-CONTINUE-KERNEL-001 | pending | ... | ... | ... | ... |

## Replacement Evidence

| Legacy row | Replacement or blocker evidence |
|---|---|

## Future Scope Recommendations

| Candidate future work | Required Director Decision | Phase |
|---|---|---|

## Validation

| Command | Result |
|---|---|
```

### 9.6 Acceptance Criteria

- Every legacy pending row has an explicit reconciliation verdict.
- No obsolete pending row remains accidentally selectable by `/continue`.
- Any genuinely valid future row is linked to a required new Director Decision.
- AgentJob registry validates.
- Control loop validation passes.
- Reconciliation report is registered as controlled evidence.

---

# Part B: Phase 2 Walking Skeleton

---

## 10. Phase 2 Product Thesis

Phase 1 created the governed skeleton: registries, validators, runtime skills, product scaffold, discovery gate, `/init`, source-first memory rules, role governance, and validation surfaces.

Phase 2 should prove that the skeleton can walk.

The Phase 2 walking skeleton is not a full production runtime. It is a traceable demonstration that `Sys4AI` can transform a new target-system idea into controlled downstream implementation artifacts.

### 10.1 Walking Skeleton Flow

```text
User target-system intent
  -> /init classification
  -> System Definition Discovery Gate
  -> Requirements Discovery Record
  -> PRD synthesis
  -> Implementation plan synthesis
  -> AgentJob/task packet generation
  -> Trace validation
  -> Target-system package/export smoke artifact
  -> Acceptance receipt
```

### 10.2 Required Demonstration Target

Use a deliberately small, domain-neutral target-system example.

Recommended sample:

```text
Target system: Repo Steward Agent
Purpose: A governed assistant that inspects a software repository, summarizes current state, identifies safe next actions, and produces a bounded implementation plan without modifying files during first-pass inspection.
Subject layer: target_system_instance for the sample output, with source templates under target_system_template.
```

Why this sample is useful:

- It resembles `Sys4AI-dev`, so evidence is available.
- It exercises brownfield first-pass rules.
- It uses `/init`, discovery, PRD generation, implementation planning, AgentJobs, and validators.
- It avoids domain-specific scientific, financial, medical, or regulated requirements.
- It demonstrates the framework without requiring a production service.

### 10.3 Minimum Phase 2 Success Claim

A successful Phase 2 walking skeleton may claim:

```text
Sys4AI can produce a governed, traceable, validated target-system planning package for a small sample agentic system.
```

It must not claim:

```text
Sys4AI can operate a production autonomous agent runtime.
Sys4AI can guarantee semantic correctness of arbitrary target systems.
Sys4AI can replace human approval for high-impact systems.
```

---

## 11. WS-17: Phase 2 Discovery and RDR

### 11.1 Purpose

Use the newly implemented `/init` and discovery gate to define the Phase 2 walking skeleton as an explicit system-development initiative. This creates a Requirements Discovery Record before generating any new Phase 2 PRD.

### 11.2 Proposed Output Paths

```text
Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md
Sys4AI/control_records/agentjobs/AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
Sys4AI/control_records/completions/RECEIPT-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
Sys4AI/control_records/handoffs/HANDOFF-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
```

### 11.3 RDR Required Sections

The RDR must include:

1. Header with subject system ID, subject layer, discovery gate, producer AgentJob, registry row, downstream artifact status.
2. Authority notice saying the RDR is controlled discovery evidence, not a baselined PRD.
3. System layer classification.
4. Mission need.
5. Problem statement.
6. Desired outcome.
7. Value case.
8. System-of-interest.
9. Stakeholders.
10. Boundaries.
11. As-is state.
12. To-be state.
13. Operational scenarios.
14. Candidate functional requirements.
15. Candidate non-functional requirements.
16. Quality attributes.
17. Architecture drivers.
18. Interface candidates.
19. V&V seeds.
20. Evidence register.
21. Assumptions.
22. Risks.
23. Constraints.
24. Open questions.
25. Downstream routing recommendation.
26. Discovery gate exit checklist.

### 11.4 Candidate Requirements

Candidate requirement examples for the RDR:

```text
REQ-CAND-P2-001: The walking skeleton shall classify a target-system request through /init before producing downstream artifacts.
REQ-CAND-P2-002: The walking skeleton shall produce a Requirements Discovery Record before producing a PRD.
REQ-CAND-P2-003: The walking skeleton shall produce a PRD that traces to the RDR.
REQ-CAND-P2-004: The walking skeleton shall produce an implementation plan that traces to the PRD.
REQ-CAND-P2-005: The walking skeleton shall produce at least three bounded AgentJob or task-packet artifacts from the implementation plan.
REQ-CAND-P2-006: The walking skeleton shall produce a target-system package or export smoke artifact.
REQ-CAND-P2-007: The walking skeleton shall run structural validators and report their results.
NFR-CAND-P2-001: The walking skeleton shall keep generated artifacts derivative until accepted.
NFR-CAND-P2-002: The walking skeleton shall preserve subject-layer declarations across generated artifacts.
NFR-CAND-P2-003: The walking skeleton shall avoid production runtime claims.
```

### 11.5 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001
objective: Run the discovery gate for the Phase 2 walking skeleton initiative and create a Requirements Discovery Record.
role: user_wants_elicitor
subject_system_id: Sys4AI-dev
subject_layer: development_system
authority_scope: phase2_discovery
allowed_reads:
  - README.md
  - PRDs/**
  - implementation_plans/**
  - Sys4AI/templates/system_definition/**
  - .agents/skills/init/**
  - .agents/skills/system-definition-interview-context-45/**
  - Sys4AI/control_records/program_state.yaml
  - Sys4AI/control_records/handoffs/**
allowed_writes:
  - Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md
  - Sys4AI/registries/discovery_record_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/control_record_registry.csv
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
forbidden_actions:
  - Generate a PRD before the RDR exists and validates.
  - Promote candidate requirements to baselined requirements.
  - Generate target-system code.
validators:
  - cd Sys4AI && make validate-discovery-records
  - cd Sys4AI && make validate-control-records
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && make validate-requirement-trace
completion_evidence:
  - RDR path
  - Discovery registry row
  - Validation output
stop_conditions:
  - Subject layer cannot be classified.
  - RDR would rely on generated derivative evidence without source trace.
```

### 11.6 Acceptance Criteria

- RDR exists and validates.
- RDR preserves candidate requirement labels.
- RDR records evidence from current repo sources.
- RDR recommends PRD generation only after discovery exit criteria are met.
- Discovery registry row exists and validates.
- No PRD is created during this AgentJob unless the AgentJob is explicitly expanded and approved, which is not recommended.

---

## 12. WS-18: Phase 2 Walking Skeleton PRD

### 12.1 Purpose

Generate and accept a Phase 2 PRD from the walking skeleton RDR. This PRD becomes the canonical product requirement source for the Phase 2 walking skeleton only after source-authority acceptance.

### 12.2 Proposed Output Path

```text
PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
```

Alternative draft path before acceptance:

```text
PRDs/drafts/Sys4AI_phase-2_walking_skeleton_prd.draft.md
```

Recommended approach:

1. Generate as draft.
2. Validate trace to RDR.
3. Review authority status.
4. Promote to canonical Phase 2 PRD through a Director Decision or completion receipt.

### 12.3 PRD Required Sections

The Phase 2 PRD should include:

1. Document status.
2. Product name.
3. Phase.
4. Depends on Phase 0, Phase 1, and Phase 2 RDR.
5. Last updated.
6. Executive summary.
7. Phase boundary.
8. User and stakeholder model.
9. Walking skeleton system-of-interest.
10. Functional requirements.
11. Non-functional requirements.
12. Artifact flow requirements.
13. Traceability requirements.
14. Validation requirements.
15. Target-system package/export requirements.
16. Non-goals.
17. Risks and mitigations.
18. Acceptance criteria.
19. Deferred items.
20. Open questions.

### 12.4 Requirement ID Scheme

Use stable IDs:

```text
SFA-P2-WS-FLOW-001
SFA-P2-WS-FLOW-002
SFA-P2-WS-RDR-001
SFA-P2-WS-PRD-001
SFA-P2-WS-PLAN-001
SFA-P2-WS-AJ-001
SFA-P2-WS-PACKAGE-001
SFA-P2-WS-TRACE-001
SFA-P2-WS-VAL-001
SFA-P2-WS-NFR-001
```

### 12.5 Core Requirements to Include

```text
SFA-P2-WS-FLOW-001: Sys4AI shall provide a walking skeleton flow from user target-system intent through /init, RDR, PRD, implementation plan, AgentJobs, validation evidence, and target-system package/export smoke output.

SFA-P2-WS-RDR-001: The walking skeleton shall consume a validated Requirements Discovery Record before PRD synthesis.

SFA-P2-WS-PRD-001: The walking skeleton shall produce a Phase 2 PRD that traces each baselined requirement to the Phase 2 RDR or an approved Director Decision.

SFA-P2-WS-PLAN-001: The walking skeleton shall produce an implementation plan from the Phase 2 PRD using the active `prd-to-implementation-plan` skill or equivalent governed procedure.

SFA-P2-WS-AJ-001: The walking skeleton shall produce at least three bounded AgentJob or task-packet artifacts from the implementation plan.

SFA-P2-WS-PACKAGE-001: The walking skeleton shall produce a sample target-system package/export surface containing a README, manifest, requirements trace, and task packet index.

SFA-P2-WS-TRACE-001: The walking skeleton shall preserve trace from RDR candidate requirements through PRD requirements, implementation plan tasks, AgentJobs, validation evidence, and package outputs.

SFA-P2-WS-VAL-001: The walking skeleton shall run structural validators and report which claims are proven by validation and which claims remain semantic or human-review obligations.

SFA-P2-WS-NFR-001: Generated artifacts shall remain derivative until accepted through source-authority workflow.

SFA-P2-WS-NFR-002: The walking skeleton shall not claim production runtime readiness, autonomous operation readiness, or domain semantic correctness.
```

### 12.6 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001
objective: Generate, validate, and promote a Phase 2 walking skeleton PRD from the approved RDR.
role: requirements_manager
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: phase2_prd_generation
allowed_reads:
  - PRDs/Sys4AI_phase-0_product_system_design_prd.md
  - PRDs/Sys4AI_phase-1_implementation_initialization_prd.md
  - Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md
  - .agents/skills/conversation-to-prd/**
allowed_writes:
  - PRDs/drafts/Sys4AI_phase-2_walking_skeleton_prd.draft.md
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - Sys4AI/registries/requirement_trace_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml
forbidden_actions:
  - Baseline PRD requirements without RDR trace or Director Decision trace.
  - Remove or supersede Phase 0 or Phase 1 PRDs.
  - Create implementation code.
validators:
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-registry-graph
  - make validate
completion_evidence:
  - Draft PRD path
  - Accepted PRD path or promotion decision
  - Trace registry rows
  - Validation output
stop_conditions:
  - RDR is missing or invalid.
  - Requirement trace cannot be established.
```

### 12.7 Acceptance Criteria

- Phase 2 PRD exists and is clearly marked as draft or canonical.
- Every Phase 2 PRD requirement traces to RDR evidence or Director Decision evidence.
- No Phase 0 or Phase 1 authority is silently replaced.
- Requirement trace validator passes.
- Source registry includes the new PRD.

---

## 13. WS-19: Phase 2 Implementation Plan and AgentJobs

### 13.1 Purpose

Convert the Phase 2 walking skeleton PRD into a concrete implementation plan and bounded AgentJobs.

### 13.2 Proposed Output Paths

```text
implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md
Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml
```

### 13.3 Implementation Plan Required Sections

1. Source PRD.
2. Product summary.
3. Repository context.
4. Assumptions.
5. Open questions.
6. Requirement traceability matrix.
7. Proposed technical approach.
8. Implementation phases.
9. Codex/AgentJob task packets.
10. Validation plan.
11. Security, privacy, and reliability notes.
12. Rollout and rollback plan.
13. Out of scope.
14. Final review checklist.

### 13.4 Proposed Technical Architecture

Add a small orchestration module or CLI surface only if consistent with current code structure. Recommended minimal implementation surfaces:

```text
Sys4AI/sys_for_ai/walking_skeleton.py
Sys4AI/sys_for_ai/target_package.py
Sys4AI/sys_for_ai/trace_flow.py
Sys4AI/templates/target_systems/repo_steward_agent/README.template.md
Sys4AI/templates/target_systems/repo_steward_agent/target-system-manifest.template.yaml
Sys4AI/templates/target_systems/repo_steward_agent/task-packet-index.template.md
Sys4AI/templates/target_systems/repo_steward_agent/requirements-trace.template.csv
Sys4AI/examples/target_systems/repo_steward_agent_package/README.md
Sys4AI/examples/target_systems/repo_steward_agent_package/target-system-manifest.yaml
Sys4AI/examples/target_systems/repo_steward_agent_package/task-packet-index.md
Sys4AI/examples/target_systems/repo_steward_agent_package/requirements-trace.csv
```

Potential CLI commands:

```bash
cd Sys4AI
.venv/bin/python -m sys_for_ai.cli walking-skeleton status --json
.venv/bin/python -m sys_for_ai.cli walking-skeleton validate-flow --json
.venv/bin/python -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
```

Potential Makefile targets:

```make
validate-walking-skeleton:
	$(PYTHON) -m sys_for_ai.cli walking-skeleton validate-flow --json

validate-target-package-smoke:
	$(PYTHON) -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
```

Add both to aggregate `validate` only after they are stable and deterministic.

### 13.5 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001
objective: Convert the Phase 2 walking skeleton PRD into a detailed implementation plan and bounded AgentJobs.
role: implementation_initialization_agent
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: phase2_implementation_planning
allowed_reads:
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - .agents/skills/prd-to-implementation-plan/**
  - Sys4AI/Makefile
  - Sys4AI/sys_for_ai/**
  - Sys4AI/templates/**
  - Sys4AI/registries/**
allowed_writes:
  - implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml
  - Sys4AI/registries/agentjob_registry.csv
  - Sys4AI/registries/requirement_trace_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml
forbidden_actions:
  - Implement code during planning.
  - Generate tasks without PRD trace.
  - Create tasks too large for one AgentJob.
validators:
  - cd Sys4AI && make validate-agentjob-registry
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-registry-graph
completion_evidence:
  - Phase 2 implementation plan
  - AgentJob files
  - Trace rows
stop_conditions:
  - Phase 2 PRD is absent or draft-only without approval to plan from draft.
  - Requirements cannot be mapped to bounded tasks.
```

### 13.6 Acceptance Criteria

- Phase 2 implementation plan exists.
- Every Phase 2 PRD requirement is mapped to a task, validation check, or explicit deferral.
- At least three bounded Phase 2 AgentJobs are created.
- AgentJob registry validates.
- Requirement trace validates.

---

## 14. WS-20: Walking Skeleton Flow Implementation

### 14.1 Purpose

Implement the minimal executable or inspectable flow that connects the artifacts from target-system intent to task packets.

This does not require a production orchestrator. It requires a deterministic, offline, validateable path that proves the artifact chain exists and is coherent.

### 14.2 Candidate Implementation Options

| Option | Description | Recommendation |
|---|---|---|
| `docs-only flow` | A generated report shows the flow but no CLI exists. | Too weak for Phase 2. |
| `CLI validation flow` | CLI validates presence, trace, and status of required artifacts. | Recommended. |
| `generator flow` | CLI creates sample artifacts from templates. | Useful, but keep minimal. |
| `runtime orchestration flow` | CLI invokes skills or agents to produce artifacts. | Too heavy for this phase. |

Recommended choice: CLI validation flow plus minimal sample package generation from templates.

### 14.3 Files to Add or Modify

```text
Sys4AI/sys_for_ai/walking_skeleton.py
Sys4AI/sys_for_ai/trace_flow.py
Sys4AI/sys_for_ai/cli.py
Sys4AI/Makefile
Sys4AI/tests/test_walking_skeleton.py
Sys4AI/registries/artifact_contract_registry.csv
Sys4AI/registries/requirement_trace_registry.csv
Sys4AI/registries/source_registry.csv
Sys4AI/docs/generated/governance/walking-skeleton-flow.md
```

### 14.4 Flow Contract

The validator should check that the following artifacts exist and are linked:

```text
RDR path
Phase 2 PRD path
Phase 2 implementation plan path
At least three AgentJob paths
At least one target-system package/export path
At least one validation receipt or demonstration receipt
Trace rows linking all of the above
```

### 14.5 Suggested Data Model

```python
@dataclass(frozen=True)
class WalkingSkeletonArtifact:
    artifact_id: str
    artifact_type: str
    path: str
    subject_layer: str
    authority_status: str
    upstream_ids: tuple[str, ...]
    downstream_ids: tuple[str, ...]
    validation_status: str

@dataclass(frozen=True)
class WalkingSkeletonFlowReport:
    flow_id: str
    result: str
    artifacts: list[WalkingSkeletonArtifact]
    missing_artifacts: list[str]
    trace_gaps: list[str]
    warnings: list[str]
```

### 14.6 CLI Behavior

Command:

```bash
cd Sys4AI
.venv/bin/python -m sys_for_ai.cli walking-skeleton validate-flow --json
```

Expected JSON shape:

```json
{
  "flow_id": "SFA-P2-WALKING-SKELETON-001",
  "result": "pass",
  "artifacts_checked": 8,
  "missing_artifacts": [],
  "trace_gaps": [],
  "warnings": [],
  "validated_at": "2026-07-08T00:00:00Z"
}
```

### 14.7 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-20-WALKING-SKELETON-FLOW-001
objective: Implement a deterministic walking-skeleton flow validator connecting RDR, PRD, implementation plan, AgentJobs, and package outputs.
role: implementation_initialization_agent
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: walking_skeleton_flow_validation
allowed_reads:
  - PRDs/**
  - implementation_plans/**
  - Sys4AI/control_records/**
  - Sys4AI/registries/**
  - Sys4AI/sys_for_ai/**
  - Sys4AI/tests/**
allowed_writes:
  - Sys4AI/sys_for_ai/walking_skeleton.py
  - Sys4AI/sys_for_ai/trace_flow.py
  - Sys4AI/sys_for_ai/cli.py
  - Sys4AI/Makefile
  - Sys4AI/tests/test_walking_skeleton.py
  - Sys4AI/docs/generated/governance/walking-skeleton-flow.md
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/derivative_registry.csv
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml
forbidden_actions:
  - Call external services.
  - Generate production target-system code.
  - Treat validator pass as semantic proof.
validators:
  - cd Sys4AI && make doctor
  - cd Sys4AI && .venv/bin/python -m unittest discover -s tests
  - cd Sys4AI && make validate-walking-skeleton
  - cd Sys4AI && make validate
completion_evidence:
  - CLI command output
  - Unit test output
  - Updated generated derivative report
stop_conditions:
  - CLI cannot be made deterministic offline.
  - Flow requires missing approved artifacts from prior workstreams.
```

### 14.8 Acceptance Criteria

- `walking-skeleton validate-flow` command exists.
- Command runs offline.
- Unit tests cover pass and failure cases.
- Makefile target exists.
- Aggregate validation includes the target after it is stable.
- Generated flow report remains derivative and registered.

---

## 15. WS-21: Target-System Package Smoke Surface

### 15.1 Purpose

Create a sample target-system package/export surface so the walking skeleton does not end at internal planning artifacts. This package is not a production target system. It is a smoke artifact proving that `Sys4AI` can emit a governed package structure for a future target system.

### 15.2 Proposed Package Root

```text
Sys4AI/examples/target_systems/repo_steward_agent_package/
```

### 15.3 Package Contents

```text
Sys4AI/examples/target_systems/repo_steward_agent_package/
├── README.md
├── target-system-manifest.yaml
├── requirements-discovery-record.md
├── product-requirements.md
├── implementation-plan.md
├── task-packets/
│   ├── TASK-001-read-only-repo-inspection.md
│   ├── TASK-002-current-state-baseline.md
│   └── TASK-003-governed-next-action-plan.md
├── registries/
│   ├── requirement-trace.csv
│   └── artifact-index.csv
└── validation/
    └── validation-summary.md
```

### 15.4 Manifest Fields

```yaml
schema_version: "0.1.0"
target_system_id: repo_steward_agent_sample
name: Repo Steward Agent Sample Package
package_status: smoke_example
subject_layer: target_system_instance
source_authority_status: derivative_draft
generated_by: Sys4AI Phase 2 walking skeleton
source_trace:
  - Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md
contents:
  rdr: requirements-discovery-record.md
  prd: product-requirements.md
  implementation_plan: implementation-plan.md
  task_packet_root: task-packets
  requirement_trace: registries/requirement-trace.csv
validation:
  status: not_run | pass | warn | fail
  commands:
    - python -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
authority_notice: >
  This package is a smoke example and derivative draft. It is not a production target system.
```

### 15.5 Target Package Validator

Add module:

```text
Sys4AI/sys_for_ai/target_package.py
```

Validator checks:

1. Package root exists.
2. Manifest exists and parses safely.
3. Manifest has `subject_layer: target_system_instance` or `target_system_template` as appropriate.
4. Manifest does not claim canonical framework authority.
5. Required package files exist.
6. Task packet root exists with at least three task packets.
7. Requirement trace CSV exists and has required headers.
8. Validation summary exists.
9. Source trace points to existing repo sources.
10. No generated example claims production readiness.

### 15.6 CLI Command

```bash
cd Sys4AI
.venv/bin/python -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
```

### 15.7 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001
objective: Add a sample target-system package smoke surface and validator.
role: implementation_initialization_agent
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: target_package_smoke_example
allowed_reads:
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md
  - Sys4AI/templates/**
  - Sys4AI/sys_for_ai/**
  - Sys4AI/tests/**
allowed_writes:
  - Sys4AI/sys_for_ai/target_package.py
  - Sys4AI/sys_for_ai/cli.py
  - Sys4AI/Makefile
  - Sys4AI/tests/test_target_package.py
  - Sys4AI/examples/target_systems/repo_steward_agent_package/**
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/derivative_registry.csv
  - Sys4AI/registries/object_relationship_registry.csv
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml
forbidden_actions:
  - Claim the sample package is production ready.
  - Treat package artifacts as canonical framework requirements.
  - Install runtime dependencies not justified by the Phase 2 PRD.
validators:
  - cd Sys4AI && make validate-target-package-smoke
  - cd Sys4AI && .venv/bin/python -m unittest discover -s tests
  - cd Sys4AI && make validate
completion_evidence:
  - Sample package path
  - Validator output
  - Test output
stop_conditions:
  - Package authority cannot be expressed without confusing framework and target-system layers.
```

### 15.8 Acceptance Criteria

- Sample package exists.
- Package manifest validates.
- Package has RDR, PRD, plan, task packets, trace, and validation summary.
- Package is clearly marked as derivative draft/smoke example.
- Target package validator and tests pass.

---

## 16. WS-22: Walking Skeleton Demonstration and Validation

### 16.1 Purpose

Run the end-to-end demonstration and produce an acceptance packet proving the walking skeleton works within its declared limits.

### 16.2 Demonstration Report

Create:

```text
implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md
```

Required sections:

1. Demo ID.
2. Date.
3. AgentJob.
4. Source PRD.
5. Flow overview.
6. Artifact chain.
7. Trace matrix.
8. Validator commands run.
9. Claims proven.
10. Claims not proven.
11. Open issues.
12. Deferred items.
13. Maintainer acceptance checklist.

### 16.3 Claims Proven vs Not Proven

Proven claims:

- Required artifacts exist.
- Required artifacts parse or validate structurally.
- Required registry rows exist.
- Trace relationships are present.
- Target package smoke example exists and validates.
- Generated derivatives remain noncanonical.

Not proven:

- Semantic correctness of target-system requirements.
- Production runtime readiness.
- Autonomous operation safety.
- Domain-specific validity.
- End-user acceptance for a real target system.

### 16.4 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-22-WALKING-SKELETON-DEMO-001
objective: Run the Phase 2 walking skeleton demonstration and produce acceptance evidence.
role: requirements_verifier
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: phase2_walking_skeleton_acceptance
allowed_reads:
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md
  - Sys4AI/control_records/system_definition/phase2_walking_skeleton_requirements_discovery_record.md
  - Sys4AI/examples/target_systems/repo_steward_agent_package/**
  - Sys4AI/registries/**
  - Sys4AI/docs/generated/**
allowed_writes:
  - implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml
  - Sys4AI/registries/completion_receipt_registry.csv
  - Sys4AI/registries/handoff_registry.csv
  - Sys4AI/registries/source_registry.csv
forbidden_actions:
  - Change requirements while validating acceptance.
  - Convert warnings into pass without evidence.
  - Omit limitations.
validators:
  - cd Sys4AI && make validate-walking-skeleton
  - cd Sys4AI && make validate-target-package-smoke
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-generated-derivatives
  - cd Sys4AI && make validate
  - make validate
completion_evidence:
  - Acceptance report
  - Completion receipt
  - Handoff
  - Validation transcript
stop_conditions:
  - Any required Phase 2 walking skeleton artifact is missing.
  - Aggregate validation fails without an approved exception.
```

### 16.5 Acceptance Criteria

- Demo report exists.
- Walking skeleton validator passes.
- Target package smoke validator passes.
- Aggregate validation passes.
- Report distinguishes structural proof from semantic proof.
- Phase 2 walking skeleton is accepted or clearly marked incomplete with blockers.

---

# Part C: PRD Decomposition

---

## 17. PRD Decomposition Philosophy

The current PRDs are large because they carried the whole product spine during early development. That was useful. It is now time to modularize, but modularization must not shatter authority.

The correct decomposition is not one sub-PRD per existing document. The correct decomposition is one sub-PRD per stable capability authority boundary.

The walking skeleton should happen first because it reveals which boundaries are real in practice. After that, PRD decomposition can follow the product's bone structure rather than its previous document history.

---

## 18. WS-23: PRD Decomposition Strategy

### 18.1 Purpose

Create a governed strategy for decomposing Phase 0, Phase 1, and Phase 2 PRDs into modular sub-PRDs without losing traceability or canonical authority.

### 18.2 Proposed Output Path

```text
PRDs/PRD_decomposition_strategy.md
```

Optional controlled planning path:

```text
implementation_plans/PRD_decomposition_strategy_implementation_plan.md
```

### 18.3 Strategy Required Sections

1. Document status and authority notice.
2. Source PRDs covered.
3. Decomposition goals.
4. Non-goals.
5. Capability boundaries.
6. Requirement ownership rules.
7. Cross-reference rules.
8. Canonical promotion workflow.
9. Supersession workflow.
10. Registry and trace updates.
11. Validator requirements.
12. Generated derivative policy.
13. Proposed sub-PRD index.
14. Migration phases.
15. Acceptance criteria.

### 18.4 Proposed Sub-PRD Set

| Proposed sub-PRD | Scope | Initial authority status |
|---|---|---|
| `PRDs/modules/Sys4AI_init_and_discovery_prd.md` | `/init`, discovery gate, RDR, candidate requirements, discovery-to-PRD routing. | derivative_draft, then controlled/canonical after promotion. |
| `PRDs/modules/Sys4AI_agentjob_and_continue_prd.md` | AgentJob contract, `/continue`, program state, memory preflight, handoffs, completions, one-job invariant. | derivative_draft. |
| `PRDs/modules/Sys4AI_source_first_memory_prd.md` | Canonical sources, registries, derivative surfaces, source authority, stale/orphan behavior. | derivative_draft. |
| `PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md` | System-layer classification, self-hosting, development-system/framework-product boundaries. | derivative_draft. |
| `PRDs/modules/Sys4AI_role_governance_prd.md` | Role registry, role-to-skill crosswalk, execution binding, temporary roles. | derivative_draft. |
| `PRDs/modules/Sys4AI_skill_lifecycle_prd.md` | Runtime skills, product scaffold skills, lifecycle statuses, promotion, deprecation. | derivative_draft. |
| `PRDs/modules/Sys4AI_validation_and_traceability_prd.md` | Validators, requirement trace, registry graph, structural vs semantic validation. | derivative_draft. |
| `PRDs/modules/Sys4AI_target_system_generation_prd.md` | Target-system templates, package/export surfaces, generated target artifacts. | derivative_draft. |
| `PRDs/modules/Sys4AI_operations_improvement_maintenance_prd.md` | Run, improve, maintain, operations, evaluation cadence, incident/issue handling. | derivative_draft. |
| `PRDs/modules/Sys4AI_interface_and_integration_prd.md` | Interfaces, external systems, tool/data boundaries, integration discovery. | derivative_draft. |
| `PRDs/modules/Sys4AI_security_safety_assurance_prd.md` | Threat modeling, permission scope, assurance cases, safety/privacy/compliance hooks. | derivative_draft. |
| `PRDs/modules/Sys4AI_domain_pack_prd.md` | Domain-pack router, project-specific domain expansion, domain-neutral core boundary. | derivative_draft. |

### 18.5 Requirement Ownership Rule

Each requirement ID must have exactly one owning PRD module after promotion.

Allowed references:

- One owner row.
- Many referencing rows.
- Many implementation trace rows.
- Zero or more derivative/generated references.

Disallowed:

- Two canonical sub-PRDs both owning the same requirement ID.
- A generated derivative claiming to own a requirement.
- A superseded historical PRD silently overriding a current module.

### 18.6 Proposed New Registry

Add, if not already present:

```text
Sys4AI/registries/prd_module_registry.csv
```

Suggested headers:

```csv
prd_module_id,path,title,status,subject_layer,authority_scope,owns_requirement_prefixes,references_source_prds,supersedes,source_authority_status,owner_role,validation_status,source_hash,last_validated_at,notes
```

Suggested initial rows:

```csv
PRD-MOD-INIT-DISCOVERY,PRDs/modules/Sys4AI_init_and_discovery_prd.md,Sys4AI Init and Discovery PRD,draft,framework_product,init_discovery,"SFA-CORE-DISCOVERY;SFA-CORE-INIT;SFA-P1-INIT-DISC;SFA-P1-INIT-FRONTDOOR",PRDs/Sys4AI_phase-0_product_system_design_prd.md;PRDs/Sys4AI_phase-1_implementation_initialization_prd.md,,derivative_draft,requirements_manager,not_run,pending,pending,
```

### 18.7 Proposed Validator

Add:

```text
Sys4AI/sys_for_ai/prd_modules.py
```

CLI:

```bash
cd Sys4AI
.venv/bin/python -m sys_for_ai.cli validate-prd-modules registries/prd_module_registry.csv
```

Makefile:

```make
validate-prd-modules:
	$(PYTHON) -m sys_for_ai.cli validate-prd-modules registries/prd_module_registry.csv
```

Validator checks:

1. Registry file exists.
2. Each module path exists.
3. Each module has an authority notice.
4. Each module declares source PRDs.
5. Each module declares subject layer.
6. Each module declares source authority status.
7. Requirement prefixes are not owned by multiple canonical modules.
8. Draft modules do not claim canonical authority.
9. Superseded canonical sources remain referenced.
10. Requirement trace registry knows the module or has TODO rows with explicit status.

### 18.8 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001
objective: Create a governed strategy for decomposing canonical PRDs into modular sub-PRDs.
role: requirements_manager
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: prd_decomposition_strategy
allowed_reads:
  - PRDs/**
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md
  - Sys4AI/registries/requirement_trace_registry.csv
  - Sys4AI/registries/source_registry.csv
allowed_writes:
  - PRDs/PRD_decomposition_strategy.md
  - Sys4AI/registries/prd_module_registry.csv
  - Sys4AI/schemas/contracts/prd_module_registry_row.schema.json
  - Sys4AI/sys_for_ai/prd_modules.py
  - Sys4AI/sys_for_ai/cli.py
  - Sys4AI/Makefile
  - Sys4AI/tests/test_prd_modules.py
  - Sys4AI/control_records/agentjobs/AJ-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml
forbidden_actions:
  - Create sub-PRDs as canonical without promotion.
  - Supersede canonical Phase 0 or Phase 1 PRDs during strategy work.
  - Delete historical PRDs.
validators:
  - cd Sys4AI && make validate-prd-modules
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && .venv/bin/python -m unittest discover -s tests
  - cd Sys4AI && make validate
completion_evidence:
  - Decomposition strategy
  - PRD module registry
  - Validator output
stop_conditions:
  - Walking skeleton evidence is absent unless maintainer explicitly waives the recommended ordering.
  - Requirement ownership cannot be represented without ambiguity.
```

### 18.9 Acceptance Criteria

- Strategy exists.
- Strategy states that generated sub-PRDs are draft until promoted.
- PRD module registry exists and validates.
- Validator prevents duplicate canonical requirement ownership.
- No canonical PRD is superseded during strategy creation.

---

## 19. WS-24: Sub-PRD Draft Generation

### 19.1 Purpose

Generate modular sub-PRD drafts from the canonical PRDs, Phase 2 PRD, walking skeleton evidence, and decomposition strategy.

### 19.2 Draft Policy

Every draft must contain this notice near the top:

```md
> Authority notice: This document is a decomposed PRD draft generated from canonical source PRDs and walking-skeleton evidence. It is not canonical unless promoted by a Director Decision and source-authority workflow. When this draft conflicts with canonical PRDs, the canonical PRDs control.
```

### 19.3 Required Metadata

Each sub-PRD draft must include:

```md
**PRD module ID:** <module ID>
**Document status:** Decomposed draft
**Subject layer:** framework_product
**Source authority status:** derivative_draft
**Source PRDs:** <paths>
**Source evidence:** <RDRs, receipts, demo reports as applicable>
**Owns requirement prefixes:** <prefix list>
**References requirement prefixes:** <prefix list>
**Promotion status:** not_promoted
**Last updated:** 2026-07-08
```

### 19.4 Sub-PRD Content Template

```md
# <Module Name> PRD

> Authority notice: ...

## 1. Executive Summary

## 2. Scope

## 3. Non-Scope

## 4. Source Authority and Trace

## 5. Definitions

## 6. Users, Roles, and Stakeholders

## 7. Requirements Owned by This Module

| Requirement ID | Requirement | Source evidence | Status |
|---|---|---|---|

## 8. Requirements Referenced from Other Modules

| Requirement ID | Owner module | Reason for reference |
|---|---|---|

## 9. Artifact Contracts

## 10. Validators and Acceptance Criteria

## 11. Risks and Open Questions

## 12. Deferred Items

## 13. Promotion Checklist
```

### 19.5 Batch Strategy

Do not generate all sub-PRDs in one uncontrolled blob if implementation happens through `/continue`. Use batches.

Recommended batch split:

| Batch | Modules |
|---|---|
| Batch A | init/discovery, AgentJob/continue, source-first memory, system layers/self-hosting |
| Batch B | role governance, skill lifecycle, validation/traceability, target-system generation |
| Batch C | operations/maintenance, interface/integration, security/safety/assurance, domain-pack |

This plan defines one AgentJob for all draft generation only if the generated files are purely derivative drafts and validators are deterministic. If the implementation agent judges the batch too large, split into `AJ-SFADEV-24A`, `24B`, and `24C`.

### 19.6 Files to Add

```text
PRDs/modules/Sys4AI_init_and_discovery_prd.md
PRDs/modules/Sys4AI_agentjob_and_continue_prd.md
PRDs/modules/Sys4AI_source_first_memory_prd.md
PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md
PRDs/modules/Sys4AI_role_governance_prd.md
PRDs/modules/Sys4AI_skill_lifecycle_prd.md
PRDs/modules/Sys4AI_validation_and_traceability_prd.md
PRDs/modules/Sys4AI_target_system_generation_prd.md
PRDs/modules/Sys4AI_operations_improvement_maintenance_prd.md
PRDs/modules/Sys4AI_interface_and_integration_prd.md
PRDs/modules/Sys4AI_security_safety_assurance_prd.md
PRDs/modules/Sys4AI_domain_pack_prd.md
PRDs/modules/README.md
```

### 19.7 Files to Modify

```text
Sys4AI/registries/prd_module_registry.csv
Sys4AI/registries/source_registry.csv
Sys4AI/registries/object_relationship_registry.csv
Sys4AI/registries/requirement_trace_registry.csv
Sys4AI/docs/generated/registry_catalog/index.md
```

### 19.8 Requirement Extraction Rules

1. Preserve existing requirement IDs exactly.
2. Do not invent new canonical IDs unless the decomposition strategy allows a new module-local requirement.
3. If text must be clarified, mark it as `draft_rewording` and keep original source reference.
4. If a requirement belongs in multiple modules, choose one owner and list the other module as reference-only.
5. If ownership is unclear, place the requirement in `PRDs/modules/OPEN_REQUIREMENT_OWNERSHIP.md` or equivalent issue register, not in two canonical slots.
6. Never move superseded historical PRD content into a draft as current authority without noting its historical status.

### 19.9 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-24-SUBPRD-DRAFTS-001
objective: Generate modular sub-PRD drafts from canonical PRDs and walking skeleton evidence.
role: requirements_manager
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: subprd_draft_generation
allowed_reads:
  - PRDs/Sys4AI_phase-0_product_system_design_prd.md
  - PRDs/Sys4AI_phase-1_implementation_initialization_prd.md
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - PRDs/Sys4AI_phase-0_prd.md
  - PRDs/PRD_decomposition_strategy.md
  - implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md
  - Sys4AI/registries/requirement_trace_registry.csv
allowed_writes:
  - PRDs/modules/**
  - Sys4AI/registries/prd_module_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/object_relationship_registry.csv
  - Sys4AI/registries/requirement_trace_registry.csv
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-24-SUBPRD-DRAFTS-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-24-SUBPRD-DRAFTS-001.yaml
forbidden_actions:
  - Mark sub-PRDs canonical.
  - Supersede canonical PRDs.
  - Delete or rewrite superseded historical PRD.
  - Resolve ambiguous requirement ownership by duplicating ownership.
validators:
  - cd Sys4AI && make validate-prd-modules
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && make validate-generated-derivatives
  - cd Sys4AI && make validate
completion_evidence:
  - List of sub-PRD drafts
  - PRD module registry status
  - Requirement ownership report
  - Validation output
stop_conditions:
  - Decomposition strategy is absent.
  - More than one module would own the same requirement.
  - Draft cannot preserve authority notice.
```

### 19.10 Acceptance Criteria

- All intended sub-PRD drafts exist.
- Each draft has authority notice, source PRDs, subject layer, and source authority status.
- PRD module registry validates.
- No duplicate canonical ownership exists.
- Drafts are not promoted during this AgentJob.
- Requirement trace remains valid.

---

## 20. WS-25: Sub-PRD Promotion or Routing

### 20.1 Purpose

Review sub-PRD drafts and decide what becomes canonical, what stays draft, what is deferred, and what requires additional decomposition work.

### 20.2 Promotion Decision Options

For each module:

| Decision | Meaning |
|---|---|
| `promote_to_canonical_module` | Module becomes canonical owner for its declared requirement set. |
| `keep_as_derivative_draft` | Draft remains useful but noncanonical. |
| `defer_for_later_phase` | Module belongs to later lifecycle work. |
| `split_module` | Module is too broad and requires smaller modules. |
| `merge_module` | Module is too narrow or overlaps another module. |
| `block_promotion` | Promotion cannot proceed due to trace gap, conflict, or missing requirement authority. |

### 20.3 Promotion Control Record

Create:

```text
Sys4AI/control_records/director_decisions/DDR-SFADEV-25-SUBPRD-PROMOTION-001.yaml
```

Decision should include a table:

```yaml
module_decisions:
  - prd_module_id: PRD-MOD-INIT-DISCOVERY
    path: PRDs/modules/Sys4AI_init_and_discovery_prd.md
    decision: promote_to_canonical_module
    canonical_effect: owns listed init and discovery requirement prefixes
    required_trace_updates:
      - requirement_trace_registry.csv
      - prd_module_registry.csv
    conditions: []
```

### 20.4 Canonical PRD Index

Add or update:

```text
PRDs/README.md
```

The README should state:

1. Which PRDs are canonical.
2. Which PRDs are historical.
3. Which modules are canonical.
4. Which modules are drafts.
5. Which source wins in conflict.
6. How to propose new requirements.
7. How to promote draft modules.

### 20.5 Supersession Strategy

Do not immediately delete or fully supersede Phase 0 and Phase 1 PRDs unless maintainer explicitly chooses full modular canonical migration.

Recommended transitional model:

```text
Phase 0 and Phase 1 PRDs remain canonical baseline sources.
Promoted modules become canonical module views for their owned requirement families.
The PRD module registry records ownership.
Conflict resolution remains explicit.
Full supersession of large PRDs is deferred to a later migration.
```

This avoids breaking existing requirement trace and lets modular PRDs mature.

### 20.6 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-25-SUBPRD-PROMOTION-001
objective: Decide promotion, deferral, or draft status for generated sub-PRDs and update authority surfaces.
role: system_director
subject_system_id: Sys4AI
subject_layer: framework_product
authority_scope: subprd_authority_promotion
allowed_reads:
  - PRDs/modules/**
  - PRDs/PRD_decomposition_strategy.md
  - PRDs/Sys4AI_phase-0_product_system_design_prd.md
  - PRDs/Sys4AI_phase-1_implementation_initialization_prd.md
  - PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
  - Sys4AI/registries/prd_module_registry.csv
  - Sys4AI/registries/requirement_trace_registry.csv
allowed_writes:
  - PRDs/README.md
  - Sys4AI/control_records/director_decisions/DDR-SFADEV-25-SUBPRD-PROMOTION-001.yaml
  - Sys4AI/registries/prd_module_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/object_relationship_registry.csv
  - Sys4AI/registries/requirement_trace_registry.csv
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-25-SUBPRD-PROMOTION-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-25-SUBPRD-PROMOTION-001.yaml
forbidden_actions:
  - Delete canonical PRDs.
  - Promote a module with unresolved duplicate requirement ownership.
  - Promote a module that lacks source trace.
  - Silently rewrite requirement IDs.
validators:
  - cd Sys4AI && make validate-prd-modules
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && make validate-control-records
  - cd Sys4AI && make validate
completion_evidence:
  - Director Decision
  - PRDs README
  - Module registry diff
  - Trace validation output
stop_conditions:
  - Maintainer approval is required but absent.
  - Promotion would create conflicting canonical authority.
```

### 20.7 Acceptance Criteria

- Each sub-PRD has an explicit promotion/routing decision.
- `PRDs/README.md` explains current PRD authority.
- PRD module registry reflects decisions.
- Requirement trace remains valid.
- No canonical conflict is introduced.

---

# Part D: Final Acceptance

---

## 21. WS-26: Final Acceptance and Handoff

### 21.1 Purpose

Close this next-scope implementation plan with a complete acceptance packet.

### 21.2 Final Acceptance Report

Create:

```text
implementation_plans/completion_receipts/CR-SFADEV-NEXT-SCOPE-IMPLEMENTED-001.md
```

Recommended sections:

1. Receipt ID.
2. Date.
3. Plan path.
4. AgentJob.
5. Result.
6. Summary.
7. Scope selection evidence.
8. Legacy pending reconciliation evidence.
9. Phase 2 walking skeleton evidence.
10. Target package evidence.
11. PRD decomposition evidence.
12. Promotion or routing evidence.
13. Commands run.
14. Validation results.
15. Open issues.
16. Deferred items.
17. Known limitations.
18. Maintainer checklist.
19. Recommended next scope.

### 21.3 Required Final Validation Commands

Root:

```bash
make validate-dev-skills
make validate-product-scaffold
make validate
```

Product scaffold:

```bash
cd Sys4AI
make doctor
make validate-discovery-records
make validate-prd-modules
make validate-walking-skeleton
make validate-target-package-smoke
make validate-requirement-trace
make validate-registry-graph
make validate-generated-derivatives
make validate
.venv/bin/python -m unittest discover -s tests
git diff --check
```

If `validate-prd-modules`, `validate-walking-skeleton`, or `validate-target-package-smoke` are intentionally not added to aggregate validation, the acceptance report must explain why and list the replacement check.

### 21.4 Proposed AgentJob

```yaml
schema_version: "0.2.0"
agentjob_id: AJ-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001
objective: Validate and close the next-scope implementation plan.
role: requirements_verifier
subject_system_id: Sys4AI-dev
subject_layer: development_system
authority_scope: next_scope_acceptance
allowed_reads:
  - implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md
  - implementation_plans/reconciliation_reports/**
  - implementation_plans/acceptance_reports/**
  - implementation_plans/completion_receipts/**
  - PRDs/**
  - Sys4AI/control_records/**
  - Sys4AI/registries/**
  - Sys4AI/docs/generated/**
  - Sys4AI/examples/target_systems/**
allowed_writes:
  - implementation_plans/completion_receipts/CR-SFADEV-NEXT-SCOPE-IMPLEMENTED-001.md
  - implementation_plans/completion_audits/PLAN-COMPLETION-AUDIT-SFADEV-26.md
  - Sys4AI/control_records/completions/RECEIPT-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml
  - Sys4AI/control_records/handoffs/HANDOFF-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml
  - Sys4AI/control_records/program_state.yaml
  - Sys4AI/registries/completion_receipt_registry.csv
  - Sys4AI/registries/handoff_registry.csv
  - Sys4AI/registries/source_registry.csv
  - Sys4AI/registries/control_record_registry.csv
forbidden_actions:
  - Modify requirements during acceptance.
  - Hide failed validation.
  - Mark future deferred work as completed.
validators:
  - make validate
  - cd Sys4AI && make validate
  - cd Sys4AI && .venv/bin/python -m unittest discover -s tests
  - git diff --check
completion_evidence:
  - Completion receipt
  - Completion audit
  - Final handoff
  - Program state update
stop_conditions:
  - Any blocking validator fails.
  - Any sub-PRD has unresolved canonical authority conflict.
  - Any legacy pending row remains accidentally selectable without Director Decision.
```

### 21.5 Final Acceptance Criteria

- New scope selection is recorded.
- Legacy pending AgentJobs are reconciled.
- Phase 2 walking skeleton has demonstrable artifact chain.
- Target-system package smoke artifact validates.
- PRD decomposition strategy exists.
- Sub-PRDs are drafted and either promoted or explicitly routed.
- Authority of canonical, draft, generated, scaffold, and historical artifacts is clear.
- Final validations pass.
- Program state is complete or intentionally blocked with explicit reason.
- Handoff names the next recommended phase.

---

# Part E: Cross-Cutting Requirements

---

## 22. Registry Updates Required Across Workstreams

### 22.1 Existing Registries to Update

```text
Sys4AI/registries/source_registry.csv
Sys4AI/registries/derivative_registry.csv
Sys4AI/registries/object_relationship_registry.csv
Sys4AI/registries/control_record_registry.csv
Sys4AI/registries/agentjob_registry.csv
Sys4AI/registries/director_decision_registry.csv
Sys4AI/registries/completion_receipt_registry.csv
Sys4AI/registries/handoff_registry.csv
Sys4AI/registries/memory_preflight_receipt_registry.csv
Sys4AI/registries/requirement_trace_registry.csv
Sys4AI/registries/artifact_contract_registry.csv
Sys4AI/registries/validation_contract_registry.csv
```

### 22.2 New Registries Recommended

```text
Sys4AI/registries/prd_module_registry.csv
```

Optional later:

```text
Sys4AI/registries/target_package_registry.csv
Sys4AI/registries/walking_skeleton_flow_registry.csv
```

Add optional registries only if needed. Do not multiply registries just to admire the spreadsheet orchard.

---

## 23. Schema and Validator Updates

### 23.1 New JSON Schema Contracts

```text
Sys4AI/schemas/contracts/prd_module_registry_row.schema.json
Sys4AI/schemas/contracts/target_system_manifest.schema.json
```

Optional:

```text
Sys4AI/schemas/contracts/target_package_registry_row.schema.json
Sys4AI/schemas/contracts/walking_skeleton_flow_registry_row.schema.json
```

### 23.2 New Python Modules

```text
Sys4AI/sys_for_ai/prd_modules.py
Sys4AI/sys_for_ai/walking_skeleton.py
Sys4AI/sys_for_ai/target_package.py
Sys4AI/sys_for_ai/trace_flow.py
```

### 23.3 CLI Commands

```bash
python -m sys_for_ai.cli validate-prd-modules registries/prd_module_registry.csv
python -m sys_for_ai.cli walking-skeleton validate-flow --json
python -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
```

### 23.4 Makefile Targets

```make
validate-prd-modules:
	$(PYTHON) -m sys_for_ai.cli validate-prd-modules registries/prd_module_registry.csv

validate-walking-skeleton:
	$(PYTHON) -m sys_for_ai.cli walking-skeleton validate-flow --json

validate-target-package-smoke:
	$(PYTHON) -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json
```

Add to aggregate `validate` after each command is implemented and stable.

---

## 24. Requirement Trace Strategy

### 24.1 Trace Chain

The desired trace chain is:

```text
User or maintainer intent
  -> Director Decision
  -> RDR candidate requirements
  -> PRD baselined requirements
  -> Implementation plan tasks
  -> AgentJobs
  -> Completion receipts
  -> Handoffs
  -> Validators
  -> Generated docs or package outputs
```

### 24.2 Trace Row Requirements

Each new trace row should include:

- Trace ID.
- Source requirement ID.
- Source artifact path.
- Target artifact path.
- Coverage status.
- Semantic trace class.
- Justification.
- Validation command.
- Semantic review verdict.
- Subject layer.
- Authority status.

### 24.3 Coverage Status Vocabulary

```text
covered
partial
deferred
not_applicable
blocked
superseded
```

### 24.4 Semantic Trace Classes

```text
implementation_initialization
walking_skeleton_demonstration
prd_decomposition
source_authority_governance
validation_contract
registry_control
later_lifecycle_deferred
```

---

## 25. Risk Register

| Risk ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---:|---:|---|
| RISK-NEXT-001 | Prior completed plan is accidentally reopened. | Medium | High | WS-15 Director Decision states closure and new scope explicitly. |
| RISK-NEXT-002 | Legacy pending AgentJobs are selected by `/continue`. | Medium | High | WS-16 reconciles pending rows before Phase 2 work. |
| RISK-NEXT-003 | Walking skeleton becomes too ambitious and drifts into production runtime. | Medium | High | PRD and AgentJobs explicitly forbid production runtime claims. |
| RISK-NEXT-004 | PRD decomposition creates conflicting canonical sources. | High | High | PRD module registry and validator enforce ownership rules. |
| RISK-NEXT-005 | Generated sub-PRDs are mistaken for canonical authority. | Medium | High | Draft authority notices, registry status, and promotion Decision required. |
| RISK-NEXT-006 | Structural validator pass is overclaimed as semantic correctness. | Medium | Medium | Acceptance reports separate proven and not-proven claims. |
| RISK-NEXT-007 | New validators become brittle due to source hash placeholders. | Medium | Medium | Preserve Phase 1 placeholder policy or introduce staged hash enforcement. |
| RISK-NEXT-008 | Module PRDs are too granular and hard to maintain. | Medium | Medium | Use walking skeleton evidence to set boundaries and allow merge decisions. |
| RISK-NEXT-009 | Target package smoke example looks like a production generated system. | Medium | Medium | Strong authority notices and package validator checks for prohibited claims. |
| RISK-NEXT-010 | Aggregate validation becomes slow or fragile. | Low | Medium | Add new targets to aggregate only after deterministic tests pass. |

---

## 26. Open Questions

| Question ID | Question | Blocking? | Recommended handling |
|---|---|---:|---|
| OPEN-NEXT-001 | Should Phase 2 PRD be canonical immediately after generation or reviewed as draft first? | No | Default to draft, then promote through completion receipt or Director Decision. |
| OPEN-NEXT-002 | Should sub-PRDs become canonical modules now or remain derivative drafts through one more cycle? | No | Promote only low-conflict modules first; keep ambiguous modules draft. |
| OPEN-NEXT-003 | Should target-system package output live under `Sys4AI/examples/` or `Sys4AI/templates/`? | No | Use `examples/` for smoke package; use `templates/` only for reusable generation templates. |
| OPEN-NEXT-004 | Should the walking skeleton include a generator or only a validator? | No | Start with validator plus static smoke package; add generation later if needed. |
| OPEN-NEXT-005 | Should legacy pending rows be set to `superseded`, `blocked`, or `deferred` if validator status vocabulary is limited? | Maybe | Inspect validator vocabulary first; choose legal statuses and record rationale. |
| OPEN-NEXT-006 | Should PRD module ownership be prefix-based or individual-requirement-based? | No | Start prefix-based for maintainability; allow exception rows for individual IDs. |

---

## 27. Implementation Timeline by Dependency

This is not a calendar timeline. It is a dependency order.

```text
WS-15 Scope Selection
  -> WS-16 Legacy Reconciliation
      -> WS-17 Phase 2 RDR
          -> WS-18 Phase 2 PRD
              -> WS-19 Phase 2 Implementation Plan and AgentJobs
                  -> WS-20 Walking Skeleton Flow Validator
                      -> WS-21 Target Package Smoke Surface
                          -> WS-22 Walking Skeleton Demo and Acceptance
                              -> WS-23 PRD Decomposition Strategy
                                  -> WS-24 Sub-PRD Drafts
                                      -> WS-25 Sub-PRD Promotion or Routing
                                          -> WS-26 Final Acceptance and Handoff
```

Parallelization is not recommended until WS-22 completes. After the walking skeleton acceptance, PRD decomposition batches may be parallelized only if each batch has separate AgentJobs and no overlapping requirement ownership.

---

## 28. Definition of Done for the Whole Plan

This plan is done when:

1. The prior all-recommendations implementation plan remains closed.
2. A new Director Decision selects and closes this next-scope plan.
3. Legacy pending AgentJob rows are reconciled.
4. Phase 2 walking skeleton RDR exists and validates.
5. Phase 2 PRD exists and traces to the RDR.
6. Phase 2 implementation plan exists and traces to the PRD.
7. Walking skeleton flow validator exists and passes.
8. Target package smoke example exists and validates.
9. Walking skeleton demonstration report exists.
10. PRD decomposition strategy exists.
11. PRD module registry exists and validates.
12. Sub-PRD drafts exist with clear authority notices.
13. Each sub-PRD has a promotion, deferral, merge, split, or draft decision.
14. Requirement trace validates.
15. Registry graph validates.
16. Generated derivatives validate.
17. Root `make validate` passes.
18. Product `make validate` passes.
19. Unit tests pass.
20. Final acceptance receipt records results, limitations, deferred items, and next scope.

---

## 29. Recommended Next Scope After This Plan

After this plan is complete, the best next scope should be selected from evidence.

Likely candidates:

1. **Phase 3 Target-System Template Generation**  
   Build reusable generation templates and stronger package/export commands.

2. **Runtime Orchestration Prototype**  
   Introduce a minimal orchestrator that can invoke or simulate skill routing under AgentJob boundaries.

3. **Source Hash Enforcement Hardening**  
   Move registry `source_hash` fields from `pending` placeholders toward deterministic hash validation.

4. **Operational Lifecycle PRD and Plan**  
   Start the run/improve/maintain side of the framework.

5. **Domain Pack Pilot**  
   Add one intentionally small domain pack after the domain-pack router and target-system generation path are stable.

Recommended choice after this plan: **Phase 3 Target-System Template Generation**, unless the walking skeleton exposes validation or authority gaps that should be repaired first.

---

## 30. Maintainer Approval Checklist

Before implementation begins:

- [ ] I approve creating `DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001`.
- [ ] I approve treating the prior all-recommendations plan as closed.
- [ ] I approve reconciling legacy pending AgentJob rows before Phase 2 work.
- [ ] I approve the Phase 2 walking skeleton as the next product capability slice.
- [ ] I approve using `Repo Steward Agent` or another small domain-neutral sample as the target-system smoke example.
- [ ] I approve PRD decomposition after walking skeleton acceptance.
- [ ] I approve generated sub-PRDs starting as derivative drafts.
- [ ] I approve adding `prd_module_registry.csv` and associated validators.
- [ ] I approve final promotion/routing decisions for sub-PRDs requiring a Director Decision.

Before final acceptance:

- [ ] Legacy pending row reconciliation is complete.
- [ ] Phase 2 walking skeleton demo passes.
- [ ] Target package smoke example validates.
- [ ] PRD decomposition strategy exists.
- [ ] Sub-PRD drafts exist and are routed.
- [ ] No canonical authority conflict exists.
- [ ] Root validation passes.
- [ ] Product validation passes.
- [ ] Final handoff names the next recommended scope.

---

## 31. First Prompt to Start Implementation

Use this as the next implementation prompt when ready:

```text
/continue

Use the active Sys4AI-dev continuation protocol. Start from source-first memory preflight, inspect Sys4AI/control_records/program_state.yaml and the latest handoff, then select or create at most one authorized AgentJob for the next-scope plan.

The intended first task is WS-15: create DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001, register implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md as the active next-scope plan, preserve closure of the prior all-recommendations plan, update required registries and program state, run the required validators, create completion receipt and handoff, commit the bounded task, and stop before any second AgentJob.
```

---

## 32. Compact Artifact List

### New Planning and Acceptance Artifacts

```text
implementation_plans/Sys4AI-dev_next_scope_full_implementation_plan.md
implementation_plans/reconciliation_reports/LEGACY-PENDING-AGENTJOB-RECONCILIATION-SFADEV-16.md
implementation_plans/Sys4AI_phase-2_walking_skeleton_implementation_plan.md
implementation_plans/acceptance_reports/PHASE2-WALKING-SKELETON-DEMO-SFADEV-22.md
implementation_plans/completion_receipts/CR-SFADEV-NEXT-SCOPE-IMPLEMENTED-001.md
implementation_plans/completion_audits/PLAN-COMPLETION-AUDIT-SFADEV-26.md
```

### New PRD Artifacts

```text
PRDs/Sys4AI_phase-2_walking_skeleton_prd.md
PRDs/PRD_decomposition_strategy.md
PRDs/README.md
PRDs/modules/README.md
PRDs/modules/Sys4AI_init_and_discovery_prd.md
PRDs/modules/Sys4AI_agentjob_and_continue_prd.md
PRDs/modules/Sys4AI_source_first_memory_prd.md
PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md
PRDs/modules/Sys4AI_role_governance_prd.md
PRDs/modules/Sys4AI_skill_lifecycle_prd.md
PRDs/modules/Sys4AI_validation_and_traceability_prd.md
PRDs/modules/Sys4AI_target_system_generation_prd.md
PRDs/modules/Sys4AI_operations_improvement_maintenance_prd.md
PRDs/modules/Sys4AI_interface_and_integration_prd.md
PRDs/modules/Sys4AI_security_safety_assurance_prd.md
PRDs/modules/Sys4AI_domain_pack_prd.md
```

### New Code and Test Artifacts

```text
Sys4AI/sys_for_ai/prd_modules.py
Sys4AI/sys_for_ai/walking_skeleton.py
Sys4AI/sys_for_ai/target_package.py
Sys4AI/sys_for_ai/trace_flow.py
Sys4AI/tests/test_prd_modules.py
Sys4AI/tests/test_walking_skeleton.py
Sys4AI/tests/test_target_package.py
```

### New Example Package Artifacts

```text
Sys4AI/examples/target_systems/repo_steward_agent_package/README.md
Sys4AI/examples/target_systems/repo_steward_agent_package/target-system-manifest.yaml
Sys4AI/examples/target_systems/repo_steward_agent_package/requirements-discovery-record.md
Sys4AI/examples/target_systems/repo_steward_agent_package/product-requirements.md
Sys4AI/examples/target_systems/repo_steward_agent_package/implementation-plan.md
Sys4AI/examples/target_systems/repo_steward_agent_package/task-packets/TASK-001-read-only-repo-inspection.md
Sys4AI/examples/target_systems/repo_steward_agent_package/task-packets/TASK-002-current-state-baseline.md
Sys4AI/examples/target_systems/repo_steward_agent_package/task-packets/TASK-003-governed-next-action-plan.md
Sys4AI/examples/target_systems/repo_steward_agent_package/registries/requirement-trace.csv
Sys4AI/examples/target_systems/repo_steward_agent_package/registries/artifact-index.csv
Sys4AI/examples/target_systems/repo_steward_agent_package/validation/validation-summary.md
```

### New Registry and Schema Artifacts

```text
Sys4AI/registries/prd_module_registry.csv
Sys4AI/schemas/contracts/prd_module_registry_row.schema.json
Sys4AI/schemas/contracts/target_system_manifest.schema.json
```

### New Control Records

```text
Sys4AI/control_records/director_decisions/DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
Sys4AI/control_records/director_decisions/DDR-SFADEV-25-SUBPRD-PROMOTION-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-24-SUBPRD-DRAFTS-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-25-SUBPRD-PROMOTION-001.yaml
Sys4AI/control_records/agentjobs/AJ-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml
```

---

## 33. Final Recommendation

Implement this plan in the stated order.

The crucial move is not PRD decomposition first. The crucial move is controlled scope selection, then registry hygiene, then a walking skeleton that proves the product can perform its own lifecycle on a small example. After that, PRD decomposition becomes much safer because the modules can be shaped by real artifact flow.

The repository should leave this sequence with three improvements:

1. A cleaner control loop with no misleading legacy pending work.
2. A demonstrated `Sys4AI` end-to-end product path.
3. A modular PRD system that is traceable, governed, and ready for later phases.

That is the bridge from scaffold to system.
