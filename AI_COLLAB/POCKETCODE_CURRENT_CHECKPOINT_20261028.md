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

13. Added a blank cross-path synthesis and decision-record template to the [fixed-task worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md). It keeps success and malformed-input results separate, records the strongest counter-evidence per path, and prevents rankings while critical evidence is unknown. This is a protocol improvement only; all path comparisons remain NOT RUN.

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


### Next highest-value pass (after synthesis template)

1. Do a focused primary-source freshness check only for facts that could change the fixed-task candidate set or a disqualifier (especially target-platform availability, first-run/package/file limitations, and current free-tier prerequisites); update existing source notes rather than creating another competitor report.
2. If an independent Gemini/Claude challenge arrives, reconcile concrete claims against source URLs and this worksheet; otherwise continue without blocking on it.
3. Do not score paths, claim a winner, or call the task comparison complete until the exact success and malformed-input scenarios have real evidence. Current comparison remains NOT RUN.

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

### Source-freshness pass — 2026-10-28

Reviewed current official Pyodios FAQ/app page, Pyodide browser file-access documentation, and AndroidHarness public listing/repository. Updated the existing [competitor addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) and [fixed-task worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) rather than creating another report.

Material findings:
- Pyodios is a serious iOS-local comparator for the standard-library CSV task; its official docs describe real file import/export and local execution, but task behavior remains NOT RUN.
- Its FAQ says running code cannot currently be interrupted directly; a 120-second timeout does not stop the code, and the session may need restarting. Timeout is not proof of termination.
- Browser-local Pyodide requires explicit file-transfer integration; its native file-system path is experimental and limited in browser support. Do not assume an iPhone PWA has the same file flow as a native local app.
- Target-device note: if the eventual comparison uses an iPhone 13, third-party technical reporting lists 4 GB RAM; Pyodios identifies 4 GB as its minimum and says startup memory pressure is more likely at that level. iOS compatibility alone does not establish reliable startup. This is a test condition to capture, not a reason to install/test now.
- Developer/app-store privacy statements are not independent security audits.
- AndroidHarness is a serious broader local-first alternative; public feature claims are not comparative test evidence.

The worksheet now distinguishes the small fixed-task test from general timeout/recovery and security questions. No app was installed, no code was run in competitor products, no provider workload was used, and no costs were incurred. All task comparisons remain NOT RUN.

## 6. Immediate next queue

**Completed in this pass:** scoped structure/link verification; exact-ref policy-barrier and disposition source trace; static prototype review; adversarial product-hypothesis review; source-to-test traceability map; PC-return blocker crosswalk; and compact evidence-record template. Do not repeat these unless source refs change.

1. **Get one independent challenge, when convenient.** The copy-ready prompt below asks Gemini or Claude to attack the product hypothesis with concrete counterexamples rather than produce another broad research report. No reviewer response is assumed.
2. **Reconcile only material reviewer findings.** Update the existing hypothesis card, competitor addendum or checkpoint only if the reviewer supplies verifiable counter-evidence, identifies a specific missing alternative, or exposes a false assumption.
3. **Preserve implementation boundaries.** The prototype status-color mismatch is a small source-reviewed polish issue; do not change source in this documentation/continuity pass. Any later UI change needs explicit authorization and must preserve the simulated-execution labels.
4. **When PC returns, follow the checklist in order.** Re-fetch exact refs, run safe offline tests in separate clean worktrees, capture command/environment/exit/results, and stop at any missing prerequisite. Provider tests remain a separate, explicit owner-approval gate.

### Ready-to-send independent review prompt

> Independently challenge PocketCode's current product hypothesis using the existing AI_COLLAB/PRODUCT_HYPOTHESIS_CARD_20261028.md, AI_COLLAB/PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md, and RESEARCH/COMPETITOR_MATRIX.md.
>
> Do not repeat broad mobile-coding research. Focus on one decision: **is a provider-neutral, portable evidence/report/continuity loop a meaningfully differentiated phone-first product, or can strong local-first alternatives plus ordinary copy/paste already do it well enough?**
>
> Return: (1) the strongest counterexample/product substitute and the exact capability that undermines the hypothesis; (2) any concrete feature gap supported by current primary sources; (3) one same-task comparison that could falsify the hypothesis; (4) missing assumptions or misleading claims in our current card; (5) a concise continue/narrow/pivot/stop recommendation.
>
> Cite exact public sources or repository paths. Label each statement DOCUMENTED CLAIM, DIRECT OBSERVATION, INFERENCE, or UNKNOWN. Do not claim hands-on testing unless you actually performed it. Do not install apps, create accounts, run providers, trigger Actions, change repository files, spend money, or recommend a paid path. Return findings only; PocketCode remains in discovery and the budget remains $0.

