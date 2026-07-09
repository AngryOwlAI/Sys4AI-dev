# Strategic Baseline Migration Requirements Discovery Record

**Record ID:** RDR-SFADEV-STRATEGIC-BASELINE-001
**Status:** draft_discovery_evidence
**System name:** Sys4AI strategic semantic-baseline migration
**Prepared by role:** requirements_manager
**Authorized by AgentJob:** TX-01-RDR user-authorized transaction; no active AgentJob runtime
**Subject system ID:** Sys4AI
**Subject layer:** framework_product
**Discovery gate:** system-definition-interview-context-45
**Producer AgentJob:** TX-01-RDR (legacy registry field; not an AgentJob claim)
**Discovery registry row:** rdr_sfadev_strategic_baseline_001
**Downstream artifact status:** Director Decision proposed after RDR validation only
**Source authority status:** derivative_draft
**Created:** 2026-07-09
**Last updated:** 2026-07-09

---

## 1. Authority Notice

This record is controlled draft discovery evidence. It is not a canonical
requirements baseline, does not baseline requirements, and does not approve a
product identity, vision, value set, execution model, host profile, Phase 2
change route, or production capability.

All `REQ-CAND-*`, `NFR-CAND-*`, `VISION-CAND-*`, and `VALUE-CAND-*` content
remains candidate material until the applicable accountable human principal
approves it through the source-authority and Director Decision workflow. This
record routes only to `WS-02`; it must not be used to edit Phase 0, restore the
removed `/continue` or AgentJob runtime, or begin downstream implementation.

## 2. System Layer Classification

| Field | Value | Evidence | Open Issues |
|---|---|---|---|
| Subject layer | `framework_product` | The proposed requirements change the governed Sys4AI product baseline. | `OPEN-SBM-017` asks whether the runtime needs a distinct authority layer. |
| Development-system write surface | `Sys4AI-dev` RDR and controlled registries | `system_layer_registry.csv` classifies the repository root and control records as development-system surfaces. | none |
| Framework product involved? | yes | Phase 0, Phase 1, policies, schemas, registries, and reference implementation are affected after approval. | `OPEN-SBM-001` through `OPEN-SBM-014` |
| Target-system template involved? | later | Strategic-intent templates and package contracts are planned after `G-04`. | `OPEN-SBM-003`, `OPEN-SBM-019` |
| Target-system instance involved? | no current production instance | The repo-steward package is a derivative smoke example, not production authority. | `OPEN-SBM-021` |
| Derivative surfaces involved? | yes, later | Module PRDs and generated docs may be regenerated only after canonical approval. | none |
| Runtime actor axis | candidate separate axis | `subject_layer` identifies the affected authority surface; `runtime_actor` would identify the performing, proposing, approving, evaluating, or accepting actor. | `OPEN-SBM-017` |

The smallest authorized write surface for this transaction is this RDR plus
its source, discovery, and relationship registry rows. No canonical PRD,
historical control record, runtime skill, product implementation, or generated
derivative is authorized for modification.

## 3. Discovery Gate Exit Checklist

| Check | Status | Evidence | Blocking Issues |
|---|---|---|---|
| Subject layer classified | pass | Section 2 distinguishes the development write surface from the framework-product subject. | none |
| Mission need captured or marked missing | pass | Section 4 defines the semantic-consistency need. | none |
| Problem statement captured or marked missing | pass | Section 8 records all twelve baseline conflicts from `WS-00`. | none |
| System-of-interest identified | pass | The system of interest is the composite Sys4AI framework product and proposed Meta-Agent Runtime. | none |
| Stakeholders identified | pass | Section 6 names accountable human principals and affected stakeholder classes. | Named individuals remain a `WS-02` approval obligation. |
| Boundaries captured | pass | Section 7 excludes PRD edits, runtime restoration, and approval claims. | none |
| Candidate requirements remain candidate-labeled | pass | Section 11 uses only candidate IDs. | none |
| Evidence register populated | pass | Section 21 cites canonical, controlled, observed, and supplied sources separately. | none |
| Open questions routed | pass | Sections 18 and 19 assign each decision to an accountable owner and gate. | Human decisions remain open by design. |
| Next route recommended | pass | Route only to `WS-02` identity and execution-model authority decision. | `OPEN-SBM-001` through `OPEN-SBM-022` |

Discovery is structurally ready for the authority-decision packet. It is not
ready for PRD synthesis because the reserved human decisions remain open.

## 4. System Intent Profile

| Field | Value | Source | Evidence status |
|---|---|---|---|
| Mission need | Reconcile Sys4AI's active requirements and governance with the post-`15a9b17` runtime reality without erasing historical evidence or silently restoring removed capabilities. | Strategic migration plan and `WS-00` receipt | stated and observed |
| Problem statement | Structural validation passes while canonical and controlled surfaces still prescribe or claim removed AgentJob and `/continue` behavior. | `CR-SFADEV-STRATEGIC-BASELINE-WS00-001` | observed |
| Desired outcome | A portable, truthful, human-governed Sys4AI baseline covers identity, strategic intent, execution, host integration, lifecycle, safety, trace, and retirement. | Strategic migration plan | candidate |
| Value case | Maintainers and adopters can reason about what Sys4AI currently requires, implements, permits, and proves without authority inversion or validator theater. | Baseline conflicts and candidate values | inferred |
| System-of-interest | Sys4AI framework product, its proposed Meta-Agent Runtime, its host integration profile, and its target-system contracts. | Strategic migration plan | candidate |
| System type | existing system under controlled semantic migration | Git baseline and program state | observed |
| Success criteria | Every recommendation is routed, active claims match observable capability, historical sources remain protected, and approval remains human-accountable. | Plan sections 0.1, 5, and 26 | stated |
| Primary constraints | No implicit restoration; no PRD edit before `G-02`; no candidate promotion; no generated authority; no self-approval by a model. | Plan gates and authority rules | binding for this migration |

## 5. Needs

| ID | Need statement | Source | Evidence status | Related stakeholders |
|---|---|---|---|---|
| NEED-SBM-001 | The product owner needs one truthful product identity that separates framework, runtime, host, targets, and derivatives. | `REC-001` through `REC-003` | stated | `STK-SBM-001`, `STK-SBM-002` |
| NEED-SBM-002 | Maintainers need an explicit disposition for AgentJob and `/continue` after their runtime retraction. | `CONFLICT-EXEC-001`, `CONFLICT-EXEC-002` | observed | `STK-SBM-001`, `STK-SBM-003` |
| NEED-SBM-003 | Stakeholders need approved vision and values that remain subordinate to law, safety, permissions, and human authority. | `REC-004`, `REC-005` | stated | `STK-SBM-001`, `STK-SBM-005`, `STK-SBM-006` |
| NEED-SBM-004 | Target-system sponsors need separate vision and core-values artifacts with approval, waiver, and impact behavior. | `REC-010` through `REC-012` | stated | `STK-SBM-004`, `STK-SBM-005` |
| NEED-SBM-005 | Operators need portable bounded execution that remains stoppable, resumable, reviewable, and host-permission-aware. | `REC-007`, `REC-013` | stated | `STK-SBM-003`, `STK-SBM-007` |
| NEED-SBM-006 | Architects need separate coordination-pattern and operational-maturity decisions. | `REC-009` | stated | `STK-SBM-002`, `STK-SBM-004` |
| NEED-SBM-007 | Verifiers need capability, evidence, approval, authority, validation, and lifecycle states to remain distinct and traceable. | `REC-011`, `REC-017` through `REC-022` | stated | `STK-SBM-008` |
| NEED-SBM-008 | Affected parties need enforceable security, privacy, isolation, self-change, rollback, and evaluator-integrity controls. | `REC-023`, `REC-027` | stated | `STK-SBM-005`, `STK-SBM-006`, `STK-SBM-008` |
| NEED-SBM-009 | Future maintainers need immutable historical evidence and deterministic noncanonical derivatives. | `REC-015`, `REC-024`, `REC-026` | stated | `STK-SBM-001`, `STK-SBM-008` |
| NEED-SBM-010 | Production owners need complete lifecycle and retirement obligations rather than a generation-only workflow. | `REC-008`, `REC-021` | stated | `STK-SBM-004`, `STK-SBM-007` |

## 6. Stakeholders And Roles

