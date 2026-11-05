# Mobile Runner Evidence Sourceability Matrix — 2026-11-05

**Status:** Design/research only. This maps the existing receipt concepts to plausible evidence authorities; it does not create a new receipt schema, select a runner, or claim device verification.  
**Authority:** The existing [Mobile Runner Task and Evidence Receipt Specification](../AI_COLLAB/MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md) and canonical LOOP/CASE suites remain authoritative.

## Executive decision

Do not expand the receipt merely because a competitor exposes a field or a backend has a status endpoint. Each displayed fact must have an identified authority at the selected execution boundary. If the boundary cannot provide it, show unavailable/unknown or omit it according to the existing receipt contract.

The report must preserve distinct concepts:
- execution outcome;
- coordinator/job disposition;
- wrapper/transport status;
- cleanup;
- artifact existence and artifact-release authorization;
- capture state and evidence provenance.

A server accepting a request, an HTTP 200 response, a client-side timer expiring, or a UI spinner stopping is not proof that user code succeeded, timed out, was cancelled, or terminated.

## 1. Field-to-authority map

| Existing receipt concept | Authoritative source required | Example evidence source | What must not be inferred |
|---|---|---|---|
| Execution status | The runner/coordinator lifecycle owner for the actual attempt | Local process supervisor; remote worker event/status read-back | UI phase, HTTP status, client timeout or model statement |
| Job disposition | Scheduler/control plane, only when a job was dispatched | API's typed accepted/queued/running/rejected state plus durable job identity | Do not invent a job ID for local execution. A static demo is NOT_APPLICABLE. |
| Runtime identity/version | Selected runner's actual runtime metadata | Runner image/runtime manifest; local interpreter version captured at launch | A language label in the UI or a conceptual Python version |
| Start/end/duration | Execution boundary with a monotonic clock | Runner-side timestamps/duration; local monotonic timing around the actual process lifecycle | Wall-clock difference from unrelated UI events; timing in a simulation |
| Exit status | Process/runner that owns the actual command result | Captured interpreter/process exit code with documented scope | HTTP 200, wrapper exit code, collector exit code or inferred success |
| stdout / stderr | The process-output collector | Separate byte streams with independent capture/truncation state | A blank panel means empty; data from another attempt; UI-generated example text |
| Timeout | Supervisor/OS boundary that actually enforces the deadline and observes termination | Deadline trigger plus confirmed process termination or authoritative timeout result | Client-side timer alone; request cancellation; missing response |
| Cancellation | Execution boundary's confirmation of cancellation/termination | Typed cancellation accepted and terminal state/termination evidence | Button pressed, HTTP request sent, relay stopped, app backgrounded |
| Artifacts | Actual workspace/filesystem or runner artifact store | Post-run file listing, metadata and optional digest from the same attempt | Fixture-expected file; stale workspace file; file card drawn by UI |
| Cleanup | Boundary that owns process/workspace teardown | Cleanup-complete event and resource identity | Hiding a file, deleting a UI card, app close or presumed ephemeral workspace |
| Artifact release | User-authorized export/share boundary | Explicit user action and successful export/share result | File existence or successful execution alone |
| Redaction/provenance | Report builder with field-level source classification | Safe allowlisted projection plus source observation/availability state | Blindly copying full environment, shell output, tokens or private logs |

## 2. Capability facts from the inspected iOS reference

The a-Shell project demonstrates a real iOS terminal with local commands and file workflows. Its public `Relay.swift` source implements HTTPS, configurable bind address, bearer-token authentication, optional mutual TLS, separate stdout/stderr capture, an output cap and a bounded request queue. Its relay integration script checks ordinary success, non-zero command status, pipes, output limits, token rejection and client-certificate behavior.

The same reference explicitly reports no execution timeout. Its README states no client cancellation is provided and a running command continues after the client disconnects or relay is turned off. The relay executes under the app's file and network permissions; it is not a restricted shell or sandbox.

Therefore, a-Shell can inform the local-runner comparison and demonstrate actual stdout/stderr and command status collection. It must not be used as proof of strong process isolation, deadline enforcement, remote cancellation or background execution. The shell's HTTP status and the command's returned `status` are separate facts.

Sources:
- https://github.com/holzschu/a-shell/blob/master/a-Shell/Relay.swift
- https://github.com/holzschu/a-shell/blob/master/tests/relay.sh
- https://github.com/holzschu/a-shell#run-commands-remotely-with-relay

## 3. Required evidence discipline by execution location

### Local native runner

The local runner may know its own process lifecycle, output streams, runtime identity and generated files. It should not claim remote job disposition or server-side cleanup. Whether it can enforce process-tree termination, hard resource limits, network restrictions or a deadline is platform-specific and must be measured. iOS background suspension must be treated as an interruption risk, not as a successful timeout.

### Browser/WASM runner

