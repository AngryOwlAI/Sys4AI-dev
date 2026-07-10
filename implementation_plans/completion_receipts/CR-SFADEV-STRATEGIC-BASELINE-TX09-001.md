# Strategic Baseline Migration TX-09 Completion Receipt

- Receipt ID: `CR-SFADEV-STRATEGIC-BASELINE-TX09-001`
- Transaction: `TX-09-EXECUTION-CONTRACT`
- Workstream: `WS-08`, portable execution-contract slice only
- Entry gate: `G-02`, accepted by `DDR-SFADEV-STRATEGIC-BASELINE-001`
- Capability-migration gate: `G-05`, entry condition satisfied by this transaction but gate not accepted here
- Observable host-verification gate: `G-07`, open
- Plan: `implementation_plans/Sys4AI-dev_strategic_baseline_migration_full_implementation_plan.md`
- Result: `PASS_WITH_WARNINGS`
- Completion date: 2026-07-10
- Subject system: `Sys4AI-dev` development system and `Sys4AI` framework product
- Change class: additive portable contract baseline with fail-closed host-profile binding

## 1. Conclusion

`TX-09-EXECUTION-CONTRACT` defines version `1.0.0` of the harness-neutral
`ExecutionTransaction` structural contract and a controlled proposed-state
template. It implements the execution route selected by `G-02` without
restoring AgentJob authoring, `/continue`, the removed control-loop package, or
any retired CLI, Make, or runtime-test surface.

The contract is not an executor. Schema conformance does not grant authority,
prove that work ran, verify a host capability, or satisfy `G-07`. A proposed
record remains non-executable. An active record must carry current human
authorization, a current permission envelope, a nonpending execution profile,
verified required capabilities, and retained state-transition evidence.

The Codex reference-host profile now binds portable contract version `1.0.0`
but remains `draft_pending_G_07`. All eight interfaces remain `unknown`, every
`execution_allowed` value remains `false`, and
`portable_execution_contract_executable` remains `false`.

## 2. Authorization And Layer Boundaries

| Surface | Layer | Authority | TX-09 disposition |
|---|---|---|---|
| Execution schema, controlled template, contract tests, artifact row, validation row, source and configuration rows, relationships, and focused trace evidence | `framework_product` | Controlled framework sources authorized by G-02 and the current human instruction | Added as the portable contract baseline |
| Implementation plan and this receipt | `development_system` | Controlled transaction and completion evidence | Records the bounded change and later gate handoff |
| Generated validation, artifact-contract, and registry pages | `derivative_surface` | Noncanonical navigation | Regenerated deterministically from controlled rows |
| Codex reference-host profile and schema | `framework_product` host-integration surface | Controlled mapping only; platform and human authority remain external | Bound to version `1.0.0` without enabling execution or changing G-07 state |
| Historical AgentJob, continuation, handoff, state, plan, audit, and receipt evidence | Historical controlled evidence | Provenance only where it conflicts with the G-02 route | Preserved unchanged |
| Target-system instances | `target_system_instance` | Separate target authority | No target instance or production state changed |

This transaction does not migrate current program state, roles, execution
bindings, active policies, memory or handoff schemas, the full trace schema, or
the target package. Those writes remain assigned to later transactions and
gates.

## 3. Portable Execution Contract

### 3.1 Contract identity and artifact governance

- Contract schema: `Sys4AI/schemas/contracts/execution_transaction.schema.json`.
- Controlled template: `Sys4AI/templates/project/execution-transaction-template.yaml`.
- Contract version: `1.0.0`.
- Artifact contract ID: `artifact_execution_transaction`.
- Validation contract ID: `contract_execution_transaction`.
- Producer roles: `system_director` and `implementation_initialization_agent`.
- Consumer roles: `software_engineer`, `verification_engineer`, and `system_director`.
- Default authority: `controlled`; structural validity never implies activation.

The template is intentionally a valid `proposed` record with no authorization
evidence, no allowed writes, no allowed tools, no allowed external actions, and
unknown required host capabilities. Copying it cannot create permission.

### 3.2 Required contract surfaces

The schema requires:

- transaction identity, contract version, objective, source requirement IDs,
  and source decision IDs;
- subject system and system layer independently from runtime actor, role, and
  approval principal;
- explicit execution authorization and permission envelope;
- allowed reads, writes, tools, external actions, and data/resource limits;
- forbidden actions, inputs, expected outputs, blocking validators, and stop
  conditions;
- required host capabilities and their evidence state;
- current state, continuation state, state-transition evidence, cancellation,
  escalation, resume evidence, and closeout evidence; and
- rollback and supersession state.

