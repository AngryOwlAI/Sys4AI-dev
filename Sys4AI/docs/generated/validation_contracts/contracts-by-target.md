> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_validation_contracts_by_target
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
    - contract_execution_transaction
    - contract_capability_migration_manifest
    - contract_memory_preflight_receipt_v0_1
    - contract_completion_receipt_v1_0
    - contract_handoff_v1_0
    - contract_target_system_package_manifest
    - contract_self_change_safety_evaluation
    - contract_self_change_holdout_suite
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivatives.validation_contracts_catalog:0.1.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Contracts By Target

Contracts grouped by target format and artifact class.

## Structural Versus Semantic Warning

Validation contracts prove structural conformance only. They do not prove semantic truth, product correctness, or implementation completeness.

## csv / agentjob_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_agentjob_registry_row | schemas/contracts/agentjob_registry_row.schema.json | 2020-12 | csv | agentjob_registry_row | registries/agentjob_registry.csv | archived-no-active-cli | control_loop | historical | pending | pending |

## csv / artifact_contract_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_artifact_contract_registry_row | schemas/contracts/artifact_contract_registry_row.schema.json | 2020-12 | csv | artifact_contract_registry_row | registries/artifact_contract_registry.csv | Sys4AI validate-artifact-contracts | implementation_initialization | controlled | pending | pending |

## csv / completion_receipt_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_completion_receipt_registry_row | schemas/contracts/completion_receipt_registry_row.schema.json | 2020-12 | csv | completion_receipt_registry_row | registries/completion_receipt_registry.csv | Sys4AI validate-completion-receipt-registry | control_loop | controlled | pending | pending |

## csv / config_source_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_config_source_registry_row | schemas/contracts/config_source_registry_row.schema.json | 2020-12 | csv | config_source_registry_row | registries/config_source_registry.csv | Sys4AI validate-config-sources | implementation_initialization | controlled | pending | pending |

## csv / control_record_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_control_record_registry_row | schemas/contracts/control_record_registry_row.schema.json | 2020-12 | csv | control_record_registry_row | registries/control_record_registry.csv | Sys4AI validate-control-records | implementation_initialization | controlled | pending | pending |

## csv / core_skill_proposal_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_core_skill_proposal_registry_row | schemas/contracts/core_skill_proposal_registry_row.schema.json | 2020-12 | csv | core_skill_proposal_registry_row | registries/core_skill_proposal_registry.csv | Sys4AI validate-core-skill-proposals | implementation_initialization | controlled | pending | pending |

## csv / director_decision_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_director_decision_registry_row | schemas/contracts/director_decision_registry_row.schema.json | 2020-12 | csv | director_decision_registry_row | registries/director_decision_registry.csv | Sys4AI validate-director-decision-registry | control_loop | controlled | pending | pending |

## csv / discovery_record_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_discovery_record_registry_row | schemas/contracts/discovery_record_registry_row.schema.json | 2020-12 | csv | discovery_record_registry_row | registries/discovery_record_registry.csv | Sys4AI validate-discovery-records | implementation_initialization | controlled | pending | pending |

## csv / format_profile_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_format_profile_registry_row | schemas/contracts/format_profile_registry_row.schema.json | 2020-12 | csv | format_profile_registry_row | registries/format_profile_registry.csv | Sys4AI validate-format-profiles | implementation_initialization | controlled | pending | pending |

## csv / handoff_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_handoff_registry_row | schemas/contracts/handoff_registry_row.schema.json | 2020-12 | csv | handoff_registry_row | registries/handoff_registry.csv | Sys4AI validate-handoff-registry | control_loop | controlled | pending | pending |

## csv / memory_preflight_receipt_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_memory_preflight_receipt_registry_row | schemas/contracts/memory_preflight_receipt_registry_row.schema.json | 2020-12 | csv | memory_preflight_receipt_registry_row | registries/memory_preflight_receipt_registry.csv | Sys4AI validate-memory-preflight-registry | control_loop | controlled | pending | pending |

## csv / prd_module_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_prd_module_registry_row | schemas/contracts/prd_module_registry_row.schema.json | 2020-12 | csv | prd_module_registry_row | registries/prd_module_registry.csv | Sys4AI validate-prd-modules | requirements_manager | controlled | pending | pending |

