# Derivative Generator Engineer

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `derivative_generator_engineer`
- Role class: `temporary_agentjob_role`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain temporary generated derivative AgentJob compatibility
- Primary outputs: `generated-derivative-update`
- Allowed artifact classes: `generated_derivatives;registries`
- May create AgentJobs: `true`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `source-authority-auditor;technical-writing-quality-gate`
- Optional skills: ``
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_derivative_generator_engineer | legacy_derivative_generation | validate-generated-derivatives;validate-registry-graph | expires with self hosting legacy AgentJob family |

Canonical inputs remain the three role registries listed in the notice.