| ID | Stakeholder class | Role in system | Primary need | Decision authority | Source | Evidence status |
|---|---|---|---|---|---|---|
| STK-SBM-001 | Repository maintainer acting as product owner | Approves product identity, canonical vision, core values, baseline changes, and release acceptance. | Truthful and maintainable product baseline. | yes; accountable human principal | Plan approval and gate model | role stated; individual confirmation due `G-02` |
| STK-SBM-002 | System architect | Proposes composite model, lifecycle, patterns, interfaces, and alternatives. | Coherent portable architecture. | recommendation only unless separately delegated | Role and plan model | stated |
| STK-SBM-003 | System Director | Governs scope, routing, supersession, stop conditions, and bounded transactions. | Controlled migration without authority expansion. | yes within accepted delegated scope; not strategic self-approval | Role registry and decision policy | observed |
| STK-SBM-004 | Target-system accountable sponsor | Approves each target's purpose, vision, values, risk acceptance, and production promotion. | Fit-for-purpose target systems. | yes; accountable non-model principal | Strategic-intent plan sections | candidate role; principal identified per target |
| STK-SBM-005 | Users and beneficiaries | Supply needs, acceptable outcomes, harms, and success evidence. | Useful and comprehensible systems. | consultation and validation; approval where designated | Candidate vision and discovery model | underrepresented pending elicitation |
| STK-SBM-006 | Affected parties, data subjects, safety, privacy, security, and compliance owners | Define constraints and evaluate harms, data use, and control adequacy. | Protection from unauthorized or unsafe behavior. | veto or approval where policy/law assigns it | Safety workstream | underrepresented pending elicitation |
| STK-SBM-007 | Operators and incident owners | Run, monitor, stop, recover, maintain, and retire systems. | Observable and reversible operation. | operational authority within permission envelope | Lifecycle and operations plan | candidate |
| STK-SBM-008 | Requirements verifier and independent evaluator | Verify trace, semantic truth, scenario performance, and self-change evidence. | Evidence that is independent of the actor under evaluation. | verification verdict; not product-purpose approval | Validation and safety workstreams | stated |
| STK-SBM-009 | Codex host owner and external-system owners | Supply host/tool capabilities, permissions, limits, and interface behavior. | Accurate capability and permission contracts. | authority over their own platforms and interfaces | Host-profile workstream | external evidence required |
| STK-SBM-010 | Future Sys4AI adopters and maintainers | Reuse templates, profiles, packages, and governance contracts. | Portable and comprehensible framework behavior. | no current baseline approval | Product vision | inferred |

No language-model identity is an approval principal. Where this record names a
role rather than an individual, `WS-02` must bind that role to an accountable
human principal or keep the decision open.

## 7. System Boundary

### 7.1 In Scope

| ID | Capability / responsibility | Source | Evidence status |
|---|---|---|---|
| BND-IN-SBM-001 | Capture all strategic-baseline recommendation families as candidates, constraints, risks, drivers, or non-goals. | `WS-01` acceptance | stated |
| BND-IN-SBM-002 | Record the four-object identity, subject-layer/runtime-actor distinction, and runtime-layer question. | `REC-001`, `REC-002` | candidate |
| BND-IN-SBM-003 | Record identity, vision, values, target intent, lifecycle, patterns, host, execution, trace, validation, safety, and retirement candidates. | Plan sections 3 through 5 | candidate |
| BND-IN-SBM-004 | Name reserved human decisions and route them to `WS-02` or their later approval gates. | `WS-01`, `WS-02`, `WS-16` | stated |
| BND-IN-SBM-005 | Register this RDR and its upstream/downstream evidence relationships. | `WS-01` registration rule | stated |

### 7.2 Out Of Scope

| ID | Exclusion | Rationale | Source | Evidence status |
|---|---|---|---|---|
| BND-OUT-SBM-001 | Editing Phase 0, Phase 1, Phase 2, or any derivative PRD. | `G-02` and later gates are not satisfied. | Plan gate model | binding |
| BND-OUT-SBM-002 | Selecting or approving an execution-model route. | The choice is reserved for the `WS-02` human authority decision. | Plan section 2.2 | binding |
| BND-OUT-SBM-003 | Restoring deleted skills, control-loop code, CLI commands, Make targets, or tests. | The no-implicit-restoration rule prohibits it. | Plan section 2.3 | binding |
| BND-OUT-SBM-004 | Creating schemas, templates, validators, host profiles, package changes, or runtime code. | Contracts and authority gates precede implementation. | `G-03` through `G-07` | binding |
| BND-OUT-SBM-005 | Regenerating module PRDs or strategic reader content. | Strategic derivatives wait for canonical approval; a deterministic noncanonical registry-catalog refresh is permitted when required by source registration. | `G-09` and repository derivative validation | binding |
| BND-OUT-SBM-006 | Treating candidate vision or values as consent, ethics approval, or permission. | Validators cannot decide desirability or stakeholder consent. | Plan section 3.8 | binding |

### 7.3 External Systems And Interfaces

| ID | External system / actor | Relationship | Input/output | Owner | Source | Open issues |
|---|---|---|---|---|---|---|
| EXT-SBM-001 | Codex App | Proposed reference host for user interaction, workspace tools, terminal actions, sub-agents, approvals, task state, and cancellation. | Capability/permission profile and execution evidence. | Codex host owner plus project maintainer | Plan `WS-06` | `OPEN-SBM-015`, `OPEN-SBM-016` |
| EXT-SBM-002 | Git and `origin/main` | Shared baseline and immutable history boundary. | Commits, refs, hashes, diffs. | Repository maintainer | `WS-00` receipt | none |
| EXT-SBM-003 | Target-system stakeholders and operating environment | Supply purpose, values, risks, interfaces, success criteria, and production constraints. | Approved intent and operational evidence. | Target accountable sponsor | `WS-05`, `WS-13` | `OPEN-SBM-003` through `OPEN-SBM-013` |
| EXT-SBM-004 | APIs, databases, tools, and business workflows | Future target integration dependencies. | Data, commands, events, credentials, failures. | Named external-system owners | Pattern and host workstreams | deferred per target |
| EXT-SBM-005 | IBM Technology source | External rationale for framework selection, coordination patterns, responsibilities, and prototype/production distinction only. | Attributed rationale. | Requirements manager | Plan attribution boundary | Attribution scope is bounded by `CON-SBM-008`. |

## 8. As-Is State

| ID | Observation | Source | Evidence type | Confidence | Notes |
|---|---|---|---|---|---|
| ASIS-SBM-001 | Commit `15a9b17` removed active `/continue`, AgentJob-authoring, control-loop, related CLI/Make, and runtime test surfaces. | Git and `WS-00` receipt | observed | high | Intentional retraction boundary. |
| ASIS-SBM-002 | Canonical Phase 0 still mandates AgentJob and `/continue`. | Phase 0 and inventory | observed | high | `CONFLICT-EXEC-001`. |
| ASIS-SBM-003 | Accepted Phase 2 still requires removed execution behavior. | Phase 2 and inventory | observed | high | `CONFLICT-EXEC-002`. |
| ASIS-SBM-004 | Trace rows still classify removed continuation capabilities as scaffolded and semantically sufficient. | Requirement trace registry | observed | high | `CONFLICT-TRACE-001`. |
| ASIS-SBM-005 | Program state retains `active_agentjob_id` and legacy actions despite no active AgentJob. | `program_state.yaml` | observed | high | `CONFLICT-STATE-001`. |
| ASIS-SBM-006 | Self-hosting and skill policies prescribe removed surfaces. | Controlled policies | observed | high | `CONFLICT-POLICY-001`. |
| ASIS-SBM-007 | Role and execution bindings use AgentJob-specific authority fields. | Role registries and schemas | observed | high | `CONFLICT-ROLE-001`. |
| ASIS-SBM-008 | Artifact contracts model AgentJob as an active controlled artifact. | Artifact and validation registries | observed | high | `CONFLICT-ART-001`. |
| ASIS-SBM-009 | Walking-skeleton code and target-package validation hard-code AgentJob concepts. | Implementation and tests | observed | high | `CONFLICT-WALK-001`, `CONFLICT-PACK-001`. |
| ASIS-SBM-010 | Earlier plans contain legitimate historical `/continue` and AgentJob evidence. | Implementation plans and completed records | observed | high | Preserve; do not rewrite. |
| ASIS-SBM-011 | Historical Phase 0 contains stronger vision language than canonical Phase 0. | Historical and canonical PRDs | observed | high | Provenance-preserving migration candidate. |
| ASIS-SBM-012 | Aggregate validation passes without capability-existence or strategic-semantic checks. | `WS-00` validation record | observed | high | Structural green is not semantic proof. |
| ASIS-SBM-013 | Source-first memory passes with 333 pending-hash warnings at the baseline capture. | `WS-00` receipt | observed | high | Freshness claims remain limited. |

## 9. To-Be State

| ID | Desired future behavior | Source | Evidence status | Related need |
|---|---|---|---|---|
| TOBE-SBM-001 | An approved composite identity distinguishes framework product, Meta-Agent Runtime, host, templates, instances, and derivatives. | `REC-001` through `REC-003` | candidate | `NEED-SBM-001` |
| TOBE-SBM-002 | Portable bounded-execution contracts replace hard-coded runtime assumptions if route 2 is approved. | `REC-006`, `REC-007` | candidate | `NEED-SBM-002`, `NEED-SBM-005` |
| TOBE-SBM-003 | Approved Sys4AI and target strategic intent traces into requirements, permissions, evaluations, operations, and change impact. | `REC-004`, `REC-005`, `REC-010`, `REC-026` | candidate | `NEED-SBM-003`, `NEED-SBM-004` |
| TOBE-SBM-004 | Lifecycle, pattern, maturity, host, and promotion decisions have explicit evidence and failure behavior. | `REC-008`, `REC-009`, `REC-013`, `REC-021` | candidate | `NEED-SBM-006`, `NEED-SBM-010` |
| TOBE-SBM-005 | Capability, evidence, approval, authority, validation, and lifecycle states are separately represented and validated. | `REC-011`, `REC-019`, `REC-020` | candidate | `NEED-SBM-007` |
| TOBE-SBM-006 | Self-change and production operation require least privilege, independent evaluation, rollback, isolation, and human approval. | `REC-023`, `REC-027` | candidate | `NEED-SBM-008` |
| TOBE-SBM-007 | Historical sources remain immutable and derivatives regenerate deterministically from approved canonical sources. | `REC-015`, `REC-024`, `REC-026` | candidate | `NEED-SBM-009` |

## 10. Operational Scenarios And ConOps Seeds

