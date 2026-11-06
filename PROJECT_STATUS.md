# PocketCode Project Status

**Status:** Discovery and product definition  
**Project name:** PocketCode is provisional; brand and repository naming are not validated.  
**Repository:** https://github.com/marcelosofficial-ctrl/PocketCode-

**Phone-only coordination:** [Continuity Hub](AI_COLLAB/POCKETCODE_CONTINUITY_HUB_20261028.md) and [four-month master plan](AI_COLLAB/FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) organize current remote research and PC-return preparation. They do not replace product/security requirements or authorize implementation, provider use, spend, merge, or deployment.

## Mission

Help people build, execute, inspect, and improve software from a phone, including when they do not have access to a computer.

## Current product hypothesis

A mobile-first, provider-neutral workspace could make AI-generated code genuinely useful by letting users run it in an appropriate environment, inspect real execution evidence, and carry that evidence into any AI assistant for debugging and iteration. This is a hypothesis to validate, not a proven market advantage.


## Expanded phone-first task direction

The owner described two real situations where a phone AI requested PC-style execution: running Python for a photo-to-Polaroid project while at an airport, and an assistant assuming the user was on PC. These anecdotes motivate a broader hypothesis: help people complete safe technical tasks from their phone when an AI assistant would otherwise require a computer. They do not establish frequency or market demand.

Added [PRODUCT/MOBILE_TECHNICAL_TASKS.md](PRODUCT/MOBILE_TECHNICAL_TASKS.md) to map possible jobs (script execution, file conversion, structured-data validation, tests, artifact generation, and more advanced remote-PC tasks) and to keep risky/high-complexity capabilities out of the first MVP. Immediate focus remains one real, bounded script workflow and a trustworthy copyable result report. RevDev and PocketCode are intended to converge into one coherent PC-and-phone product/program; that product direction is settled, while integration topology, accounts, synchronized storage, provider choice, and repository migration remain undecided and approval-gated. Budget remains $0, and no runtime or account was created.

## Execution-loop acceptance plan

Reviewed the owner-provided RevDev handoff as design evidence, not proof that every described feature is present or verified in the Windows product. The transferable lesson is the full AI → guarded execution → structured per-check report → AI correction loop. Added [PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md](PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) with verdict semantics, 14 acceptance criteria, adversarial/failure scenarios, and a staged automation ladder. It explicitly separates script-reported checks from execution-service evidence and treats automatic cross-app capture as unproven. This is planning only: no runner, provider, account, live workload, or automation integration was added or tested.

## Current phase

Discovery, competitive research, and MVP definition. No production architecture, runtime provider, monetization model, or public brand commitment has been approved.

## Working MVP direction

- Mobile-first responsive web application/PWA as the first testable interface.
- Execution location is undecided. Compare local on-device Python, browser-local Pyodide/WASM, a user-owned remote PC, hosted execution, and manual copy/paste on the same bounded task before selecting an architecture.
- Paste or upload code and supporting files.
- Run with explicit timeout and cancellation behavior.
- Show stdout, stderr, exit status, and generated files where supported.
- Preserve a small, understandable execution history.
- Make actual execution evidence easy to copy/share with any AI provider.
- No mandatory AI-provider lock-in.

## Budget and workflow policy

- **Budget: $0 unless the owner explicitly changes it.** No paid trials, payment methods, billing enablement, purchases, or potentially billable workloads without explicit approval.
- Free credits are not a guarantee of zero cost. Do not create provider accounts or run live workloads just to explore.
- Conserve GitHub Actions minutes; documentation-only edits should not trigger deployments.
- Current priority is public desk research, small improvements to the simulated prototype, and local/source-level checks—not recruiting interviews or backend implementation.
- See the [zero-budget work plan](PRODUCT/ZERO_BUDGET_WORK_PLAN.md) and accepted [D-005](DECISIONS.md).

## Guardrails

- Do not claim code execution works until an actual execution path and tests demonstrate it.
- Treat submitted code as untrusted.
- Never put credentials, API keys, tokens, private user data, or production secrets in this public repository.
- Do not execute untrusted code directly on the application server or developer workstation.
- Avoid promising every language or unrestricted OS access.
- No paid infrastructure, external service commitments, or irreversible actions without explicit owner approval.
- Keep assumptions separate from verified facts.
- RevDev and PocketCode are intended to converge into one coherent PC-and-phone product/program. Keep repositories, roadmaps, implementations, acceptance suites, evidence, and release gates separately managed during discovery and development; this does not authorize a merge, shared-code migration, shared runtime, or execution/security-boundary change.

## Immediate next steps

The active queue and copy-ready review prompts are in [POCKETCODE_CURRENT_CHECKPOINT_20261028.md](AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md). The full dated evidence handoff is [CHAT_HANDOFF_ADDENDUM_20261101.md](AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md). Do not restart completed resource/teardown research unless official sources or pinned contracts change.

1. Obtain Claude's source-backed review of the exact updated resource review, lifecycle regression plan and readiness backlog. Treat any inaccessible file as NOT REVIEWED.
2. Obtain Gemini's exact alternative artifact pins for its mismatched AWC labels, or a corrected response with those labels removed. Preserve the original RevDev AWC fixture IDs and PocketCode helper OBS register.
3. Continue the existing fixed-task comparison and product-hypothesis validation across local iPhone, browser/WASM, user-owned remote PC, hosted and manual AI paths. Use public desk research only until hands-on access and owner-approved test conditions exist.
4. Prepare the PC-return checklist and safe offline verification sequence. Keep source/implementation tests, PRs, provider selection, accounts, workloads, billing, host operations, Actions, merge and deployment closed.
## Progress log

