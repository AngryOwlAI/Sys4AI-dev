> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_configuration_control_index
  authority_status: generated_noncanonical
  derivative_type: configuration_control_wiki_page
  source_registries:
    - registries/format_profile_registry.csv
    - registries/config_source_registry.csv
    - registries/control_record_registry.csv
  validation_contracts:
    - contract_agentjob
    - contract_agentjob_v0_2
    - contract_completion_receipt
    - contract_completion_receipt_v0_2
    - contract_director_decision
    - contract_handoff
    - contract_handoff_v0_2
    - contract_memory_preflight_receipt
    - contract_program_state
    - contract_self_hosting_mode
    - contract_state_snapshot
    - contract_sys4ai_config
    - contract_target_project_config
  generated_at: 2026-07-06T00:00:00Z
  generator: sys_for_ai.derivatives.config_control_wiki:0.1.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Configuration And Control Wiki

This generated page indexes registered configuration and control surfaces. It is navigation, not authority.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_configuration_control_index | docs/generated/configuration_control/index.md | SRC-REG-FORMAT-PROFILES;SRC-REG-CONFIG-SOURCES;SRC-REG-CONTROL-RECORDS | sys_for_ai.derivatives.config_control_wiki:0.1.0 | generated_derivative |
| der_configuration_control_yaml | docs/generated/configuration_control/yaml-control-records.md | SRC-REG-CONTROL-RECORDS;SRC-REG-VALIDATION-CONTRACTS | sys_for_ai.derivatives.config_control_wiki:0.1.0 | generated_derivative |
| der_configuration_control_toml | docs/generated/configuration_control/toml-configuration-sources.md | SRC-REG-CONFIG-SOURCES;SRC-REG-VALIDATION-CONTRACTS | sys_for_ai.derivatives.config_control_wiki:0.1.0 | generated_derivative |

## Format Profile IDs

| format_id | extension | family | authority_class | validator_required |
| --- | --- | --- | --- | --- |
| fmt_markdown_source | .md | Markdown | source_document | false |
| fmt_csv_registry | .csv | CSV | registry_row | true |
| fmt_yaml_control | .yaml | YAML | control_record | true |
| fmt_toml_config | .toml | TOML | configuration_source | true |
| fmt_jsonschema_contract | .schema.json | JSON Schema | validation_contract | true |

## Registered Surface Counts

| surface | count | source_path |
| --- | --- | --- |
| format profiles | 5 | registries/format_profile_registry.csv |
| configuration sources | 4 | registries/config_source_registry.csv |
| control records | 136 | registries/control_record_registry.csv |

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