| ID | Scenario | Actors | Trigger | Normal flow | Exception/degraded flow | Related needs | Evidence |
|---|---|---|---|---|---|---|---|
| SCN-SBM-001 | Decide identity and execution route | Product owner, system director, architect, verifier | Validated RDR routes to `WS-02`. | Review four-object model and four routes; record evidence, selection, compatibility, and rollback. | If authority or evidence is insufficient, keep decision open and block PRD edits. | `NEED-SBM-001`, `NEED-SBM-002` | `WS-02` |
| SCN-SBM-002 | Define strategic intent | Product owner, users, affected parties, requirements manager | Identity route accepted. | Elicit beneficiaries, horizon, exclusions, success signals, values, anti-values, and evidence; obtain human approval. | If representation or consent is inadequate, retain candidates and continue elicitation. | `NEED-SBM-003` | `WS-03`, `WS-16` |
| SCN-SBM-003 | Initialize a target system | Target sponsor, elicitor, safety/privacy owners | New or materially changed target request. | Create separate target vision and values; approve or document a time-bounded waiver before baselining requirements. | Missing approval blocks or constrains the downstream baseline. | `NEED-SBM-004` | `WS-05` |
| SCN-SBM-004 | Execute a bounded transaction | Human principal, Codex host, delegated role agent, verifier | Approved work packet and permission envelope exist. | Verify host capabilities, execute within scope, persist state/evidence, validate, and hand off. | Missing permission/capability produces blocked, degraded, cancelled, or rerouted state. | `NEED-SBM-005` | `WS-06`, `WS-08` |
| SCN-SBM-005 | Select architecture and maturity | Target sponsor, architect, operator, security owner | Target discovery reaches architecture selection. | Record coordination pattern, maturity, alternatives, integrations, reliability, monitoring, and promotion criteria. | A prototype cannot become operational without the production evidence gate. | `NEED-SBM-006`, `NEED-SBM-010` | `WS-04`, `WS-12` |
| SCN-SBM-006 | Evaluate a self-change | Meta-agent runtime, independent evaluator, product owner | Runtime proposes a change to its own governed behavior. | Separate proposer, evaluator, and approver; use holdouts; assess permission, regression, rollback, and value impact. | Suspected evaluator gaming, isolation failure, or missing rollback blocks promotion. | `NEED-SBM-008` | `WS-13`, `WS-16` |
| SCN-SBM-007 | Retire a target system | Sponsor, operator, data owner, security owner | End-of-life decision or unacceptable residual risk. | Withdraw credentials and authority, archive required evidence, dispose of data, stop dependencies, notify stakeholders. | Legal hold or retained-risk obligation changes disposal while remaining documented. | `NEED-SBM-010` | Lifecycle candidate |

## 11. Candidate Requirements

All candidate statements in this section are noncanonical.

### 11.1 Candidate Functional Requirements

| ID | Candidate requirement | Source need/scenario | Rationale | Priority | Verification seed | Status |
|---|---|---|---|---|---|---|
| REQ-CAND-SBM-ID-001 | Sys4AI should define a composite identity comprising a governed framework product and an executable Meta-Agent Runtime. | `NEED-SBM-001` | Removes the ambiguous unrelated-root-agent model. | Must | `VVE-SBM-001` | candidate |
| REQ-CAND-SBM-ID-002 | Governed artifacts should distinguish framework product, Meta-Agent Runtime, host harness, target template, target instance, and derivative surface, while separately recording runtime actor. | `NEED-SBM-001` | Prevents layer and actor authority conflation. | Must | `VVE-SBM-002` | candidate |
| REQ-CAND-SBM-ID-003 | Sys4AI should distinguish planning or orchestration from execution and should not claim execution without observable evidence. | `NEED-SBM-007` | Prevents false capability claims. | Must | `VVE-SBM-003` | candidate |
| REQ-CAND-SBM-EXEC-001 | An accountable human authority should select and record one post-retraction execution-model route before canonical PRD edits. | `NEED-SBM-002` / `SCN-SBM-001` | Resolves the core semantic conflict. | Must | `VVE-SBM-004` | candidate |
| REQ-CAND-SBM-EXEC-002 | If portable replacement is approved, Sys4AI should define bounded authorization, permission envelope, resumable state, current-state resolution, validation, closeout, handoff, stop, cancellation, and escalation contracts. | `NEED-SBM-005` / `SCN-SBM-004` | Preserves valuable controls without hard-coded host mechanics. | Must | `VVE-SBM-005` | candidate |
| REQ-CAND-SBM-EXEC-003 | Execution state should distinguish proposed, authorized, active, blocked, cancelled, completed, accepted, and superseded states. | `NEED-SBM-005`, `NEED-SBM-007` | Avoids collapsing authority, work, and acceptance. | Must | `VVE-SBM-006` | candidate |
| REQ-CAND-SBM-HOST-001 | Sys4AI should define Codex App as the initial reference-host profile without embedding Codex mechanics in portable semantics. | `NEED-SBM-005` | Provides one testable integration while preserving portability. | Should | `VVE-SBM-007` | candidate |
| REQ-CAND-SBM-HOST-002 | Before execution, the host profile should verify required capabilities and permissions and should report missing capabilities as degraded, blocked, denied, or rerouted. | `SCN-SBM-004` | Prevents assumed capability and permission expansion. | Must | `VVE-SBM-008` | candidate |
| REQ-CAND-SBM-STRAT-001 | Canonical Phase 0 should contain one human-approved Sys4AI vision with owner, beneficiaries, horizon, scope, exclusions, success signals, evidence, version, and revision triggers. | `NEED-SBM-003` / `SCN-SBM-002` | Makes future-state intent explicit and governable. | Must | `VVE-SBM-009` | candidate |
| REQ-CAND-SBM-STRAT-002 | Canonical Phase 0 should contain stable-ID core values with rationale, expected behavior, anti-patterns, decision tests, conflict rules, and evidence obligations. | `NEED-SBM-003` | Converts values from slogans into reviewable commitments. | Must | `VVE-SBM-010` | candidate |
| REQ-CAND-SBM-STRAT-003 | Material decisions and changes should trace affected vision and value IDs and should route value conflicts through an accountable decision. | `NEED-SBM-003`, `NEED-SBM-007` | Supports impact analysis and transparent tradeoffs. | Must | `VVE-SBM-011` | candidate |
| REQ-CAND-SBM-TARGET-001 | Every new or substantially changed target system should have separate target vision and core-values artifacts. | `NEED-SBM-004` / `SCN-SBM-003` | Keeps target intent distinct from framework governance. | Must | `VVE-SBM-012` | candidate |
| REQ-CAND-SBM-TARGET-002 | A target requirements baseline should require approved intent artifacts or an authorized waiver with risk, expiry, and downstream handling. | `NEED-SBM-004` | Makes incomplete intent visible rather than implicit. | Must | `VVE-SBM-013` | candidate |
| REQ-CAND-SBM-TARGET-003 | Approved vision or value changes should trigger impact analysis across requirements, architecture, permissions, tests, evaluations, operations, maintenance, and retirement. | `NEED-SBM-004`, `NEED-SBM-007` | Prevents strategic change from bypassing downstream controls. | Must | `VVE-SBM-014` | candidate |
| REQ-CAND-SBM-LIFE-001 | Sys4AI should support Design, Develop, Implement, Test, Run, Maintain, Improve, and Retire lifecycle stages. | `NEED-SBM-010` | Completes the lifecycle beyond generation. | Must | `VVE-SBM-015` | candidate |
| REQ-CAND-SBM-LIFE-002 | Each lifecycle stage should define entry criteria, inputs, roles, permissions, activities, outputs, evidence, exit criteria, failures, transitions, rollback, and review cadence. | `NEED-SBM-010` | Makes stage transitions testable and governable. | Must | `VVE-SBM-016` | candidate |
| REQ-CAND-SBM-LIFE-003 | Sys4AI should distinguish test execution, requirements verification, stakeholder/system validation, and behavioral/performance evaluation. | `NEED-SBM-007`, `NEED-SBM-010` | Prevents different evidence claims from being conflated. | Must | `VVE-SBM-017` | candidate |
| REQ-CAND-SBM-PATTERN-001 | Discovery should classify coordination pattern separately from operational maturity. | `NEED-SBM-006` | Architecture topology and readiness answer different questions. | Must | `VVE-SBM-018` | candidate |
| REQ-CAND-SBM-PATTERN-002 | Architecture selection should record alternatives, autonomy, roles, integrations, communication, state, monitoring, failure, security, recovery, and promotion criteria. | `NEED-SBM-006` / `SCN-SBM-005` | Supports evidence-based pattern selection. | Must | `VVE-SBM-019` | candidate |
| REQ-CAND-SBM-TRACE-001 | Trace data should represent requirement, capability, evidence, approval, authority, validation, and lifecycle state independently. | `NEED-SBM-007` | Makes retractions and partial evidence truthful. | Must | `VVE-SBM-020` | candidate |
| REQ-CAND-SBM-TRACE-002 | Sys4AI should trace stakeholder evidence through vision, values, goals, requirements, architecture, permissions, tests, evaluations, operations, and improvements. | `NEED-SBM-007`, `NEED-SBM-009` | Enables no-orphan and impact analysis. | Must | `VVE-SBM-021` | candidate |
| REQ-CAND-SBM-VALID-001 | Focused validation should detect strategic-intent gaps, PRD semantic conflicts, host-profile failures, lifecycle/pattern errors, capability-migration drift, and generalized trace inconsistency. | `NEED-SBM-007` | Structural validation alone is insufficient. | Must | `VVE-SBM-022` | candidate |
| REQ-CAND-SBM-VALID-002 | Target-package validation should reject missing, unapproved, stale, duplicate, model-self-approved, or untraceable strategic and execution evidence. | `NEED-SBM-007`, `NEED-SBM-010` | Prevents weak packages from appearing production-ready. | Must | `VVE-SBM-023` | candidate |
| REQ-CAND-SBM-PH2-001 | Accepted Phase 2 evidence should remain unchanged while an approved addendum or successor carries new strategic and execution obligations. | `NEED-SBM-009` | Preserves accepted history. | Must | `VVE-SBM-024` | candidate |
| REQ-CAND-SBM-SAFETY-001 | Purpose, permissions, evaluation standards, production promotion, and authority hierarchy should remain reserved for accountable human approval. | `NEED-SBM-008` | Prevents model self-authorization. | Must | `VVE-SBM-025` | candidate |
| REQ-CAND-SBM-SAFETY-002 | Self-change should separate proposer, evaluator, and approver and should require independent holdout, regression, security, value-impact, and rollback evidence. | `NEED-SBM-008` / `SCN-SBM-006` | Reduces self-evaluation and evaluator-gaming risk. | Must | `VVE-SBM-026` | candidate |
| REQ-CAND-SBM-SAFETY-003 | Runtime operation should enforce least privilege, cross-layer and data isolation, hostile-input handling, bounded reflection, monitoring, incident response, and emergency stop. | `NEED-SBM-008` | Defines practical control boundaries. | Must | `VVE-SBM-027` | candidate |
| REQ-CAND-SBM-DOC-001 | Derivative PRDs and generated documentation should regenerate only after canonical approval and should remain explicitly noncanonical. | `NEED-SBM-009` | Prevents derivative authority inversion. | Must | `VVE-SBM-028` | candidate |
| REQ-CAND-SBM-ATTR-001 | External-source claims should preserve the IBM-versus-Sys4AI attribution boundary and use APA 7 attribution. | `NEED-SBM-007` | Prevents unsupported provenance claims. | Must | `VVE-SBM-029` | candidate |
| REQ-CAND-SBM-RETIRE-001 | Retirement should cover archival, data disposition, credential and authority withdrawal, dependency shutdown, retained evidence, and stakeholder notification. | `NEED-SBM-010` / `SCN-SBM-007` | Completes operational stewardship. | Must | `VVE-SBM-030` | candidate |

