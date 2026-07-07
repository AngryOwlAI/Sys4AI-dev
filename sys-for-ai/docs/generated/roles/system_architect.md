# System Architect

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `system_architect`
- Role class: `system_design_core`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Derive architecture drivers views and decisions
- Primary outputs: `ARD`
- Allowed artifact classes: `architecture;diagrams`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `decision-grilling;mermaid-diagrams;plantuml-diagrams`
- Optional skills: `artifact-contract-governance;interface-and-integration-discovery`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| artifact-contract-governance | optional | when artifact contracts need validation | framework_product;target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |
| decision-grilling | required | when architecture decisions are unclear | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |
| mermaid-diagrams | required | when diagrams are needed | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |
| plantuml-diagrams | required | when PlantUML diagrams are needed | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
