# PocketCode Continuity Hub — Read First

**Purpose:** Fast orientation for the owner, ChatGPT, Claude, and Gemini. This is a navigation and operating guide; it does not override accepted decisions, product/security requirements, or exact branch evidence.

## Start here — the 3-document route

1. **[Current Checkpoint](POCKETCODE_CURRENT_CHECKPOINT_20261028.md)** — latest verified state, completed passes, blockers, and next bounded task. Read this every session.
2. **[Four-Month Phone-Only Master Plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md)** — priorities and month-by-month gates through 2027-02-28. This is the schedule.
3. **[New-Chat Handoff](NEW_CHAT_HANDOFF_20261028.md)** — fuller restart context when a chat has ended or working context is missing.

Then open only the source/workstream docs relevant to the task. Do not paste or reread every project file by default.

## 1. Project in 60 seconds

**Core product hypothesis:** PocketCode helps a phone-first user take a small code task from AI or their own editor, execute it through an appropriate and understood boundary, inspect the actual result/files/errors, and carry trustworthy evidence back to any AI assistant to fix and rerun.

**Core loop:** provide code + explicit input → run in a fit-for-purpose environment → inspect truthful outcome and files → copy a bounded evidence-rich report → correct with any AI assistant → rerun.

**Execution location is undecided.** Local phone apps, browser-local WASM, a user-controlled remote PC, hosted execution, and ordinary manual copy/paste are alternatives—not a predetermined architecture. The fixed-task worksheet is the comparison protocol; results remain NOT RUN.

**AI Workflow Director is a supporting hypothesis.** Compact task packets, profiles, continuation capsules, and manual handoff may improve continuity across free or paid AI apps. They must support the core workflow rather than displace it with a generic multi-agent cockpit. Director recommendations D-01–D-08 and AWD-01–AWD-16 remain proposals/tests NOT RUN.

## 2. Current truth and non-negotiable guardrails

- Phase: **discovery and product definition**. The published mobile prototype is static and its displayed result is **SIMULATED**. No production execution backend or provider is established.
- Budget: **$0** unless the owner explicitly changes it. No paid trials, payment methods, billing enablement, account/credential setup, or potentially billable workload without explicit approval.
- No merge, deployment, GitHub Actions run, release, destructive repository action, or PR #2/#3 change without explicit authorization.
- The project is public: never add secrets, credentials, private user data, or production configuration.
- No PC/local access is expected from 2026-10-28 through approximately 2027-02-28. Treat local source, installed binaries, runtime and device state as UNKNOWN until actual evidence becomes available.
- No system-wide overlay, background clipboard polling, private-chat scraping, silent cross-app control, quota evasion, unrestricted shell, or unrestricted user-code networking.
- Never infer security from a container/WASM label. Real guarantees depend on exposed APIs, enforcement, termination, cleanup, authorization, artifact handling and evidence.
- Keep PocketCode and RevDev separate. Compare actual source/contracts before compatibility claims; do not merge repositories or map fields from memory.
- Research plans do not authorize implementation/provider use. Keep proposals labelled until accepted.

## 3. Source-of-truth order

When sources conflict, inspect the exact file, branch, date and status. Do not silently choose a convenient version.

1. Exact repository source and commit determine what is present.
2. AGENTS.md governs collaboration/change discipline.
3. DECISIONS.md contains accepted decisions only; proposal sections are not approvals.
4. PRODUCT_SPEC.md, PROJECT_STATUS.md, ROADMAP.md, ARCHITECTURE.md, SECURITY.md, and PRODUCT/EXECUTION_CONTRACT.md govern product intent and trust requirements.
5. Exact branch-local contracts, tests, decision records and PR metadata define their own workstream only.
6. This hub is navigation; the four-month plan is the schedule; the current checkpoint is the operational queue.
7. Chat memory and commit/document counts are not evidence.

## 4. Repository / branch map