### 11.2 Candidate Quality Attributes

| ID | Quality attribute | Candidate statement | Source | Threshold / measure | Verification seed | Status |
|---|---|---|---|---|---|---|
| NFR-CAND-SBM-001 | Portability | Portable framework contracts should contain no mandatory host command, UI, or proprietary task-state vocabulary. | `REC-007`, `REC-013` | Host-specific terms occur only in declared profiles. | `VVE-SBM-031` | candidate |
| NFR-CAND-SBM-002 | Authority integrity | No model or generated derivative should approve purpose, values, permissions, evaluation standards, promotion, or supersession. | `REC-005`, `REC-011` | Negative fixtures fail every prohibited self-approval state. | `VVE-SBM-032` | candidate |
| NFR-CAND-SBM-003 | Historical integrity | Protected Phase 0, Phase 2, decisions, plans, receipts, handoffs, and AgentJob records should retain baseline Git evidence. | `REC-024` | Protected hashes or immutable Git objects remain reproducible. | `VVE-SBM-033` | candidate |
| NFR-CAND-SBM-004 | Security and privacy | Permissions, secrets, personal data, tool access, and cross-target memory should be deny-by-default outside an approved envelope. | `REC-023` | Threat and negative-isolation scenarios pass. | `VVE-SBM-034` | candidate |
| NFR-CAND-SBM-005 | Resilience | Required capabilities should have defined blocked, degraded, cancellation, retry, recovery, and rollback behavior. | `REC-013`, `REC-023` | Every required interface declares at least one failure path. | `VVE-SBM-035` | candidate |
| NFR-CAND-SBM-006 | Verifiability | Every active capability claim should cite observable implementation and current evidence or be classified as unimplemented, removed, optional, or historical. | `REC-018` through `REC-022` | No active claim lacks capability/evidence state. | `VVE-SBM-036` | candidate |
| NFR-CAND-SBM-007 | Maintainability | Existing registries and contracts should be extended before a new authority surface is introduced. | `REC-025` | New registry requires a documented representation gap and decision. | `VVE-SBM-037` | candidate |
| NFR-CAND-SBM-008 | Evidence freshness | Populated hashes and review timestamps should be validated; pending hashes should remain warnings with bounded freshness claims. | `WS-00` warning | No stale or pending evidence is represented as fresh. | `VVE-SBM-038` | candidate |

## 12. Architecture Drivers

| ID | Driver | Type | Source | Why it matters | Related candidates | Open issues |
|---|---|---|---|---|---|---|
| DRV-SBM-001 | Post-retraction semantic truth | constraint | `15a9b17` and `WS-00` | Active requirements and claims must reflect observable capability. | `REQ-CAND-SBM-EXEC-001`, `NFR-CAND-SBM-006` | `OPEN-SBM-014` |
| DRV-SBM-002 | Human accountable authority | safety/governance | Plan gates and candidate values | Models cannot approve purpose, permissions, or evaluation standards. | `REQ-CAND-SBM-SAFETY-001`, `NFR-CAND-SBM-002` | `OPEN-SBM-001` through `OPEN-SBM-003` |
| DRV-SBM-003 | Host-neutral portability | architecture/interface | Recommended execution route | Portable contracts must survive host changes. | `REQ-CAND-SBM-EXEC-002`, `NFR-CAND-SBM-001` | `OPEN-SBM-014`, `OPEN-SBM-015` |
| DRV-SBM-004 | Strategic-intent trace | traceability | `REC-004`, `REC-005`, `REC-026` | Purpose and values must influence downstream decisions without granting permission. | `REQ-CAND-SBM-STRAT-001` through `003`, `REQ-CAND-SBM-TRACE-002` | `OPEN-SBM-004` through `OPEN-SBM-013` |
| DRV-SBM-005 | Full-lifecycle stewardship | operations | `REC-008`, `REC-023` | Production systems require operation, maintenance, improvement, and retirement. | `REQ-CAND-SBM-LIFE-001` through `003`, `REQ-CAND-SBM-RETIRE-001` | `OPEN-SBM-021`, `OPEN-SBM-022` |
| DRV-SBM-006 | Pattern/maturity separation | architecture | `REC-009` | Architecture topology must not be confused with readiness. | `REQ-CAND-SBM-PATTERN-001`, `REQ-CAND-SBM-PATTERN-002` | `OPEN-SBM-007` |
| DRV-SBM-007 | Immutable historical boundary | source authority | `WS-00` manifest | Migration must not rewrite accepted evidence. | `REQ-CAND-SBM-PH2-001`, `NFR-CAND-SBM-003` | `OPEN-SBM-018` |
| DRV-SBM-008 | Independent self-change evaluation | safety/evaluation | `REC-023`, `REC-027` | A changing actor must not control its own evaluator or acceptance criteria. | `REQ-CAND-SBM-SAFETY-002`, `REQ-CAND-SBM-SAFETY-003` | `OPEN-SBM-020` |
| DRV-SBM-009 | Existing-registry preference | maintainability | `REC-025` | Authority surfaces should remain comprehensible and minimal. | `NFR-CAND-SBM-007` | none |
| DRV-SBM-010 | Evidence freshness and semantic limits | quality | `WS-00` warnings | Structural green and registration do not prove current truth. | `REQ-CAND-SBM-VALID-001`, `NFR-CAND-SBM-008` | `OPEN-SBM-013` |

## 13. Interface Candidates

| ID | Interface candidate | Producer | Consumer | Data / command / event | Frequency | Owner | Related scenario | Open issues |
|---|---|---|---|---|---|---|---|---|
| IF-SBM-001 | Strategic-baseline Director Decision | RDR and product owner | Phase 0/Phase 1 migration work | Identity route, execution disposition, authority, compatibility, rollback. | once, review-triggered | product owner/system director | `SCN-SBM-001` | `OPEN-SBM-001`, `OPEN-SBM-014`, `OPEN-SBM-017` |
| IF-SBM-002 | Target strategic-intent package | Elicitor and target sponsor | Requirements manager, architect, verifier | Purpose, vision, values, approvals, waiver, impact links. | per new/materially changed target | target sponsor | `SCN-SBM-003` | `OPEN-SBM-003` |
| IF-SBM-003 | Host capability profile | Codex host owner/interface owner | Execution transaction verifier | Capability state, permission, evidence method, limitations, degraded behavior. | host/version change and pre-execution | interface owner | `SCN-SBM-004` | `OPEN-SBM-015`, `OPEN-SBM-016` |
| IF-SBM-004 | Portable execution transaction | Human principal/system director | Host and delegated role actor | Objective, envelope, state, allowed actions, stop/cancel/escalate, validation, handoff. | per bounded transaction | system director | `SCN-SBM-004` | `OPEN-SBM-014` |
| IF-SBM-005 | Pattern and maturity decision | Architect and target sponsor | Implementer, operator, evaluator | Pattern, maturity, alternatives, interfaces, risks, monitoring, promotion criteria. | initial selection and material change | architect/product owner | `SCN-SBM-005` | `OPEN-SBM-007`, `OPEN-SBM-021` |
| IF-SBM-006 | Capability/evidence trace | Source and implementation owners | Semantic validators and reviewers | Requirement, capability, evidence, authority, approval, validation, lifecycle states. | every controlled change | trace owner | `SCN-SBM-001` through `SCN-SBM-007` | none |
| IF-SBM-007 | Self-change evaluation packet | Meta-Agent Runtime proposer | Independent evaluator and human approver | Proposed change, threats, holdouts, regressions, value impact, permissions, rollback. | per self-change | independent evaluator | `SCN-SBM-006` | `OPEN-SBM-020` |
| IF-SBM-008 | Retirement record | Operator and target sponsor | Data, security, compliance, stakeholder, and archive owners | Stop decision, authority withdrawal, data disposition, retained evidence, notifications. | per retirement | operations owner | `SCN-SBM-007` | `OPEN-SBM-022` |

