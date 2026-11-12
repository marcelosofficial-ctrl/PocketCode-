# Phone and browser device validation runbook

Date: 2026-11-12  
Status: read-only owner/device protocol; no device result claimed.  
Scope: collect reproducible evidence for the existing Pyodios bridge issue and future PocketCode browser execution, origin and artifact-recovery acceptance. This document does not authorize implementation, deployment, provider selection or spending.

## 1. Rules before testing

- Record device model, OS version/build, browser/app name and exact version, install context (browser tab, Home Screen web app, WKWebView, Android PWA or Android WebView), network state and local timestamp for every observation.
- Keep each context separate. Safari tab evidence does not prove Home Screen app behaviour; neither proves WKWebView. Desktop browser results do not prove iOS or Android.
- Use only synthetic, non-sensitive inputs. Never enter credentials, private source, tokens or real user artifacts into the shared `github.io` origin.
- Do not clear site data, reinstall, update runtime, change settings, grant permissions, enable network, or rerun an artifact-producing attempt as part of diagnosis.
- Capture exact visible text and screenshots where practical. Redact source code, filenames, personal data and tokens before sharing logs.
- A missing console message, unavailable browser inspector or absent saved exception is UNKNOWN, not proof that the event did not occur.
- Record each test as PASS, FAIL, BLOCKED or NOT RUN, with the exact context and evidence. Never promote a manual observation into adapter, production or canonical CASE acceptance.

## 2. Immediate non-destructive Pyodios diagnostic

This is a third-party app observation, not PocketCode runtime acceptance.

1. Preserve the existing project and its already matching `summary.json`. Do not rerun `main.py`, the wrapper, or any artifact-producing task.
2. Record Pyodios version/build, iOS version/build, Pyodide version, Python version and whether the original project remains open.
3. The app Error Log has already been inspected and exposed only `Editor: PythonError`; do not clear it.
4. In the same existing session, open Console and run only the read-only saved-exception probe already specified in `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md` (prefer `sys.last_exc`, fallback to `sys.last_value`; print type, repr and formatted traceback). Do not import or execute `main.py`.
5. Record exact output, including “no previous exception” if returned. Do not infer the root cause from the bridge label.
6. If the probe is unavailable or empty, stop. Any later controlled reproduction requires a separate disposable project and an explicit fresh attempt; the successful project and artifact remain untouched.

Interpretation:
- A traceback identifies a candidate Python-level cause, not native process exit or PocketCode acceptance.
- No saved exception leaves the cause UNKNOWN.
- A matching existing JSON proves only the inspected artifact values, not the bridge, lifecycle, termination or full-run verdict.
- The wrapper's local CPython checks are not Pyodide/iPhone evidence.


## 2A. Owner-friendly instructions: what to tap and what to send

You do not need to understand Python or diagnose the error. This is just a read-only check that asks the already-open Python session whether it still remembers the error from the earlier run. It does **not** run your project, change `main.py`, or write/replace `summary.json`.

1. Open the **Pyodios** app on your iPhone.
2. Leave the existing project and its files alone. Do not tap the green play/run button.
3. At the bottom of the app, tap **Console** (not Editor).
4. Tap the Console input area so the keyboard appears.
5. Copy the entire small code block below, paste it into Console, and tap the Console's run/return control once. If the app does not show an obvious input area or run control, stop and tell us what you see. Do not guess or tap Editor's green play button.
6. Wait for the text output. Copy all output from the first line through the last line and send it here. If copying is difficult, a screenshot is fine, but check that it contains no private information first.
7. If it says **“No previous Python exception is available.”**, that is a valid result. Send that exact message. It does not mean you did anything wrong.
8. If Console is missing, unavailable, or shows an unexpected prompt/error before you can run the block, stop and tell us the exact screen text. Do not try another command.

Copy this exact block, without changing it:

```python
import sys
import traceback

exc = getattr(sys, "last_exc", None)
if exc is None:
    exc = getattr(sys, "last_value", None)

if exc is None:
    print("No previous Python exception is available.")
else:
    print("EXCEPTION TYPE:", type(exc).__name__)
    print("EXCEPTION VALUE:", repr(exc))
    print("TRACEBACK:")
    print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
```

**Privacy:** before sending, check the output for personal paths, private filenames, source code, tokens or other private data. Redact those parts. The exception type, short error message and traceback lines are the useful parts. Do not send the whole project or `summary.json` again; its successful values are already recorded.

**Stop conditions:** do not close/restart the project or Console, clear the Error Log, reinstall/update Pyodios, run `main.py`, run the diagnostic wrapper, or create a new project for this check. This is only the single read-only Console inspection. If it cannot be done as written, stop and report the obstacle.

## 3. Origin and application-context inventory

For each available context, record the exact URL (including scheme, host and port), app/browser version, whether installed, and whether the app opens standalone or in browser chrome:

