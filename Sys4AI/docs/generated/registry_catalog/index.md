> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_registry_catalog_index
  authority_status: generated_noncanonical
  derivative_type: governance_registry_catalog_page
  source_registries:
    - registries/agentjob_registry.csv
    - registries/artifact_contract_registry.csv
    - registries/completion_receipt_registry.csv
    - registries/config_source_registry.csv
    - registries/control_record_registry.csv
    - registries/core_skill_proposal_registry.csv
    - registries/derivative_registry.csv
    - registries/director_decision_registry.csv
    - registries/discovery_record_registry.csv
    - registries/evidence_closure_plan_registry.csv
    - registries/format_profile_registry.csv
    - registries/handoff_registry.csv
    - registries/local_evidence_execution_registry.csv
    - registries/memory_preflight_receipt_registry.csv
    - registries/object_relationship_registry.csv
    - registries/plan_scope_interpretation_registry.csv
    - registries/prd_module_registry.csv
    - registries/registry_definition_registry.csv
    - registries/requirement_trace_registry.csv
    - registries/role_execution_binding_registry.csv
    - registries/role_registry.csv
    - registries/role_skill_crosswalk.csv
    - registries/skill_lifecycle_status_registry.csv
    - registries/skill_registry.csv
    - registries/source_registry.csv
    - registries/system_layer_registry.csv
    - registries/validation_contract_registry.csv
  validation_contracts:
    - contract_registry_header
  generated_at: 2026-07-12T14:24:41Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  validation_status: generated_content_checked
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Registry Catalog

This generated page indexes registered CSV registries. It is a navigation surface, not a registry authority.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_registry_catalog_index | docs/generated/registry_catalog/index.md | SRC-REG-SOURCES;SRC-REG-DERIVATIVES;SRC-REG-OBJECT-RELATIONSHIPS;SRC-REG-CONTROL-RECORDS;SRC-REG-VALIDATION-CONTRACTS;SRC-REG-SYSTEM-LAYERS;SRC-REG-ARTIFACT-CONTRACTS;SRC-REG-ROLES;SRC-PRODUCT-SKILL-REGISTRY;SRC-REG-CORE-SKILL-PROPOSALS;SRC-REG-SKILL-LIFECYCLE;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Registered Registries

| registry_file | registered_source_id | source_type | authority_status | row_count | owner |
| --- | --- | --- | --- | --- | --- |
| registries/agentjob_registry.csv | SRC-REG-AGENTJOBS | agentjob_registry | controlled | 34 | control_loop |
| registries/artifact_contract_registry.csv | SRC-REG-ARTIFACT-CONTRACTS | artifact_contract_registry | controlled | 30 | implementation_initialization |
| registries/completion_receipt_registry.csv | SRC-REG-COMPLETION-RECEIPTS | completion_receipt_registry | controlled | 56 | control_loop |
| registries/config_source_registry.csv | SRC-REG-CONFIG-SOURCES | config_source_registry | controlled | 6 | implementation_initialization |
| registries/control_record_registry.csv | SRC-REG-CONTROL-RECORDS | control_record_registry | controlled | 281 | implementation_initialization |
| registries/core_skill_proposal_registry.csv | SRC-REG-CORE-SKILL-PROPOSALS | core_skill_proposal_registry | controlled | 18 | implementation_initialization |
| registries/derivative_registry.csv | SRC-REG-DERIVATIVES | derivative_registry | controlled | 49 | implementation_initialization |
| registries/director_decision_registry.csv | SRC-REG-DIRECTOR-DECISIONS | director_decision_registry | controlled | 42 | control_loop |
| registries/discovery_record_registry.csv | SRC-REG-DISCOVERY-RECORDS | discovery_record_registry | controlled | 3 | implementation_initialization |
| registries/evidence_closure_plan_registry.csv | SRC-REG-EVIDENCE-CLOSURE-PLAN | evidence_closure_plan_registry | controlled | 484 | verification_engineer |
| registries/format_profile_registry.csv | SRC-REG-FORMAT-PROFILES | format_profile_registry | controlled | 5 | implementation_initialization |
| registries/handoff_registry.csv | SRC-REG-HANDOFFS | handoff_registry | controlled | 56 | control_loop |
| registries/local_evidence_execution_registry.csv | SRC-REG-LOCAL-EVIDENCE-EXECUTION | local_evidence_execution_registry | controlled | 74 | verification_engineer |
| registries/memory_preflight_receipt_registry.csv | SRC-REG-MEMORY-PREFLIGHT-RECEIPTS | memory_preflight_receipt_registry | controlled | 56 | control_loop |
| registries/object_relationship_registry.csv | SRC-REG-OBJECT-RELATIONSHIPS | object_relationship_registry | controlled | 422 | source_first_memory |
| registries/plan_scope_interpretation_registry.csv | SRC-REG-PLAN-SCOPE-INTERPRETATION | plan_scope_interpretation_registry | controlled | 410 | system_director |
| registries/prd_module_registry.csv | SRC-REG-PRD-MODULES | registry | controlled | 12 | framework_product |
| registries/registry_definition_registry.csv | SRC-REG-REGISTRY-DEFINITIONS | registry | controlled | 27 | registry_governance |
| registries/requirement_trace_registry.csv | SRC-REG-REQ-TRACE | requirement_trace_registry | controlled | 227 | requirements_verifier |
| registries/role_execution_binding_registry.csv | SRC-REG-ROLE-EXECUTION-BINDINGS | role_execution_binding_registry | controlled | 20 | implementation_initialization |
| registries/role_registry.csv | SRC-REG-ROLES | role_registry | controlled | 31 | implementation_initialization |
| registries/role_skill_crosswalk.csv | SRC-REG-ROLE-SKILL-CROSSWALK | role_skill_crosswalk | controlled | 45 | implementation_initialization |
| registries/skill_lifecycle_status_registry.csv | SRC-REG-SKILL-LIFECYCLE | skill_lifecycle_status_registry | controlled | 8 | implementation_initialization |
| registries/skill_registry.csv | SRC-PRODUCT-SKILL-REGISTRY | skill_registry | controlled | 32 | skill_governance |
| registries/source_registry.csv | SRC-REG-SOURCES | source_registry | controlled | 621 | implementation_initialization |
| registries/system_layer_registry.csv | SRC-REG-SYSTEM-LAYERS | system_layer_registry | controlled | 5 | implementation_initialization |
| registries/validation_contract_registry.csv | SRC-REG-VALIDATION-CONTRACTS | validation_contract_registry | controlled | 51 | implementation_initialization |

## Generation Boundary

The catalog is derived from CSV file presence plus source-registry rows. Missing or stale source rows must be corrected in the source registries, not here.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
