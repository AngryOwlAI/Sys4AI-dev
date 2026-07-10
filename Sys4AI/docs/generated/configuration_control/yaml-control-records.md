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
| ctrl_generated_docs_director_decision | control_records/director_decisions/DDR-SFADEV-09-GENERATED-DOCS-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_generated_docs_agentjob | control_records/agentjobs/AJ-SFADEV-09-GENERATED-DOCS-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_generated_docs_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-09-GENERATED-DOCS-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_generated_docs_completion | control_records/completions/RECEIPT-SFADEV-09-GENERATED-DOCS-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_generated_docs_handoff | control_records/handoffs/HANDOFF-SFADEV-09-GENERATED-DOCS-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_end_to_end_acceptance_director_decision | control_records/director_decisions/DDR-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_end_to_end_acceptance_agentjob | control_records/agentjobs/AJ-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_end_to_end_acceptance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_end_to_end_acceptance_completion | control_records/completions/RECEIPT-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_end_to_end_acceptance_handoff | control_records/handoffs/HANDOFF-SFADEV-10-END-TO-END-ACCEPTANCE-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_sys4ai_name_migration_director_decision | control_records/director_decisions/DDR-SYS4AI-DEV-NAME-MIGRATION-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_sys4ai_name_migration_agentjob | control_records/agentjobs/AJ-SYS4AI-DEV-NAME-MIGRATION-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_sys4ai_name_migration_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SYS4AI-DEV-NAME-MIGRATION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_sys4ai_name_migration_completion | control_records/completions/RECEIPT-SYS4AI-DEV-NAME-MIGRATION-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_sys4ai_name_migration_handoff | control_records/handoffs/HANDOFF-SYS4AI-DEV-NAME-MIGRATION-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_init_frontdoor_director_decision | control_records/director_decisions/DDR-SFADEV-11-INIT-FRONTDOOR-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_init_frontdoor_agentjob | control_records/agentjobs/AJ-SFADEV-11-INIT-FRONTDOOR-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_init_frontdoor_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-11-INIT-FRONTDOOR-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_init_frontdoor_completion | control_records/completions/RECEIPT-SFADEV-11-INIT-FRONTDOOR-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_init_frontdoor_handoff | control_records/handoffs/HANDOFF-SFADEV-11-INIT-FRONTDOOR-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_ws00_baseline_agentjob | control_records/agentjobs/AJ-SFADEV-WS00-BASELINE-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_discovery_gate_smoke_director_decision | control_records/director_decisions/DDR-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | director_decision | controlled | system_definition | contract_director_decision | pending |
| ctrl_discovery_gate_smoke_closeout_agentjob | control_records/agentjobs/AJ-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | agentjob_v0_2 | controlled | system_definition | contract_agentjob_v0_2 | pending |
| ctrl_discovery_gate_smoke_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_discovery_gate_smoke_completion | control_records/completions/RECEIPT-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | completion_receipt_v0_2 | controlled | system_definition | contract_completion_receipt_v0_2 | pending |
| ctrl_discovery_gate_smoke_handoff | control_records/handoffs/HANDOFF-SFADEV-12-DISCOVERY-GATE-SMOKE-001.yaml | handoff_v0_2 | controlled | system_definition | contract_handoff_v0_2 | pending |
| ctrl_plan_control_director_decision | control_records/director_decisions/DDR-SFADEV-13-PLAN-CONTROL-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_plan_control_agentjob | control_records/agentjobs/AJ-SFADEV-13-PLAN-CONTROL-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_plan_control_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-13-PLAN-CONTROL-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_plan_control_completion | control_records/completions/RECEIPT-SFADEV-13-PLAN-CONTROL-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_plan_control_handoff | control_records/handoffs/HANDOFF-SFADEV-13-PLAN-CONTROL-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_plan_completion_audit_director_decision | control_records/director_decisions/DDR-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_plan_completion_audit_agentjob | control_records/agentjobs/AJ-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_plan_completion_audit_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_plan_completion_audit_completion | control_records/completions/RECEIPT-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_plan_completion_audit_handoff | control_records/handoffs/HANDOFF-SFADEV-14-PLAN-COMPLETION-AUDIT-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_next_scope_selection_director_decision | control_records/director_decisions/DDR-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_next_scope_selection_agentjob | control_records/agentjobs/AJ-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_next_scope_selection_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_next_scope_selection_completion | control_records/completions/RECEIPT-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_next_scope_selection_handoff | control_records/handoffs/HANDOFF-SFADEV-15-NEXT-SCOPE-SELECTION-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_legacy_pending_reconciliation_director_decision | control_records/director_decisions/DDR-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | director_decision | controlled | implementation_initialization | contract_director_decision | pending |
| ctrl_legacy_pending_reconciliation_agentjob | control_records/agentjobs/AJ-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | agentjob_v0_2 | controlled | implementation_initialization | contract_agentjob_v0_2 | pending |
| ctrl_legacy_pending_reconciliation_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_legacy_pending_reconciliation_completion | control_records/completions/RECEIPT-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | completion_receipt_v0_2 | controlled | implementation_initialization | contract_completion_receipt_v0_2 | pending |
| ctrl_legacy_pending_reconciliation_handoff | control_records/handoffs/HANDOFF-SFADEV-16-LEGACY-PENDING-ROW-RECONCILIATION-001.yaml | handoff_v0_2 | controlled | implementation_initialization | contract_handoff_v0_2 | pending |
| ctrl_phase2_walking_skeleton_rdr_director_decision | control_records/director_decisions/DDR-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | director_decision | controlled | system_definition | contract_director_decision | pending |
| ctrl_phase2_walking_skeleton_rdr_agentjob | control_records/agentjobs/AJ-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | agentjob_v0_2 | controlled | system_definition | contract_agentjob_v0_2 | pending |
| ctrl_phase2_walking_skeleton_rdr_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_phase2_walking_skeleton_rdr_completion | control_records/completions/RECEIPT-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | completion_receipt_v0_2 | controlled | system_definition | contract_completion_receipt_v0_2 | pending |
| ctrl_phase2_walking_skeleton_rdr_handoff | control_records/handoffs/HANDOFF-SFADEV-17-PHASE2-WALKING-SKELETON-RDR-001.yaml | handoff_v0_2 | controlled | system_definition | contract_handoff_v0_2 | pending |
| ctrl_phase2_walking_skeleton_prd_director_decision | control_records/director_decisions/DDR-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |
| ctrl_phase2_walking_skeleton_prd_agentjob | control_records/agentjobs/AJ-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_phase2_walking_skeleton_prd_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_phase2_walking_skeleton_prd_completion | control_records/completions/RECEIPT-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_phase2_walking_skeleton_prd_handoff | control_records/handoffs/HANDOFF-SFADEV-18-PHASE2-WALKING-SKELETON-PRD-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_phase2_walking_skeleton_plan_director_decision | control_records/director_decisions/DDR-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |
| ctrl_phase2_walking_skeleton_plan_agentjob | control_records/agentjobs/AJ-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_phase2_walking_skeleton_plan_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_walking_skeleton_flow_agentjob | control_records/agentjobs/AJ-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_target_package_smoke_agentjob | control_records/agentjobs/AJ-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_walking_skeleton_demo_agentjob | control_records/agentjobs/AJ-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_phase2_walking_skeleton_plan_completion | control_records/completions/RECEIPT-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_phase2_walking_skeleton_plan_handoff | control_records/handoffs/HANDOFF-SFADEV-19-PHASE2-WALKING-SKELETON-PLAN-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_walking_skeleton_flow_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_walking_skeleton_flow_completion | control_records/completions/RECEIPT-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_walking_skeleton_flow_handoff | control_records/handoffs/HANDOFF-SFADEV-20-WALKING-SKELETON-FLOW-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_target_package_smoke_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_target_package_smoke_completion | control_records/completions/RECEIPT-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_target_package_smoke_handoff | control_records/handoffs/HANDOFF-SFADEV-21-TARGET-PACKAGE-SMOKE-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_walking_skeleton_demo_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_walking_skeleton_demo_completion | control_records/completions/RECEIPT-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_walking_skeleton_demo_handoff | control_records/handoffs/HANDOFF-SFADEV-22-WALKING-SKELETON-DEMO-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_prd_decomposition_strategy_agentjob | control_records/agentjobs/AJ-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_prd_decomposition_strategy_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_prd_decomposition_strategy_completion | control_records/completions/RECEIPT-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_prd_decomposition_strategy_handoff | control_records/handoffs/HANDOFF-SFADEV-23-PRD-DECOMPOSITION-STRATEGY-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_subprd_drafts_agentjob | control_records/agentjobs/AJ-SFADEV-24-SUBPRD-DRAFTS-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_subprd_drafts_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-24-SUBPRD-DRAFTS-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_subprd_drafts_completion | control_records/completions/RECEIPT-SFADEV-24-SUBPRD-DRAFTS-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_subprd_drafts_handoff | control_records/handoffs/HANDOFF-SFADEV-24-SUBPRD-DRAFTS-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_subprd_promotion_director_decision | control_records/director_decisions/DDR-SFADEV-25-SUBPRD-PROMOTION-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |
| ctrl_subprd_promotion_agentjob | control_records/agentjobs/AJ-SFADEV-25-SUBPRD-PROMOTION-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_subprd_promotion_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-25-SUBPRD-PROMOTION-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_subprd_promotion_completion | control_records/completions/RECEIPT-SFADEV-25-SUBPRD-PROMOTION-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_subprd_promotion_handoff | control_records/handoffs/HANDOFF-SFADEV-25-SUBPRD-PROMOTION-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_next_scope_acceptance_director_decision | control_records/director_decisions/DDR-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |
| ctrl_next_scope_acceptance_agentjob | control_records/agentjobs/AJ-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | agentjob_v0_2 | controlled | framework_product | contract_agentjob_v0_2 | pending |
| ctrl_next_scope_acceptance_memory_preflight | control_records/memory_preflights/MEMPREFLIGHT-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | memory_preflight_receipt | controlled | source_first_memory | contract_memory_preflight_receipt | pending |
| ctrl_next_scope_acceptance_completion | control_records/completions/RECEIPT-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | completion_receipt_v0_2 | controlled | framework_product | contract_completion_receipt_v0_2 | pending |
| ctrl_next_scope_acceptance_handoff | control_records/handoffs/HANDOFF-SFADEV-26-NEXT-SCOPE-ACCEPTANCE-001.yaml | handoff_v0_2 | controlled | framework_product | contract_handoff_v0_2 | pending |
| ctrl_strategic_baseline_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |
| ctrl_strategic_baseline_g03_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G03-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |
| ctrl_strategic_baseline_g04_director_decision | control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-G04-001.yaml | director_decision | controlled | framework_product | contract_director_decision | pending |

