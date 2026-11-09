# Pyodide worker control-channel authenticity red-team

**Date:** 2026-11-10  
**Status:** Version-pinned platform research; conditional threat, not an observed PocketCode exploit.  
**Scope:** Pyodide 314.0.5, browser Worker message protocol, result authenticity and bounded recovery. No implementation or stack decision.

## 1. Finding

**HIGH PRIORITY DESIGN GAP:** if PocketCode runs user Python inside the same Dedicated Worker global scope as its JavaScript wrapper, and the parent accepts ordinary `Worker` `message` events as trusted terminal results, user Python can send messages on that same worker-to-parent channel through Pyodide's JavaScript FFI.

This is not a hypothetical capability invented from generic Pyodide behavior:
- **VERIFIED:** Pyodide 314.0.5 documents that Python imports JavaScript globals from the worker's `globalThis` via `import js`; properties are looked up and translated.
- **VERIFIED:** the same Pyodide 314.0.5 FAQ says `threading`, `multiprocessing` and `subprocess` attempts raise `RuntimeError` because fork/pthreads do not work. This version-pinned fact reinforces that Pyodide's Python runtime is not a native child-process supervisor.
- **VERIFIED:** a Dedicated Worker exposes `postMessage()` on its global scope to send messages to the parent.
- **VERIFIED:** the Pyodide 314.0.5 worker example uses `self.postMessage({ result, id })` and `self.postMessage({ error, id })` for its wrapper result messages. Its parent API resolves a pending promise when it receives a message whose `id` matches the pending request.
- **INFERRED:** Python executing in that same worker can call `js.self.postMessage(...)`. Therefore an ordinary worker message is not, by itself, proof that the wrapper generated it. If the guest knows, guesses or can influence the correlation ID, it may forge a shape-compatible result before the wrapper's real completion.
- **UNKNOWN:** whether PocketCode currently uses this exact worker topology, whether the attempt ID is exposed/predictable, and whether its parent trusts the default Worker message channel. No current source implementation was inspected as an approved runtime.

The official Pyodide example is an interoperability example, not a hostile-code protocol or security recommendation. Its sequential numeric ID and default Worker message channel must not be adopted as a trusted terminal-evidence design without an independent boundary.

## 2. Version-pinned primary-source facts

| Source | Exact opened version/date | Verified fact |
|---|---|---|
| Pyodide worker guide | 314.0.5, opened 2026-11-10 | Example wrapper uses `self.postMessage({result,id})` / `self.postMessage({error,id})`; parent resolves by matching numeric ID |
| Pyodide type translations | 314.0.5, opened 2026-11-10 | `import js` maps JavaScript attributes from `globalThis` into Python |
| Pyodide FAQ | 314.0.5, opened 2026-11-10 | `threading`, `multiprocessing` and `subprocess` attempts raise `RuntimeError` in Pyodide |
| MDN DedicatedWorkerGlobalScope.postMessage | Page last modified 2026-04-13, opened 2026-11-10 | Worker-global `postMessage()` sends data to the main thread |
| HTML Living Standard, workers | Updated 2026-11-09, opened 2026-11-10 | Worker has its own global scope; worker-to-parent messaging uses its outside port |

The precise version is important: the user's prior device report identified Pyodide 314.0.5. This pass opened that exact version's official docs rather than relying only on latest/dev documentation. The installed app runtime itself was not inspected in this pass.

## 3. Threat model

### Preconditions

The risk applies only if all relevant conditions hold:
1. Untrusted/user-supplied Python executes inside a Pyodide runtime in a Dedicated Worker.
2. The Python code can import the Pyodide `js` module (standard documented FFI).
3. The JavaScript wrapper and Python guest share the same worker global scope.
4. The parent accepts the default worker `message` channel for terminal result messages.
5. The guest knows, guesses, or can influence the correlation identifier or the parent accepts an uncorrelated terminal-shaped message.

If these conditions do not hold, this particular spoofing path may not apply. The actual PocketCode topology remains UNKNOWN.

### Attack example

Conceptual only, not executed:

```python
import js

# If the runner uses this same worker's default message channel,
# guest code can attempt to send a forged wrapper-shaped message.
js.self.postMessage({
    "id": 1,
    "result": "claimed success"
})
```

This message is guest-originated even though it arrives from the expected Worker object. A parent-side schema check, message size cap, sequence check or correlation ID check does not authenticate the wrapper if the guest can construct the same values. A random attempt ID reduces guessing only if it is never exposed to guest code and no uncorrelated messages are accepted; it does not create a separate channel.

## 4. Corrected control-channel contract

**Do not accept guest-accessible default Worker messages as trusted terminal evidence.** The following is a candidate protocol to test, not a frozen implementation choice:

