# Sys4AI PRD Decomposition Strategy

## 1. Document Status and Authority Notice

**Document status:** Controlled decomposition strategy
**Subject layer:** framework_product
**Source authority status:** controlled
**Owning role:** requirements_manager
**Last updated:** 2026-07-08

> Authority notice: This document defines the governed strategy for decomposing Sys4AI PRDs into modular sub-PRDs. It is not itself a sub-PRD, it does not supersede any canonical PRD, and it does not promote generated module drafts. When this strategy conflicts with canonical PRDs, the canonical PRDs control until a source-authority workflow changes that status.

## 2. Source PRDs Covered

This strategy covers decomposition of the current canonical and controlled product-requirements sources:

- `PRDs/Sys4AI_phase-0_product_system_design_prd.md`
- `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md`
- `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`

It also recognizes `PRDs/Sys4AI_phase-0_prd.md` as historical reference only. Historical content can inform migration, but it cannot override current canonical sources without explicit promotion.

## 3. Decomposition Goals

The goal is to split large PRDs along stable capability boundaries while preserving source authority, requirement identity, and traceability from PRD text to implementation evidence.

The decomposition must make ownership clearer without creating competing canonical sources. It should support smaller review packets, tighter validators, and easier future maintenance.

## 4. Non-Goals

This strategy does not:

- Promote sub-PRD drafts to canonical status.
- Supersede Phase 0, Phase 1, or Phase 2 PRDs.
- Rewrite requirement IDs.
- Convert generated derivatives into authority.
- Resolve every semantic requirement gap during the strategy packet.
- Execute sub-PRD draft generation; that belongs to `AJ-SFADEV-24-SUBPRD-DRAFTS-001`.

## 5. Capability Boundaries

Sub-PRDs should map to capability authority boundaries, not to the accidental shape of previous documents. A capability boundary is stable when it has a coherent purpose, a natural owning role, identifiable artifacts, and distinct validation obligations.

The initial boundaries are:

- Init and discovery
- AgentJob and `/continue`
- Source-first memory
- System layers and self-hosting
- Role governance
- Skill lifecycle
- Validation and traceability
- Target-system generation
- Operations, improvement, and maintenance
- Interface and integration
- Security, safety, and assurance
- Domain packs

## 6. Requirement Ownership Rules

After promotion, each requirement ID or declared requirement-prefix family must have exactly one owning PRD module. A module can reference requirements owned by another module, but it must not claim ownership of them.

Draft and planned modules may declare intended ownership. Canonical ownership begins only after source-authority promotion. Generated derivatives cannot own requirements.

If a requirement appears to belong in two modules, the strategy is to choose one owner and record the second module as a reference. If ownership remains ambiguous, the requirement must stay unresolved until a follow-up routing decision assigns it.

## 7. Cross-Reference Rules

Cross-references are allowed and expected. A valid cross-reference must identify the owner module, the referenced requirement or prefix, and the reason for the dependency.

Cross-references must not silently copy canonical language into a second authoritative location. The owning module retains the controlling wording after promotion.

## 8. Canonical Promotion Workflow

Promotion requires:

1. A Director Decision or equivalent source-authority record approving the module's authority scope.
2. A module file with an authority notice, source PRDs, subject layer, source authority status, and ownership metadata.
3. A `prd_module_registry.csv` row changed from `planned` or `draft` to `controlled`, `canonical_draft`, or `canonical`.
4. Requirement trace updates showing owned and referenced requirement families.
5. Validator evidence showing no duplicate canonical ownership.
6. A completion receipt and handoff recording promotion results.

## 9. Supersession Workflow

Supersession must be explicit. A module may supersede part of an older PRD only after promotion identifies the superseded source, preserves traceability to the replaced language, and leaves the superseded document available as historical evidence.

No canonical PRD is superseded by AJ23. Supersession is a later controlled operation.

## 10. Registry and Trace Updates

`Sys4AI/registries/prd_module_registry.csv` is the controlling registry for PRD module status, paths, authority scope, ownership prefixes, source PRDs, supersession, owner role, and validation status.

The requirement trace registry should remain the bridge from source requirements to implementation evidence. During AJ23, planned rows can declare intended ownership without requiring module files. During AJ24 and later, draft or promoted modules must appear in trace evidence or have explicit TODO/deferred trace status.

