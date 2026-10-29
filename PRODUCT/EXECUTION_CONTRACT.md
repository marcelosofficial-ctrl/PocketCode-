# PocketCode Execution Contract (Proposed)

**Status:** Provider-neutral design proposal. Not an implemented API and not yet an approved public contract.  
**Updated:** 2026-10-20  
**Purpose:** Define the smallest execution interface before choosing a provider or framework.

## Goals

- Make one bounded Python run usable from a mobile browser.
- Keep provider credentials and privileged configuration on the server.
- Distinguish a program failure from a platform failure.
- Return verifiable execution evidence without promising unsupported behavior.
- Keep the API independent of a specific provider SDK.

## Non-goals for the first proof

No autonomous LLM loop, arbitrary shell access exposed as a public product feature, arbitrary runtime images, unrestricted package installation, persistent project workspace, multi-user collaboration, or guarantee of network access.

## Conceptual lifecycle

A run has exactly one terminal outcome. The server is authoritative; client-side timeouts are not evidence that execution stopped.

States:
- **accepted**: request passed validation and a run record was created.
- **queued**: waiting for execution capacity.
- **running**: provider confirms execution started.
- **succeeded**: program ended with exit code 0 and the provider returned a complete result.
- **program_failed**: program ended with a non-zero exit code or reported a language/runtime failure.
- **timed_out**: trusted server/provider enforcement ended the run because its deadline expired.
- **cancelled**: trusted execution control confirms cancellation/termination.
- **rejected**: request failed validation or policy checks before execution.
- **infrastructure_failed**: provider/coordinator failure prevented a trustworthy program result.

Accepted and queued are nonterminal. A client disconnect does not cancel or complete a run by itself. Any automatic cancellation-on-disconnect policy must be explicit and tested.

## Conceptual request

The first implementation should accept only a small JSON/multipart request with fields equivalent to:

- idempotency key: random client-generated value scoped to the authenticated user.
- runtime: allowlisted identifier; initially only Python with a server-pinned image/runtime version.
- entrypoint: constrained filename within the uploaded workspace; not an arbitrary host command.
- files: bounded set of named file contents; safe names only, with explicit byte limits.
- limits: no user-selectable increases. Server applies configured wall time, memory, CPU, process, disk, file-count, and output caps.

Authentication and user identity come from the API session/token, never from a client-supplied user ID. Provider credentials, image references, network policy, mounts, secrets, and host configuration are not client-controlled fields.

The contract must define maximum request size, maximum individual file size, maximum file count, filename normalization, allowed encoding/binary behavior, and behavior for duplicate filenames before implementation begins. Initial values are configuration decisions, not fixed by this document.

## Conceptual result

A result should contain:
- stable run ID;
- current/terminal state;
- runtime identifier and pinned runtime/image version;
- timestamps and measured duration when provided by a trusted source;
- exit code only if actually available;
- bounded stdout/stderr plus explicit truncation flags;
- bounded output file metadata and authenticated download links/handles;
- a stable error category and concise message for rejection/infrastructure failure;
- a report-ready summary that distinguishes observed facts from missing data.

Do not expose raw provider errors, host paths, internal IPs, credentials, stack traces from the control plane, or infrastructure identifiers to end users. Store operational diagnostics separately with access controls.

## Idempotency and retries

- The same authenticated user and idempotency key must not create multiple billable runs during the documented retention window.
- Reusing the key with a different request body must return a conflict, not silently execute the changed body.
- Provider retries must not turn an unknown result into success. If the provider cannot confirm whether a run executed, represent that uncertainty as an infrastructure error or explicit unknown state; do not report a fabricated exit code.
- A retry policy must define whether a new run is allowed after a terminal failure and how it is linked to the previous run.

## Cancellation and deadlines

- The server records a trusted deadline before dispatch.
- The provider's maximum lifetime is configured server-side and must not exceed the product's maximum.
- A client cancel action requests cancellation; the API must report whether cancellation was confirmed, already terminal, or could not be confirmed.
- If the provider cannot guarantee termination after timeout/cancel, this is a provider-selection blocker for untrusted code.
- Idle timeouts are not substitutes for an absolute maximum lifetime.
- Cost caps are enforced by the server/coordinator, not only by UI behavior.

