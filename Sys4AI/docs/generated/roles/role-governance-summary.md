> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_role_governance_summary
  authority_status: generated_noncanonical
  derivative_type: governance_role_summary_page
  source_registries:
    - registries/role_registry.csv
    - registries/role_skill_crosswalk.csv
    - registries/role_execution_binding_registry.csv
    - registries/derivative_registry.csv
  validation_contracts:
    - contract_role_registry_row
    - contract_role_skill_crosswalk_row
    - contract_role_execution_binding_registry_row
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Role Governance Summary

This generated page summarizes role governance registries and execution binding coverage.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_role_governance_summary | docs/generated/roles/role-governance-summary.md | SRC-REG-ROLES;SRC-REG-ROLE-SKILL-CROSSWALK;SRC-REG-ROLE-EXECUTION-BINDINGS;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Role Rows

| role_id | role_class | required_skills | optional_skills | legacy_agentjob_creation_enabled | requires_director_decision |
| --- | --- | --- | --- | --- | --- |
| system_director | framework_governance | director-decision-governor;system-layer-classifier | source-first-memory | false | true |
| user_wants_elicitor | system_design_core | system-definition-interview-context-45 | conversation-to-prd;decision-grilling-context-45 | false | false |
| existing_system_analyst | system_design_support | domain-grilling-with-docs | source-first-memory | false | false |
| requirements_manager | system_design_core | conversation-to-prd;technical-writing-quality-gate | decision-grilling;traceability-matrix-engine | false | false |
| system_architect | system_design_core | decision-grilling;mermaid-diagrams;plantuml-diagrams | artifact-contract-governance;interface-and-integration-discovery | false | false |
| technical_requirements_engineer | system_design_core | prd-to-implementation-plan;verification-validation-planner | pending | false | false |
| reconciliation_analyst | system_design_core | decision-grilling | traceability-matrix-engine | false | false |
| reconciled_architecture_architect | system_design_core | mermaid-diagrams;decision-grilling | artifact-contract-governance | false | false |
| final_system_requirements_packager | system_design_core | prd-to-implementation-plan;technical-writing-quality-gate | traceability-matrix-engine | false | false |
| requirements_verifier | verification | technical-writing-quality-gate;traceability-matrix-engine | verification-validation-planner | false | false |
| domain_specialist | system_design_support | domain-grilling-with-docs | technical-writing-quality-gate | false | false |
| security_safety_privacy_compliance_reviewer | verification | threat-model-and-permission-scope;assurance-case-builder | verification-validation-planner | false | false |
| documentation_librarian | framework_governance | source-authority-auditor;skill-import-generalizer | technical-writing-quality-gate | false | false |
| runtime_maintenance_planner | maintenance | operations-and-maintenance-planner | evaluation-harness-designer | false | false |
| control_loop_agentjob_planner | runtime_control | context-window-and-handoff-manager | director-decision-governor | false | true |
| bounded_execution_planner | runtime_control | context-window-and-handoff-manager;baseline-change-manager | director-decision-governor | true | true |
| context_memory_knowledge_architect | system_design_support | source-first-memory;source-authority-auditor | artifact-contract-governance | false | false |
| svc_documentation_surface_architect | system_design_support | source-authority-auditor;baseline-change-manager | technical-writing-quality-gate | false | false |
| implementation_initialization_agent | implementation | prd-to-implementation-plan | source-first-memory | false | true |
| verification_engineer | verification | verification-validation-planner;technical-writing-quality-gate;evaluation-harness-designer | pending | false | false |
| software_engineer | implementation | prd-to-implementation-plan | source-first-memory | false | true |
| system_engineer | system_design_core | prd-to-implementation-plan;technical-writing-quality-gate | decision-grilling | false | false |
| system_analyst | system_design_core | decision-grilling;source-first-memory | conversation-to-prd | false | false |
| control_loop_engineer | temporary_legacy_role | source-first-memory | codex-usage-metrics | false | true |
| validator_engineer | temporary_legacy_role | technical-writing-quality-gate;verification-validation-planner | source-first-memory | false | true |
| derivative_generator_engineer | temporary_legacy_role | source-authority-auditor;technical-writing-quality-gate | pending | false | true |
| skill_surface_engineer | temporary_legacy_role | skill-import-generalizer;technical-writing-quality-gate | source-first-memory | false | true |
| acceptance_engineer | temporary_legacy_role | verification-validation-planner;technical-writing-quality-gate | source-first-memory | false | true |
| skill_dependency_adaptation_agent | temporary_legacy_role | skill-import-generalizer;codex-usage-metrics | technical-writing-quality-gate | false | true |
| skill_integration_agent | temporary_legacy_role | skill-import-generalizer;source-first-memory | technical-writing-quality-gate | false | true |
| system_definition_template_agent | temporary_legacy_role | system-definition-interview;technical-writing-quality-gate | conversation-to-prd | false | true |

## Crosswalk Coverage Counts

