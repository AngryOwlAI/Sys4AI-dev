# Verification Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `verification_engineer`
- Role class: `verification`
- System layer scope: `development_system;framework_product;target_system_template;target_system_instance`
- Primary mission: Create and run validation evidence
- Primary outputs: `validation-report`
- Allowed artifact classes: `validation;tests`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `verification-validation-planner;technical-writing-quality-gate`
- Optional skills: `evaluation-harness-designer`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| evaluation-harness-designer | optional | when validation needs scenario or rubric design | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| verification-validation-planner | required | when validation evidence is authored | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
