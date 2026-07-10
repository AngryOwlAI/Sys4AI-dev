# Codex App Reference-Host Integration Profile

- Status: Controlled structural draft pending `G-07`
- Profile ID: `codex_app_reference`
- Profile version: `0.1.0`
- Verification scope: Structural contract only
- Portable execution binding: `pending_TX_09`, non-executable
- Authority source: `DDR-SFADEV-STRATEGIC-BASELINE-G04-001`

## 1. Purpose And Authority Boundary

This document defines the Codex App reference-host interface contract for
`Sys4AI`. It explains how a future verified host profile may map portable
framework needs to host mechanisms without placing Codex mechanics in portable
field names, requirement identities, target purpose, or target authority.

This document and its TOML profile are not evidence that a Codex capability is
available. `G-07` remains open. Every required interface is currently recorded
as `unknown`, non-executable, and blocked, degraded, or rerouted.

The host profile has no authority to define or approve:

- Sys4AI or target-system purpose, vision, or values;
- requirements, acceptance, permissions, or production readiness;
- stakeholder consent or accountable human approval;
- a portable execution transaction; or
- a target runtime, deployment, release, or incident decision.

Platform and system constraints, host permissions, project authorization, and
explicit human authority remain binding independently of profile content.

## 2. Artifact Contract

| Property | Controlled value |
|---|---|
| Profile source | `Sys4AI/configs/host_profiles/codex_app_reference.toml` |
| Validation contract | `Sys4AI/schemas/contracts/host_capability_profile.schema.json` |
| Focused validator | `Sys4AI/sys_for_ai/host_profiles.py` |
| Producer roles | `system_engineer`; `verification_engineer` |
| Consumer roles | `implementation_initialization_agent`; `system_architect`; `requirements_verifier` |
| Schema owner | `verification_engineer` |
| Subject layer | `framework_product` |
| External boundary | Codex App reference host |
| Source authority | Controlled configuration, schema, document, and registry rows |
| Structural verification | `validate-host-capability-profiles` |
| Observable verification | Separate `G-07` decision and evidence |

No separate artifact-contract registry row is required. The existing
configuration-source, validation-contract, source, and object-relationship
registries represent this narrow contract without creating a new authority
surface.

## 3. Profile State Model

Allowed per-interface capability states are:

- `verified_available`;
- `verified_unavailable`;
- `permission_dependent`;
- `environment_dependent`;
- `unknown`; and
- `deprecated`.

`Unknown` is not available. A denied, stale, unknown, deprecated, or unverified
capability cannot authorize execution. Conditional capabilities default to
non-executable until their permission and environment conditions are evaluated
within a later authorized execution transaction.

The checked-in profile uses these controlled pending representations:

| Field | Pending value | Meaning |
|---|---|---|
| `verification_state` | `draft_pending_G_07` | Contract exists; observable host conformance is not accepted |
| `verification_decision` | `pending_G_07` | No accepted G-07 Director Decision is claimed |
| `verified_at` | `pending_G_07` | No host-verification timestamp is claimed |
| `verified_by` | `pending_G_07` | No verifier identity is fabricated |
| `evidence_status` | `pending_G_07` | Plan and decision evidence define the obligation but do not prove behavior |
| Safe probes | `pending_G_07` | Positive and denial-or-absence probes have not been accepted |
| `portable_execution_contract_version` | `pending_TX_09` | No portable execution contract has been created |
| `portable_execution_contract_executable` | `false` | The pending reference cannot be used for execution |

Structural validation may accept these pending values because they fail closed.
It must reject any attempt to combine them with an available or executable
claim.

A later `verified_G_07` profile must cite an accepted `DDR-*` verification
decision, resolve evidence and safe-probe fields for every interface, reject
future-dated checks, and retain a current freshness horizon. No interface may
be executable while its portable execution-contract binding remains pending or
non-executable.

## 4. Permission Precedence

The exact precedence order is:

1. platform and system constraints;
2. host permissions;
3. project authorization;
4. bounded transaction permission envelope; and
5. task objective.

