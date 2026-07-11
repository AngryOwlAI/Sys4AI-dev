> **Generated derivative notice**
>
> This page is a generated reader surface. It is not canonical. Canonical authority remains with the linked source files, registry rows, and validation contracts. Do not hand-edit this page as source authority.

```yaml
page_metadata:
  derivative_id: der_host_capability_profile
  authority_status: generated_noncanonical
  derivative_type: host_capability_profile_summary
  source_registries:
    - registries/config_source_registry.csv
    - configs/host_profiles/codex_app_reference.toml
    - registries/derivative_registry.csv
  validation_contracts:
    - contract_host_capability_profile
  generated_at: 2026-07-11T14:12:24Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Host Capability Profile

This page summarizes the controlled reference-host profile. Structural validation does not satisfy G-07 or prove observable host behavior.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_host_capability_profile | docs/generated/governance/host-capability-profile.md | SRC-REG-CONFIG-SOURCES;SRC-HOST-PROFILE-CODEX-APP-REFERENCE;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Profile Status

| profile_id | version | verification_state | gate | scope | executable |
| --- | --- | --- | --- | --- | --- |
| codex_app_reference | 0.2.0 | draft_pending_G_07 | G-07 | structural_contract_only | false |

## Interface States

| interface_id | capability_status | execution_allowed | fallback_mode | evidence_status |
| --- | --- | --- | --- | --- |
| user_interaction | unknown | false | blocked | pending_G_07 |
| workspace_filesystem | unknown | false | blocked | pending_G_07 |
| terminal_and_tests | unknown | false | degraded | pending_G_07 |
| tools_connectors_and_network | unknown | false | rerouted | pending_G_07 |
| sub_agents | unknown | false | rerouted | pending_G_07 |
| task_and_thread_state | unknown | false | blocked | pending_G_07 |
| memory_and_retrieval | unknown | false | rerouted | pending_G_07 |
| target_runtime | unknown | false | blocked | pending_G_07 |

## Boundary

G-07 remains open. This reader grants no host, tool, filesystem, network, sub-agent, thread-state, cancellation, permission, production, or operational authority.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