- 2026-11-01 follow-up: Traced the portable receipt hypothesis to the existing proposed LOOP-07/08 report contract in `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and `PRODUCT/EXECUTION_CONTRACT.md`, plus the proposed adapter envelope. Updated the product-path desk review Section 9 to reuse that existing report projection rather than invent a parallel schema. Paired experiment now compares raw evidence with the exact same facts rendered through the proposed report; no diagnosis added, no facts dropped, no new acceptance IDs or schema changes. Design-only; NOT RUN.

- 2026-11-01: Added `AI_COLLAB/PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md` (blob `2592cafe479faed5059357074b5e7cbd80fc22ae`). Source-reviewed current Pyodios/iOS local Python behavior, Safari OPFS vs Pyodide native filesystem mounting, iOS background execution constraints, AndroidHarness/PhoneCode/Atlan, Kodo, Codeg, Pairlet and Codespaces. Main decision: no provider/general runner selection; next discriminating research is paired raw-evidence vs portable-receipt correction experiment with identical facts and no extra diagnosis. All product paths and paired test remain NOT RUN; no apps, accounts, provider workloads, implementation, PRs, Actions or spending. Budget $0.

- 2026-11-01 follow-up: Verified Firecracker's current API schema directly. Its serial token-bucket limiter is optional and absent by default; when enabled, over-rate guest writes are dropped and counted in `uart.rate_limiter_dropped_bytes`. Tightened RES-10/PC-EXT-09 and WP-08 to require effective-config verification, dropped-byte telemetry and independently bounded VMM log sinks. Updated source pins are recorded in CHAT_HANDOFF_ADDENDUM_20261101.md §20. Still documentation-only; no tests, host/provider calls or workloads.

- 2026-11-01: Completed a source-backed resource-containment and provider-teardown research pass on the isolated research branch. Added supplementary RES-10 (Firecracker host-side VMM/log sink pressure) and PC-EXT-08/09 (provider API-generation/resource-scope reconciliation and host-side VMM/log containment); refined Cloudflare current 1.0 versus legacy SDK 0.x lifecycle semantics, Modal async create/detach/terminate distinctions, cgroup process-migration constraints, and TDN attached-resource inventory. Reconciled Claude's canonical-gap challenges and verified Gemini's AWC identifier mismatch against the pinned RevDev fixture manifest. Updated resource review, lifecycle regression plan, provider research, WP-08 backlog, handoff and current checkpoint. All new cases are SPECIFIED ONLY / NOT RUN; no canonical LOOP/CASE IDs, source/tests, PRs, provider, runtime, account, billing, host, queue, Actions, merge or deployment changed. Provider selection NONE; WP-08 BLOCKED; budget $0; PC state UNKNOWN.

- 2026-10-28: Reconciled the status/spec/architecture wording with the phone-only hypothesis. Execution location remains undecided while local phone, browser/WASM, remote-PC, hosted and manual alternatives are compared on one task. Reorganized the AI continuity hub and start-here route, added dated gates to the existing four-month plan, refreshed the new-chat handoff/checkpoint, labelled hosted/remote architecture as one candidate rather than the only shape, and removed a duplicated RevDev compatibility section in PRODUCT_SPEC.md. Documentation-only work on the isolated research branch; no execution/provider tests, implementation, deployment, Actions run, merge or spend occurred.


- 2026-10-23: Expanded `PRODUCT/EXECUTION_CONTRACT.md` with a versioned, plain-text copyable report example, explicit provenance labels for runner evidence versus script-reported checks, honest handling of unknown values and truncation, and 10 report-formatting checks. The sample is marked illustrative, not a real run. Design-only change; no runtime, provider, live workload, paid service, or Actions workflow was used.


- 2026-10-20: Owner chose public online evidence instead of recruiting interview participants. Added `RESEARCH/MOBILE_CODING_USER_EVIDENCE.md` with a balanced preliminary review of firsthand forum posts, community feature requests, and app reviews, including positive experiences, existing alternatives, and limitations. Updated README, zero-budget work plan, and project status so desk research is the default and interviews are optional. No interviews or accounts were used, no paid services were used, and no GitHub Actions workflow was triggered.


- 2026-10-20: Made the user-validation script easier to use from a phone by adding a neutral copy/paste recruiting invitation and a six-step session checklist. This lowers the effort to start no-cost discovery without leading participants. No interviews were conducted, no user data was collected, and no Actions workflow was triggered.


- 2026-10-20: Owner confirmed a zero-spend constraint. Added `PRODUCT/ZERO_BUDGET_WORK_PLAN.md`, recorded accepted decision D-005, and linked the plan from the README. Work is now explicitly prioritized toward user validation, the static prototype, and local/source-level checks; no provider accounts, live workloads, paid services, or Actions runs were initiated by this documentation update.


- Repository created by owner and made public.
- Initial README exists; its current wording is temporary.
- Initial product hypothesis and working documents established.
- Added a working vibe-coding marketing/positioning hypothesis and updated the README headline; positioning is not customer-validated.
- 2026-10-20: Reviewed the architectural specification pasted by the owner from Gemini. Added [AI_COLLAB/CHATGPT_REVIEW_OF_GEMINI_PLAN.md](AI_COLLAB/CHATGPT_REVIEW_OF_GEMINI_PLAN.md) with an independent desk review, a scoped MVP recommendation, provider/cost caveats, security launch gates, and proposed test IDs. This is not a provider selection or implementation proof; no code, paid workload, customer interview, benchmark, or live security test was run. The pasted Gemini specification has not been verified as a canonical repository update.

- 2026-10-20: Added [AI_COLLAB/MVP_DECISION_BRIEF.md](AI_COLLAB/MVP_DECISION_BRIEF.md), a sourced desk-research shortlist for Cloudflare Sandbox Containers, Modal Sandboxes, and Daytona Sandboxes, plus provider gates, a narrow vertical slice, proposed test IDs, and implementation sequencing. No provider selected and no live test performed.

- 2026-10-20: Added [PRODUCT/EXECUTION_CONTRACT.md](PRODUCT/EXECUTION_CONTRACT.md) defining a proposed provider-neutral run lifecycle, request/result fields, idempotency, cancellation, file safety, egress/security expectations, report format, and 14 proposed API acceptance tests. This is design documentation only; no API is implemented.

- 2026-10-20: Added a self-contained mobile UI prototype at `prototypes/mobile-runner/index.html`. It is responsive and offers sample success/error states; all output is simulated, and no backend or code execution is implemented. Browser interaction tests have not yet been run.

- 2026-10-20: Added `.github/workflows/preview-prototype.yml` to publish only the static prototype folder via GitHub Pages and `prototypes/mobile-runner/README.md` with phone review instructions. The initial workflow failed until the owner enabled Pages for GitHub Actions; the subsequent deployment succeeded. Live preview: https://marcelosofficial-ctrl.github.io/PocketCode-/. No backend or code execution was added.

- 2026-10-20: Owner reviewed the prototype and found the controls unclear. Simplified the UI by removing Reset, renaming sample-state actions, and explaining the difference between copying a report and copying a debugging prompt. Latest UI update is committed and the static preview deployment succeeded at https://marcelosofficial-ctrl.github.io/PocketCode-/. Browser interaction checks have not been run by the project team.
- 2026-10-20: Updated `AI_COLLAB/MVP_DECISION_BRIEF.md` with current official provider pricing and egress defaults. Cloudflare Containers currently requires the Workers Paid plan; Modal advertises monthly compute credit, while public outbound access is allowed by default unless blocked/allowlisted. This remains desk research only; no provider selected, account created, or workload run.

- 2026-10-20: Refined the provider comparison with a conditional first-proof recommendation: evaluate Modal Sandbox first because its SDK documents an explicit `block_network=True` control and its Starter plan advertises compute credit that applies to Sandboxes; retain Cloudflare as fallback, noting the $5/month Workers Paid minimum for Containers. Added an illustrative rate calculation with explicit exclusions. This is not a provider selection; no account, credentials, live run, or charges are authorized.

- 2026-10-20: Added `PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md` with synthetic fixtures, expected outcomes, evidence template, and safety gates for a future provider test. It is a plan only; no test was run and no provider account or billing was enabled.

- 2026-10-20: Improved the prototype's debugging-prompt handoff: it now copies the user's current editor contents and the sample CSV alongside the explicitly simulated report, rather than omitting the code being debugged. Static consistency checks found no duplicate HTML IDs or unresolved `getElementById` references, and confirmed all six UI actions have handlers. These were source-level checks only; no browser interaction test has been run. GitHub Actions deployment for the prototype update completed successfully (workflow run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/39430438169).

- 2026-10-20: Added dependency-free source regression checks in `scripts/check_mobile_prototype.py` and wired them into the Pages workflow before deployment. The check verifies unique HTML IDs, resolvable `getElementById` references, six expected click handlers, simulation disclaimers, and that the debugging prompt includes editor code, sample CSV, and report. The GitHub Actions run triggered by this change is the authoritative result; these checks do not test browser interactions or execute submitted code.

- 2026-10-20: Reviewed the new regression-check logic and corrected its click-handler matcher to recognize the prototype's cached `codeTab`/`csvTab` element references as well as direct lookups. Confirmed GitHub Actions run https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/39431175201 completed successfully, including the static-check step and Pages deployment. This verifies the source checks and deployment only; no browser interaction test or real code execution/security test has been performed.

- 2026-10-20: Added five automated unit tests for the prototype source checker, covering valid cached/direct click handlers, duplicate IDs, missing referenced IDs, missing simulation disclaimers, and a debugging prompt that omits the sample CSV. The first CI run caught a case-sensitive assertion mismatch in the test itself; that assertion was corrected. GitHub Actions run https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/39432249569 then completed successfully: all five unit tests, the actual prototype source check, and the static Pages deployment passed. This is still not a browser interaction test and does not execute submitted Python.
- 2026-10-20: Cleaned up duplicate prototype links in `README.md` and linked the checker and its regression tests. No backend, provider account, live code execution, or paid infrastructure was added.

- 2026-10-20: Expanded `scripts/check_mobile_prototype.py` with lightweight mobile/accessibility source heuristics: responsive viewport metadata, one primary heading, accessible labels for textareas, detectable button names, tab roles/selection state, and a live status/output region. Added a regression test for unlabeled textareas and adjusted the duplicate-ID fixture to match the updated accessible tab markup. Latest GitHub Actions run https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/39432719962 succeeded: all six checker unit tests passed, the actual prototype source check passed, and Pages deployment succeeded. These heuristics are not a full accessibility audit and do not replace keyboard/screen-reader/browser testing; no submitted code is executed.

- 2026-10-20: Reduced avoidable GitHub Actions runs: the Pages preview workflow now triggers on prototype HTML changes or workflow changes, not checker/test-script-only edits. The unit tests and static source checker still run before each preview deployment, and manual dispatch remains available. This deliberately trades immediate CI feedback for checker-only edits to conserve the owner's Actions-minute budget; run the Python checks locally when possible and use a preview deployment when the actual prototype changes.

- 2026-10-20: Added `PRODUCT/USER_VALIDATION_SCRIPT.md` with a 10–15 minute, behavior-first interview flow, non-identifying notes template, and directional continue/narrow/pause criteria. Linked it from the README. This is preparation only; no user interviews or customer validation have occurred. No Actions workflow was triggered because the changes do not touch the prototype HTML or workflow.

- 2026-10-23: Added `scripts/report_contract.py` and `scripts/test_report_contract.py` as dependency-free, pure report-contract helpers and unit tests. The helper classifies verdicts only from supplied execution status/exit-code evidence, marks simulated reports explicitly, distinguishes empty from unavailable output, labels check provenance, bounds report content, and escapes control characters in user-provided text. Ran the 12 unit tests locally in a temporary workspace; all passed. These tests cover formatting/verdict rules only: no submitted code, runner, provider, live workload, backend, or GitHub Actions workflow was used. The helper is not a source of trusted execution evidence and is not integrated into the static prototype.

- 2026-10-28: Added [AI_COLLAB/MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md](AI_COLLAB/MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md) as the focused master reference for three research passes on Ponytail-style workflow optimization, provider-neutral phone handoffs, persistent instructions, free-tier usage efficiency, and RevDev/PocketCode convergence. Added feature-hypothesis pointers to PRODUCT_SPEC.md, ROADMAP.md and README.md. This is documentation/research only: no AI API, provider account, workload, spend, implementation, test run, merge or deployment. Work is on the isolated branch pocketcode-ai-workflow-director-research-2026-10-28; PR #2 and PR #3 remain untouched.

## 2026-11-01 Gemini open-source research review and decisions

## 2026-11-01 Gemini open-source research review and decisions

Reviewed the owner-supplied Gemini open-source reuse report against targeted current upstream documentation/source and existing PocketCode contracts. The full verdict and source links are in [AI_COLLAB/GEMINI_OPEN_SOURCE_RESEARCH_REVIEW_20261101.md](AI_COLLAB/GEMINI_OPEN_SOURCE_RESEARCH_REVIEW_20261101.md).

The report is a useful candidate catalogue, not an approved architecture. No technology or provider is selected. PocketCode and RevDev remain distinct systems with separate runtime, security and acceptance boundaries; future protocol compatibility is possible, but no unified graph/runtime design is approved. CodeMirror 6 and Pyodide remain browser-path candidates, wasmsh and Aider repo-map remain investigation/pattern candidates, while LangGraph, tsnet/AsyncSSH, Piston hosted, Watchdog, FlaUI and archived OpenHands ACI are deferred or rejected for the reasons in the review. Judge0 GPL-3.0 is not an automatic blanket source-disclosure trigger.

The next work is to await Claude's independent research, reconcile candidate claims against pinned upstream sources, and continue the fixed-task comparison design. No code, tests, PRs, Actions, accounts, provider workloads, spending, merge or deployment. Budget $0; PC/source/runtime/queue state remains UNKNOWN.

## 2026-11-01 follow-up: pinned open-source candidate review

Added [AI_COLLAB/OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md](AI_COLLAB/OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md) with exact upstream commit/blob pins and source-level constraints for CodeMirror 6, Pyodide, wasmsh and Aider repo-map. Key correction: CodeMirror 6's GitHub repositories were archived because development moved to a new Forgejo host; npm `@codemirror/view@6.43.15` remains active, but current source commit was not fetched. Pyodide remains a candidate for the fixed task, not a general security boundary. wasmsh is not a full OS shell and its zero-valued limits are unlimited. Aider's repo-map is coupled to Aider internals, so the concept is preferable to importing the module. No candidate has been adopted or run.

## 2026-11-01 fixed-task protocol hardening

Updated `AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md` with a canonical, frozen `main.py` source fixture. This closes a comparability gap: every execution path must now run the same source unchanged or explicitly record its adaptation/wrapper. The fixture validates input before writing output and defines exact success and malformed-header behavior. Design-only; not run or device-tested.

The canonical fixed-task source fixture received an isolated logic sanity check in ChatGPT's Python 3.13.5/Linux environment: expected success output and malformed-header failure behavior matched; see worksheet Section 2B. This is not a product-path test and does not change NOT RUN status for mobile/browser/remote/hosted comparison.

## 2026-11-01 new-chat transfer package

Created `AI_COLLAB/NEW_CHAT_BOOTSTRAP_20261101.md` as the primary comprehensive continuation handoff, including a full copy/paste prompt. It carries forward PocketCode and RevDev goals, three-AI roles, constraints, Claude's expected medium-sized report and evaluation rules, Gemini's adjudicated findings, fixed-task state, acceptance/crosswalk rules and next actions. Claude's recommendations are to be treated as valuable evidence and proposals, not as authority to overwrite the product goals or owner decisions. See the handoff addendum for final repository state.


- 2026-11-03 Linux strict-service boundary audit: Added Section 11 to [RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md](AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md), commit `6683d7d8b1ef1da83b178afcd459015b248967ab`, resulting blob `edafc4eb0b9815d2f23bea8326ea98449d411b56`. Pinned source review of Happy Agent Linux service confirms useful patterns (private filesystem, explicit environment, scoped cgroups, network-off policy, process reconciliation) but finds no trusted wall-clock deadline or CPU quota, incomplete storage/input constraints, special-file and scratch-overlap gaps, egress-on IP/L7 policy gaps, and an unchecked parent-death race in the egress child. Decision: retain it as a Linux reference only, not a PocketCode dependency/provider/selected architecture. No implementation, tests, Actions, provider workload, account, billing, PR, merge or deployment. Canonical LOOP/CASE unchanged; runtime/provider NONE; budget $0; local PC state UNKNOWN.


- 2026-11-03 iOS browser-runtime revalidation: Added Section 10 to [PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md](AI_COLLAB/PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md), commit `7572aa432052615956293637e0bd0bae06fa8934`, resulting blob `01f8b1f2b08caab56fc4b6b4977893aa70d81693`. Current official Pyodide stable remains 314.0.7; 315.0.0-alpha.2 is prerelease. Core-only delivery is the better fixed-task hypothesis than assuming the 200+ MB full distribution, but its device payload/startup is not measured. Pyodide's SharedArrayBuffer interrupt is cooperative and separate from Worker.terminate. WebKit bug 289686 is fixed in WebKit main and listed in Safari Technology Preview 252, but public stable iOS 27.2 release notes do not establish that exact fix shipped. Added a concrete Safari/PWA stop, lifecycle, storage and resource-pressure test matrix. No device test, runtime selection, package install, workload or provider use. All product-path execution remains NOT RUN.


- 2026-11-03 cross-origin browser boundary specification: Expanded [PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md](AI_COLLAB/PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md), commit `9274cc11c85c20f39d9cfc2bbe8172a0fbd7af28`, then source-list and review corrections commit `36c105ed532c166b85029f71550871a50dcd5175`, final blob `9e8b0c6b430cf11b9ecf5cbc474cf675b38702c2`. Added a proposed authenticated-app → cross-origin static-only iframe → module-worker topology; illustrative iframe/worker CSP; exact origin/cookie/API restrictions; run/attempt/nonce/sequence-bound MessageChannel; Pyodide 314.0.7 jsglobals minimization experiment; storage and message-flood controls; BR-01..BR-12 research threat cases; and a narrow browser proof order. The proposal explicitly is not a verified sandbox and does not establish CPU/memory quotas or hostile-code containment. Primary-source references added. No code, tests, runtime or canonical acceptance changed.
- 2026-11-03 WP-09 browser-local proof plan: Added [WP-09 — Browser-local execution boundary proof](AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md), commit `ef73190781eb41e91cc6a77faf6575f143f423e5`, final blob `57c784532357b909e46f9050f9e72a49ca8e4960`. WP-09 is separate from hosted/provider WP-08; it is research specified, not implemented or run. It does not authorize a provider, account, install, Actions, device test, source/test change, PR change, merge or deployment. Physical iOS/PWA proof remains NOT RUN; runtime/provider NONE; budget $0.


- 2026-11-03 Pyodide Python-visible API audit: Expanded [PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md](AI_COLLAB/PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md), commit `e8623d9a1c2435693a68c7ea35a410d5521be81b`, and added BR-05/06/13 threat cases in commit `6b7bf589d6dd72120b53b6b46d28fb2cec710d80`, final blob `329cfe82d4281824c3e910e351e516d8b35049e6`. Pinned Pyodide 314.0.7 source confirms jsglobals only scopes the Python js module; Pyodide also registers pyodide_js backed by its public API object, exposing FS, _module and _api. FS documents persistent IDBFS. pyodide.code.run_js delegates to JavaScript eval through the js module. The Pyodide 314.0.7 test suite marks restrictive-CSP test as xfail on Safari because Safari does not support wasm-unsafe-eval. Therefore an empty jsglobals object is insufficient; complete Python-visible API attenuation and Safari CSP behavior are hard gates. WP-09 updated accordingly in commit `19e0e42a03c16aa73fa4e0b397db33183eb91361`, final blob `5da5cb0b71c229c8e874785b337e0b246b36b8fc`. This remains source-inspected only: no Pyodide runtime or device tests were executed. No implementation, runtime/provider selection, canonical acceptance change, PR change, workflow, install, account, billing or workload.


- 2026-11-03 Pyodide trusted-bootstrap feasibility refinement: Added Section 10.11.1 to the browser desk review, commit `a69b4d55848ac00d7b637cc48d9b41af9f53e86b`, pinned additional 314.0.7 import-hook/Python module sources in commit `a591357e5b33be54a62f198b4f6b8f4593a4da82`, and accounted for the package-loader cached JS proxy in commit `a7ed283ecbcbe932078c301d630b8017e709a220`, final desk-review blob `ae0c5d5a4b4e0c7edae39c53fc9118fa70aee493`. Source review confirms a possible attenuation experiment: unregister pyodide_js from the import hook, clear cached pyodide_js modules, restrict jsglobals, and audit pyodide.code.run_js; however pyodide._package_loader imports a JS-backed loadedPackages proxy during bootstrap, so that cached reference must also be handled. Pyodide webloop and HTTP helpers depend on pyodide_js, so async/network functionality may be unavailable in the first proof. This is a source-derived hypothesis only, not a verified mitigation. WP-09 updated with the cached-proxy caveat, commit `ef5929ec67b41906c2756984302c724429199ec2`, final blob `5041cafde16fbd07a87c87f93ee5d9caf6a0b8a5`. No runtime or tests executed.


## 2026-11-03 primary continuation handoff

The current primary new-chat transfer document is [AI_COLLAB/NEW_CHAT_HANDOFF_20261103.md](AI_COLLAB/NEW_CHAT_HANDOFF_20261103.md). It supersedes the 2026-11-01 bootstrap's live-state snapshot, while retaining that bootstrap and the long addendum as historical context. The new handoff includes a self-contained copy/paste prompt, current product direction, three-AI roles, phone-only/$0 constraints, PocketCode canonical acceptance and owner-open decisions, fixed-task/paired experiment state, Claude/Gemini research adjudication, current Linux and Pyodide source findings, RevDev/RelayRef/P8U continuity, protected PR state, exact next passes and no-go boundaries.

Handoff file creation commit: `7ee551b698616d030e1651c2189bb21ef92c759c`; verified blob after read-back: `cd223994ce689a83469070e48e82c4a909cfbd7b`.

Latest verified branch state before this status-pointer update: `c0514044707b6a440bed2f7a7f758bdbf6500d14`, 546 ahead / 0 behind main `555840d8d83342513d9cd353d4d1522d46a5c82d`. PR #2 and #3 remained open, draft and unmerged at their protected heads; re-fetch before consequential work. This status-pointer update is documentation-only on the existing research branch.

Latest work conclusions:
- Happy Agent Linux strict-service remains a source-level reference only, not a selected provider/dependency; absolute deadline, CPU/disk quotas and input/egress/lifecycle gaps remain.
- Happy Agent Windows adapter is not acceptable as-is for untrusted code due broad root read and inherited environment.
- Pyodide 314.0.7 empty `jsglobals` is insufficient because `pyodide_js`, FS/IDBFS, `_module`, `_api`, `run_js`, cached module/proxy references and Safari CSP limitations remain. A trusted-bootstrap attenuation experiment is only a hypothesis, not verified.
- Browser/Pyodide and Linux paths remain unselected; product-path execution and device tests NOT RUN; budget $0.
- No source, tests, canonical acceptance, PR, Actions, provider, account, workload, installation, merge, deployment or local PC state changed.


## 2026-11-03 final handoff verification

After creating the handoff and adding this status pointer, the research branch was re-fetched and compared again:
- Immediately before this verification append, branch head: `f58437b177e883f32bb002cccf662a86121dc584`.
- Ahead/behind: **548 ahead / 0 behind** main `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- Handoff file read-back blob: `cd223994ce689a83469070e48e82c4a909cfbd7b`; 442 lines; includes the complete copy/paste prompt.
- Status pointer read-back blob before this append: `5c6abae101c32222ea80908718b40a42b8c7ac46`.
- PR #2 and #3 were re-fetched after handoff creation; both remain OPEN, DRAFT, UNMERGED. Their protected head SHAs remain `eb8b7ea83cb0e8fe1880351276c485b761431791` and `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- This is a documentation-only status append. No PR, source/test, canonical acceptance, Action/workflow, provider, account, workload, host, queue, installation, merge, deployment or spend changed.


