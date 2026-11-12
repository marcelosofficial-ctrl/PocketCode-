# Opaque-origin browser execution protocol

Date: 2026-11-12
Status: proposed security and message contract; not implemented or device-verified.
Contract version: opaque-origin-execution/v1. This is a protocol version, not a canonical LOOP, CASE or D-ID.
Scope: browser-based execution of explicitly imported user code, parent/sandbox messaging, staged artifacts and teardown.

## 1. Ranked risk and scope

Rank 2 for this pass: browser Workers improve responsiveness but do not create a separate web origin. An untrusted Python task must not inherit PocketCode's cookies, DOM, browser storage, service-worker control or authenticated API access.

This contract covers the browser boundary only. It does not approve arbitrary code execution in production, prove hard CPU/memory quotas, choose a hosting domain or runtime, or close the implementation gate.

Trust classes:
- Trusted shell/supervisor: static, version-pinned PocketCode code responsible for frame bootstrap, limits, parent messaging, file staging and teardown. It is still browser-delivered code and must be integrity-controlled.
- Untrusted task: imported source, package hooks, Python code, generated code, WASM and all task output. Treat as adversarial even when supplied by the user.
- Parent application: authority for user gesture, identity, imported file selection, current policy, local persistence, report projection and artifact release.
- Browser boundary: opaque-origin sandbox reduces ambient web authority; it is not an OS process/container and does not provide a guaranteed memory quota.

Existing Pyodios observation remains unchanged: owner-reported iPhone app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2; [Bridge/executePython] PythonError; Console probe NOT RUN; worker topology UNKNOWN. Do not infer that the described frame/worker protocol is the topology of the installed app.

## 2. Non-negotiable isolation properties

1. The untrusted task never executes in the parent application's document or same-origin Worker.
2. The execution document is inside an iframe with sandbox token allow-scripts only. In particular, do not add allow-same-origin, allow-top-navigation, allow-top-navigation-by-user-activation, allow-popups, allow-popups-to-escape-sandbox, allow-forms, allow-downloads, allow-modals or pointer-lock grants.
3. The user task is not loaded as iframe HTML, srcdoc, a navigation URL or an imported script in the trusted supervisor. Only a fixed, trusted supervisor document is loaded.
4. Use a dedicated Worker created by that supervisor for task responsiveness and deadline-based termination. Worker isolation is not treated as an origin boundary; the opaque iframe is the origin boundary.
5. The worker receives no parent MessagePort, provider credential, cookie, authorization token, storage handle, generic network function or arbitrary JavaScript callback.
6. The parent/supervisor control channel is held only by the trusted supervisor. Worker messages are untrusted task output and cannot become authoritative lifecycle evidence merely because the supervisor received them.
7. No default network access. CSP and browser controls are both required; iframe sandboxing alone does not block every network request.
8. Inputs are explicit bounded copies selected by the user. Outputs are bounded staged bytes verified by the parent before entering the application's artifact store.
9. The MVP does not stream results or artifacts. OD-01 remains: stage the complete artifact, verify its length and digest, then authorize bounded download/share.
10. If a browser cannot enforce the required isolation or cancellation boundary on a target device, classify this execution mode as unavailable/INCOMPLETE; do not silently fall back to same-origin Pyodide.

## 3. Frame setup and browser policy

Frame source:
- The src is a fixed PocketCode supervisor entry point pinned to an immutable application release. No task-controlled URL, data URL, blob URL, srcdoc or user HTML is accepted as the frame document.
- Each DispatchAttemptId gets a fresh frame/session. Never reuse a frame after task execution or a protocol fault.
- The parent keeps the exact iframe element and its contentWindow reference. A different frame, even one with the same visible origin string, is a different authority context.
- The sandbox attribute contains allow-scripts and no allow-same-origin. The absence of allow-same-origin yields a unique opaque origin under the HTML sandbox model.
- Parent and supervisor apply restrictive Permissions Policy. Camera, microphone, geolocation, payment, USB, serial, clipboard, accelerometer and other powerful features are denied unless a separately approved requirement exists. No clipboard read/write path is part of this protocol.

