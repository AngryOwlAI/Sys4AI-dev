# SVC and Documentation Surface Architect

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `svc_documentation_surface_architect`
- Role class: `system_design_support`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Define source control and derivative surfaces
- Primary outputs: `SVCDA`
- Allowed artifact classes: `source_control;derivatives`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `source-authority-auditor;baseline-change-manager`
- Optional skills: `technical-writing-quality-gate`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| baseline-change-manager | required | when baselines or supersession change | framework_product;target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