## 14. Strategic Intent Candidates

### 14.1 Vision Candidate

`VISION-CAND-SBM-001`:

> Sys4AI envisions a future in which people, working through Codex and
> compatible AI harnesses, can reliably create and steward fit-for-purpose AI
> agents across their complete lifecycle, while accountable stakeholders
> retain authority and every consequential claim, decision, and change remains
> evidence-grounded, traceable, safe, and reviewable.

This is AI-drafted candidate wording. It is not stakeholder-approved and does
not imply model desire, consciousness, moral agency, or purpose-setting
authority.

### 14.2 Value Candidates

| Candidate ID | Candidate value | Observable behavior | Anti-value or prohibited behavior |
|---|---|---|---|
| VALUE-CAND-SBM-001 | Human-directed purpose and accountable authority | Names the human authorization for purpose, scope, and consequential action. | Invented goals, self-approved values, or silence treated as consent. |
| VALUE-CAND-SBM-002 | Purpose-fit architecture | Selects pattern and tools from the target problem, risk, coordination, and maturity evidence. | Fashion-driven or universal-best framework claims. |
| VALUE-CAND-SBM-003 | Evidence and intellectual honesty | Traces claims and discloses inference, assumption, uncertainty, and validator limits. | Retrieval or structural validation represented as established fact. |
| VALUE-CAND-SBM-004 | Bounded autonomy and accountability | Keeps actions permissioned, scoped, observable, stoppable, and reversible where practical. | Goals, values, or efficiency used to expand permission. |
| VALUE-CAND-SBM-005 | Safety, security, privacy, and responsible control | Evaluates threats, affected parties, data, permissions, and failure modes before execution. | Safety deferred to production or innovation used to bypass controls. |
| VALUE-CAND-SBM-006 | Clear roles and accountable collaboration | Defines responsibility, inputs, outputs, tools, boundaries, handoffs, and escalation. | Silent assumption of another role's authority. |
| VALUE-CAND-SBM-007 | Traceable, testable, and reproducible engineering | Preserves intent-to-evidence trace and independent review. | Orphan artifacts, hidden changes, validator theater, or unverifiable claims. |
| VALUE-CAND-SBM-008 | Full-lifecycle and reversible stewardship | Plans monitoring, maintenance, regression control, rollback, improvement, and retirement. | Treating agent or package generation as lifecycle completion. |

Candidate precedence is: applicable law and mandatory platform policy; safety,
security, privacy, and compliance constraints; source authority, host
permissions, and required human approvals; approved Sys4AI governance;
approved target values; ordinary product and implementation preferences.
Values never grant permission.

## 15. Approval Principals And Reserved Decisions

| Decision | Required principal | Model approval allowed? | Due gate | Current state |
|---|---|---:|---|---|
| Sys4AI product identity and execution route | Repository maintainer acting as product owner, recorded in a Director Decision | no | `G-02` | open |
| Sys4AI vision and values | Product owner with represented stakeholder evidence | no | `G-08` | candidate only |
| Target purpose, vision, and values | Named target-system accountable sponsor | no | target strategic-intent gate | open per target |
| Host permissions and tool access | Human project principal plus host/platform authority | no | before execution | open per transaction |
| Evaluation standards and holdouts | Accountable evaluation owner independent of the evaluated actor | no | before self-change or production evaluation | open |
| Prototype-to-production promotion | Target sponsor, operator, security/privacy owners, and other required authorities | no | production promotion gate | open |
| Baseline supersession | Product owner and source-authority workflow | no | applicable baseline gate | open |
| Emergency stop and incident disposition | Named operator/incident owner within platform policy | no | before operational use | open |

## 16. Inherited Governance Constraints

| ID | Constraint | Source | Effect |
|---|---|---|---|
| CON-SBM-001 | Memory and generated derivatives are navigation, not authority. | Source-first policy | Inspect registered canonical or controlled sources before claims. |
| CON-SBM-002 | Activated control history must not be rewritten. | Baseline-change skill | Supersede or reclassify with explicit evidence. |
| CON-SBM-003 | No runtime actor gains authority merely from capability. | Strategic migration plan | Separate actor from subject layer and approval principal. |
| CON-SBM-004 | No deleted runtime surface may be restored implicitly. | Plan section 2.3 | Route restoration through a separate explicit decision. |
| CON-SBM-005 | Candidate content must not enter canonical PRDs before `G-02`. | Plan gate model | Keep all discovery wording candidate-labeled. |
| CON-SBM-006 | Approval, authority, validation, capability, evidence, and lifecycle states remain distinct. | `REC-011`, `REC-020` | Schemas and reviews must not infer one from another. |
| CON-SBM-007 | Existing registries are preferred over new registries. | `REC-025` | Prove a representation gap before adding authority surfaces. |
| CON-SBM-008 | IBM attribution is limited to framework selection, common patterns, explicit roles, integrations/monitoring/task/communication support, and prototype-versus-production distinction. | Plan section 1.6 | Sys4AI-specific vision, values, self-change, permissions, lifecycle, and strategic artifacts remain Sys4AI proposals. |
| CON-SBM-009 | Host and project permissions outrank values and target goals. | Candidate precedence | Missing permission blocks or reroutes execution. |

## 17. Target-Specific Commitments And Waiver Candidates

The framework should require each target to supply its own purpose, vision,
values, beneficiaries, exclusions, risks, success evidence, approvals, and
revision triggers. This RDR does not invent those target-specific commitments.

`WAIVER-CAND-SBM-001` may allow a downstream target requirements baseline to
proceed without approved target vision or values only when an accountable
human authority records the missing artifact, rationale, affected parties,
risk, compensating controls, expiry, review trigger, and downstream handling.
It must never be implicit, permanent by default, or model-approved.

## 18. Execution-Model Disposition And Codex Host Capability Candidates

### 18.1 Execution Routes Requiring Decision

| Route | Candidate disposition | Primary benefit | Primary risk | Discovery recommendation |
|---|---|---|---|---|
| 1 | Retain AgentJob and `/continue` requirements as temporarily unimplemented. | Lowest prose migration. | Canonical requirements remain coupled to removed behavior. | not preferred |
| 2 | Replace hard-coded semantics with portable bounded-execution contracts. | Portable and truthful while preserving control obligations. | Broad coordinated migration. | preferred candidate |
| 3 | Retire the concepts completely. | Smallest capability surface. | Loses resumability, scope, closeout, and handoff obligations. | not preferred |
| 4 | Restore removed implementation. | Recreates earlier behavior quickly. | Reverses an intentional retraction without new justification. | prohibited absent separate authority |

No route is approved by this RDR.

### 18.2 Codex Capability Candidates

| Capability | Candidate state | Required evidence | Missing-capability behavior | Owner |
|---|---|---|---|---|
| User interaction and explicit instruction | required | Observable task input and scope | block | project principal |
| Workspace read/write tools | required per packet | Host capability and permission check | block or narrow scope | host/project authority |
| Terminal execution | optional unless validator requires it | Command capability and approved working directory | reroute or block validation | host/project authority |
| Sub-agents | optional | Availability and bounded delegation contract | execute serially or reduce scope | system director |
| Approval prompts | required for actions needing new authority | Observable approval mechanism or direct human decision | block | human principal |
| Persistent task or transaction state | required for resumability | State contract and recovery test | degrade to explicit handoff | system director |
| Cancellation and emergency stop | required for execution | Observable stop behavior and state transition | block execution | operator/host owner |
| Evidence capture | required | Command, diff, validator, completion, and handoff evidence | block completion claim | verifier |

## 19. Lifecycle And Pattern Candidates

The lifecycle candidate is:

`Design -> Develop -> Implement -> Test -> Run -> Maintain -> Improve -> Retire`

Testing, requirements verification, stakeholder validation, and behavioral or
performance evaluation also act as cross-cutting gates.

Candidate coordination patterns are `linear_workflow`,
`goal_directed_autonomous_agent`, `role_based_multi_agent`,
`production_orchestration`, and `hybrid`. Candidate operational-maturity
states are `concept`, `prototype`, `validated_prototype`,
`production_candidate`, `production_approved`, `operational`, `maintenance`,
and `retired`. Rapid prototyping is a maturity condition, not an architecture.

## 20. Verification And Validation Seeds

