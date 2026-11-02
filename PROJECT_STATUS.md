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

The active queue is maintained in the [current checkpoint](AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md) and the dated work sequence in the [four-month phone-only plan](AI_COLLAB/FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md). Do not restart the broad research list on every chat.

1. Keep source-of-truth/navigation tidy and resolve stale wording; the execution location must stay undecided until the fixed-task comparison provides evidence.
2. Finish exact-ref lifecycle/report review, especially policy-revision-before-start evidence and disposition versus artifact-release behavior.
3. Reuse the [fixed-task worksheet](AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) and existing competitor evidence. Hands-on alternatives have not been compared yet.
4. Review the static prototype for task-specific mobile-flow issues; sample output must remain labelled simulated. Do not trigger deployment/Actions for this review.
5. Prepare the PC-return checklist by February 2027. Provider testing remains separate and approval-gated; no provider, account or spend is selected.
6. Revisit naming risk without renaming the repository or buying a domain as a side effect.

## Progress log

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


## Execution-boundary and trust crosswalk (2026-11-01)

Added [AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md](AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md) on the isolated documentation branch \`pocketcode-execution-boundary-crosswalk-2026-11-01\`, based on research-branch commit \`97db362e3f57c4d605d5d84a28d5cbb264c23c24\`.

The crosswalk reconciles PR #2, PR #3 and the separate research branch without merging their evidence. It records the current Pyodide 314.0.7 mobile/WebAssembly limits, worker interruption and same-origin credential boundaries, file/network constraints, collector-versus-termination semantics, COORD-01 execution/release separation, the PR #3 tombstone overwrite/retention gap, and proposed local/remote acceptance batches.

**Decision for next research phase:** run a fixed, synthetic CSV-to-CSV feasibility experiment with local browser Python before choosing a hosted provider. This is not a production runtime selection. Budget remains $0. No code, tests, PR #2/#3, provider, account, workload, billing, Actions, deployment or merge changed. Exact helper/test suites remain NOT RUN in this pass.


### iPhone/Safari feasibility addendum — 2026-11-01

Extended the execution-boundary crosswalk with iOS-specific findings: Safari/iOS file-system API limitations, memory-pressure and reload handling, a narrowly scoped current WebKit WASM compilation report, and LOC-17..LOC-24 acceptance cases. The report explicitly does not generalize the Asyncify-specific WebKit issue to Pyodide. The first experiment remains a small standard-library CSV/JSON transformation, tested in foreground on an actual iPhone. No runtime, source code, PR, provider, workflow, account, billing, deployment or merge was changed.


### Lifecycle sibling-branch lineage correction — 2026-11-01

Added Section 16 to the execution-boundary crosswalk after inspecting \`pocketcode-lifecycle-fingerprint-audit-2026-10-27\`. That separate branch already contains source/tests for tombstone retention/fingerprint conflict and blank fingerprint identity validation. These are not merged into PR #3; the PR #3 pinned source still has the earlier behavior. Remaining sibling-branch gaps include OutputBudget integer type validation, malformed limit-flag truthiness, event binding/snapshot ownership and redaction length ceilings. Tests were inspected but not run.


### Exact lifecycle branch ancestry and source delta — 2026-11-01

A direct commit comparison established that `pocketcode-lifecycle-fingerprint-audit-2026-10-27` is a direct descendant of the pinned PR #3 head used in the audit: 34 commits ahead, 0 behind, with the PR #3 commit as the merge base. It is not a divergent branch. The descendant contains tombstone retry/fingerprint protection, blank canonical fingerprint identity validation, malformed terminal-event input validation, and six additional lifecycle test methods (30 total versus 24 at the PR #3 base). The helper also retains the known OutputBudget type, malformed limit-flag, output/termination, event-binding/deep-snapshot, and redaction limitations. Source and test files were inspected; tests were not run. No PR for the descendant was found in the repository PR search. No merge, cherry-pick, implementation edit, Actions run, provider activity, billing, or deployment occurred.

See Section 17 of [the execution-boundary crosswalk](AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md) for exact commits, changed-file inventory, and disposition.


**Delta inventory correction:** inspection of the full GitHub compare patch additionally confirms `reserve_idempotency()` now rejects blank/non-string tenant ID, key, fingerprint and proposed job ID. Its regression test is one of the six added methods. The crosswalk now lists all six additions and distinguishes pure-helper input validation from upstream authentication and transactional storage guarantees.


### Event reducer integrity follow-up — 2026-11-01

A line-level review of the lifecycle descendant found that malformed-event shape validation does not solve nested payload immutability: the reducer uses shallow outer copies, and its accepted events, invalid-event records and duplicate-comparison state can retain caller-owned references. It also flags duplicate coordinator sequence numbers without returning the colliding records in a dedicated diagnostic collection. These map to existing D-04 / COORD-11 / COORD-12 and FLA-04/06/07 concerns, not new duplicate finding IDs. D-04 remains owner-open; no event schema or source patch was approved. See Section 18 of the crosswalk. Tests remain NOT RUN.


### Report formatter/redactor boundary follow-up — 2026-11-01

Exact source inspection confirms PR #2's `_safe_text()` escapes control characters and truncates fields but does not redact secrets; `format_report()` renders stdout/stderr and user/program-supplied metadata. PR #3's `OutputBudget` uses a best-effort `StreamingRedactor`, but no integrated data flow proves that all PR #2 report fields pass through it. This remains an integration/data-flow gap, not a verified production exploit. See Section 19 of the crosswalk. No source edits or tests were run.


### Fresh lifecycle helper and test coverage review — 2026-11-01

Refreshed the exact lifecycle audit branch name and pins, then reviewed the descendant helper and 30-method test source line by line. The prior `lifecycle-fingerprint` shorthand was incorrect; the live name is `pocketcode-lifecycle-fingerprint-audit-2026-10-27`, HEAD `26de6bb29020d6781d342c691e430616a4321083`.

New findings added to Section 20 of the execution-boundary crosswalk and the consolidated patch sequence:
- Expand G-01 strict boolean validation to include `contradictory_evidence`; malformed falsey contradiction or truncation values can otherwise be treated as absent and allow an otherwise valid EXIT_ZERO to project PASS.
- Validate effective-policy mapping keys as strings recursively before JSON fingerprint serialization; Python's JSON encoder coerces non-string dictionary keys to strings.
- Confirm G-07 remains open: Windows documents COM¹/COM²/COM³ and LPT¹/LPT²/LPT³ as reserved aliases, but the helper regex and current tests cover only ASCII digits.
- Add whitespace-only `ReportHistory` job/evidence-reference rejection.
- Keep immutable event metadata bound at trusted ingress under D-04; the reducer's duplicate signature currently compares only sequence, kind and payload.
- Add redactor tests at and beyond configured maximum token lengths without claiming universal secret detection.

Official references: [Microsoft Windows file-naming rules](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) and [Python JSON serialization behavior](https://docs.python.org/3.13/library/json.html).

This remains static source review and documentation. No implementation source changed, no tests were executed, and D-01/D-04 remain owner-open. See [crosswalk Section 20](AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md) and [consolidated patch sequence](AI_COLLAB/CONSOLIDATED_LIFECYCLE_AND_REPORT_PATCH_SEQUENCE_20261101.md).


### Tombstone expiry and report completeness follow-up — 2026-11-01

A further static source pass identified that an expired in-memory tombstone may continue blocking a new fingerprint until `lookup()` first removes it. Expiry therefore depends on call order and needs a trusted-time/atomic reservation rule under D-08. The PR #2 formatter also renders malformed truncation flags as `no` in its summary while adding a separate warning; the summary should preserve UNKNOWN rather than imply completeness. These are documented in crosswalk Section 21 and patch-sequence Section 12. Exact source blobs unchanged; no tests executed or implementation changed.


### End-to-end trust-chain synthesis — 2026-11-01

A read-only synthesis now connects request admission, semantic fingerprinting, durable reservation, dispatch intent, actual policy binding, provider start/reconciliation, scoped event ingress, terminal/cleanup evidence, output collection, redaction/report projection, durable report publication, artifact publication/release, and mobile presentation.

The central finding is that the documents and helpers describe compatible pieces but do not establish one integrated trusted execution path. In particular:
- D-05 remains BLOCKED because no selected provider/runtime has demonstrated immutable per-attempt policy binding or atomic conditional dispatch.
- D-06 remains an owner-open proposal; no selected durable store/provider proves atomic reservation, provider idempotency, or lost-ack recovery.
- D-04 remains owner-open; no authenticated provider ingress has been verified, and the reviewed reducer has immutable-snapshot and sequence-collision diagnostic gaps.
- PR #2 report formatting has no verified end-to-end redaction/typed-projection path from PR #3.
- D-08 report history and D-07 artifact publication/release remain proposals without selected durable stores or API integration.
- Device execution acceptance remains NOT RUN.

Published [END_TO_END_TRUST_CHAIN_GAP_MATRIX_20261101.md](AI_COLLAB/END_TO_END_TRUST_CHAIN_GAP_MATRIX_20261101.md) with the stage-by-stage authoritative producer, identity invariant, current evidence, proof gate, cross-stage failure rules, owner decision blockers, and implementation order.

This is documentation-only synthesis. No implementation or canonical acceptance changed; no tests/workloads ran; no provider/store was selected; no PR was merged and no deployment occurred.

### Coordinator crash-window and stale-worker audit — 2026-11-01

A focused static review of the provider-neutral interfaces and crash/recovery plans identified an additional design gap: worker leases are discussed, but no monotonic fencing epoch is specified for every coordinator mutation. A stale worker could resume after lease expiry and attempt dispatch, event acceptance, report projection or artifact publication. A database lease by itself cannot fence an external provider call.

The audit also requires a complete provider idempotency-token namespace and retention contract; an exact dispatch-intent crash/call-order table; stale-worker handling for late evidence and projections; separate source-event, coordinator-event, projection, append and publication identities; and exact immutable-byte/range-transfer semantics at artifact release.

Published [COORDINATOR_CRASH_WINDOW_AND_FENCING_AUDIT_20261101.md](AI_COLLAB/COORDINATOR_CRASH_WINDOW_AND_FENCING_AUDIT_20261101.md), including proposed STALE/TOKEN/PUB/REL falsification cases. These are proposed test additions, not canonical acceptance IDs.

D-06 remains OPEN; D-04/D-07/D-08 remain OPEN; no provider/store is selected. Static review only: no implementation changes, tests, workloads, account/billing actions, merges or deployments.

### Unified coordinator failure-injection specification — 2026-11-01

Published [UNIFIED_COORDINATOR_FAILURE_INJECTION_SPEC_20261101.md](AI_COLLAB/UNIFIED_COORDINATOR_FAILURE_INJECTION_SPEC_20261101.md), a 14-section synthesis of the existing DR-01..12 and COORD-01..12 inventories, report-history and artifact-release checklists, the provider-neutral boundary and the two 2026-11-01 architecture audits.

The specification defines the distinct identity namespaces, proposed durable state machine, fourteen crash/commit boundaries, fencing-epoch requirements, provider token namespace/retention requirements, and proposed STALE-01..05, TOKEN-01..04, PUB-01..02 and REL-01..03 failure-injection cases. These proposed cases do not replace or renumber canonical LOOP/CASE or existing DR/COORD IDs. It separates owner decisions D-01..D-08 from engineering/test design and defines proof gates from pure tests through fake coordinator, persistence, provider, artifact/API and device acceptance.

Source pins were refreshed from the active documentation branch immediately before authoring. The new specification blob is `51edbb9bd1e3f3518b0e80620be9c0ebe88f49ab`. No implementation, canonical acceptance, PR #2/#3, provider/store selection, tests, workloads, account/billing, merge or deployment changed. D-05 remains BLOCKED; D-06..D-08 remain unproven at real boundaries; all new cases are NOT RUN.


### Independent coordinator adversarial review — 2026-11-01

Published [UNIFIED_COORDINATOR_ADVERSARIAL_REVIEW_20261101.md](AI_COLLAB/UNIFIED_COORDINATOR_ADVERSARIAL_REVIEW_20261101.md), a static adversarial pass against the unified coordinator failure-injection baseline.

The review adds eight design findings: same-epoch concurrent writes require expected-version CAS; a delayed provider Start may arrive after worker takeover despite an earlier valid dispatch authorization; cancellation request/acknowledgement is not proof of termination; provider event identity/payload digest/sequence scope must be explicit; projection commits must bind an immutable event-set watermark; garbage collection must coordinate with pending artifact publication; provider token retention must cover the complete job/outage/delayed-request uncertainty horizon; and transfer revocation cannot recall bytes already sent.

Proposed additional cases are CAS-01, DISPATCH-01, CANCEL-01/02, EVENT-01..05, PROJECTION-01, PUB-03, TOKEN-05 and REL-04. These are not canonical acceptance IDs and remain NOT RUN. Priority is ADV-01/02/04/05 before coordinator implementation, followed by cancellation, publication-GC, token-retention and transfer semantics before provider/artifact integration.

This is documentation-only. No implementation, canonical acceptance, PR #2/#3, provider/store, workflow, workload, account/billing, merge or deployment changed. D-04/D-05/D-06/D-07/D-08 remain open or blocked as previously recorded.


### Lifecycle ordering review — 2026-11-01

Published [LIFECYCLE_ORDERING_AND_EVIDENCE_PRESERVATION_REVIEW_20261101.md](AI_COLLAB/LIFECYCLE_ORDERING_AND_EVIDENCE_PRESERVATION_REVIEW_20261101.md). Static review identified three design clarifications: (1) separate execution finalization from destructive cleanup and preserve required outputs before deletion unless durable provider-side output retention is proven; (2) define a trusted per-task artifact expectation and explicit artifact-not-required path so successful artifact-free jobs can finish; (3) separate release authorization, first-byte disclosure, partial transfer, server-side byte completion and any explicitly verified client receipt. Proposed LIFE-01..12 are not canonical acceptance IDs and remain NOT RUN. P0 before implementation design: evidence preservation and artifact-free branch. P1 before release/API design: transfer semantics. Documentation-only; no source, PRs, provider/store, tests, workflows, workloads, billing, merge or deployment changed. D-01..D-08 remain open/blocked as previously recorded.


### RevDev + PocketCode convergence and Gemini open-source research audit — 2026-11-01

Published [REVDEV_POCKETCODE_ARCHITECTURE_CONVERGENCE_AND_GEMINI_RESEARCH_AUDIT_20261101.md](AI_COLLAB/REVDEV_POCKETCODE_ARCHITECTURE_CONVERGENCE_AND_GEMINI_RESEARCH_AUDIT_20261101.md). The review treats Gemini's report as a candidate inventory, not an approved implementation plan. It recommends sharing versioned, language-neutral task/lifecycle/outcome/evidence/artifact contracts while keeping coordinators, queues, execution adapters, authorization, storage, security policy, acceptance suites and release gates product-specific.

The audit highlights useful references (Cline layering, Aider repo maps, River, MCP, DevPod SSH, isomorphic-git/LightningFS, Pyodide and Linux sandbox tools) while recording key caveats: MCP is not durable job orchestration; queue leases do not fence external side effects; LightningFS documents crash-ordering/repository-corruption risk and browser CORS constraints; DevPod's client/provider model is not proof of a phone-ready runtime; Linux sandbox tools do not apply to iOS or Windows; generic iOS memory thresholds and the 9–14 month acceleration estimate are unsupported; credential handling and license claims require deeper review. River's current repository metadata describes a polyglot Postgres/SQLite queue, but exact Go/backend compatibility and RevDev fit remain unverified.

No adoption decision was made. The next research step is to reconcile Claude's independent report, then score exact modules against fixed project needs. RevDev queue selection remains deferred until PC access and read-only source/runtime inventory return. PocketCode execution location remains undecided and its fixed-task comparison remains the priority. Documentation-only: no source/tests, PR #2/#3, provider, account, workload, Actions, billing, merge, deployment, or host state changed. No tests were run.


**River source-level follow-up:** inspected the current Go tree and confirmed a dedicated `riverdriver/riversqlite` package exists. Its own source labels the driver early testing with minimal real-world use, warns about SQLite single-operation concurrency/`SQLITE_BUSY`, suggests a one-connection pool, and notes slower row-at-a-time completion/InsertMany behavior versus Postgres. The root Go module currently depends on the separate `riverpgxv5` driver. The architecture audit was refined accordingly: River is a real RevDev candidate, but the Go SQLite backend is not assumed production-ready and must be assessed against actual local/offline requirements. This is upstream source inspection only, not an installation or compatibility test.


### Shared contract readiness and state-domain crosswalk — 2026-11-01

Published [SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md](AI_COLLAB/SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md). This reconciles the existing PocketCode shared-core/execution-contract proposals with RevDev P8U and shared-infrastructure reliability authorities. Key design finding: do not flatten execution outcome, coordinator/job disposition, publication/release/transfer state, and user-facing verdict into one status field. RevDev P8U explicitly allows product execution PASS while publication remains PENDING_RETRY; publication retry must not rerun execution. PocketCode's user-facing PASS/FAIL/INCOMPLETE remains a derived projection of trusted execution evidence, not publication state. The report also maps native identities (task/job/attempt/operation/event/evidence/artifact/release-decision/transfer), identifies ten contract gaps, and proposes golden negative fixtures. It is a provisional analysis, not a frozen schema or implementation approval. No tests or runtime work were performed.


- 2026-11-01: Added [shared contract readiness and state-domain crosswalk](AI_COLLAB/SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md) and [shared contract golden fixture catalogue](AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_20261101.md). The catalogue defines 18 provisional scenarios across execution, coordination, evidence capture, publication, release and transfer, with conservative crosswalks to native PocketCode and RevDev acceptance IDs. Canonical LOOP/CASE/P8U/P0-D/RelayRef suites remain unchanged; conceptual fixture relationships do not imply acceptance equivalence. Documentation-only work: no schema freeze, implementation, executable tests, provider/store selection, workload, Actions run, deployment, merge, or spend.


### Comprehensive RevDev + PocketCode new-chat handoff — 2026-11-01

Published [NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_20261101.md](AI_COLLAB/NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_20261101.md). It consolidates current verified repository/branch/PR state, three-AI roles, the expected forthcoming medium-sized Claude report and explicit instruction not to let recommendations overwrite project goals, PC/$0/HOSTED_DENY constraints, shared product direction, Gemini candidate audit, cross-project state/identity rules, SCF-001..018, canonical acceptance boundaries, technical audit findings and next priorities. Includes a ready-to-paste bootstrap for the next chat. Documentation-only continuity update; no source/tests, PR #2/#3, default branch, provider, Actions, workload, host state, merge, deployment, billing or spend changed.


### Shared fixture preliminary review and fixed-task alignment — 2026-11-01

Added [SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_CHATGPT_PRELIMINARY_REVIEW_20261101.md](AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_CHATGPT_PRELIMINARY_REVIEW_20261101.md). This is ChatGPT's independent static semantic/acceptance review of provisional SCF-001..018, not Claude/Gemini review, owner approval, schema freeze or executable acceptance. It recommends retaining the 18 IDs while tightening selected proof preconditions and preserving supplemental CAS/DISPATCH/CANCEL/EVENT/PROJECTION/PUB/TOKEN/REL adversarial cases without renumbering canonical suites. Claude's dedicated catalogue review and Gemini's dedicated red-team review remain pending.

The newer execution-boundary crosswalk's example CSV-cleaning/CSV-to-CSV task could be mistaken for a replacement of the already-established fixed-task worksheet. Section 11 was aligned to the existing canonical PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md (items.csv to real summary.json, including the malformed-header case). The alternate cleaning task is not adopted. The worksheet remains the single canonical fixed task; LOC-01..24 refine browser/device acceptance but do not change it.

Documentation-only changes on this isolated research branch. No schema, canonical acceptance, source/tests, PR #2/#3, provider/store/runtime, account, workload, Actions, billing, deployment, merge or PC/host/queue state changed. No tests or device execution occurred.


### State and identity mapping preparation — 2026-11-01

Added [STATE_AND_IDENTITY_MAPPING_PREPARATION_20261101.md](AI_COLLAB/STATE_AND_IDENTITY_MAPPING_PREPARATION_20261101.md). It sharpens the existing shared-contract readiness work into seven independent state axes (execution outcome, coordination disposition, evidence persistence/integrity, publication, release authorization, transfer/delivery/receipt, and derived user-facing verdict), plus separate artifact expectation and operation records. It clarifies why rejected/pre-start and infrastructure-uncertain lifecycle labels must not fabricate execution outcomes, why cancellation request/acknowledgement is not termination, and why PocketCode CASE-04's trusted-timeout INCOMPLETE/timed_out behavior remains the working canonical default.

The note provides a provisional identity map for task, RevDev MissionId/RunId, PocketCode runId, coordinator job/attempt, side-effect operation/provider token, source/coordinator event, evidence/result, artifact, report version, release decision and transfer/receipt identities. It preserves LOOP/CASE/AEC/AWC, COORD/DR, SCF, P8U, P0-D, RelayRef and RevDev AWC namespaces without claiming equivalence. It does not freeze names/enums or resolve lifecycle D-01..D-04 / D-05..D-08.

Claude research availability was rechecked: all eight PocketCode branches were enumerated; no dedicated medium-sized Claude research report appears in the active research tree or listed branches. Branch search returned no Claude-specific research branch. Repository commit search found only the older CLAUDE.md entry-instructions commit, not the promised report. This means NOT RECEIVED in this checked snapshot, not that Claude has not written it elsewhere. Claude's SCF-specific review and Gemini's SCF-specific red-team review remain pending.

Documentation-only work on the isolated research branch. No schema, owner decision, canonical acceptance, source/tests, PR #2/#3, main branch, provider/store, account, workflow, Actions, workload, billing, deployment, merge or PC/host/queue state changed or exercised. No tests/device/provider execution occurred.


### Pyodide 314.0.7 official-source mobile feasibility review — 2026-11-01

Added [PYODIDE_314_0_7_MOBILE_RUNTIME_FEASIBILITY_REVIEW_20261101.md](AI_COLLAB/PYODIDE_314_0_7_MOBILE_RUNTIME_FEASIBILITY_REVIEW_20261101.md) and linked its findings from Section 22 of the execution-boundary crosswalk. This is official-source desk research only; the fixed task and LOC-01..24 remain NOT RUN.

Key refinements: Pyodide 314.0.7 requires a module-type worker; its documented cooperative KeyboardInterrupt path requires a Web Worker plus SharedArrayBuffer/cross-origin isolation, so LOC-05 gates LOC-06; maxMemoryBytes appears in the current Unreleased changelog section and is not part of the pinned 314.0.7 release; the default MEMFS is lost on reload; Safari file handling requires explicit picker/import and Blob save/share rather than Chromium-only File System Access API; and Worker.terminate does not establish Python cleanup or terminal outcome. The pinned standard-library task remains a suitable narrow candidate using decimal.Decimal, CSV and JSON, but does not prove general Python compatibility or security isolation.

No change to product direction, canonical task, provider ranking or approval gates. No code, tests, device run, app install, account, provider, workload, Actions, billing, PR, merge, deployment or host/queue operation occurred.


### Continuation handoff refreshed — 2026-11-01

Appended the verified post-handoff continuation delta to [NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_20261101.md](AI_COLLAB/NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_20261101.md). It records the new state/identity and Pyodide reviews, fixed-task alignment, Claude report availability check, current branch/PR snapshots, remaining reviewer/owner blockers and explicit non-actions. The original handoff snapshot is preserved above the appended delta. Re-fetch branch heads again before future work.


### Claude open-source research independently reconciled — 2026-11-01

Claude's "PocketCode + RevDev: Open-Source Research Master" was received and reviewed. The full independent reconciliation is [CLAUDE_RESEARCH_MASTER_INDEPENDENT_RECONCILIATION_20261101.md](AI_COLLAB/CLAUDE_RESEARCH_MASTER_INDEPENDENT_RECONCILIATION_20261101.md).

Primary-source checks confirmed the important architectural leads while narrowing their claims: srt Windows is explicitly alpha and documents Schannel failures, persistent ACL grants, cross-session read implications and WFP limitations; MCP Tasks is an optional extension outside the stateless core, not a durable-execution guarantee; ACP public docs list v1 as latest and v2 as draft; OpenHands documents an append-only EventLog plus distinct state-only/event-based updates and persistence/resume; StreamJsonRpc and Polly provide libraries, not our trust or durability model.

Disposition: srt/Codex sandbox and OpenHands are study targets; MCP Tasks is mapping vocabulary only; ACP is deferred to a later read-only spike; Happy requires source-level pairing/crypto review before fork discussion; StreamJsonRpc/Polly are conditional dependencies; no new SQLite journal is selected until existing RevDev P8U/source contracts can be audited. DSSE/in-toto remain format-study candidates, not a 100-line implementation commitment. Pyodide remains a constrained candidate under the existing 314.0.7 review, not an adopted or device-validated runtime.

Critical guardrail: parser syntax tolerance must never relax ACK/nonce/identity/confirmation/guard authority. Retry, cancellation, Job Object termination, durable recovery and verified terminal evidence remain distinct. PocketCode's product direction, fixed task, seven state axes and D-01..D-08 boundaries remain unchanged. RevDev PC state remains UNKNOWN.

This was documentation and selected public-source review only. No code, schema, acceptance, PR #2/#3, provider, account, workload, spend, Actions, install, device test, merge, deployment, PC host, watcher, queue or publication state was changed or exercised.


- 2026-11-01: Added [AI_COLLAB/WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md](AI_COLLAB/WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md), reconciling Claude's partial Windows sandbox audit with an independent exact-ref read of Codex token/runner source at 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635 and srt PR #745 metadata. Corrected the Codex token-flag evidence classification: flags are present in upstream source, not merely a derivative. Audit remains PARTIAL / STUDY ONLY; srt Rust source, Codex ACL/firewall/setup/cleanup/process containment and all Windows runtime behavior remain unverified. No sandbox selection, install, host change, test, schema, acceptance, implementation, PR, deployment, provider or spend.


- 2026-11-01: Extended the Windows sandbox source audit with pinned srt Rust/TypeScript reads. Verified token hardening (Administrators/logon SID disablement, privilege deletion except SeChangeNotifyPrivilege, write-restricted SID list/read-back), Job Object kill-on-close and suspended assign/resume, additive ACL/FDC semantics, per-user refcount/recovery model, WFP's ALE_AUTH_CONNECT-only layers and explicit ICMP non-coverage. Confirmed current srt main still marks WFP installed if any block filter exists; issue #723 reports partial-filter false health and IPv6 verification gaps; PR #716 proposes a fix but remains open. Recorded the shared-machine CA-key trade-off. Audit remains PARTIAL / STUDY ONLY; no runtime test, install, adoption, source change, schema, acceptance, PR, deployment or spend.


- 2026-11-01: Extended Codex source review at pinned commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635. Verified offline firewall rule scope and loopback behavior; identified high-priority ACL review concerns (target-only deny vs parent FILE_DELETE_CHILD grant, partial-deny detection, swallowed ACL write errors and refresh-only error aggregation), machine-scope DPAPI/secret-directory ACLs, size+mtime helper freshness, random SID-scoped runner pipes/PID check, and no Job Object in the inspected process launch path. These are source findings and review hypotheses, not demonstrated exploits. Audit remains PARTIAL / STUDY ONLY; no Windows tests or host operations.


- 2026-11-01: Follow-up recheck of srt current main and issue #723. Current main commit 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77 still reports WFP installed when any block-user filter remains, and its default readiness helper binds only IPv4 loopback. Issue #723 reports a one-machine Windows 11 26200 partial-IPv6-filter reproduction (3 repetitions per state); PR #716 remains open/unmerged and proposes partial state plus repair. A separate issue-comment branch proposes dual-family readiness probing but is not merged and was not source-inspected. Pinned tests explicitly show ICMP is not fenced and DNS Client service queries bypass the child-token ALE_USER_ID fence. srt remains ALPHA / STUDY ONLY. No Windows tests or upstream changes by ChatGPT.


- 2026-11-01: Added source-level review of OpenHands EventLog/state/lease and Happy pairing/encryption. OpenHands EventLog provides per-event JSON append-only evidence, stable disk sequence IDs, parent validation and gap reporting; LocalFileStore locking is not reliable on NFS, and event append plus base-state HEAD update are separate writes (crash-window hypothesis, not reproduced). EventService generation-checked guarded writes fence persistence writes but not arbitrary external side effects. Happy Android client uses transcript-bound X25519/HKDF, emoji comparison and mutual MAC proof; client tests use FakeDaemon and the public repo search did not locate the daemon-side handshake route, leaving server replay/expiry/rate-limit semantics unknown. Happy CLI credentials are plaintext JSON with requested POSIX modes; Windows ACL behavior unverified. Full detail: AI_COLLAB/OPENHANDS_EVENTLOG_AND_HAPPY_PAIRING_SOURCE_REVIEW_20261101.md. No tests/builds/device runs or upstream changes.


- 2026-11-01: Integrated the OpenHands/Happy findings into Section 23 of the execution-boundary crosswalk, Section 11 of the state/identity mapping, and the Gemini independent-review packet. These remain study findings only; D-01..D-08, canonical acceptance, fixed task and product direction are unchanged. Updated handoff includes the exact next reviewer challenges.


### OpenHands EventLog crash-window falsification plan — 2026-11-02

Added [AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md](AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md). This turns the observed append-event-then-save-active-leaf ordering into a bounded future fault-injection plan, not a defect claim. Eight deterministic process-crash points cover event persistence, leaf assignment/base-state replacement, lost acknowledgement and concurrent lease takeover. The plan requires fresh-process restore and independent classification of event durability, discoverability, active HEAD, active ancestry, acknowledgement and lease generation. It also covers retry/replay conflicts and distinguishes a missing leaf from an old still-existing leaf.

The plan has NOT been executed. It is not PocketCode acceptance and changes no IDs, schema, owner decisions, fixed task, provider/store selection or product direction. Gemini's review packet now asks for an independent challenge of the test boundaries. No source/tests, PR #2/#3, main branch, Actions, provider, account, workload, spend, deployment, merge or host/PC/RevDev queue state was changed or exercised. RevDev PC state remains UNKNOWN.


### OpenHands recovery-path refinement — 2026-11-02

Pinned source recheck found an explicit agent-server recovery path that must qualify the original crash-window hypothesis. In `event_service.py` lines 1424–1467, restored RUNNING conversations are marked ERROR; the service scans the full event log for unmatched actions and appends a non-retryable internal AgentErrorEvent explicitly parented to the first unmatched action when no ObservationBaseEvent exists for its tool_call_id. SDK `state.py` lines 268–320 show a still-existing saved leaf remains active; missing-leaf repair is separate. This confirms the SDK append/HEAD writes are not atomic while showing targeted recovery for interrupted tool actions. The recovery is conditional and does not prove whether an external side effect occurred or authorize retry. The falsification plan now includes six additional recovery-specific cases (OH-HEAD-FI-09..14). NOT EXECUTED; no acceptance/owner decision or product direction changed.


### Existing OpenHands recovery tests reconciled — 2026-11-02

Targeted search at pinned OpenHands commit found recovery unit tests in `tests/agent_server/test_event_service.py` (blob `fc6e589f71318ac36df92b72c1fd0225549d1436`, lines 2419–2678) and `tests/sdk/conversation/test_get_unmatched_actions.py` (blob `35798b1bccb60b0976cf0785682ef17181e4450b`). A documented F31.crash-tool-call SIGKILL integration scenario exists in the agent-server verification feature map (blob `5082730e1ba1d333daeaf321c21214ad4924cd12`, lines 191–220). Existing unit tests are mocked and do not assert recovery parent_id or restored active ancestry. F31 checks status/error event/no observation/resumed delivery but not parent_id/ancestry and has a DeepSeek key/model precondition in the broader recipe. Remaining minimum gap: real local persistence/restore fault injection asserting action → recovery error active ancestry, plus explicit parent_id. ChatGPT did not run these tests. No upstream source/tests changed.


### Final OpenHands EventLog marker/test-plan refinement — 2026-11-02

The pinned EventLog append sequence is event JSON write, in-memory index/length update, then sidecar marker update. The marker update deletes the old marker before writing the new one; LocalFileStore string writes use atomic_write_text. The falsification plan now includes marker crash boundaries and explicitly distinguishes process-crash survival from power-loss durability. Existing mocked unit tests and F31 SIGKILL integration recipe have been mapped; they do not assert recovery event parent_id or restored active ancestry. Do not duplicate them. Minimum residual test is real local persisted-file crash/restore with action → recovery error ancestry and explicit parent_id. No test run, no upstream code/test modification.


### OpenHands recovery review priority update — 2026-11-02

Pinned source supports multiple ActionEvents per LLM response and executes the batch only after emitting all action records. Batch results are emitted after the parallel executor returns. Startup recovery currently writes one AgentErrorEvent for the first unmatched action, whereas the normal interrupt path writes errors for every active-branch orphan. This creates a high-priority multi-action crash-recovery test gap (FI-15..18).

In-place navigate/re-root is also supported and preserves abandoned events in the full log, while startup recovery scans the full log and suppresses recovery on any matching observation-like event by tool_call_id. This makes stale-observation suppression after navigation a concrete test target (FI-19..22), subject to verifying the RUNNING lifecycle and intended re-execution semantics. F31 crash-tool-call configures a local llm-stub per-conversation agent; the wider F31 setup also presets DeepSeek for other subfeatures, so isolated provider-free execution remains to be verified.

Detailed evidence and tests: `AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md` Section 13. No tests executed, no upstream source changed, no PocketCode acceptance or owner decisions changed.


### OpenHands recovery error wording qualification — 2026-11-02

Startup recovery's AgentErrorEvent says the tool execution “did not complete” while classifying it INTERNAL/non-retryable. The code cannot prove no external side effect occurred before the crash, especially where parallel batch results are emitted only after the full batch returns. Treat the wording as potentially overconfident; missing observation/evidence does not prove non-execution. PocketCode design warning only: represent external outcome as UNKNOWN absent independent proof. Detailed test addition is in crash-window plan Section 14. No owner decision changed.