The exact portable execution states are `proposed`, `authorized`, `active`,
`blocked`, `cancelled`, `completed`, `accepted`, and `superseded`.

### 3.3 Fail-closed activation and terminal-state rules

- `model_self_approval` and `self_authorized` must be `false`.
- `permission_expansion_allowed` and
  `values_or_goals_may_override` must be `false`.
- The permission envelope names its validity window, sensitive-data, secret,
  egress, external-side-effect, delegation, and delegation-expiry posture.
- `authorized` and `active` require current authorization, current permission,
  and accountable-principal authorization evidence.
- `active` additionally requires a nonpending execution profile, verified
  required capabilities, capability evidence, a current check timestamp, and
  state-transition evidence.
- `blocked` requires blocked continuation state, escalation, and transition
  evidence.
- `cancelled` requires an explicit cancellation outcome and evidence.
- `completed` requires closeout and validation evidence.
- `accepted` additionally requires acceptance evidence.
- `superseded` requires a replacement transaction and supersession evidence.

These are structural consistency rules. Operational freshness, permission,
host conformance, and semantic correctness require evidence outside the schema.

### 3.4 Threat and permission-scope review

| Material risk | Owner | Contract control | Verification | Residual classification |
|---|---|---|---|---|
| Model or runtime self-authorizes | Accountable human principal and `system_director` | Human-only principal type; `model_self_approval = false`; `self_authorized = false`; retained authority evidence | Negative contract tests | Mitigated structurally; runtime enforcement deferred |
| Placeholder actor or principal reaches execution | `system_director` | Authorized, active, completed, and accepted records reject pending subject, actor, principal, or host-profile identities | Positive active fixture and negative placeholder tests | Mitigated structurally |
| Unknown, denied, or stale capability is treated as executable | `verification_engineer` | Active state requires `verified_available`, current check time, and capability evidence; completed state retains verified or later-stale evidence | Active and completed positive/negative tests | Mitigated structurally; G-07 operational proof deferred |
| Tool or external side effect escapes scope | Approval principal and runtime operator | Explicit tool and external-action allowlists; external actions require `external_side_effects_allowed = true`; all other actions remain forbidden | Negative external-action test and schema review | Mitigated structurally; executor enforcement deferred |
| Sensitive data, secrets, or egress are implicit | Approval principal and security reviewer | Explicit data classes plus sensitive-data, secret, and egress flags; secret access requires sensitive-data permission | Negative secret-scope test | Mitigated structurally; data-flow inspection deferred |
| Delegation persists or silently expands | Approval principal | Explicit delegation flag and mandatory expiry when enabled; permission expansion is always false | Negative delegation and permission-expansion tests | Mitigated structurally; expiry comparison deferred |
| Cancellation leaves uncertain side effects | Runtime operator and approval principal | Safe-stop behavior, uncertain-operation list, cancellation evidence, escalation, and rollback fields | Negative cancelled-state test | Mitigated structurally; host cancellation behavior deferred to G-07 |
| Claimed completion lacks retained execution proof | `verification_engineer` and accepter | Completed and accepted states require authorization, permission time bounds, host evidence, transition evidence, validation, closeout, and acceptance evidence | Positive completed fixture and negative closeout/capability/acceptance tests | Mitigated structurally |

Timestamp ordering, expiry-at-validation-time, exact path/tool semantics, secret
scanning of instantiated records, and operational enforcement remain deferred to
the focused validator work assigned to `TX-13` and to applicable host evidence.

## 4. Compatibility And Host Boundary

The schema and template contain no Codex-specific mechanics, AgentJob field,
or `/continue` command. Host-specific mappings remain isolated in registered
host profiles. Historical AgentJob schemas and records remain available for
provenance and were not deleted or rewritten.

The Codex profile advances from a `pending_TX_09` contract pointer to version
`1.0.0`. The profile itself remains non-executable because `G-07` observable
verification has not occurred. The host-profile schema now permits a completed
portable contract version while a profile remains pending G-07 but still
requires `portable_execution_contract_executable = false` in that state.

The TX-08 receipt is immutable historical evidence of the then-current pending
TX-09 fact. Current routing uses the live profile, source registry, relationship
registry, this receipt, and the G-02 decision.

## 5. Validation Scope

`test_execution_transactions.py` checks the schema and controlled template
without creating a runtime validator or CLI surface assigned to `TX-13`. It
includes positive proposed and active fixtures plus negative cases for missing
contract surfaces, unknown keys, duplicate scope, invalid layers, self-
approval, permission expansion, unknown or unevidenced required capabilities,
unsafe active state, incomplete cancellation, incomplete closeout, missing
acceptance, and incomplete supersession.