1. Parent creates a dedicated `MessageChannel` for one attempt and retains port A.
2. Parent transfers port B to the worker in the initial bootstrap control message. The bootstrap captures it in a lexical closure before evaluating user code.
3. The bootstrap does not assign the port, its send function, attempt ID or other control capability to `globalThis`, the Pyodide Python globals, `registerJsModule`, stdout/stderr callbacks or any object passed to the guest.
4. Capture the required `MessagePort` send method before guest execution and keep both port and sender in closure state. Do not look up a mutable global function after guest code runs.
5. Parent listens for terminal messages only on port A. Default `Worker` `message` events are diagnostic/untrusted and cannot settle the attempt.
6. Parent binds every accepted control message to its own CommandId, DispatchAttemptId, worker instance, expected protocol version and strictly increasing sequence. Unknown, duplicate, stale, oversized, malformed or cross-attempt messages are rejected.
7. A trusted bootstrap sends a terminal observation only after its awaited `runPythonAsync` invocation returns or throws. The message describes a runner-level observation, not an OS child exit.
8. If the worker is terminated, closes itself, crashes, loses its private channel or fails before a valid terminal message is committed, the attempt remains INCOMPLETE / UNKNOWN. Do not infer exit code, termination acknowledgement or cleanup.
9. A private MessagePort is a protocol-isolation measure, not a process sandbox. Guest code may still access worker-global capabilities, interfere with runtime state, consume resources or stop the worker. Retain the existing default-deny and untrusted-execution restrictions.
10. Do not treat the private channel as cryptographic authentication. Its value is that the guest's ordinary `self.postMessage` does not directly address the parent listener that settles the attempt. Verify the actual reachability and tamper resistance in a controlled test harness.

An alternative is a separately isolated supervisor/guest realm, but it must prove that the guest cannot access the supervisor's result capability. Do not assume that placing two JavaScript functions in the same worker makes them isolated.

## 5. Adversarial acceptance tests

Proposed test IDs only. They do not alter LOOP/CASE/D identifiers.

| ID | Attack or interruption | Required result |
|---|---|---|
| PYO-CTRL-01 | Python sends `js.self.postMessage({id:known,result:...})` on default worker channel | Parent does not settle attempt from that message |
| PYO-CTRL-02 | Python sends forged `error`, `cancelled`, `timeout` and `completed` message shapes | All default-channel guest messages remain untrusted |
| PYO-CTRL-03 | Guest guesses predictable sequential request IDs | No guessed/default-channel message can settle a run |
| PYO-CTRL-04 | Guest attempts to enumerate `globalThis` for private control port or callback | No private result capability is exposed in global scope or Python globals |
| PYO-CTRL-05 | Guest overwrites `self.postMessage`, `MessagePort.prototype.postMessage`, timers or common globals | Captured private sender remains correct or execution is marked compromised/INCOMPLETE; no false PASS |
| PYO-CTRL-06 | Guest calls `js.self.close()` or parent invokes `Worker.terminate()` | No fabricated terminal result; preserve termination request/invocation and unresolved status |
| PYO-CTRL-07 | Guest emits default-channel fake result before wrapper completion | Private control channel alone may settle; fake result ignored |
| PYO-CTRL-08 | Wrapper sends duplicate, reordered, stale or wrong-attempt control messages | Parent rejects invalid sequence/binding; no cross-attempt mutation |
| PYO-CTRL-09 | Worker crashes after sending terminal message but before durable receipt commit | Recovery reconciles committed receipt state; no inferred durable completion and no automatic rerun |
| PYO-CTRL-10 | Guest mutates result data after wrapper capture or sends oversized/cyclic/uncloneable values | Parent validates bounded serialized result and independently verifies artifacts; no unsafe render or unbounded allocation claim |

### Minimum test fixture

Use synthetic code only. For each run, log:
- parent-generated attempt identity and expected sequence;
- default Worker message events (untrusted channel);
- private MessagePort events (candidate control channel);
- bootstrap phase and `runPythonAsync` resolve/reject observation;
- worker error/messageerror events;
- cancellation request, `terminate()` invocation and worker disappearance;
- IndexedDB transaction completion and receipt revision;
- whether any terminal result was accepted and why.

A test passes only if a forged default-channel message cannot cause a terminal verdict or publish an artifact. The test must separately assert that a real bootstrap terminal message can be accepted when the run finishes normally.

## 6. Red-team corrections to previous PocketCode research

1. **Previous EP-35 was underspecified.** It said to validate channel, schema, identity and sequence, but did not explicitly require a channel inaccessible to the Python guest. Schema and correlation checks are insufficient when guest code can post to the same channel.
2. **Previous worker contract treated the wrapper result channel too generically.** It now needs to distinguish guest-accessible Worker messages from the private supervisor control channel.
3. **Pyodide's official example was only an interoperability reference.** It must not be interpreted as a secure hostile-code protocol; the default numeric-ID message pattern is a teaching sample.
4. **The version evidence is now exact.** The 314.0.5 docs were opened directly, matching the version in the earlier owner device report. This still does not prove the deployed PocketCode app uses that runtime today.

## 7. Reuse and licensing

- Pyodide docs are the upstream project's official documentation, authored by Pyodide contributors and Mozilla; no sample code was copied.
- MDN reference content is published under its stated Creative Commons terms; no code was copied.
- HTML Living Standard is the normative platform reference; no code was copied.
- No dependency, runtime, worker library or third-party service is proposed or added.

## 8. Verification status

- **VERIFIED:** Pyodide 314.0.5 FFI maps `js` names to worker `globalThis`; the version-pinned Pyodide example uses default `self.postMessage` for wrapper result; DedicatedWorkerGlobalScope.postMessage sends to the parent.
- **INFERRED:** same-realm guest code can attempt to forge wrapper-shaped messages over that default channel; predictable/exposed IDs make correlation checks insufficient.
- **UNKNOWN:** PocketCode's actual worker architecture, guest globals, correlation-ID exposure, current message listener, any private port/supervisor channel, and whether this conditional attack path exists.
- **NOT RUN:** exploit demonstration, private-channel isolation prototype, iOS/Android browser tests, crash/termination tests, resource exhaustion tests.
- No PocketCode source/tests, canonical IDs, owner decisions, deployment, PRs, runtime choice or spending changed. P39/P40 remains CLOSED; OD-01..OD-13 remain OPEN.