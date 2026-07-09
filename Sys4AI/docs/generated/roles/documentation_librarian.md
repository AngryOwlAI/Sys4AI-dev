# Documentation Librarian / Configuration Controller

> Generated derivative. Canonical role authority remains with `registries/role_registry.csv`, `registries/role_skill_crosswalk.csv`, and `registries/role_execution_binding_registry.csv`.

## Role

- Role ID: `documentation_librarian`
- Role class: `framework_governance`
- System layer scope: `development_system;framework_product`
- Primary mission: Maintain artifact index IDs derivative policy and source authority
- Primary outputs: `artifact-index;configuration-control`
- Allowed artifact classes: `documentation;registries;generated_derivatives`
- Legacy AgentJob creation enabled: `false`
- Requires Director decision: `false`

## Registry Skills

- Required skills: `source-authority-auditor;skill-import-generalizer`
- Optional skills: `technical-writing-quality-gate`
- Forbidden skills: ``

## Crosswalk Bindings

| Skill ID | Binding Type | Required When | System Layer Scope | Evidence Path |
|---|---|---|---|---|
| project-ontology-and-glossary | required | when controlled terminology is needed | development_system;framework_product | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |
| skill-import-generalizer | required | when skill import is governed | development_system;framework_product | PRDs/Sys4AI_phase-0_product_system_design_prd.md |
| source-authority-auditor | required | when source authority is reviewed | development_system;framework_product | implementation_plans/Sys4AI-dev_all_recommendations_implementation_plan.md |

## Execution Bindings

| Binding ID | Binding Scope | Required Validators | Expiry Policy |
|---|---|---|---|
| bind_documentation_librarian | configuration_control;runtime_skill_reconciliation | validate-generated-derivatives;validate-registry-graph | registered role no expiry |

Canonical inputs remain the three role registries listed in the notice.
