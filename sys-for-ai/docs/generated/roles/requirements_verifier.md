# Requirements Verifier / Consistency Auditor

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `requirements_verifier`
- Role class: `verification`
- System layer scope: `framework_product;target_system_template;target_system_instance`
- Primary mission: Check consistency traceability and quality
- Primary outputs: `review-report`
- Allowed artifact classes: `validation;requirements`
- May create AgentJobs: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `technical-writing-quality-gate;traceability-matrix-engine`
- Optional skills: `verification-validation-planner`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| technical-writing-quality-gate | required | before accepting requirements | framework_product;target_system_template;target_system_instance | PRDs/sys-for-ai_phase-0_product_system_design_prd.md |
| traceability-matrix-engine | required | when traceability is reviewed | framework_product;target_system_template;target_system_instance | implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

No role execution binding is registered for this role.

Canonical inputs remain the three role registries listed in the notice.
