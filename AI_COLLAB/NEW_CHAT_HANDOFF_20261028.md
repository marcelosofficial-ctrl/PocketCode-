# PocketCode — Complete New-Chat Handoff (2026-10-28)

**Purpose:** Restart in a fresh chat without losing the product direction, four-month phone-only plan, three-AI operating model, repository boundaries, evidence status, or the exact next task. Read this before doing more work.

**Current handoff status:** Current GitHub state was checked on 2026-10-28. This document is a continuity artifact, not permission to implement, merge, deploy, spend money, run a provider, or alter either existing draft PR.

## 1. Read these first, in order

1. [PocketCode Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md) — concise navigation and source-of-truth map.
2. [Current Checkpoint](POCKETCODE_CURRENT_CHECKPOINT_20261028.md) — latest verified status and next bounded task; treat this as the operational queue.
3. [Four-Month Phone-Only Master Plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) — dated operating plan and ordered gates through 2027-02-28.
4. [Cross-Branch Execution-Contract Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) — exact-ref comparison of main, PR #2, and PR #3 contract concepts; its verdict mapping is advisory.
5. [Product Hypothesis Card](PRODUCT_HYPOTHESIS_CARD_20261028.md) — the product problem hypothesis, strongest alternatives, and falsification criteria.
6. [Fixed-Task Comparison Worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) — one synthetic CSV-to-JSON task and success/failure evidence sheet; design only, not executed.
7. [Phone-Only Competitor Scan Addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) — dated competitor claims, including local iOS Python/WASM.
8. [PC-Return Checklist Draft](PC_RETURN_CHECKLIST_DRAFT_20261028.md) — exact-ref verification, offline-first testing, evidence capture, and separate provider gate.

For the AI Workflow Director feature specifically, consult the [Director Master Research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md), [MVP Slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md), [Conformance Test Spec](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md), [Canonical Fixtures](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md), [Contract Decision Register](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md), [Readiness Audit](AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md), [Bounded Implementation Plan](AI_WORKFLOW_DIRECTOR_BOUNDED_IMPLEMENTATION_PLAN_20261028.md), [Evaluation Kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md), [Reference Fixtures](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md), and [Manual Run Sheet](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md).

## 2. Mission and product direction

PocketCode is a separate, public, phone-first project intended to help people code and work with AI from an iPhone or Android phone when PC access is unavailable. The provisional name has a real discoverability/name-conflict risk because an existing Android product is called “Pocket Code”; do not treat the current name as final or initiate a rename without research/owner decision.

The strongest product hypothesis is a small, trustworthy loop:

**Provide code and input → run in a suitably constrained environment → inspect truthful status, output and files → produce a useful evidence-rich report → use that report with any AI assistant to correct the task → rerun.**

The product is not yet proven to need a full mobile IDE, a general autonomous coding agent, a cloud runner, or a multi-agent platform. The candidate first task is small Python/CSV processing that writes a deterministic output file, but it remains an unvalidated hypothesis.

