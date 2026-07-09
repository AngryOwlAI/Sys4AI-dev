# System Engineer / Technical Requirements Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `technical_requirements_engineer`
- Role class: `system_design_core`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Convert requirements and architecture into buildable technical requirements
- Primary outputs: `TRP`
- Allowed artifact classes: `requirements;implementation_plans`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `prd-to-implementation-plan;verification-validation-planner`
- Optional skills: ``
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| prd-to-implementation-plan | required | when technical plan is needed | framework_product;target_system_template;target_system_instance | PRDs/Sys4AI_phase-0_product_system_design_prd.md |
| verification-validation-planner | required | when verification evidence is needed | framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
