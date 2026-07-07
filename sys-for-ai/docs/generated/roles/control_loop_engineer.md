# Control Loop Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `control_loop_engineer`
- Role class: `temporary_agentjob_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain temporary self hosting continue loop implementation compatibility
- Primary outputs: `control-loop-kernel;program-state-update`
- Allowed artifact classes: `control_records;validators`
- May create AgentJobs: `true`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `continue;source-first-memory`
- Optional skills: `codex-usage-metrics`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_control_loop_engineer | legacy_selfhost_control_loop | validate-control-loop;validate-check-diff | expires with self hosting legacy AgentJob family |

Canonical inputs remain the three role registries listed in the notice.