Content Security Policy requirements:
- Default deny. Set connect-src 'none' to deny fetch, XHR, WebSocket, EventSource, sendBeacon and ping initiated by the sandbox.
- Also deny form submission, objects, nested frames, media, images, fonts, manifest and unneeded worker/script sources. Deny base URL mutation. Do not rely on connect-src alone to stop every possible request or navigation path.
- Permit only the exact immutable supervisor and interpreter/WASM resources required to boot. Do not use broad network host allowlists to work around a boot failure.
- Keep JavaScript unsafe-eval disabled. If a pinned Pyodide build demonstrably requires WebAssembly compilation permission, evaluate wasm-unsafe-eval separately; do not grant unsafe-eval as a substitute.
- If the selected interpreter requires a fetch or package download at run time, the default-deny network condition is not met. Preloading or explicit import may be designed separately; never enable arbitrary package/network retrieval as a silent fallback.
- Exact CSP source expressions for an opaque-origin document and the pinned Pyodide loader must be verified on target iOS Safari and Android browsers. They are NOT assumed proven by this document.

Origin and hosting:
- The opaque origin prevents ordinary same-origin access from the sandbox to the parent, but it does not prove that a separate hostname, deployment, or asset supply chain is secure.
- Current PocketCode Pages and portfolio URLs share host/scheme/port and remain one parent-origin trust domain. Different paths do not isolate parent storage or same-origin scripts.
- A dedicated execution hostname could provide an additional boundary, but host/domain/DNS changes and spending are not approved or selected. Do not assume one exists.
- Never store credentials, provider tokens, session identifiers or security authority in localStorage, IndexedDB, Cache API or OPFS on the shared origin.

## 4. Parent-to-supervisor handshake

Threat: opaque origins serialize as the string null in MessageEvent.origin. Many unrelated opaque origins also serialize as null. Therefore event.origin === "null" is not a unique sender identity.

Handshake:
1. Parent creates the fixed iframe, sets sandbox and restrictive policy before navigation, and retains the iframe's exact contentWindow reference plus a new local frame-generation value.
2. After the fixed supervisor loads, it sends HELLO with protocol version and a fresh supervisor-generated challenge. No secret or user data is included.
3. Parent accepts HELLO only when event.source is exactly that iframe's current contentWindow, event.origin is the expected opaque-origin marker, frame generation is current and the strict HELLO schema validates. The origin marker is an additional check, never the identity check by itself.
4. Parent creates a MessageChannel and sends one minimal INIT message with the transferred port to that exact contentWindow. Because the receiver has an opaque origin, a tuple targetOrigin cannot address it; the wildcard target is permitted only for this bootstrap to the retained exact WindowProxy. It must contain no provider credentials, session tokens, secrets or authority beyond the new channel.
5. INIT contains protocol version, one-time session nonce, CommandId, DispatchAttemptId, ExecutionId, per-attempt limits and the supervisor challenge binding. It contains no ambient credentials.
6. Supervisor verifies the parent message's exact parent origin and source, validates challenge/session shape, then binds the transferred port to this one execution. All subsequent control messages use the MessagePort, not window message events.
7. Parent never accepts a new window message as a continuation after channel establishment. Duplicate HELLO, replayed INIT, a stale frame generation or a message from another source closes the channel and fails the attempt.
8. Close both port ends and destroy the frame on completion, cancellation, malformed message, timeout or navigation.

The child-to-parent HELLO checks event.source === parent and the exact configured parent origin. Do not use wildcard target origins from the supervisor to the parent. The parent-to-opaque-child wildcard bootstrap is a narrowly scoped exception, not a general messaging rule.

## 5. Message envelope and allowlist

Every post-handshake message is a structured object with exactly these envelope fields:
- protocol: opaque-origin-execution/v1.
- session_nonce: one-time per-frame session binding.
- execution_instance_id: unique frame execution instance.
- command_id and dispatch_attempt_id: existing identities; they are not interchangeable.
- sequence: positive safe integer, monotonically increasing independently in each direction.
- message_id: unique within this execution direction.
- kind: one of the explicit message kinds below.
- payload: strict kind-specific object; reject unknown security-sensitive keys.

