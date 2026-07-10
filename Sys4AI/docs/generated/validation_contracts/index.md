> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_validation_contracts_index
  authority_status: generated_noncanonical
  derivative_type: validation_contracts_catalog_page
  source_registries:
    - registries/validation_contract_registry.csv
  validation_contracts:
    - contract_agentjob
    - contract_handoff
    - contract_completion_receipt
    - contract_state_snapshot
    - contract_sys4ai_config
    - contract_self_hosting_mode
    - contract_target_project_config
    - contract_format_profile_registry_row
    - contract_config_source_registry_row
    - contract_control_record_registry_row
    - contract_validation_contract_registry_row
    - contract_registry_header
    - contract_requirement_trace_registry_row
    - contract_program_state
    - contract_director_decision
    - contract_agentjob_v0_2
    - contract_handoff_v0_2
    - contract_completion_receipt_v0_2
    - contract_memory_preflight_receipt
    - contract_agentjob_registry_row
    - contract_director_decision_registry_row
    - contract_handoff_registry_row
    - contract_completion_receipt_registry_row
    - contract_memory_preflight_receipt_registry_row
    - contract_system_layer_registry_row
    - contract_discovery_record_registry_row
    - contract_role_registry_row
    - contract_role_skill_crosswalk_row
    - contract_role_execution_binding_registry_row
    - contract_artifact_contract_registry_row
    - contract_core_skill_proposal_registry_row
    - contract_skill_lifecycle_status_registry_row
    - contract_prd_module_registry_row
    - contract_strategic_intent_common
    - contract_target_vision_statement
    - contract_target_core_values
    - contract_host_capability_profile
  generated_at: 2026-07-06T00:00:00Z
  generator: sys_for_ai.derivatives.validation_contracts_catalog:0.1.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Validation Contracts Catalog

This generated page indexes executable validation contracts. It is a reader catalog, not a contract authority.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_validation_contracts_index | docs/generated/validation_contracts/index.md | SRC-REG-VALIDATION-CONTRACTS | sys_for_ai.derivatives.validation_contracts_catalog:0.1.0 | generated_derivative |
| der_validation_contracts_by_target | docs/generated/validation_contracts/contracts-by-target.md | SRC-REG-VALIDATION-CONTRACTS | sys_for_ai.derivatives.validation_contracts_catalog:0.1.0 | generated_derivative |

## Structural Versus Semantic Warning

Validation contracts prove structural conformance only. They do not prove semantic truth, product correctness, or implementation completeness.