## Validation Contract Trace

| contract_id | path | target_format | target_artifact_type | validator_command |
| --- | --- | --- | --- | --- |
| contract_agentjob | schemas/contracts/agentjob.schema.json | yaml | agentjob | Sys4AI validate-jsonschema-contracts |
| contract_agentjob_v0_2 | schemas/contracts/agentjob_v0_2.schema.json | yaml | agentjob_v0_2 | archived-no-active-cli |
| contract_completion_receipt | schemas/contracts/completion_receipt.schema.json | yaml | completion_receipt | Sys4AI validate-jsonschema-contracts |
| contract_completion_receipt_v0_2 | schemas/contracts/completion_receipt_v0_2.schema.json | yaml | completion_receipt_v0_2 | Sys4AI validate-completion-receipts |
| contract_director_decision | schemas/contracts/director_decision.schema.json | yaml | director_decision | Sys4AI validate-director-decisions |
| contract_handoff | schemas/contracts/handoff.schema.json | yaml | handoff | Sys4AI validate-jsonschema-contracts |
| contract_handoff_v0_2 | schemas/contracts/handoff_v0_2.schema.json | yaml | handoff_v0_2 | Sys4AI validate-handoffs |
| contract_memory_preflight_receipt | schemas/contracts/memory_preflight_receipt.schema.json | yaml | memory_preflight_receipt | Sys4AI validate-memory-preflight |
| contract_program_state | schemas/contracts/program_state.schema.json | yaml | program_state | Sys4AI validate-program-state |
| contract_state_snapshot | schemas/contracts/state_snapshot.schema.json | yaml | state_snapshot | Sys4AI validate-jsonschema-contracts |

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