Limits:
- Validate message shape, direction, state and size before copying buffers or parsing deep structures.
- Bound source bytes, file count, per-file bytes, total input bytes, output file count, per-file/total output bytes, log bytes, message count, nesting depth and wall-clock duration. Exact numeric limits remain product requirements to be set before implementation; they are not invented here.
- Reject booleans where integer counters are expected; require finite integers in safe range. Large identifiers/counters use strings.
- Reject duplicate message IDs, gaps, replay, wrong execution/attempt/command, wrong direction, unknown message kind, unsupported protocol version and messages after terminal state.
- All data is hostile. Render logs and exception strings with textContent, never innerHTML or executable markup.

Allowed parent-to-supervisor kinds:
- INIT: one-time port/session setup, limits and explicit user-imported input copies.
- EXECUTE: one bounded task invocation, only after READY and policy checks.
- CANCEL: request to stop this exact attempt.
- SHUTDOWN: close the worker and supervisor.
No generic RPC, arbitrary function name, source-eval, URL fetch, storage operation or provider call is allowed.

Allowed supervisor-to-parent kinds:
- READY: fixed supervisor and protocol initialized.
- STARTED: supervisor accepted this exact execution request.
- FINISHED: task returned a result envelope and zero or more staged output candidates. These are task-reported results, not by themselves authenticated child-process exit evidence.
- CANCEL_ACK: supervisor confirms it requested termination of its exact worker and closed the task channel; this is a controller acknowledgement, not proof of OS-level containment.
- FAULT: protocol, worker, resource or validation fault with bounded diagnostic text.
- SHUTDOWN_ACK: supervisor reports local teardown completed.
No artifact is releasable on READY, STARTED, FINISHED, CANCEL_ACK or SHUTDOWN_ACK alone.

No stdout/stderr streaming is required in MVP. A bounded final log buffer may be returned with FINISHED; exceeding its cap terminates the task and records truncation/degradation.

## 6. Explicit file input and output protocol

Input:
- User selects/imports files explicitly. No clipboard polling, directory crawl, automatic phone file access or background capture.
- Parent validates count, byte length, safe file name/path and SHA-256 before transfer.
- Parent transfers immutable copies only. A worker receives the bytes and safe logical names, not a filesystem path to the parent or a general file picker.
- No implicit package install, remote import, environment variable, secret file, app database or parent storage access.
- File names reject absolute paths, drive prefixes, traversal segments, NUL/control characters and duplicate normalized names. Exact normalization rules must be identical in parent and supervisor.

Output:
- Supervisor receives task output from the worker as untrusted bytes and bounded metadata.
- Supervisor returns staged candidates over the control port only after the task invocation has ended or been cancelled. This is a bounded final message, not live streaming.
- Parent recomputes byte length and SHA-256 from received bytes, validates attempt/session binding and file name, and writes the verified copy through its own storage path.
- A supervisor-supplied digest is a claim, not proof. The parent digest is authoritative for the bytes it received.
- Missing, oversized, mismatched or malformed output is quarantined and marks collection INCOMPLETE. The supervisor cannot write into the parent's IndexedDB, OPFS, Cache API, service worker or report database.
- A successful digest proves byte integrity after transfer, not that the program was correct or that the client later received it.

## 7. Cancellation, teardown and evidence

Normal completion:
- Supervisor closes the child Worker, drains only bounded final output, sends FINISHED and then SHUTDOWN_ACK. Parent verifies message ordering and closes the port/frame.
- Worker-reported exception, success string or exit number is preserved as a task observation. It is not promoted to a native child-process exit status without an approved trusted runtime contract.