The browser runtime can expose its own interpreter/runtime metadata, virtual filesystem and captured output if the adapter collects them. WebAssembly alone does not prove a safe sandbox against all host APIs, worker/resource exhaustion, browser integration or egress. Cooperative interruption and a true external hard deadline are different claims. Do not fabricate OS process IDs or native child exit codes when no native child exists.

### Remote PC runner

The remote agent/PC is the authority for process start, terminal state, exit status, output capture and workspace artifacts. The phone is a client. Reconnect should retrieve the same attempt by stable identity and cursor, not submit the original command again. A disconnected phone does not imply the PC process stopped.

### Hosted worker

The service must separate request acceptance, queue/job state, execution state, program result and cleanup. The client may show a typed job disposition, but only the worker/supervisor can prove execution termination and cleanup. Read-back after ambiguous acknowledgement is required before retrying a side effect.

## 4. Capture-state rules

Reuse the current receipt's explicit output states:
- `SAMPLE CONTENT`: authored fixture or demonstration content;
- `CAPTURED EMPTY`: collector ran and observed zero bytes;
- `UNAVAILABLE`: the selected boundary does not expose or retain the stream;
- `NOT OBSERVED`: no trustworthy observation exists.

Do not map missing data to empty output. Do not change `NOT_CREATED` into proof of absence unless the same attempt's fresh workspace was actually inspected. A sample file expected by a fixed fixture remains an expected value until a real runner creates and reports it.

## 5. Proposed field-level provenance labels

These are explanatory source labels for implementation/review, not new canonical receipt fields:

| Provenance | Meaning | Example |
|---|---|---|
| Observed | Captured from the authoritative boundary for this attempt | Process exit code, actual stderr bytes, file digest |
| Derived | Deterministically computed from observed evidence | Duration from monotonic start/end; SHA-256 over captured artifact bytes |
| Fixture-defined | Expected by the frozen test fixture, not seen at runtime | Expected `summary.json` content in the static prototype |
| Unavailable | Boundary lacks the capability or does not expose this fact | No child exit code on a browser-only runtime |
| Unknown | A fact might exist but could not be established | Lost acknowledgement; uncertain process termination |

Every value should be tied to task/attempt identity and should retain uncertainty. A derived value must identify its underlying observations. Do not use fixture-defined expectations as observed data.

## 6. Acceptance alignment and implementation gates

This matrix refines evidence collection only. It does not change LOOP-01..14, CASE-01..16 or their expected values.

Before a real receipt is accepted:
1. Identify which process or service owns the lifecycle and which adapter observes it.
2. Bind each observation to the same task and attempt identity.
3. Capture output and artifacts before reporting terminal completion.
4. Keep wrapper status, child/command result and infrastructure result distinct.
5. Verify timeout/cancellation at the execution boundary.
6. Verify cleanup independently from execution result.
7. Keep artifact release separate and user-authorized.
8. Test interruption, duplicate observation, lost acknowledgement and stale attempt data.
9. State unsupported capabilities as unavailable/unknown rather than simulating them.

**Current state:** no mobile runner, browser runner or hosted boundary has been selected or tested. The current prototype remains a labelled simulation. This document is not evidence of an actual run.


## 7. Field-level sourceability and requirement classification — 2026-11-05

This classification is about what a truthful receipt must represent, not a promise that every runner can produce every fact. **Mandatory representation** means the receipt must state the value or an explicit unavailable/unknown state when the concept applies. It does not authorize fabricating a value to fill a field.

