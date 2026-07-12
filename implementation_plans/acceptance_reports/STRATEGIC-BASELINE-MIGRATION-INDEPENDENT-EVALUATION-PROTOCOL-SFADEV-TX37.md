# TX-37 Independent, Confidential, Rotated Evaluation Protocol Readiness

## Conclusion

`TX-37-INDEPENDENT-ROTATED-EVALUATION-PROTOCOL` is complete at the protocol-readiness boundary. The controlled contract specifies evaluator independence, confidential holdout protection, mandatory rotation, complete value/scenario coverage, exact scoring, result-receipt fields, and permission limits.

No independent evaluation was executed. No evaluator was selected, no confidential holdout suite was created or transferred, and no external side effect or data egress was authorized.

## Scope And Layer

The subject is the Sys4AI framework product's deterministic self-change safety-control interface, `sys_for_ai.safety_evaluation.evaluate_candidate`. TX-37 changes controlled framework/development-system protocol, validation, test, and control surfaces. It does not change a generated target, production runtime, canonical PRD, requirement trace state, or target-domain artifact.

## Protocol

- External evaluator class: independent human or organization.
- Prohibited evaluator identities: the Codex runtime, the accountable repository principal, and the repository-local deterministic evaluator.
- Confidential suite: external, absent from this repository, committed by SHA-256 before execution.
- Rotation: no reuse; rotate after material change, escaped failure, suspected gaming/disclosure, or rubric change.
- Coverage: all eight values across positive, negative, and conflict scenarios; at least 24 scenarios.
- Threshold: 100% exact outcome and reason-code matches; zero unexpected accepts.
- Result: a later external receipt must bind evaluator identity and attestations, evaluated commit and artifact hash, holdout commitment, rotation ID, counts, environment, deviations, and limitations.

## External Prerequisites

| ID | Status | Required evidence |
|---|---|---|
| `IEP-PREREQ-001` | Complete | Controlled protocol, schema, validator, tests, and G-11-014 decision. |
| `IEP-PREREQ-002` | Blocked | Named independent evaluator and conflict-of-interest attestation. |
| `IEP-PREREQ-003` | Blocked | Confidential external suite and pre-execution commitment. |
| `IEP-PREREQ-004` | Blocked | Separately authorized minimal artifact transfer. |
| `IEP-PREREQ-005` | Blocked | Complete externally produced result receipt. |

## Evidence Boundary

The public TX-17 holdouts remain valid local regression evidence, but they are visible to the implementation actor and therefore are not confidential external holdouts. Protocol readiness is not an evaluation result. It does not establish general model behavior, stakeholder benefit, affected-party acceptance, domain fitness, production readiness, target-runtime behavior, monitoring, incident recovery, maintenance ownership, operational authority, permission expansion, or `G-10` acceptance.

## Verification

- Focused protocol tests: 7/7 passed.
- Focused protocol and boundary suite: 70/70 passed.
- Full product suite: 352/352 passed.
- Protocol validation: passed with four external prerequisites explicitly blocked.
- Product and root aggregate validation: passed.
- Generated derivatives and diff integrity: passed.
- Frozen TX-23/TX-25 evidence and the `pass=94`, `planned=133` trace remained unchanged.
- Memory: `PASS_WITH_WARNINGS`; 1,305 objects, 592 known warnings, zero authority inversions.

## Logical Next Step

Obtain a named independent evaluator proposal and conflict-of-interest attestation for accountable review. Do not transfer artifacts, create a confidential suite in this repository, or execute an external evaluation until a separate transaction and permission envelope authorize those exact actions.