## 11. Validator Requirements

The PRD module validator must check:

- Registry existence and exact header.
- Required row fields.
- Valid module status, subject layer, owner role, and source authority status.
- Source PRD references that resolve to existing files.
- Planned rows may reference future module paths.
- Non-planned rows must resolve to real module files.
- Module files must declare authority notice, source PRDs, subject layer, and source authority status.
- Draft and planned rows cannot claim canonical authority.
- Canonical ownership prefixes cannot be duplicated across active canonical modules.
- Superseded sources must remain referenced.

## 12. Generated Derivative Policy

Generated derivatives can summarize, index, or render the decomposition state. They cannot promote drafts, own requirements, supersede PRDs, or authorize implementation. Any generated module draft remains `derivative_draft` until promotion.

## 13. Proposed Sub-PRD Index

| Module ID | Proposed path | Status |
|---|---|---|
| `PRD-MOD-INIT-DISCOVERY` | `PRDs/modules/Sys4AI_init_and_discovery_prd.md` | planned |
| `PRD-MOD-AGENTJOB-CONTINUE` | `PRDs/modules/Sys4AI_agentjob_and_continue_prd.md` | planned |
| `PRD-MOD-SOURCE-FIRST-MEMORY` | `PRDs/modules/Sys4AI_source_first_memory_prd.md` | planned |
| `PRD-MOD-SYSTEM-LAYERS-SELF-HOSTING` | `PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md` | planned |
| `PRD-MOD-ROLE-GOVERNANCE` | `PRDs/modules/Sys4AI_role_governance_prd.md` | planned |
| `PRD-MOD-SKILL-LIFECYCLE` | `PRDs/modules/Sys4AI_skill_lifecycle_prd.md` | planned |
| `PRD-MOD-VALIDATION-TRACEABILITY` | `PRDs/modules/Sys4AI_validation_and_traceability_prd.md` | planned |
| `PRD-MOD-TARGET-SYSTEM-GENERATION` | `PRDs/modules/Sys4AI_target_system_generation_prd.md` | planned |
| `PRD-MOD-OPERATIONS-MAINTENANCE` | `PRDs/modules/Sys4AI_operations_improvement_maintenance_prd.md` | planned |
| `PRD-MOD-INTERFACE-INTEGRATION` | `PRDs/modules/Sys4AI_interface_and_integration_prd.md` | planned |
| `PRD-MOD-SECURITY-SAFETY-ASSURANCE` | `PRDs/modules/Sys4AI_security_safety_assurance_prd.md` | planned |
| `PRD-MOD-DOMAIN-PACK` | `PRDs/modules/Sys4AI_domain_pack_prd.md` | planned |

## 14. Migration Phases

1. Strategy: define rules, planned registry rows, validator, and AJ24 route.
2. Drafting: generate module drafts as derivative drafts from canonical sources and walking-skeleton evidence.
3. Review: validate ownership, trace, gaps, and cross-module references.
4. Promotion or routing: promote, defer, split, merge, or keep modules as drafts.
5. Supersession: only after promotion, update canonical-source authority records if appropriate.

## 15. Acceptance Criteria

AJ23 is acceptable when:

- This strategy exists with the required authority notice.
- `prd_module_registry.csv` exists with planned module rows.
- `validate-prd-modules` passes and rejects duplicate canonical ownership.
- No sub-PRD draft is created as canonical.
- No canonical PRD is superseded.
- A controlled handoff routes the next bounded task to AJ24.

## References

Sys4AI-dev. (2026a). *Sys4AI phase 0 product system design PRD* [Product requirements document]. `PRDs/Sys4AI_phase-0_product_system_design_prd.md`.

Sys4AI-dev. (2026b). *Sys4AI phase 1 implementation initialization PRD* [Product requirements document]. `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md`.

Sys4AI-dev. (2026c). *Sys4AI phase 2 walking skeleton PRD* [Product requirements document]. `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`.

Sys4AI-dev. (2026d). *Sys4AI-dev next scope full implementation plan* [Implementation plan]. `implementation_plans/Sys4AI_next_scope_full_implementation_plan.md`.
