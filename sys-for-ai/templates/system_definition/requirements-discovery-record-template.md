# Requirements Discovery Record

**Record ID:** RDR-<YYYYMMDD>-<NNN>
**Status:** draft_discovery_evidence
**System name:** <system name>
**Prepared by role:** <role or agent>
**Authorized by AgentJob:** <AgentJob ID or Director decision ID>
**Source authority status:** derivative_draft
**Created:** <YYYY-MM-DD>
**Last updated:** <YYYY-MM-DD>

---

## 1. Authority Notice

This record is a discovery artifact. It captures stakeholder statements, source evidence, assumptions, candidate requirements, risks, and open questions.

This record is not a canonical requirements baseline unless promoted through the project source-authority process. Canonical PRDs, source registries, decision records, approved requirements, and control records outrank this document.

Candidate requirements must remain labeled as `REQ-CAND-*` or `NFR-CAND-*` until promoted by project authority.

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
| AgentJob ID | <ID> |
| Sources inspected | <list> |
| Questions asked | <count/list> |
| Candidate requirements created | <count/list> |
| Open issues created | <count/list> |
| Validators run | <commands> |
| Validation status | pass / repair / block |
| Next recommended role | <role/skill> |