## File safety

- Normalize filenames and reject absolute paths, traversal segments, NUL bytes, platform-specific path escapes, and unsafe archive entries.
- Do not extract archives until an archive-specific validation policy exists; the initial proof can accept individually uploaded files only.
- Enforce request, per-file, total-input, output-file-count, per-output, total-output, and output-expansion limits.
- Never return a worker filesystem path as a download URL.
- Output downloads must be authenticated, scoped to the owner of the run, and expire or be deleted according to documented retention.
- Treat all filenames and file content as untrusted when rendering or processing them.

## Network policy and secrets

- No application, provider, model, Git, or user credentials are passed into untrusted program execution.
- Outbound networking is disabled by default. If a candidate cannot demonstrate enforceable network restrictions outside the untrusted process, do not use it for arbitrary public code.
- Do not assume HTTP proxy environment variables alone enforce egress restrictions.
- If package installation is later required, design a separate allowlisted dependency-fetching strategy; do not silently enable general Internet access.
- Do not rely on regex log redaction as the primary secret-protection mechanism.

## Execution outcome versus artifact release

Execution verdict and artifact release are separate decisions.

- A process/run may be **PASS** when trusted terminal evidence confirms success and exit code 0, subject to the evidence gates explicitly required by the applicable acceptance case.
- A task that does not generate files may still PASS. An empty output-file list is not a universal execution-failure condition.
- If output files exist, report their observed metadata and uncertainty honestly. Do not invent an artifact, manifest, or successful publication.
- A successful execution does not grant current authorization to download/release an artifact. If an artifact exists and release is requested, re-check the current authorization, exact run/attempt association, trusted manifest, quarantine/lifecycle state, safe object identity, size/type/path policy, and exact immutable bytes at the release boundary.
- A release denial, missing artifact, quarantined artifact, or stale authorization must not rewrite the historical execution verdict. Report execution outcome and artifact availability/release status separately.
- If a particular acceptance case requires a named output artifact, that case's explicit condition applies. This is not a universal artifact-presence gate for artifact-free tasks.

This is a proposed contract clarification only. It does not select a store/API/provider, assert implementation, or override canonical LOOP/CASE acceptance.

## Report format

The user-copyable report should be bounded and human-readable, with fields such as:
- PocketCode run ID;
- runtime/version;
- final status;
- exit code if known;
- duration if known;
- stdout/stderr (truncated with clear markers);
- output file names and sizes;
- exact uncertainty or missing fields;
- no credentials, private control-plane details, or unbounded source/output by default.

The report must not claim that an AI fixed the code, that the code is correct, or that a run succeeded unless the result supports that statement.

## Canonical copyable report (proposed)

The report is plain text first. A UI may render it as a pink result block, but the copied text must preserve stable field names and remain understandable when pasted into any AI assistant.

Example of a **synthetic illustration only**; these values are not evidence of a real PocketCode run:

```text
POCKETCODE RUN REPORT
Report format: 1
Run ID: demo-run-001
Verdict: FAIL
Execution status: program_failed
Runtime: Python 3.x (illustrative; actual version must be supplied by the runner)
Exit code: 1
Duration: 0.42 s (illustrative)
Evidence source: controlled runner result
Task summary: Convert input.csv into cleaned.csv

CHECKS REPORTED BY PROGRAM (not independently verified by PocketCode)
- PASS | input_file_exists | Input file was found
- FAIL | required_column_present | Missing column: email

EXECUTION OUTPUT
stdout:
Validation started.
1 check passed, 1 check failed.

stderr:
ValueError: required column 'email' not found

Output files:
- none reported

Truncation:
- stdout: no
- stderr: no
- check list: no

Uncertainty / notes:
- The process failure is supported by the runner's terminal status and exit code.
- The listed checks are script-reported; PocketCode has not independently validated their truth.
- Example values are illustrative and must never be displayed as a real run.
```

A real report must omit unknown values or mark them `unknown`; it must not reuse the illustrative runtime, timing, run ID, output, or checks. A report generated from sample UI state must be visibly labeled `SIMULATED EXAMPLE — NOT AN EXECUTION` in both the UI and copied text.

### Required report semantics

