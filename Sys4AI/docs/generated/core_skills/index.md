> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_core_skills_index
  authority_status: generated_noncanonical
  derivative_type: governance_core_skills_page
  source_registries:
    - registries/skill_registry.csv
    - registries/core_skill_proposal_registry.csv
    - registries/skill_lifecycle_status_registry.csv
    - registries/derivative_registry.csv
  validation_contracts:
    - contract_core_skill_proposal_registry_row
    - contract_skill_lifecycle_status_registry_row
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Core Skills

This generated page summarizes product scaffold skills and proposed core organizational skills.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_core_skills_index | docs/generated/core_skills/index.md | SRC-PRODUCT-SKILL-REGISTRY;SRC-PRODUCT-CORE-SKILL-MANIFEST;SRC-REG-CORE-SKILL-PROPOSALS;SRC-REG-SKILL-LIFECYCLE;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Product Skill Registry Rows

| skill_id | family | adaptation_status | lifecycle_status | local_path |
| --- | --- | --- | --- | --- |
| codex-usage-metrics | runtime_session_accounting | adapter_shell | adapter_shell | skills/core/codex-usage-metrics |
| system-definition-interview | system_definition_elicitation | adapter_shell | adapter_shell | skills/core/system-definition-interview |
| system-definition-interview-context-45 | system_definition_elicitation | adapter_shell | adapter_shell | skills/core/system-definition-interview-context-45 |
| conversation-to-prd | requirements_production | adapter_shell | adapter_shell | skills/core/conversation-to-prd |
| decision-grilling | decision_clarification | adapter_shell | adapter_shell | skills/core/decision-grilling |
| decision-grilling-context-45 | decision_clarification | adapter_shell | adapter_shell | skills/core/decision-grilling-context-45 |
| domain-grilling-with-docs | domain_documentation_clarification | adapter_shell | adapter_shell | skills/core/domain-grilling-with-docs |
| domain-grilling-with-docs-context-45 | domain_documentation_clarification | adapter_shell | adapter_shell | skills/core/domain-grilling-with-docs-context-45 |
| mermaid-diagrams | technical_communication | adapter_shell | adapter_shell | skills/core/mermaid-diagrams |
| plantuml-diagrams | technical_communication | adapter_shell | adapter_shell | skills/core/plantuml-diagrams |
| prd-to-implementation-plan | implementation_planning | adapter_shell | adapter_shell | skills/core/prd-to-implementation-plan |
| skill-import-generalizer | skill_library_maintenance | adapter_shell | adapter_shell | skills/core/skill-import-generalizer |
| technical-writing-quality-gate | technical_writing_verification | adapter_shell | adapter_shell | skills/core/technical-writing-quality-gate |
| source-first-memory | source_first_memory | scaffold_template | product_scaffold_reference | skills/core/source-first-memory |
| role-catalog-governance | role_governance | adapter_shell | adapter_shell | skills/core/role-catalog-governance |
| system-layer-classifier | system_layer_governance | adapter_shell | adapter_shell | skills/core/system-layer-classifier |
| artifact-contract-governance | artifact_governance | adapter_shell | adapter_shell | skills/core/artifact-contract-governance |
| traceability-matrix-engine | traceability_governance | adapter_shell | adapter_shell | skills/core/traceability-matrix-engine |
| director-decision-governor | decision_governance | adapter_shell | adapter_shell | skills/core/director-decision-governor |
| source-authority-auditor | source_authority | adapter_shell | adapter_shell | skills/core/source-authority-auditor |
| context-window-and-handoff-manager | context_handoff | adapter_shell | adapter_shell | skills/core/context-window-and-handoff-manager |
| verification-validation-planner | verification_planning | adapter_shell | adapter_shell | skills/core/verification-validation-planner |
| assurance-case-builder | assurance_case | adapter_shell | adapter_shell | skills/core/assurance-case-builder |
| threat-model-and-permission-scope | safety_security_privacy | adapter_shell | adapter_shell | skills/core/threat-model-and-permission-scope |
| evaluation-harness-designer | evaluation_design | adapter_shell | adapter_shell | skills/core/evaluation-harness-designer |
| baseline-change-manager | change_control | adapter_shell | adapter_shell | skills/core/baseline-change-manager |
| operations-and-maintenance-planner | operations_maintenance | adapter_shell | adapter_shell | skills/core/operations-and-maintenance-planner |
| project-ontology-and-glossary | ontology_glossary | adapter_shell | adapter_shell | skills/core/project-ontology-and-glossary |
| domain-pack-router | domain_routing | adapter_shell | adapter_shell | skills/core/domain-pack-router |
| interface-and-integration-discovery | interface_discovery | adapter_shell | adapter_shell | skills/core/interface-and-integration-discovery |
| requirements-discovery-governor | discovery_governance | adapter_shell | adapter_shell | skills/core/requirements-discovery-governor |
| init | system_adoption_front_door | adapter_shell | adapter_shell | skills/core/init |

