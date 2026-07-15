# Sys4AI Concepts and Invariants

**Status:** Controlled conceptual guide
**Last reviewed:** 2026-07-15
**Authority:** This guide explains existing requirements and controls. The
registered source, contract, or accepted decision controls when wording
conflicts.

## Why these distinctions matter

Agentic systems can produce persuasive artifacts quickly. A generated plan can
look approved, a passing schema can look correct, a tool can look permitted,
and a summary can look authoritative. Sys4AI treats those as different kinds
of state and evidence.

## Observation is not truth

An observation is evidence produced under stated conditions. Truth claims
require an appropriate source, method, uncertainty treatment, and review.

```text
observed(x under conditions c) does not imply universally_true(x)
```

A host probe, test, benchmark, or document inspection supports only the claim
its conditions and method can establish.

## Retrieval is not authority

Memory search, indexes, generated pages, embeddings, summaries, and chat
context can locate candidate evidence. They do not decide scope, truth,
permission, or completion.

```text
authority(derivative) <= authority(source)
```

unless an explicit source-authority workflow promotes a new controlled source.
Practical rule: **memory finds; sources decide**.

## Capability is not permission

- Capability asks whether a mechanism can perform an action.
- Permission asks whether the action may be performed now.
- Authority asks who may decide purpose, scope, approval, or state change.

```text
capable(actor, action) does not imply authorized(actor, action)
```

Readable files do not authorize edits. A network tool does not authorize data
transfer. A model that can draft a vision cannot approve it. A host profile is
not a permission grant.

## Structure is not semantics

A document can parse, satisfy a schema, contain required headings, and resolve
every path while remaining wrong, harmful, misleading, or unfit for its
domain.

A structural pass supports only structural claims. It does not prove strategic
quality, ethical correctness, stakeholder consensus, behavioral alignment,
domain truth, security, production readiness, or operational fitness.

## Artifact is not execution

A plan, transaction, script, prompt, test definition, or file named
`completion` can exist without the claimed action occurring.

```text
admissible execution claim requires retained observable evidence
```

The evidence must match the applicable contract, environment, version, actor,
and claim boundary.

## Evidence is not approval

Evidence can inform a decision without making it:

- tests support behavior claims under recorded conditions;
- verification supports named requirement claims;
- user or domain research supports accountable judgment;
- evaluation supports performance against a defined rubric;
- an authorized principal accepts, rejects, limits, or defers the result.

For consequential model proposals, the proposer cannot be the sole approver.
Purpose, values, permissions, evaluation standards, production promotion, and
authority hierarchy require accountable non-model authority.

## Verification, validation, evaluation, and acceptance are distinct

| Activity | Question |
|---|---|
| Test execution | What behavior occurred under the stated test conditions? |
| Verification | Was a specified requirement satisfied and traced to evidence? |
| Validation | Is the right system being built for its intended use and stakeholders? |
| Evaluation | How does behavior compare with a defined rubric, dataset, metric, or threshold? |
| Acceptance | Does an accountable authority judge the evidence sufficient for a stated scope? |

These activities may share evidence but cannot silently replace one another.

## Current state is not accepted history

Current state is a projection over decisions, transactions, receipts,
handoffs, snapshots, validations, waivers, expirations, and supersession.

Accepted history is append-and-supersede. A later result adds a record and
explicit relationship rather than rewriting earlier evidence to look as though
the later state always existed.

## Generated reader is not source authority

Generated pages can be deterministic, current, linked, and validated while
remaining readers.

```text
generated(document) does not imply canonical(document)
```

Change the registered source or generator and regenerate. Do not edit the
reader as if convenience promoted it.

## Domain-agnostic framework is not domain acceptance

Sys4AI can provide portable process, trace, permission, evidence, and lifecycle
contracts. It cannot manufacture the truth conditions of physics, medicine,
finance, law, biology, security, or another domain.

Domain fitness requires target-specific requirements, qualified reviewers,
appropriate data and tests, uncertainty treatment, affected-party
consideration, and accountable acceptance.

## Self-hosting is not self-authorization

When Sys4AI helps develop Sys4AI:

- the development system remains distinct from the framework product;
- the runtime actor remains distinct from the subject layer;
- the host remains the source of platform mechanisms and constraints;
- target systems retain separate purpose and authority;
- generated artifacts remain distinct from controlled sources;
- self-reference does not approve purpose, values, permissions, evaluation,
  release, or production state.

## Host observation is freshness-bounded

A host capability profile records an environment, evidence, and freshness
horizon. If required evidence is stale, absent, denied, or conflicting, the
dependent action blocks, degrades, or reroutes. It is not silently assumed.

## Maturity does not follow from architecture

A workflow, autonomous agent, multi-agent design, or production-orchestration
pattern describes coordination. It does not prove operational maturity.

A transition requires, for the exact target and scope:

```text
authority
and entry criteria
and exit evidence
and validation
and rollback readiness
```

The current Sys4AI baseline remains bounded and non-production even though its
repository validation is extensive.

## Minimum claim form

Use this form for consequential results:

> Within **scope**, under **authority**, using **versioned inputs and
> environment**, **actor** performed **action**. **Evidence** supports
> **specific claim**. The result does not establish **explicit limitations**.
> The next permitted state or action is **bounded continuation**.

## Review questions

1. Which system and subject layer changed?
2. Which runtime actor acted?
3. What authorized the action?
4. Which current host capabilities and permissions applied?
5. Which registered sources controlled the work?
6. Which artifact and validation contracts applied?
7. What was actually executed?
8. What evidence was retained?
9. Which exact claim does it support?
10. Which claims remain unsupported?
11. Who accepted the result, if acceptance was required?
12. What state transition occurred?
13. What rollback or supersession path remains?
