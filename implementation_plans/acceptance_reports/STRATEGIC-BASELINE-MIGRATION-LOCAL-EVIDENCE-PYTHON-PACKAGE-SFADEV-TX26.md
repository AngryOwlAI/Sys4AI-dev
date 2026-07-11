# TX-26 Local Evidence: Python Reference And Package Surface

## Conclusion

`TX-26-LOCAL-EVIDENCE-PYTHON-PACKAGE` verifies the four dependency-ready Python/package obligations `SFA-CORE-PY-001`, `SFA-CORE-PY-002`, `SFA-CORE-PY-003`, and `SFA-P0-NFR-015`. Their verification states advance from `planned` to `pass`; capability remains `implemented`, coverage remains `covered`, and no waiver is used.

This packet is additive to the frozen TX-23 ledger and the completed TX-24 semantic evidence. It does not execute the remaining 63 local verification obligations, change the 410 TX-25 future-work dispositions, obtain external evidence, accept `G-10`, or grant production, operational, stakeholder, domain, target-runtime, or permission authority.

## Authority And Baseline

- Accountable authorization: the user authorized the smallest bounded Python/package-surface verification family on 2026-07-11.
- Gate decision: `DDR-SFADEV-STRATEGIC-BASELINE-G11-003`.
- Entry commit and shared baseline: `4fa003b068c41ec14a05e18a5b77b477b9f17603`.
- Entry handoff: `HANDOFF-SFADEV-STRATEGIC-BASELINE-TX25-001`.
- Memory preflight: `MEMPREFLIGHT-TX-26-LOCAL-EVIDENCE-PYTHON-PACKAGE-20260711T171757Z`, `PASS_WITH_WARNINGS`, zero authority inversions.
- Frozen TX-23 ledger SHA-256: `1e9e2b2a0a7bc4f589addd65b8d34642899a3f812e7ce35be6e62a2c0fcc6138`.
- Frozen TX-25 interpretation SHA-256: `9ed89d6ff5872ee2fb2b740791c268d9048e97f31eae8ff7d3b4d2d8929d5f38`.
- Subject layer: `framework_product`; the development checkout supplies tests and evidence, while generated readers remain noncanonical.

## Verification Method

The focused validator parses `Sys4AI/pyproject.toml`, compares it byte-semantically with `Sys4AI/requirements.txt`, checks the declared package entry point and package discovery, requires the current reference modules and structured-control roots, and executes import probes through both `.venv/bin/python` and an activated-environment `python` resolved from `.venv/bin`.

Negative tests reject an extra heavy or unbounded dependency, dependency-file drift, and a missing reference module. The active local environment was rebuilt from the installed Python 3.12 interpreter because the prior ignored `.venv` used Python 3.9, below the declared `>=3.10` support range.

## Evidence Disposition

| Requirement | Executed evidence | Disposition |
|---|---|---|
| `SFA-CORE-PY-001` | Package metadata, reference modules, control/config/schema roots, focused validator, and negative tests | Python reference implementation surface verified. |
| `SFA-CORE-PY-002` | `requires-python = ">=3.10"`; exact bounded dependency parity across pyproject and requirements | Supported-version and dependency policy verified. |
| `SFA-CORE-PY-003` | Direct `.venv/bin/python` import probe and activated-PATH `python` import probe under Python 3.12 | Both interpreter invocation modes verified. |
| `SFA-P0-NFR-015` | Architecture-policy check allowing exactly PyYAML, conditional tomli, and jsonschema; negative extra-dependency test | Lightweight deterministic parser/validator dependency boundary verified. |

## Results And Boundaries

- Focused validator: `4/4` passed.
- Focused positive/negative unit suite: `5/5` passed.
- Focused control, evidence, trace, and acceptance suite: `66/66` passed.
- Full product unit suite: `266/266` passed.
- Repository-root aggregate validation: passed.
- Verification state: `pass` increases from 27 to 31; `planned` decreases from 200 to 196.
- Remaining locally executable verification obligations: 63.
- Capability and coverage states for the four rows: unchanged at `implemented` and `covered`.
- Trace waiver fields: unchanged and empty.
- Accepted waivers: 0.
- `G-10`: deferred and not accepted.
- Memory status: `PASS_WITH_WARNINGS`; 1097 objects, 489 known pending-hash warnings, zero authority inversions.

The package-surface checks prove the current local reference scaffold and dependency declarations. They do not prove compatibility on every supported Python minor version, package publication, production deployment, runtime operations, stakeholder acceptance, or target-domain fitness.

## Rollback And Supersession

Before publication, revert the complete TX-26 packet. The ignored prior Python 3.9 environment is retained temporarily outside the worktree at `/tmp/Sys4AI-dev-venv-py39-20260711` for local rollback. After publication, preserve G-11-003, the four additive evidence rows, trace verification evidence, report, transaction, receipt, and handoff as activated history; use a new bounded transaction for any later family.

## References

AngryOwlAI. (2026, July 9). *Sys4AI-dev strategic baseline migration full implementation plan* [Implementation plan].

Sys4AI-dev. (2026a, July 11). *Strategic baseline migration evidence closure plan* [Implementation plan].

Sys4AI-dev. (2026b, July 11). *TX-25 controlled plan interpretation* [Acceptance report].
