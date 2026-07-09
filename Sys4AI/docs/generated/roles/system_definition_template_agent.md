# System Definition Template Agent

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `system_definition_template_agent`
- Role class: `temporary_legacy_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain system definition template compatibility
- Primary outputs: `template-update`
- Allowed artifact classes: `templates;discovery`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `system-definition-interview;technical-writing-quality-gate`
- Optional skills: `conversation-to-prd`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_system_definition_template_agent | legacy_system_definition_template | validate-discovery-template;validate-discovery-records | expires with Phase 1 legacy system definition template evidence |

Canonical inputs remain the three role registries listed in the notice.
