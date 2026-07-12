# TX-33 Local Evidence: Generated Reader Surfaces

## Decision

`TX-33-LOCAL-EVIDENCE-GENERATED-READERS` verifies exactly `SFA-CORE-CCWIKI-001` through `SFA-CORE-CCWIKI-005`, `SFA-CORE-VCCAT-001` through `SFA-CORE-VCCAT-005`, `SFA-P0-FR-037`, `SFA-P0-FR-038`, `SFA-P0-FR-044`, and `SFA-P0-NFR-017`. Their verification states advance from `planned` to `pass`; capability remains `implemented`, coverage remains `covered`, semantic review remains `sufficient`, and no waiver is used.

External evidence, cross-version CI, `G-10`, production readiness, stakeholder or domain truth, target-runtime operation, permission expansion, and operational authority remain unproven. Local verification closure does not make those claims true.

## Authority and baseline

- Accountable authorization: the user explicitly authorized the quoted fourteen-row generated-reader family on 2026-07-12.
- Scope decision: `DDR-SFADEV-STRATEGIC-BASELINE-G11-010`.
- Input handoff: `HANDOFF-SFADEV-STRATEGIC-BASELINE-TX32-001`.
- Memory preflight: `MEMPREFLIGHT-TX-33-LOCAL-EVIDENCE-GENERATED-READERS-20260712T142441Z`, `PASS_WITH_WARNINGS`, zero authority inversions.
- Frozen TX-23 SHA-256: `1e9e2b2a0a7bc4f589addd65b8d34642899a3f812e7ce35be6e62a2c0fcc6138`.
- Frozen TX-25 SHA-256: `9ed89d6ff5872ee2fb2b740791c268d9048e97f31eae8ff7d3b4d2d8929d5f38`.
- Canonical Phase 0 and Phase 1 PRDs remain unchanged.

## Verification design

The focused validator requires exact YAML, TOML, and JSON Schema format-profile assignments; complete registered source IDs, source paths, and validation-contract links; five exact derivative registrations; deterministic current pages; noncanonical authority banners; format, registry, contract, hash, generator, time, validation, freshness, and promotion metadata; complete per-contract catalog fields; and links from every declaring artifact-contract, configuration-source, and control-record row.

Negative probes reject missing profiles, missing canonical sources, unknown contracts, canonical derivative registration, mirrors outside the generated root, standalone JSON-wiki registration, unlinked declaring rows, and weakened mirror policy. A registry-driven generation probe confirms a future validation-contract format is cataloged without generator code specialization.

## Requirement dispositions

| Requirement family | Evidence method | Disposition |
| --- | --- | --- |
| `SFA-CORE-CCWIKI-001..005` | Generator, derivative registry, policy, deterministic freshness, source/contract trace, and negative mirror/authority checks | YAML and TOML reader pages are complete, current, noncanonical, and fail closed on missing or promoted evidence. |
| `SFA-CORE-VCCAT-001..005` | Registry-driven generator, complete entry-field checks, declaration-link audit, policy, and no-wiki probes | Current and future registered contract formats are cataloged with full metadata and declaring-row trace, without creating a JSON wiki. |
| `SFA-P0-FR-037` | Configuration/control generated-page inspection and focused validator | The YAML/TOML wiki is derivative, registry-traced, hash-aware, and stale-checkable. |
| `SFA-P0-FR-038` | Validation-catalog generated-page inspection and focused validator | The JSON Schema catalog is derivative, contract-traced, target-aware, and registry driven. |
| `SFA-P0-FR-044` | Shared page-template and page-content audit | Every generated reader has an authority banner and source trace. |
| `SFA-P0-NFR-017` | Policy, promotion-path, registry-status, and negative authority tests | Reader surfaces remain subordinate to registered sources, registries, and contracts. |

## Executed validation

- Focused validator: 14/14 requirements passed.
- Focused positive/negative tests: 11/11 passed.
- Full product tests: 329/329 passed.
- Trace: 227 rows; `pass=94`, `planned=133`; semantic review `sufficient=227`.
- Local evidence: 74 accepted rows; zero local verification obligations remain.
- Product and repository-root `make validate`: passed.
- Memory: `PASS_WITH_WARNINGS`; 1,229 objects, 554 known pending-hash warnings, zero derivative authority inversions.
- Frozen TX-23 and TX-25 hashes: unchanged.
- Accepted waivers: zero.

## Limitations

These checks prove current local generated-reader assignment, completeness, deterministic freshness, declaration trace, noncanonical authority, and promotion boundaries. They do not prove external truth, cross-version execution, target-runtime operations, production fitness, stakeholder consensus, domain validity, or operational readiness.

## Rollback and next gate

Before publication, revert the complete TX-33 packet. After publication, preserve G-11-010, the fourteen additive evidence rows, trace verification evidence, report, transaction, receipt, and handoff as activated history; use a new bounded transaction for retained external evidence.

The local verification family is exhausted. The next dependency-ready transaction must be selected from the retained external evidence obligations, and `G-10` remains deferred until that evidence is executed and accountably accepted.
