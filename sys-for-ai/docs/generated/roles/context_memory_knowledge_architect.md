# Context Memory and Knowledge Architect

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `context_memory_knowledge_architect`
- Role class: `system_design_support`
- System layer scope: `development_system;framework_product;target_system_template;target_system_instance`
- Primary mission: Define source-first memory retrieval and registry rules
- Primary outputs: `CKMSRA`
- Allowed artifact classes: `memory;registries`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `source-first-memory;source-authority-auditor`
- Optional skills: `artifact-contract-governance`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| source-authority-auditor | required | when authority audit is needed | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |
| source-first-memory | required | when source-first memory is designed | development_system;framework_product;target_system_template;target_system_instance | implementation_plans/self_hosting_boundary_decision_record.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