## 2026-11-03 Pyodide attenuation decision and lifecycle crosswalk

Research addendum: [PYODIDE_ATTENUATION_EXECUTION_BOUNDARY_AND_LIFECYCLE_MATRIX_20261103.md](AI_COLLAB/PYODIDE_ATTENUATION_EXECUTION_BOUNDARY_AND_LIFECYCLE_MATRIX_20261103.md).

- Completed pinned Pyodide 314.0.7 source audit of import-hook unregister behavior, FFI re-registration, package-loader and webloop JS proxy references, state snapshots, to_js/JsProxy, and Safari CSP.
- Decision: reject the trusted-bootstrap attenuation experiment as a maintainable no-fork hostile-code sandbox. Keep Pyodide only as a possible trusted/small-task convenience comparator. The fixed synchronous standard-library fixture does not inherently require JS/network/async APIs, but post-attenuation operation remains untested.
- Exact source shows unregister removes the import-finder registration but not cached imports; package_loader retains loadedPackages; webloop retains scheduleCallback; FFI exposes module registration; _state admits there is no general way to track all module global state. Pyodide 314.0.7 marks restrictive CSP expected-fail on Safari because wasm-unsafe-eval is unsupported.
- Completed comparison of browser Pyodide, isolated Linux service reference, future user-owned remote PC, and manual copy/paste against LOOP-01..14 and CASE-01..16.
- Added nine-stage lifecycle/evidence matrix: user intent, policy, authorization, reservation/dispatch, execution, result/disposition, cleanup, artifact release, and report publication. Unknown states and D-01..D-08 remain intact. No canonical IDs or acceptance meanings changed.
- No runtime/device/security test, provider workload, implementation, Actions, PR, account, spend, host, queue, or local PC state changed. Fixed-task product comparison and paired AI correction experiment remain NOT RUN; differentiator UNVALIDATED.


