# Pyodide 314.0.7 — Mobile Runtime Feasibility Review

**Date:** 2026-11-01  
**Status:** Official-source desk review only. NOT DEVICE-TESTED, NOT IMPLEMENTED, NOT A SECURITY APPROVAL, NOT A RUNTIME SELECTION.  
**Scope:** Browser-local Pyodide candidate for the existing fixed synthetic `items.csv` → `summary.json` task on iPhone Safari / Home Screen web app.  
**Pinned candidate:** Pyodide 314.0.7.  
**Canonical task:** `AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`.  
**Related acceptance:** LOC-01..LOC-24 in `AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md`.

## 1. Executive finding

Pyodide 314.0.7 remains a technically credible **bounded local-execution experiment**, not a selected PocketCode runtime. The canonical task uses only standard-library CSV/JSON and decimal arithmetic, so it avoids the most obvious WebAssembly compatibility gaps and package-installation/network needs.

However, the current official documentation exposes three architectural constraints that should be treated as hard test gates rather than implementation details:

1. Pyodide requires a **module-type Web Worker** for its documented worker model. Classic workers using `importScripts()` are unsupported.
2. Pyodide's documented cooperative Python interrupt mechanism requires both a Web Worker and `SharedArrayBuffer`, which in turn requires the server's cross-origin-isolation security headers. If the deployed origin cannot expose `crossOriginIsolated === true` and `SharedArrayBuffer`, do not claim that the documented `KeyboardInterrupt` mechanism is available.
3. The pinned 314.0.7 release does **not** include the new `maxMemoryBytes` option shown in the changelog's Unreleased section. Do not design the first proof around that option or claim it is a hard device-memory quota.

The product direction does not change. Continue the same fixed task, keep execution location undecided, and use the experiment to falsify or support the local-browser hypothesis. A browser worker is not a security sandbox for arbitrary hostile code and does not establish process-tree cleanup, OS resource enforcement, credential isolation, or production suitability.

## 2. Version and compatibility facts

### 2.1 Pinned release

The official Pyodide changelog identifies version 314.0.7 as released on 2026-09-14. Its release-specific entry adds a `dedent` option to `runPython` / `runPythonAsync`; the 314.0.0 release line corresponds to Python 3.14.2 and Emscripten 5.0.3.

The changelog currently places `maxMemoryBytes` under **Unreleased**, after the 314.0.7 section. It describes a cap on growth of the WebAssembly heap for that instance, with allocation failure as `MemoryError`. This option must not be assumed available in the pinned 314.0.7 build. Even when released, a WASM heap-growth option would not itself prove a whole-browser-process, CPU, wall-time, storage or OS-level resource limit.

**Required record:** exact Pyodide asset version and hashes, Python version, Emscripten/runtime build, browser/iOS version and actual fetched asset bytes. Do not silently float to a later `latest` or `dev` build during comparison.

### 2.2 Standard library fit for the canonical task

The official 314.0.7 compatibility page says most of the standard library works. It documents:
- `decimal.Decimal` is supported through the C `_decimal` implementation; the Python `_pydecimal` implementation is unavailable.
- `threading`, `multiprocessing` and sockets can be imported but are not functional in the WebAssembly VM.
- Some modules are removed, including OS-specific/process/system modules.
- Browser networking uses browser APIs and is subject to browser CORS and network-policy behavior; it is not ordinary unrestricted Python socket access.

The fixed task can use `from decimal import Decimal`, `csv`, `json`, `pathlib` or ordinary file I/O. It does not need threads, subprocesses, sockets, package installation or network access. This is a good first compatibility target, but its correctness still needs a real run.

Do not infer that a package-heavy or general Python workload will work because this small standard-library task works.

## 3. Worker and interruption constraints

### 3.1 Module worker is required

Pyodide 314.0.7's official worker guide states that `pyodide.asm.mjs` is an ES module and Pyodide requires a module-type worker. Classic workers using `importScripts()` are not supported.

The guide recommends a worker so long-running synchronous Python does not block the browser UI. The worker runs in a separate global context and cannot directly manipulate the DOM. The worker/main-thread bridge must therefore be explicit and narrow.

**LOC implications:**
- LOC-04 must test a module worker, not a classic worker.
- Pin the worker script and all imported runtime assets.
- Define and validate a bounded message schema for run ID, command, input bytes, progress, output, terminal observation and error.
- Do not pass the entire application state, credentials, cookies, arbitrary object graphs or unrestricted JS capabilities into the worker.
- Preserve a request/attempt identity so late messages from a previous run cannot overwrite a newer run's UI.

### 3.2 Cooperative KeyboardInterrupt has a prerequisite

