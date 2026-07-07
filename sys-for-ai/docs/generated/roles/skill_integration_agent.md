# Skill Integration Agent

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `skill_integration_agent`
- Role class: `temporary_agentjob_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain temporary skill integration AgentJob compatibility
- Primary outputs: `skill-manifest-update`
- Allowed artifact classes: `skills;registries`
- May create AgentJobs: `true`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `skill-import-generalizer;source-first-memory`
- Optional skills: `technical-writing-quality-gate`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_skill_integration_agent | legacy_skill_integration | validate-dev-skills;validate-skills | expires with Phase 1 legacy skill integration AgentJobs |

Canonical inputs remain the three role registries listed in the notice.