## 2026-11-03 continuation read-back verification

- Companion audit: [PYODIDE_ATTENUATION_EXECUTION_BOUNDARY_AND_LIFECYCLE_MATRIX_20261103.md](AI_COLLAB/PYODIDE_ATTENUATION_EXECUTION_BOUNDARY_AND_LIFECYCLE_MATRIX_20261103.md), blob SHA 016b5e5145aa891a6503be58b29f2fa9bebe96c7, 179 lines.
- Updated primary handoff: [NEW_CHAT_HANDOFF_20261103.md](AI_COLLAB/NEW_CHAT_HANDOFF_20261103.md), blob SHA 357600e42dd3649e006c83e7fcc659df92a2591e, 485 lines.
- Before this status read-back pointer commit, research branch head df495036cfb045a58b68eaa5989cffb2f48118e3; comparison to main: 552 ahead / 0 behind. Main remains 555840d8d83342513d9cd353d4d1522d46a5c82d.
- PR #2 remains OPEN/DRAFT/UNMERGED at eb8b7ea83cb0e8fe1880351276c485b761431791. PR #3 remains OPEN/DRAFT/UNMERGED at 0ddcc0bc97bac5d446aefedf3d71f99411bd841d. Both re-fetched after the documentation commits and left untouched.
- This continuation's changes are documentation-only commits on the authorized research branch. No source/tests, canonical acceptance, PRs, Actions, provider, account, workload, spend, host, queue, runtime, install, deployment or merge changed.


## 2026-11-03 final continuation and PC-return read-back

- Pyodide / boundary / lifecycle audit blob: 016b5e5145aa891a6503be58b29f2fa9bebe96c7 (179 lines).
- Primary handoff blob after continuation addenda: 7a8522363ac18d73597bcea8b41dd868979c6074 (492 lines).
- PC-return checklist blob after refresh: 6bfa59becb1992bb02ae46500673c85f3aa858a7 (211 lines).
- Immediately before this final status pointer, branch head 7319e3e4c28aecf1f88c68447b31d30c584f5390; 555 ahead / 0 behind main 555840d8d83342513d9cd353d4d1522d46a5c82d.
- PR #2 and #3 remain OPEN/DRAFT/UNMERGED at their previously verified head SHAs eb8b7ea83cb0e8fe1880351276c485b761431791 and 0ddcc0bc97bac5d446aefedf3d71f99411bd841d. Both remain untouched.
- The PC-return checklist is still a draft plan. Current PC/source/runtime/binary/queue state remains UNKNOWN. No local tests, builds, installs, host changes, or execution tests were performed.
- All updates in this continuation are documentation-only on the authorized research branch. No source/tests, canonical acceptance, PR, Actions, provider, account, workload, spend, host, queue, runtime, install, deployment or merge changed.


## 2026-11-03 branch-pointer reconciliation

The owner-designated PocketCode research branch for this continuation is pocketcode-ai-workflow-director-research-2026-10-28. Its live comparison was 556 ahead / 0 behind main 555840d8d83342513d9cd353d4d1522d46a5c82d. PR #2 and #3 remain OPEN / DRAFT / UNMERGED at their unchanged protected heads eb8b7ea83cb0e8fe1880351276c485b761431791 and 0ddcc0bc97bac5d446aefedf3d71f99411bd841d.