| ID | Candidate evidence or check | Traces to | Method | Owner/gate | Acceptance idea | Status |
|---|---|---|---|---|---|---|
| VVE-SBM-001 | Inspect approved identity decision and canonical definition. | `REQ-CAND-SBM-ID-001` | review | product owner / `G-02` | Four-object model and boundaries are explicit. | seed |
| VVE-SBM-002 | Validate subject-layer and runtime-actor fields and negative authority cases. | `REQ-CAND-SBM-ID-002` | test/review | system-layer classifier | Actor capability does not grant layer authority. | seed |
| VVE-SBM-003 | Compare capability claims with executable paths and evidence. | `REQ-CAND-SBM-ID-003` | inspection/test | requirements verifier | No planning-only surface claims execution. | seed |
| VVE-SBM-004 | Inspect accepted route decision, alternatives, rollback, and supersession. | `REQ-CAND-SBM-EXEC-001` | review | product owner / `G-02` | One route is explicitly selected or work remains blocked. | seed |
| VVE-SBM-005 | Validate portable execution contract positive and negative fixtures. | `REQ-CAND-SBM-EXEC-002` | test | contract verifier | Every required section and stop condition is enforced. | seed |
| VVE-SBM-006 | Exercise allowed and forbidden execution-state transitions. | `REQ-CAND-SBM-EXEC-003` | test | state verifier | Invalid authority or acceptance inference fails. | seed |
| VVE-SBM-007 | Verify Codex profile against observable host behavior. | `REQ-CAND-SBM-HOST-001` | demonstration | interface owner / `G-07` | Each claim has current evidence or is unknown. | seed |
| VVE-SBM-008 | Deny a required capability and inspect blocked/degraded routing. | `REQ-CAND-SBM-HOST-002` | negative test | host verifier | No assumed success or permission expansion. | seed |
| VVE-SBM-009 | Review vision metadata and human approval evidence. | `REQ-CAND-SBM-STRAT-001` | review | product owner / `G-08` | Vision is approved, sourced, scoped, and revision-controlled. | seed |
| VVE-SBM-010 | Run positive, negative, and conflict probes for each approved value. | `REQ-CAND-SBM-STRAT-002` | evaluation | independent evaluator | Each value has behavior and anti-behavior evidence. | seed |
| VVE-SBM-011 | Change a value candidate and inspect affected graph nodes. | `REQ-CAND-SBM-STRAT-003` | demonstration | trace owner | Impact set covers all dependent artifact classes. | seed |
| VVE-SBM-012 | Validate target vision and values templates and examples. | `REQ-CAND-SBM-TARGET-001` | test/review | artifact contract owner | Separate approved or candidate artifacts exist. | seed |
| VVE-SBM-013 | Test missing, expired, unauthorized, and model-approved waivers. | `REQ-CAND-SBM-TARGET-002` | negative test | source authority auditor | Invalid waiver blocks baseline. | seed |
| VVE-SBM-014 | Supersede target intent and inspect downstream review set. | `REQ-CAND-SBM-TARGET-003` | demonstration | baseline change manager | Required impact analysis is produced. | seed |
| VVE-SBM-015 | Validate complete lifecycle vocabulary and allowed transitions. | `REQ-CAND-SBM-LIFE-001` | test | lifecycle owner | All eight stages are represented. | seed |
| VVE-SBM-016 | Inspect stage contracts for required fields and rollback. | `REQ-CAND-SBM-LIFE-002` | test/review | operations owner | No stage lacks entry, exit, evidence, or failure behavior. | seed |
| VVE-SBM-017 | Review evidence labels for test, verification, validation, and evaluation. | `REQ-CAND-SBM-LIFE-003` | semantic review | requirements verifier | Claims use the correct evidence class. | seed |
| VVE-SBM-018 | Validate independent pattern and maturity fields. | `REQ-CAND-SBM-PATTERN-001` | test | architect | Prototype is never accepted as a pattern. | seed |
| VVE-SBM-019 | Inspect a pattern decision and rejected alternatives. | `REQ-CAND-SBM-PATTERN-002` | review | architect/product owner | Required decision evidence is complete. | seed |
| VVE-SBM-020 | Migrate trace rows and test invalid state combinations. | `REQ-CAND-SBM-TRACE-001` | test/review | trace owner | ID/count parity and semantic states pass. | seed |
| VVE-SBM-021 | Run no-orphan and impact queries over the evidence graph. | `REQ-CAND-SBM-TRACE-002` | test | trace owner | Required links exist without implying ethical approval. | seed |
| VVE-SBM-022 | Run focused validators against positive and negative fixtures. | `REQ-CAND-SBM-VALID-001` | test | validator owner | Each validator catches its named failure class. | seed |
| VVE-SBM-023 | Validate target packages missing each required artifact or approval. | `REQ-CAND-SBM-VALID-002` | negative test | package verifier | Every invalid package fails clearly. | seed |
| VVE-SBM-024 | Compare protected Phase 2 objects before and after addendum/successor. | `REQ-CAND-SBM-PH2-001` | hash/diff review | source authority auditor | Accepted Phase 2 evidence is unchanged. | seed |
| VVE-SBM-025 | Exercise prohibited model self-approval cases. | `REQ-CAND-SBM-SAFETY-001` | negative test | independent evaluator | Every reserved decision rejects model approval. | seed |
| VVE-SBM-026 | Evaluate a self-change with hidden holdouts and rollback. | `REQ-CAND-SBM-SAFETY-002` | evaluation | independent evaluator | Proposal cannot alter its evaluator or acceptance criteria. | seed |
| VVE-SBM-027 | Run permission, isolation, hostile-input, recursion, and emergency-stop probes. | `REQ-CAND-SBM-SAFETY-003` | test/evaluation | security and operations owners | Boundaries hold under adverse cases. | seed |
| VVE-SBM-028 | Regenerate modules/docs twice and compare outputs and authority labels. | `REQ-CAND-SBM-DOC-001` | deterministic test | derivative owner / `G-09` | Output is stable and noncanonical. | seed |
| VVE-SBM-029 | Review every external rationale for source scope and APA 7 attribution. | `REQ-CAND-SBM-ATTR-001` | source review | requirements manager | No Sys4AI-specific proposal is attributed to IBM. | seed |
| VVE-SBM-030 | Demonstrate retirement with archival, withdrawal, disposal, shutdown, and notification evidence. | `REQ-CAND-SBM-RETIRE-001` | demonstration | operator/product owner | Obligations are complete or explicitly inapplicable. | seed |
| VVE-SBM-031 | Scan portable contracts for undeclared host-specific mechanics. | `NFR-CAND-SBM-001` | static/semantic test | interface owner | Host terms occur only in profiles. | seed |
| VVE-SBM-032 | Run self-approval negative matrix. | `NFR-CAND-SBM-002` | negative test | source authority auditor | All prohibited combinations fail. | seed |
| VVE-SBM-033 | Recompute protected Git objects and selected SHA-256 hashes. | `NFR-CAND-SBM-003` | hash test | baseline change manager | Historical manifest matches. | seed |
| VVE-SBM-034 | Run least-privilege, secret, data, and cross-target isolation tests. | `NFR-CAND-SBM-004` | security test | security/privacy owner | Unauthorized access is denied and recorded. | seed |
| VVE-SBM-035 | Exercise blocked, degraded, cancel, recovery, and rollback paths. | `NFR-CAND-SBM-005` | fault injection | operations owner | No failure path becomes silent success. | seed |
| VVE-SBM-036 | Scan active claims against capability/evidence status and implementation paths. | `NFR-CAND-SBM-006` | semantic test | requirements verifier | No unsupported current claim remains. | seed |
| VVE-SBM-037 | Review each new registry proposal for an unrepresentable need. | `NFR-CAND-SBM-007` | design review | system director | Existing representation is used unless gap is approved. | seed |
| VVE-SBM-038 | Validate populated hashes and report pending/stale evidence distinctly. | `NFR-CAND-SBM-008` | hash/review | source authority auditor | Freshness is never inferred from registration alone. | seed |

## 21. Evidence Register

| ID | Source | Source type | Authority class | Used for | Notes |
|---|---|---|---|---|---|
| EVD-SBM-001 | `implementation_plans/Sys4AI-dev_strategic_baseline_migration_full_implementation_plan.md` | implementation plan | planning, noncanonical | Full recommendation, candidate, gate, and workstream scope | Primary discovery source; cannot approve its own candidates. |
| EVD-SBM-002 | `implementation_plans/completion_receipts/CR-SFADEV-STRATEGIC-BASELINE-WS00-001.md` | baseline completion receipt | controlled | Runtime retraction, conflict inventory, hashes, validation, warnings | `TX-00` entry evidence. |
| EVD-SBM-003 | `PRDs/Sys4AI_phase-0_product_system_design_prd.md` | PRD | canonical | Current identity and active requirements | Must not be changed in this transaction. |
| EVD-SBM-004 | `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md` | PRD | canonical_draft | Current implementation obligations | Candidate downstream target only. |
| EVD-SBM-005 | `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md` | PRD | controlled and accepted | Accepted AgentJob and `/continue` flow | Preserve; addendum/successor question remains open. |
| EVD-SBM-006 | `PRDs/Sys4AI_phase-0_prd.md` | historical PRD | historical reference | Vision provenance | Never promote the historical file itself. |
| EVD-SBM-007 | `Sys4AI/control_records/program_state.yaml` | control record | controlled but semantically stale | Current closed state and legacy fields | No active Director Decision or AgentJob at baseline. |
| EVD-SBM-008 | `Sys4AI/registries/system_layer_registry.csv` | registry | controlled | Layer classification | Runtime actor remains a separate candidate axis. |
| EVD-SBM-009 | `Sys4AI/registries/requirement_trace_registry.csv` | registry | controlled | Stale capability and evidence states | Generalized trace migration candidate. |
| EVD-SBM-010 | `Sys4AI/registries/role_registry.csv` and `role_execution_binding_registry.csv` | registries | controlled | Existing role owners and AgentJob-specific fields | Human principal binding remains decision evidence. |
| EVD-SBM-011 | `Sys4AI/registries/artifact_contract_registry.csv` | registry | controlled | Existing RDR and AgentJob contracts | RDR contract reused; no new registry introduced. |
| EVD-SBM-012 | Commit `15a9b17635db2cc76d3f1003f60ea20e46a4e313` | Git commit | immutable repository evidence | Removed runtime capability boundary | Established observation, not a route decision. |
| EVD-SBM-013 | User instruction dated 2026-07-09 | stakeholder direction | direct task authority | Authorizes implementation of the first not-yet-complete plan step | Does not itself approve candidate strategic wording or `WS-02`. |
| EVD-SBM-014 | Supplied PRD analysis summarized in the strategic plan | review memorandum | supplied external evidence | Recommendation families and open decisions | Claims remain subject to repository and stakeholder verification. |

