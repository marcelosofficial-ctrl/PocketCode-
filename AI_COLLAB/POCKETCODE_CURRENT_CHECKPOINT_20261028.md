# PocketCode — Current Work Checkpoint

**Checkpoint date:** 2026-10-28  
**Status:** Discovery/research only. No production execution path, provider, or Director implementation is established.  
**Purpose:** The compact live queue for every new chat. Detailed evidence stays in specialist documents linked below; this file is not a duplicate history log.

## 1. Current direction

PocketCode's core hypothesis is a phone-first **run → inspect → report → correct → rerun** loop for small coding tasks. The user should be able to see what actually happened and carry truthful evidence to any AI assistant.

**Execution location is undecided.** Local phone runtime, browser-local WASM, user-owned remote PC, hosted execution and manual copy/paste must compete on the same bounded task. Do not choose a remote provider by default.

The AI Workflow Director is a **supporting feature hypothesis** for task packets, continuation capsules and better handoff between AI chats. It must not displace the core run/report loop.

## 2. Verified operating state

| Area | Current verified status | Limit |
|---|---|---|
| Product phase | Discovery and product definition | No validated market advantage or final MVP decision |
| Published mobile prototype | Static UI exists | Result display is SIMULATED; no real code execution |
| Main product spec / architecture | Updated on this research branch to keep local and remote paths open | These edits are not integrated into main |
| Fixed-task comparison | Synthetic CSV-to-JSON success/failure protocol exists | App/browser/remote/hosted comparison NOT RUN |
| Competitor research | Current dated public-source scan includes local iOS Python/WASM and Android/remote alternatives | Claims are source-led; no hands-on performance/security benchmark |
| PR #2 | [Open draft PR](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2), head eb8b7ea83cb0e8fe1880351276c485b761431791 | Description records 25 passing Python tests in a temporary reconstructed tree; no real runtime/provider/security proof |
| PR #3 | [Open draft PR](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3), head 0ddcc0bc97bac5d446aefedf3d71f99411bd841d | Contains lifecycle contract/helper/tests; exact checked-in helper/test pair reported NOT RUN; no live provider test |
| AI Workflow Director | Spec, fixtures, decision register, evaluation kit and manual run sheet exist | Not implemented; AWD-01–AWD-16 and EVAL-01–08 NOT RUN |
| Provider / cost | No provider or paid service selected; budget remains $0 | No account setup, billing, live workload or spend authorized |
| User research | Existing qualitative public-source research | No representative interviews, product-market validation or completed fixed-task study |

The Director research branch is isolated and is **not main**. Its head/ahead count changes with every commit; refresh exact branch/main refs before consequential work. PR #2 and PR #3 are separate streams and must remain untouched without explicit authorization.

## 3. Work completed in the latest organization pass

1. Reorganized the [Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md) into a simpler start route, source-of-truth map, branch map, role definitions and default priorities.
2. Added ordered Gates A–H and concrete outputs to the [four-month master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md), ending 2027-02-28.
3. Corrected the stale “remote runtime first” wording in [PROJECT_STATUS.md](../PROJECT_STATUS.md), [PRODUCT_SPEC.md](../PRODUCT_SPEC.md) and [ARCHITECTURE.md](../ARCHITECTURE.md). Execution location is now explicitly undecided; the architecture shows hosted/remote and local/browser as different candidates.
4. Simplified the README's start-here route and refreshed the [new-chat handoff](NEW_CHAT_HANDOFF_20261028.md).
5. Removed a duplicated RevDev compatibility section from PRODUCT_SPEC.md.
6. Added future-only ideas to the master plan: environment/trust preflight, diff-first repair, run-to-run comparison, portable workspace/evidence bundle, and offline-first task recipes. These are options, not approved MVP scope.
7. Tightened the [fixed-task worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) with canonical inputs, failure behavior, evidence capture and disqualifiers.
8. Refined the [cross-branch contract audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) around disposition ordering, artifact-release separation and policy-revision evidence.

These were documentation/source-review changes on the isolated research branch. No implementation tests, app installs, provider workload, AI evaluation, merge, deployment, Actions run or spending occurred in the organization pass.