A separate RevDev handoff references pocketcode-execution-boundary-crosswalk-2026-11-01 at a previously reported 602-ahead snapshot. This is a different branch. Do not silently switch, merge, copy branch-specific files or conflate blob IDs. Continue on the branch explicitly designated by the owner unless clarified.


## 2026-11-03 static mobile-prototype UX/evidence audit

Read-only review: [MOBILE_RUNNER_PROTOTYPE_STATIC_UX_EVIDENCE_AUDIT_20261103.md](AI_COLLAB/MOBILE_RUNNER_PROTOTYPE_STATIC_UX_EVIDENCE_AUDIT_20261103.md), blob 4e5679dccd041bdae55a05b22e51a0d5bd668f58.

Reviewed prototype source blob e2c4ece041be95ce9a73bc60ff354702b21c33c2. The current page is an honest simulated UX sketch, but it is not yet a representative demonstration of the primary product hypothesis:
- the sample sales-CSV-to-summary task differs from the frozen CSV-to-JSON comparison task;
- the copied report omits separate stdout/stderr capture states and explicit artifact state, and hides the sample failure artifact card without stating artifact status in the copied report;
- the CSV panel is hard-coded sample text, not a user file-import flow;
- timeout/cancellation controls and their distinct states are absent;
- tab/panel ARIA relationships and keyboard navigation are incomplete;
- clipboard behavior remains browser-dependent and unverified.

Recommendation: align the demo task with the frozen fixture (or clearly label it as a separate example), make the copied receipt truthful about execution and artifact state, and then add actual input-intake and timeout/cancellation UI only when their behavior can be implemented and tested. No source/test changes or browser/device tests were made. The prototype remains simulated; execution and differentiator remain unvalidated.


## 2026-11-03 live branch and cross-project reconciliation

Fresh comparison of the owner-designated branch \`pocketcode-ai-workflow-director-research-2026-10-28\` now reports **561 ahead / 0 behind** main, merge base \`555840d8d83342513d9cd353d4d1522d46a5c82d\`. This supersedes earlier same-day 555/556 snapshots in this file. The count is branch divergence, not merge readiness.

PR #2 remains OPEN / DRAFT / UNMERGED at unchanged head \`eb8b7ea83cb0e8fe1880351276c485b761431791\`; PR #3 remains OPEN / DRAFT / UNMERGED at unchanged head \`0ddcc0bc97bac5d446aefedf3d71f99411bd841d\`. Both were re-fetched and left untouched.

The separate RevDev branch \`review/revdev-adaptive-ai-workshare-2026-10-27\` currently compares 463 ahead / 0 behind its main (merge base \`058f9025319d12e76195659c715ccb4afce133b8\`). Keep repository and branch identities separate.

No PR, source, test, Actions, provider, account, workload, spend, host, queue, runtime, install, deployment or merge was changed. The fixed-task product-path comparison and paired AI correction experiment remain NOT RUN; differentiator remains UNVALIDATED.


## 2026-11-03 branch-count snapshot supersession

The 561-ahead PocketCode figure in the preceding addendum is superseded. The latest comparison immediately before this documentation update reported this owner-designated branch at **563 ahead / 0 behind** main, merge base \`555840d8d83342513d9cd353d4d1522d46a5c82d\`. This is a historical snapshot taken before the present continuity commits, not a live count after them. Re-fetch the branch comparison before making any decision. PR #2/#3 remain open, draft, unmerged, at their unchanged protected heads.


## 2026-11-03 mobile prototype next-pass design decision

Added [MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md](AI_COLLAB/MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md), blob \`2b2b05bd0efbd339cdef2dff14cd404bc25f168b\`.

The design reference aligns the simulated mobile prototype with the frozen CSV-to-JSON task rather than the unrelated sales-summary example. It defines truthful success and malformed-header example receipts, separate stdout/stderr sample expectation labels, job disposition, duration/runtime unknowns, artifact/cleanup/release distinctions, and existing LOOP/CASE mapping. It deliberately does not add a fake file picker, Run action, cancellation behavior, new acceptance IDs, or a runtime decision.

Decision remains design-only. The prototype remains simulated. No source/tests/browser/device/file-import/clipboard/runtime/provider/Actions/host/queue/PR changes occurred. Fixed-task product-path comparison and paired AI correction experiment remain NOT RUN; differentiator remains UNVALIDATED.


- **2026-11-03 follow-up:** Added [`AI_COLLAB/PYODIDE_314_0_7_CAPABILITY_ATTENUATION_AUDIT_20261103.md`](AI_COLLAB/PYODIDE_314_0_7_CAPABILITY_ATTENUATION_AUDIT_20261103.md), a pinned-source review of Pyodide 314.0.7's JS module registration, public API exposure, import-hook unregister behavior, cached package-loader/webloop/http JS references, `run_js` eval path, CSP fixture, worker termination, and iOS background suspension. Executive decision: stock Pyodide is not approved as a hostile-code sandbox; do not prioritize an import-scrub shim for MVP. Keep browser Pyodide only as a possible user-approved convenience path with strict origin/CSP/worker controls and explicit limitations. Isolated Linux/VM remains the research direction for arbitrary untrusted code; no provider/runtime selected. Canonical LOOP/CASE unchanged; all browser/device/adversarial tests and fixed-task product comparison remain NOT RUN.

- **2026-11-03 live GitHub refresh:** PocketCode research branch `78b0c15273ff0f66072dbb5d58a9a0f6c0c904cf`, 569 ahead / 0 behind main (merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`). RevDev research branch `675902cced5bf92a63ab73bb865834014c0e2b59`, 471 ahead / 0 behind main (merge base `058f9025319d12e76195659c715ccb4afce133b8`). PocketCode PR #2/#3 and RevDev PR #1 remain OPEN / DRAFT / UNMERGED at unchanged heads. No PR/Actions/source/test/runtime/host/queue change occurred.


- **Correction to the earlier same-day snapshot:** the 569-ahead PocketCode / 471-ahead RevDev values above were captured before the later Pyodide audit and P8U continuity commits. A fresh comparison immediately before this correction found PocketCode at 572 ahead / 0 behind (head `2d6e6c478dfa22a1e6efeeaf1e672ff2d1871be6`) and RevDev at 477 ahead / 0 behind (head `01e0858bfd8733070b7c0f78b0f62bafe1fd2649`). Both merge bases are unchanged. This is a pre-correction snapshot; the correction commit itself advances the PocketCode branch. Re-fetch before future decisions.


## 2026-11-03 iOS runner competitive baseline and product differentiation decision

Added [`AI_COLLAB/IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md`](AI_COLLAB/IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md). Public-source research checked a-Shell, Carnets, Pyto, Pythonista 3, Coilbook and Python Code Editor & IDE, plus official Python iOS and Apple sandbox documentation.

**Executive decision:** do not build a generic iPhone Python IDE/interpreter as PocketCode's differentiator. The market already advertises free/low-cost local offline Python, project/file import, notebooks, consoles, stop controls and debugging. Especially relevant:
- a-Shell's App Store listing advertises free offline local Python and Unix tools.
- Carnets advertises free local/offline Jupyter with file/directory support and sharing.
- Pyto and Pythonista advertise embedded local Python IDEs and file/automation workflows.
- Coilbook's first-party pages claim CPython 3.14, free unlimited runs, Files-app project folders, input/console and Stop. Its App Store storefront presence was not independently confirmed in this pass.
- Python Code Editor & IDE's App Store listing advertises local offline Python, debugger, pip, pytest, project import and ZIP export. The listing is recent and public ratings are sparse; all such feature claims remain unverified until hands-on use.

Official Python iOS documentation says Python must be embedded in an iOS app, not used as a system-wide Python executable. Pythonista/Pyto documentation describes same-process interpreter operation and iOS subprocess restrictions. Therefore a native embedded interpreter is useful for trusted local work, not a hostile-code OS sandbox. A Stop button does not prove process isolation or hard quotas.

PocketCode's differentiation should be the provider-neutral **task/evidence/recovery/AI-correction layer**:
1. immutable task/run packet binding exact source and input hashes;
2. explicit entrypoint/working directory and user authorization;
3. host-observed lifecycle/output evidence, exit/outcome, artifact hashes and cleanup uncertainty;
4. durable report/run history and recovery without rerunning a completed task;
5. portable AI debugging packet, explicit user-mediated handoff, patch preview/approval and attempt lineage.