The official interrupt guide states that WebAssembly has no native preemptive multitasking. Pyodide's documented interrupt mechanism requires:
- Pyodide running in a Web Worker;
- a `SharedArrayBuffer` shared between the main thread and worker;
- `pyodide.setInterruptBuffer()` called in the Pyodide worker;
- a write of the documented interrupt signal to the buffer.

The guide explicitly says the server must set appropriate security headers to enable SharedArrayBuffer. Therefore, LOC-05 is a gate for LOC-06, not merely an informational check.

**Decision rule for the experiment:**
- If `crossOriginIsolated` is false or `SharedArrayBuffer` is unavailable, mark the documented cooperative-interrupt capability UNSUPPORTED in that deployment and mark LOC-06 BLOCKED/NOT RUN for that mechanism.
- Do not simulate a KeyboardInterrupt by terminating the worker and call it cooperative interruption.
- If available, test a pure Python infinite loop and a Python program that catches `KeyboardInterrupt`; capture request-to-interrupt latency, resulting exception/terminal observation, whether user code caught it, whether the worker remains responsive, and whether the runtime can be used again.
- A custom Python signal handler may catch/alter SIGINT behavior. The host must not treat a UI button press as confirmed termination.
- If no trustworthy terminal response arrives, preserve UNKNOWN/INCOMPLETE.

Cross-origin isolation headers can affect resource loading and embedding. Test the actual deployed response headers and every runtime asset under the intended CSP/CORS/COEP configuration. Do not assume that a CDN asset which loads in an ordinary page will also load under the final isolation policy.

### 3.3 Hard worker termination is not graceful cleanup

`Worker.terminate()` is a host-level stop action. It does not prove Python `finally` blocks ran, files were flushed, buffers were drained, temporary state was cleaned, or complete stdout/stderr was captured.

After hard termination:
- record that the host terminated the worker;
- mark child/script cleanup UNKNOWN;
- mark terminal execution evidence unavailable unless a trusted terminal record was already durably captured;
- retain only the last safely received bounded output;
- do not infer exit code or PASS/FAIL from the disappearance of the worker;
- do not silently rerun after reload or recovery.

## 4. Browser file access and persistence

The official Pyodide FAQ says browser JavaScript cannot read arbitrary local `file://` paths. The File System Access API is supported in Chrome but not Safari/Firefox. The Pyodide filesystem guide describes `mountNativeFS()` as experimental and limited to Chromium-based browsers.

For iPhone Safari, the first proof should therefore use:
1. user-selected file input via the normal browser file picker;
2. explicit transfer of selected bytes into the worker's virtual filesystem;
3. real creation of `summary.json` in Pyodide's virtual filesystem;
4. explicit export through a generated Blob and user-initiated browser save/share path.

The default Pyodide filesystem is MEMFS, an in-memory virtual filesystem. Its contents are lost when the page reloads. IDBFS and other filesystems exist, but persistence adds storage lifecycle, privacy, deletion, quota and recovery questions. Do not add persistence to the first task unless the fixed worksheet shows it is required.

**Acceptance requirement:** inspect the actual exported `summary.json` bytes/content and prove that the file can be saved/shared in Safari and Home Screen web-app mode. Displaying JSON in the UI or copying text is not equivalent to creating/exporting a real file.

## 5. Network and credential boundary

Pyodide's browser network operations use browser APIs. The official compatibility/HTTP documentation describes CORS limitations and lack of raw socket access; it does not provide an application-level guarantee that arbitrary code cannot use browser networking capabilities exposed to it.

For this fixed task, no network is required after the runtime assets have loaded. The future implementation should test:
- a dedicated execution origin that carries no application authentication cookies or privileged same-origin credentials;
- restrictive CSP and worker policy on the actual deployment;
- no application API credentials, tokens, secrets, private user state or ambient privileged JS objects passed to the worker;
- same-origin and cross-origin fetch attempts from the Python/JS execution context;
- whether user code can reach app APIs or same-origin endpoints despite the intended policy;
- exact runtime/package asset loading under COOP/COEP/CORS requirements.

A separate origin and CSP are proposed risk-reduction measures, not proof by themselves. Test the browser's actual request behavior and credential attachment. Do not describe Pyodide/WASM as a complete sandbox or claim a hostile-code security boundary from this local feasibility task.

## 6. Resource and lifecycle acceptance

The pinned Pyodide changelog does not expose `maxMemoryBytes` in 314.0.7. The first test must therefore measure observed memory/reload behavior without pretending to have a hard memory cap.

Record:
- cold runtime load time and actual bytes fetched;
- warm startup/run time;
- peak and post-run browser process/memory indicators if the platform exposes them;
- WASM heap size/observations where available;
- repeated runs in one instance;
- a controlled fresh-instance comparison;
- large output and large allocation behavior;
- browser tab backgrounding, screen lock, incoming interruption, memory pressure, reload, tab eviction and Home Screen relaunch;
- whether a terminal message was durably captured before interruption.

