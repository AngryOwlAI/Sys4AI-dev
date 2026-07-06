# System Document Spine

## Purpose

Define the document chain used by `sys-for-ai` when designing, developing, running, improving, and maintaining target agentic systems.

This spine prevents a Product Requirements Document from absorbing every systems-engineering responsibility. It also gives agents a predictable route from early discovery through requirements, architecture, verification, operations, and closeout.

## PRD acronym rule

Always expand `PRD` on first use. In this repository, `PRD` usually means Product Requirements Document unless a document explicitly says Project Requirements Document.

A Product Requirements Document is not the only requirements source for complex systems. It records product intent and product-facing obligations; system, software, interface, verification, and operations obligations require separate controlled surfaces when the work becomes complex enough.

## Practical document chain

The normal chain is:

1. Mission Need or Business Case
2. Program or Project Charter
3. System Definition Discovery Record
4. Concept of Operations
5. Stakeholder Requirements
6. Product Requirements Document or Business Requirements Document, when product-facing
7. System Requirements Document or System Requirements Specification
8. Software Requirements Specification for software-specific obligations
9. Architecture Description or Architecture Requirements Document
10. Interface Control Documents or interface specifications
11. Systems Engineering Management Plan and technical management plans
12. Requirements Traceability Matrix or Requirements Verification Matrix
13. Verification and Validation Plan and Test Plan
14. Deployment, Operations, and Maintenance Plan
15. Closeout and Lessons Learned

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
