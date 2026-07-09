# System Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `system_engineer`
- Role class: `system_design_core`
- System layer scope: `development_system;framework_product;target_system_template;target_system_instance`
- Primary mission: Compatibility engineering role used by current skill manifests
- Primary outputs: `requirements;implementation_plan`
- Allowed artifact classes: `requirements;implementation_plans`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `prd-to-implementation-plan;technical-writing-quality-gate`
- Optional skills: `decision-grilling`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_system_engineer | prd_integration;requirements_trace | validate-requirement-trace | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
