# Control Loop and AgentJob Planner

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `control_loop_agentjob_planner`
- Role class: `runtime_control`
- System layer scope: `development_system;framework_product;target_system_template;target_system_instance`
- Primary mission: Define continuation and bounded work semantics
- Primary outputs: `CLRA;AgentJob`
- Allowed artifact classes: `control_records;handoffs`
- May create AgentJobs: `true`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `continue;agentjob-task-packet-author;context-window-and-handoff-manager`
- Optional skills: `director-decision-governor`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| agentjob-task-packet-author | required | when task packets are authored | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |
| codex-usage-metrics | required | when continuation metrics are recorded | development_system;framework_product | implementation_plans/self_hosting_boundary_decision_record.md |
| continue | required | when continuation is designed | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/self_hosting_boundary_decision_record.md |

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_control_loop_agentjob_planner | agentjob_planning;handoff_planning | validate-control-loop;validate-agentjobs | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
