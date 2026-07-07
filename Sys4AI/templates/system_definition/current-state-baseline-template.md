# Current-State Baseline

**Record ID:** CSB-<YYYYMMDD>-<NNN>
**Status:** draft_discovery_evidence
**System name:** <system name>
**Prepared by role:** <role or agent>
**Authorized by AgentJob:** <AgentJob ID or Director decision ID>
**Subject system ID:** <system ID>
**Subject layer:** development_system / framework_product / target_system_template / target_system_instance / derivative_surface
**Source authority status:** derivative_draft
**Created:** <YYYY-MM-DD>
**Last updated:** <YYYY-MM-DD>

---

## 1. Authority Notice

This record is a brownfield discovery artifact. It captures observed repository state, source evidence, assumptions, risks, maintenance goals, migration pressures, and open questions.

This record is not a canonical requirements baseline unless promoted through the project source-authority process. Canonical PRDs, source registries, decision records, approved requirements, and control records outrank this document.

Candidate requirements must remain labeled as `REQ-CAND-*` or `NFR-CAND-*` until promoted by project authority.

## 2. Repository Identity

| Field | Value | Evidence | Open Issues |
|---|---|---|---|
| Repository root | <path> | <source> | <OPEN-*> |
| Primary language or stack | <text> | <source> | <OPEN-*> |
| Main entry points | <text> | <source> | <OPEN-*> |
| Test or validation commands | <text> | <source> | <OPEN-*> |
| Build or packaging commands | <text> | <source> | <OPEN-*> |

## 3. System Of Interest

| Field | Value | Evidence status | Source |
|---|---|---|---|
| System name | <text> | stated / inferred / missing | <source> |
| Current system purpose | <text> | stated / inferred / missing | <source> |
| Intended lifecycle goal | build / improve / maintain / operate / migrate / recover / unknown | stated / inferred / missing | <source> |
| Subject layer | <layer> | stated / inferred / missing | <source> |

## 4. Source Evidence

| ID | Source | Source type | Authority class | Used for | Notes |
|---|---|---|---|---|---|
| EVD-001 | <path or statement> | repo file / PRD / test / config / user statement / unavailable | canonical / controlled / derivative / external / unavailable | <IDs> | <notes> |

## 5. Documentation And Governance Surfaces

| Surface | Present? | Evidence | Observed status | Open issues |
|---|---|---|---|---|
| README or front door | yes / no / unknown | <source> | current / stale / conflicting / unknown | <OPEN-*> |
| PRD or product requirements | yes / no / unknown | <source> | current / stale / conflicting / unknown | <OPEN-*> |
| Implementation plan | yes / no / unknown | <source> | current / stale / conflicting / unknown | <OPEN-*> |
| Tests or validation | yes / no / unknown | <source> | current / stale / failing / unknown | <OPEN-*> |
| Source registry or authority map | yes / no / unknown | <source> | current / stale / missing / unknown | <OPEN-*> |
| Control records or handoffs | yes / no / unknown | <source> | current / stale / missing / unknown | <OPEN-*> |

## 6. Architecture Observations

| ID | Observation | Evidence | Confidence | Notes |
|---|---|---|---|---|
| ARCH-001 | <observation> | <source> | high / medium / low | <notes> |

## 7. Interface And Integration Observations

| ID | Interface or external system | Direction | Evidence | Owner | Open issues |
|---|---|---|---|---|---|
| IF-001 | <interface> | input / output / bidirectional / unknown | <source> | <owner> | <OPEN-*> |

## 8. Operational Risks And Maintenance Goals

| ID | Risk or goal | Type | Evidence | Impact | Recommended handling |
|---|---|---|---|---|---|
| RISK-001 | <risk> | reliability / security / maintainability / migration / governance / unknown | <source> | high / medium / low | <route> |
| GOAL-001 | <goal> | improve / maintain / operate / migrate / recover | <source> | high / medium / low | <route> |

## 9. Migration Pressures

| ID | Pressure | Cause | Evidence | Timing | Open issues |
|---|---|---|---|---|---|
| MIG-001 | <pressure> | <cause> | <source> | now / later / unknown | <OPEN-*> |

## 10. Sys4AI Adoption Recommendation

| Route | Use when | Current recommendation | Blocking open issues |
|---|---|---|---|
| Requirements Discovery Record | Intent or requirements need controlled discovery. | yes / no / later | OPEN-* |
| Product Requirements Document | Product-facing intent is ready and approved. | yes / no / later | OPEN-* |
| Implementation plan or AgentJob | Governance adoption is approved. | yes / no / later | OPEN-* |
| Operations and maintenance planning | Sustainment goals are explicit. | yes / no / later | OPEN-* |

## 11. Open Questions

| ID | Question | Why it matters | Owner | Blocks | Recommended next route | Status |
|---|---|---|---|---|---|---|
| OPEN-001 | <question> | <impact> | <owner> | <IDs> | stakeholder answer / source inspection / decision-grilling / domain-grilling | open |

