# Domain Specialist

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `domain_specialist`
- Role class: `system_design_support`
- System layer scope: `target_system_instance`
- Primary mission: Validate domain assumptions and terminology
- Primary outputs: `domain-review`
- Allowed artifact classes: `analysis;requirements`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `domain-grilling-with-docs`
- Optional skills: `technical-writing-quality-gate`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| domain-grilling-with-docs-context-45 | recommended | when long documentation review sessions need checkpointing | target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |
| domain-pack-router | optional | when domain-specific skill routing is needed | target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