The frozen CSV-to-JSON task remains a workflow benchmark, not proof of runtime advantage or sandbox security. First controlled comparison should use a-Shell plus one current native IDE (Python Code Editor & IDE if available in the owner's Belgian storefront, otherwise Pyto free tier), optionally Coilbook if store availability is confirmed. Do not install/run anything without explicit owner/device authorization. Mark capabilities advertised-but-unverified, unknown or verified; do not treat silence in marketing as absence.

No apps were installed, no tasks run, and no canonical LOOP/CASE meanings changed. Runtime/provider selection remains NONE; budget remains $0; fixed-task product comparison remains NOT RUN. Full rationale, source links, benchmark dimensions and go/no-go criteria are in the competitive baseline.


## 2026-11-05 focused remote-agent and workflow-protocol research

Added [Remote Agent Control Plane and Workflow Protocol Research](RESEARCH/REMOTE_AGENT_CONTROL_PLANE_AND_WORKFLOW_PROTOCOL_RESEARCH_20261105.md), commit `dfe5c0bae5169bfc6623adc8b211ff56dc355795`. It source-audits Happier, Cretli, agent-device and OpenWOP, including MIT/Apache license checks and selected implementation files.

Executive decision: do not pivot PocketCode into a generic remote agent control room. Happier and Cretli control agents that still require a reachable host; they do not solve the no-PC execution problem. Preserve PocketCode's run/inspect/report/iterate hypothesis and differentiate through truthful execution evidence, portable receipts, safe AI correction and attempt lineage.

Adopt as future design ideas: provider capability negotiation, same-session reconnect using durable cursors, explicit native-fork vs replay-fork choices, separate permission approvals from user questions, partial-commit reporting, request/effect idempotency separation, and witness-based conformance. Cretli's local lock/JSON persistence is not distributed coordination and its network terminal exposes a full shell. OpenWOP's own known-limits page reports no independent tier-3 host and no witnessed multi-instance/multi-region durability. agent-device may be an optional UI/device QA adapter, not a user-code runner.

No new code copied. No runtime/provider/cloud/sandbox selected; $0 default budget remains. Fixed-task comparison and AI Director evaluation remain NOT RUN. LOOP/CASE and AWD acceptance remain unchanged. PR #2/#3 untouched.

- Final live branch verification after this pass: `pocketcode-ai-workflow-director-research-2026-10-28` is **665 ahead / 0 behind** `main`. PocketCode PR #2 and #3 remain the only open PRs and were not modified. New research document read-back blob: `d63d840e8730ab2ec472889c94a5580d8da43a7b`. No code copied or executed.

- Additional OpenWOP security refinement: RFC 0229 documents a persisted secret-digest confirmation-oracle risk. PocketCode receipts, task fingerprints, caches and AI debugging packets must exclude secret values structurally, not only redact logs. The RFC's own history records provisional acceptance and a steward override of the comment-window rule; protocol status is not independent assurance. Updated research note blob: `bdc17692e25e9938bbca94d6b8be1ab0613dc196`.

## 2026-11-05 execution-readiness and competitor research checkpoint

Latest focused source audit: [Remote Execution, Event Recovery and Scheduler Competitor Audit](RESEARCH/REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md), created in commit 4728e5a6108ef187065441f706331d67a0bd4f90.

New source-backed findings:
- Cline Apache-2.0: SSH remote environment service with explicit profile/connection states, remote host inspection, SSH tunnel ownership, bounded command/transfer deadlines, output cap and pending cleanup. Useful as a future optional user-owned-PC adapter pattern, not a mobile implementation or sandbox proof.
- Cline Apache-2.0: SQLite scheduler with durable run rows, claim token/lease, renew/complete transitions, concurrency controls and tests for competing claims and stale tokens. Design/test reference only; local SQLite is not distributed coordination and leases do not make external side effects exactly-once.
- OpenHands Agent SDK MIT: caller-selected conversation ID plus capability-negotiated retry after a lost create acknowledgement. The exact test commits then drops the first response and verifies same-ID retry avoids duplicate creation. Adapt as a command-dispatch contract only if the host explicitly guarantees deduplication for the same command ID and payload.
- OpenHands event-store gaps: sequence/cursor and stable IDs are useful, but some ancestry traversal bridges missing parent files and a file-store listing error is tested as an empty log. PocketCode must never use this behavior for authoritative execution evidence; unavailable/corrupt/partial history must be distinct from truly empty history.

Executive priority reset:
1. Stop broad competitor cataloguing unless a finding changes a concrete decision.
2. Complete the smallest provider-neutral command/receipt contract and choose one execution path only after the existing fixed-task comparison.
3. Prove one vertical slice before adding schedules, SSH, multi-agent features or IDE breadth.
4. Preserve separate command outbox, remote execution, local runner, observation sync, immutable receipt and workspace checkpoint identities.
5. Keep $0 budget and all no-provider/no-host/no-live-run restrictions.

**Product progression estimate:** approximately 20% toward a dependable combined product, as a qualitative planning estimate only. Discovery, acceptance semantics and risk research are materially ahead of implementation and integration. PocketCode has a static/simulated UI prototype but no real execution backend, selected runner, real receipt or demonstrated end-to-end workflow. Therefore the first usable PocketCode MVP is not close yet. Current work is productive in definition and risk reduction, but implementation progress is blocked by the phone-only period and unselected execution path. Commit counts are not product progress.

Canonical LOOP-01..14, CASE-01..16 and D-01..D-08 unchanged. Fixed-task comparison and EVAL-06 remain NOT RUN. No product code/test, runtime, provider, account, workload, device test, Actions, deployment or PR change occurred. PR #2/#3 remain protected.


### GitHub verification correction — 2026-11-05

After the latest documentation-only continuity updates, live GitHub comparison reports the PocketCode research branch at **691 ahead / 0 behind** main, merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. The branch head immediately before the final handoff refresh was 27a89fbed6a5b1c4d3a44e5398026fc220f918d6. This count is accumulated branch history, not implementation progress. PR #2 and #3 remain OPEN / DRAFT / UNMERGED, untouched. Re-fetch before future consequential work.


- 2026-11-05: Extended the existing fixed-task comparison worksheet with Section 5D, a staged interruption/reconnect/receipt/artifact-recovery protocol. It separates natural iOS/browser interruption from remote-host reconnect and controlled product fault injection; requires inspect-before-retry, same-attempt identity, exact artifact read-back, report-to-source reconciliation, and transfer integrity. Explicitly separated this CSV execution/recovery experiment from EVAL-06 (the independent compact-checkpoint prompt-bundle comparison) and from the raw-evidence-versus-portable-report A/B. Read-back verified the worksheet update at blob `c883ccd45e78758997642861623351957c1d31a1`. This is documentation-only; all hands-on paths, interruption cases and paired experiments remain NOT RUN. No canonical fixture, LOOP/CASE ID, schema, provider/runtime choice, owner decision, source/test, PR, Action, account, workload, spend, merge or deployment changed.


## 2026-11-05 owner authorization update

The owner has superseded the earlier blanket documentation-only/no-implementation restriction across the RevDev + PocketCode programme. ChatGPT should carry out useful implementation, test authoring/execution, builds and CI work when the actual environment and target are available. Do not treat the old temporary phone-only safeguard as a permanent project limitation.

PocketCode's own product phase remains Discovery and product definition; this authorization does not select a runtime/provider, prove product demand, or justify a paid workload. The $0 default budget remains in force. Continue hosted/local source and prototype work where no-cost access is verified, and keep the product's security and execution boundaries intact. The owner's Windows PC and installed RevDev runtime remain inaccessible, so no PC parity or local runtime claim is possible.

RevDev has a separate narrow maintenance-source hardening change on its own repository/branch. See [the RevDev fail-closed publisher patch note](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/R5_MAINTENANCE_PUBLISHER_FAIL_CLOSED_PATCH_2026-11-05.md). This does not change PocketCode code, architecture, acceptance IDs or release gates.


## 2026-11-06 Pyodios device-comparison preparation

The owner reports Pyodios is already installed on the iPhone. Reconciled current official Pyodios v1.1 documentation and added `AI_COLLAB/PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md`. The protocol uses the existing frozen CSV-to-JSON source and success/malformed fixtures unchanged, with separate fresh projects, exact artifact inspection/export, normal relaunch persistence observation, and truthful evidence classification. It explicitly does not infer child exit status from UI text or treat Pyodios' documented 120-second timeout as execution termination.

Key public-source constraints now recorded: v1.1.0 advertises CPython 3.14.2 / Pyodide 314.0.5 and iOS 26+; each app launch starts a fresh Python session; project files persist but the working session is copied/synchronized at specific moments; project import may require reopen; files over 16 MB are not copied into the Python session; the FAQ states approximately 300 MB Python memory and says running code cannot currently be interrupted, with a 120-second UI timeout that leaves code running until session restart or app close/reopen. These remain DOCUMENTED CLAIMS until checked against the installed build/device. Sources: https://pyodios.caffeinatedmath.com/ ; https://pyodios.caffeinatedmath.com/faq ; https://pyodios.caffeinatedmath.com/guide/projects ; https://pyodios.caffeinatedmath.com/guide/files ; https://pyodios.caffeinatedmath.com/guide/editor .

**Status:** documentation review complete; device test AWAITING OWNER OBSERVATIONS; no device execution or app version was observed by ChatGPT. No product code/tests, canonical fixtures, LOOP/CASE IDs, schemas, runner/provider selection, PRs, Actions, merge or deployment changed. $0 budget preserved.


The owner-ready fixture archive was also generated and checked: `pocketcode_pyodios_fixed_task.zip` (2,184 bytes; SHA-256 `706c6a87d07c496d5a461c9395fb0b967b961fa9c430c719d9799998df5b4099`). Its embedded `main.py` is 1,939 bytes and SHA-256 matches the worksheet's canonical source hash `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`. Archive includes README, exact source, success CSV and malformed-input CSV. It is a convenience import package; canonical source remains the worksheet. No mobile execution was performed by ChatGPT.


## 2026-11-06 multi-chat continuity operating model

PocketCode now has a compact live chat entrypoint at `AI_COLLAB/CHAT_START_HERE.md`, an append-only work log at `AI_COLLAB/CHAT_WORK_LOG.md`, and a reusable operating protocol at `AI_COLLAB/CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md`.

This changes how long-running work is coordinated, not the product's execution/runtime status. GitHub is the durable source of truth; each chat is a replaceable worker. New chats read the live entrypoint and only the task-specific source/evidence. Meaningful passes are checkpointed every two or three passes or after any important source/test/review/decision event. Rotation occurs before context exhaustion, never after a full-chat error.

The 2026-11-06 branch compare is 710 ahead / 0 behind main, merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`; this is branch-history divergence, not implementation progress. PR #2 and #3 remain open and unchanged.

OpenAI's current Free Tier FAQ explains that context-full is based on the amount of information in the current conversation, including user and assistant messages, not a fixed message count. Free users should not assume a new chat will recall every earlier project chat. The new GitHub entrypoint therefore becomes mandatory for continuity.

Canonical LOOP/CASE/D acceptance remains unchanged. Product phase remains Discovery; no runtime/provider/runner selected; $0 default budget remains. The owner-reported Pyodios device test is still awaiting owner observations; no device execution or product acceptance was performed by this continuity update.


## 2026-11-06 — Multi-chat continuity process extension

The 2026-11-06 chat continuity system has been strengthened for months/hundreds of conversations. The current live entrypoint and protocol in `AI_COLLAB/CHAT_START_HERE.md` and `AI_COLLAB/CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md` are authoritative.

New operating requirements: checkpoint every two or three meaningful passes or after significant source/test/review/decision events; rotate before context exhaustion; keep the append-only log and entrypoint current during work; do not rely on a nearly full chat to create a giant handoff. Use one lead writer per branch/work item, parallelize independent reads, and serialize shared-branch writes. For related multi-file changes, use one Git Data API tree/commit with an expected-head ref lease and exact read-back. On tool failures, re-fetch live state, determine whether a write occurred, recover and report instead of silently stopping.

ChatGPT may lead bounded implementation when source/tools are available; Claude and Gemini remain scoped reviewers/co-developers, with the owner forwarding reports manually. This process update does not select a runtime/provider, change PocketCode implementation, redefine LOOP/CASE/D semantics, or alter its phone-first/security/$0 constraints.

RevDev-only lesson: query push-triggered Actions runs through the repository Actions runs API when the default connector's commit-workflow lookup is PR-filtered. Never infer that CI did not run from an empty partial status view. Do not copy RevDev implementation or acceptance results into PocketCode.


## 2026-11-06 — Cross-project Actions discovery result (RevDev only)

RevDev's previously unknown push-triggered Windows test workflow was directly queried through the GitHub Actions runs API. After fixing its source byte-decoding order and stale Pester source assertions, run #13 passed 15/15 on Windows PowerShell 5.1 / Pester 5.7.1: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42130948334. This validates only RevDev's tracked maintenance source/test contract. PocketCode should reuse the method of querying exact workflow runs and logs, not RevDev code or its acceptance suites.

PocketCode remains Discovery; CASE-04 timeout/report-contract correction remains the next implementation task; device comparison is awaiting owner observations; no runtime/provider is selected; $0 default budget and separate canonical LOOP/CASE/D semantics remain unchanged. PocketCode branch was 723 ahead / 0 behind main at this recorded snapshot; this is commit history, not product progress. PR #2/#3 remain open drafts and untouched.


## 2026-11-06 — Pyodios installed build confirmed by owner

Owner-provided transcription of the installed app screens reports Pyodios **1.1.0 / Build 7**, Pyodide **314.0.5**, Python **3.14.2**, and WebAssembly (WASM) runtime. Settings also displayed 13 cached packages / 0 KB cache, 85,557 objects / 0 referrers, and GC stats 1,650 collected / 0 uncollectable. These are owner-reported observations, not independently inspected by ChatGPT; the memory and GC counters are transient diagnostics, not performance or capacity measurements. The app/runtime values match the public v1.1.0 documentation.

This resolves the installed app/build/runtime baseline. Device model and iOS version remain unknown. No fixed-task execution has been reported: success/failure behavior, real artifact integrity/export, and normal relaunch persistence remain NOT RUN. Follow `AI_COLLAB/PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md`; do not restart or clear the current session merely to reset counters. This does not select Pyodios as PocketCode's runtime or change any acceptance contract.


## 2026-11-06 — Final cross-project CI result (RevDev only)

RevDev's typed HTTP parser and publisher preflight increment passed GitHub Actions run #17 with **24/24** tests on Windows PowerShell 5.1 / Pester 5.7.1 at commit `c559aa7db595cb890981544184807381991e7490`: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42132258538. This is RevDev source/test evidence only. It validates the continuity rule to inspect the repository Actions run collection and job logs by exact head SHA when a connector's commit workflow view is incomplete.

PocketCode remains independent. Its next implementation priority is CASE-04 timeout classification/report-contract integrity in `scripts/report_contract.py`; no runtime/provider is selected, device comparison awaits owner observations, $0 budget and phone-first constraints remain, and canonical LOOP/CASE/D suites remain unchanged. PR #2/#3 are not modified by this update.


## 2026-11-06 — RevDev fake-process test result (process lesson only)

RevDev's fake native-process transport harness passed run #21, **34/34** on Windows PowerShell 5.1 / Pester 5.7.1 at commit `65d9b95ed346c42ed22bd920d70cb4e5c4429a26`: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42133707971. The transferable process lesson is to exercise real process boundaries with controlled fakes, without live network or external writes. This is not PocketCode implementation or acceptance. PocketCode's CASE-04 timeout/report-contract correction remains its immediate next task.


## 2026-11-06 — Cross-project process update: exact-SHA CI and no-silent-stop

RevDev's current process-harness hardening caught a PowerShell module/global automatic-variable issue after the earlier 34/34 success. The fix is committed, but run #26/#27 were pending/in progress at last observation. This is an example of the desired workflow: use exact-SHA CI evidence, inspect logs, fix regressions, and preserve the distinction between earlier green and current unverified code. PocketCode may adopt this work discipline, not RevDev implementation. For PocketCode, inspect CASE-04 and its own CI independently.

Each project chat should checkpoint GitHub after every meaningful pass, refresh its start page/work log, state exact head SHA and verification status, and rotate before context exhaustion. If a tool call fails, recover from last confirmed GitHub state and provide a concise result rather than silently stopping.


## 2026-11-06 — Cross-project CI evidence refresh

RevDev run #29 passed 36/36 on Windows PowerShell 5.1 / Pester 5.7.1 at 5c0435d6e9412f3a1dc72410be6495a61acaeceb. Its latest 404 classification hardening is at commit 144d0aa361343277aed9af76ad5736969c29abc9 with 42 tests; run #30 42136315313 was in progress at last observation. This is RevDev-only evidence and implementation. PocketCode must continue with its own CASE-04/report-contract and independent CI.


## 2026-11-06 — Cross-project testing-method note

RevDev's 404 classifier change caused one stale static source assertion to fail after the implementation moved behind a helper; 41/42 tests otherwise passed. The test was updated to follow the helper boundary and two malformed-body cases were added. Latest RevDev commit 5a18ba76860be7ab466fc0fe6b43ebd3aa0349c6 has 44 tests; run #31 was in progress. PocketCode should favour semantic contract tests over brittle text matches where possible. This is process guidance only.


## 2026-11-06 — Cross-project update: RevDev recovery and reliable chat rotation

This is a cross-project progress/process update only. PocketCode remains a separate product, codebase, runtime, security boundary, roadmap and acceptance suite. Do not import RevDev PowerShell code, test counts or acceptance conclusions.

RevDev's current branch has advanced beyond the previous transport-only work. Latest observed branch head: `e00e20d44f240b24faa769f558c9d61b99bdffb1`. The immediately preceding source checkpoint `40a8698060b50b3a94f946fe443caf201fd0f168` adds:
- Atomic create-only local result persistence and strict discovery. Only one validated matching result is accepted; multiple candidates are AMBIGUOUS; malformed, partial or unreadable discovery is DISCOVERY_INCOMPLETE. No newest-timestamp heuristic.
- Runner writes `queue-result.json` atomically and exposes SHA-256; watcher forwards the expected digest.
- Publisher verifies the local bytes/digest and binds the requested Project/Mission to the identity inside the result before any GitHub request.
- Typed process + HTTP response handling, exact remote prepared-envelope byte readback, and stricter 404 absence proof.
- Recovery quarantine uses GUID destinations, avoids `Move-Item -Force`, and writes metadata atomically. Partial failure reports the destination because the source may already have moved.
- Fake native process harness tests stdout/stderr, HTTP 200/404/429, process exit/status conflicts, missing executable, and PowerShell 5.1 LASTEXITCODE lifecycle.

At source checkpoint `40a8698060b50b3a94f946fe443caf201fd0f168`, the test target is 59 publisher tests + 22 local-result/quarantine tests = 81. Run #42 `42180012296` targets that exact source commit and was still in progress during Pester installation at last observation. Current branch head has a docs-only follow-up commit; re-fetch exact run state before quoting a result. Prior run #37 passed 73/73 at an earlier revision only. Do not call the current 81 tests green until run #42 finishes.

**Transferable PocketCode lessons:**
1. Keep CI evidence exact-SHA scoped. An older green run never validates a later commit.
2. Query repository Actions runs, match workflow path, branch, event and SHA, inspect jobs and retrieve logs for actual test counts. Do not rely on incomplete PR-only summaries.
3. Test real process boundaries with controlled fake executables/adapters where applicable, without live network or writes.
4. Prefer semantic contract assertions over brittle static string checks; when an abstraction moves, update the guard to test the new boundary.
5. Treat ambiguity as UNKNOWN/INCOMPLETE, never as absence or success. This principle is portable; implementation details are not.
6. A failing test is evidence. Trace it to source/fixture/contract, preserve the finding, fix only after confirming the intended behavior.
7. If a tool call fails or a chat appears to stop, recover from the last confirmed GitHub state and close the pass with a user-visible status. Never silently stop.

**Chat lifecycle:** GitHub is durable memory and each chat is a replaceable worker. Do not wait for a maximum-context warning or a huge final handoff. Every 2–3 meaningful passes, or after any meaningful source/test/review/decision event, append the project work log and refresh the start page with branch head, exact pins, CI status, next action and unresolved risks. Rotate chats while context remains. New chats should read the start page, fetch live branch/PR/CI state, then read only task-specific canonical docs. Keep one lead writer per repo/branch/work item; parallelize independent read/review tasks, serialize writes to shared paths, re-fetch before writing and read back after. A multi-file Git tree commit with expected-head protection is preferred where available.

**PocketCode priority unchanged:** continue CASE-04 timeout/report-contract integrity in `scripts/report_contract.py`; preserve LOOP/CASE/D IDs and meanings; device comparison awaits owner observations; $0 budget, phone-first, no PC requirement, explicit paste-to-context and no clipboard polling/overlays remain. Do not change architecture or select a runtime based on RevDev work. PR #2/#3 remain untouched.


## 2026-11-06 — Cross-project engineering method update

RevDev's latest source work provides transferable reliability methods, not PocketCode implementation or acceptance: hermetic fake-process testing at the actual boundary, exact-SHA CI evidence, strict UNKNOWN/INCOMPLETE classification, identity/digest binding before external effects, create-only immutable result writes, and recovery-safe quarantine. See `AI_COLLAB/CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md`.

PocketCode remains independent. Do not copy RevDev PowerShell scripts, runtime assumptions, test counts or verdicts. PocketCode's immediate task remains CASE-04 timeout/report-contract correction, with its own tests and evidence. The GitHub-backed multi-chat protocol is now the standard: update start page/work log/canonical docs during work and rotate chats before context exhaustion rather than waiting for a full chat to request a large handoff.


## 2026-11-06 — Cross-project CI closeout: RevDev recovery suite

RevDev run #42 `42180012296` completed **81 passed, 0 failed, 0 skipped** on Windows PowerShell 5.1 / Pester 5.7.1 at exact source/test commit `40a8698060b50b3a94f946fe443caf201fd0f168`. Run: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42180012296. It covers 59 publisher identity/transport cases plus 22 local-result/recovery/quarantine cases. This is maintenance-source CI evidence only, not live network/queue/watcher/mission execution, installed-PC parity, or P0/P8U acceptance. The RevDev branch has docs-only commits after the tested source SHA.

PocketCode must continue its own CASE-04 timeout/report-contract work. No RevDev implementation, test count, or acceptance transfers. Reusable method: exact-SHA CI, fake process boundaries, semantic contract assertions, explicit UNKNOWN/INCOMPLETE outcomes, review partial-failure paths, and update GitHub before rotating chats.


## Collaboration and continuity objective

PocketCode is expected to span many short-lived ChatGPT conversations. The project workflow must not depend on one chat retaining its full history. GitHub is the durable source of truth; each chat is a replaceable worker. Optimize for resumability, not maximum conversation length.

Operational acceptance criteria:
- The chat entrypoint identifies live branch state, current source/test pins, verified outcomes, blockers and next action.
- Every work pass ends with a durable checkpoint and a user-visible result, including when tools or CI fail.
- Related documentation is checkpointed in batches rather than fragmented into repeated per-file commits.
- CI polling, file reads and tool output are bounded. Pending work is checkpointed and resumed later.
- Chat rotation starts before context exhaustion, without waiting for a user-requested handoff.

This reduces avoidable interruptions but cannot eliminate platform context limits or external service failures. The target is graceful interruption without lost project state. PocketCode remains separate from RevDev in implementation, roadmap, runtime, acceptance suites and release gates.


## 2026-11-06 — Pyodios first Editor attempt

The owner reports one attempt using canonical `main.py` and renamed `items.csv` in the same Pyodios project. The green whole-file Editor play control was used; the complete visible result was `[Bridge/executePython] PythonError`, with no traceback. Status is **ATTEMPT OBSERVED / ROOT CAUSE UNKNOWN / ARTIFACT OUTCOME UNKNOWN**. No PASS/FAIL is assigned.

Do not rerun `main.py` yet. First inspect the same project's Files tab for `summary.json`, preserve/read it if present, then inspect Settings → Diagnostics → Error Logs → View Error Log at the attempt timestamp. Pyodios documents timestamped details and warns that source text may appear in logs, so redact before sharing. If the artifact is absent and the log unhelpful, use the separately attached guarded diagnostic wrapper; local CPython 3.13.5 checks were 2/2, while Pyodios device execution of that wrapper remains NOT RUN.

Pyodide 314.0.5 documents Python exceptions crossing the JavaScript boundary as `PythonError`; Python documents `sys.exit()` as raising `SystemExit`. Since the frozen fixture ends with `raise SystemExit(main())`, that is a plausible but unconfirmed bridge explanation. Missing input visibility or another exception remains possible. Details: [Pyodios PythonError bridge triage](AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md).

The current start-page instruction to reorder `classify_verdict()` is superseded by `AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md`: generic exit code may be child exit, wrapper exit, forced termination, stale or contradictory. Resolve typed provenance and termination evidence at the coordinator boundary first. Preserve canonical CASE-04 as INCOMPLETE / timed_out; no formatter patch is made in this pass.

No product source, canonical fixture, LOOP/CASE/D suite, provider/runtime selection, PR #2/#3, Actions, merge, deployment, account or budget changed. $0 default remains.

## 2026-11-06 — Cross-project installer lesson

RevDev's latest integration review found that newly imported runtime modules were absent from its clean installer. Its review branch is adding dependency staging, fail-closed pre-existing-file checks, backup/rollback, self-test verification and one pinned source commit. The exact 91-case CI run was pending. PocketCode may reuse the process lesson: every runtime dependency must be traced through packaging/install/update/rollback, and a multi-file installation should fetch from one immutable source revision. Do not copy RevDev scripts or treat its CI as PocketCode proof. CASE-04 remains next.


## 2026-11-06 — RevDev CI closeout (process evidence only)

RevDev Actions run #48 passed 91/91 at exact source/test head `935108a6937f15b76f75850ebdbe70c69000be32`. It includes tests for clean-installer module dependency closure and single-commit source pinning. No installer or PC/live runtime operation occurred. PocketCode should reuse the method of testing dependency closure and immutable multi-file source snapshots, not the RevDev code or acceptance. CASE-04 remains next.
