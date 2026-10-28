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

Added [PRODUCT/MOBILE_TECHNICAL_TASKS.md](PRODUCT/MOBILE_TECHNICAL_TASKS.md) to map possible jobs (script execution, file conversion, structured-data validation, tests, artifact generation, and more advanced remote-PC tasks) and to keep risky/high-complexity capabilities out of the first MVP. Immediate focus remains one real, bounded script workflow and a trustworthy copyable result report. Long-term PC/phone convergence remains a goal to evaluate; accounts, synchronized storage, provider choice, and repository merge are not approved decisions. Budget remains $0, and no runtime or account was created.

## Execution-loop acceptance plan

Reviewed the owner-provided RevDev handoff as design evidence, not proof that every described feature is present or verified in the Windows product. The transferable lesson is the full AI → guarded execution → structured per-check report → AI correction loop. Added [PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md](PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) with verdict semantics, 14 acceptance criteria, adversarial/failure scenarios, and a staged automation ladder. It explicitly separates script-reported checks from execution-service evidence and treats automatic cross-app capture as unproven. This is planning only: no runner, provider, account, live workload, or automation integration was added or tested.

## Current phase

Discovery, competitive research, and MVP definition. No production architecture, runtime provider, monetization model, or public brand commitment has been approved.

## Working MVP direction

- Mobile-first responsive web application/PWA as the first testable interface.
- Start with one real, isolated remote runtime, likely Python.
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
- PocketCode is separate from RevDev.

## Immediate next steps

1. Use the owner-reviewed [live mobile prototype](https://marcelosofficial-ctrl.github.io/PocketCode-/) only to refine the core flow; keep sample output clearly marked as simulated.
2. Compare local-on-device Python, browser-local Pyodide/WASM, remote-PC, and hosted execution against the [fixed-task worksheet](AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md). The [MVP decision brief](AI_COLLAB/MVP_DECISION_BRIEF.md) is a historical hosted-provider shortlist from 2026-10-20; revisit it only if the task demonstrates a need for remote execution. Modal/Cloudflare remain unselected candidates, not the default path.
3. Review the [controlled Python proof runbook](PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md), which defines test fixtures, expected evidence, and safety gates.
4. Before any provider account or live workload, obtain explicit owner approval, verify billing/budget controls, and confirm the exact network-blocking and termination semantics. If approved, run the proof and record actual evidence rather than assuming success.
5. Use public firsthand discussions and reviews in [mobile-coding user evidence](RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) to refine the problem hypothesis; user interviews are optional, not a blocker.
6. Revisit the provisional name before investing in a final brand or domain.
7. Use public desk research first. The [user validation interview script](PRODUCT/USER_VALIDATION_SCRIPT.md) remains optional; no interviews have been conducted.

## Progress log

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