Repository: [marcelosofficial-ctrl/PocketCode-](https://github.com/marcelosofficial-ctrl/PocketCode-) — preserve the trailing hyphen.

| Workstream | Current reference | Rules |
|---|---|---|
| Main baseline | [main](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/main) | Re-fetch exact current SHA before consequential work. |
| PR #2 — report formatter/regressions | [PR #2](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2), branch chat-continuity-report-regressions-2026-10-26, last checked head eb8b7ea83cb0e8fe1880351276c485b761431791 | Open/draft/unmerged at last check. Its described 25-test pass is limited to a reconstructed Python helper/static-check tree, not real execution or runtime security. Do not edit without explicit approval. |
| PR #3 — lifecycle/security research | [PR #3](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3), branch pocketcode-pass0-audit-2026-10-26, last checked head 0ddcc0bc97bac5d446aefedf3d71f99411bd841d | Open/draft/unmerged at last check. Exact checked-in helper/tests were reported NOT RUN. No provider/live run was tested. Do not edit without explicit approval. |
| Director / phone-only research | [research branch](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/pocketcode-ai-workflow-director-research-2026-10-28) | Docs/research only; not main. Last observed head before this reorganization was 34a5c4cbb37357a577a64ce0617597001455e7ff. Refresh head/ahead counts every session. |
| Static prototype | [source](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/main/prototypes/mobile-runner) · [preview](https://marcelosofficial-ctrl.github.io/PocketCode-/) | UI study only; sample result is simulated. Do not trigger Pages just to verify docs. |

**Do not conflate decision scopes:** PR #3's delegated lifecycle decisions do not approve the separate Director's D-01–D-08 contract recommendations. Neither draft PR is merged into main.

## 5. Canonical document map — use the smallest relevant set

### Product authority
- [Product specification](../PRODUCT_SPEC.md) — target-user hypothesis, core loop, MVP candidate and open decisions.
- [Project status](../PROJECT_STATUS.md) — current high-level phase and immediate priorities.
- [Roadmap](../ROADMAP.md) — evidence-based stage/exit gates.
- [Architecture](../ARCHITECTURE.md) and [security requirements](../SECURITY.md) — trust boundaries and execution preconditions.
- [Decision log](../DECISIONS.md) — accepted decisions vs unresolved proposals.
- [Execution-loop acceptance](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) and [execution contract](../PRODUCT/EXECUTION_CONTRACT.md) — what a real end-to-end proof/report must establish.

### Active phone-only work
- [Four-month master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) — month gates, sequence, future feature stages.
- [Current checkpoint](POCKETCODE_CURRENT_CHECKPOINT_20261028.md) — latest results and next pass.
- [Product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) — candidate user/job, counter-hypotheses and falsification criteria.
- [Fixed-task comparison worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) — canonical synthetic CSV success/failure task; comparison NOT RUN.
- [Phone-only competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) — dated public-source delta.
- [PC-return checklist](PC_RETURN_CHECKLIST_DRAFT_20261028.md) — exact-ref tests and a separate approval-gated provider path.

### Contract and lifecycle review
- [Cross-branch execution-contract audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) — main vs PR #2 vs PR #3 semantics and integration gaps; static review only.
- [PR #3 lifecycle contract](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md) and [offline acceptance matrix](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md) — proposed provider-neutral baseline and synthetic checks; not live evidence.
- [Zero-budget work plan](../PRODUCT/ZERO_BUDGET_WORK_PLAN.md) and [controlled Python runbook](../PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md) — cost and future proof gates.

### AI Workflow Director — supporting feature, design-only
- [Director master research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md) — full rationale/research.
- [MVP slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) — proposed bounded behavior.
- [Decision register](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) — D-01–D-08 recommendations, not approved.
- [Conformance test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) and [canonical fixtures](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md) — AWD-01–AWD-16 design fixtures; NOT RUN.
- [Readiness audit](AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md) and [bounded implementation plan](AI_WORKFLOW_DIRECTOR_BOUNDED_IMPLEMENTATION_PLAN_20261028.md) — proposed, not an implementation authorization.
- [Evaluation kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md), [manual run sheet](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md), and [reference fixtures](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) — evaluation protocol/examples only; no comparative run claimed.

### Older research / contextual material
- [Mobile-coding user evidence](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) — qualitative public-source evidence, not representative research.
- [Competitor matrix](../RESEARCH/COMPETITOR_MATRIX.md) and [competitive analysis](../RESEARCH/COMPETITIVE_ANALYSIS.md) — baseline comparison; read the addendum for new deltas.
- [RevDev shared-core proposal](../PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md) — exploratory only; never assume shared implementation.
- [Historical provider decision brief](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/AI_COLLAB/MVP_DECISION_BRIEF.md) — dated hosted-provider shortlist, not a provider selection; local execution must be compared before a remote provider is assumed.

## 6. Three-AI collaboration model

- **Claude — primary implementer** when implementation is authorized and correct repository/runtime access is available.
- **Gemini — independent architecture/spec/security reviewer**, adversarial reviewer, and test planner; may co-develop a bounded piece when useful.
- **ChatGPT — continuity holder, research/requirements lead, evidence reconciler, product/architecture comparison, and acceptance/test architect.**

Use all three only when their roles add independent value. Assign one primary owner per task; ask reviewers one specific question; reconcile evidence before changes. No AI should assume access to the user's PC, private files, installed binary, live provider or uncommitted state.

## 7. Standard operating procedure for every substantial pass

1. **Orient:** re-fetch relevant exact files, research branch head, main SHA and PR #2/#3 status when consequential.
2. **Choose one decision:** state which uncertainty the pass reduces and why it matters.
3. **Reuse first:** inspect existing source, docs, test traces and approved open-source dependencies before adding utilities or another document.
4. **Batch one coherent deliverable:** pair a finding with its source reference, acceptance criteria, and the smallest useful update.
5. **Review adversarially:** look for contrary evidence, false-positive success, skipped gates, mobile friction, stale links and scope creep.
6. **Verify honestly:** report exact revision/command/environment/results for executed checks. Otherwise mark NOT RUN; source reading is not a test.
7. **Keep continuity tidy:** update this hub only for navigation changes; update the checkpoint for current state; update accepted decisions only when a decision is truly accepted; update the four-month plan only when schedule/strategy materially changes.
8. **Close the loop:** report what changed, what it proves/doesn't prove, the next bounded task, and any necessary owner action.

Evidence labels: VERIFIED_PRIMARY_SOURCE, SECONDARY_SOURCE, INFERENCE, ASSUMPTION, UNVERIFIED, NEEDS_LIVE_TEST, NEEDS_OWNER_APPROVAL. Execution/test status labels: PASS, FAIL, BLOCKED, INCONCLUSIVE, NOT RUN.

## 8. Default priority order until evidence changes it

1. **P0 — direction and continuity:** keep one current queue and one project map; remove stale contradictions.
2. **P0 — first job / alternatives:** prove or falsify the small run-inspect-report-iterate job against the strongest existing workaround.
3. **P0 — truthful contract and trust:** align execution outcome, job disposition, cleanup, policy revision, artifact release and report behavior.
4. **P1 — phone UX and evidence capture:** improve the prototype only where a defined task shows confusion; keep demo output labelled.
5. **P1 — Director:** validate compact continuation/handoff with a tiny, honest comparison if free usage permits.
6. **P0 by late February — PC-return readiness:** exact refs, offline tests, artifacts, decision gates and next command sequence.
7. **P2 — future capabilities:** maintain a staged backlog; do not implement speculative features.

**Core rule:** PocketCode earns each layer of complexity by solving a real user problem better than the strongest workaround. More branches, documents, features or commits are not the goal.