Cancellation:
1. Parent sends CANCEL bound to exact CommandId, DispatchAttemptId and ExecutionId.
2. Supervisor stops accepting task messages, invokes terminate() on the exact Worker object it created, rejects later worker messages and sends CANCEL_ACK only after that controller action.
3. Parent accepts CANCEL_ACK only on the current session port with current attempt/execution, correct message sequence and before the local deadline.
4. If acknowledgement is absent, malformed, late, stale or contradictory, parent removes the iframe, closes ports and records termination UNKNOWN and execution/job INCOMPLETE. It must not report cancelled, terminated or clean merely because the frame was removed.
5. Already emitted browser resource consumption cannot be retroactively recalled. Browser memory exhaustion, process suspension, engine defects or tab crashes may prevent the controller from completing.

Resource boundary:
- A trusted supervisor can enforce a best-effort wall-clock deadline and output/message caps by terminating its held Worker. This is stronger than asking untrusted Python to stop itself.
- The browser API does not expose a portable hard per-task memory quota or OS-like container resource accounting to this protocol. Browser-wide CPU scheduling, memory pressure, tab suspension and renderer crashes remain UNKNOWN.
- If requirements demand enforceable memory/CPU quotas, network denial beyond the tested CSP/browser boundary, host filesystem isolation or authoritative process exit status, browser-only execution is insufficient until a separate constrained executor is approved.
- Do not claim a hard sandbox or full resource containment from iframe sandbox + Worker alone.

Projection:
- Keep task-reported outcome, trusted supervisor lifecycle observation, parent cancellation/teardown observation, execution verdict, overall evidence/job disposition and artifact disposition separate.
- A missing same-attempt termination acknowledgement remains UNKNOWN. A missing required security barrier is INCOMPLETE.
- Preserve OD-09..OD-13. CASE-04 remains INCOMPLETE / timed_out until direct-child/wrapper/termination provenance and same-attempt authoritative acknowledgement satisfy its canonical acceptance.

## 8. Adversarial acceptance matrix

| Attack or fault | Required result |
|---|---|
| Missing allow-same-origin token | Required invariant; reject frame config if present |
| Same-origin plus allow-scripts | Reject as unsafe configuration |
| Different iframe sends HELLO with origin null | Reject because event.source is not the retained contentWindow |
| Expected iframe sends malformed/replayed HELLO | Close and fail the session |
| Replayed INIT or old frame-generation message | Reject; no execution |
| Wildcard used for any message beyond minimal opaque-origin bootstrap | Reject design review |
| Parent sends credential/token in INIT | Reject protocol/schema; bootstrap carries no secrets |
| Worker obtains or is transferred the parent MessagePort | Reject architecture; port remains only in trusted supervisor |
| Untrusted worker sends arbitrary kinds or huge messages | Supervisor rejects/caps and terminates worker |
| Worker message for stale attempt or wrong ExecutionId | Reject and record fault |
| Attempted fetch/XHR/WebSocket/EventSource/sendBeacon | Block under CSP and verify on target browsers |
| Attempted image, form, media, nested frame, object or navigation exfiltration | Block by CSP and sandbox policy; verify each available path |
| Attempt to access parent DOM/cookies/storage/service-worker registration | Denied by opaque origin and browser boundary |
| Input traversal/duplicate file names/oversized files | Reject before execution |
| Output changed after supervisor digest claim | Parent recomputes digest; quarantine on mismatch |
| Worker reports forged success/exit code | Preserve only as task-reported result, not trusted process verdict |
| Worker runs forever | Supervisor deadline terminates its exact Worker; record controller result |
| Worker allocates until renderer failure | Browser containment is UNKNOWN; never claim hard memory quota |
| CANCEL_ACK withheld or sent for another attempt | Termination UNKNOWN, job INCOMPLETE; parent closes frame |
| Artifact emitted before full staging/current authorization | Block release under OD-01/OD-02 |
| Parent/tab/browser crashes mid-task | Recover as interrupted/UNKNOWN; no inferred success |

These are acceptance cases for a future model/browser test suite. No browser or device test was run in this pass.

## 9. Research, maintenance and reuse

