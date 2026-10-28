# PocketCode — Four-Month Phone-Only Master Plan

**Planning window:** 2026-10-28 to 2027-02-28, approximately four months without reliable PC/local access.  
**Status:** Owner-requested operating plan; it authorizes research and continuity planning, not implementation, provider spend, merging, or deployment.  
**Continuity entry point:** [PocketCode Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md).  
**Project authority:** Existing product, architecture, security, decision, and branch-specific evidence documents remain authoritative.

## 1. Mission for these four months

Use the phone-only period to arrive at a **decision-ready, security-aware, evidence-backed plan**—not to pretend a real runner or production architecture can be validated without its required environment.

By the end of this period, the project should have:

1. One clearly stated primary user/problem hypothesis, with evidence for and against it and explicit continue/narrow/pivot criteria.
2. One narrow first-workflow candidate, with observable acceptance criteria and a realistic comparison to the user's current workaround.
3. A reconciled map of the product report/lifecycle contracts, test coverage, unresolved security gates, and the exact status of PR #2 and PR #3.
4. A tidy, linked documentation structure that a new AI can navigate in minutes, not a sprawling collection of competing “master” documents.
5. A tested or honestly untested phone UX review plan and a small, evidence-conscious AI Workflow Director evaluation.
6. A PC-return checklist that tells the next session exactly which revisions to fetch, which tests to run, what results to save, and which actions remain prohibited.
7. A future-feature shortlist ordered by user value, differentiation, safety, and zero-cost feasibility.

**Success is reduced uncertainty and faster, safer next steps. It is not a document count, commit count, claimed test pass, provider selection, or production launch.**

## 2. Strategic direction: protect the actual differentiator

### Core product hypothesis

PocketCode should first prove a small, phone-friendly loop:

**Provide code and input → run it in a suitably isolated environment → inspect truthful status/output/files → copy an evidence-rich report → use the report to correct the task with any AI assistant → rerun.**

The first useful product is not necessarily a full mobile IDE, general-purpose coding agent, remote-control cockpit, or multi-agent platform. The hypothesis to validate is that a focused “run, inspect, report, iterate” workflow is easier and more trustworthy for a particular mobile task than existing free or familiar alternatives.

### Supporting feature: AI Workflow Director

The Director can reduce repeated context, prepare compact task packets, preserve verified state in continuation capsules, and help users move between AI apps. Keep it provider-neutral and usable with manual copy/paste. It should support the core product, not displace proof of real execution.

The Director's **AWD-01–AWD-16** are proposed conformance cases and remain **NOT RUN**. Its **D-01–D-08** defaults are recommendations, not owner-approved product contracts. The separate lifecycle choices recorded in PR #3 are not Director decisions.

### Competitive caution discovered during this review

