# Implementation Initialization Agent

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `implementation_initialization_agent`
- Role class: `implementation`
- System layer scope: `development_system;framework_product`
- Primary mission: Initialize implementation scaffold
- Primary outputs: `implementation-scaffold`
- Allowed artifact classes: `code;registries;schemas;validators`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `prd-to-implementation-plan`
- Optional skills: `source-first-memory`
- Forbidden skills: ``

## Crosswalk Bindings

No role-skill crosswalk bindings are registered for this role.

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_implementation_initialization_agent | implementation_initialization | make validate | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
