# Sys4AI Documentation Map

**Status:** Controlled navigation guide
**Last reviewed:** 2026-07-15
**Boundary:** This map routes readers. It does not replace source-registry,
decision, contract, or supersession authority.

## Authority classes

| Class | Meaning | Typical location |
|---|---|---|
| Canonical source | Normative product or phase requirements | `PRDs/` |
| Controlled source | Current policy, contract, configuration, registry, decision, transaction, or evidence | `Sys4AI/docs/`, `schemas/`, `configs/`, `registries/`, `control_records/` |
| Historical source | Preserved evidence that no longer defines current behavior | explicitly classified PRDs, plans, and control records |
| Generated derivative | Deterministic noncanonical reader or navigation page | `Sys4AI/docs/generated/` |
| Local support | Cache, local receipt support, working material, or unpromoted retrieval data | ignored or `.local/` surfaces |

When files conflict, inspect
[`source_registry.csv`](../registries/source_registry.csv), accepted decisions,
contracts, and supersession evidence. Do not select the most convenient file.

## New contributor

1. [root README](../../README.md)
2. [architecture overview](../../ARCHITECTURE.md)
3. [getting-started guide](getting_started.md)
4. [concepts and invariants](concepts_and_invariants.md)
5. [contributor guide](../../CONTRIBUTING.md)
6. [current program state](../control_records/program_state.yaml)

## Product researcher

1. [Phase 0 Product and System-Design PRD](../../PRDs/Sys4AI_phase-0_product_system_design_prd.md)
2. [Phase 1 Implementation Initialization PRD](../../PRDs/Sys4AI_phase-1_implementation_initialization_prd.md)
3. [system-document spine](system_document_spine.md)
4. [PRD authority index](../../PRDs/README.md)
5. [requirement trace](../registries/requirement_trace_registry.csv)
6. [program state](../control_records/program_state.yaml)
7. assurance and independent-evaluation sources under `Sys4AI/assurance/`

The strategic-baseline migration plan is retained planning evidence, not the
current state source.

## Systems engineer

1. [architecture overview](../../ARCHITECTURE.md)
2. [system-layer registry](../registries/system_layer_registry.csv)
3. [artifact-contract registry](../registries/artifact_contract_registry.csv)
4. [role registry](../registries/role_registry.csv)
5. [role-to-skill crosswalk](../registries/role_skill_crosswalk.csv)
6. [portable execution schema](../schemas/contracts/execution_transaction.schema.json)
7. [Codex reference-host profile](../configs/host_profiles/codex_app_reference.toml)
8. target-package and walking-skeleton implementations under `Sys4AI/sys_for_ai/`

## Software engineer

1. [getting-started guide](getting_started.md)
2. [product Makefile](../Makefile)
3. [package metadata](../pyproject.toml)
4. [Python reference implementation](../sys_for_ai/)
5. [unit and integration tests](../tests/)
6. [cross-version workflow](../../.github/workflows/cross-version-python.yml)
7. [source registry](../registries/source_registry.csv)
8. [derivative registry](../registries/derivative_registry.csv)

## Documentation contributor

1. [concepts and invariants](concepts_and_invariants.md)
2. [format-profile policy](format_profile_policy.md)
3. [memory-retrieval policy](memory_retrieval_policy.md)
4. [source registry](../registries/source_registry.csv)
5. [object relationships](../registries/object_relationship_registry.csv)
6. [derivative registry](../registries/derivative_registry.csv)
7. `make validate-markdown-source-surface`
8. existing deterministic generator commands in the product Makefile

## Security reviewer

1. security, permission, self-change, and authority requirements in the
   [Phase 0 PRD](../../PRDs/Sys4AI_phase-0_product_system_design_prd.md)
2. [self-hosting boundary policy](self_hosting_boundary_policy.md)
3. [Codex reference-host profile](../configs/host_profiles/codex_app_reference.toml)
4. safety and independent-evaluation sources under `Sys4AI/assurance/`
5. security and permission validators under `Sys4AI/sys_for_ai/`
6. threat-model and permission-scope skills in the active runtime

There is no promoted `SECURITY.md`. Private vulnerability reporting is
disabled and no verified private fallback route or supported-version statement
is registered. Establish those facts before publishing a security policy.

## Independent evaluator

1. independent-evaluation protocol under `Sys4AI/assurance/`
2. exact baseline commit and evaluated interface
3. public reference holdouts for regression context only
4. confidential external holdout requirements
5. result-receipt contract and conflict-of-interest disclosures
6. explicit excluded claims and accountable acceptance route

The protocol is ready, but current program state records that external
evaluation has not been executed.

## Target-system designer

1. [system-document spine](system_document_spine.md)
2. [skill-integration policy](skill_integration_policy.md)
3. discovery and strategic-intent templates under `Sys4AI/templates/`
4. target-package manifest schema under `Sys4AI/schemas/contracts/`
5. example target packages under `Sys4AI/examples/target_systems/`
6. target-package and walking-skeleton validators
7. target-specific stakeholder, affected-party, domain, permission, and
   operational evidence

The framework cannot grant target-specific domain acceptance.

## Maintainer reconstructing current state

Use this order:

1. [`program_state.yaml`](../control_records/program_state.yaml)
2. latest accepted Director Decision named by state
3. latest completion receipt
4. latest handoff
5. latest memory preflight receipt
6. relevant source, control, and relationship registries
7. generated readers for navigation only
8. Git history for exact baseline and publication evidence

Do not use a generated page, old plan checklist, or chat narrative as current
state when controlled state and accepted evidence are available.

## Generated readers

Generated pages under [`docs/generated/`](generated/) include configuration
and control catalogs, validation-contract catalogs, role pages, registry and
system-layer summaries, artifact-contract and core-skill summaries, and flow
reports. They are useful indexes. Make normative edits in their registered
sources and regenerate.
