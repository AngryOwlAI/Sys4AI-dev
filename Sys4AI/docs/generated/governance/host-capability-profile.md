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
  generated_at: 2026-07-12T14:24:41Z
  generator: sys_for_ai.derivative_generation.governance_generated_docs:0.2.0
  validation_status: generated_content_checked
  stale_or_orphan_status: current
  source_hashes:
    - pending
```

# Host Capability Profile

This page summarizes an accepted G-07 reference-host profile. The retained probe report proves the observed behavior; structural validation checks the profile and registered decision bindings.

## Registry Trace

| derivative_id | path | source_ids | generation_method | status |
| --- | --- | --- | --- | --- |
| der_host_capability_profile | docs/generated/governance/host-capability-profile.md | SRC-REG-CONFIG-SOURCES;SRC-HOST-PROFILE-CODEX-APP-REFERENCE;SRC-DERIVATIVE-GENERATION | sys_for_ai.derivative_generation.governance_generated_docs:0.2.0 | generated_derivative |

## Profile Status

| profile_id | version | verification_state | gate | scope | executable |
| --- | --- | --- | --- | --- | --- |
| codex_app_reference | 1.0.0 | verified_G_07 | G-07 | observable_host_conformance | true |

## Interface States

| interface_id | capability_status | execution_allowed | fallback_mode | evidence_status |
| --- | --- | --- | --- | --- |
| user_interaction | verified_available | true | blocked | current |
| workspace_filesystem | verified_available | true | blocked | current |
| terminal_and_tests | verified_available | true | degraded | current |
| tools_connectors_and_network | environment_dependent | false | rerouted | current |
| sub_agents | permission_dependent | false | rerouted | current |
| task_and_thread_state | environment_dependent | false | blocked | current |
| memory_and_retrieval | verified_available | true | rerouted | current |
| target_runtime | verified_unavailable | false | blocked | current |

## Boundary

G-07 is accepted only for the exact current mixed interface states. This reader grants no permission, production readiness, operational authority, target-runtime authority, stakeholder consensus, or domain truth.

## Allowed Promotion Path

Promotion requires an explicit source-authority decision, registry update, and validation evidence. This generated page is not promoted by generation.