Official sources opened 2026-11-12:
- WHATWG HTML Living Standard iframe sandbox model: https://html.spec.whatwg.org/dev/iframe-embed-object.html. Living standard; opaque origin without allow-same-origin, and warning against combining allow-scripts with allow-same-origin for same-origin content. No code copied.
- MDN Window.postMessage: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage. Sender origin can change; exact source/origin validation and transferable ports; opaque origin requires narrow wildcard bootstrap. MDN content is CC BY-SA 2.5; requirements paraphrased, no text/code copied.
- MDN iframe reference: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe. Sandbox token semantics and same-origin escape warning. No code copied.
- MDN CSP connect-src: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/connect-src. Connect-src coverage for fetch/XHR/WebSocket/EventSource/sendBeacon/ping; other CSP directives still required.
- W3C Permissions Policy: https://www.w3.org/TR/permissions-policy/. Restrict powerful APIs; standards reference, no code copied.
- Pyodide web worker docs: https://pyodide.org/en/latest/usage/webworker.html. Versioned build documentation; current docs surfaced 314.1.0.dev0 and warn against unpinned dev URLs. User's installed 314.0.5 remains a separate reported version; no upgrade or runtime decision.
- MDN Worker.terminate(): https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate. Terminates the held Worker immediately; does not prove whole-browser process containment.
- Existing upstream incident: GitHub advisory GHSA-4r2p-27mh-5m22 / CVE-2026-59214, patched by Open WebUI 0.10.0. Advisory demonstrates same-origin Pyodide bridge risk. Open WebUI code/licence not reused; current branding restrictions make copying especially unsuitable.
- OWASP HTML5 Security Cheat Sheet, Worker and sandbox guidance: https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html. CC BY-SA 4.0; patterns paraphrased, no code copied.

Reuse decision: use browser-standard iframe sandbox, MessageChannel and dedicated Worker primitives rather than a proprietary isolation library. No framework or source code copied. Standards and browser behaviour must be rechecked against the exact target devices at implementation time.

## 10. Red-team corrections to prior sandbox research

1. The prior opaque-origin pattern did not fully explain that opaque origins serialize to null and cannot be distinguished by checking event.origin alone. Fix: exact event.source reference, per-frame generation and one-time nonce; port-bound messages after bootstrap.
2. The prior protocol did not account for the wildcard targetOrigin required when posting to an opaque-origin child. Fix: permit wildcard only for the minimal bootstrap to the exact retained iframe WindowProxy; no secrets or credentials; all later messages use the dedicated port.
3. The prior statement “default-deny network” could be read as an effect of iframe sandbox alone. Fix: strict CSP connect-src 'none' plus form/object/media/image/frame/script restrictions and adversarial checks; do not broaden the allowlist to get past interpreter boot issues.
4. The prior design understated the worker-to-supervisor trust boundary. Fix: never transfer parent MessagePort to the task worker; all task messages remain untrusted, including claimed success, exit code and cancellation.
5. The prior teardown language risked implying frame removal proved process death. Fix: parent requires a same-attempt controller acknowledgement; absent proof means termination UNKNOWN. Browser hard memory quotas and renderer failure containment remain UNKNOWN.
6. The previous design treated a worker as if it had a native child-process exit. Fix: separate task-reported completion from child-process exit and overall evidence disposition; preserve CASE-04 as INCOMPLETE / timed_out.

## 11. Gate and evidence boundary

VERIFIED: WHATWG, MDN, W3C, Pyodide and OWASP source materials listed above were opened on 2026-11-12. Current PocketCode constraints and OD-01..OD-13 were re-read from the active branch.
INFERRED: opaque-origin frame plus a supervisor-owned Worker and narrow MessageChannel is a reasonable browser-only architecture candidate for bounded tasks.
UNKNOWN: exact Pyodide 314.0.5 bridge topology, CSP compatibility of the actual build, iOS/Android support and behaviour, hard memory quotas, browser-level termination after renderer failure, live Pages headers and any separate execution hostname.
NOT RUN: browser protocol tests, CSP exfiltration tests, Pyodios Console probe, target-device tests, worker kill/crash tests or production adapter tests.

This is a proposed protocol, not implementation authorization or proof of security. No runtime, host, database, provider, transport or storage choice made. No canonical identifier changed. P39 implementation/adapter gate remains CLOSED; CASE-04 remains INCOMPLETE / timed_out.
