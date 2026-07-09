# Control Loop Planner

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `control_loop_agentjob_planner`
- Role class: `runtime_control`
- System layer scope: `development_system;framework_product;target_system_template;target_system_instance`
- Primary mission: Define continuation and bounded work semantics
- Primary outputs: `CLRA`
- Allowed artifact classes: `control_records;handoffs`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `context-window-and-handoff-manager`
- Optional skills: `director-decision-governor`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| codex-usage-metrics | required | when continuation metrics are recorded | development_system;framework_product | implementation_plans/self_hosting_boundary_decision_record.md |
| context-window-and-handoff-manager | required | when resumable handoffs or context checkpoints are needed | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_control_loop_agentjob_planner | legacy_control_review;handoff_planning | validate-handoffs;validate-registry-graph | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
