# Strategic Baseline Migration TX-08 Completion Receipt

- Receipt ID: `CR-SFADEV-STRATEGIC-BASELINE-TX08-001`
- Transaction: `TX-08-HOST-PROFILE`
- Workstream: `WS-06`
- Entry gate: `G-04`, accepted by `DDR-SFADEV-STRATEGIC-BASELINE-G04-001`
- Observable host-verification gate: `G-07`, open
- Plan: `implementation_plans/Sys4AI-dev_strategic_baseline_migration_full_implementation_plan.md`
- Result: `PASS_WITH_WARNINGS`
- Completion date: 2026-07-10
- Subject system: `Sys4AI-dev` development system and `Sys4AI` framework product
- Change class: additive reference-host contract baseline

## 1. Conclusion

`TX-08-HOST-PROFILE` is complete. It creates the G-04-approved Codex App reference-host
profile, its validation contract, its controlled interface and trust-boundary
description, and the focused structural validator needed to prove fail-closed
profile behavior. It does not verify Codex behavior or satisfy `G-07`.

The checked-in profile is deliberately `draft_pending_G_07`. All eight
required interface states are `unknown`; all have `execution_allowed = false`
and an explicit blocked, degraded, or rerouted fallback. The required
`verified_at` and `verified_by` fields use the controlled `pending_G_07`
sentinel rather than fabricated evidence, and `verification_decision` remains
`pending_G_07`. The portable execution-contract
binding uses `pending_TX_09` and is non-executable.

## 2. Authorization And Layer Boundaries

| Surface | Layer | Authority | TX-08 disposition |
|---|---|---|---|
| Host profile, schema, controlled integration document, validator, tests, CLI, Make target, and registries | `framework_product` | Controlled framework sources authorized by G-04 and the current human instruction | Added without claiming external host behavior |
| Implementation plan and this receipt | `development_system` | Controlled transaction and completion evidence | Records the bounded change and handoff |
| Generated configuration, validation-contract, and registry pages | `derivative_surface` | Noncanonical navigation | Regenerated deterministically from controlled rows |
| Codex App behavior and permissions | External reference-host trust boundary | Platform, system/developer instructions, host permissions, and user authorization remain binding | Not mutated or accepted as verified by TX-08 |
| Target-system templates and instances | `target_system_template` and `target_system_instance` | Separate target authority | No target write or capability promotion |

The transaction does not mutate historical program state, handoffs, AgentJob
records, accepted decisions, or Phase 2 evidence. It does not restore
AgentJob or `/continue`, introduce a new system layer, add a role or registry,
approve purpose or values, expand permissions, or authorize production.

## 3. Controlled Host-Profile Baseline

### 3.1 Profile identity and pending dependencies

- Profile: `Sys4AI/configs/host_profiles/codex_app_reference.toml`.
- Contract: `Sys4AI/schemas/contracts/host_capability_profile.schema.json`.
- Controlled interface description: `Sys4AI/docs/codex_host_integration_profile.md`.
- Producer roles: `system_engineer` and `verification_engineer`.
- Consumer roles: `implementation_initialization_agent`, `system_architect`, and `requirements_verifier`.
- Verification state: `draft_pending_G_07`.
- Portable execution binding: `pending_TX_09`, non-executable.
- Capability claims: zero `verified_available` and zero `verified_unavailable` claims.

### 3.2 Required interfaces

The profile covers exactly:

1. user interaction;
2. workspace filesystem;
3. terminal and tests;
4. tools, connectors, and network;
5. sub-agents;
6. task and thread state;
7. memory and retrieval; and
8. target runtime.

Each entry records the proposed host mechanism, capability and evidence state,
permission source, positive and denial-or-absence probe status, degraded or
blocked behavior, cancellation behavior, evidence capture, known limitations,
and review triggers. Pending or stale evidence never authorizes execution.

### 3.3 Permission precedence

The schema, profile, validator, and negative tests preserve this exact order:

`platform and system constraints -> host permissions -> project authorization -> bounded transaction permission envelope -> task objective`

Purpose, vision, values, role assignment, urgency, or efficiency cannot
override an earlier constraint. The host profile has no purpose, value,
approval, permission, requirement, or production authority.

## 4. Interface And Trust-Boundary Contract

The controlled integration document records, for every interface, the data
exchanged, direction, representation, cadence, owner, trust boundary, controls,
and missing-capability behavior. Retrieved content, tool results, commands,
connector data, and sub-agent results remain untrusted until verified.

External side effects remain distinct from local writes. Credentials are
referenced by mechanism only and cannot appear in the profile. Cancellation
and evidence capture are explicit interface obligations rather than inferred
host properties.

## 5. Validation Scope

