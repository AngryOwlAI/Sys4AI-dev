# Acceptance Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `acceptance_engineer`
- Role class: `temporary_legacy_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain acceptance evidence compatibility
- Primary outputs: `acceptance-report;completion-receipt`
- Allowed artifact classes: `validation;control_records`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `verification-validation-planner;technical-writing-quality-gate`
- Optional skills: `source-first-memory`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_acceptance_engineer | legacy_acceptance | make validate | expires with self hosting legacy control records |

Canonical inputs remain the three role registries listed in the notice.
