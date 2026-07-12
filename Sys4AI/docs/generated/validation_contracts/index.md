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
    - registries/artifact_contract_registry.csv
    - registries/config_source_registry.csv
    - registries/control_record_registry.csv
  format_profile_ids:
    - fmt_jsonschema_contract
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
    - contract_execution_transaction
    - contract_capability_migration_manifest
    - contract_memory_preflight_receipt_v0_1
    - contract_completion_receipt_v1_0
    - contract_handoff_v1_0
    - contract_target_system_package_manifest
    - contract_self_change_safety_evaluation
    - contract_self_change_holdout_suite
    - contract_evidence_closure_plan_registry_row
    - contract_local_evidence_execution_registry_row
    - contract_plan_scope_interpretation_registry_row
    - contract_skill_import_manifest
    - contract_registry_definition_registry_row
    - contract_strategic_vision_measurement
  generated_at: 2026-07-12T14:24:41Z
  generator: sys_for_ai.derivatives.validation_contracts_catalog:0.2.0
  validation_status: generated_content_checked
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Validation Contracts Catalog

This generated page indexes executable validation contracts. It is a reader catalog, not a contract authority.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_validation_contracts_index | docs/generated/validation_contracts/index.md | SRC-REG-VALIDATION-CONTRACTS;SRC-REG-ARTIFACT-CONTRACTS;SRC-REG-CONFIG-SOURCES;SRC-REG-CONTROL-RECORDS;SRC-REG-FORMAT-PROFILES | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | generated_derivative |
| der_validation_contracts_by_target | docs/generated/validation_contracts/contracts-by-target.md | SRC-REG-VALIDATION-CONTRACTS;SRC-REG-ARTIFACT-CONTRACTS;SRC-REG-CONFIG-SOURCES;SRC-REG-CONTROL-RECORDS;SRC-REG-FORMAT-PROFILES | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | generated_derivative |

## Structural Versus Semantic Warning

Validation contracts prove structural conformance only. They do not prove semantic truth, product correctness, or implementation completeness.