| Context | Required observation | Status |
|---|---|---|
| iOS Safari tab at PocketCode Pages URL | What loads; exact URL; reload/cold-open behaviour | NOT RUN |
| iOS Home Screen web app, if already installed | Standalone launch; exact URL/origin; data/context visibly distinct from Safari | NOT RUN |
| iOS WKWebView | Test only when a real PocketCode native host exists; record host build and WebKit context | BLOCKED: no verified host build |
| Android Chrome tab | What loads; exact URL; browser version | NOT RUN |
| Android installed PWA | Standalone launch and origin/context | NOT RUN |
| Android WebView | Test only in an actual host build; record Android System WebView version | BLOCKED: no verified host build |

The known PocketCode and portfolio Pages paths share one scheme/host/port. Different paths are not separate origins. Do not store secrets or security authority on that origin. A Home Screen app's storage separation from Safari, where documented by WebKit, is not evidence of backup or guaranteed retention.

## 4. Future browser acceptance sequence

These tests require an explicitly approved test build and synthetic fixtures. They are NOT authorized or run by this runbook.

A. **Isolation and message boundary**
- Confirm the task document is a fixed supervisor in an iframe sandboxed with `allow-scripts` only and without `allow-same-origin`.
- Verify the parent accepts HELLO only from the exact current iframe `contentWindow`; `event.origin === "null"` alone is never identity.
- Verify the wildcard target is used only for the one-time credential-free bootstrap to that exact WindowProxy; all later control uses the transferred MessagePort.
- Bind the canonical `ExecutionId` separately from the parent-generated `execution_instance_id` in INIT and every subsequent channel message. Neither identifier may be chosen or rebound by task output.
- Attempt malformed, replayed, wrong-CommandId, wrong-DispatchAttemptId, wrong-ExecutionId, wrong-execution_instance_id, wrong-sequence, oversized and post-terminal messages. Each must fail closed without privileged action.
- Verify network requests are blocked by the actual deployed CSP and browser behaviour. A source declaration alone is not proof.
- Verify timeout/cancel invokes `terminate()` on the exact Worker held by the trusted supervisor. Accept the bounded `worker_termination_action_acknowledged` fact only from the current MessagePort and only when CommandId, DispatchAttemptId, ExecutionId, execution_instance_id and sequence all match.
- The supervisor acknowledgement proves only that its controller invoked Worker termination and closed that task channel. It is not a native child wait, proof the browser renderer/OS process stopped, or proof all external side effects ended. Without the matching acknowledgement, report termination UNKNOWN; frame removal is cleanup action, not termination proof.

B. **Artifact staging and recovery**
- Use a synthetic artifact with a known byte length and SHA-256. Verify the parent reads the bytes back from the actual store before committing a manifest.
- Inject interruption during write, after write/before manifest, and after manifest. Partial or orphan bytes must never be releasable.
- Test missing, truncated, changed, wrong-version and wrong-attempt objects. Expected result: quarantine/MISSING/INCOMPLETE, never empty success or silent rerun.
- Test quota failure, denied/unsupported persistence request, browser restart, force-close, offline reopen, storage clear and return after inactivity. Record exact engine/version and storage result.
- Test two tabs racing a receipt-head successor; one compare-and-swap wins and the other re-reads/reconciles.
- Export only a verified manifest-bound object through an explicit user action; record browser save/share outcome separately from client acknowledgement.

C. **Lifecycle and evidence**
- Keep child natural exit, wrapper exit, signal, embedded Python exception/SystemExit, termination request, worker termination action acknowledgement, broader termination/cleanup confirmation, artifact collection and client receipt as separate observations. Preserve canonical `ExecutionId` and frame `execution_instance_id` as distinct bindings.
- Wrong-attempt, missing, unauthenticated or contradictory evidence must remain UNKNOWN/INCOMPLETE.
- A UI toast, worker self-report, frame removal or wrapper code does not prove child exit or termination.
- CASE-04 remains INCOMPLETE / timed_out until authoritative same-attempt evidence and canonical acceptance are supplied.

## 5. Evidence record template

For every run, retain:
- Test ID and exact scenario; PASS/FAIL/BLOCKED/NOT RUN.
- Device model; OS/build; browser/app and version; install context.
- Application build/release and exact source SHA, if applicable.
- Start/end timestamps and network state.
- Exact steps and exact output; screenshot/log reference with secrets redacted.
- Expected result vs observed result; any ambiguity or missing evidence.
- Whether this is owner observation, model test, adapter test, device test or canonical CASE evidence.

## 6. Exit criteria and limits

- Immediate Pyodios diagnostic closes only when the exact probe output is recorded; an empty/unavailable probe remains UNKNOWN.
- Browser origin inventory closes only for the contexts actually observed. No cross-context generalization.
- Isolation, storage, recovery and lifecycle acceptance require an approved build, synthetic fixture, repeatable test steps and captured device/version evidence.
- No device tests, implementation, storage-engine selection, provider/host selection, deployment, DNS/settings change, or budget change are authorized here.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. Keep P39 implementation/adapter gate CLOSED and D-005/D-006 at $0.