Host-profile tests separately confirm the live profile binds version `1.0.0`
while all host execution remains disabled. Validation does not simulate or
accept observable host behavior.

## 6. Validation Evidence

| Check | Result |
|---|---|
| `execution_transaction.schema.json` Draft 2020-12 metaschema check | PASS |
| Controlled proposed template against execution schema | PASS |
| Focused execution-contract unit suite | PASS; 36 of 36 tests |
| Focused host-profile unit suite | PASS; 30 of 30 tests |
| Positive active-state fixture | PASS only with explicit authorization, permission, verified capability, and transition evidence |
| Negative and guard cases | PASS; unsafe or incomplete identity, authorization, permission time, delegation, data, external-action, capability, state, cancellation, closeout, acceptance, and supersession mutations rejected |
| `make validate-artifact-contracts` | PASS |
| `make validate-config-sources` and `make validate-toml-config` | PASS |
| `make validate-validation-contract-registry` | PASS |
| `make validate-host-capability-profiles` | PASS; structural contract only and `G-07` remains open |
| `make validate-jsonschema-contracts` | PASS |
| `make validate-registry-graph` | PASS |
| `make validate-requirement-trace` | PASS; 214 Phase 0 and 128 Phase 1 requirements indexed with existing partial and scaffolded states preserved |
| Full product unit suite | PASS; 106 of 106 tests |
| Generated validation-contract and governance checks | PASS; four changed indexes and all deterministic derivatives current |
| Root `make validate` | PASS |
| Python compilation and `git diff --check` | PASS |
| Source-first memory status | `PASS_WITH_WARNINGS`; 810 objects, 345 pending-hash warnings, zero authority inversions after TX-09 registration |

The remaining warnings are the repository pending-hash backlog and the
deliberately open G-07 and active-surface migration states. They are not
execution or host-capability claims.

## 7. Source-First And Trace Evidence

Source-first memory status passed with pending-hash warnings and zero authority
inversions. Exact TX-09 lookup returned no registered object before the
transaction was created. The controlled implementation plan, G-02 decision,
Phase 1 requirements, live registries, and TX-08 profile evidence were
therefore inspected directly and now own the completion evidence.

No formal memory-preflight receipt was fabricated because the current receipt
contract still requires a historical AgentJob ID. TX-09 is a portable bounded
transaction rather than an AgentJob.

The existing trace rows for `ID-004`, `ID-007`, `AJ-001`, `AJ-002`, `AJ-003`,
and `SFA-P0-FR-017` now cite the exact schema, template, tests, G-02 decision,
and this receipt. They remain `partial` and `scaffolded`: contract structure
exists but an authorized runtime and migrated active surfaces do not.

Full trace-schema generalization and all-row migration remain assigned to
`TX-11` and `TX-12`.

## 8. Registry And Derivative Disposition

The configuration-source, artifact-contract, validation-contract, source,
object-relationship, and requirement-trace registries carry the new contract
and host binding without a new registry.
Generated reader surfaces remain noncanonical and must be regenerated from
these rows rather than edited by hand.

## 9. Rollback And Residual Risk

Rollback is additive: remove the execution schema, template, tests, artifact
row, validation row, source rows, relationships, focused trace changes, and
this receipt; restore the prior host-profile version binding and host-profile
schema condition; then regenerate deterministic derivatives. Historical
AgentJob and TX-08 evidence remain unchanged in either direction.

Residual risks:

- no execution engine consumes the contract yet;
- all Codex host capabilities remain unverified until `G-07`;
- program state, roles, bindings, policies, memory, handoffs, and legacy active
  references remain unmigrated until their assigned transactions;
- schema tests establish structural consistency rather than semantic truth,
  operational freshness, safety, or execution success; and
- the repository-wide pending-hash backlog limits global freshness claims.

## 10. Handoff

TX-09 satisfies the entry condition for `G-05` capability-migration safety and
makes `TX-11-TRACE-SCHEMA` dependency-ready. `TX-10-ACTIVE-SURFACE-MIGRATION`
must not begin until `G-05` is accepted and its stale-reference classification
and boundary-protection disposition are explicit.

Separately, `G-07` remains eligible for observable host verification because
the host profile is drafted. No host-dependent execution claim may precede
accepted G-07 evidence, and TX-09 contract conformance does not substitute for
that gate.

## References

Sys4AI-dev. (2026). *Sys4AI Phase 1 implementation initialization product requirements document* [Unpublished product requirements document].

Sys4AI-dev. (2026). *Sys4AI-dev strategic baseline migration full implementation plan* [Unpublished implementation plan].

Sys4AI-dev. (2026, July 9). *DDR-SFADEV-STRATEGIC-BASELINE-001* [Director decision record].
