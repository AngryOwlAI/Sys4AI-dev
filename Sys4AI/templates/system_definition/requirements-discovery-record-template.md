# Requirements Discovery Record

**Record ID:** RDR-<YYYYMMDD>-<NNN>
**Status:** draft_discovery_evidence
**System name:** <system name>
**Prepared by role:** <role or agent>
**Authorized by:** <Explicit project authorization, Director decision ID, or portable transaction ID>
**Subject system ID:** <system ID>
**Subject layer:** development_system / framework_product / target_system_template / target_system_instance / derivative_surface
**Discovery gate:** system-definition-interview-context-45
**Producer authority:** <Explicit project authorization, Director decision ID, or portable transaction ID>
**Discovery registry row:** <discovery_record_registry.csv row ID>
**Downstream artifact status:** no USRD yet / USRD proposed / USRD created / discovery waived
**Source authority status:** derivative_draft
**Created:** <YYYY-MM-DD>
**Last updated:** <YYYY-MM-DD>

---

## 1. Authority Notice

This record is a discovery artifact. It captures stakeholder statements, source evidence, assumptions, candidate requirements, risks, and open questions.

This record is not a canonical requirements baseline unless promoted through the project source-authority process. Canonical PRDs, source registries, decision records, approved requirements, and control records outrank this document.

Candidate requirements must remain labeled as `REQ-CAND-*` or `NFR-CAND-*` until promoted by project authority.

---

## 2. System Layer Classification

| Field | Value | Evidence | Open Issues |
|---|---|---|---|
| Subject layer | <layer> | <source> | <OPEN-*> |
| Active authority root | <path or registry> | <source> | <OPEN-*> |
| Product scaffold involved? | yes / no / unknown | <source> | <OPEN-*> |
| Target-system instance involved? | yes / no / unknown | <source> | <OPEN-*> |
| Derivative surfaces involved? | yes / no / unknown | <source> | <OPEN-*> |

---

## 3. Discovery Gate Exit Checklist

| Check | Status | Evidence | Blocking Issues |
|---|---|---|---|
| Subject layer classified | pass / warn / fail | <evidence> | <OPEN-*> |
| Mission need captured or marked missing | pass / warn / fail | <evidence> | <OPEN-*> |
| Problem statement captured or marked missing | pass / warn / fail | <evidence> | <OPEN-*> |
| System-of-interest identified | pass / warn / fail | <evidence> | <OPEN-*> |
| Stakeholders identified | pass / warn / fail | <evidence> | <OPEN-*> |
| Boundaries captured | pass / warn / fail | <evidence> | <OPEN-*> |
| Candidate requirements remain candidate-labeled | pass / warn / fail | <evidence> | <OPEN-*> |
| Evidence register populated | pass / warn / fail | <evidence> | <OPEN-*> |
| Open questions routed | pass / warn / fail | <evidence> | <OPEN-*> |
| Next route recommended | pass / warn / fail | <evidence> | <OPEN-*> |

---

## 2. System Intent Profile

| Field | Value | Source | Evidence status |
|---|---|---|---|
| Mission need | <text> | <source> | stated / inferred / missing |
| Problem statement | <text> | <source> | stated / inferred / missing |
| Desired outcome | <text> | <source> | stated / inferred / missing |
| Value case | <text> | <source> | stated / inferred / missing |
| System-of-interest | <text> | <source> | stated / inferred / missing |
| System type | new / existing / partially built / documentation recovery | <source> | stated / inferred / missing |
| Success criteria | <text> | <source> | stated / inferred / missing |
| Primary constraints | <text> | <source> | stated / inferred / missing |

---

## Strategic Intent Candidates

Candidate strategic intent is discovery evidence, not approval. Use `VISION-CAND-*`, `VALUE-CAND-*`, and `WAIVER-CAND-*` labels until an accountable human approves a separately registered target artifact.

### Mission Versus Vision And Future State

| ID | Candidate future-state statement | Mission distinction | Intended users and beneficiaries | Desired condition and impact | Horizon | Scope and non-goals | Success signals | Source | Evidence status |
|---|---|---|---|---|---|---|---|---|---|
| VISION-CAND-001 | <candidate future state> | <difference from mission> | <stakeholders> | <condition and impact> | <horizon> | <scope> | <signals> | <source> | stated / inferred / missing |