A quick public scan on 2026-10-28 surfaced active projects in adjacent categories: [AndroidHarness](https://github.com/Sanuu7/AndroidHarness) describes an Android-native coding agent that works without a PC; [PhoneCode](https://github.com/dttdrv/phonecode) describes a local Android coding environment; [Pairlet](https://github.com/heypandax/pairlet) focuses on steering coding agents running on another machine; and [Atlan](https://github.com/Atlansdaddy/atlan) describes an on-phone development cockpit based on Termux. These are maintainer-described capabilities, not hands-on comparative results.

**Implication:** “AI coding from a phone” alone is unlikely to be a sufficiently sharp differentiator. Revalidate the landscape before making product claims. Compare alternatives on the actual job, where code runs, whether a PC is required, iOS/Android support, execution evidence, file flow, privacy, setup burden, price, and portability—not feature counts or popularity alone.

## 3. Operating constraints for the whole period

- Budget remains $0. Promotional credits and “free” trials are not a hard spend cap.
- No paid provider/API, account/credential creation, live user-code workload, billing activation, or paid cloud environment without explicit owner approval and verification of the exact cost/safety conditions.
- No GitHub Actions, deployment, merge, release, or edit to PR #2/#3 as part of this plan.
- Documentation, public research, contract review, source review, offline test design, and clearly labelled simulated UX are allowed work products.
- If an offline Python test can be executed in an available isolated assistant environment, fetch the exact branch files, verify their Git blob identities, record the precise command/environment/output, and state limitations. This is not proof of mobile behavior, cloud isolation, cleanup, billing safety, or production security.
- Do not require the owner to access a PC or run commands during this period. Ask for input only when genuinely blocking, with one precise request.
- No system-wide overlays, background clipboard polling, private-chat scraping, silent app control, quota evasion, or unrestricted shell/network access.
- Keep repositories separate. Cross-project concepts may be mapped through exact contracts but not merged or inferred from memory.

## 4. Workstreams and their priority

| ID | Workstream | Priority | What good progress looks like during phone-only work |
|---|---|---|---|
| WS-0 | Continuity and repository control | P0 | A new AI can identify authoritative docs, branches, test truth, and next task quickly; no duplicated masters |
| WS-1 | User problem, market, and MVP focus | P0 | A sourced, skeptical comparison of alternatives and a narrow workflow hypothesis with disconfirming evidence |
| WS-2 | Execution report/lifecycle and safety | P0 | Cross-branch semantic conflicts and test gaps are recorded; security gates remain explicit and unclaimed |
| WS-3 | Mobile UX and static prototype | P1 | The phone flow and simulated states are assessed against observable tasks; no deployment required |
| WS-4 | AI Workflow Director | P1, supporting | Contract proposals stay bounded; at most one carefully recorded paired evaluation when free usage permits |
| WS-5 | PC-return technical readiness | P0 by Month 4 | Exact source/test revisions, commands, gates, and owner approvals are listed for a controlled restart |
| WS-6 | Future product opportunities | P2 | Options are ranked and gated, not silently added to MVP scope |

Do not work on all streams in every pass. Prefer one high-value workstream per pass and combine adjacent documents only when doing so removes a real contradiction or repeated effort.

## 5. Four-month schedule

### Month 1 — Stabilize, orient, narrow (2026-10-28 to 2026-11-27)

**Primary objective:** establish one reliable map of the project and narrow the problem without pretending the current hypotheses are validated.

Work to complete:
1. Use this [Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md) as the orientation index. Verify branch and PR metadata before consequential work; treat PR #2, PR #3, and the Director branch as separate streams.
2. Cross-read the current main product spec/status/roadmap and the PR #3 research handoff. Note genuine contradictions only; do not copy whole files into a new master.
3. Refresh the existing [competitor matrix](../RESEARCH/COMPETITOR_MATRIX.md) and [competitive analysis](../RESEARCH/COMPETITIVE_ANALYSIS.md) against today's phone coding options and local/remote/cloud execution alternatives. Use the new projects above as leads, not as a complete benchmark.
4. Reuse [mobile-coding user evidence](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) and the PR #3 [user/problem evidence protocol](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_USER_PROBLEM_EVIDENCE.md). Do not repeat the same search unless the evidence is outdated or the decision changed.
5. Prepare a compact “problem hypothesis card”: target user, last-mile situation, current workaround, proposed advantage, strongest counter-hypothesis, evidence quality, and the result that would change the recommendation.
6. Revisit naming collision risk before public brand/domain investments; do not rename the repository as a side effect.

**Exit gate:** a small set of candidate workflows is ranked against actual alternatives, with one recommended first workflow and explicit uncertainty. It is still a hypothesis; no market validation claim without representative evidence.

### Month 2 — Reconcile contracts, security gates, and test evidence (2026-11-28 to 2026-12-27)

**Primary objective:** make sure the contract being discussed is the same contract the helper/tests are meant to express.

Work to complete:
1. Compare the main branch's [proposed execution contract](../PRODUCT/EXECUTION_CONTRACT.md) and [security requirements](../SECURITY.md) with PR #3's draft execution contract, selected lifecycle baseline, acceptance matrix, helper, and test traceability.
2. Preserve the distinction between execution observation, derived job disposition, cleanup state, and permission to release artifacts. Keep uncertain cleanup, contradictory terminal evidence, overflow, cancellation, and malformed evidence from becoming PASS.
3. Produce a single focused cross-branch discrepancy list only if material conflicts remain. Include each exact file/branch and the smallest correction needed; do not overwrite PR #3.
4. Review test traceability for each required behavior and mark whether it is: source-reviewed, executed in an isolated test environment, requires a real device, or requires a controlled provider test.
5. If test execution is possible in an approved offline assistant environment, run only the exact pure helper/test pair from the exact PR #3 head in a temporary reconstruction; record blob SHAs, command, interpreter, output, and limitations. Do not dispatch Actions or use a real provider.
6. Keep provider/security proof blocked until owner approval, documented cost bound, policy verification plan, and all provider-specific preconditions are satisfied.

**Exit gate:** the project can state precisely which contract rules are selected for the PR #3 offline baseline, which tests actually ran, which remain NOT RUN, and what cannot be proven without real infrastructure. No “secure” or “production-ready” claim is unlocked by static analysis alone.

### Month 3 — Test the mobile workflow and the Director hypothesis (2026-12-28 to 2027-01-27)

**Primary objective:** reduce UX and workflow uncertainty using phone-accessible methods and very small AI usage.

Work to complete:
1. Review the existing static prototype source and its Python check/test utilities. List the few most important mobile usability questions: first action clarity, paste/file entry, status comprehension, copy-report affordance, and clear labeling of simulated output.
2. Build a bounded phone usability protocol around one synthetic task, with observable completion steps and failure points. If the owner can voluntarily review the published preview on their phone, record their observations; do not make that a prerequisite.
3. For the AI Workflow Director, if free-tier capacity is available, prioritize **one** baseline-vs-Director EVAL-06 pair in the same AI app/model and fresh comparable chats. Save the complete prompts/outputs and mark incomplete conditions. Stop at the free-tier limit; no quota evasion or paid completion.
4. Do not attempt all eight evaluations by default. If a paired run cannot be completed under the available limits, record it as NOT RUN and use the offline fixtures for design review.
5. Compare low-risk deterministic tasks that may work locally (for example, basic text/JSON/CSV validation or simple conversions) with tasks that need a real Python environment. WebAssembly is a potential future tool for bounded local work, not a blanket answer: its sandbox still depends on the APIs and permissions exposed by the embedding application ([official security model](https://webassembly.org/docs/security/)).
6. Create no new native app, remote agent, API adapter, local-model integration, or backend feature merely because an alternative supports it.

**Exit gate:** one documented UX/evaluation result—or an honest NOT RUN record—changes or confirms a specific decision. Do not claim an efficiency gain from one anecdotal pair.

### Month 4 — Consolidate and prepare the PC-return gate (2027-01-28 to 2027-02-28)

**Primary objective:** turn accumulated research into a safe, ordered next-step package.

Work to complete:
1. Recheck the current main SHA, PR #2/#3 heads, active research branch, and all evidence records. Older handoffs and ahead/behind counts are snapshots only.
2. Create/update a concise decision memo: continue, narrow, pivot, or stop; the recommended first workflow; key alternatives; known costs/risks; and what evidence is still missing.
3. Prepare the PC-return runbook: clone/fetch instructions, exact branch/commit references, test commands, test environment expectations, required artifacts, and safety gates. Do not run a deployment workflow.
4. Order first-PC actions: inspect the exact current state; execute pure offline tests; compare output to expected fixtures; review differences; then revisit the separate controlled-runtime gate only if explicitly approved. Never begin with provider signup or live code execution.
5. Prepare a single integration/review checklist for PR #2 and #3 without changing either PR. Resolve code conflicts only after review and explicit authorization.
6. Revisit possible shared contracts with RevDev using the actual source/artifact revisions available at that time. Keep repositories separate and field mappings provisional until evidence supports them.
7. Archive stale status only by clearly marking it superseded; do not delete history or rewrite git history.

**Exit gate:** a new session with PC access can follow the checklist from a clean environment and knows the exact status of every gate. If PC access is still unavailable, continue with the next highest-value research task rather than treating the date as a deadline.

## 6. The repeatable work loop

For every substantial AI pass:

1. **Orient:** read this hub and the relevant source/checkpoint. Verify the branch/commit before making state claims.
2. **Name the decision:** state what uncertainty will be reduced and why it matters.
3. **Reuse:** inspect existing docs, code, libraries, tests, and prior research before creating new material.
4. **Batch:** complete one coherent deliverable with its supporting audit, links, and acceptance mapping in the same pass.
5. **Verify:** validate links/structure; execute only safe, in-scope checks in an available environment; report exact results or NOT RUN.
6. **Update continuity:** update the current checkpoint or existing decision/evidence register instead of creating duplicate master documents.
7. **Hand off:** report artifact links, branch/commit, evidence, limitations, blockers, and the next highest-value pass. Ask for owner input only when a real decision cannot be progressed without it.

Use existing evidence labels from the project research: **VERIFIED_PRIMARY_SOURCE**, **SECONDARY_SOURCE**, **INFERENCE**, **ASSUMPTION**, **UNVERIFIED**, **NEEDS_LIVE_TEST**, and **NEEDS_OWNER_APPROVAL**. For execution/testing, use **PASS**, **FAIL**, **BLOCKED**, **INCONCLUSIVE**, and **NOT RUN** only where those terms are justified.

## 7. Free-plan and phone-only efficiency rules

- Keep prompts and handoffs compact. Reference canonical GitHub files instead of pasting entire masters into every chat.
- Use one clearly scoped request per AI; ask another AI to review a specific risk or contract, not independently repeat the whole task.
- Batch related changes but keep high-risk work isolated.
- Prefer original/official sources for consequential vendor claims; date them. Use community posts to discover friction and counter-evidence, not to claim prevalence.
- Avoid repeatedly uploading the same documents. Ask connected file tools or GitHub sources to fetch only relevant sections whenever possible.
- Do not use token count, output length, number of AIs, commit count, or document volume as a proxy for progress.
- Stop a task when the next step requires PC-only evidence, a live provider, private data, owner approval, or spending. Record the blocker and work on an independent item.

## 8. Future feature portfolio — ordered by value and evidence gates

These are **ideas to evaluate, not approved scope**.

### Tier A — Strongest fit with the core hypothesis
1. **Trustworthy execution receipt:** show program outcome separately from service/job disposition; preserve exact exit/result evidence, runtime metadata, bounded outputs, and not-checked items.
2. **Copyable AI diagnostic report:** one explicit action that produces useful status, stderr/stdout summaries, file manifest, and the next debugging context without silently including secrets.
3. **Safe input/output file flow:** explicit file selection, clear supported-size/type limits, output manifest and integrity metadata, and no release of quarantined artifacts until cleanup/integrity/ownership gates pass.
4. **One tested task recipe:** a tiny task with sample inputs, expected output, one success and one failure case. CSV/JSON processing or a small image/file conversion are candidates, not frozen choices.
5. **Portable continuity capsule:** concise project/task state with verified facts separated from claims, assumptions, unknowns, checks-run, not-checked, and next action.

### Tier B — Useful extensions if the first workflow proves value
6. **Local deterministic tools:** JSON/CSV validation, text diffing, filename checks, simple conversions, or metadata inspection that can safely run on-device/browser without a paid backend. Use a browser sandbox/WASM approach only after capability, file-access, performance, privacy, and abuse constraints are explicit.
7. **Provider-neutral execution adapters:** keep UI, request/result contract, and execution backend separate so a future local phone runner, remote PC, or cloud sandbox can be swapped without rewriting reports.
8. **Opt-in remote PC bridge:** SSH/Tailscale or an equivalent controlled connection when the PC is available. A PC-hosted agent stops when its host is asleep/offline unless a separate always-on host exists; remote control must be explicit, auditable, and permission-limited.
9. **Privacy tools:** local redaction, data-preview before submission, clear retention/delete behavior, and exportable code/results. Never claim perfect secret detection.
10. **Phone-first reliability/accessibility:** interrupted-session recovery, resumable drafts, large touch targets, keyboard-aware layout, clear errors, screen-reader-friendly status, and low-bandwidth behavior.
11. **User-owned reusable recipes and profiles:** reusable prompts, constraints, verification checklists, and copy/paste setup instructions; no background app interception.
12. **Interoperable execution receipt format:** a versioned, provider-neutral receipt for code run/result/cleanup/artifact state that can eventually be compared with RevDev. Only after the contracts are reconciled from actual source revisions.

### Tier C — Defer until demand, security, and operating cost justify them
- Full desktop IDE replacement or broad autonomous multi-agent orchestration.
- Native iOS/Android apps before the PWA has measured, blocking limitations.
- Accounts, cross-device synchronization, cloud project history, teams/collaboration, public sharing, or a marketplace.
- Direct model APIs, hosted LLMs, local-model management, subscription/credit systems, provider-specific “one click” connections.
- Arbitrary shell, unrestricted outbound networking, long-running services, large builds/GPU jobs, or unattended agents.

## 9. Decision gates and falsification

Reconsider the product direction if:
- existing free local tools consistently solve the target task faster and more privately;
- users mostly want authoring/keyboard ergonomics or a full coding-agent environment rather than execution/reporting;
- representative target users rarely encounter the problem or will not trust the required file/execution path;
- no viable execution path can meet isolation, cleanup, output limits, latency, and a sustainable zero-cost or explicitly approved cost model;
- the report does not meaningfully improve AI-assisted correction over a simple copy of the error;
- the Director adds work or prompt overhead without improving continuation correctness.

A positive result from a desk-research exercise, one user anecdote, one AI pair, a simulated UI, or an offline fake adapter is not sufficient by itself to establish market demand or runtime safety.

## 10. Current state and next pass

This plan and the Continuity Hub are documentation artifacts on the isolated AI Workflow Director research branch. They do not change main or PR #2/#3. No live execution, provider test, spending, AI benchmark, merge, deployment, or Actions run is authorized by this plan.

**Completed during the first coordination passes (2026-10-28):**
- Prepared the [PC-return checklist draft](PC_RETURN_CHECKLIST_DRAFT_20261028.md) with exact-ref verification, separate worktrees, offline test sequence, evidence template, and an independently approval-gated provider path.
- Added the read-first [Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md) and this four-month plan.
- Completed a static [cross-branch execution-contract audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) using exact source refs and blob SHAs. It identified a user-facing verdict projection gap and a policy-revision-before-execution refinement; it did not edit either PR or run tests.
- Added a dated [phone-only competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md), supplementing rather than repeating the existing PR #3 competitor research.
- Added a [falsifiable product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) with counter-hypotheses and proposed decision criteria.
- Rechecked PR #2 and PR #3 metadata; both remain open, draft, unmerged, and their known head SHAs were unchanged. Counts and SHAs must be rechecked before consequential action.

**Next pass sequence:**
1. Reconcile the audit and new scan with the existing main-branch documents, editing only this isolated documentation branch and only where it resolves stale/contradictory navigation or status. Do not promote PR #3 decisions to main or overwrite their branch.
2. Refresh the existing competitor matrix with only the dated high-value delta, plus a link to the richer PR #3 competitor study; avoid a second competing full matrix.
3. Review the hypothesis card against the product spec, user evidence, and fixed-task comparison protocol. Keep the first task candidate provisional until compared against actual alternatives.
4. Draft a compact PC-return runbook that starts with exact branch/hash verification and offline tests, and keeps provider/live execution as a separate gated step.
5. Stop creating new high-level masters once navigation and decision gaps are closed. Focus remaining phone-only work on resolving a decision or preserving clear evidence, not producing more paperwork.

