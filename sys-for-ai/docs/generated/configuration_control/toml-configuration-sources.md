> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_configuration_control_toml
  authority_status: generated_noncanonical
  derivative_type: configuration_control_wiki_page
  source_registries:
    - registries/config_source_registry.csv
    - registries/validation_contract_registry.csv
    - registries/format_profile_registry.csv
  validation_contracts:
    - contract_self_hosting_mode
    - contract_sys_for_ai_config
    - contract_target_project_config
  generated_at: 2026-07-06T00:00:00Z
  generator: sys_for_ai.derivatives.config_control_wiki:0.1.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# TOML Configuration Sources

Registered TOML configuration sources are listed below. Runtime values and secrets are not generated here.

## Configuration Source Rows

| config_id | path | domain | authority_status | owner | validation_contract_id | source_hash |
| --- | --- | --- | --- | --- | --- | --- |
| cfg_pyproject | pyproject.toml | python_package | controlled | implementation_initialization | contract_sys_for_ai_config | pending |
| cfg_self_hosting_mode | configs/self_hosting_mode.toml | self_hosting_mode | controlled | implementation_initialization | contract_self_hosting_mode | pending |
| cfg_sys_for_ai_example | configs/examples/sys_for_ai.example.toml | framework_example | controlled | implementation_initialization | contract_sys_for_ai_config | pending |
| cfg_target_project_example | configs/examples/target_project.example.toml | target_project_template | controlled | implementation_initialization | contract_target_project_config | pending |

## Validation Contract Trace

| contract_id | path | target_format | target_artifact_type | validator_command |
| --- | --- | --- | --- | --- |
| contract_self_hosting_mode | schemas/contracts/self_hosting_mode.schema.json | toml | self_hosting_mode | sys-for-ai validate-system-layers |
| contract_sys_for_ai_config | schemas/contracts/sys_for_ai_config.schema.json | toml | framework_config | sys-for-ai validate-toml-config |
| contract_target_project_config | schemas/contracts/target_project_config.schema.json | toml | target_project_config | sys-for-ai validate-toml-config |

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