### Core-Value Candidates Anti-Values And Conflicts

| ID | Candidate commitment | Rationale | Positive behavior | Prohibited behavior or anti-value | Decision test | Conflict or precedence | Source and owner | Evidence status |
|---|---|---|---|---|---|---|---|---|
| VALUE-CAND-001 | <commitment> | <why> | <behavior> | <prohibition> | <test> | <rule or OPEN-*> | <source and owner> | stated / inferred / missing |

### Authority Inheritance Waiver And Review

| Field | Candidate value | Source or authority | Status / blocking effect |
|---|---|---|---|
| Missing or unrepresented stakeholders | <classes> | <source> | none / review required / blocks approval |
| Accountable approval principal | <human role or missing> | <source> | identified / missing |
| Inherited Sys4AI constraints | <constraints> | <source> | binding / candidate / unknown |
| Waiver candidate | <WAIVER-CAND-* or none> | <authority> | proposed / active / expired / superseded / none |
| Review cadence and triggers | <cadence> | <owner> | candidate |

### Pattern Operations And Promotion Context

| Field | Candidate value | Source | Evidence status / open issue |
|---|---|---|---|
| Coordination pattern | hierarchical / flat_multi_agent / blackboard / market_or_contract_net / hybrid / unknown | <source> | stated / inferred / missing |
| Operational maturity | conceptual / planned / prototype / test_run / staging / production / maintenance / retired / unknown | <source> | stated / inferred / missing |
| Autonomy and permission boundary | <boundary> | <source> | stated / inferred / missing |
| Integrations and interfaces | <systems> | <source> | stated / inferred / missing |
| Communication and handoffs | <channels> | <source> | stated / inferred / missing |
| Monitoring and review | <signals and cadence> | <source> | stated / inferred / missing |
| Degraded or blocked behavior | <behavior> | <source> | stated / inferred / missing |
| Promotion evidence | <required evidence> | <source> | candidate / missing |

---

## 3. Needs

| ID | Need statement | Source | Evidence status | Related stakeholders |
|---|---|---|---|---|
| NEED-001 | <need> | <source> | stated / inferred / missing | STK-001 |

---

## 4. Stakeholders And Roles

| ID | Stakeholder class | Role in system | Primary need | Decision authority | Source | Evidence status |
|---|---|---|---|---|---|---|
| STK-001 | <class> | <role> | <need> | yes / no / unknown | <source> | stated / inferred / missing |

---

## 5. System Boundary

### 5.1 In Scope

| ID | Capability / responsibility | Source | Evidence status |
|---|---|---|---|
| BND-IN-001 | <text> | <source> | stated / inferred / missing |

### 5.2 Out Of Scope

| ID | Exclusion | Rationale | Source | Evidence status |
|---|---|---|---|---|
| BND-OUT-001 | <text> | <why excluded> | <source> | stated / inferred / missing |

### 5.3 External Systems And Interfaces

| ID | External system / actor | Relationship | Input/output | Owner | Source | Open issues |
|---|---|---|---|---|---|---|
| EXT-001 | <name> | <relationship> | <I/O> | <owner> | <source> | OPEN-001 |

---

## 6. As-Is State

| ID | Observation | Source | Evidence type | Confidence | Notes |
|---|---|---|---|---|---|
| ASIS-001 | <text> | <source> | observed / stated / inferred | high / medium / low | <notes> |

---

## 7. To-Be State

| ID | Desired future behavior | Source | Evidence status | Related need |
|---|---|---|---|---|
| TOBE-001 | <text> | <source> | stated / inferred / missing | NEED-001 |

---

## 8. Operational Scenarios And ConOps Seeds

| ID | Scenario | Actors | Trigger | Normal flow | Exception/degraded flow | Related needs | Evidence |
|---|---|---|---|---|---|---|---|
| SCN-001 | <name> | <actors> | <trigger> | <flow> | <exceptions> | NEED-001 | <source> |

---

## 9. Candidate Requirements

### 9.1 Candidate Functional Requirements

