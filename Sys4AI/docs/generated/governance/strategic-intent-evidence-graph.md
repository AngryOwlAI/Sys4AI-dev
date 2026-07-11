> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_strategic_intent_evidence_graph
  authority_status: generated_noncanonical
  derivative_type: strategic_intent_evidence_graph
  source_registries:
    - registries/source_registry.csv
    - registries/object_relationship_registry.csv
    - registries/requirement_trace_registry.csv
    - registries/derivative_registry.csv
  validation_contracts:
    - contract_requirement_trace_registry_row
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Strategic Intent Evidence Graph

This graph is a generated navigation view over registered evidence. Status labels summarize source state and never replace the named authority.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_strategic_intent_evidence_graph | docs/generated/governance/strategic-intent-evidence-graph.md | SRC-REG-SOURCES;SRC-REG-OBJECT-RELATIONSHIPS;SRC-REG-REQ-TRACE;SRC-PRD-P0;SRC-DDR-STRATEGIC-BASELINE-G08-001;SRC-SAFETY-EVALUATION-PACKET-TX17;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Evidence Nodes

| node | state | source_id | boundary |
| --- | --- | --- | --- |
| stakeholder evidence | approved_bounded | SRC-DDR-STRATEGIC-BASELINE-G08-001 | Exact framework G-08 decision only |
| vision | approved | SRC-PRD-P0 | SFA-VISION-001 version 1.0 |
| values | approved | SRC-PRD-P0 | SFA-VALUE-001 through SFA-VALUE-008 |
| requirements | current_mixed_capability | SRC-REG-REQ-TRACE | absent=5; implemented=85; scaffolded=137 |
| architecture | current_design_basis | SRC-PRD-P0 | Pattern and maturity remain independent |
| permissions | bounded | SRC-SCHEMA-EXECUTION-TRANSACTION | Values do not grant permission |
| tests | current_local_evidence | SRC-TEST-SAFETY-EVALUATION | pass=52; planned=175 |
| evaluations | current_with_gaps | SRC-SAFETY-EVALUATION-PACKET-TX17 | current=227 |
| operations | planned_not_operational | SRC-SAFETY-EVALUATION-PACKET-TX17 | No operational authority |
| maintenance | planned | SRC-PRD-P0 | Requires current operational evidence |
| improvement proposals | governed_not_self_authorizing | SRC-SAFETY-EVALUATION-PACKET-TX17 | Independent review and rollback required |

## Directed Evidence Flow

`stakeholder evidence -> vision and values -> requirements -> architecture and permissions -> tests and evaluations -> operations, maintenance, and improvement`

## State Distinctions

Approved strategic content remains distinct from current source authority, capability, verification, evidence freshness, host verification, operational maturity, and target-specific acceptance. Missing or planned evidence is not converted to current evidence by this graph.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