`validate-host-capability-profiles` is a structural and consistency validator.
It checks schema conformance, the exact unique interface set, pending-gate
truthfulness, permission precedence, evidence freshness representation,
non-executable unknown or unavailable states, non-executable pending TX-09
binding, degraded and cancellation fields, secret absence, and resolution of
any future `verified_G_07` claim to a completed registered G-07 Director
Decision with non-self-approved human authorization evidence.

It cannot prove that a Codex feature exists, that a permission will be granted,
that cancellation is effective, that an external action is safe, or that a
host implementation conforms operationally. Those claims require `G-07`
observable or official evidence plus safe positive and denial-or-absence
probes.

The host-specific validator is implemented in TX-08 because WS-06 requires
executable permission-precedence and degraded-state evidence for this profile.
`TX-13` still owns the remaining strategic, PRD, lifecycle, capability-migration,
and cross-artifact validation families and their coordinated regression suite.

## 6. Validation Evidence

| Check | Result |
|---|---|
| Registered Codex profile against `host_capability_profile.schema.json` | PASS |
| `make validate-host-capability-profiles` | PASS; output states structural contract only and `G-07` open |
| Focused host-profile unit suite | PASS; 29 of 29 tests |
| Positive current-profile case | PASS; eight required interfaces, all `unknown` and non-executable |
| Negative and guard cases | PASS; 26 cases rejected invalid schema, missing or duplicate interfaces, invalid or false-verified states, pending or unregistered verification decisions, pending interface evidence, future or stale evidence, unknown or unavailable execution, executable pending or disabled TX-09 binding, missing evidence or controls, altered precedence, secret-like keys, and purpose/value authority |
| CLI and Make surface check | PASS; direct text/JSON command and aggregate target present |
| `make validate-config-sources` | PASS |
| `make validate-validation-contract-registry` | PASS |
| `make validate-toml-config` | PASS |
| `make validate-jsonschema-contracts` | PASS |
| `make validate-registry-graph` | PASS |
| `make validate-requirement-trace` | PASS; 214 Phase 0 and 128 Phase 1 requirements indexed with existing partial/scaffolded states preserved |
| Full product unit suite | PASS; 69 of 69 tests |
| Generated configuration, validation-contract, and governance checks | PASS; deterministic derivatives current |
| Root `make validate` | PASS |
| Python compilation and JSON CLI result | PASS |
| `git diff --check` | PASS |
| Source-first memory status | `PASS_WITH_WARNINGS`; 805 objects, 344 pending-hash warnings, zero authority inversions |

Warnings are the existing repository pending-hash debt plus the deliberately
open `G-07` and pending `TX-09` states. They are not host-capability claims or
validation failures.

## 7. Source-First And Authority Evidence

Source-first memory status passed with pending-hash warnings and zero authority
inversions. Targeted lookup located the controlled implementation plan and G-04
decision; their canonical files and registry rows were inspected directly.

No formal memory-preflight receipt was fabricated because the current receipt
contract still requires a historical AgentJob ID. TX-08 is a portable bounded
transaction, not an AgentJob.

## 8. Registry And Derivative Disposition

The existing configuration-source, validation-contract, source, and object-
relationship registries represent the profile contract without a new registry
or broad artifact-contract row. Generated reader surfaces remain noncanonical.

Generalized requirement-trace schema and full data migration remain assigned
to `TX-11` and `TX-12`. TX-08 refreshes only the existing `ID-005`, `ID-006`,
`ID-007`, and `VALUES-004` rows with exact profile, schema, document,
validator, test, and receipt evidence. They remain `partial` and `scaffolded`
because observable host verification and executable runtime evidence are absent.

## 9. Rollback And Residual Risk

Rollback is additive: remove the profile, schema, document, validator, tests,
CLI and Make integration, registry and relationship rows, and this receipt;
then regenerate the deterministic derivatives. Do not mutate G-04 or prior
completion evidence in place.

Residual risks:

- all eight host interfaces remain unverified until `G-07`;
- the portable execution contract remains unavailable until `TX-09`;
- host changes can invalidate later evidence and require review;
- schema and local tests cannot establish platform behavior or permission;
- the repository-wide pending-hash backlog limits global freshness claims.

## 10. Handoff

The drafted profile satisfies the entry condition for a separate `G-07`
observable host-verification transaction, but no host-dependent execution claim
may rely on it before that gate is accepted.

The next implementation transaction in plan order is
`TX-09-EXECUTION-CONTRACT`. It may define the harness-neutral portable
transaction contract under G-02 without treating this pending host profile as
an executable capability grant. `G-08` also remains open.

## References

Sys4AI-dev. (2026). *Sys4AI-dev strategic baseline migration full implementation plan* [Unpublished implementation plan].

Sys4AI-dev. (2026, July 10). *DDR-SFADEV-STRATEGIC-BASELINE-G04-001* [Director decision record].
