> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_configuration_control_yaml
  authority_status: generated_noncanonical
  derivative_type: configuration_control_wiki_page
  source_registries:
    - registries/control_record_registry.csv
    - registries/validation_contract_registry.csv
    - registries/format_profile_registry.csv
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
    - contract_state_snapshot
  generated_at: 2026-07-06T00:00:00Z
  generator: sys_for_ai.derivatives.config_control_wiki:0.1.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# YAML Control Records

Registered YAML control records are listed below. Their source files and registry rows remain authoritative.

## Control Record Rows

| control_record_id | path | record_type | authority_status | owner | validation_contract_id | source_hash |
| --- | --- | --- | --- | --- | --- | --- |
| ctrl_phase1_smoke_agentjob | control_records/examples/phase1_smoke_agentjob.yaml | agentjob | controlled | implementation_initialization | contract_agentjob | pending |
| ctrl_skill_sync_agentjob | control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml | agentjob | controlled | skill_governance | contract_agentjob | pending |
| ctrl_codex_metrics_agentjob | control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml | agentjob | controlled | runtime_session_accounting | contract_agentjob | pending |
| ctrl_system_definition_template_agentjob | control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml | agentjob | controlled | system_definition | contract_agentjob | pending |
| ctrl_skill_import_manifest | control_records/examples/skill_import_manifest.yaml | skill_import_manifest | controlled | skill_governance | pending | pending |
| ctrl_handoff_example | control_records/examples/handoff.example.yaml | handoff | controlled | implementation_initialization | contract_handoff | pending |
| ctrl_completion_receipt_example | control_records/examples/completion_receipt.example.yaml | completion_receipt | controlled | implementation_initialization | contract_completion_receipt | pending |
| ctrl_state_snapshot_example | control_records/examples/state_snapshot.example.yaml | state_snapshot | controlled | implementation_initialization | contract_state_snapshot | pending |
| ctrl_program_state | control_records/program_state.yaml | program_state | controlled | control_loop | contract_program_state | pending |
| ctrl_memory_preflight_example | control_records/memory_preflights/memory_preflight_receipt.example.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_selfhost_director_decision | control_records/director_decisions/DDR-P1-SELFHOST-001.yaml | director_decision | controlled | control_loop | contract_director_decision | pending |
| ctrl_selfhost_continue_kernel_agentjob | control_records/agentjobs/AJ-P1-SELFHOST-CONTINUE-KERNEL-001.yaml | agentjob_v0_2 | controlled | control_loop | contract_agentjob_v0_2 | pending |
| ctrl_selfhost_continue_kernel_completion | control_records/completions/completion_receipt.example.v0_2.yaml | completion_receipt_v0_2 | controlled | control_loop | contract_completion_receipt_v0_2 | pending |
| ctrl_selfhost_continue_kernel_handoff | control_records/handoffs/handoff.example.v0_2.yaml | handoff_v0_2 | controlled | control_loop | contract_handoff_v0_2 | pending |
| ctrl_selfhost_continue_kernel_state_snapshot | control_records/state_snapshots/state_snapshot.example.v0_2.yaml | state_snapshot | controlled | control_loop | contract_state_snapshot | pending |
| ctrl_boundary_validators_agentjob | control_records/agentjobs/AJ-P1-BOUNDARY-VALIDATORS-001.yaml | agentjob_v0_2 | controlled | control_loop | contract_agentjob_v0_2 | pending |
| ctrl_derivative_generators_agentjob | control_records/agentjobs/AJ-P1-DERIVATIVE-GENERATORS-001.yaml | agentjob_v0_2 | controlled | control_loop | contract_agentjob_v0_2 | pending |
| ctrl_continue_skills_agentjob | control_records/agentjobs/AJ-P1-CONTINUE-SKILLS-001.yaml | agentjob_v0_2 | controlled | skill_governance | contract_agentjob_v0_2 | pending |
| ctrl_selfhost_acceptance_agentjob | control_records/agentjobs/AJ-P1-SELFHOST-ACCEPTANCE-001.yaml | agentjob_v0_2 | controlled | control_loop | contract_agentjob_v0_2 | pending |
| ctrl_selfhost_acceptance_completion | control_records/completions/RECEIPT-P1-SELFHOST-ACCEPTANCE-001.yaml | completion_receipt_v0_2 | controlled | control_loop | contract_completion_receipt_v0_2 | pending |
| ctrl_selfhost_acceptance_handoff | control_records/handoffs/HANDOFF-P1-SELFHOST-ACCEPTANCE-001.yaml | handoff_v0_2 | controlled | control_loop | contract_handoff_v0_2 | pending |
| ctrl_selfhost_acceptance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-P1-SELFHOST-ACCEPTANCE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_runtime_skill_reconciliation_agentjob | control_records/agentjobs/AJ-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | agentjob_v0_2 | controlled | skill_governance | contract_agentjob_v0_2 | pending |
| ctrl_runtime_skill_reconciliation_completion | control_records/completions/RECEIPT-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | completion_receipt_v0_2 | controlled | skill_governance | contract_completion_receipt_v0_2 | pending |
| ctrl_runtime_skill_reconciliation_handoff | control_records/handoffs/HANDOFF-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | handoff_v0_2 | controlled | skill_governance | contract_handoff_v0_2 | pending |
| ctrl_runtime_skill_reconciliation_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-05-RUNTIME-SKILL-RECONCILIATION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_prd_integration_director_decision | control_records/director_decisions/DDR-SFADEV-01-PRD-INTEGRATION-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_prd_integration_agentjob | control_records/agentjobs/AJ-SFADEV-01-PRD-INTEGRATION-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_prd_integration_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-01-PRD-INTEGRATION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_prd_integration_completion | control_records/completions/RECEIPT-SFADEV-01-PRD-INTEGRATION-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_prd_integration_handoff | control_records/handoffs/HANDOFF-SFADEV-01-PRD-INTEGRATION-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_registry_schema_expansion_director_decision | control_records/director_decisions/DDR-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_registry_schema_expansion_agentjob | control_records/agentjobs/AJ-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_registry_schema_expansion_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_registry_schema_expansion_completion | control_records/completions/RECEIPT-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_registry_schema_expansion_handoff | control_records/handoffs/HANDOFF-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_discovery_gate_director_decision | control_records/director_decisions/DDR-SFADEV-03-DISCOVERY-GATE-001.yaml | director_decision | controlled | system_definition | contract_director_decision | pending |
| ctrl_discovery_gate_agentjob | control_records/agentjobs/AJ-SFADEV-03-DISCOVERY-GATE-001.yaml | agentjob_v0_2 | controlled | system_definition | contract_agentjob_v0_2 | pending |
| ctrl_discovery_gate_smoke_agentjob | control_records/agentjobs/AJ-P1-DISCOVERY-GATE-SMOKE-001.yaml | agentjob_v0_2 | controlled | system_definition | contract_agentjob_v0_2 | pending |
| ctrl_discovery_gate_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-03-DISCOVERY-GATE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_discovery_gate_completion | control_records/completions/RECEIPT-SFADEV-03-DISCOVERY-GATE-001.yaml | completion_receipt_v0_2 | controlled | system_definition | contract_completion_receipt_v0_2 | pending |
| ctrl_discovery_gate_handoff | control_records/handoffs/HANDOFF-SFADEV-03-DISCOVERY-GATE-001.yaml | handoff_v0_2 | controlled | system_definition | contract_handoff_v0_2 | pending |
| ctrl_role_governance_director_decision | control_records/director_decisions/DDR-SFADEV-04-ROLE-GOVERNANCE-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_role_governance_agentjob | control_records/agentjobs/AJ-SFADEV-04-ROLE-GOVERNANCE-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_role_governance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-04-ROLE-GOVERNANCE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_role_governance_completion | control_records/completions/RECEIPT-SFADEV-04-ROLE-GOVERNANCE-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_role_governance_handoff | control_records/handoffs/HANDOFF-SFADEV-04-ROLE-GOVERNANCE-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_skill_lifecycle_director_decision | control_records/director_decisions/DDR-SFADEV-06-SKILL-LIFECYCLE-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_skill_lifecycle_agentjob | control_records/agentjobs/AJ-SFADEV-06-SKILL-LIFECYCLE-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_skill_lifecycle_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-06-SKILL-LIFECYCLE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_skill_lifecycle_completion | control_records/completions/RECEIPT-SFADEV-06-SKILL-LIFECYCLE-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_skill_lifecycle_handoff | control_records/handoffs/HANDOFF-SFADEV-06-SKILL-LIFECYCLE-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_core_skills_batch_1_director_decision | control_records/director_decisions/DDR-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_core_skills_batch_1_agentjob | control_records/agentjobs/AJ-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_core_skills_batch_1_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_core_skills_batch_1_completion | control_records/completions/RECEIPT-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_core_skills_batch_1_handoff | control_records/handoffs/HANDOFF-SFADEV-07-CORE-SKILLS-BATCH-1-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_core_skills_batch_2_director_decision | control_records/director_decisions/DDR-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_core_skills_batch_2_agentjob | control_records/agentjobs/AJ-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_core_skills_batch_2_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_core_skills_batch_2_completion | control_records/completions/RECEIPT-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_core_skills_batch_2_handoff | control_records/handoffs/HANDOFF-SFADEV-08-CORE-SKILLS-BATCH-2-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |

## Validation Contract Trace

| contract_id | path | target_format | target_artifact_type | validator_command |
| --- | --- | --- | --- | --- |
| contract_agentjob | schemas/contracts/agentjob.schema.json | yaml | agentjob | sys-for-ai validate-jsonschema-contracts |
| contract_agentjob_v0_2 | schemas/contracts/agentjob_v0_2.schema.json | yaml | agentjob_v0_2 | sys-for-ai validate-agentjob |
| contract_completion_receipt | schemas/contracts/completion_receipt.schema.json | yaml | completion_receipt | sys-for-ai validate-jsonschema-contracts |
| contract_completion_receipt_v0_2 | schemas/contracts/completion_receipt_v0_2.schema.json | yaml | completion_receipt_v0_2 | sys-for-ai validate-completion-receipts |
| contract_director_decision | schemas/contracts/director_decision.schema.json | yaml | director_decision | sys-for-ai validate-director-decisions |
| contract_handoff | schemas/contracts/handoff.schema.json | yaml | handoff | sys-for-ai validate-jsonschema-contracts |
| contract_handoff_v0_2 | schemas/contracts/handoff_v0_2.schema.json | yaml | handoff_v0_2 | sys-for-ai validate-handoffs |
| contract_memory_preflight_receipt | schemas/contracts/memory_preflight_receipt.schema.json | yaml | memory_preflight_receipt | sys-for-ai validate-memory-preflight |
| contract_program_state | schemas/contracts/program_state.schema.json | yaml | program_state | sys-for-ai validate-program-state |
| contract_state_snapshot | schemas/contracts/state_snapshot.schema.json | yaml | state_snapshot | sys-for-ai validate-jsonschema-contracts |

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
