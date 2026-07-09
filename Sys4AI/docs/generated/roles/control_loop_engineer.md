# Control Loop Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `control_loop_engineer`
- Role class: `temporary_legacy_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain legacy self hosting control evidence compatibility
- Primary outputs: `legacy-control-record-review`
- Allowed artifact classes: `control_records;validators`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `source-first-memory`
- Optional skills: `codex-usage-metrics`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_control_loop_engineer | legacy_selfhost_control_loop | make validate | expires with self hosting legacy control records |

Canonical inputs remain the three role registries listed in the notice.
