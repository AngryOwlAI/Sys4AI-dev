> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_artifact_contracts_index
  authority_status: generated_noncanonical
  derivative_type: governance_artifact_contracts_page
  source_registries:
    - registries/artifact_contract_registry.csv
    - registries/derivative_registry.csv
  validation_contracts:
    - contract_agentjob_v0_2
    - contract_artifact_contract_registry_row
    - contract_completion_receipt_v0_2
    - contract_director_decision
    - contract_discovery_record_registry_row
    - contract_execution_transaction
    - contract_handoff_v0_2
    - contract_memory_preflight_receipt
    - contract_role_registry_row
    - contract_self_change_holdout_suite
    - contract_self_change_safety_evaluation
    - contract_target_core_values
    - contract_target_system_package_manifest
    - contract_target_vision_statement
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Artifact Contracts

This generated page summarizes artifact contracts, producers, consumers, derivative surfaces, and promotion rules.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_artifact_contracts_index | docs/generated/artifact_contracts/index.md | SRC-REG-ARTIFACT-CONTRACTS;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Structural Versus Semantic Warning

Validation contracts prove structural conformance only. They do not prove semantic truth, product correctness, or implementation completeness.

## Artifact Contract Rows

| artifact_contract_id | artifact_type | producer_role_ids | consumer_role_ids | authority_default | validation_contract_id | derivative_surfaces | promotion_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_rdr | RDR | user_wants_elicitor | requirements_manager;system_director | controlled_candidate | contract_discovery_record_registry_row | none | Promote only through requirements authority workflow |
| artifact_usrd | USRD | user_wants_elicitor | requirements_manager;reconciliation_analyst | canonical_draft | pending | markdown_derivative | Director baseline approval required |
| artifact_esar | ESAR | existing_system_analyst | requirements_manager;system_architect;technical_requirements_engineer | controlled | pending | markdown_derivative | Controlled source baseline |
| artifact_srd | SRD | requirements_manager | system_architect;technical_requirements_engineer;requirements_verifier | canonical_draft | pending | markdown_derivative | Requirements baseline approval required |
| artifact_ard | ARD | system_architect | technical_requirements_engineer;requirements_verifier | canonical_draft | pending | markdown_derivative | Architecture baseline approval required |
| artifact_trp | TRP | technical_requirements_engineer | reconciliation_analyst;requirements_verifier | canonical_draft | pending | markdown_derivative | Technical baseline approval required |
| artifact_rsrd | RSRD | reconciliation_analyst | reconciled_architecture_architect;final_system_requirements_packager | canonical_draft | pending | markdown_derivative | Reconciliation baseline approval required |
| artifact_rard | RARD | reconciled_architecture_architect | final_system_requirements_packager | canonical_draft | pending | markdown_derivative | Reconciled architecture baseline approval required |
| artifact_srp | SRP | final_system_requirements_packager | implementation_initialization_agent | canonical | pending | markdown_derivative | Final package signoff required |
| artifact_clra | CLRA | control_loop_agentjob_planner | final_system_requirements_packager;implementation_initialization_agent | historical | pending | markdown_derivative | No current promotion; preserve only as historical compatibility evidence |
| artifact_ckmsra | CKMSRA | context_memory_knowledge_architect | system_architect;implementation_initialization_agent | controlled | pending | markdown_derivative | Controlled annex baseline |
| artifact_svcda | SVCDA | svc_documentation_surface_architect | final_system_requirements_packager;implementation_initialization_agent | controlled | pending | markdown_derivative | Controlled annex baseline |
| artifact_agentjob | AgentJob | control_loop_agentjob_planner | software_engineer;verification_engineer | historical | contract_agentjob_v0_2 | configuration_control_wiki | No current promotion; preserve only as historical compatibility evidence |
| artifact_director_decision | DirectorDecision | system_director | bounded_execution_planner;implementation_initialization_agent | controlled | contract_director_decision | configuration_control_wiki | Supersede activated records |
| artifact_handoff | Handoff | system_engineer;implementation_initialization_agent;documentation_librarian | system_director;all_agents | controlled | contract_handoff_v0_2 | configuration_control_wiki | Supersede activated records |
| artifact_completion_receipt | CompletionReceipt | system_engineer;implementation_initialization_agent;verification_engineer | system_director;all_agents | controlled | contract_completion_receipt_v0_2 | configuration_control_wiki | Supersede activated records |
| artifact_memory_preflight | MemoryPreflightReceipt | context_memory_knowledge_architect;system_engineer | system_director;all_agents | controlled | contract_memory_preflight_receipt | configuration_control_wiki | Supersede activated records |
| artifact_role_registry | RoleRegistry | system_director | all_agents | controlled | contract_role_registry_row | configuration_control_wiki | Controlled registry update |
| artifact_skill_manifest | SkillManifest | documentation_librarian;implementation_initialization_agent | all_agents | controlled | pending | configuration_control_wiki | Controlled skill governance update |
| artifact_validation_contract | ValidationContract | verification_engineer | all_agents | controlled | pending | validation_contracts_catalog | Controlled contract update |
| artifact_generated_configuration_control_wiki | GeneratedConfigurationControlWiki | documentation_librarian | all_agents | derivative | pending | none | Promotion requires source authority decision |
| artifact_generated_validation_contracts_catalog | GeneratedValidationContractsCatalog | documentation_librarian | all_agents | derivative | pending | none | Promotion requires source authority decision |
| artifact_target_vision | TargetVisionStatement | user_wants_elicitor;requirements_manager | requirements_manager;requirements_verifier;system_architect;verification_engineer;runtime_maintenance_planner | controlled_candidate | contract_target_vision_statement | target_package;strategic_intent_contract_index | Promote only with accountable human evidence stable VISION ID current hash validation impact review and registered active-version relationships |
| artifact_target_core_values | TargetCoreValues | user_wants_elicitor;requirements_manager | requirements_manager;requirements_verifier;system_architect;verification_engineer;runtime_maintenance_planner | controlled_candidate | contract_target_core_values | target_package;strategic_intent_contract_index | Promote only with accountable human evidence stable VALUE IDs current hash validation impact review and registered active-version relationships |
| artifact_execution_transaction | ExecutionTransaction | system_director;implementation_initialization_agent | software_engineer;verification_engineer;system_director | controlled | contract_execution_transaction | configuration_control_wiki | Activate only with current human authorization a current permission envelope verified required capabilities and registered state evidence |
| artifact_bera | BoundedExecutionRequirementsAnnex | bounded_execution_planner | final_system_requirements_packager;implementation_initialization_agent | controlled | pending | markdown_derivative | Baseline through requirements authority and bind execution only through an authorized transaction |
| artifact_target_system_package_manifest | TargetSystemPackageManifest | implementation_initialization_agent | requirements_verifier;verification_engineer;system_architect;runtime_maintenance_planner | derivative | contract_target_system_package_manifest | target_package;registry_catalog | Promote only through accountable source authority with current strategic approval impact trace hashes validation and production evidence where claimed |
| artifact_self_change_safety_evaluation_packet | SelfChangeSafetyEvaluationPacket | security_safety_privacy_compliance_reviewer;verification_engineer;runtime_maintenance_planner;svc_documentation_surface_architect | system_director;requirements_verifier;software_engineer | controlled | contract_self_change_safety_evaluation | none | Consequential baseline acceptance requires TX-18 accountable human review and cannot grant production or operational authority |
| artifact_self_change_holdout_suite | SelfChangeHoldoutSuite | verification_engineer | security_safety_privacy_compliance_reviewer;system_director | controlled | contract_self_change_holdout_suite | none | Threshold or scenario mutation requires accountable approval independent review updated baseline evidence and full regression |

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