## csv / registry_header

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_registry_header | schemas/contracts/registry_header.schema.json | 2020-12 | csv | registry_header | registries/*.csv | Sys4AI validate-registry-graph | implementation_initialization | controlled | pending | pending |

## csv / requirement_trace_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_requirement_trace_registry_row | schemas/contracts/requirement_trace_registry_row.schema.json | 2020-12 | csv | requirement_trace_registry_row | registries/requirement_trace_registry.csv | Sys4AI validate-requirement-trace;Sys4AI validate-requirement-trace-migration | implementation_initialization | controlled | pending | pending |

## csv / role_execution_binding_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_role_execution_binding_registry_row | schemas/contracts/role_execution_binding_registry_row.schema.json | 2020-12 | csv | role_execution_binding_registry_row | registries/role_execution_binding_registry.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending |

## csv / role_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_role_registry_row | schemas/contracts/role_registry_row.schema.json | 2020-12 | csv | role_registry_row | registries/role_registry.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending |

## csv / role_skill_crosswalk_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_role_skill_crosswalk_row | schemas/contracts/role_skill_crosswalk_row.schema.json | 2020-12 | csv | role_skill_crosswalk_row | registries/role_skill_crosswalk.csv | Sys4AI validate-roles | implementation_initialization | controlled | pending | pending |

## csv / skill_lifecycle_status_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_skill_lifecycle_status_registry_row | schemas/contracts/skill_lifecycle_status_registry_row.schema.json | 2020-12 | csv | skill_lifecycle_status_registry_row | registries/skill_lifecycle_status_registry.csv | Sys4AI validate-skill-lifecycle | implementation_initialization | controlled | pending | pending |

## csv / system_layer_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_system_layer_registry_row | schemas/contracts/system_layer_registry_row.schema.json | 2020-12 | csv | system_layer_registry_row | registries/system_layer_registry.csv | Sys4AI validate-system-layers | implementation_initialization | controlled | pending | pending |

## csv / validation_contract_registry_row

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_validation_contract_registry_row | schemas/contracts/validation_contract_registry_row.schema.json | 2020-12 | csv | validation_contract_registry_row | registries/validation_contract_registry.csv | Sys4AI validate-validation-contract-registry | implementation_initialization | controlled | pending | pending |

## json / strategic_intent_shared_metadata

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_strategic_intent_common | schemas/contracts/strategic_intent_common.schema.json | 2020-12 | json | strategic_intent_shared_metadata | schemas/contracts/target_vision_statement.schema.json;schemas/contracts/target_core_values.schema.json | Sys4AI validate-jsonschema-contracts | verification_engineer | controlled | pending | pending |

## markdown / target_core_values

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_target_core_values | schemas/contracts/target_core_values.schema.json | 2020-12 | markdown | target_core_values | templates/governance/target-core-values-template.md;examples/strategic_intent/*/core-values.md | Sys4AI validate-strategic-intent | verification_engineer | controlled | pending | pending |

