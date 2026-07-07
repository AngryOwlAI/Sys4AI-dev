# System Developer / User Wants Elicitor

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `user_wants_elicitor`
- Role class: `system_design_core`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Run discovery gate and capture user intent
- Primary outputs: `RDR;USRD`
- Allowed artifact classes: `requirements;discovery`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `system-definition-interview-context-45`
- Optional skills: `conversation-to-prd;decision-grilling-context-45`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| conversation-to-prd | optional | after discovery is complete | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |
| decision-grilling-context-45 | optional | when decisions need structured clarification | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |
| system-definition-interview-context-45 | required | new or changed system definition | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |
| system-definition-interview | optional | when lightweight discovery is sufficient | framework_product;target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_user_wants_elicitor | discovery_gate | validate-discovery-records | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