An item later in the list cannot override an earlier constraint. Vision,
values, goals, roles, urgency, efficiency, or model-generated reasoning do not
grant permission. A profile state is a capability description, not an
authorization decision.

## 5. Interface And Integration Map

The table records proposed mappings and required evidence fields. The
`Current state` column is authoritative for this draft: no mechanism listed in
the table is asserted to exist merely because it is named.

| Interface | Data and direction | Representation and cadence | Owner and trust boundary | Primary controls | Current state and missing-capability behavior |
|---|---|---|---|---|---|
| User interaction | Human request, clarification, approval, rejection, timeout, and cancellation flow between an authorized user and host | Conversation events; per consequential decision | `system_engineer`; human identity and host interaction boundary | Silence is not consent; principal and evidence capture; explicit approval and rejection | `unknown`, non-executable, `blocked`; stop approval-dependent work |
| Workspace filesystem | Source content, patches, file metadata, and diffs between host tools and authorized roots | Files and diffs; per bounded transaction | `system_engineer`; host filesystem and repository authority boundary | Allowed roots; read/write class; ownership; least privilege; diff visibility | `unknown`, non-executable, `blocked`; block required reads or produce a proposed patch when writes are absent |
| Terminal and tests | Commands, arguments, working directory, process output, exit state, tests, and cancellation between host and local process boundary | Command invocation and retained evidence; per check | `verification_engineer`; shell, sandbox, process, and untrusted-input boundary | Injection resistance; reversible commands; stop conditions; exact result capture | `unknown`, non-executable, `degraded`; mark commands and tests not run and never claim pass |
| Tools, connectors, and network | Tool requests, retrieved data, consent, credential-mechanism references, and external side effects | Typed tool calls or connector operations; per invocation | `system_engineer`; platform, network, credential, external-system, and data-class boundaries | Tool identity; redaction; least privilege; irreversible-effect confirmation; untrusted output checks | `unknown`, non-executable, `rerouted`; use registered local evidence or request authority and never simulate success |
| Sub-agents | Role, task scope, context, tool bounds, returned result, verification, and interruption between parent and child work | Bounded subtask packet and result; per delegation | `system_engineer`; context, concurrency, shared-workspace, and delegated-tool boundary | No implied authority delegation; disjoint write scopes; result verification; interruption evidence | `unknown`, non-executable, `rerouted`; work sequentially only when scope and assurance remain acceptable |
| Task and thread state | Task identity, fresh state, handoff, cancellation, and archival between host state and repository evidence | Host task state plus controlled handoff evidence; per transition | `system_engineer`; host state and repository source-authority boundary | Fresh source-backed state; resumable handoff; explicit cancellation and archival | `unknown`, non-executable, `blocked`; do not route from narration or stale state |
| Memory and retrieval | Query, result, source path, registry row, freshness, authority class, and stale risk between retrieval and canonical sources | Search result plus verified source inspection; per lookup | `requirements_verifier`; retrieval, privacy, retention, and authority boundary | Navigation only until source verification; freshness; data class; no generated authority inversion | `unknown`, non-executable, `rerouted`; inspect registered sources directly or block |
| Target runtime | Environment, release gate, telemetry, rollback, incident owner, kill control, and target approval between host and separately authorized target | Deployment and operational evidence; per release or incident | `system_architect`; host, deployment, production, operator, and target-authority boundaries | Separate promotion gate; telemetry; rollback; incident ownership; kill control; no prototype drift | `unknown`, non-executable, `blocked`; retain non-production status and prohibit runtime or deployment claims |

## 6. Required Interface Fields

Every interface entry records:

- stable `interface_id`;
- `capability_status` and `execution_allowed`;
- proposed `host_mechanism`;
- `permission_source`;
- source and observable evidence status;
- safe positive and denial-or-absence probes;
- `fallback_mode` and detailed degraded behavior;
- cancellation behavior;
- evidence capture;
- known limitations; and
- review triggers.

