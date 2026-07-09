# Existing System Analyst

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `existing_system_analyst`
- Role class: `system_design_support`
- System layer scope: `target_system_instance`
- Primary mission: Analyze brownfield or related current state
- Primary outputs: `ESAR`
- Allowed artifact classes: `analysis;requirements`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `domain-grilling-with-docs`
- Optional skills: `source-first-memory`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| domain-grilling-with-docs | required | when brownfield evidence needs domain stress testing | target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| init | required | when brownfield repository adoption begins | target_system_instance | PRDs/Sys4AI_phase-0_product_system_design_prd.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
