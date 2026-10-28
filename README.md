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

## Start here — read in this order

1. **[PocketCode Continuity Hub](AI_COLLAB/POCKETCODE_CONTINUITY_HUB_20261028.md)** — source-of-truth order, branch/PR map, evidence boundaries, and three-AI collaboration method.
2. **[Complete new-chat handoff](AI_COLLAB/NEW_CHAT_HANDOFF_20261028.md)** — consolidated mission, phone-only plan, exact branch/PR state, constraints, and next actions.
3. **[Four-month phone-only master plan](AI_COLLAB/FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md)** — month-by-month workstreams through February 2027, future-feature priorities, and decisions to defer.
4. **[Current work checkpoint](AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md)** — latest pass results, status, open work, and exact next actions.
5. **[PC-return checklist draft](AI_COLLAB/PC_RETURN_CHECKLIST_DRAFT_20261028.md)** — safe branch/blob verification and offline tests for when a PC becomes available; no live provider testing is authorized by this checklist.

This is an isolated research branch. These documents do not mean the plan or research is integrated into `main`, and they do not authorize implementation, spending, merges, deployment, Actions, or provider workloads.

## Product and execution contracts

- [Product specification](PRODUCT_SPEC.md) — target-user hypothesis, core workflow, MVP candidate, open decisions.
- [Project status](PROJECT_STATUS.md) and [roadmap](ROADMAP.md) — current phase and evidence-based exit gates.
- [Execution contract](PRODUCT/EXECUTION_CONTRACT.md) — proposed request/result/report lifecycle; not an implemented API.
- [Execution-loop acceptance criteria](PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) — evidence required for a useful end-to-end proof; not yet implemented or run.
- [Security requirements](SECURITY.md) — gates that must be satisfied before any public user-code execution.
- [Architecture proposal](ARCHITECTURE.md) and [decision log](DECISIONS.md) — proposed system boundaries and recorded decisions.
- [Zero-budget work plan](PRODUCT/ZERO_BUDGET_WORK_PLAN.md) and [controlled Python proof runbook](PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md) — cost limits and future proof steps; the runbook is not executed.
- [Mobile technical task map](PRODUCT/MOBILE_TECHNICAL_TASKS.md) and [first-run workflow](PRODUCT/FIRST_RUN_WORKFLOW.md) — wider opportunities and onboarding flow.
- [RevDev + PocketCode shared-core proposal](PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md) — exploratory cross-project alignment only; the repositories and source-of-truth remain separate.

## Current decision and research

- **[Product hypothesis card](AI_COLLAB/PRODUCT_HYPOTHESIS_CARD_20261028.md)** — candidate job, alternatives, counter-hypotheses, and falsification criteria; not validated.
- **[Fixed-task comparison worksheet](AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md)** — synthetic CSV-to-JSON task across local iOS, browser/WASM, remote-PC, hosted, and manual paths; design only, comparison NOT RUN.
- **[Execution-contract cross-branch audit](AI_COLLAB/EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md)** — static main/PR #2/PR #3 comparison and candidate verdict mapping; no tests run by this audit.
- **[Phone-only competitor scan addendum](AI_COLLAB/PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md)**, [competitor matrix](RESEARCH/COMPETITOR_MATRIX.md), and [competitive analysis](RESEARCH/COMPETITIVE_ANALYSIS.md) — source-based research, not hands-on performance/security tests.
- [Mobile-coding user evidence](RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) — preliminary public evidence, not representative research.
- [Marketing and positioning hypothesis](MARKETING/POSITIONING_HYPOTHESIS.md), [optional interview script](PRODUCT/USER_VALIDATION_SCRIPT.md), and [provider research](RESEARCH/EXECUTION_PROVIDER_RESEARCH.md) — hypotheses and protocols, not validated demand or provider selection.
- [Historical MVP decision brief](AI_COLLAB/MVP_DECISION_BRIEF.md) — dated hosted-provider comparison from 2026-10-20. It is not a provider selection; local execution must be compared before a remote provider is assumed.

## AI collaboration and workstreams

- Read [AGENTS.md](AGENTS.md) before changing files; [CLAUDE.md](CLAUDE.md) and [GEMINI.md](GEMINI.md) contain role-specific guidance.
- [Master research/implementation plan](AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md), [Gemini handoff](AI_COLLAB/GEMINI_HANDOFF.md), [initial independent provider review](AI_COLLAB/CHATGPT_INITIAL_PROVIDER_REVIEW.md), and [independent architecture review](AI_COLLAB/CHATGPT_REVIEW_OF_GEMINI_PLAN.md) provide earlier research context.
- [PR #2](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2) is the report-contract regression stream; [PR #3](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3) is the evidence/lifecycle research stream. Both were open, draft, and unmerged at the last metadata check. Do not mix their commits or assume their work is integrated.

### Supporting proposal: AI Workflow Director

The Director explores compact prompts, profiles, and continuation capsules to improve work across AI assistants. It is secondary to PocketCode's core run/inspect/report/iterate hypothesis and remains unimplemented. All AWD conformance fixtures remain NOT RUN.

- [Director master research](AI_COLLAB/MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md) and [first testable feature slice](AI_COLLAB/AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md).
- [Contract decision register](AI_COLLAB/AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) — D-01–D-08 are recommendations, not owner-approved decisions.
- [Conformance specification](AI_COLLAB/AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) and [canonical fixtures](AI_COLLAB/AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md) — 16 proposed cases, not implementation or passing tests.
- [Readiness audit](AI_COLLAB/AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md) and [bounded implementation plan](AI_COLLAB/AI_WORKFLOW_DIRECTOR_BOUNDED_IMPLEMENTATION_PLAN_20261028.md) — planning only; implementation requires explicit authorization.
- [Offline evaluation kit](AI_COLLAB/AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md), [manual run sheet](AI_COLLAB/AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md), and [reference output fixtures](AI_COLLAB/AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) — protocols and human-authored examples only; no benchmark runs are claimed.

## Prototype and test limitations

- [Mobile runner prototype source](prototypes/mobile-runner/index.html) and [preview instructions](prototypes/mobile-runner/README.md). The preview is static/simulated; it does not execute submitted code.
- [Prototype source checker](scripts/check_mobile_prototype.py) and [its tests](scripts/test_check_mobile_prototype.py) validate source patterns only. They do not prove browser interaction, execution isolation, provider security, or billing behavior.
- [PC-return checklist](AI_COLLAB/PC_RETURN_CHECKLIST_DRAFT_20261028.md) describes the proposed safe first-session checks. No tests are claimed to have run as part of this documentation pass.

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
