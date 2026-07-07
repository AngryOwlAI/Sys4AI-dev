# System Document Spine

## Purpose

Define the document chain used by `Sys4AI` when designing, developing, running, improving, and maintaining target agentic systems.

This spine prevents a Product Requirements Document from absorbing every systems-engineering responsibility. It also gives agents a predictable route from early discovery through requirements, architecture, verification, operations, and closeout.

## PRD acronym rule

Always expand `PRD` on first use. In this repository, `PRD` usually means Product Requirements Document unless a document explicitly says Project Requirements Document.

A Product Requirements Document is not the only requirements source for complex systems. It records product intent and product-facing obligations; system, software, interface, verification, and operations obligations require separate controlled surfaces when the work becomes complex enough.

## Practical document chain

When the user invokes `/init`, treat it as the practical entry into this
document spine. `/init` classifies whether the system is greenfield,
brownfield, partially built, or in documentation recovery; identifies the
system-of-interest and subject layer; inspects available evidence; and asks for
approval before writing controlled artifacts.

For brownfield repositories, `/init` may produce a chat-visible Current-State
Baseline summary during its first pass, but the first pass remains read-only.
A controlled Current-State Baseline file, Requirements Discovery Record,
Product Requirements Document, system requirements document, implementation
plan, AgentJob, or scaffold requires explicit approval.

The normal chain is:

1. Mission Need or Business Case
2. Program or Project Charter
3. `/init` classification and evidence summary
4. Current-State Baseline, when the target is brownfield
5. System Definition Discovery Record
6. Concept of Operations
7. Stakeholder Requirements
8. Product Requirements Document or Business Requirements Document, when product-facing
9. System Requirements Document or System Requirements Specification
10. Software Requirements Specification for software-specific obligations
11. Architecture Description or Architecture Requirements Document
12. Interface Control Documents or interface specifications
13. Systems Engineering Management Plan and technical management plans
14. Requirements Traceability Matrix or Requirements Verification Matrix
15. Verification and Validation Plan and Test Plan
16. Deployment, Operations, and Maintenance Plan
17. Closeout and Lessons Learned

This is a practical route, not a demand to create every artifact for every target system.

## Phase 1 immediate scope

Phase 1 creates the scaffolding needed to govern later system work:

- skill adapters,
- discovery templates,
- validators,
- registries,
- AgentJobs,
- source-first authority rules.

Phase 1 does not create every formal system document. It creates enough validated structure for future agents to produce those documents under explicit authorization.

## Authority rules

- Discovery records are draft evidence until promoted.
- Product Requirements Documents define product intent and phase boundaries.
- System requirements documents define system obligations.
- Software requirements documents define software obligations.
- Architecture documents explain solution structure and tradeoffs.
- Interface documents define boundary contracts.
- Verification and validation artifacts define evidence.
- Operations and maintenance artifacts define sustainment obligations.
- Closeout artifacts preserve decisions, lessons, and residual risks.

When these surfaces conflict, use the source registry, control records, decision records, and validators to identify the current authority before changing downstream documents.