| Receipt concept | Requirement class | Authoritative source | Safe representation when unavailable | Prohibited inference |
|---|---|---|---|---|
| Task/attempt identity | Mandatory when an actual attempt exists | Coordinator-created identity before dispatch, or local runner identity at actual run creation | No run ID for a simulation; UNKNOWN if an existing attempt cannot be recovered | UI/demo identifier treated as a real run |
| Execution status | Mandatory for an actual attempt | Lifecycle owner: local supervisor, remote worker, or browser runner adapter | UNKNOWN / NOT OBSERVED if authority cannot be queried | UI phase, spinner, HTTP response, assistant claim |
| Job disposition | Conditional: only if a scheduler/remote job was dispatched | Scheduler/control plane with durable job ID and typed state | NOT_APPLICABLE for purely local execution; UNKNOWN if a dispatched job cannot be read back | Inventing a job ID or treating HTTP 200 as execution |
| Runtime identity/version | Conditional: a runtime was selected and launched | Actual interpreter/runtime metadata captured at launch; worker image/manifest | NOT_SELECTED before launch; UNAVAILABLE/UNKNOWN if launch metadata is not exposed | Language label or planned version as actual runtime |
| Start/end/duration | Optional unless an existing case explicitly requires it | Execution boundary with a monotonic clock; duration is DERIVED from same-clock observations | NOT OBSERVED / UNAVAILABLE | Wall-clock subtraction across unrelated clocks or UI timestamps |
| Exit status | Conditional: only where the execution boundary exposes a command/process result | Child process or runner result, with scope stated | UNAVAILABLE for a path with no native child exit; UNKNOWN if lost | HTTP, wrapper, collector, or coordinator exit substituted for child exit |
| stdout and stderr | Mandatory capture-state representation for each stream; raw bytes are conditional on safe capture/export | Per-attempt output collector | CAPTURED EMPTY only after collector observes zero bytes; otherwise UNAVAILABLE or NOT OBSERVED | Blank panel interpreted as empty; one stream inferred from the other |
| Truncation/byte counts | Conditional when output is bounded; truncation state mandatory if a cap is reached | Collector at the point bytes are counted/discarded | UNKNOWN if collector metadata is lost | Treating retained prefix as complete output |
| Timeout | Conditional when a deadline actually fires | Trusted execution supervisor that owns/enforces the deadline and observes terminal/termination state | Distinguish client wait timeout from execution timeout; UNKNOWN if process termination is unconfirmed | Client timer, request timeout, missing response or UI stop treated as runner termination |
| Cancellation | Conditional when cancellation is requested | Execution boundary's typed cancellation and terminal/termination evidence | REQUESTED / ACCEPTED / TERMINATION_UNCONFIRMED as separately observed; UNKNOWN if authority is unavailable | Button press or cancel HTTP request treated as confirmed cancellation |
| Artifacts | Conditional when the selected path has a workspace/artifact store | Same-attempt filesystem inventory or runner artifact store read-back | NOT_APPLICABLE only if no workspace/artifact capability exists; UNKNOWN if inventory failed | Fixture expectation, stale file, UI card, or filename alone treated as generated artifact |
| Artifact digest | Optional derived evidence | Hash over actual bytes read from the same-attempt artifact | UNAVAILABLE if bytes cannot be read safely | Hash of expected fixture content treated as observed artifact integrity |
| Cleanup | Conditional when the runner allocates resources requiring teardown | Boundary that owns workspace/process/resource cleanup | NOT_APPLICABLE only when no such resource was allocated; otherwise UNKNOWN/FAILED/NOT_CONFIRMED | App close, hidden card, missing directory, or execution success treated as cleanup |
| Artifact release/export | Conditional when user requests export/share | OS file/share boundary and successful completion result | NOT_IMPLEMENTED / NOT_AUTHORIZED / NOT_OBSERVED as appropriate | File existence or execution success treated as a completed export |
| Error/stage provenance | Conditional when an error occurs; source label mandatory | Process stderr or typed runner/coordinator/transport failure at the owning stage | UNAVAILABLE / UNKNOWN with the failing stage preserved if known | User-code failure inferred from wrapper/network failure |
| Field provenance/redaction | Mandatory for every emitted fact | Report builder's allowlisted projection tied to source observations | OBSERVED / DERIVED / FIXTURE-DEFINED / UNAVAILABLE / UNKNOWN | Copying unrestricted environment, credentials, private logs, or model-generated facts |

### 7.1 Control-plane evidence that is separate from the receipt

Durable result commit, publication acknowledgement, journal recovery, and history retention are essential to the product's continuity goals, but they are not interchangeable with execution observations. Keep them as separate control-plane/storage evidence unless the canonical receipt contract is explicitly revised. A UI displaying a result does not prove it was durably committed; a storage acknowledgement does not prove the child program succeeded.

### 7.2 Sourceability gaps and current disposition

- **No selected mobile runner:** no actual iOS/Android lifecycle, exit, output, artifact, cleanup, cancellation, or timeout source has been verified. All target-product evidence remains NOT RUN.
- **iOS local execution:** app backgrounding/suspension is an interruption risk. A local runner must prove its own lifecycle and termination semantics; a phone-side timeout cannot stand in for them.
- **Browser/WASM:** runtime and virtual-filesystem observations may be available from an adapter, but a browser runtime does not inherently expose a native child process, native exit code, OS process-tree termination, or hard resource enforcement.
- **Remote PC:** the PC/agent is authoritative for execution and cleanup. The phone's disconnect or timeout is only a client observation; reconnect must query the same attempt identity rather than redispatch.
- **Hosted worker:** acceptance, queue state, execution result, cleanup and artifact release belong to different authorities and must be read back separately.
- **a-Shell reference:** inspected source provides actual command status and separate stdout/stderr, but the reviewed reference has no execution timeout or client cancellation and is not a sandbox. It is a capability comparator, not proof for PocketCode.
- **Artifact release:** an actual Files/share-sheet completion result is not currently implemented or tested in PocketCode. Do not show a real downloadable artifact in the simulation.
- **Durability:** receipt sourceability does not prove the history journal/outbox is durable or recoverable. That requires separate storage/transaction/restart evidence.

No row in this table is an implementation claim. The matrix remains a design/sourceability audit; LOOP-01..14 and CASE-01..16 are unchanged, and no mobile receipt or runner test has run.
