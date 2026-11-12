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
- Attempt malformed, replayed, wrong-attempt, wrong-sequence, oversized and post-terminal messages. Each must fail closed without privileged action.
- Verify network requests are blocked by the actual deployed CSP and browser behaviour. A source declaration alone is not proof.
- Verify timeout/cancel destroys the frame and worker, but do not claim termination until an authoritative same-attempt controller acknowledgement exists.

B. **Artifact staging and recovery**
- Use a synthetic artifact with a known byte length and SHA-256. Verify the parent reads the bytes back from the actual store before committing a manifest.
- Inject interruption during write, after write/before manifest, and after manifest. Partial or orphan bytes must never be releasable.
- Test missing, truncated, changed, wrong-version and wrong-attempt objects. Expected result: quarantine/MISSING/INCOMPLETE, never empty success or silent rerun.
- Test quota failure, denied/unsupported persistence request, browser restart, force-close, offline reopen, storage clear and return after inactivity. Record exact engine/version and storage result.
- Test two tabs racing a receipt-head successor; one compare-and-swap wins and the other re-reads/reconciles.
- Export only a verified manifest-bound object through an explicit user action; record browser save/share outcome separately from client acknowledgement.

C. **Lifecycle and evidence**
- Keep child natural exit, wrapper exit, signal, embedded Python exception/SystemExit, termination request, termination acknowledgement, cleanup, artifact collection and client receipt as separate observations.
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