9. Latest scoped link check covered ten orientation/product documents (README, Project Status, Product Spec, Architecture, Continuity Hub, four-month plan, handoff, checkpoint, hypothesis card and PC-return checklist): 170 relative Markdown links resolved against the branch tree with zero missing paths; no fragment-only anchors were present in this set. Twenty-eight external URL references were identified but not checked for live availability. This is a static path check, not a repository-wide or rendered-Markdown audit.
10. Confirmed at source level that Project Status/Product Spec no longer treat a remote runtime as selected, Architecture documents local/browser and hosted/remote paths as unselected candidates, and Product Spec now has one RevDev compatibility section rather than a duplicate.
11. Added an adversarial product-hypothesis section to the existing [Product Hypothesis Card](PRODUCT_HYPOTHESIS_CARD_20261028.md): strongest counterargument, possible provider-neutral evidence/continuity differentiator, explicit falsification conditions, and current continue-discovery/no-provider recommendation.
12. Added a source-to-test traceability table to the [Cross-Branch Execution-Contract Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) and exact blocker checklist to the [PC-return checklist](PC_RETURN_CHECKLIST_DRAFT_20261028.md). These map policy-before-start, EXIT_NONZERO plus gate failures, artifact release, cleanup history, event ordering and output limits to source/test refs while preserving NOT RUN/provider-only boundaries.

## 4. Critical unresolved contract questions

### A. Policy revision before start

PR #3 research specifies NET-BARRIER-01 and NET-SEM-01: the exact mandatory policy revision must be confirmed applied before execution; missing, late, failed or mismatched policy evidence must prevent task start. The reviewed pure lifecycle helper receives a boolean policy_confirmed and cannot itself prove the revision identity or start ordering.

**Next:** trace the requirement to the coordinator/adapter seam and a test that proves execute cannot be called before the exact revision is confirmed. This is a source/test-design gap, not a proven live vulnerability and not a passing control.

### B. EXIT_NONZERO plus failed or unknown gates

The PR #3 helper returns FAILED for EXIT_NONZERO before checking cleanup, policy, termination, artifact validity or tenant/job authorization. That can preserve an observed program failure, but the job-disposition contract must decide how missing/failed gates affect the overall disposition.

**Invariant:** preserve trustworthy process observations separately; FAILED must never imply artifact release. Artifact-release eligibility remains independently fail-closed on cleanup, integrity, job association and authorization. The precise FAILED-vs-INCOMPLETE projection remains unresolved.

Full source refs and the next proposed cases are recorded in the [Cross-Branch Execution-Contract Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md). Do not modify PR #2 or PR #3 to settle the question without explicit authorization.

## 4A. Additional source-review findings (2026-10-28)

### Policy barrier — exact evidence boundary

- Reviewed PR #3 branch tree at head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d` (71 tracked paths). The relevant executable logic found is the pure `scripts/lifecycle_contract.py` helper and `scripts/test_lifecycle_contract.py`; no coordinator/provider-adapter implementation path is present in that tree. This is a scoped repository-tree observation, not proof that no external/private integration exists.
- `derive_disposition(...)` accepts a boolean `policy_confirmed`. It can fail closed when that value is not exactly `True` for EXIT_ZERO, but the function cannot establish which policy revision was applied or whether application occurred before process start.
- The draft contract and matrix define the stronger barrier: exact required revision confirmed on the intended boundary before the task-start call; pending, missing, failed, late or mismatched revision must prevent start. NET-BARRIER-01 / NET-SEM-01 are test requirements, not evidence that a coordinator/adapter enforces them.
- The current pure tests cover false/malformed gate values and EXIT_ZERO gate failures. The source reviewed does not itself prove a test of a real start-call ordering barrier. Exact checked-in tests remain NOT RUN.
- The nonzero-exit question remains a semantic decision, not a proven bug: the helper returns FAILED for EXIT_NONZERO before checking cleanup/policy/authorization gates. Preserve the nonzero observation, independently deny artifact release when any release gate fails, and obtain reviewer/owner agreement on FAILED versus INCOMPLETE for the overall disposition in those combinations.

### Mobile prototype — static UX source review only

Reviewed `prototypes/mobile-runner/index.html` at blob `e2c4ece041be95ce9a73bc60ff354702b21c33c2`, plus the existing static checker and its test source. The prototype's controls explicitly select fixed sample success/failure examples; the page, report and copy-debugging prompt disclose that submitted code is not executed. It remains ineligible for execution/correctness scoring.

**Concrete UX issue:** the top workspace status uses the green `.status` style for both sample-success and sample-failure states. The render handler changes its text to “Sample failed” but does not switch the status color/dot to a failure style. The result badge and exit-status metric do change, so this is a visual inconsistency rather than evidence of a false execution claim. Record it as a prototype polish item; no prototype code was changed in this documentation-only pass.

