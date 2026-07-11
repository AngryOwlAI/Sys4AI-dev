> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_capability_migration_status
  authority_status: generated_noncanonical
  derivative_type: capability_migration_status_summary
  source_registries:
    - configs/capability_migration.toml
    - registries/requirement_trace_registry.csv
    - registries/derivative_registry.csv
  validation_contracts:
    - contract_capability_migration_manifest
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Capability Migration Status

This page summarizes the registered retired-runtime migration classifications. It does not restore AgentJob, `/continue`, or any removed runtime capability.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_capability_migration_status | docs/generated/governance/capability-migration-status.md | SRC-CONFIG-CAPABILITY-MIGRATION;SRC-REG-REQ-TRACE;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Classification State Counts

| state | count |
| --- | --- |
| active_but_stale | 1 |
| active_valid | 6 |
| authority_deferred | 2 |
| generated_derivative | 2 |
| historical | 1 |
| legacy_compatibility | 3 |

## Classification Rows

| classification_id | state | authority_scope | disposition |
| --- | --- | --- | --- |
| active_valid_migration_control | active_valid | pending | Retired terms are used only to define migration controls, negative tests, or explicit absence; they do not assert capability. |
| canonical_legacy_context | active_valid | pending | The canonical Phase 1 baseline retains explicitly labeled historical compatibility requirements and verbatim provenance examples while its current commands state and execution route use the portable contract. TX-13 must enforce the labels semantically. |
| legacy_registry_compatibility | legacy_compatibility | pending | Registry headers and current rows use portable execution fields lifecycle states and profile markers. Stable historical IDs paths and evidence relationships remain visible but cannot establish current capability. |
| legacy_schema_compatibility | legacy_compatibility | pending | Preserve read-only validation of explicitly historical records; TX-10 must prevent these contracts from serving as current execution authority. |
| legacy_reader_compatibility | legacy_compatibility | pending | Current writers use portable fields. These readers tests and the retained template support read-only validation and inspection of explicitly historical records and do not expose a current authoring route. |
| trace_migration_reviewed | active_valid | pending | TX-12 reviewed generalized capability and evidence states while compatibility columns retain retired terms only for exact rollback and historical provenance. |
| phase2_authority_deferred | authority_deferred | pending | Preserve the accepted Phase 2 artifact unchanged; its retired execution clauses are not current capability evidence and require G-06 plus a controlled addendum or successor. |
| target_package_deferred | authority_deferred | pending | Retain the older target-project configuration example as deferred compatibility evidence; TX-15 migrates the package validator and smoke example but does not redesign this separate configuration contract. |
| target_package_tx15_active | active_valid | pending | TX-15 implements the manifest-driven nonproduction package contract; retained retired terms occur only in explicit rejection logic and negative fixtures. |
| walking_skeleton_tx16_active | active_valid | pending | TX-16 implements the manifest-driven active flow; retained retired terms occur only in explicit rejection logic, negative tests, and historical-evidence boundaries. |
| tx19_module_validation_compatibility | active_valid | pending | Active TX-19 transaction and module validator retain AgentJob and /continue terms only in historical compatibility mappings forbidden-action boundaries and negative checks; no retired runtime surface is active. |
| prd_derivative_migration_tx19 | generated_derivative | pending | TX-19 regenerated the twelve module PRDs as noncanonical derivative drafts; retained AgentJob and /continue terms are historical compatibility labels only and current execution semantics are portable. |
| generated_reader_migration_tx20 | generated_derivative | pending | TX-20 regenerated the named strategic governance readers from registered controlled sources. The pages remain noncanonical navigation, and later changes must occur through their source registries and generators. |
| active_surface_tx10 | active_but_stale | pending | Migrate current state, roles, policies, registries, schemas, memory, tests, and active canonical execution requirements atomically in TX-10. |
| historical_control_evidence | historical | pending | Preserve completed plans, decisions, receipts, handoffs, discovery records, snapshots, and AgentJob-era records without rewriting activated history. |

## Boundary

Historical and compatibility references remain provenance only. Generated readers remain noncanonical; current capability requires separate implementation, verification, authority, and host evidence.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
