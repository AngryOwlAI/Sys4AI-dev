# System Manager / Requirements Manager

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `requirements_manager`
- Role class: `system_design_core`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Convert user wants to system requirements
- Primary outputs: `SRD`
- Allowed artifact classes: `requirements`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `conversation-to-prd;technical-writing-quality-gate`
- Optional skills: `decision-grilling;traceability-matrix-engine`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| conversation-to-prd | required | when producing requirements artifacts | framework_product;target_system_template;target_system_instance | PRDs/Sys4AI_phase-0_product_system_design_prd.md |
| requirements-discovery-governor | optional | when discovery output moves toward requirements baseline | framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| technical-writing-quality-gate | required | before requirements baseline | framework_product;target_system_template;target_system_instance | PRDs/Sys4AI_phase-0_product_system_design_prd.md |
| traceability-matrix-engine | optional | when trace matrix is needed | framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
