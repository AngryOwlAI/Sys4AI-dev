# Skill Surface Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `skill_surface_engineer`
- Role class: `temporary_agentjob_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain temporary runtime and scaffold skill surface compatibility
- Primary outputs: `skill-surface-update`
- Allowed artifact classes: `skills;registries`
- May create AgentJobs: `true`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `skill-import-generalizer;technical-writing-quality-gate`
- Optional skills: `source-first-memory`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_skill_surface_engineer | legacy_skill_surface | validate-dev-skills;validate-skills | expires with self hosting legacy AgentJob family |

Canonical inputs remain the three role registries listed in the notice.
