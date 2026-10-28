# RevDev + PocketCode: Shared Core Proposal

Status: proposal only. Budget remains $0 unless the owner explicitly changes it.

## Vision

The long-term goal could be one script-execution and diagnostics system that works on PC and phone. RevDev is the reference for the PC workflow; PocketCode is the mobile-first path. Keep repositories separate for now. A future shared app is a direction to evaluate, not a decision to merge code today.

PocketCode's core loop: receive AI-generated script; paste/import code and input files; execute in a controlled environment; show an evidence-based result; copy a report into any AI assistant; apply a correction and rerun.

The pink result block is presentation. The portable interface is a stable plain-text report that works when copied into ChatGPT, Gemini, or another assistant.

## Shared result contract

Each run should produce a structured result rendered as a visible result block and copyable text:

- Verdict: PASS, FAIL, or INCOMPLETE.
- Exact execution status: succeeded, program_failed, timed_out, cancelled, rejected, or infrastructure_failed.
- Run ID, runtime/version, exit code when actually available, trusted duration when available.
- Actual stdout and stderr, bounded with explicit truncation markers.
- Generated filenames and sizes, plus any limit or uncertainty notes.

PASS requires confirmed completion and exit code 0. FAIL means a confirmed program/runtime error or non-zero exit. INCOMPLETE means timeout, cancellation, rejection, or no trustworthy result due to infrastructure failure. Never call a run PASS merely because a request was accepted or a client-side timer expired. Never invent missing exit codes or output.

## Phone flow

1. Code: paste or edit the script.
2. Files: add small input/helper files.
3. Run: one primary action, with runtime and limits visible.
4. Result: one prominent block with verdict, real output/errors, exit code and duration when available, and generated files.
5. Copy result: one obvious action copies the complete bounded report.
6. Edit and rerun: retain the last result while correcting the code.

Avoid a row of equally prominent buttons. Secondary actions appear only when useful. Provide selectable report text if clipboard access fails. Do not monitor the clipboard or other apps in the background. Never silently include credentials, private files, or unlimited source/output in the report.

## Proposed architecture

Separate four conceptual layers: (1) phone and PC clients; (2) shared run/report contract; (3) provider-specific execution adapter; (4) isolated runtime with enforced time, CPU, memory, process, file, output, and network limits. Share the contract before attempting to share a frontend framework or repository. A responsive web app/PWA is plausible but not approved. The application server must not execute submitted code itself; provider credentials must never reach the browser or untrusted code; outbound networking is denied by default.

## Stages

### Stage 0: align behavior without cloud execution
- Agree on result fields and PASS/FAIL/INCOMPLETE rules.
- Compare the intended result block with RevDev's actual output and tests when those artifacts are available.
- Simplify the phone prototype around one primary action and one obvious Copy result action.
- Keep sample output explicitly simulated.

### Stage 1: test report logic without a provider
- Add deterministic formatting/verdict tests for success, program error, timeout, cancellation, infrastructure failure, missing exit code, and truncated output.
- Require that incomplete evidence never becomes PASS.

### Stage 2: gate a real run
- Verify a $0 path or stop before execution.
- Obtain explicit approval before account creation or potentially billable workloads.
- Use synthetic code in a disposable sandbox only after egress, resource limits, termination, cancellation, and cleanup are verified.

### Stage 3: validate the loop
- Add small input/output files and short run history.
- Test AI code -> run -> copy report -> AI correction -> rerun before adding more runtimes or direct AI integrations.

### Stage 4: evaluate convergence
- Compare the shared contract and user journeys with RevDev.
- Decide whether a shared responsive app, shared backend with separate clients, or merged product is justified by evidence.
- Keep repositories separate unless the owner explicitly approves a migration.

## Open questions

- What exact fields and pass/fail rules does RevDev use?
- How does RevDev execute scripts, and what safety assumptions apply?
- Which script types and file formats are needed first?
- What execution limits are useful while preserving the $0 constraint?
- Is one responsive app eventually preferable to separate clients sharing a contract?

## Current reality

PocketCode's current prototype is static and simulated. No backend or real execution path exists. The execution contract and provider research are proposals. RevDev implementation details have not been inspected here, so compatibility is a target to compare, not a verified fact. No provider has been selected or tested; this proposal authorizes no cloud workload.


## Related product strategy research (2026-10-28)

See [RevDev + PocketCode Product, Architecture, and Commercial Strategy](../RESEARCH/REVDEV_POCKETCODE_PRODUCT_STRATEGY_2026-10-28.md) for the current research synthesis on competitor positioning, naming collision, App Store constraints, commercial hypotheses, and convergence options. This is research only: it does not override accepted decision D-001 (keep repositories separate), approve a rename/merge/provider/backend, or change the $0 budget. The recommended next seam remains a versioned, conformance-tested run/result/report contract; execution adapters and trust boundaries remain distinct.


## Conformance matrix (2026-10-28)

The [Shared Run/Result Conformance Matrix v0.1](SHARED_RUN_RESULT_CONFORMANCE_MATRIX_v0_1.md) turns the proposed common seam into 20 cross-product fixture cases, provenance rules, enforcement-boundary requirements, and staged adoption gates. It is a test plan only: no shared suite has been run, and it does not supersede the accepted decision to keep the repositories separate.

The [Shared Run/Result Conformance Gap Review (2026-10-28)](SHARED_RUN_RESULT_CONFORMANCE_GAP_REVIEW_2026-10-28.md) audits v0.1 against the existing PocketCode API, execution-loop, and security requirements. It proposes additional vectors for cross-user access, input limits, egress/secret isolation, quotas, cleanup, terminal-state races, and actual RevDev guard enforcement. These are gaps to test, not claims that any implementation passed.