Source-first memory preflight recorded `PASS_WITH_WARNINGS`; the targeted search
for `strategic baseline migration AgentJob continue` routed inspection to the
registered `WS-00` receipt, current registries, trace source, and historical
plans. A generated documentation hit was rejected as authority. Current source
hash warnings remain bounded by `NFR-CAND-SBM-008`.

## 22. Assumptions, Risks, And Constraints

### 22.1 Assumptions

| ID | Assumption | Source | Risk if wrong | Owner | Status |
|---|---|---|---|---|---|
| ASM-SBM-001 | The direct implementation instruction authorizes `TX-01-RDR` discovery and registration, but not later strategic approval. | User instruction and plan gates | Work could cross into unauthorized baseline change. | system director | accepted for this bounded transaction |
| ASM-SBM-002 | The existing RDR and relationship registries can represent this discovery without a new registry. | Registry inspection | A missing concept could be forced into an unsuitable field. | system director | accepted; revisit only on demonstrated gap |
| ASM-SBM-003 | Product-owner and target-sponsor roles can be identified now while named individuals are bound at the applicable approval gate. | Plan gate model | Role-only language could be mistaken for actual approval. | product owner | open; mitigated by authority notice |
| ASM-SBM-004 | The recommended portable execution route can remain a candidate without biasing the formal decision. | Four-route analysis | Preferred wording could suppress viable alternatives. | decision facilitator | open; all four routes retained |

### 22.2 Risks

| ID | Risk | Cause | Impact | Likelihood | Mitigation | Owner | Related IDs |
|---|---|---|---|---|---|---|---|
| RISK-SBM-001 | Discovery candidates are treated as approved requirements. | Detailed candidate wording resembles a baseline. | Premature PRD or implementation change. | medium | Authority notice, candidate IDs, registry status, and `WS-02` gate. | requirements manager | all candidates |
| RISK-SBM-002 | Preferred route 2 becomes an implicit decision. | Plan recommendation is repeated in the RDR. | Alternatives receive inadequate review. | medium | Preserve four routes, contrary evidence, and human decision requirement. | decision facilitator | `REQ-CAND-SBM-EXEC-001` |
| RISK-SBM-003 | Human approval is reduced to a role label without represented stakeholders. | Named individuals and affected-party evidence are not yet supplied. | Weak consent and legitimacy. | high | Bind principals and gather missing stakeholder evidence before `G-02`/`G-08`. | product owner | `STK-SBM-005`, `STK-SBM-006` |
| RISK-SBM-004 | Active and historical AgentJob references are migrated together. | File-level inventories contain mixed authority classes. | Historical evidence loss or stale active claims. | high | Use baseline manifest and per-row semantic review. | baseline change manager | `NFR-CAND-SBM-003`, `NFR-CAND-SBM-006` |
| RISK-SBM-005 | Host profile overclaims current Codex behavior. | Host behavior and permissions may change. | Unsafe or nonportable execution assumptions. | medium | Verify observable behavior at `G-07`; mark unknowns explicitly. | interface owner | `REQ-CAND-SBM-HOST-001` |
| RISK-SBM-006 | Values become slogans or permission grants. | Abstract wording lacks probes or precedence. | Inconsistent or unsafe decisions. | medium | Define behaviors, anti-values, conflict decisions, and negative tests. | product owner/evaluator | `REQ-CAND-SBM-STRAT-002` |
| RISK-SBM-007 | Structural validators provide false assurance. | Semantic truth and stakeholder approval are not machine-decidable. | Incorrect completion or ethical claims. | high | Preserve validator-limit disclaimers and manual semantic/human review. | requirements verifier | `REQ-CAND-SBM-VALID-001` |
| RISK-SBM-008 | Broad migration obscures atomic rollback. | Many authority surfaces depend on one decision. | Difficult review and recovery. | medium | Keep bounded transactions and hard serialization gates. | system director | `NFR-CAND-SBM-007` |

### 22.3 Constraints

| ID | Constraint | Source | Binding status | Related IDs | Open issues |
|---|---|---|---|---|---|
| CON-SBM-010 | `TX-01-RDR` writes only the RDR, required registry relationships, and the deterministic noncanonical registry-catalog refresh caused by source registration. | `WS-01` and repository derivative contract | binding | `BND-IN-SBM-005` | none |
| CON-SBM-011 | All later PRD and implementation changes wait for the named gate. | Gate model | binding | all candidates | `OPEN-SBM-001` through `OPEN-SBM-022` |
| CON-SBM-012 | Historical and generated surfaces are not manually rewritten in this transaction. | Baseline manifest | binding | `NFR-CAND-SBM-003` | none |
| CON-SBM-013 | The RDR routes to `WS-02` only. | `WS-01` acceptance | binding | `REQ-CAND-SBM-EXEC-001` | none |

## 23. Value Conflicts And Anti-Values

Material conflicts must record affected value IDs, context, alternatives,
binding constraints, selected precedence, authority, supporting and contrary
evidence, consequences, review or expiry trigger, and downstream impact.

Explicit anti-values are: unaccountable autonomy; permission expansion by
goal, value, or convenience; hidden authority transfer; unsupported certainty;
framework selection by fashion; validator theater; silent role substitution;
irreversible self-change; cross-target data leakage; evaluator manipulation;
prototype-to-production drift; and history rewriting.

## 24. Phase 2 Change Route And Capability-Retraction Evidence

Phase 2 must use either a controlled addendum or a successor PRD. The existing
accepted Phase 2 source and its draft evidence remain protected. The preferred
candidate is an addendum because it preserves accepted evidence with the
smallest authority change, but `OPEN-SBM-018` reserves the selection for human
decision.

Capability-retraction evidence is established by commit `15a9b17`, the absence
tests, and the exhaustive `WS-00` inventory. The retraction facts are treated
as observed. The meaning of those facts for requirements, lifecycle status,
compatibility, and optional profiles remains a `WS-02` decision.

## 25. Recommendation Coverage

| Recommendation | RDR coverage |
|---|---|
| REC-001 | `REQ-CAND-SBM-ID-001`, `TOBE-SBM-001` |
| REC-002 | `REQ-CAND-SBM-ID-002`, `OPEN-SBM-017` |
| REC-003 | `REQ-CAND-SBM-ID-001`, `VISION-CAND-SBM-001` |
| REC-004 | `REQ-CAND-SBM-STRAT-001`, `OPEN-SBM-004` through `OPEN-SBM-006` |
| REC-005 | `REQ-CAND-SBM-STRAT-002`, value candidates, `OPEN-SBM-007` through `OPEN-SBM-013` |
| REC-006 | `REQ-CAND-SBM-EXEC-001`, Section 24 |
| REC-007 | `REQ-CAND-SBM-EXEC-002`, `NFR-CAND-SBM-001` |
| REC-008 | Candidate requirements in Sections 11 and 12 |
| REC-009 | `REQ-CAND-SBM-PATTERN-001`, `REQ-CAND-SBM-PATTERN-002` |
| REC-010 | `REQ-CAND-SBM-TARGET-001` through `003` |
| REC-011 | `REQ-CAND-SBM-EXEC-003`, `REQ-CAND-SBM-TRACE-001` |
| REC-012 | `REQ-CAND-SBM-TARGET-001` through `003`, `WAIVER-CAND-SBM-001` |
| REC-013 | `REQ-CAND-SBM-HOST-001`, `REQ-CAND-SBM-HOST-002` |
| REC-014 | `CON-SBM-011`; downstream file-specific review |
| REC-015 | `REQ-CAND-SBM-DOC-001` |
| REC-016 | `REQ-CAND-SBM-VALID-001`; downstream Phase 1 initialization |
| REC-017 | `REQ-CAND-SBM-VALID-001` |
| REC-018 | `REQ-CAND-SBM-ID-003`, `REQ-CAND-SBM-VALID-001` |
| REC-019 | `REQ-CAND-SBM-TRACE-001`, `NFR-CAND-SBM-006` |
| REC-020 | `REQ-CAND-SBM-TRACE-001`, `REQ-CAND-SBM-TRACE-002` |
| REC-021 | `REQ-CAND-SBM-VALID-002` |
| REC-022 | `RISK-SBM-007`, `VVE-SBM-022` |
| REC-023 | `REQ-CAND-SBM-SAFETY-001` through `003`, `NFR-CAND-SBM-004` |
| REC-024 | `REQ-CAND-SBM-PH2-001`, `NFR-CAND-SBM-003` |
| REC-025 | `NFR-CAND-SBM-007`, `ASM-SBM-002` |
| REC-026 | `REQ-CAND-SBM-TRACE-002` |
| REC-027 | `REQ-CAND-SBM-STRAT-002`, `VVE-SBM-010` |
| REC-028 | `REQ-CAND-SBM-ATTR-001`, `CON-SBM-008` |
| REC-029 | `CON-SBM-011`, `CON-SBM-013` |

