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