Do not infer iOS Safari's memory limit from old WebKit issue comments or from installed device RAM. Record actual device/iOS/browser and treat browser process eviction as a normal UNKNOWN/INCOMPLETE recovery case.

The first fixed task is deliberately small. Its successful completion would prove only that this exact standard-library transformation works in the tested browser/device/build. It would not establish general Python compatibility, hard resource enforcement, security isolation, background execution, persistence or provider equivalence.

## 7. Updated LOC test interpretation

| Existing ID | Refined interpretation |
|---|---|
| LOC-01 | Pin 314.0.7 exactly; record module-worker boot, Python/runtime version, assets and cold/warm load. |
| LOC-02 | Run the canonical worksheet success and malformed-header cases unchanged. Verify actual file bytes and no misleading output on failure. |
| LOC-03 | Verify unsupported modules/capabilities against 314.0.7; do not generalize from one small task. |
| LOC-04 | Use a module-type worker. Classic worker failure is expected by design, not a Pyodide regression. |
| LOC-05 | Record actual response headers, `crossOriginIsolated`, `SharedArrayBuffer`, COEP/CORS asset behavior. This gates LOC-06. |
| LOC-06 | Run only if LOC-05 passes; use the documented interrupt buffer and record caught/uncaught KeyboardInterrupt behavior. |
| LOC-07 | Separately test `Worker.terminate()`; record host termination only, cleanup/exit status UNKNOWN. |
| LOC-08/09 | Test browser fetch, CSP/CORS and credential isolation; no network is required for the canonical task. |
| LOC-10 | Validate a strict worker message protocol and reject stale/unknown message IDs. |
| LOC-11 | Confirm MEMFS loss on reload; persistent storage is a separate later decision. |
| LOC-12/17/18 | Use explicit file picker input and real Blob save/share in Safari and Home Screen mode; do not rely on File System Access API. |
| LOC-13/19/20/24 | Measure cold/warm/repeated-run/instance memory behavior; do not claim a 314.0.7 hard memory cap. |
| LOC-14/21/22 | Background, reload or worker disappearance yields UNKNOWN/INCOMPLETE unless trusted terminal evidence already exists; no automatic replay. |
| LOC-15 | Treat stdout/stderr and filenames as untrusted program data in the copied AI report. |
| LOC-16 | Compare the same fixed task against ordinary AI chat and an available no-cost phone workflow; keep NOT RUN visible until observed. |
| LOC-23 | Verify the actual deployed cross-origin isolation and every required asset, not just a local development server. |

LOC-01..LOC-24 remain proposed device acceptance cases. No case is marked PASS by this document.

## 8. Decision and next step

**Recommendation:** retain Pyodide 314.0.7 as the pinned browser-local candidate for the bounded experiment, subject to actual Safari/Home Screen feasibility. Do not choose it as the production runtime yet.

The next research-only action is to convert the above constraints into a one-page preflight checklist attached to the existing worksheet, so a future hands-on attempt records the prerequisites before running either success or failure fixture. No new task, second scorecard or alternative architecture is needed.

If hands-on testing later becomes possible, use the exact canonical worksheet and LOC-01..24. Do not install an app, create an account, use a provider, enable billing or start a hosted workload as part of this research pass.

## 9. Primary sources reviewed

- Pyodide 314.0.7 changelog, including the 314.0.7 section and current Unreleased section: https://pyodide.org/en/stable/project/changelog.html
- Pyodide 314.0.7 web worker guide: https://pyodide.org/en/stable/usage/webworker.html
- Pyodide 314.0.7 interrupt guide: https://pyodide.org/en/stable/usage/keyboard-interrupts.html
- Pyodide 314.0.7 Python compatibility: https://pyodide.org/en/stable/usage/wasm-constraints.html
- Pyodide 314.0.7 filesystem guide: https://pyodide.org/en/stable/usage/file-system.html
- Pyodide 314.0.7 FAQ: https://pyodide.org/en/stable/usage/faq.html
- Pyodide 314.0.7 deployment guide: https://pyodide.org/en/stable/usage/downloading-and-deploying.html
- Pyodide 314.0.7 HTTP API: https://pyodide.org/en/stable/usage/api/python-api/http.html

## 10. Evidence status and non-actions

This is official-source desk research only. No Pyodide code was deployed, no worker was built, no device was tested, no file was executed, no app was installed, no account/provider/workload was created, no Actions workflow was run, and no source/test file or PR was changed. The fixed task remains NOT RUN. Runtime security, resource limits, cleanup, persistence, file export, Safari compatibility and product value remain unproven.
