# PocketCode Continuity Hub — Read First

**Last structured review:** 2026-10-28  
**Purpose:** One reliable orientation point for future ChatGPT, Claude, Gemini, and human sessions. This is a navigation/continuity document, not a replacement for product requirements, accepted decisions, security rules, or branch-local evidence.

## 1. The project in 60 seconds

PocketCode's core product hypothesis is a **phone-first, provider-neutral workflow for turning AI-generated code into real, inspectable execution evidence, then using that evidence to fix and rerun the task**. The product should be much easier to use on a small screen than a general desktop IDE and must be honest about what did or did not happen.

The AI Workflow Director is a **supporting feature hypothesis**: compact task prompts, profiles, continuity capsules, and explicit handoff across AI assistants. It should improve the core workflow, not quietly replace the project's primary purpose with a generic multi-agent coding cockpit.

The project is in discovery/product definition. The published prototype is static/simulated; no production execution runtime is established. No provider, stack, billing plan, or final public name is approved. Budget remains $0 unless the owner explicitly changes it.

## 2. Non-negotiable constraints

- Owner is phone-first and expects no PC/local access for roughly four months from late October 2026.
- Keep spend at $0. No paid API, paid trial, billing enablement, account/credential setup, live provider workload, or potentially billable action without explicit approval.
- No merge, deployment, GitHub Actions run, production implementation, release, destructive git operation, or change to PR #2/#3 without explicit authorization.
- Never run submitted code on an app server or developer workstation as a shortcut. Do not claim security from a configuration label alone.
- No background clipboard polling, private-chat scraping, system-wide overlay, silent cross-app control, quota evasion, or unrestricted user-code network access.
- The public repo contains no secrets or private user data.
- Keep PocketCode separate from RevDev. Future shared concepts require verified contract crosswalks; do not merge repositories or infer field mappings from remembered details.
- Treat simulated results as simulated in both UI and copied text. Distinguish an executed program result from infrastructure, lifecycle, cleanup, or evidence uncertainty.

## 3. Authority order — what future chats must trust