| ID | Candidate requirement | Source need/scenario | Rationale | Priority | Verification seed | Status |
|---|---|---|---|---|---|---|
| REQ-CAND-001 | The system should <candidate behavior>. | NEED-001 / SCN-001 | <why> | Must / Should / Could / Later / unknown | VVE-001 | candidate |

### 9.2 Candidate Quality Attributes

| ID | Quality attribute | Candidate statement | Source | Threshold / measure | Verification seed | Status |
|---|---|---|---|---|---|---|
| NFR-CAND-001 | <attribute> | <candidate statement> | <source> | <measure or OPEN-*> | VVE-002 | candidate |

---

## 10. Architecture Drivers

| ID | Driver | Type | Source | Why it matters | Related candidates | Open issues |
|---|---|---|---|---|---|---|
| DRV-001 | <driver> | quality / interface / data / safety / security / operations / constraint | <source> | <rationale> | REQ-CAND-001 | OPEN-001 |

---

## 11. Interface Candidates

| ID | Interface candidate | Producer | Consumer | Data / command / event | Frequency | Owner | Related scenario | Open issues |
|---|---|---|---|---|---|---|---|---|
| IF-001 | <interface> | <producer> | <consumer> | <payload> | <frequency> | <owner> | SCN-001 | OPEN-002 |

---

## 12. Verification And Validation Seeds

| ID | Candidate evidence or check | Traces to | Method | Owner/gate | Acceptance idea | Status |
|---|---|---|---|---|---|---|
| VVE-001 | <evidence/check> | REQ-CAND-001 | inspection / analysis / demonstration / test / review | <owner> | <acceptance idea> | seed |

---

## 13. Evidence Register

| ID | Source | Source type | Authority class | Used for | Notes |
|---|---|---|---|---|---|
| EVD-001 | <path, statement, interview note, source ID> | user statement / repo file / PRD / ADR / test / diagram | canonical / controlled / derivative / external / unavailable | <IDs> | <notes> |

---

## 14. Assumptions, Risks, And Constraints

### 14.1 Assumptions

| ID | Assumption | Source | Risk if wrong | Owner | Status |
|---|---|---|---|---|---|
| ASM-001 | <text> | <source> | <risk> | <owner> | open / accepted / rejected |

### 14.2 Risks

| ID | Risk | Cause | Impact | Likelihood | Mitigation | Owner | Related IDs |
|---|---|---|---|---|---|---|---|
| RISK-001 | <risk> | <cause> | <impact> | high / medium / low | <mitigation> | <owner> | <IDs> |

### 14.3 Constraints

| ID | Constraint | Source | Binding status | Related IDs | Open issues |
|---|---|---|---|---|---|
| CON-001 | <constraint> | <source> | binding / candidate / unknown | <IDs> | OPEN-001 |

---

## 15. Open Questions

| ID | Question | Why it matters | Owner | Blocks | Recommended next route | Status |
|---|---|---|---|---|---|---|
| OPEN-001 | <question> | <impact> | <owner> | <IDs> | decision-grilling / domain-grilling / stakeholder answer / source inspection | open |

---

## 16. Downstream Routing Recommendation

| Route | Use when | Current recommendation | Blocking open issues |
|---|---|---|---|
| decision-grilling-context-45 | Scope or design decision remains unclear. | yes / no / later | OPEN-* |
| domain-grilling-with-docs-context-45 | Terminology or documentation conflict remains unresolved. | yes / no / later | OPEN-* |
| conversation-to-prd | Product requirements are ready to synthesize. | yes / no / later | OPEN-* |
| SRD/SyRS generation | System requirements are ready to baseline. | yes / no / later | OPEN-* |
| architecture requirements | Requirements are stable enough for architecture. | yes / no / later | OPEN-* |

---

## 17. Completion Evidence

| Evidence item | Value |
|---|---|
| Authorization or transaction ID | <ID> |
| Sources inspected | <list> |
| Questions asked | <count/list> |
| Candidate requirements created | <count/list> |
| Open issues created | <count/list> |
| Validators run | <commands> |
| Validation status | pass / repair / block |
| Next recommended role | <role/skill> |
