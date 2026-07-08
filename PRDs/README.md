# Sys4AI PRD Authority Index

**Document status:** Controlled PRD authority index
**Subject layer:** framework_product
**Source authority status:** controlled
**Last updated:** 2026-07-08

> Authority notice: This index explains current PRD authority. It does not promote
> derivative draft sub-PRDs, supersede canonical PRDs, or create new canonical
> requirement ownership.

## Canonical And Controlled PRDs

| Source | Status | Current authority |
|---|---|---|
| `PRDs/Sys4AI_phase-0_product_system_design_prd.md` | canonical | Product and system-design baseline for Sys4AI. |
| `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md` | canonical_draft | Phase 1 implementation initialization baseline and scaffold requirements. |
| `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md` | controlled | Accepted Phase 2 walking-skeleton PRD. |
| `PRDs/PRD_decomposition_strategy.md` | controlled strategy | Decomposition and promotion strategy for modular PRD work. |

## Historical PRDs

| Source | Status | Use |
|---|---|---|
| `PRDs/Sys4AI_phase-0_prd.md` | historical reference | Superseded Phase 0 reference. Use for historical context only unless a later source-authority decision promotes specific content. |

## Canonical Modules

No PRD module is canonical as of `DDR-SFADEV-25-SUBPRD-PROMOTION-001`.

## Draft Modules

All AJ24 modules remain `draft` and `derivative_draft`. Their WS-25 routing decision is `keep_as_derivative_draft`.

| Module ID | Draft | Authority scope | WS-25 decision |
|---|---|---|---|
| `PRD-MOD-INIT-DISCOVERY` | `PRDs/modules/Sys4AI_init_and_discovery_prd.md` | `init_discovery` | `keep_as_derivative_draft` |
| `PRD-MOD-AGENTJOB-CONTINUE` | `PRDs/modules/Sys4AI_agentjob_and_continue_prd.md` | `agentjob_continue` | `keep_as_derivative_draft` |
| `PRD-MOD-SOURCE-FIRST-MEMORY` | `PRDs/modules/Sys4AI_source_first_memory_prd.md` | `source_first_memory` | `keep_as_derivative_draft` |
| `PRD-MOD-SYSTEM-LAYERS-SELF-HOSTING` | `PRDs/modules/Sys4AI_system_layers_and_self_hosting_prd.md` | `system_layers_self_hosting` | `keep_as_derivative_draft` |
| `PRD-MOD-ROLE-GOVERNANCE` | `PRDs/modules/Sys4AI_role_governance_prd.md` | `role_governance` | `keep_as_derivative_draft` |
| `PRD-MOD-SKILL-LIFECYCLE` | `PRDs/modules/Sys4AI_skill_lifecycle_prd.md` | `skill_lifecycle` | `keep_as_derivative_draft` |
| `PRD-MOD-VALIDATION-TRACEABILITY` | `PRDs/modules/Sys4AI_validation_and_traceability_prd.md` | `validation_traceability` | `keep_as_derivative_draft` |
| `PRD-MOD-TARGET-SYSTEM-GENERATION` | `PRDs/modules/Sys4AI_target_system_generation_prd.md` | `target_system_generation` | `keep_as_derivative_draft` |
| `PRD-MOD-OPERATIONS-MAINTENANCE` | `PRDs/modules/Sys4AI_operations_improvement_maintenance_prd.md` | `operations_improvement_maintenance` | `keep_as_derivative_draft` |
| `PRD-MOD-INTERFACE-INTEGRATION` | `PRDs/modules/Sys4AI_interface_and_integration_prd.md` | `interface_integration` | `keep_as_derivative_draft` |
| `PRD-MOD-SECURITY-SAFETY-ASSURANCE` | `PRDs/modules/Sys4AI_security_safety_assurance_prd.md` | `security_safety_assurance` | `keep_as_derivative_draft` |
| `PRD-MOD-DOMAIN-PACK` | `PRDs/modules/Sys4AI_domain_pack_prd.md` | `domain_pack` | `keep_as_derivative_draft` |

## Conflict Resolution

When sources disagree, use this order:

1. Explicit Director Decision or accepted source-authority migration for the disputed scope.
2. Canonical or controlled PRDs listed above.
3. Controlled registries and validated control records.
4. Derivative draft modules.
5. Generated derivatives and temporary handoffs.

Derivative draft modules are explanatory decomposition views. They do not override
the canonical or controlled PRDs.

## Proposing New Requirements

New requirements should enter as candidate requirements in a requirements discovery
record, PRD draft, or module change proposal. The proposer should include:

- Source evidence or user need.
- A stable candidate requirement ID or proposed requirement prefix.
- A target authority scope.
- Trace evidence paths.
- Known conflicts with existing PRDs or module ownership.

The candidate remains noncanonical until accepted by the appropriate source-authority
workflow.

## Promoting Draft Modules

To promote a draft module:

1. Create a Director Decision that names the module, scope, owned requirement prefixes, and conflict rule.
2. Verify the module has complete normative requirement text, source trace, and validation evidence.
3. Update `Sys4AI/registries/prd_module_registry.csv` from `draft` to the selected canonical status.
4. Update `Sys4AI/registries/requirement_trace_registry.csv` and related source/relationship registries.
5. Run the required validators and close the bounded AgentJob with a completion receipt and handoff.

Full supersession of the large Phase 0, Phase 1, or Phase 2 PRDs is deferred to a
later migration unless a maintainer explicitly chooses that route.

## References

Sys4AI-dev. (2026a). *Sys4AI product and system-design PRD* [Product requirements document]. `PRDs/Sys4AI_phase-0_product_system_design_prd.md`.

Sys4AI-dev. (2026b). *Sys4AI implementation initialization PRD* [Product requirements document]. `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md`.

Sys4AI-dev. (2026c). *Sys4AI Phase 2 walking skeleton PRD* [Product requirements document]. `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`.

Sys4AI-dev. (2026d). *Sys4AI PRD decomposition strategy* [Decomposition strategy]. `PRDs/PRD_decomposition_strategy.md`.

Sys4AI-dev. (2026e). *Sub-PRD promotion Director Decision* [Director Decision Record]. `Sys4AI/control_records/director_decisions/DDR-SFADEV-25-SUBPRD-PROMOTION-001.yaml`.