## Core Skill Proposal Rows

| proposal_id | skill_id | priority | status | required_by_roles | target_runtime_path | validator_plan |
| --- | --- | --- | --- | --- | --- | --- |
| proposal_role_catalog_governance | role-catalog-governance | 1 | scaffolded | system_director;documentation_librarian | .agents/skills/role-catalog-governance | validate-roles |
| proposal_system_layer_classifier | system-layer-classifier | 2 | scaffolded | system_director | .agents/skills/system-layer-classifier | validate-system-layers |
| proposal_artifact_contract_governance | artifact-contract-governance | 3 | scaffolded | system_architect;documentation_librarian | .agents/skills/artifact-contract-governance | validate-artifact-contracts |
| proposal_traceability_matrix_engine | traceability-matrix-engine | 4 | scaffolded | requirements_manager;requirements_verifier | .agents/skills/traceability-matrix-engine | validate-requirement-trace |
| proposal_director_decision_governor | director-decision-governor | 5 | scaffolded | system_director | .agents/skills/director-decision-governor | validate-director-decisions |
| proposal_verification_validation_planner | verification-validation-planner | 6 | scaffolded | technical_requirements_engineer;requirements_verifier;verification_engineer | .agents/skills/verification-validation-planner | make validate |
| proposal_source_authority_auditor | source-authority-auditor | 7 | scaffolded | documentation_librarian;context_memory_knowledge_architect | .agents/skills/source-authority-auditor | validate-registry-graph |
| proposal_context_window_and_handoff_manager | context-window-and-handoff-manager | 8 | scaffolded | bounded_execution_planner | .agents/skills/context-window-and-handoff-manager | validate-handoffs |
| proposal_threat_model_permission_scope | threat-model-and-permission-scope | 9 | scaffolded | security_safety_privacy_compliance_reviewer | .agents/skills/threat-model-and-permission-scope | make validate |
| proposal_evaluation_harness_designer | evaluation-harness-designer | 10 | scaffolded | runtime_maintenance_planner;verification_engineer | .agents/skills/evaluation-harness-designer | make validate |
| proposal_baseline_change_manager | baseline-change-manager | 11 | scaffolded | svc_documentation_surface_architect | .agents/skills/baseline-change-manager | validate-registry-graph |
| proposal_operations_maintenance_planner | operations-and-maintenance-planner | 13 | scaffolded | runtime_maintenance_planner | .agents/skills/operations-and-maintenance-planner | make validate |
| proposal_project_ontology_glossary | project-ontology-and-glossary | 14 | scaffolded | documentation_librarian | .agents/skills/project-ontology-and-glossary | make validate |
| proposal_domain_pack_router | domain-pack-router | 15 | scaffolded | domain_specialist;system_director | .agents/skills/domain-pack-router | make validate |
| proposal_requirements_discovery_governor | requirements-discovery-governor | 16 | scaffolded | user_wants_elicitor;requirements_manager | .agents/skills/requirements-discovery-governor | validate-discovery-records |
| proposal_interface_integration_discovery | interface-and-integration-discovery | 17 | scaffolded | system_architect | .agents/skills/interface-and-integration-discovery | make validate |
| proposal_assurance_case_builder | assurance-case-builder | 18 | scaffolded | security_safety_privacy_compliance_reviewer | .agents/skills/assurance-case-builder | make validate |
| proposal_init | init | 0 | scaffolded | user_wants_elicitor;system_director;requirements_manager | .agents/skills/init | make validate |

## Lifecycle Vocabulary Rows

| status_id | status_name | may_execute_runtime | may_be_used_as_authority | requires_manifest | allowed_roots |
| --- | --- | --- | --- | --- | --- |
| status_proposed | proposed | false | false | false | .agents/skills;Sys4AI/skills/core |
| status_imported_unadapted | imported_unadapted | false | false | true | Sys4AI/skills/core |
| status_adapter_shell | adapter_shell | false | false | true | Sys4AI/skills/core |
| status_adapted_runtime_active | adapted_runtime_active | true | true | true | .agents/skills |
| status_product_scaffold_reference | product_scaffold_reference | false | false | true | Sys4AI/skills/core |
| status_deprecated | deprecated | false | false | true | .agents/skills;Sys4AI/skills/core |
| status_superseded | superseded | false | false | true | .agents/skills;Sys4AI/skills/core |
| status_blocked | blocked | false | false | false | .agents/skills;Sys4AI/skills/core |

## Authority Boundary

Product scaffold skills are reference surfaces. Active runtime authority remains with registered runtime skill surfaces unless separately promoted.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
