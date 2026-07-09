# Validator Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `validator_engineer`
- Role class: `temporary_legacy_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain validation evidence compatibility
- Primary outputs: `validator-update;diff-check`
- Allowed artifact classes: `validators;tests`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `technical-writing-quality-gate;verification-validation-planner`
- Optional skills: `source-first-memory`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_validator_engineer | legacy_validation | make validate | expires with self hosting legacy control records |

Canonical inputs remain the three role registries listed in the notice.
