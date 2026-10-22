# PocketCode Execution Loop: Acceptance Criteria

**Status:** Proposed acceptance plan; not implemented or run  
**Budget:** $0 unless the owner explicitly changes it  
**Purpose:** Turn the AI → execution → evidence → AI correction loop into testable behavior before choosing or integrating a runtime.

## Product principle

PocketCode is not merely a mobile code editor or terminal. Its first useful job is to make AI-generated technical work executable from a phone and return trustworthy evidence the AI can use for the next iteration.

The first version does not need autonomous message interception. A reliable copy/paste loop is sufficient to validate the core value. Any deeper automation must be separately demonstrated on the target mobile platform.

## Verdict and run status

Keep the user-facing verdict separate from the execution lifecycle.

| User-facing verdict | Meaning | Required evidence |
|---|---|---|
| PASS | The requested program completed successfully | Trusted terminal result confirms completion and exit code 0 |
| FAIL | The program ran and a failure was confirmed | Non-zero exit code or a confirmed program/runtime failure |
| INCOMPLETE | The result is not a confirmed success or confirmed program failure | Timeout, cancellation, rejection, infrastructure failure, or missing/ambiguous terminal evidence |

The report must also preserve the exact lifecycle status where known: accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected, or infrastructure_failed. Acceptance is not execution. A browser timeout is not proof that the worker stopped. Missing evidence must never be silently converted to PASS.

A script's own per-check lines (for example, PASS/FAIL/SKIP/WARN) are program output unless PocketCode independently validates them. PocketCode must distinguish script-reported checks from facts verified by the execution service.

## Acceptance criteria

| ID | Requirement | Acceptance evidence | Current status |
|---|---|---|---|
| LOOP-01 | Phone-first code and input workflow | A user can paste a small script and attach individually selected input files without a PC | NOT IMPLEMENTED |
| LOOP-02 | Honest execution state | UI distinguishes validation, queued/running, and each terminal outcome; sample output remains visibly simulated | Static prototype only; no real run |
| LOOP-03 | Truthful PASS | PASS appears only after trusted completion evidence and exit code 0 | Proposed; NOT RUN |
| LOOP-04 | Truthful failure | Syntax/runtime error and non-zero exit are shown as program failures, not infrastructure failures | Proposed; NOT RUN |
| LOOP-05 | Incomplete result | Timeout, cancellation, rejection, or uncertain infrastructure outcome cannot be shown as success | Proposed; NOT RUN |
| LOOP-06 | Structured checks | Individual checks and their names/statuses remain visible; source of each check is identified | Proposed; NOT RUN |
| LOOP-07 | Useful diagnostics | Report includes run ID, runtime/version, final status, exit code and duration when known, bounded stdout/stderr, truncation markers, and output-file metadata | Proposed; NOT RUN |
| LOOP-08 | One obvious handoff | One primary Copy result action copies a complete, bounded, plain-text report; selectable text remains available if clipboard access fails | Static prototype only; simulated report |
| LOOP-09 | Repeatable correction loop | User can preserve the previous result, edit the script, rerun, and distinguish each run | Proposed; NOT RUN |
| LOOP-10 | File outputs | Generated files can be listed and downloaded; filenames and sizes are bounded and validated | Proposed; NOT RUN |
| LOOP-11 | Privacy | Copying a report does not silently include secrets, unrelated files, or unlimited source/output | Proposed; NOT RUN |
| LOOP-12 | Runtime isolation | Untrusted code runs only in a disposable, constrained environment; egress is denied by default and resource limits are enforced outside the code | No runtime/provider selected; NOT RUN |
| LOOP-13 | Mobile automation honesty | No claim of automatic AI-message capture, cross-app clipboard monitoring, or background execution without platform-specific proof | Design requirement |
| LOOP-14 | Zero-cost gate | No provider account, billing enablement, or potentially billable workload without explicit approval and verified zero-cost conditions | No provider selected; no workload run |

## Minimum adversarial and failure scenarios

These scenarios are proposals for the first real execution proof. They must be run against a controlled implementation before any capability is described as verified.