## 26. Open Questions

| ID | Question | Current candidate answer or deferral | Owner | Blocks | Due gate | Status |
|---|---|---|---|---|---|---|
| OPEN-SBM-001 | Who may approve Sys4AI's product identity? | Repository maintainer acting as product owner; bind an accountable human in the decision. | product owner | `G-02` | `G-02` | decision required |
| OPEN-SBM-002 | Who may approve Sys4AI's vision and values? | Product owner with represented stakeholder evidence; model approval prohibited. | product owner | `G-08` | `G-02` role binding; `G-08` approval | decision required |
| OPEN-SBM-003 | Who may approve a target system's purpose, vision, and values? | A named accountable target sponsor, with additional required safety/privacy authorities. | target sponsor | target baseline | `G-04` contract approval | decision required |
| OPEN-SBM-004 | Whose future should improve if Sys4AI succeeds? | People who create, operate, maintain, govern, use, and are affected by target systems. | product owner/user researcher | vision approval | `G-03` | elicitation required |
| OPEN-SBM-005 | What future state and horizon should the vision define? | Candidate future is reliable full-lifecycle stewardship through Codex and compatible hosts; horizon is unset. | product owner | vision approval | `G-03` | decision required |
| OPEN-SBM-006 | What is outside that future state? | Autonomous purpose-setting, permission expansion, consciousness claims, universal framework claims, and automatic ethical approval. | product owner | vision approval | `G-03` | confirm candidate |
| OPEN-SBM-007 | Which tradeoffs will Sys4AI and target agents face? | Safety versus speed, autonomy versus control, portability versus host optimization, evidence cost versus iteration speed, and reuse versus target specificity. | architect/product owner | values and patterns | `G-03` | confirm and expand |
| OPEN-SBM-008 | What observable behavior demonstrates each value? | Section 14 supplies candidate behaviors; scenario probes remain to be approved. | independent evaluator | `G-08` | `WS-13` | evaluation design required |
| OPEN-SBM-009 | What behavior violates each value? | Sections 14 and 23 supply candidate anti-values. | independent evaluator | `G-08` | `WS-13` | evaluation design required |
| OPEN-SBM-010 | Which limits are mandatory constraints rather than values? | Law, platform policy, safety/security/privacy/compliance, source authority, host permissions, and required human approval. | product owner/security owner | values precedence | `G-03` | confirm candidate |
| OPEN-SBM-011 | What happens when values conflict? | Use the proposed precedence and an accountable typed conflict decision; no automatic resolution. | product owner/system director | value governance | `G-03` | decision required |
| OPEN-SBM-012 | Which decisions must remain human-approved? | Purpose, vision, values, authority, permissions, evaluation standards, production promotion, and baseline supersession. | product owner | safety baseline | `G-02` | decision required |
| OPEN-SBM-013 | What evidence and cadence demonstrate continuing alignment? | Incidents, user feedback, model/host changes, evaluation regressions, operational metrics, and periodic value review; cadence unset. | product owner/operations owner | maintenance contract | `G-03` | cadence required |
| OPEN-SBM-014 | Which execution-model route is acceptable after `15a9b17`? | Route 2 is preferred but not approved; all four routes remain under review. | product owner | all canonical migration | `G-02` | decision required |
| OPEN-SBM-015 | Which Codex capabilities are required, optional, denied, or unknown? | Section 18.2 is the candidate inventory; current host evidence is required. | interface owner/host authority | host-dependent claims | `G-07` | verification required |
| OPEN-SBM-016 | What degraded behavior is acceptable when a host capability is missing? | Block required actions; reroute or explicitly degrade optional actions; never assume success. | product owner/interface owner | host profile | `G-07` | decision and tests required |
| OPEN-SBM-017 | Does the Meta-Agent Runtime need a separate authority layer? | No initially; use `runtime_actor` unless a representation gap is demonstrated. | system architect/product owner | layer schemas | `G-02` | decision required |
| OPEN-SBM-018 | Should Phase 2 use an addendum or successor PRD? | Addendum is preferred for minimal historical disturbance. | product owner | `G-06` | `G-06` | decision required |
| OPEN-SBM-019 | Which roles own strategic-intent facilitation, custody, verification, approval, and impact analysis? | Existing elicitor, requirements manager, source auditor, verifier, system director, and human product/target owners are candidates. | system director/product owner | artifact contracts | `G-04` | role decision required |
| OPEN-SBM-020 | What is the maximum default reflection depth? | Candidate default is one; expansion requires explicit bounded authorization and stop conditions. | product owner/security owner | self-change controls | `WS-13` | decision required |
| OPEN-SBM-021 | What evidence is required before prototype-to-production promotion? | Evaluation, security, integration, ownership, rollback, monitoring, incident response, and human approval evidence. | target sponsor/operations/security owners | production promotion | `WS-13` | thresholds required |
| OPEN-SBM-022 | What retirement, archival, and data-disposition obligations apply? | Section 11 provides a candidate minimum; target, legal, privacy, and operational specifics remain per system. | target sponsor/data/operations owners | retirement contract | `G-03` | decision required |

## 27. Downstream Routing Recommendation

| Route | Use when | Current recommendation | Blocking open issues |
|---|---|---|---|
| `WS-02` Director Decision | Composite identity and post-retraction execution route require authority. | yes; only next route | `OPEN-SBM-001`, `OPEN-SBM-014`, `OPEN-SBM-017` |
| decision-grilling-context-45 | Product owner wants structured exploration of identity, route, principal binding, or Phase 2 route. | optional support inside `WS-02` | `OPEN-SBM-001`, `OPEN-SBM-014`, `OPEN-SBM-017`, `OPEN-SBM-018` |
| stakeholder elicitation | Vision, values, affected parties, cadence, and production thresholds need evidence. | required before `G-03`/`G-08` | `OPEN-SBM-002` through `OPEN-SBM-013`, `OPEN-SBM-021`, `OPEN-SBM-022` |
| conversation-to-PRD | Candidate content is approved for canonical synthesis. | no | `G-02` not accepted |
| schema, validator, host, or runtime implementation | Contracts and authority are approved. | no | `G-03` through `G-07` not accepted |

The next transaction must be `TX-02-DECISION`/`WS-02`. It may approve, reject,
revise, or split the identity and execution decisions. It must not treat this
RDR as the decision itself.

## 28. Completion Evidence

| Evidence item | Value |
|---|---|
| Transaction | `TX-01-RDR` |
| Sources inspected | Strategic plan; `WS-00` receipt; Phase 0, Phase 1, Phase 2, historical Phase 0; program state; layer, role, artifact, source, discovery, relationship, and trace registries; RDR template and validator |
| Required discovery questions | 22 recorded as `OPEN-SBM-001` through `OPEN-SBM-022` with owner and due gate |
| Candidate requirements created | 38: `REQ-CAND-SBM-*` (30) and `NFR-CAND-SBM-*` (8) |
| Strategic candidates created | 1 vision, 8 values, and 1 waiver candidate |
| Recommendation coverage | `REC-001` through `REC-029` mapped in Section 25 |
| Open issues created | 22 decision or elicitation questions |
| Manual semantic review | Candidate status, source type, actor/authority distinction, execution-route neutrality, stakeholder coverage, and recommendation coverage reviewed by the requirements-manager role; no human approval claimed |
| Validators run | `validate-discovery-records`; `validate-registry-graph`; `memory validate-hashes --json`; `generate-governance-docs --check`; `git diff --check`; aggregate `make validate` |
| Generated derivative refresh | Only `Sys4AI/docs/generated/registry_catalog/index.md`, regenerated deterministically after the initial check detected expected source-registry drift |
| Validation status | `PASS_WITH_WARNINGS`; focused checks pass, populated hashes match, and pending source hashes remain explicit freshness warnings |
| Next recommended role | Product owner and system director using the Director Decision governor for `WS-02` |

## References

AngryOwlAI. (2026a). *Sys4AI Phase 0 product and system-design PRD* [Product requirements document]. `PRDs/Sys4AI_phase-0_product_system_design_prd.md`.

AngryOwlAI. (2026b). *Sys4AI Phase 1 implementation initialization PRD* [Product requirements document]. `PRDs/Sys4AI_phase-1_implementation_initialization_prd.md`.

AngryOwlAI. (2026c). *Sys4AI Phase 2 walking skeleton PRD* [Product requirements document]. `PRDs/Sys4AI_phase-2_walking_skeleton_prd.md`.

Sys4AI-dev. (2026a). *Strategic baseline migration full implementation plan* [Implementation plan]. `implementation_plans/Sys4AI-dev_strategic_baseline_migration_full_implementation_plan.md`.

Sys4AI-dev. (2026b). *Strategic baseline migration WS-00 completion receipt* [Completion receipt]. `implementation_plans/completion_receipts/CR-SFADEV-STRATEGIC-BASELINE-WS00-001.md`.
