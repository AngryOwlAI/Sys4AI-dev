# TX-31 Local Evidence: TOML Configuration Governance

## Conclusion

`TX-31-LOCAL-EVIDENCE-TOML-CONFIG` verifies exactly `SFA-CORE-TOML-001` through `SFA-CORE-TOML-007`, `SFA-P0-FR-034`, and `SFA-P0-FR-043`. Their verification states advance from `planned` to `pass`; capability remains `implemented`, coverage remains `covered`, semantic review remains `sufficient`, and no waiver is used.

The user also authorized later external-evidence, cross-version-CI, `G-10`, production-readiness, and operational-authority work. That authorization permits later bounded planning; it is not executed evidence and does not make those claims true inside TX-31.

## Authority And Baseline

- Accountable authorization: the user explicitly authorized all items in the quoted TOML and retained-gate boundary on 2026-07-12.
- Gate decision: `DDR-SFADEV-STRATEGIC-BASELINE-G11-008`.
- Entry commit and shared baseline: `dc923d03a2a852f1595eff994aa31f9c163ef447`.
- Entry handoff: `HANDOFF-SFADEV-STRATEGIC-BASELINE-TX30-001`.
- Memory preflight: `MEMPREFLIGHT-TX-31-LOCAL-EVIDENCE-TOML-CONFIG-20260712T130256Z`, `PASS_WITH_WARNINGS`, zero authority inversions.
- Frozen TX-23 ledger SHA-256: `1e9e2b2a0a7bc4f589addd65b8d34642899a3f812e7ce35be6e62a2c0fcc6138`.
- Frozen TX-25 interpretation SHA-256: `9ed89d6ff5872ee2fb2b740791c268d9048e97f31eae8ff7d3b4d2d8929d5f38`.
- Subject layer: `framework_product`; the Configuration and Control Wiki remains a generated noncanonical derivative.

## Verification Method

The focused validator requires the governed TOML format assignment, complete unique configuration registry rows, existing `.toml` sources, dictionary-like parsed roots, TOML-targeting validation contracts, Python 3.11+ `tomllib` with the retained conditional Python 3.10 `tomli` fallback, a parse-only TOML API, secrets-disabled policy, retained YAML example secret checks, and a current noncanonical generated TOML index.

Negative probes reject format-assignment drift, missing ownership, parser substitution, secret-policy expansion, secret-like TOML values, wrong contract formats, stale generated indexing, and TOML writer APIs.

## Evidence Disposition

| Requirement | Executed evidence | Disposition |
|---|---|---|
| `SFA-CORE-TOML-001` | Format profile, policy, registry, and source audit | TOML is verified as the governed core configuration format. |
| `SFA-CORE-TOML-002` | Size-limited parsing of every source to a mapping | Human-readable TOML sources parse deterministically to dictionary-like structures. |
| `SFA-CORE-TOML-003` | Complete registry-field and contract-binding checks | Every source has governed path, domain, owner, authority, parser, contract, consumer, environment, secret, supersession, and metadata fields. |
| `SFA-CORE-TOML-004` | Dependency and parser-source inspection | Python 3.11+ uses `tomllib`; retained Python 3.10 uses conditional `tomli`. |
| `SFA-CORE-TOML-005` | AST parse-only API check and writer negative | Phase 1 exposes parsing and validation without TOML writing or style-preserving editing. |
| `SFA-CORE-TOML-006` | Secret scan and secrets-disabled registry checks | TOML examples reject secret-like keys and private-key blocks. |
| `SFA-CORE-TOML-007` | Deterministic generated-page freshness and coverage check | Every registered TOML source is indexed through a noncanonical generated reader. |
| `SFA-P0-FR-034` | Exact profile and policy assignment | TOML is assigned to project, package, tool, runtime, framework, and target-system configuration. |
| `SFA-P0-FR-043` | TOML secret scan plus retained YAML control-record validation | Governed YAML and TOML examples do not contain secrets by default. |

## Results And Boundaries

- Focused validator: `9/9` requirements passed.
- Focused positive/negative suite: `10/10` tests passed.
- Full product suite: `307/307` tests passed.
- Product and repository-root `make validate`: passed.
- Verification state: `pass` increases from 61 to 70; `planned` decreases from 166 to 157.
- Local evidence registry: 50 accepted rows total; 24 local verification obligations remain.
- Capability and coverage remain `implemented` and `covered`.
- Trace waiver fields remain empty; accepted waivers remain 0.
- `G-10` remains deferred and not accepted because retained evidence closure is incomplete.
- Final memory status: `PASS_WITH_WARNINGS`; 1,193 objects, 536 known pending-hash warnings, zero derivative authority inversions.

These checks prove current local TOML assignment, registration, parsing, schema binding, parse-only scope, example secret policy, and generated-reader freshness. They do not prove external truth, target-runtime operations, production fitness, stakeholder consensus, cross-version Python execution, or operational readiness.

## Rollback And Supersession

Before publication, revert the complete TX-31 packet. After publication, preserve G-11-008, the nine additive evidence rows, trace verification evidence, report, transaction, receipt, and handoff as activated history; use new bounded transactions for later evidence families.

## References

AngryOwlAI. (2026, July 9). *Sys4AI-dev strategic baseline migration full implementation plan* [Implementation plan].

Sys4AI-dev. (2026a, July 11). *Strategic baseline migration evidence closure plan* [Implementation plan].

Sys4AI-dev. (2026b, July 12). *TX-30 local evidence: Markdown source authority* [Verification report].