| role_id | required | optional | forbidden | conditional | recommended |
| --- | --- | --- | --- | --- | --- |
| system_director | 4 | 1 | 0 | 0 | 0 |
| user_wants_elicitor | 2 | 4 | 0 | 0 | 0 |
| existing_system_analyst | 2 | 0 | 0 | 0 | 0 |
| requirements_manager | 2 | 2 | 0 | 0 | 0 |
| system_architect | 3 | 2 | 0 | 0 | 0 |
| technical_requirements_engineer | 2 | 0 | 0 | 0 | 0 |
| reconciliation_analyst | 0 | 0 | 0 | 0 | 0 |
| reconciled_architecture_architect | 0 | 0 | 0 | 0 | 0 |
| final_system_requirements_packager | 0 | 0 | 0 | 0 | 0 |
| requirements_verifier | 2 | 1 | 0 | 0 | 0 |
| domain_specialist | 0 | 1 | 0 | 0 | 1 |
| security_safety_privacy_compliance_reviewer | 2 | 0 | 0 | 0 | 0 |
| documentation_librarian | 3 | 0 | 0 | 0 | 0 |
| runtime_maintenance_planner | 1 | 1 | 0 | 0 | 0 |
| control_loop_agentjob_planner | 2 | 0 | 0 | 0 | 0 |
| bounded_execution_planner | 2 | 0 | 0 | 0 | 0 |
| context_memory_knowledge_architect | 2 | 0 | 0 | 0 | 0 |
| svc_documentation_surface_architect | 1 | 0 | 0 | 0 | 0 |
| implementation_initialization_agent | 0 | 0 | 0 | 0 | 0 |
| verification_engineer | 2 | 0 | 0 | 0 | 0 |
| software_engineer | 0 | 0 | 0 | 0 | 0 |
| system_engineer | 0 | 0 | 0 | 0 | 0 |
| system_analyst | 0 | 0 | 0 | 0 | 0 |
| control_loop_engineer | 0 | 0 | 0 | 0 | 0 |
| validator_engineer | 0 | 0 | 0 | 0 | 0 |
| derivative_generator_engineer | 0 | 0 | 0 | 0 | 0 |
| skill_surface_engineer | 0 | 0 | 0 | 0 | 0 |
| acceptance_engineer | 0 | 0 | 0 | 0 | 0 |
| skill_dependency_adaptation_agent | 0 | 0 | 0 | 0 | 0 |
| skill_integration_agent | 0 | 0 | 0 | 0 | 0 |
| system_definition_template_agent | 0 | 0 | 0 | 0 | 0 |

## Execution Binding Rows

| role_id | binding_id | binding_scope | required_validators | completion_evidence |
| --- | --- | --- | --- | --- |
| system_director | bind_system_director | director_decision;legacy_control_review | validate-registry-graph | decision record;handoff |
| user_wants_elicitor | bind_user_wants_elicitor | discovery_gate | validate-discovery-records | RDR path;validation status |
| existing_system_analyst | pending | pending | pending | pending |
| requirements_manager | pending | pending | pending | pending |
| system_architect | pending | pending | pending | pending |
| technical_requirements_engineer | pending | pending | pending | pending |
| reconciliation_analyst | pending | pending | pending | pending |
| reconciled_architecture_architect | pending | pending | pending | pending |
| final_system_requirements_packager | pending | pending | pending | pending |
| requirements_verifier | pending | pending | pending | pending |
| domain_specialist | pending | pending | pending | pending |
| security_safety_privacy_compliance_reviewer | bind_security_safety_privacy_compliance_reviewer | safety_review;permission_scope;assurance_case | validate-safety-evaluation;validate-roles;make validate | threat model;permission scope;assurance case;residual risk |
| documentation_librarian | bind_documentation_librarian | configuration_control;runtime_skill_reconciliation | validate-generated-derivatives;validate-registry-graph | registry rows;generated derivative check |
| runtime_maintenance_planner | bind_runtime_maintenance_planner | operations_planning;maintenance_planning;readiness_review | validate-safety-evaluation;validate-roles;make validate | operations and maintenance plan;readiness gap register |
| control_loop_agentjob_planner | bind_control_loop_agentjob_planner | legacy_control_review;handoff_planning | validate-handoffs;validate-registry-graph | historical review evidence |
| bounded_execution_planner | bind_bounded_execution_planner | baseline_migration;implementation;validation;handoff_planning | make validate;validate-capability-migration | execution transaction;completion evidence;handoff |
| context_memory_knowledge_architect | pending | pending | pending | pending |
| svc_documentation_surface_architect | bind_svc_documentation_surface_architect | baseline_change;rollback_planning;supersession | validate-safety-evaluation;validate-generated-derivatives;make validate | baseline and rollback record;supersession evidence |
| implementation_initialization_agent | bind_implementation_initialization_agent | implementation_initialization | make validate | completion receipt;handoff |
| verification_engineer | bind_verification_engineer | verification;self_change_evaluation;holdout_evaluation | validate-safety-evaluation;validate-roles;make validate | evaluation harness;holdout result;regression evidence;validation report |
| software_engineer | bind_software_engineer | implementation | make validate | code change;test evidence |
| system_engineer | bind_system_engineer | prd_integration;requirements_trace | validate-requirement-trace | trace rows;completion receipt |
| system_analyst | pending | pending | pending | pending |
| control_loop_engineer | bind_control_loop_engineer | legacy_selfhost_control_loop | make validate | historical validation evidence |
| validator_engineer | bind_validator_engineer | legacy_validation | make validate | validation evidence;handoff |
| derivative_generator_engineer | bind_derivative_generator_engineer | legacy_derivative_generation | validate-generated-derivatives;validate-registry-graph | generated docs;registry rows |
| skill_surface_engineer | bind_skill_surface_engineer | legacy_skill_surface | validate-dev-skills;validate-skills | skill manifests;registry rows |
| acceptance_engineer | bind_acceptance_engineer | legacy_acceptance | make validate | acceptance report;completion receipt |
| skill_dependency_adaptation_agent | bind_skill_dependency_adaptation_agent | legacy_skill_dependency_adaptation | validate-dev-skills;validate-skills | adapter files;manifest rows |
| skill_integration_agent | bind_skill_integration_agent | legacy_skill_integration | validate-dev-skills;validate-skills | manifest rows;adapter files |
| system_definition_template_agent | bind_system_definition_template_agent | legacy_system_definition_template | validate-discovery-template;validate-discovery-records | template path;validation status |

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