## markdown / target_vision_statement

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_target_vision_statement | schemas/contracts/target_vision_statement.schema.json | 2020-12 | markdown | target_vision_statement | templates/governance/target-vision-statement-template.md;examples/strategic_intent/*/vision-statement.md | Sys4AI validate-strategic-intent | verification_engineer | controlled | pending | pending |

## toml / capability_migration_manifest

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_capability_migration_manifest | schemas/contracts/capability_migration.schema.json | 2020-12 | toml | capability_migration_manifest | configs/capability_migration.toml | Sys4AI validate-capability-migration | baseline_change_manager | controlled | pending | pending |

## toml / framework_config

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_sys4ai_config | schemas/contracts/sys4ai_config.schema.json | 2020-12 | toml | framework_config | pyproject.toml;configs/examples/sys4ai.example.toml | Sys4AI validate-toml-config | implementation_initialization | controlled | pending | pending |

## toml / host_capability_profile

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_host_capability_profile | schemas/contracts/host_capability_profile.schema.json | 2020-12 | toml | host_capability_profile | configs/host_profiles/*.toml | Sys4AI validate-host-capability-profiles | verification_engineer | controlled | pending | pending |

## toml / self_hosting_mode

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_self_hosting_mode | schemas/contracts/self_hosting_mode.schema.json | 2020-12 | toml | self_hosting_mode | configs/self_hosting_mode.toml | Sys4AI validate-system-layers | implementation_initialization | controlled | pending | pending |

## toml / target_project_config

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_target_project_config | schemas/contracts/target_project_config.schema.json | 2020-12 | toml | target_project_config | configs/examples/target_project.example.toml | Sys4AI validate-toml-config | implementation_initialization | controlled | pending | pending |

## yaml / agentjob

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_agentjob | schemas/contracts/agentjob.schema.json | 2020-12 | yaml | agentjob | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending |

## yaml / agentjob_v0_2

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_agentjob_v0_2 | schemas/contracts/agentjob_v0_2.schema.json | 2020-12 | yaml | agentjob_v0_2 | control_records/agentjobs/*.yaml | archived-no-active-cli | control_loop | historical | pending | pending |

## yaml / completion_receipt

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_completion_receipt | schemas/contracts/completion_receipt.schema.json | 2020-12 | yaml | completion_receipt | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending |
| contract_completion_receipt_v1_0 | schemas/contracts/completion_receipt_v1_0.schema.json | 2020-12 | yaml | completion_receipt | control_records/completions/*.yaml | Sys4AI validate-completion-receipts | verification_engineer | controlled | pending | pending |

## yaml / completion_receipt_v0_2

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_completion_receipt_v0_2 | schemas/contracts/completion_receipt_v0_2.schema.json | 2020-12 | yaml | completion_receipt_v0_2 | control_records/completions/*.yaml | Sys4AI validate-completion-receipts | control_loop | historical | pending | pending |

## yaml / director_decision

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_director_decision | schemas/contracts/director_decision.schema.json | 2020-12 | yaml | director_decision | control_records/director_decisions/*.yaml | Sys4AI validate-director-decisions | control_loop | controlled | pending | pending |

## yaml / execution_transaction

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_execution_transaction | schemas/contracts/execution_transaction.schema.json | 2020-12 | yaml | execution_transaction | templates/project/execution-transaction-template.yaml;control_records/execution_transactions/*.yaml | .venv/bin/python -m unittest discover -s tests -p test_execution_transactions.py | verification_engineer | controlled | pending | pending |

## yaml / handoff

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_handoff | schemas/contracts/handoff.schema.json | 2020-12 | yaml | handoff | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending |
| contract_handoff_v1_0 | schemas/contracts/handoff_v1_0.schema.json | 2020-12 | yaml | handoff | control_records/handoffs/*.yaml | Sys4AI validate-handoffs | bounded_execution_planner | controlled | pending | pending |

## yaml / handoff_v0_2

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_handoff_v0_2 | schemas/contracts/handoff_v0_2.schema.json | 2020-12 | yaml | handoff_v0_2 | control_records/handoffs/*.yaml | Sys4AI validate-handoffs | control_loop | historical | pending | pending |

## yaml / historical_memory_preflight_receipt

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_memory_preflight_receipt_v0_1 | schemas/contracts/memory_preflight_receipt_v0_1.schema.json | 2020-12 | yaml | historical_memory_preflight_receipt | control_records/memory_preflights/*.yaml | Sys4AI validate-memory-preflight | source_first_memory | historical | pending | pending |

## yaml / memory_preflight_receipt

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_memory_preflight_receipt | schemas/contracts/memory_preflight_receipt.schema.json | 2020-12 | yaml | memory_preflight_receipt | control_records/memory_preflights/*.yaml | Sys4AI validate-memory-preflight | control_loop | controlled | pending | pending |

## yaml / program_state

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_program_state | schemas/contracts/program_state.schema.json | 2020-12 | yaml | program_state | control_records/program_state.yaml | Sys4AI validate-program-state | control_loop | controlled | pending | pending |

## yaml / self_change_holdout_suite

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_self_change_holdout_suite | schemas/contracts/self_change_holdout_suite.schema.json | 2020-12 | yaml | self_change_holdout_suite | assurance/holdouts/*.yaml | Sys4AI validate-safety-evaluation | verification_engineer | controlled | pending | pending |

## yaml / self_change_safety_evaluation

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_self_change_safety_evaluation | schemas/contracts/self_change_safety_evaluation.schema.json | 2020-12 | yaml | self_change_safety_evaluation | assurance/meta_agent_self_change_safety_evaluation.yaml | Sys4AI validate-safety-evaluation | verification_engineer | controlled | pending | pending |

## yaml / state_snapshot

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_state_snapshot | schemas/contracts/state_snapshot.schema.json | 2020-12 | yaml | state_snapshot | control_records/**/*.yaml | Sys4AI validate-jsonschema-contracts | implementation_initialization | historical | pending | pending |

## yaml / target_system_package_manifest

| contract_id | path | dialect | target_format | target_artifact_type | target_glob | validator_command | owner | authority_status | supersedes | source_hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_target_system_package_manifest | schemas/contracts/target_system_package_manifest.schema.json | 2020-12 | yaml | target_system_package_manifest | examples/target_systems/*/target-system-manifest.yaml | Sys4AI target-package validate | verification_engineer | controlled | pending | pending |

## Known Limitations

Target groups are derived from registry rows. A row with stale metadata can mislead this page until the registry is corrected.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