## Contract Rows

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash | generator_version | generation_timestamp | stale_or_orphan_status | known_limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_agentjob | schemas/contracts/agentjob.schema.json | 2020-12 | yaml | agentjob | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_handoff | schemas/contracts/handoff.schema.json | 2020-12 | yaml | handoff | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_completion_receipt | schemas/contracts/completion_receipt.schema.json | 2020-12 | yaml | completion_receipt | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_state_snapshot | schemas/contracts/state_snapshot.schema.json | 2020-12 | yaml | state_snapshot | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_sys4ai_config | schemas/contracts/sys4ai_config.schema.json | 2020-12 | toml | framework_config | pyproject.toml;configs/examples/sys4ai.example.toml | Sys4AI validate-toml-config | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_self_hosting_mode | schemas/contracts/self_hosting_mode.schema.json | 2020-12 | toml | self_hosting_mode | configs/self_hosting_mode.toml | Sys4AI validate-system-layers | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_target_project_config | schemas/contracts/target_project_config.schema.json | 2020-12 | toml | target_project_config | configs/examples/target_project.example.toml | Sys4AI validate-toml-config | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_format_profile_registry_row | schemas/contracts/format_profile_registry_row.schema.json | 2020-12 | csv | format_profile_registry_row | registries/format_profile_registry.csv | Sys4AI validate-format-profiles | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_config_source_registry_row | schemas/contracts/config_source_registry_row.schema.json | 2020-12 | csv | config_source_registry_row | registries/config_source_registry.csv | Sys4AI validate-config-sources | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_control_record_registry_row | schemas/contracts/control_record_registry_row.schema.json | 2020-12 | csv | control_record_registry_row | registries/control_record_registry.csv | Sys4AI validate-control-records | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_validation_contract_registry_row | schemas/contracts/validation_contract_registry_row.schema.json | 2020-12 | csv | validation_contract_registry_row | registries/validation_contract_registry.csv | Sys4AI validate-validation-contract-registry | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_registry_header | schemas/contracts/registry_header.schema.json | 2020-12 | csv | registry_header | registries/*.csv | Sys4AI validate-registry-graph | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_requirement_trace_registry_row | schemas/contracts/requirement_trace_registry_row.schema.json | 2020-12 | csv | requirement_trace_registry_row | registries/requirement_trace_registry.csv | Sys4AI validate-requirement-trace;Sys4AI validate-requirement-trace-migration | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_program_state | schemas/contracts/program_state.schema.json | 2020-12 | yaml | program_state | control_records/program_state.yaml | Sys4AI validate-program-state | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_director_decision | schemas/contracts/director_decision.schema.json | 2020-12 | yaml | director_decision | control_records/director_decisions/*.yaml | Sys4AI validate-director-decisions | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_agentjob_v0_2 | schemas/contracts/agentjob_v0_2.schema.json | 2020-12 | yaml | agentjob_v0_2 | control_records/agentjobs/*.yaml | archived-no-active-cli | control_loop | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_handoff_v0_2 | schemas/contracts/handoff_v0_2.schema.json | 2020-12 | yaml | handoff_v0_2 | control_records/handoffs/*.yaml | Sys4AI validate-handoffs | control_loop | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_completion_receipt_v0_2 | schemas/contracts/completion_receipt_v0_2.schema.json | 2020-12 | yaml | completion_receipt_v0_2 | control_records/completions/*.yaml | Sys4AI validate-completion-receipts | control_loop | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_memory_preflight_receipt | schemas/contracts/memory_preflight_receipt.schema.json | 2020-12 | yaml | memory_preflight_receipt | control_records/memory_preflights/*.yaml | Sys4AI validate-memory-preflight | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_agentjob_registry_row | schemas/contracts/agentjob_registry_row.schema.json | 2020-12 | csv | agentjob_registry_row | registries/agentjob_registry.csv | archived-no-active-cli | control_loop | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_director_decision_registry_row | schemas/contracts/director_decision_registry_row.schema.json | 2020-12 | csv | director_decision_registry_row | registries/director_decision_registry.csv | Sys4AI validate-director-decision-registry | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_handoff_registry_row | schemas/contracts/handoff_registry_row.schema.json | 2020-12 | csv | handoff_registry_row | registries/handoff_registry.csv | Sys4AI validate-handoff-registry | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_completion_receipt_registry_row | schemas/contracts/completion_receipt_registry_row.schema.json | 2020-12 | csv | completion_receipt_registry_row | registries/completion_receipt_registry.csv | Sys4AI validate-completion-receipt-registry | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_memory_preflight_receipt_registry_row | schemas/contracts/memory_preflight_receipt_registry_row.schema.json | 2020-12 | csv | memory_preflight_receipt_registry_row | registries/memory_preflight_receipt_registry.csv | Sys4AI validate-memory-preflight-registry | control_loop | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_system_layer_registry_row | schemas/contracts/system_layer_registry_row.schema.json | 2020-12 | csv | system_layer_registry_row | registries/system_layer_registry.csv | Sys4AI validate-system-layers | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_discovery_record_registry_row | schemas/contracts/discovery_record_registry_row.schema.json | 2020-12 | csv | discovery_record_registry_row | registries/discovery_record_registry.csv | Sys4AI validate-discovery-records | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_role_registry_row | schemas/contracts/role_registry_row.schema.json | 2020-12 | csv | role_registry_row | registries/role_registry.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_role_skill_crosswalk_row | schemas/contracts/role_skill_crosswalk_row.schema.json | 2020-12 | csv | role_skill_crosswalk_row | registries/role_skill_crosswalk.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_role_execution_binding_registry_row | schemas/contracts/role_execution_binding_registry_row.schema.json | 2020-12 | csv | role_execution_binding_registry_row | registries/role_execution_binding_registry.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_artifact_contract_registry_row | schemas/contracts/artifact_contract_registry_row.schema.json | 2020-12 | csv | artifact_contract_registry_row | registries/artifact_contract_registry.csv | Sys4AI validate-artifact-contracts | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_core_skill_proposal_registry_row | schemas/contracts/core_skill_proposal_registry_row.schema.json | 2020-12 | csv | core_skill_proposal_registry_row | registries/core_skill_proposal_registry.csv | Sys4AI validate-core-skill-proposals | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_skill_lifecycle_status_registry_row | schemas/contracts/skill_lifecycle_status_registry_row.schema.json | 2020-12 | csv | skill_lifecycle_status_registry_row | registries/skill_lifecycle_status_registry.csv | Sys4AI validate-skill-lifecycle | implementation_initialization | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_prd_module_registry_row | schemas/contracts/prd_module_registry_row.schema.json | 2020-12 | csv | prd_module_registry_row | registries/prd_module_registry.csv | Sys4AI validate-prd-modules | requirements_manager | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_strategic_intent_common | schemas/contracts/strategic_intent_common.schema.json | 2020-12 | json | strategic_intent_shared_metadata | schemas/contracts/target_vision_statement.schema.json;schemas/contracts/target_core_values.schema.json | Sys4AI validate-jsonschema-contracts | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_target_vision_statement | schemas/contracts/target_vision_statement.schema.json | 2020-12 | markdown | target_vision_statement | templates/governance/target-vision-statement-template.md;examples/strategic_intent/*/vision-statement.md | Sys4AI validate-strategic-intent | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_target_core_values | schemas/contracts/target_core_values.schema.json | 2020-12 | markdown | target_core_values | templates/governance/target-core-values-template.md;examples/strategic_intent/*/core-values.md | Sys4AI validate-strategic-intent | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_host_capability_profile | schemas/contracts/host_capability_profile.schema.json | 2020-12 | toml | host_capability_profile | configs/host_profiles/*.toml | Sys4AI validate-host-capability-profiles | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_execution_transaction | schemas/contracts/execution_transaction.schema.json | 2020-12 | yaml | execution_transaction | templates/project/execution-transaction-template.yaml;control_records/execution_transactions/*.yaml | .venv/bin/python -m unittest discover -s tests -p test_execution_transactions.py | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_capability_migration_manifest | schemas/contracts/capability_migration.schema.json | 2020-12 | toml | capability_migration_manifest | configs/capability_migration.toml | Sys4AI validate-capability-migration | baseline_change_manager | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_memory_preflight_receipt_v0_1 | schemas/contracts/memory_preflight_receipt_v0_1.schema.json | 2020-12 | yaml | historical_memory_preflight_receipt | control_records/memory_preflights/*.yaml | Sys4AI validate-memory-preflight | source_first_memory | historical | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_completion_receipt_v1_0 | schemas/contracts/completion_receipt_v1_0.schema.json | 2020-12 | yaml | completion_receipt | control_records/completions/*.yaml | Sys4AI validate-completion-receipts | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_handoff_v1_0 | schemas/contracts/handoff_v1_0.schema.json | 2020-12 | yaml | handoff | control_records/handoffs/*.yaml | Sys4AI validate-handoffs | bounded_execution_planner | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_target_system_package_manifest | schemas/contracts/target_system_package_manifest.schema.json | 2020-12 | yaml | target_system_package_manifest | examples/target_systems/*/target-system-manifest.yaml | Sys4AI target-package validate | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_self_change_safety_evaluation | schemas/contracts/self_change_safety_evaluation.schema.json | 2020-12 | yaml | self_change_safety_evaluation | assurance/meta_agent_self_change_safety_evaluation.yaml | Sys4AI validate-safety-evaluation | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_self_change_holdout_suite | schemas/contracts/self_change_holdout_suite.schema.json | 2020-12 | yaml | self_change_holdout_suite | assurance/holdouts/*.yaml | Sys4AI validate-safety-evaluation | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_evidence_closure_plan_registry_row | schemas/contracts/evidence_closure_plan_registry_row.schema.json | 2020-12 | csv | evidence_closure_plan_registry_row | registries/evidence_closure_plan_registry.csv | Sys4AI validate-evidence-closure-plan | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_local_evidence_execution_registry_row | schemas/contracts/local_evidence_execution_registry_row.schema.json | 2020-12 | csv | local_evidence_execution_registry_row | registries/local_evidence_execution_registry.csv | Sys4AI validate-local-evidence-execution | requirements_verifier | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_plan_scope_interpretation_registry_row | schemas/contracts/plan_scope_interpretation_registry_row.schema.json | 2020-12 | csv | plan_scope_interpretation_registry_row | registries/plan_scope_interpretation_registry.csv | Sys4AI validate-plan-interpretation | system_director | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_skill_import_manifest | schemas/contracts/skill_import_manifest.schema.json | 2020-12 | yaml | skill_import_manifest | control_records/examples/skill_import_manifest.yaml | Sys4AI validate-yaml-control-surface | skill_governance | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_registry_definition_registry_row | schemas/contracts/registry_definition_registry_row.schema.json | 2020-12 | csv | registry_definition_registry_row | registries/registry_definition_registry.csv | Sys4AI validate-csv-registry-surface | registry_governance | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |
| contract_strategic_vision_measurement | schemas/contracts/strategic_vision_measurement.schema.json | 2020-12 | yaml | strategic_vision_measurement | assurance/strategic_vision_measurement_tx35.yaml | Sys4AI validate-strategic-metrics | verification_engineer | controlled | pending | pending | sys_for_ai.derivatives.validation_contracts_catalog:0.2.0 | 2026-07-12T14:24:41Z | current | structural conformance only; semantic and acceptance review remain separate |

## Declaring Artifact And Registry Rows

| contract_id | declaring_registry | registry_row_id | source_or_pattern | artifact_type |
| --- | --- | --- | --- | --- |
| contract_agentjob | registries/control_record_registry.csv | ctrl_codex_metrics_agentjob | control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml | agentjob |
| contract_agentjob | registries/control_record_registry.csv | ctrl_phase1_smoke_agentjob | control_records/examples/phase1_smoke_agentjob.yaml | agentjob |
| contract_agentjob | registries/control_record_registry.csv | ctrl_skill_sync_agentjob | control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml | agentjob |
| contract_agentjob | registries/control_record_registry.csv | ctrl_system_definition_template_agentjob | control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml | agentjob |
| contract_agentjob_v0_2 | registries/artifact_contract_registry.csv | artifact_agentjob | control_records/agentjobs/*.yaml | AgentJob |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_boundary_validators_agentjob | control_records/agentjobs/AJ-P1-BOUNDARY-VALIDATORS-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_continue_skills_agentjob | control_records/agentjobs/AJ-P1-CONTINUE-SKILLS-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_core_skills_batch_1_agentjob | control_records/agentjobs/AJ-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_core_skills_batch_2_agentjob | control_records/agentjobs/AJ-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_derivative_generators_agentjob | control_records/agentjobs/AJ-P1-DERIVATIVE-GENERATORS-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_agentjob | control_records/agentjobs/AJ-SFADEV-03-DISCOVERY-GATE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_smoke_agentjob | control_records/agentjobs/AJ-P1-DISCOVERY-GATE-SMOKE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_smoke_closeout_agentjob | control_records/agentjobs/AJ-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_end_to_end_acceptance_agentjob | control_records/agentjobs/AJ-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_generated_docs_agentjob | control_records/agentjobs/AJ-SFADEV-09-GENERATED-DOCS-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_init_frontdoor_agentjob | control_records/agentjobs/AJ-SFADEV-11-INIT-FRONTDOOR-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_legacy_pending_reconciliation_agentjob | control_records/agentjobs/AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_next_scope_acceptance_agentjob | control_records/agentjobs/AJ-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_next_scope_selection_agentjob | control_records/agentjobs/AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_plan_agentjob | control_records/agentjobs/AJ-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_prd_agentjob | control_records/agentjobs/AJ-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_rdr_agentjob | control_records/agentjobs/AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_plan_completion_audit_agentjob | control_records/agentjobs/AJ-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_plan_control_agentjob | control_records/agentjobs/AJ-SFADEV-13-PLAN-CONTROL-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_prd_decomposition_strategy_agentjob | control_records/agentjobs/AJ-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_prd_integration_agentjob | control_records/agentjobs/AJ-SFADEV-01-PRD-INTEGRATION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_registry_schema_expansion_agentjob | control_records/agentjobs/AJ-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_role_governance_agentjob | control_records/agentjobs/AJ-SFADEV-04-ROLE-GOVERNANCE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_runtime_skill_reconciliation_agentjob | control_records/agentjobs/AJ-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_selfhost_acceptance_agentjob | control_records/agentjobs/AJ-P1-SELFHOST-ACCEPTANCE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_selfhost_continue_kernel_agentjob | control_records/agentjobs/AJ-P1-SELFHOST-CONTINUE-KERNEL-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_skill_lifecycle_agentjob | control_records/agentjobs/AJ-SFADEV-06-SKILL-LIFECYCLE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_subprd_drafts_agentjob | control_records/agentjobs/AJ-SFADEV-24-SUBPRD-DRAFTS-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_subprd_promotion_agentjob | control_records/agentjobs/AJ-SFADEV-25-SUBPRD-PROMOTION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_sys4ai_name_migration_agentjob | control_records/agentjobs/AJ-SYS4AI-DEV-NAME-MIGRATION-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_target_package_smoke_agentjob | control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_walking_skeleton_demo_agentjob | control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_walking_skeleton_flow_agentjob | control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | agentjob_v0_2 |
| contract_agentjob_v0_2 | registries/control_record_registry.csv | ctrl_ws00_baseline_agentjob | control_records/agentjobs/AJ-SFADEV-WS00-BASELINE-001.yaml | agentjob_v0_2 |
| contract_capability_migration_manifest | registries/config_source_registry.csv | cfg_capability_migration | configs/capability_migration.toml | capability_migration |
| contract_completion_receipt | registries/control_record_registry.csv | ctrl_completion_receipt_example | control_records/examples/completion_receipt.example.yaml | completion_receipt |
| contract_completion_receipt_v0_2 | registries/artifact_contract_registry.csv | artifact_completion_receipt | control_records/completions/*.yaml | CompletionReceipt |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_core_skills_batch_1_completion | control_records/completions/RECEIPT-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_core_skills_batch_2_completion | control_records/completions/RECEIPT-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_completion | control_records/completions/RECEIPT-SFADEV-03-DISCOVERY-GATE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_smoke_completion | control_records/completions/RECEIPT-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_end_to_end_acceptance_completion | control_records/completions/RECEIPT-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_generated_docs_completion | control_records/completions/RECEIPT-SFADEV-09-GENERATED-DOCS-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_init_frontdoor_completion | control_records/completions/RECEIPT-SFADEV-11-INIT-FRONTDOOR-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_legacy_pending_reconciliation_completion | control_records/completions/RECEIPT-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_next_scope_acceptance_completion | control_records/completions/RECEIPT-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_next_scope_selection_completion | control_records/completions/RECEIPT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_plan_completion | control_records/completions/RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_prd_completion | control_records/completions/RECEIPT-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_rdr_completion | control_records/completions/RECEIPT-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_plan_completion_audit_completion | control_records/completions/RECEIPT-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_plan_control_completion | control_records/completions/RECEIPT-SFADEV-13-PLAN-CONTROL-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_prd_decomposition_strategy_completion | control_records/completions/RECEIPT-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_prd_integration_completion | control_records/completions/RECEIPT-SFADEV-01-PRD-INTEGRATION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_registry_schema_expansion_completion | control_records/completions/RECEIPT-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_role_governance_completion | control_records/completions/RECEIPT-SFADEV-04-ROLE-GOVERNANCE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_runtime_skill_reconciliation_completion | control_records/completions/RECEIPT-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_selfhost_acceptance_completion | control_records/completions/RECEIPT-P1-SELFHOST-ACCEPTANCE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_selfhost_continue_kernel_completion | control_records/completions/completion_receipt.example.v0_2.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_skill_lifecycle_completion | control_records/completions/RECEIPT-SFADEV-06-SKILL-LIFECYCLE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_subprd_drafts_completion | control_records/completions/RECEIPT-SFADEV-24-SUBPRD-DRAFTS-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_subprd_promotion_completion | control_records/completions/RECEIPT-SFADEV-25-SUBPRD-PROMOTION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_sys4ai_name_migration_completion | control_records/completions/RECEIPT-SYS4AI-DEV-NAME-MIGRATION-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_target_package_smoke_completion | control_records/completions/RECEIPT-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_walking_skeleton_demo_completion | control_records/completions/RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v0_2 | registries/control_record_registry.csv | ctrl_walking_skeleton_flow_completion | control_records/completions/RECEIPT-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | completion_receipt_v0_2 |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx10_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX10-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx11_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX11-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx12_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX12-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx13_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX13-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx14_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX14-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx15_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX15-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx16_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX16-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx17_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX17-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx18_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX18-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx19_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX19-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx20_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX20-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx21_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX21-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx22_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX22-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx23_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX23-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx24_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX24-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx25_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX25-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx26_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX26-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx27_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX27-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx28_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX28-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx29_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX29-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx30_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX30-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx31_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX31-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx32_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX32-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx33_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX33-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx34_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX34-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx35_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX35-001.yaml | completion_receipt |
| contract_completion_receipt_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx36_completion | control_records/completions/RECEIPT-SFADEV-STRATEGIC-BASELINE-TX36-001.yaml | completion_receipt |
| contract_director_decision | registries/artifact_contract_registry.csv | artifact_director_decision | control_records/director_decisions/*.yaml | DirectorDecision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_core_skills_batch_1_director_decision | control_records/director_decisions/DDR-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_core_skills_batch_2_director_decision | control_records/director_decisions/DDR-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_discovery_gate_director_decision | control_records/director_decisions/DDR-SFADEV-03-DISCOVERY-GATE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_discovery_gate_smoke_director_decision | control_records/director_decisions/DDR-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_end_to_end_acceptance_director_decision | control_records/director_decisions/DDR-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_generated_docs_director_decision | control_records/director_decisions/DDR-SFADEV-09-GENERATED-DOCS-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_init_frontdoor_director_decision | control_records/director_decisions/DDR-SFADEV-11-INIT-FRONTDOOR-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_legacy_pending_reconciliation_director_decision | control_records/director_decisions/DDR-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_next_scope_acceptance_director_decision | control_records/director_decisions/DDR-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_next_scope_selection_director_decision | control_records/director_decisions/DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_plan_director_decision | control_records/director_decisions/DDR-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_prd_director_decision | control_records/director_decisions/DDR-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_rdr_director_decision | control_records/director_decisions/DDR-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_plan_completion_audit_director_decision | control_records/director_decisions/DDR-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_plan_control_director_decision | control_records/director_decisions/DDR-SFADEV-13-PLAN-CONTROL-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_prd_integration_director_decision | control_records/director_decisions/DDR-SFADEV-01-PRD-INTEGRATION-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_registry_schema_expansion_director_decision | control_records/director_decisions/DDR-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_role_governance_director_decision | control_records/director_decisions/DDR-SFADEV-04-ROLE-GOVERNANCE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_selfhost_director_decision | control_records/director_decisions/DDR-P1-SELFHOST-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_skill_lifecycle_director_decision | control_records/director_decisions/DDR-SFADEV-06-SKILL-LIFECYCLE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g03_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G03-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g04_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G04-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g05_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G05-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g07_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G07-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g08_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G08-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g10_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G10-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_cross_version_ci_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-011.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_csv_registry_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-006.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_format_governance_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-005.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_generated_reader_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-010.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_jsonschema_contract_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-009.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_markdown_source_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-007.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_plan_interpretation_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-002.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_python_package_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-003.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_quantitative_acceptance_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-013.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_quantitative_measurement_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-012.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_toml_config_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-008.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_strategic_baseline_g11_yaml_control_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G11-004.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_subprd_promotion_director_decision | control_records/director_decisions/DDR-SFADEV-25-SUBPRD-PROMOTION-001.yaml | director_decision |
| contract_director_decision | registries/control_record_registry.csv | ctrl_sys4ai_name_migration_director_decision | control_records/director_decisions/DDR-SYS4AI-DEV-NAME-MIGRATION-001.yaml | director_decision |
| contract_discovery_record_registry_row | registries/artifact_contract_registry.csv | artifact_rdr | requirements-discovery-record.md | RDR |
| contract_execution_transaction | registries/artifact_contract_registry.csv | artifact_execution_transaction | control_records/execution_transactions/*.yaml | ExecutionTransaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx10_execution_transaction | control_records/execution_transactions/TX-10-ACTIVE-SURFACE-MIGRATION.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx11_execution_transaction | control_records/execution_transactions/TX-11-TRACE-SCHEMA.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx12_execution_transaction | control_records/execution_transactions/TX-12-TRACE-DATA.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx13_execution_transaction | control_records/execution_transactions/TX-13-VALIDATORS.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx14_execution_transaction | control_records/execution_transactions/TX-14-PHASE2.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx15_execution_transaction | control_records/execution_transactions/TX-15-TARGET-PACKAGE.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx16_execution_transaction | control_records/execution_transactions/TX-16-WALKING-SKELETON.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx17_execution_transaction | control_records/execution_transactions/TX-17-SAFETY-EVALUATION.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx18_execution_transaction | control_records/execution_transactions/TX-18-HUMAN-APPROVAL.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx19_execution_transaction | control_records/execution_transactions/TX-19-MODULES.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx20_execution_transaction | control_records/execution_transactions/TX-20-GENERATED-DOCS.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx21_execution_transaction | control_records/execution_transactions/TX-21-FINAL-ACCEPTANCE.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx22_execution_transaction | control_records/execution_transactions/TX-22-G07-HOST-VERIFICATION.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx23_execution_transaction | control_records/execution_transactions/TX-23-EVIDENCE-CLOSURE-PLAN.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx24_execution_transaction | control_records/execution_transactions/TX-24-LOCAL-EVIDENCE-SEMANTIC-REVIEW.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx25_execution_transaction | control_records/execution_transactions/TX-25-PLAN-INTERPRETATION.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx26_execution_transaction | control_records/execution_transactions/TX-26-LOCAL-EVIDENCE-PYTHON-PACKAGE.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx27_execution_transaction | control_records/execution_transactions/TX-27-LOCAL-EVIDENCE-YAML-CONTROL.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx28_execution_transaction | control_records/execution_transactions/TX-28-LOCAL-EVIDENCE-FORMAT-GOVERNANCE.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx29_execution_transaction | control_records/execution_transactions/TX-29-LOCAL-EVIDENCE-CSV-REGISTRY.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx30_execution_transaction | control_records/execution_transactions/TX-30-LOCAL-EVIDENCE-MARKDOWN-SOURCE.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx31_execution_transaction | control_records/execution_transactions/TX-31-LOCAL-EVIDENCE-TOML-CONFIG.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx32_execution_transaction | control_records/execution_transactions/TX-32-LOCAL-EVIDENCE-JSON-SCHEMA.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx33_execution_transaction | control_records/execution_transactions/TX-33-LOCAL-EVIDENCE-GENERATED-READERS.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx34_execution_transaction | control_records/execution_transactions/TX-34-CROSS-VERSION-PYTHON-CI.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx35_execution_transaction | control_records/execution_transactions/TX-35-QUANTITATIVE-STRATEGIC-EVIDENCE.yaml | execution_transaction |
| contract_execution_transaction | registries/control_record_registry.csv | ctrl_strategic_baseline_tx36_execution_transaction | control_records/execution_transactions/TX-36-QUANTITATIVE-STRATEGIC-EVIDENCE-ACCEPTANCE.yaml | execution_transaction |
| contract_handoff | registries/control_record_registry.csv | ctrl_handoff_example | control_records/examples/handoff.example.yaml | handoff |
| contract_handoff_v0_2 | registries/artifact_contract_registry.csv | artifact_handoff | control_records/handoffs/*.yaml | Handoff |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_core_skills_batch_1_handoff | control_records/handoffs/HANDOFF-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_core_skills_batch_2_handoff | control_records/handoffs/HANDOFF-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_handoff | control_records/handoffs/HANDOFF-SFADEV-03-DISCOVERY-GATE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_discovery_gate_smoke_handoff | control_records/handoffs/HANDOFF-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_end_to_end_acceptance_handoff | control_records/handoffs/HANDOFF-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_generated_docs_handoff | control_records/handoffs/HANDOFF-SFADEV-09-GENERATED-DOCS-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_init_frontdoor_handoff | control_records/handoffs/HANDOFF-SFADEV-11-INIT-FRONTDOOR-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_legacy_pending_reconciliation_handoff | control_records/handoffs/HANDOFF-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_next_scope_acceptance_handoff | control_records/handoffs/HANDOFF-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_next_scope_selection_handoff | control_records/handoffs/HANDOFF-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_plan_handoff | control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_prd_handoff | control_records/handoffs/HANDOFF-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_rdr_handoff | control_records/handoffs/HANDOFF-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_plan_completion_audit_handoff | control_records/handoffs/HANDOFF-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_plan_control_handoff | control_records/handoffs/HANDOFF-SFADEV-13-PLAN-CONTROL-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_prd_decomposition_strategy_handoff | control_records/handoffs/HANDOFF-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_prd_integration_handoff | control_records/handoffs/HANDOFF-SFADEV-01-PRD-INTEGRATION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_registry_schema_expansion_handoff | control_records/handoffs/HANDOFF-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_role_governance_handoff | control_records/handoffs/HANDOFF-SFADEV-04-ROLE-GOVERNANCE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_runtime_skill_reconciliation_handoff | control_records/handoffs/HANDOFF-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_selfhost_acceptance_handoff | control_records/handoffs/HANDOFF-P1-SELFHOST-ACCEPTANCE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_selfhost_continue_kernel_handoff | control_records/handoffs/handoff.example.v0_2.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_skill_lifecycle_handoff | control_records/handoffs/HANDOFF-SFADEV-06-SKILL-LIFECYCLE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_subprd_drafts_handoff | control_records/handoffs/HANDOFF-SFADEV-24-SUBPRD-DRAFTS-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_subprd_promotion_handoff | control_records/handoffs/HANDOFF-SFADEV-25-SUBPRD-PROMOTION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_sys4ai_name_migration_handoff | control_records/handoffs/HANDOFF-SYS4AI-DEV-NAME-MIGRATION-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_target_package_smoke_handoff | control_records/handoffs/HANDOFF-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_walking_skeleton_demo_handoff | control_records/handoffs/HANDOFF-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | handoff_v0_2 |
| contract_handoff_v0_2 | registries/control_record_registry.csv | ctrl_walking_skeleton_flow_handoff | control_records/handoffs/HANDOFF-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | handoff_v0_2 |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx10_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX10-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx11_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX11-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx12_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX12-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx13_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX13-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx14_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX14-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx15_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX15-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx16_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX16-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx17_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX17-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx18_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX18-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx19_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX19-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx20_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX20-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx21_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX21-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx22_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX22-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx23_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX23-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx24_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX24-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx25_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX25-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx26_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX26-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx27_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX27-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx28_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX28-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx29_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX29-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx30_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX30-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx31_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX31-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx32_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX32-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx33_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX33-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx34_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX34-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx35_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX35-001.yaml | handoff |
| contract_handoff_v1_0 | registries/control_record_registry.csv | ctrl_strategic_baseline_tx36_handoff | control_records/handoffs/HANDOFF-SFADEV-STRATEGIC-BASELINE-TX36-001.yaml | handoff |
| contract_host_capability_profile | registries/config_source_registry.csv | cfg_codex_app_reference | configs/host_profiles/codex_app_reference.toml | host_capability_profile |
| contract_memory_preflight_receipt | registries/artifact_contract_registry.csv | artifact_memory_preflight | control_records/memory_preflights/*.yaml | MemoryPreflightReceipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx10_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-10-ACTIVE-SURFACE-MIGRATION-20260710T135843Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx11_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-11-TRACE-SCHEMA-20260710T142714Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx12_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-12-TRACE-DATA-20260710T145240Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx13_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-13-VALIDATORS-20260710T151414Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx14_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-14-PHASE2-20260710T155212Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx15_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-15-TARGET-PACKAGE-20260710T165733Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx16_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-16-WALKING-SKELETON-20260710T172717Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx17_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-17-SAFETY-EVALUATION-20260710T175106Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx18_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-18-HUMAN-APPROVAL-20260710T184803Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx19_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-19-MODULES-20260710T193535Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx20_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-20-GENERATED-DOCS-20260711T141224Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx21_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-21-FINAL-ACCEPTANCE-20260711T143842Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx22_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-22-G07-HOST-VERIFICATION-20260711T151753Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx23_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-23-EVIDENCE-CLOSURE-PLAN-20260711T155250Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx24_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-24-LOCAL-EVIDENCE-SEMANTIC-REVIEW-20260711T161917Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx25_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-25-PLAN-INTERPRETATION-20260711T164526Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx26_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-26-LOCAL-EVIDENCE-PYTHON-PACKAGE-20260711T171757Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx27_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-27-LOCAL-EVIDENCE-YAML-CONTROL-20260711T174814Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx28_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-28-LOCAL-EVIDENCE-FORMAT-GOVERNANCE-20260711T181109Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx29_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-29-LOCAL-EVIDENCE-CSV-REGISTRY-20260711T195006Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx30_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-30-LOCAL-EVIDENCE-MARKDOWN-SOURCE-20260712T121134Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx31_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-31-LOCAL-EVIDENCE-TOML-CONFIG-20260712T130256Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx32_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-32-LOCAL-EVIDENCE-JSON-SCHEMA-20260712T132623Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx33_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-33-LOCAL-EVIDENCE-GENERATED-READERS-20260712T142441Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx34_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-34-CROSS-VERSION-PYTHON-CI-20260712T145255Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx35_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-35-QUANTITATIVE-STRATEGIC-EVIDENCE-20260712T153133Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt | registries/control_record_registry.csv | ctrl_strategic_baseline_tx36_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-TX-36-QUANTITATIVE-STRATEGIC-EVIDENCE-ACCEPTANCE-20260712T161021Z.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_core_skills_batch_1_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_core_skills_batch_2_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_discovery_gate_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-03-DISCOVERY-GATE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_discovery_gate_smoke_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_end_to_end_acceptance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_generated_docs_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-09-GENERATED-DOCS-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_init_frontdoor_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-11-INIT-FRONTDOOR-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_legacy_pending_reconciliation_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_memory_preflight_example | control_records/memory_preflights/memory_preflight_receipt.example.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_next_scope_acceptance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_next_scope_selection_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_plan_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_prd_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_phase2_walking_skeleton_rdr_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_plan_completion_audit_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_plan_control_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-13-PLAN-CONTROL-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_prd_decomposition_strategy_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_prd_integration_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-01-PRD-INTEGRATION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_registry_schema_expansion_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_role_governance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-04-ROLE-GOVERNANCE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_runtime_skill_reconciliation_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_selfhost_acceptance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-P1-SELFHOST-ACCEPTANCE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_skill_lifecycle_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-06-SKILL-LIFECYCLE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_subprd_drafts_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-24-SUBPRD-DRAFTS-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_subprd_promotion_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-25-SUBPRD-PROMOTION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_sys4ai_name_migration_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SYS4AI-DEV-NAME-MIGRATION-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_target_package_smoke_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_walking_skeleton_demo_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | memory_preflight_receipt |
| contract_memory_preflight_receipt_v0_1 | registries/control_record_registry.csv | ctrl_walking_skeleton_flow_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | memory_preflight_receipt |
| contract_program_state | registries/control_record_registry.csv | ctrl_program_state | control_records/program_state.yaml | program_state |
| contract_role_registry_row | registries/artifact_contract_registry.csv | artifact_role_registry | registries/role_registry.csv | RoleRegistry |
| contract_self_change_holdout_suite | registries/artifact_contract_registry.csv | artifact_self_change_holdout_suite | assurance/holdouts/*.yaml | SelfChangeHoldoutSuite |
| contract_self_change_safety_evaluation | registries/artifact_contract_registry.csv | artifact_self_change_safety_evaluation_packet | assurance/meta_agent_self_change_safety_evaluation.yaml | SelfChangeSafetyEvaluationPacket |
| contract_self_hosting_mode | registries/config_source_registry.csv | cfg_self_hosting_mode | configs/self_hosting_mode.toml | self_hosting_mode |
| contract_skill_import_manifest | registries/control_record_registry.csv | ctrl_skill_import_manifest | control_records/examples/skill_import_manifest.yaml | skill_import_manifest |
| contract_state_snapshot | registries/control_record_registry.csv | ctrl_selfhost_continue_kernel_state_snapshot | control_records/state_snapshots/state_snapshot.example.v0_2.yaml | state_snapshot |
| contract_state_snapshot | registries/control_record_registry.csv | ctrl_state_snapshot_example | control_records/examples/state_snapshot.example.yaml | state_snapshot |
| contract_strategic_vision_measurement | registries/artifact_contract_registry.csv | artifact_strategic_vision_measurement | assurance/strategic_vision_measurement_tx35.yaml | StrategicVisionMeasurement |
| contract_sys4ai_config | registries/config_source_registry.csv | cfg_pyproject | pyproject.toml | python_package |
| contract_sys4ai_config | registries/config_source_registry.csv | cfg_sys4ai_example | configs/examples/sys4ai.example.toml | framework_example |
| contract_target_core_values | registries/artifact_contract_registry.csv | artifact_target_core_values | governance/core-values.md | TargetCoreValues |
| contract_target_project_config | registries/config_source_registry.csv | cfg_target_project_example | configs/examples/target_project.example.toml | target_project_template |
| contract_target_system_package_manifest | registries/artifact_contract_registry.csv | artifact_target_system_package_manifest | target-system-manifest.yaml | TargetSystemPackageManifest |
| contract_target_vision_statement | registries/artifact_contract_registry.csv | artifact_target_vision | governance/vision-statement.md | TargetVisionStatement |

## Known Limitations

Validators listed here check declared structure and registered paths. They do not replace source review, semantic review, or human approval gates.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