**Critical architecture correction:** Do not assume remote/hosted execution is the default. The 2026-10-28 desk scan found [Pyodios](https://pyodios.caffeinatedmath.com/), whose public pages claim local Python 3.14 via Pyodide/WebAssembly on iOS/iPadOS 26+ without a server. Other alternatives include local Android tools, browser-local WASM, remote-PC/SSH tools, hosted coding environments, and ordinary AI chat plus manual copy/paste. All claims are desk-research leads, not independent product/security benchmarks. The next comparison must test a narrow job and allow existing alternatives to win.

### Supporting feature: AI Workflow Director

The AI Workflow Director is a distinct, provider-neutral feature that helps users prepare compact task packets, carry verified state between chats, and continue work with any AI app—free or paid. It must optimize legitimate efficiency, not bypass quotas or access controls. It can help PocketCode and may later be useful as a phone counterpart to concepts from RevDev, but PocketCode and RevDev repositories/contracts must remain separate unless exact source evidence and an explicit decision establish a mapping.

Proposed Director features include Lite, Balanced, Careful, and Review-only profiles; deterministic packet building; continuation capsules; truthful evidence/provenance; preview/edit/copy; and optional user-initiated sharing later. The profiles and contracts are proposals, not frozen product behavior. Capsule statuses proposed so far: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `READY_TO_VERIFY`, `DONE_UNVERIFIED`, `DONE_VERIFIED`. A model claim is not proof; `DONE_VERIFIED` needs concrete evidence.

## 3. Four-month operating plan (2026-10-28 to 2027-02-28)

The objective is a decision-ready, security-aware, evidence-backed plan—not pretending to validate runtime behavior without the required environment.

- **Month 1 (2026-10-28–2026-11-27): Stabilize, orient, narrow.** Keep one continuity hub/checkpoint; reconcile the product hypothesis with real alternatives; finish the cross-branch contract map; maintain exact PR/source refs; define a narrow fixed task and disconfirming criteria.
- **Month 2 (2026-11-28–2026-12-27): Reconcile contracts, security gates, and test evidence.** Review lifecycle/report semantics, policy revision barriers, terminal events, idempotency, cleanup, artifacts, malformed inputs and evidence gaps. Improve test traceability/design only where useful. Do not call an offline fake test a live security proof.
- **Month 3 (2026-12-28–2027-01-27): Test mobile workflow and Director hypothesis.** Review the phone UX and simulated prototype honestly. If free AI usage allows, perform at most one carefully recorded paired Director evaluation, prioritizing EVAL-06, with no quota evasion. Do not claim efficiency gains without comparative evidence. Compare local app/browser WASM/manual/remote/hosted options against the fixed task only when a real hands-on session is explicitly chosen.
- **Month 4 (2027-01-28–2027-02-28): Consolidate and prepare PC-return gate.** Remove stale/conflicting navigation, freeze only approved decisions, assemble exact source revisions and offline test commands, record blockers/approvals required, and prepare a controlled first-PC-session runbook. Do not infer PC state while access is unavailable.

**Priority order:** (P0) continuity and branch safety; (P0) problem/market/MVP focus; (P0) report/lifecycle/security contracts; (P1) phone UX; (P1) Director as a supporting feature; (P0 by Month 4) PC-return readiness; (P2) future features. Success is lower uncertainty and safer next steps, not commit/document count.

## 4. Three-AI collaboration model

- **Claude — lead implementer** when code work is authorized and actual repository/runtime access is available.
- **Gemini — independent architecture/specification/security reviewer**, adversarial reviewer, test planner, and targeted co-developer where helpful.
- **ChatGPT — continuity holder, evidence reconciler, research/requirements and architecture comparison, acceptance/test architect, and integration coordinator.**

These roles are flexible defaults. Do not force all three AIs onto every task. Give one AI a bounded primary task; ask another a narrow review question; use the third only for distinct research/reconciliation. Consolidate evidence before acting. Do not assume any AI has access to the user's PC, installed binary, private files, runtime, queues, or uncommitted state.

## 5. Repository and branch state — verified 2026-10-28

Repository: `marcelosofficial-ctrl/PocketCode-` (keep the trailing hyphen).

- Current research branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Before creating the handoff and navigation updates, branch head was `e37d5cbb08df47303a3643f241ff1dd9d3e79812` (129 ahead, 0 behind). After adding the handoff and updating the hub/checkpoint/README, the latest completed comparison showed head `3b931874ae923df30fd6102d3a8d983899c989d9`, **133 commits ahead, 0 behind**. This handoff/checkpoint refresh itself advances the branch again; treat both SHA/counts as audit snapshots, not live state, and recheck before consequential work.
- [PR #2](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2), branch `chat-continuity-report-regressions-2026-10-26): open, draft, unmerged; head `eb8b7ea83cb0e8fe1880351276c485b761431791`. The PR records 25 Python tests passing in a temporary reconstructed tree from exact branch blobs on 2026-10-26 and a prototype static checker. This is limited offline evidence, not a runtime/security/provider test.
- [PR #3](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3), branch `pocketcode-pass0-audit-2026-10-26`: open, draft, unmerged; head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`. Research/lifecycle contract/test source exists; its current checked-in helper/test pair and full suite were reported NOT RUN. No provider/live execution was tested.
- Both PRs must remain untouched unless the owner explicitly authorizes a specific change. No merge, deployment, GitHub Actions run, or release is authorized.

The current branch includes docs-only Director research and phone-only planning. It does not mean the new docs are integrated into main.

## 6. Recent work completed on the research branch

1. Created a four-month phone-only master plan, continuity hub, checkpoint, and PC-return checklist.
2. Audited exact source blobs across main, PR #2, and PR #3; all 11 source blob SHAs recorded in the cross-branch audit matched their exact refs at that audit. The audit identified a gap between detailed execution outcome/cleanup/disposition and a user-facing PASS/FAIL/INCOMPLETE verdict.
3. Added an **advisory-only** projection table. PASS must not hide unknown cleanup; rejected/cancelled/timed-out/limit/provider-error/incomplete states should not be presented as a completed successful run. Do not freeze the schema or treat this proposal as owner-approved.
4. Created the product hypothesis card and dated competitor scan addendum; refreshed existing `RESEARCH/COMPETITOR_MATRIX.md` and `RESEARCH/COMPETITIVE_ANALYSIS.md` on this branch.
5. Added the fixed-task worksheet. Synthetic input is a CSV with notebook (2 × 3.50) and pen (3 × 1.25); expected `summary.json` has grand total `10.75`, line count 2, item totals notebook `7.00` and pen `3.75`. A deliberate failure case removes the required `unit_price` header and should produce a clear error without a misleading valid output. The task, scoring and evidence form are design-only.
6. The AI Workflow Director research set contains AWD-01–AWD-16 conformance cases, canonical fixtures, eight proposed defaults D-01–D-08, readiness audit, evaluation kit EVAL-01–08, reference fixtures, and a manual run sheet. These are design artifacts, not a product implementation or proof of AI savings.
7. The competitor scan surfaced Pyodios as a serious iOS local-execution comparator, plus AndroidHarness, PhoneCode, Atlan and Pairlet. All current capability/limitation claims are source-led; no hands-on tests or market validation were performed.

## 7. Current evidence status — do not overstate

- Real PocketCode execution backend: **NOT IMPLEMENTED / NOT VERIFIED**.
- Static prototype's run result: **SIMULATED**, not actual code execution.
- Director implementation: **NOT IMPLEMENTED**.
- AWD-01–AWD-16 tests: **NOT RUN**.
- Director AI comparison / token or time savings: **NOT RUN**.
- Fixed-task app/browser/remote/hosted comparison: **NOT RUN**.
- User interviews/market validation: **NOT RUN**.
- Provider approved under strict $0 budget: **NONE**.
- Live user-code workload, cloud isolation, network egress restrictions, termination, cleanup, artifact quarantine, billing safety: **NOT VERIFIED**.
- No code implementation, paid API calls, provider workload, account/billing setup, merge, deployment, release, or Actions run occurred in this work.

Use evidence labels precisely: `VERIFIED_PRIMARY_SOURCE`, `SECONDARY_SOURCE`, `INFERENCE`, `ASSUMPTION`, `UNVERIFIED`, `NEEDS_LIVE_TEST`, `NEEDS_OWNER_APPROVAL`. For execution tests, use PASS/FAIL/BLOCKED/INCONCLUSIVE/NOT RUN only when supported by evidence.

## 8. Non-negotiable operating constraints

- User is phone-only for approximately four months and does not have PC/local runtime access. Treat PC source/runtime/installed binary/queue state as unknown unless newly evidenced.
- Budget $0. No paid provider/API, billing activation, paid cloud, credentials, live user-code workload or account creation without explicit owner approval and verified conditions.
- No GitHub Actions, deployments, merge, release, or edits to PR #2/#3 without explicit approval.
- Do not treat a research plan as implementation authorization.
- No system-wide overlay, background clipboard polling, private-chat scraping, silent control of other AI apps, quota evasion, unrestricted shell or unrestricted outbound networking.
- Use local-first options when they meet the actual task. Browser/WASM is not automatically a hard sandbox; embedding APIs, file permissions, resource limits, and host policy matter.
- Keep PocketCode and RevDev distinct. Do not copy contracts or claim compatibility from memory; fetch exact source revisions first.
- Prefer updating existing authoritative docs rather than creating more master documents.
- If user input is needed, ask one precise, short question at the end. Otherwise continue independently and report the next highest-value pass.

## 9. Exact next pass for the new chat

1. Re-fetch the current research branch head, main SHA and PR #2/#3 metadata. Counts and SHAs in this handoff are snapshots; re-check before consequential actions.
2. Continue the exact-ref contract review: PR #3's draft specifies NET-BARRIER-01 / NET-SEM-01 policy-revision checks, but the reviewed pure helper only receives a boolean policy confirmation. Trace that requirement to a concrete coordinator/adapter seam and test design; do not claim a runtime defect or passing control from source review alone.
3. Clarify EXIT_NONZERO combined with unknown/failed cleanup or authorization. Keep process outcome, job disposition and artifact-release eligibility separate. Artifact release remains fail-closed; do not change PR #2/#3.
4. Keep the fixed-task worksheet as a protocol, not completed evidence. Hands-on comparisons remain NOT RUN until a concrete attempt is selected and recorded.
5. Follow the ordered work packages in the four-month plan. Update the existing checkpoint after material progress; do not create another master plan or repeat completed link audits.
6. By the end of Month 1, make the product hypothesis and strongest alternatives decision-ready without selecting a provider/name/architecture prematurely.

Owner action is needed only when a future step genuinely requires a phone observation, another AI's independent review, or explicit cost/safety approval.

## 10. Future features to keep visible, not add automatically

Highest-value candidates if the core task proves demand: truthful execution receipt; copyable AI diagnostic report; safe explicit input/output file flow; one tested task recipe; portable verified continuation capsule; local deterministic tools (JSON/CSV/text validation); provider-neutral adapters; opt-in remote-PC bridge when a host exists; local redaction with honest limitations; interruption recovery/accessibility/low-bandwidth behavior; reusable user recipes; interoperable execution receipt only after contract reconciliation.

Defer until evidence and safety justify them: full IDE replacement, broad autonomous multi-agent orchestration, native apps before a PWA blocker is measured, accounts/sync/team sharing/marketplace, direct model APIs and subscription systems, arbitrary shell/network access, long-running services, GPU/large builds, unattended agents.

**Core rule:** PocketCode must earn each layer of complexity by solving a real user problem better than the strongest existing workaround. Keep the MVP narrow, local-first where practical, truthful about evidence, and safe by design.