**Review limits:** source inspection only. Browser interactions, clipboard behavior, mobile layout, accessibility and the Python source-check suite were not executed. The static checker itself says it does not run browser JavaScript or submitted code.

## 5. Four-month plan — operating schedule

Use the [master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) as the schedule; the gates below summarize it.

| Period | Main focus | Required output |
|---|---|---|
| **Oct 28–Nov 10** | Orientation, stale-source conflict cleanup, evidence/branch map | Navigation a new chat can follow quickly; one current queue |
| **Nov 11–Nov 27** | Product/problem hypothesis and strongest alternatives | Decision-ready recommendation to continue, narrow, pivot or stop |
| **Nov 28–Dec 13** | Lifecycle/report/security contract reconciliation | Exact discrepancy list and explicit outcome/disposition/artifact gates |
| **Dec 14–Dec 27** | Test traceability and deterministic protocol | Requirement-to-test/evidence matrix and PC-return command/artifact list |
| **Dec 28–Jan 13** | Phone UX/static prototype and Director scope | Task-based UX findings; no deployment or implementation claim |
| **Jan 14–Jan 27** | Optional minimal Director evaluation | One properly recorded EVAL-06 pair or explicit NOT RUN |
| **Jan 28–Feb 13** | PC-return preparation | Ordered clean-session runbook with stop conditions |
| **Feb 14–Feb 28** | Final direction and handoff | Evidence-backed continue/narrow/pivot/stop recommendation and exact next steps |

This schedule is a sequence of evidence gates, not a promise of PC availability or a requirement to fill every date. If evidence is unavailable, record NOT RUN/UNKNOWN and progress on an independent task.

## 6. Immediate next queue

**Completed in this pass:** scoped structure/link verification; exact-ref policy-barrier and disposition source trace; static prototype review; adversarial product-hypothesis review; source-to-test traceability map; and PC-return checklist crosswalk. Do not repeat these unless source refs change.

1. **Finish the first-PC-session evidence packet.** The PC-return checklist now names exact offline commands, worktree separation, source blobs, hard stops and the contract blockers. The next documentation-only improvement is to add a one-page result-record template that makes each claim's source, test evidence, limits and follow-up explicit; do not create a new master file.
2. **Prepare a bounded independent-review prompt** for Gemini or Claude to challenge the strongest counterargument/falsification conditions and the claimed value of a portable evidence/continuity layer against local-first alternatives. Require concrete counterexamples and cited sources; ask for a decision recommendation, not more broad research. Do not treat silence as approval.
3. **Preserve implementation boundaries.** The prototype status-color mismatch is a small source-reviewed polish issue; do not change source in this documentation/continuity pass. Any later UI change needs explicit authorization and must preserve the simulated-execution labels.
4. **When PC returns, follow the checklist in order.** Re-fetch exact refs, run safe offline tests in separate clean worktrees, capture command/environment/exit/results, and stop at any missing prerequisite. Provider tests remain a separate, explicit owner-approval gate.

No owner action is required to continue documentation-only work. Ask only when a specific task truly requires a phone observation, independent reviewer response or an explicit cost/safety decision.

## 7. Canonical links for the next chat

- **Orientation:** [Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md)
- **Calendar and future opportunities:** [Four-Month Master Plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md)
- **Product problem and falsification:** [Product Hypothesis Card](PRODUCT_HYPOTHESIS_CARD_20261028.md)
- **Fair comparison protocol:** [Fixed-Task Worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md)
- **Execution/report contract questions:** [Cross-Branch Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md)
- **Competitor evidence:** [Phone-Only Competitor Addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) and the existing [Competitor Matrix](../RESEARCH/COMPETITOR_MATRIX.md)
- **PC-return preparation:** [PC-Return Checklist](PC_RETURN_CHECKLIST_DRAFT_20261028.md)
- **Director details:** use the document map in the [Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md); all Director contracts remain design-only until approved.

## 8. Rules that must survive every handoff

- Public repo: no secrets or private user data.
- Budget $0; no billing, paid APIs, live provider runs, Actions, merge, deployment or PR #2/#3 changes without explicit authorization.
- No quota evasion, background clipboard polling, private-chat scraping, system-wide overlay, silent cross-app control or unrestricted shell/network.
- A simulated UI is not execution evidence; source review is not a test.
- Reuse existing docs/dependencies before writing new code or creating a new document.
- One primary task per AI pass; specific adversarial review question for the second AI; consolidate evidence before acting.
- Keep PocketCode separate from RevDev. Exact source revisions and explicit decisions are required before any mapping.