No owner action is required to continue documentation-only work. If you send this to another AI, bring its complete answer back for evidence reconciliation; do not treat silence or unsupported opinion as approval.

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


## 4B. Competitor evidence-handoff counterexamples — 2026-10-28

A targeted public-source review found that evidence/log handoff is already described by adjacent tools, so the current differentiator must be narrowed:

- AndroidHarness documents inspectable tool cards, command exit/termination outcomes, run history/recovery, build/test status, failed-run handoff, and a whitelisted diagnostic report.
- Atlan documents mirrored console logs and automatic attachment of errors to the agent's next turn.
- Pairlet documents streaming output/tool events, session continuity/replay, file diffs and usage context, subject to per-backend limits.
- Pyodios documents local execution and file import/export; PhoneCode documents a local agent/workspace and an AI-output-report endpoint.

Sources, qualifications, and the revised falsification questions are recorded in the [competitor addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md), with a concise delta in the [competitor matrix](../RESEARCH/COMPETITOR_MATRIX.md) and the [product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md).

**Revised hypothesis only:** test whether a portable, execution-location-neutral receipt that binds evidence to a particular run/input/source/artifact and explicitly represents unknown evidence improves a separate AI's next correction or cross-tool portability beyond competitors' native logs/reports and raw-error copy/paste. This is not a demonstrated gap.

**Next bounded task:** update the fixed-task worksheet's report-layer comparison criteria to compare each alternative's native evidence against the proposed receipt, including whether the separate AI correction actually improves. Keep every path NOT RUN until a real, approved attempt. Do not select an execution location, implement the receipt, or change PR #2/#3 on the basis of desk research alone.


## 4C. Report-contract alignment check — 2026-10-28

The new portable-receipt falsification protocol was cross-checked against the existing [proposed execution contract](../PRODUCT/EXECUTION_CONTRACT.md) and [execution-loop acceptance criteria](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md). These already define the core report requirements: lifecycle status, exit evidence only when available, runtime/version and duration when known, bounded stdout/stderr with truncation, output-file metadata, and explicit missing evidence. Acceptance separates user-facing PASS/FAIL/INCOMPLETE from exact lifecycle status and keeps script-reported checks distinct from independently verified facts.

**Constraint for future work:** do not create a competing report schema. Treat the existing proposed PocketCode report as the candidate format and compare it with each alternative's native report/logs and raw-error handoff. The research question is whether its provenance, unknown-state and cross-tool portability semantics improve the next correction enough to matter. This is a source consistency check only; no report implementation or task comparison was run.


## 4D. Remaining report-contract question — run/input/source binding

A closer read of [PRODUCT/EXECUTION_CONTRACT.md](../PRODUCT/EXECUTION_CONTRACT.md) confirms the proposed report currently calls for a run ID, runtime/version, final status, exit/duration when known, bounded stdout/stderr, output filenames/sizes, and explicit uncertainty. It does **not** explicitly require an input digest, source/script revision, or output-content digest.

Do not silently treat those extra identifiers as already accepted. The fixed-task study may test whether run-to-input/source/artifact binding improves repeatability or the next AI correction; record its value and privacy/collection cost. If evidence supports adding it, propose a versioned change to the canonical contract. Otherwise keep the simpler report. No implementation or comparison has been run.


## 4E. Pyodios direct-iPhone comparator — 2026-10-29

Official source review confirms Pyodios is a stronger direct iPhone baseline than previously stated: its v1.1 docs describe local CPython 3.14.2/Pyodide 314.0.5, project working directories, script run controls, CSV and JSON preview, persistent real files, and import/export through the iOS Files/share sheet. A standard-library-only CSV-to-JSON task should not require installing a package (inference only; not run).