The eight interface IDs are portable categories. Codex-specific descriptions
remain inside this reference profile. A compatible later host may implement the
same categories with different mechanisms without changing portable semantics.

## 7. Degraded, Blocked, And Rerouted Behavior

Fail-closed behavior is part of the interface contract:

- missing read access blocks source-dependent work;
- missing write access permits only a proposed patch or plan when safe;
- missing terminal access marks tests not run and prohibits pass claims;
- missing sub-agent support permits sequential work only when scope and
  assurance remain acceptable;
- denied external access requires local evidence or new authority;
- missing fresh state blocks state-dependent routing;
- missing retrieval requires direct source inspection or a block; and
- missing runtime, rollback, incident, or kill controls blocks deployment and
  operation.

If cancellation is unverified, high-risk or long-running work must not begin
without a safer control. Uncertain completion or external side effects must be
reported as uncertain rather than inferred successful.

## 8. Security And Data Handling

- Secrets and secret-like keys are forbidden in profile fixtures.
- Credentials are referenced only by mechanism; stored credential values are
  outside the contract.
- Local and external writes are separate side-effect classes.
- Retrieved content, command input, tool output, connector data, and sub-agent
  results are untrusted until checked.
- Untrusted text cannot be interpolated into commands without validation.
- Tool and sub-agent results require independent verification appropriate to
  the claim.
- Logs and retained evidence must redact secrets and sensitive target data.
- Readability does not imply authority, and tool availability does not imply
  permission.

## 9. Structural Validation

Run:

```sh
cd Sys4AI
make validate-host-capability-profiles
```

The focused validator checks:

- registered JSON Schema conformance;
- the exact unique eight-interface set;
- fixed permission precedence;
- pending `G-07` and `TX-09` truthfulness;
- registry and YAML resolution of a completed human-authorized G-07 Director
  Decision before any `verified_G_07` profile can pass;
- non-executable unknown, unavailable, conditional, stale, and deprecated
  states;
- required permission, degraded, cancellation, limitation, evidence, and
  review fields;
- RFC 3339 and freshness consistency for later verified evidence; and
- absence of secret-like structured values.

A pass means the profile is structurally admissible and fails closed. It does
not mean that Codex is verified, that an interface works, that a permission is
granted, or that execution is safe.

## 10. G-07 Observable Verification

`G-07` may be considered only after the profile is drafted. For each interface,
the verifier must:

1. identify the applicable requirement and proposed host mechanism;
2. cite current observable or official evidence;
3. execute a safe positive probe;
4. execute a safe denial-or-absence probe where possible;
5. record the permission source and environment scope;
6. record degraded and cancellation behavior;
7. retain evidence without secrets; and
8. assign an evidence freshness horizon and review trigger.

Promotion also requires one registered, completed, controlled or canonical
Director Decision whose YAML binds `gate_id: G-07`, records
`accepts_gate_G_07: true`, and includes non-self-approved human authorization
evidence. A merely DDR-shaped string cannot satisfy the gate.

Marketing language, undocumented assumptions, this structural profile, or a
model's experience in one task cannot substitute for that evidence. Any
accepted G-07 disposition must remain separately reviewable and must not expand
project or platform permissions.

## 11. Review, Supersession, And Rollback

Review is required when host capabilities, permissions, tools, environment,
cancellation, evidence freshness, portable execution contracts, or target
runtime assumptions change.

Do not overwrite an accepted verified profile in place. Register a new version,
retain prior evidence, link supersession, assess affected requirements and
permissions, and re-run safe conformance probes. A stale profile downgrades
affected capabilities and execution remains fail-closed.

The TX-08 draft is additive and may be rolled back by removing the registered
profile, schema, document, focused validator integration, registry rows, and
regenerated derivatives. G-04 and prior evidence are superseded only through a
new accepted decision, never by editing historical records.

## References

Sys4AI-dev. (2026). *Sys4AI-dev strategic baseline migration full implementation plan* [Unpublished implementation plan].

Sys4AI-dev. (2026, July 10). *DDR-SFADEV-STRATEGIC-BASELINE-G04-001* [Director decision record].