| ID | Scenario | Expected result |
|---|---|---|
| CASE-01 | Valid short script prints expected output and exits 0 | PASS; output and exit code match observed evidence |
| CASE-02 | Syntax error before program starts | FAIL if the runtime confirms a program error; show actual diagnostic output |
| CASE-03 | Runtime exception after partial output | FAIL; preserve bounded partial output and actual error |
| CASE-04 | Infinite loop or script exceeding the enforced deadline | INCOMPLETE / timed_out only when trusted execution control confirms the timeout outcome |
| CASE-05 | User requests cancellation while the run is active | Show cancellation confirmation or explicitly state that termination could not be confirmed |
| CASE-06 | Worker/provider fails before a trustworthy program result exists | INCOMPLETE / infrastructure_failed; never fabricate an exit code |
| CASE-07 | Output exceeds the configured limit | Enforce the limit; mark truncation or rejection explicitly |
| CASE-08 | Input file is missing or has an unsafe path/name | Reject safely before execution or return a clearly evidenced program failure, depending on when it is detected |
| CASE-09 | Script exits 0 but prints a line claiming a failed check | Overall execution may be PASS, but the script-reported failed check must remain visible; do not equate process success with task correctness |
| CASE-10 | Script prints “PASS” but exits non-zero | Overall verdict FAIL; preserve the conflicting text and actual exit status |
| CASE-11 | Browser loses connection while execution continues | On reconnect, recover authoritative server state; do not infer completion from the disconnect |
| CASE-12 | Report is copied after a failed or incomplete run | Report preserves the actual terminal state, uncertainty, diagnostics and truncation markers; no green/success wording is invented |
| CASE-13 | Same request is retried after an ambiguous network response | Idempotency prevents accidental duplicate execution where the backend supports it; unknown execution state stays unknown |
| CASE-14 | Output file attempts path traversal or exceeds limits | Reject the unsafe output and never expose a worker filesystem path as a download link |
| CASE-15 | Untrusted script attempts outbound network access or reads environment secrets | Network is blocked by enforced policy and no service credentials are present in the execution environment |
| CASE-16 | Two runs finish in a different order than they were started | Each report and output remains tied to the correct run ID; results are not crossed |

## Automation ladder

Build and validate these in order; later stages are not implied by earlier ones.

1. **Reliable manual loop:** paste/import → run → inspect → Copy result → paste to any AI → edit/rerun.
2. **Low-friction phone UX:** retain the last result, support input/output files, offer selectable report text, and make the primary action obvious.
3. **Platform-supported conveniences:** investigate share sheets, file-provider integration, notifications, or shortcuts only after checking actual OS and browser restrictions.
4. **Direct AI integration:** consider explicit integrations only if a supported API and an affordable, secure authentication model exist.
5. **Autonomous loop:** consider automatic capture, execution, and continuation only with explicit consent, clear run boundaries, safeguards against replay/injection, and demonstrated platform support.

A completion sound or notification is a convenience, not proof that a run succeeded. The authoritative report remains the source of truth.

## Report design rules

- Use stable, parseable field labels and plain text so any AI assistant can consume the report.
- Include observed facts and clearly label unavailable values.
- Bound stdout, stderr, check count, file count, and report size; mark all truncation.
- Preserve individual checks, including failures, rather than only displaying a summary.
- Distinguish process exit success from whether the user's broader task was accomplished.
- Never trust a script's self-reported status as proof of isolation, security, or correctness.
- Keep report copying user-initiated. Never include private files or credentials implicitly.
- Retain a run identifier so later corrections can be compared to the exact previous result.

## Out of scope for the first proof

- Guaranteed automatic interception of messages from ChatGPT, Gemini, or other apps.
- Monitoring the system clipboard or reading other apps in the background.
- Unrestricted shell, arbitrary package installation, or general Internet access from user code.
- Remote control of a PC.
- Persistent accounts, cloud history, project synchronization, or multi-user workspaces.
- Paid services or potentially billable execution without explicit owner approval.

## Definition of first useful proof

The first useful proof is complete only when a controlled, real run demonstrates one success case, one program failure, one timeout, one bounded report, and one input-to-output file transformation; the report can be pasted into a separate AI assistant and used for a correction; and the isolation, egress, resource-limit, cancellation, and cleanup gates have evidence. Until then, execution and provider integration remain proposals, not product capabilities.