## Contract Rows

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_agentjob | schemas/contracts/agentjob.schema.json | 2020-12 | yaml | agentjob | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | controlled | pending | pending |
| contract_handoff | schemas/contracts/handoff.schema.json | 2020-12 | yaml | handoff | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | controlled | pending | pending |
| contract_completion_receipt | schemas/contracts/completion_receipt.schema.json | 2020-12 | yaml | completion_receipt | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | controlled | pending | pending |
| contract_state_snapshot | schemas/contracts/state_snapshot.schema.json | 2020-12 | yaml | state_snapshot | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | controlled | pending | pending |
| contract_sys4ai_config | schemas/contracts/sys4ai_config.schema.json | 2020-12 | toml | framework_config | pyproject.toml;configs/examples/sys4ai.example.toml | Sys4AI validate-toml-config | implementation_initialization | controlled | pending | pending |
| contract_self_hosting_mode | schemas/contracts/self_hosting_mode.schema.json | 2020-12 | toml | self_hosting_mode | configs/self_hosting_mode.toml | Sys4AI validate-system-layers | implementation_initialization | controlled | pending | pending |
| contract_target_project_config | schemas/contracts/target_project_config.schema.json | 2020-12 | toml | target_project_config | configs/examples/target_project.example.toml | Sys4AI validate-toml-config | implementation_initialization | controlled | pending | pending |
| contract_format_profile_registry_row | schemas/contracts/format_profile_registry_row.schema.json | 2020-12 | csv | format_profile_registry_row | registries/format_profile_registry.csv | Sys4AI validate-format-profiles | implementation_initialization | controlled | pending | pending |
| contract_config_source_registry_row | schemas/contracts/config_source_registry_row.schema.json | 2020-12 | csv | config_source_registry_row | registries/config_source_registry.csv | Sys4AI validate-config-sources | implementation_initialization | controlled | pending | pending |
| contract_control_record_registry_row | schemas/contracts/control_record_registry_row.schema.json | 2020-12 | csv | control_record_registry_row | registries/control_record_registry.csv | Sys4AI validate-control-records | implementation_initialization | controlled | pending | pending |
| contract_validation_contract_registry_row | schemas/contracts/validation_contract_registry_row.schema.json | 2020-12 | csv | validation_contract_registry_row | registries/validation_contract_registry.csv | Sys4AI validate-validation-contract-registry | implementation_initialization | controlled | pending | pending |
| contract_registry_header | schemas/contracts/registry_header.schema.json | 2020-12 | csv | registry_header | registries/*.csv | Sys4AI validate-registry-graph | implementation_initialization | controlled | pending | pending |
| contract_requirement_trace_registry_row | schemas/contracts/requirement_trace_registry_row.schema.json | 2020-12 | csv | requirement_trace_registry_row | registries/requirement_trace_registry.csv | Sys4AI validate-requirement-trace | implementation_initialization | controlled | pending | pending |
| contract_program_state | schemas/contracts/program_state.schema.json | 2020-12 | yaml | program_state | control_records/program_state.yaml | Sys4AI validate-program-state | control_loop | controlled | pending | pending |
| contract_director_decision | schemas/contracts/director_decision.schema.json | 2020-12 | yaml | director_decision | control_records/director_decisions/*.yaml | Sys4AI validate-director-decisions | control_loop | controlled | pending | pending |
| contract_agentjob_v0_2 | schemas/contracts/agentjob_v0_2.schema.json | 2020-12 | yaml | agentjob_v0_2 | control_records/agentjobs/*.yaml | archived-no-active-cli | control_loop | controlled | pending | pending |
| contract_handoff_v0_2 | schemas/contracts/handoff_v0_2.schema.json | 2020-12 | yaml | handoff_v0_2 | control_records/handoffs/*.yaml | Sys4AI validate-handoffs | control_loop | controlled | pending | pending |
| contract_completion_receipt_v0_2 | schemas/contracts/completion_receipt_v0_2.schema.json | 2020-12 | yaml | completion_receipt_v0_2 | control_records/completions/*.yaml | Sys4AI validate-completion-receipts | control_loop | controlled | pending | pending |
| contract_memory_preflight_receipt | schemas/contracts/memory_preflight_receipt.schema.json | 2020-12 | yaml | memory_preflight_receipt | control_records/memory_preflights/*.yaml | Sys4AI validate-memory-preflight | control_loop | controlled | pending | pending |
| contract_agentjob_registry_row | schemas/contracts/agentjob_registry_row.schema.json | 2020-12 | csv | agentjob_registry_row | registries/agentjob_registry.csv | archived-no-active-cli | control_loop | controlled | pending | pending |
| contract_director_decision_registry_row | schemas/contracts/director_decision_registry_row.schema.json | 2020-12 | csv | director_decision_registry_row | registries/director_decision_registry.csv | Sys4AI validate-director-decision-registry | control_loop | controlled | pending | pending |
| contract_handoff_registry_row | schemas/contracts/handoff_registry_row.schema.json | 2020-12 | csv | handoff_registry_row | registries/handoff_registry.csv | Sys4AI validate-handoff-registry | control_loop | controlled | pending | pending |
| contract_completion_receipt_registry_row | schemas/contracts/completion_receipt_registry_row.schema.json | 2020-12 | csv | completion_receipt_registry_row | registries/completion_receipt_registry.csv | Sys4AI validate-completion-receipt-registry | control_loop | controlled | pending | pending |
| contract_memory_preflight_receipt_registry_row | schemas/contracts/memory_preflight_receipt_registry_row.schema.json | 2020-12 | csv | memory_preflight_receipt_registry_row | registries/memory_preflight_receipt_registry.csv | Sys4AI validate-memory-preflight-registry | control_loop | controlled | pending | pending |
| contract_system_layer_registry_row | schemas/contracts/system_layer_registry_row.schema.json | 2020-12 | csv | system_layer_registry_row | registries/system_layer_registry.csv | Sys4AI validate-system-layers | implementation_initialization | controlled | pending | pending |
| contract_discovery_record_registry_row | schemas/contracts/discovery_record_registry_row.schema.json | 2020-12 | csv | discovery_record_registry_row | registries/discovery_record_registry.csv | Sys4AI validate-discovery-records | implementation_initialization | controlled | pending | pending |
| contract_role_registry_row | schemas/contracts/role_registry_row.schema.json | 2020-12 | csv | role_registry_row | registries/role_registry.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending |
| contract_role_skill_crosswalk_row | schemas/contracts/role_skill_crosswalk_row.schema.json | 2020-12 | csv | role_skill_crosswalk_row | registries/role_skill_crosswalk.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending |
| contract_role_execution_binding_registry_row | schemas/contracts/role_execution_binding_registry_row.schema.json | 2020-12 | csv | role_execution_binding_registry_row | registries/role_execution_binding_registry.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending |
| contract_artifact_contract_registry_row | schemas/contracts/artifact_contract_registry_row.schema.json | 2020-12 | csv | artifact_contract_registry_row | registries/artifact_contract_registry.csv | Sys4AI validate-artifact-contracts | implementation_initialization | controlled | pending | pending |
| contract_core_skill_proposal_registry_row | schemas/contracts/core_skill_proposal_registry_row.schema.json | 2020-12 | csv | core_skill_proposal_registry_row | registries/core_skill_proposal_registry.csv | Sys4AI validate-core-skill-proposals | implementation_initialization | controlled | pending | pending |
| contract_skill_lifecycle_status_registry_row | schemas/contracts/skill_lifecycle_status_registry_row.schema.json | 2020-12 | csv | skill_lifecycle_status_registry_row | registries/skill_lifecycle_status_registry.csv | Sys4AI validate-skill-lifecycle | implementation_initialization | controlled | pending | pending |
| contract_prd_module_registry_row | schemas/contracts/prd_module_registry_row.schema.json | 2020-12 | csv | prd_module_registry_row | registries/prd_module_registry.csv | Sys4AI validate-prd-modules | requirements_manager | controlled | pending | pending |
| contract_strategic_intent_common | schemas/contracts/strategic_intent_common.schema.json | 2020-12 | json | strategic_intent_shared_metadata | schemas/contracts/target_vision_statement.schema.json;schemas/contracts/target_core_values.schema.json | Sys4AI validate-jsonschema-contracts | verification_engineer | controlled | pending | pending |
| contract_target_vision_statement | schemas/contracts/target_vision_statement.schema.json | 2020-12 | markdown | target_vision_statement | templates/governance/target-vision-statement-template.md;examples/strategic_intent/*/vision-statement.md | Sys4AI validate-strategic-intent | verification_engineer | controlled | pending | pending |
| contract_target_core_values | schemas/contracts/target_core_values.schema.json | 2020-12 | markdown | target_core_values | templates/governance/target-core-values-template.md;examples/strategic_intent/*/core-values.md | Sys4AI validate-strategic-intent | verification_engineer | controlled | pending | pending |
| contract_host_capability_profile | schemas/contracts/host_capability_profile.schema.json | 2020-12 | toml | host_capability_profile | configs/host_profiles/*.toml | Sys4AI validate-host-capability-profiles | verification_engineer | controlled | pending | pending |

## Known Limitations

Validators listed here check declared structure and registered paths. They do not replace source review, semantic review, or human approval gates.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