- **Verdict** describes what the runner can prove about the process outcome, not whether the user's broader goal is correct.
- **Execution status** is the authoritative lifecycle outcome. Never infer `succeeded` from HTTP acceptance, a UI animation, or text printed by the script.
- **Evidence source** must distinguish trusted runner metadata from script output and user-provided claims.
- **Checks** must have provenance: runner-verified, program-reported, or user-supplied. Do not mix these without labels.
- **Exit code** and **duration** are optional only when genuinely unavailable. Do not fabricate them to make the report look complete.
- **stdout**, **stderr**, checks, filenames, and the complete report have server-enforced or otherwise trusted size bounds. Every truncation is explicit.
- **Output files** list safe display names and sizes only. Download links, when added, must be scoped to the authenticated owner and expire according to a defined policy.
- The copied report excludes secrets, environment variables, unrelated files, and full source code by default.
- Report format changes require a version increment or backward-compatible extension. Consumers should tolerate unknown optional fields.

### Report formatting checks to implement

1. A confirmed exit code of zero plus a confirmed terminal success can produce `PASS`.
2. A confirmed non-zero exit or confirmed program/runtime error produces `FAIL`.
3. Timeout, cancellation, rejection, missing terminal evidence, or infrastructure uncertainty produces `INCOMPLETE`.
4. A script's printed `PASS` cannot override a non-zero exit code.
5. A script-reported failed check remains visible even if the process exits zero; process success does not prove task correctness.
6. Missing exit code or duration is represented honestly, not replaced by a default.
7. Truncated output is marked, with no claim that the report contains all output.
8. Simulated reports are labeled as simulated in the UI and copied text.
9. Empty stdout/stderr and no generated files are rendered distinctly from missing/unavailable data.
10. All user-controlled strings are safely escaped in the UI and bounded before inclusion in the report.

## Acceptance tests

| Test ID | Contract behavior | Pass condition |
|---|---|---|
| PC-API-001 | Request validation | Unsupported runtime and oversized requests rejected before provider dispatch |
| PC-API-002 | Authentication/authorization | User A cannot read/cancel/download User B's run |
| PC-API-003 | Idempotency | Repeating same key/body does not create a second run |
| PC-API-004 | Idempotency conflict | Same key with different body is rejected |
| PC-API-005 | Terminal status | Exactly one authoritative terminal result is persisted |
| PC-API-006 | Program vs infrastructure failure | Distinct states and safe user messages |
| PC-API-007 | Timeout | Trusted deadline stops execution and records timed_out only when supported by evidence |
| PC-API-008 | Cancellation | Result reflects confirmed cancellation or honestly reports uncertainty |
| PC-API-009 | Output caps | stdout/stderr and file outputs cannot exceed configured bounds |
| PC-API-010 | Path safety | Traversal and unsafe paths rejected |
| PC-API-011 | Download ownership | Download handle cannot be used by another user |
| PC-API-012 | Report safety | Report is bounded and does not contain provider credentials or control-plane secrets |
| PC-API-013 | Disconnect/reconnect | Reopening the page recovers the authoritative run state |
| PC-API-014 | Cleanup | Run workspace and files follow the defined retention policy |

These tests are proposed. None is marked passed until implemented and executed in a controlled environment.

## Decisions intentionally left open

- HTTP polling versus server-sent events/WebSocket for result updates.
- Authentication provider and session implementation.
- Exact file/timeout/output quotas.
- Database and temporary-file storage.
- Provider-specific execution API and adapter implementation.
- User-visible retention period and deletion semantics.
- Whether the first proof needs accounts or can use a strictly private test harness.

## Definition of done for the first implementation

The implementation can be considered a candidate for a controlled internal proof only when:
1. The API validates and bounds inputs before provider dispatch.
2. The server applies fixed runtime and resource limits.
3. The lifecycle and error mapping are truthful.
4. Files and reports are scoped to the authenticated user and bounded.
5. The security launch gates in SECURITY.md are mapped to tests.
6. The tests above are implemented with explicit evidence.
7. A real provider run has been performed and documented without exposing secrets.
8. No public arbitrary-code execution endpoint is enabled until isolation, egress, cleanup, and abuse controls pass review.
