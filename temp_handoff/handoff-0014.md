# Handoff 0014: Registry and Schema Expansion

Date: 2026-07-07
Plan: `implementation_plans/sys-for-ai-dev_all_recommendations_implementation_plan.md`
Completed slice: WS-02 / AJ-02 - Registry and Schema Expansion

## Latest prior handoff check

The latest controlled handoff before this work was `sys-for-ai/control_records/handoffs/HANDOFF-SFADEV-01-PRD-INTEGRATION-001.yaml`. It closed the PRD integration slice and recommended `AJ-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001` as the next bounded AgentJob.

## Work completed

- Added controlled registry surfaces for:
  - system layers
  - discovery records
  - roles
  - role-skill crosswalks
  - role execution bindings
  - artifact contracts
  - core skill proposals
  - skill lifecycle statuses
- Added JSON Schema row contracts for each new registry.
- Added CLI validators and Makefile targets for the new registry surfaces.
- Added aggregate validation coverage for the new registry surfaces.
- Extended registry graph checks for role, skill, artifact, layer, discovery, and lifecycle references.
- Added validation contract registry rows for the new schema contracts.
- Added the bounded AJ-02 control packet:
  - `sys-for-ai/control_records/director_decisions/DDR-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml`
  - `sys-for-ai/control_records/agentjobs/AJ-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml`
  - `sys-for-ai/control_records/memory_preflights/MEMPREFLIGHT-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml`
  - `sys-for-ai/control_records/completions/RECEIPT-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml`
  - `sys-for-ai/control_records/handoffs/HANDOFF-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001.yaml`
- Updated program state to point at the new completion, handoff, and memory preflight.
- Retargeted current diff-boundary validation to `AJ-SFADEV-02-REGISTRY-SCHEMA-EXPANSION-001`.
- Registered the new registry, schema, control, source, and handoff artifacts.

## Validation evidence

- `cd sys-for-ai && make validate-jsonschema-contracts`
- `cd sys-for-ai && make validate-system-layers`
- `cd sys-for-ai && make validate-discovery-records`
- `cd sys-for-ai && make validate-roles`
- `cd sys-for-ai && make validate-artifact-contracts`
- `cd sys-for-ai && make validate-core-skill-proposals`
- `cd sys-for-ai && make validate-skill-lifecycle`
- `cd sys-for-ai && make validate-registry-graph`
- `cd sys-for-ai && make validate-agentjobs`
- `cd sys-for-ai && make validate-check-diff`

## Remaining uncertainty

The all-recommendations plan remains incomplete. This pass established the registry and schema control surfaces; it did not implement the operational discovery gate, role-specific runtime workflows, proposed core skills, or final acceptance closure.

## Next logical step

Select `AJ-SFADEV-03-DISCOVERY-GATE-001` so the Requirements Discovery Record and `system-definition-interview-context-45` become an operational discovery gate without automatically promoting candidate requirements into canonical PRDs.
