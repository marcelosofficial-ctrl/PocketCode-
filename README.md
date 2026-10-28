# PocketCode

**Vibe code. Run it. Fix it. From your phone.**

PocketCode is an early-stage project exploring a mobile-first workspace for people who use AI to create code and want to test and improve it without always having access to a computer.

## The idea

AI can generate code, but generated code still needs to be run, inspected, and corrected. PocketCode is exploring a provider-neutral workflow that helps people:

1. Bring code and project files into a phone-friendly workspace.
2. Run supported code in an appropriate isolated environment.
3. Inspect actual output, errors, exit status, and generated files.
4. Share execution evidence with the AI assistant of their choice.
5. Review changes and rerun to check whether they worked.

This is a product hypothesis, not a claim that these capabilities are already implemented or unique to PocketCode. Our working marketing angle is vibe coding from your phone; the product proof we need is reliable, real execution and debugging.

## Current status

**Discovery and product definition.** No production runtime, cloud provider, framework, pricing model, or supported-language commitment has been finalized.

The initial MVP candidate is a mobile-first web app with one remote runtime and a clear, verifiable run-and-inspect workflow. The scope will be narrowed through competitor research, user feedback, and technical testing.

## Project documents

## AI Workflow Director research

The proposed AI Workflow Director aims to help users hand off compact tasks and preserve verified state across AI apps. It is a research proposal, not an implemented feature. The [current research checkpoint](AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md) records the active branch, verified boundaries, and next work sequence. The [deterministic conformance test specification](AI_COLLAB/AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) defines proposed assertions for all 16 static acceptance cases; no tests have been run. See the [master research](AI_COLLAB/MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md), [first testable slice](AI_COLLAB/AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md), [offline evaluation kit](AI_COLLAB/AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md), [human-authored reference fixtures](AI_COLLAB/AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md), and [phone-friendly paired-run sheet](AI_COLLAB/AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md). No evaluation runs or benchmark results are claimed.

## Project documents

- [Project status](PROJECT_STATUS.md)
- [Zero-budget work plan](PRODUCT/ZERO_BUDGET_WORK_PLAN.md)
- [Product specification](PRODUCT_SPEC.md)
- [RevDev + PocketCode shared-core proposal](PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md)
- [Mobile technical task opportunity map](PRODUCT/MOBILE_TECHNICAL_TASKS.md)
- [First-run workflow](PRODUCT/FIRST_RUN_WORKFLOW.md)
- [Execution loop acceptance criteria](PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) (proposed; not yet implemented or run)
- [Desk research on mobile-coding user feedback](RESEARCH/MOBILE_CODING_USER_EVIDENCE.md)
- [Optional user validation interview script (not yet conducted)](PRODUCT/USER_VALIDATION_SCRIPT.md)
- [Controlled Python execution proof runbook (not yet executed)](PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md)
- [Interactive mobile runner prototype source (simulated; no code execution)](prototypes/mobile-runner/index.html)
- [How to enable and review the phone preview](prototypes/mobile-runner/README.md)
- [Prototype static checker](scripts/check_mobile_prototype.py) and [its regression tests](scripts/test_check_mobile_prototype.py) (CI checks source patterns only; no browser execution or submitted-code execution)
- [Proposed provider-neutral execution contract](PRODUCT/EXECUTION_CONTRACT.md)
- [Roadmap](ROADMAP.md)
- [Architecture proposal](ARCHITECTURE.md)
- [Safety requirements](SECURITY.md)
- [Decision log](DECISIONS.md)
- [Cross-agent contributor instructions](AGENTS.md)
- [Marketing and positioning hypothesis](MARKETING/POSITIONING_HYPOTHESIS.md)
- [Gemini co-developer handoff](AI_COLLAB/GEMINI_HANDOFF.md)
- [Master research and implementation plan](AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md)
- [Master AI Workflow Director research](AI_COLLAB/MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md) (proposal; not implemented or validated)
- [AI Workflow Director first testable feature slice](AI_COLLAB/AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) (proposed profiles, packet/capsule contracts, and acceptance cases)
- [AI Workflow Director offline evaluation kit](AI_COLLAB/AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md) (eight paired-test fixtures and scoring protocol; no results claimed)
- [AI Workflow Director reference output fixtures](AI_COLLAB/AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) (human-authored scoring examples for five cases; not benchmark results)  
- [AI Workflow Director canonical conformance fixtures](AI_COLLAB/AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md) (16 proposed deterministic inputs and observable assertions; not executed)
- [AI Workflow Director contract decision register](AI_COLLAB/AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) (MVP reconciliation, open decisions, and implementation gate; recommendations not approved)
- [AI Workflow Director pre-implementation readiness audit](AI_COLLAB/AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md) (focused risk review; implementation still requires explicit authorization)
- [Initial independent provider review](AI_COLLAB/CHATGPT_INITIAL_PROVIDER_REVIEW.md)
- [MVP execution-provider decision brief](AI_COLLAB/MVP_DECISION_BRIEF.md)
- [Independent review of Gemini's architecture proposal](AI_COLLAB/CHATGPT_REVIEW_OF_GEMINI_PLAN.md)
- [Initial competitor research](RESEARCH/COMPETITOR_MATRIX.md)
- [Competitive analysis and positioning hypotheses](RESEARCH/COMPETITIVE_ANALYSIS.md)
- [Code execution backend research](RESEARCH/EXECUTION_PROVIDER_RESEARCH.md)

## Principles

- Mobile-first, with no assumption that the user has a PC nearby.
- Provider-neutral, with no mandatory AI subscription or vendor lock-in.
- Honest about which runtimes and features are actually supported.
- Execution evidence over unverified success claims.
- User code and files must be handled with security, privacy, and resource limits in mind.
- Code, projects, and results should remain exportable.

## Contributing and AI collaboration

Read [AGENTS.md](AGENTS.md) before proposing or making changes. Claude-specific and Gemini-specific entry instructions are provided in [CLAUDE.md](CLAUDE.md) and [GEMINI.md](GEMINI.md).

The repository is public. Do not commit API keys, credentials, private user data, or production secrets.

## Naming

PocketCode is a provisional project name. Naming, product collisions, trademark risk, and domain availability have not yet been fully reviewed.
