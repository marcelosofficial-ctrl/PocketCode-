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

The first useful product is not necessarily a full mobile IDE, general-purpose coding agent, remote-control cockpit, or multi-agent platform. The hypothesis to validate is that a focused “run, inspect, report, iterate” workflow is easier and more trustworthy for a particular mobile task than existing free or familiar alternatives. The execution location is deliberately unresolved: compare local device apps, browser-embedded WebAssembly, a user's remote PC, and hosted execution. Do not assume a remote provider is required merely because the product goal includes running code.

### Supporting feature: AI Workflow Director

The Director can reduce repeated context, prepare compact task packets, preserve verified state in continuation capsules, and help users move between AI apps. Keep it provider-neutral and usable with manual copy/paste. It should support the core product, not displace proof of real execution.

The Director's **AWD-01–AWD-16** are proposed conformance cases and remain **NOT RUN**. Its **D-01–D-08** defaults are recommendations, not owner-approved product contracts. The separate lifecycle choices recorded in PR #3 are not Director decisions.

### Competitive caution discovered during this review

A public-source scan on 2026-10-28 surfaced local and remote alternatives: [AndroidHarness](https://github.com/Sanuu7/AndroidHarness), [PhoneCode](https://github.com/dttdrv/phonecode), [Atlan](https://github.com/Atlansdaddy/atlan), and [Pairlet](https://github.com/heypandax/pairlet). A more consequential iOS-specific finding is [Pyodios](https://pyodios.caffeinatedmath.com/), which describes local Python 3.14 via Pyodide/WebAssembly on iOS/iPadOS 26+ with no server. The relevant limitations and sources are documented in the [competitor addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md). These are maintainer/public-page claims, not hands-on results.

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
3. Keep the [competitor matrix](../RESEARCH/COMPETITOR_MATRIX.md) and [competitive analysis](../RESEARCH/COMPETITIVE_ANALYSIS.md) current. Compare local-on-device, browser/WASM, remote-PC, hosted, and plain copy/paste paths; include Pyodios as a serious iOS local-run comparator. The 2026-10-28 delta is recorded in the [competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md); no hands-on comparison has been run.
4. Reuse [mobile-coding user evidence](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) and the PR #3 [user/problem evidence protocol](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_USER_PROBLEM_EVIDENCE.md). Do not repeat the same search unless the evidence is outdated or the decision changed.
5. Prepare a compact “problem hypothesis card”: target user, last-mile situation, current workaround, proposed advantage, strongest counter-hypothesis, evidence quality, and the result that would change the recommendation.
6. Revisit naming collision risk before public brand/domain investments; do not rename the repository as a side effect.

**Exit gate:** a small set of candidate workflows is ranked against actual alternatives, with one recommended first workflow and explicit uncertainty. It is still a hypothesis; no market validation claim without representative evidence.

### Month 2 — Reconcile contracts, security gates, and test evidence (2026-11-28 to 2026-12-27)

**Primary objective:** make sure the contract being discussed is the same contract the helper/tests are meant to express.

Work to complete:
1. Compare the main branch's [proposed execution contract](../PRODUCT/EXECUTION_CONTRACT.md) and [security requirements](../SECURITY.md) with PR #3's draft execution contract, selected lifecycle baseline, acceptance matrix, helper, and test traceability. Separate invariants that apply to any execution path from provider/server-specific gates; do not assume the PR #3 policy-revision barrier or tenant controls apply unchanged to browser-local WASM.
2. Preserve the distinction between execution observation, derived job disposition, cleanup state, and permission to release artifacts. Keep uncertain cleanup, contradictory terminal evidence, overflow, cancellation, and malformed evidence from becoming PASS.
3. Produce a single focused cross-branch discrepancy list only if material conflicts remain. Include each exact file/branch and the smallest correction needed; do not overwrite PR #3.
4. Review test traceability for each required behavior and mark whether it is: source-reviewed, executed in an isolated test environment, requires a real device, or requires a controlled provider test.
5. If test execution is possible in an approved offline assistant environment, run only the exact pure helper/test pair from the exact PR #3 head in a temporary reconstruction; record blob SHAs, command, interpreter, output, and limitations. Do not dispatch Actions or use a real provider.
6. Keep provider/security proof blocked until owner approval, documented cost bound, policy verification plan, and all provider-specific preconditions are satisfied.

**Exit gate:** the project can state which safety/report invariants apply to the selected candidate path, which PR #3 rules remain remote-provider-specific, which tests actually ran, which remain NOT RUN, and what cannot be proven without real infrastructure. If local/WASM remains a candidate, separately define its exposed APIs, worker termination, input/output quotas, package policy, persistence, and report evidence. Static analysis alone does not unlock any “secure” or “production-ready” claim.

### Month 3 — Test the mobile workflow and the Director hypothesis (2026-12-28 to 2027-01-27)

**Primary objective:** reduce UX and workflow uncertainty using phone-accessible methods and very small AI usage.

Work to complete:
1. Review the existing static prototype source and its Python check/test utilities. List the few most important mobile usability questions: first action clarity, paste/file entry, status comprehension, copy-report affordance, and clear labeling of simulated output.
2. Build a bounded phone usability protocol around one synthetic task, with observable completion steps and failure points. If the owner can voluntarily review the published preview on their phone, record their observations; do not make that a prerequisite.
3. For the AI Workflow Director, if free-tier capacity is available, prioritize **one** baseline-vs-Director EVAL-06 pair in the same AI app/model and fresh comparable chats. Save the complete prompts/outputs and mark incomplete conditions. Stop at the free-tier limit; no quota evasion or paid completion.
4. Do not attempt all eight evaluations by default. If a paired run cannot be completed under the available limits, record it as NOT RUN and use the offline fixtures for design review.
5. Compare local-on-device Python (for example Pyodios), browser-local Pyodide/WASM, remote-PC, and hosted execution against the same synthetic task. Pyodide is promising for a bounded compatible subset, but package support is limited to pure-Python wheels or supported WASM builds ([official package docs](https://micropip.pyodide.org/en/latest/project/usage.html)); WebAssembly confinement also depends on the APIs and policies exposed by the embedding application ([security model](https://webassembly.org/docs/security/)). Do not treat local WASM as general-purpose CPython or an automatic hard resource/security boundary.
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


### Ordered execution board — concrete outputs and gates

Use this sequence alongside the dated Month 1–4 plan. Complete a gate or record why evidence is unavailable, then move on. Do not create a parallel master document.

#### Gate A — orientation and conflict cleanup (now through 2026-11-10)
- Reconcile root project status with the newer local-first / execution-location-neutral hypothesis.
- Make the Continuity Hub a clean navigation index and keep the checkpoint as the single current task queue.
- Verify branch state and preserve PR boundaries.
- **Output:** one simple start route, one current checkpoint and no contradictory statement that remote execution is already selected.
- **Exit:** a new chat can find the accepted decisions, current task, source-of-truth rules and next action in a few minutes.

#### Gate B — product/problem decision (2026-11-11 to 2026-11-27)
- Reuse existing public user evidence and competitor work; research only gaps that could change the decision.
- Compare manual copy/paste, local phone runtime, browser-local WASM, remote PC and hosted execution using the same fixed task.
- Review name/discoverability risk without renaming the repository or buying a domain.
- **Output:** update the existing hypothesis card and competitor matrix with pro/con evidence and a continue/narrow/pivot/stop recommendation.
- **Exit:** one target job is clearly stated, strongest alternatives are identified, and at least one falsifying observation is specified. Desk research is not representative market validation.

#### Gate C — contract and safety reconciliation (2026-11-28 to 2026-12-13)
- Reconcile exact main / PR #2 / PR #3 semantics for execution outcome, job disposition, cleanup, report verdict and artifact release.
- Treat policy-revision-before-start as a concrete evidence/barrier requirement, not a boolean magically proven by a report formatter.
- Resolve or explicitly preserve the reviewer question for EXIT_NONZERO combined with failed/unknown mandatory gates; FAILED must never implicitly release artifacts.
- Separate universal invariants from hosted-provider controls and local/WASM-specific boundaries.
- **Output:** a small discrepancy/decision list with exact refs, test expectation and whether owner/reviewer approval is needed.
- **Exit:** important lifecycle states and release gates have explicit expected behavior and a test/evidence class.

#### Gate D — test traceability and deterministic protocol (2026-12-14 to 2026-12-27)
- Trace each material requirement to existing test IDs/helpers and classify it as source-reviewed, offline-executable, device-only or provider-only.
- If a safe isolated assistant environment is available, run only exact pure-helper/test files from exact branch blobs; record revision, command, interpreter, output and limitations. Otherwise mark NOT RUN and continue with independent work.
- Keep the CSV/JSON success and malformed-input worksheet as a protocol, not completed evidence.
- **Output:** test/evidence matrix plus PC-return test/fixture list.
- **Exit:** no test is called passing unless the exact checked-in revision was actually executed.

#### Gate E — phone UX and Director scope check (2026-12-28 to 2027-01-13)
- Review the static prototype source for first-action clarity, code/input flow, status legibility, copy-report affordance, simulated labels and failure-state clarity.
- Do not trigger Pages/Actions to view or validate documentation. Voluntary owner phone observations are helpful but not required for independent source work.
- Keep the Director a thin supporting feature; its first pure packet/capsule proposal should remain local/offline.
- **Output:** a short UX issue list, ranked by user impact and evidence quality.
- **Exit:** each proposed UI change has a task-based reason; no code/runtime claim is inferred.

#### Gate F — minimal evaluation (2027-01-14 to 2027-01-27)
- Only if the owner chooses and free usage permits, perform at most one baseline-vs-Director pair, prioritizing EVAL-06, using the same app/model and comparable fresh chats.
- Record complete prompts/outputs and measurement conditions. Stop at any free-tier limit; never evade it.
- If the pair is not feasible, record NOT RUN and preserve the protocol instead.
- **Output:** one honestly scoped result or a reasoned NOT RUN record.
- **Exit:** no broad savings/correctness claim is inferred from a single exploratory pair.

#### Gate G — PC-return preparation (2027-01-28 to 2027-02-13)
- Refresh exact main and PR heads; inspect differences without modifying PR #2/#3.
- Prepare the sequence: inspect worktree/branch → verify exact blobs → run pure offline tests → compare expected fixtures → inspect the resulting diff → review permissions → only then consider whether a separate controlled-runtime request is justified.
- Name any test requiring a real device/provider, prerequisites, cost/safety approvals and expected evidence.
- **Output:** a clean-session PC-return runbook with explicit stop conditions.
- **Exit:** the first PC session starts with repository/test inspection, never provider signup or live execution.

#### Gate H — decision and restart handoff (2027-02-14 to 2027-02-28)
- Choose continue, narrow, pivot or stop, and state evidence for and against.
- Finalize the first workflow candidate, contract discrepancy list, future-feature ranking and PC-return checklist.
- Revisit whether formal name review is worthwhile; do not rename or spend as a side effect.
- **Output:** one updated checkpoint/handoff and an owner-readable decision, not another set of competing master docs.
- **Exit:** a fresh chat or returning PC session can take the next safe action using exact refs without guessing.

#### Recurring cadence
Each pass should deliver at least one of: a clearer decision, reconciled evidence conflict, reproducible test/protocol, reviewed risk, or safer next action. Update only the checkpoint every one or two weeks if state or priority changed. Stop polishing docs once navigation is clear; work on the highest-uncertainty decision instead.

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
13. **Environment and trust preflight:** before a task starts, show the selected execution location, supported runtime/packages, file permissions, network policy, resource limits, persistence/cleanup behavior and any unknowns. Every claim should carry a source or be labelled unknown; this must not be a marketing-only “secure” badge.
14. **Diff-first AI repair loop:** let the user preview a suggested code change as a diff, accept/reject it explicitly, preserve the prior version, run the same fixture again and compare results. No silent overwrite or automatic change application in the first version.
15. **Run-to-run regression view:** compare exit/outcome, bounded logs, output manifest and file diffs between attempts so users can see whether a fix changed the result rather than relying on an AI's assertion.
16. **Portable workspace/evidence bundle:** export/import a clearly scoped project snapshot containing source, selected inputs, outputs, report, version metadata and manifest, while excluding credentials and unrelated files. This supports handoff and PC-return without mandatory cloud sync.
17. **Offline-first task recipes:** a small library of narrow, deterministic workflows (for example CSV/JSON validation, text/metadata inspection and file conversion) that can be useful before a general code runner or provider is viable.

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
- Completed a static [cross-branch execution-contract audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) using exact source refs and blob SHAs. It identified a user-facing verdict projection gap and a policy-revision-before-execution refinement; it did not edit either PR or run tests. Verified all 11 source blob SHAs in the audit against the exact referenced branch/files. Added a proposed PASS/FAIL/INCOMPLETE projection table that preserves execution outcome, cleanup/evidence, and derived disposition; it remains advisory.
- Added a dated [phone-only competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md), supplementing rather than repeating the existing PR #3 competitor research.
- Added a [falsifiable product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) with counter-hypotheses and proposed decision criteria.
- Added a [fixed-task comparison worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) that defines one synthetic CSV-to-JSON success/failure task and a record/scoring template across local, browser/WASM, remote-PC, hosted, and manual-chat paths. It is design-only and NOT RUN.
- Refreshed the existing competitor matrix and competitive analysis on this branch with the new alternatives and the local-first/WASM question; did not edit PR #3. The dated scan now includes Pyodios, whose current public pages claim local Python via Pyodide/WASM on iOS 26+; package/memory/file-flow suitability remains unverified.
- Rechecked PR #2 and PR #3 metadata; both remain open, draft, unmerged, and their known head SHAs were unchanged. Counts and SHAs must be rechecked before consequential action.

**Latest structure/direction pass (2026-10-28):** aligned README, Project Status, Product Spec, Architecture, Continuity Hub, new-chat handoff and checkpoint. Remote execution is now explicitly one candidate, not the chosen MVP path; the duplicate RevDev compatibility section was removed from Product Spec. The existing plan now includes ordered Gates A–H and five additional gated future ideas (trust preflight, diff-first repair, run comparison, portable workspace/evidence bundle, offline recipes). These are proposals, not scope approvals.

**Static check of the changed navigation set:** 160 relative Markdown links across the six updated orientation/status documents resolved against the research-branch tree with zero missing paths. Their Markdown code-fence counts were balanced. Twenty-five external references were identified but not checked for live availability; there were no fragment-only heading anchors in the scoped files. This is not a repository-wide link audit or rendered-Markdown test.

**Current next-pass sequence:**
1. Continue exact-ref contract review for the policy-revision-before-start requirement and EXIT_NONZERO with missing/failed gates. Preserve the difference between process outcome, overall job disposition and artifact-release eligibility.
2. Reconcile the fixed-task findings against the existing product hypothesis and competitor matrix; make a continue/narrow/pivot recommendation without claiming an unrun benchmark.
3. Conduct a focused source review of the static prototype's mobile flow and simulated-label correctness; do not trigger deployment/Actions.
4. Follow Gates A–H above, update only existing authoritative docs/checkpoint when findings materially change, and leave PR #2/#3 untouched.

Progress means reducing uncertainty, increasing evidence quality or improving the next safe action—not document/commit volume.