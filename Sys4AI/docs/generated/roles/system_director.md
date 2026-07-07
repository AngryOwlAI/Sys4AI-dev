# System Director

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `system_director`
- Role class: `framework_governance`
- System layer scope: `development_system;framework_product;target_system_template;target_system_instance`
- Primary mission: Orchestrate phases gates handoffs and artifact governance
- Primary outputs: `system-design-run-manifest;artifact-registry;traceability-ledger;open-issues-register;design-phase-readiness-report`
- Allowed artifact classes: `control_records;requirements;handoffs`
- May create AgentJobs: `true`
- Requires Director decision: `true`

## Registry Skills

- Required skills: `director-decision-governor;system-layer-classifier`
- Optional skills: `source-first-memory`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| director-decision-governor | required | when routing is not determined | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| domain-pack-router | optional | when core versus domain-pack boundary is disputed | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| init | required | when routing Sys4AI adoption or system-definition entry | development_system;framework_product;target_system_template;target_system_instance | PRDs/Sys4AI_phase-0_product_system_design_prd.md |
| role-catalog-governance | required | when role catalog governance is needed | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| system-layer-classifier | required | before mutating controlled authority | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

| Binding ID | Allowed AgentJob Types | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_system_director | director_decision;agentjob_selection | validate-control-loop;validate-registry-graph | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