1. **Actual source and exact branch/commit** determine what code is present. A PR branch is not main; a planned change is not integrated.
2. **[AGENTS.md](../AGENTS.md)** controls collaboration and change discipline.
3. **[DECISIONS.md](../DECISIONS.md)** records accepted product decisions; proposal sections do not count as acceptance.
4. **[PRODUCT_SPEC.md](../PRODUCT_SPEC.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [SECURITY.md](../SECURITY.md), and [execution contract](../PRODUCT/EXECUTION_CONTRACT.md)** govern product intent, trust boundaries, and the proposed execution lifecycle.
5. **[PROJECT_STATUS.md](../PROJECT_STATUS.md) and [ROADMAP.md](../ROADMAP.md)** give the high-level phase and long-term stages.
6. The current workstream's source, tests, acceptance matrix, decision register, and checkpoint establish the status of that workstream only.
7. This hub and the [four-month phone-only plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) coordinate work; they do not override the documents above.
8. Chat history and AI recollection are secondary context, never proof of repository state or test results.

If documents disagree, identify the exact files, branches, dates, and claims; record the conflict instead of silently picking the more convenient wording.

## 4. Repository and branch map (last verified 2026-10-28)

| Work area | Location | What it is / caution |
|---|---|---|
| Main baseline | [main](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/main) | Integrated baseline at the time it is checked. Re-read its current SHA before work. |
| PR #2 — report contract regression work | [PR #2](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2), branch `chat-continuity-report-regressions-2026-10-26`, head `eb8b7ea83cb0e8fe1880351276c485b761431791` | Draft/open/unmerged when checked. PR description records 25 Python tests passing in a temporary reconstruction from exact branch blobs on 2026-10-26; that is not a live runtime/security test. **Do not change this PR as part of the phone-only plan.** |
| PR #3 — evidence-led research and lifecycle contract | [PR #3](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3), branch `pocketcode-pass0-audit-2026-10-26`, head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d` | Draft/open/unmerged when checked. Has research, a lifecycle helper, contract-to-code/test traceability, and synthetic test source. Its exact checked-in helper/test pair and full suite were reported **NOT RUN** in the PR body. No provider or live execution was tested. **Read it for planning; do not edit or merge it without approval.** |
| AI Workflow Director research | [research branch](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/pocketcode-ai-workflow-director-research-2026-10-28) | Isolated documentation/feature-research branch. It was 85 commits ahead of main and 0 behind at the last comparison before this hub/plan work. It is not main and must not be described as integrated. |
| Static prototype | [repository source](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/main/prototypes/mobile-runner) · [published preview](https://marcelosofficial-ctrl.github.io/PocketCode-/) | Execution display is simulated. Never use the preview as evidence that real code ran. Do not trigger its Pages/deployment workflow just to verify documentation. |

**Branch-specific decision warning:** PR #3's 2026-10-27 owner-delegated execution-lifecycle selections apply to that workstream's provider-neutral lifecycle baseline and offline design. They are not the same as AI Workflow Director contract defaults D-01–D-08, which remain proposals in the Director branch. Do not merge those decision sets or widen either approval by implication.

## 5. Canonical document map

### Product and execution
- [Product specification](../PRODUCT_SPEC.md) — problem, audience hypothesis, core loop, MVP candidate, exclusions, product acceptance.
- [Project status](../PROJECT_STATUS.md) — high-level state and immediate work.
- [Roadmap](../ROADMAP.md) — evidence-based phases and exit gates; not calendar promises.
- [Architecture](../ARCHITECTURE.md) — conceptual system and trust boundaries; no stack is selected.
- [Security requirements](../SECURITY.md) — mandatory preconditions before public execution.
- [Execution loop acceptance](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) — end-to-end definition of a useful real proof.
- [Provider-neutral execution contract](../PRODUCT/EXECUTION_CONTRACT.md) — proposed request/result/report lifecycle; not an implemented API.
- [Controlled Python proof runbook](../PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md) — prepared, not executed; live runs require separate authorization and a proven zero-cost path.
- [Zero-budget work plan](../PRODUCT/ZERO_BUDGET_WORK_PLAN.md) — spend and provider gates.
- [Mobile technical task map](../PRODUCT/MOBILE_TECHNICAL_TASKS.md) — broader phone-only jobs and future PC/phone convergence.

### Evidence-led research and report lifecycle (PR #3 branch)
- [Complete continuation handoff](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/CHAT_HANDOFF_20261027.md)
- [Master workflow efficiency rules](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/MASTER_WORKFLOW_EFFICIENCY_RULES_20261027.md)
- [Research checkpoint](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/RESEARCH_CHECKPOINT.md)
- [Contract → code → test traceability](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/CONTRACT_CODE_TEST_TRACEABILITY_20261027.md)
- [Offline acceptance matrix](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md)
- [Owner decision packet](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_OWNER_DECISION_PACKET_20261027.md) — selections are scoped to that lifecycle baseline only.

### AI Workflow Director (this research branch; still proposed)
- [Master Director research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md)
- [First testable feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md)
- [Canonical fixture catalogue, AWD-01–AWD-16](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md)
- [Conformance test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md)
- [Contract decision register D-01–D-08](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) — advisory only.
- [Pre-implementation readiness audit](AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md)
- [Bounded implementation plan](AI_WORKFLOW_DIRECTOR_BOUNDED_IMPLEMENTATION_PLAN_20261028.md)
- [Current Director branch checkpoint](POCKETCODE_CURRENT_CHECKPOINT_20261028.md)

## 6. Current evidence boundary

**Established from repository/PR records at the last check:**
- A static phone UI prototype and Python report/source-check utilities exist.
- PR #2 describes a passing 25-test run from a temporary reconstructed tree of exact branch blobs on 2026-10-26; scope was helper and static-check behavior only.
- PR #3 contains 24 synthetic lifecycle test methods in its test source, but the exact current checked-in pair/full suite was explicitly reported NOT RUN.
- The AI Workflow Director contains research and proposed fixture documents, not an implementation; AWD-01–AWD-16 remain NOT RUN.
- PR #2 and #3 were open, draft, and unmerged at the last metadata check; their head SHAs matched the values above.
- No production provider, live user-code execution, live security proof, representative user study, or comparative AI benchmark is established by these records.

These statements must be rechecked before a consequential decision. Do not count the number of commits or documents as product progress.

## 7. Three-AI working model

- **Claude — primary implementation lead** when code work is authorized and repository/runtime access is actually available. Give one coherent, bounded implementation task.
- **ChatGPT — research, requirements, architecture comparisons, continuity, cross-branch reconciliation, and evidence-based acceptance review.**
- **Gemini — independent architecture/specification review, adversarial review, test planning, and focused co-development when helpful.**

The roles are defaults, not a demand to use all three for every task. Assign one primary owner, give reviewers specific questions, and consolidate before integration. For PocketCode, do not automatically copy RevDev role assumptions or mix the two repositories.

## 8. Standard working method for every substantial pass

1. Verify the active branch, exact relevant files, latest PR heads, and current objective. Do not trust old counts without rechecking.
2. Name the decision/uncertainty that matters and define the smallest useful deliverable.
3. Search existing source/docs/dependencies before creating a new artifact or utility.
4. Do one coherent pass across related work, not many tiny changes. Keep unrelated or risky branches isolated.
5. Separate **VERIFIED_PRIMARY_SOURCE**, **SECONDARY_SOURCE**, **INFERENCE**, **ASSUMPTION**, **UNVERIFIED**, **NEEDS_LIVE_TEST**, and **NEEDS_OWNER_APPROVAL**. Mark execution/test status as PASS/FAIL/BLOCKED/INCONCLUSIVE/NOT RUN only when justified.
6. For any tests, report exact revision, command, environment, result counts, and what the tests do not prove. If not executed, say NOT RUN.
7. Keep research reproducible: date sources, distinguish primary docs from self-reported posts, and include counter-evidence.
8. Update the existing checkpoint/decision record when state changes; do not create parallel masters.
9. End with completed work, evidence, limitations, next highest-value pass, and the smallest owner action only if genuinely blocked.

## 9. Next work sequence

Use [the four-month phone-only master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) as the active plan. The immediate next work should reconcile the cross-branch execution-contract/report semantics and refresh the competitor/user-problem evidence against current alternatives. Do not start code implementation, provider tests, or PR changes merely because a written plan exists.
