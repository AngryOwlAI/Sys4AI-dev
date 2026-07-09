# Security Safety Privacy and Compliance Reviewer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `security_safety_privacy_compliance_reviewer`
- Role class: `verification`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Review risk controls and compliance obligations
- Primary outputs: `risk-review`
- Allowed artifact classes: `security;validation`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `threat-model-and-permission-scope;assurance-case-builder`
- Optional skills: `verification-validation-planner`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| assurance-case-builder | required | when high impact claims need evidence argument | framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| threat-model-and-permission-scope | required | when safety or privacy risk is present | framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