Important caveat: Pyodios says a run can time out after 120 seconds while the code keeps executing in the background. The timeout message is therefore not proof of termination. The FAQ also describes a fresh Python session per app launch and about 300 MB of Python memory, with startup susceptible to memory pressure.

The reviewed documentation does not establish whether Pyodios exposes a PocketCode-equivalent structured per-run report, authoritative exit code/terminal lifecycle status, bounded stdout/stderr with truncation metadata, or machine-readable timeout-but-still-running state. Mark these UNKNOWN / NOT DOCUMENTED until a hands-on attempt; do not treat silence in docs as proof of absence.

**Next direct comparator:** Pyodios, then browser-local Pyodide only if an iPhone Safari file-import/export workflow is shown to be practical. Use fresh project folders for success and malformed-input cases, verify real output file and export, capture native evidence, and compare with the existing canonical report. All hands-on work remains NOT RUN; no app was installed and no product or report contract was changed.


## Additional direct iPhone alternatives — 2026-10-29

A source review identified Carnets as another direct $0 local-execution comparator: the App Store describes offline Python/Jupyter on iPhone/iPad, and the developer project describes directory access. Its listed app size is about 1.5 GB (2.2 GB for the scipy variant), so storage is a meaningful cost. Juno documents free execution as a trial before paid Pro; Pyroid lists five free runs before paid Pro. These are product-description claims, not hands-on verification.

If a future comparison is approved, prioritize ordinary AI chat/copy-paste, Pyodios, and Carnets; treat Juno/Pyroid as limited-run alternatives and browser-local Pyodide as conditional on practical iPhone Safari file handling. All task comparisons remain NOT RUN; no apps were installed.

## Carnets workflow-fit delta — 2026-10-29

A follow-up source check found that Carnets is a real $0 on-device Jupyter/Python comparator, but the end-to-end workflow needs verification before scoring it as a direct script IDE. The App Store currently lists 1.5 GB. Official developer materials describe local execution and directory access; older maintainer support guidance describes running standalone `.py` scripts from a notebook with `%run file.py` and explains that iOS permission to open one file may not grant access to sibling data files unless the containing directory is explicitly selected. These older reports are test prompts, not proof of current limitations. Sources: [developer page](https://holzschu.github.io/Carnets_Jupyter/), [App Store](https://apps.apple.com/us/app/carnets-jupyter/id1450994949), [historical script guidance](https://github.com/holzschu/Carnets/issues/38), [directory permissions](https://github.com/holzschu/Carnets/issues/101).

The competitor matrix and fixed-task worksheet now record this caveat and its preflight. The comparison remains NOT RUN; no app was installed, no task executed, and no report contract or product code changed. Ahead/behind counts are snapshots; refresh before consequential work. PR #2 and PR #3 remain open, draft, and unmerged with their previously recorded head SHAs.


## Open-source reuse audit — 2026-10-29

Completed a focused public-source review of RunSeal, AndroidHarness, PhoneCode, OpenHand, Pairlet and OpenHands. The new [Open-Source Reuse Audit](OPEN_SOURCE_REUSE_AUDIT_20261029.md) records source links, license cautions, patterns worth adopting, and what not to port. Main conclusion: reuse proven lifecycle/conformance and recovery patterns before copying code; do not vendor a full runtime while the execution location and implementation stack remain undecided.

High-value candidate patterns: one lifecycle owner; distinguish child/process outcome from wrapper/coordinator failure; explicit capabilities and fail-closed behavior; timeout/cancellation only when confirmed by the execution boundary; persist completed steps before continuing; inspect uncertain side effects rather than blindly replaying them; fixed-whitelist diagnostics with explicit missing evidence; per-backend capability matrices; bounded retry for known transient errors; and exact upstream revision/license/dependency tracking. The fixed-task worksheet now has proposed adversarial cases derived from these patterns. These are design/test additions, not approved changes to the execution contract or PR #2/#3.

No third-party code was copied, no competitor was run, and no implementation/test/security claim was validated. PR #2 and PR #3 remain protected and unchanged. Ahead/behind counts are snapshots and must be refreshed before consequential work.
