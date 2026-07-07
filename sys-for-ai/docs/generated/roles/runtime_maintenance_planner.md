# Runtime and Maintenance Planner

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `runtime_maintenance_planner`
- Role class: `maintenance`
- System layer scope: `target_system_template;target_system_instance`
- Primary mission: Define operations monitoring updates and maintenance
- Primary outputs: `maintenance-plan`
- Allowed artifact classes: `operations;maintenance`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `operations-and-maintenance-planner`
- Optional skills: `evaluation-harness-designer`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| operations-and-maintenance-planner | required | when operations plan is needed | target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
