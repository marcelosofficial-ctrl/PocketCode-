# Pyodide 314.0.7 Capability and Attenuation Audit

**Date:** 2026-11-03  
**Status:** Pinned-source desk audit. No browser execution, exploit test, mobile-device test, build, or product-path run performed.  
**Authority:** Research decision aid only. Does not amend canonical LOOP-01..14 / CASE-01..16, select a runtime, or authorize implementation/provider use.

## Executive decision

**Do not use stock Pyodide as PocketCode's security boundary for arbitrary hostile or untrusted Python. Do not spend the next implementation cycle trying to turn stock Pyodide into one by deleting imports.**

Keep browser-local Pyodide as a possible **user-approved convenience runner for code the user already trusts**, with explicit limitations, isolated origin, disposable worker, strict CSP, no app credentials, no network, bounded inputs/outputs, and no claim of hard resource quotas or hostile-code containment. This is a conditional product experiment, not an approved runtime selection.

The previous attenuation hypothesis is technically plausible as a capability-reduction experiment, but the pinned source shows more retained references and bootstrap coupling than a simple `unregisterJsModule()` call. It would require an explicit object-capability inventory, adversarial browser tests, a maintained version-pinned bootstrap shim, and re-audit on every Pyodide update. That cost is not justified for the first product proof, and a successful attenuation test would still not establish a hard memory/disk quota or general-purpose hostile-code sandbox.

For arbitrary untrusted code, keep a separately supervised OS/VM boundary as the required research direction. Happy Agent's Linux strict service remains a reference only, not a selected/ready implementation. A user-owned remote PC is not automatically safe: it needs its own disposable execution boundary and credential separation.

## 1. Exact source findings

All source references below are the **Pyodide tag 314.0.7**, not a moving main/stable branch. Blob SHAs are included so a future reviewer can confirm the exact material reviewed.

| Source | Blob SHA | Verified finding |
|---|---|---|
| `src/js/pyodide.ts` | `297380c5afcdcb46a1895ccd8f2c40f70f3adccb` | `jsglobals` defaults to `globalThis`; it is the object registered as the Python `js` module. |
| `src/js/api.ts` | `a7029cb25bb1dcfcb893237fe91b2eff7b6a2ff8` | Bootstrap separately registers both `js` and `pyodide_js`; public API exposes `FS`, `PATH`, `_module`, and `_api`; `registerJsModule` and `unregisterJsModule` delegate to Python FFI. |
| `src/py/_pyodide/_importhook.py` | `4829efccb39a17561af2839c9e5e4a1230780e8a` | Unregister deletes the name from the import finder's `jsproxies` mapping, but explicitly does not remove an already-imported module from `sys.modules`. |
| `src/py/pyodide/ffi/__init__.py` | `772e6f59127ab34b9b55809760a4bc917720ffb5` | Python-visible `register_js_module` and `unregister_js_module` remain exported from `pyodide.ffi`. |
| `src/py/pyodide/__init__.py` | `b9832a3386f949978e86ae03e292365b25557b26` | Documents that `js` and `pyodide_js` are available when `pyodide` is imported. |
| `src/py/pyodide/_package_loader.py` | `c4cd7b2efae824f7ea5c365cd512330a02f1712f` | Imports `loadedPackages` from `pyodide_js` into a module-global reference; that reference is not erased merely by unregistering the module. |
| `src/js/load-package.ts` | `ebb37a0d4faccb153086272663743db07ab15efe` | `loadedPackages` is a JS object held by the package manager and exposed through the public API. |
| `src/py/pyodide/code.py` | `2918b1a0392e29aa30726715d64ed30e972b1749` | `pyodide.code.run_js()` imports `js.eval` and invokes it. Removing the `js` import capability should make this helper fail, but does not itself prove there are no other JS references. |
| `src/py/pyodide/webloop.py` | `0e1274967008bbb907683f1fda299e48ea018169` | Imports `pyodide_js._api.scheduleCallback` at module import and later reads `pyodide_js._api.config`; importing it before attenuation leaves cached references. |
| `src/py/pyodide/http/_pyfetch.py` | `1039cad919e692b015c14b254c3aec5a9eb39834` | On Pyodide, imports JS fetch/Abort APIs and `pyodide_js._api.abortSignalAny`; importing it before attenuation leaves JS-backed references. |
| `src/tests/test_pyodide.py` | `3cc0103c67c3d09d08312ba16853f0741cd98c95` | The pinned test marks the CSP test expected-fail on Safari because Safari does not support `wasm-unsafe-eval` in this test environment. |
| `src/templates/test_csp.html` | `172fe79af5feb8c2db55ea73af3c9247b0a5e6d5` | The upstream CSP fixture is a compatibility test policy, not a PocketCode no-egress policy: it uses `default-src http: 'wasm-unsafe-eval'`. |

### 1.1 What the source proves about attenuation

1. `jsglobals: Object.create(null)` or another empty object only changes the global object exposed through the Python `js` module. It does **not** suppress the separately registered `pyodide_js` module.
2. `pyodide_js` is not a harmless empty namespace. Its public object has direct properties `FS`, `PATH`, `_module`, and `_api`. The API's `FS` is the Emscripten filesystem interface; `_module` is the Emscripten module; `_api` is the internal API object.
3. `unregister_js_module("pyodide_js")` removes the import-hook registration only. A trusted bootstrap would also have to remove the imported `pyodide_js` module from `sys.modules` before user code starts.
4. That still does not remove already-copied JS references. During final bootstrap, Pyodide imports `pyodide._package_loader`; that module captures `loadedPackages` as a module-global JS proxy. If `pyodide.webloop` or `pyodide.http._pyfetch` has been imported, those modules also cache JS-backed functions/objects.
5. `pyodide.ffi` keeps module registration helpers visible. Re-registration requires a `JsProxy`, so the key security question is whether **any** JS proxy or equivalent host capability remains reachable to untrusted Python after the scrub. The source review has identified at least one cached JS object reference, but has not demonstrated that this object alone can recover `globalThis` or the full API. Treat it as a residual capability requiring adversarial testing, not as a proven exploit.
6. `pyodide.code.run_js()` is a direct eval wrapper through the `js` module. Removing `js` from both the import hook and `sys.modules` should break this specific path unless another JS proxy can reintroduce it. Do not allow a CSP fallback to `unsafe-eval` to restore this capability.
7. Upstream's CSP fixture is not suitable as PocketCode's policy. Its `default-src http:` does not express the intended deny-by-default execution origin and does not establish a no-egress guarantee. A PocketCode worker would need a separately designed policy such as deny-by-default sources, explicit runtime asset sources, and `connect-src 'none'`, validated against actual browser behavior.
8. The upstream test itself is marked expected-fail for Safari on the `wasm-unsafe-eval` feature. Do not silently add `unsafe-eval` to make Safari work. If the required WebAssembly CSP is unsupported on a target Safari version, mark that browser/runtime combination unsupported until a safe supported solution is demonstrated.

### 1.2 Why an import scrub is not a security boundary

A scrub could be useful as defense in depth, but the trusted bootstrap would need to run after all required Pyodide initialization and before any user bytecode. It would need to enumerate every JS proxy reachable from:
- `sys.modules`, module globals, package-loader state, event-loop state, and imported helpers;
- Pyodide's public and internal API objects;
- cached package-loader and stream callbacks;
- any host-supplied Python globals, callbacks, file handles, or message-port wrappers;
- Python FFI conversion/proxy APIs and any object created by `to_js()`.

It must also prove that untrusted Python cannot reconstruct a usable JS capability, register a privileged module again, or use a JS object prototype/constructor path under the actual CSP. The present audit has not run that adversarial test. A source-only list of known references is not a complete object-capability proof.

Even if all these paths were successfully attenuated, that would only reduce exposed browser capabilities. It would not provide:
- an OS process boundary separate from the browser;
- a hard, product-configurable memory ceiling or disk quota per run;
- a trusted wall-clock deadline that is guaranteed to fire while iOS suspends the page;
- a guarantee that browser-managed origin storage is erased or quota-bounded per attempt;
- a formal security guarantee against Pyodide/runtime/WASM/browser implementation vulnerabilities.

## 2. Browser worker and mobile lifecycle

A dedicated worker is useful for keeping computation off the UI thread and gives the trusted parent a direct `Worker.terminate()` control. That is meaningful process-stop evidence **when the parent is alive and can issue the call**. It is not equivalent to a provider/OS supervisor with durable deadline enforcement.

WebKit documents that on iOS inactive tabs can be completely suspended and timers throttled. Therefore a browser timer is not a reliable wall-clock deadline when the app is backgrounded, and a PWA cannot claim it will keep a run alive or terminate it at a precise time while backgrounded. On foreground return, the app must reconcile what it actually knows; if the worker or page disappeared, the result is UNKNOWN/INCOMPLETE, not a fabricated timeout or exit code.

Worker termination also does not provide per-run memory/disk quotas or trusted cleanup evidence for persistent browser storage. Use a fresh disposable worker per run, do not mount OPFS/IDBFS for untrusted input, and treat any persistent browser storage as a separate product feature requiring explicit retention/deletion semantics.

## 3. Execution-path decision against PocketCode's first proof

The frozen first task is a bounded standard-library CSV-to-JSON script using `main.py` and `items.csv`, producing `summary.json`. Its simplicity is intentional: the product proof is the phone workflow and trustworthy result, not package breadth.

| Path | Fit for frozen task | Security and lifecycle reality | Current decision |
|---|---|---|---|
| Browser-local Pyodide in a disposable worker | Technically plausible for standard-library CSV/JSON; no hosted spend | Browser-origin capability model; Pyodide exposes Web APIs by default; no demonstrated hard memory/disk quota; iOS background suspension weakens deadline claims; file access/export is browser-mediated | Keep only as a user-approved convenience experiment. Not a hostile-code sandbox and not selected. |
| Isolated Linux/VM execution | Strong fit; normal CPython semantics and file I/O | Can enforce namespaces, cgroups, seccomp, network isolation, hard deadline, bounded filesystem and supervisor/workload separation if implemented and proven correctly | Required research path for arbitrary untrusted code. Happy Agent strict service is a reference, not a ready adapter; provider/host and cost remain unresolved. |
| User-owned remote PC | Strong fit if PC is available and user wants desktop resources | No hosted-provider bill, but remote reachability, auth, PC uptime and a disposable local isolation boundary are required. Ordinary user account execution is not safe for hostile code; host secrets must not enter the workload | Future RevDev/PocketCode bridge candidate, not available during current phone-only period and not a default sandbox. |
| Manual copy/paste to another AI or existing tool | No execution by PocketCode; can support correction and report comprehension | No PocketCode execution evidence; user runs elsewhere under that tool's actual boundary | Keep as transparent fallback and as a control condition in the report-value experiment. Never label it a PocketCode run. |

**Decision:** do not select an execution backend yet. The first product comparison should prioritize actual iOS local Python (Pyodios) versus browser Pyodide versus manual workflow on the same task, while separately assessing Android local alternatives. This is product-path validation, not permission to install apps or run workloads. The execution-location decision remains OPEN.

## 4. Lifecycle and evidence implications

The following table applies to any path. It reinforces existing contract semantics; it does not add acceptance IDs.

| Stage | Browser worker can establish (if implemented and observed) | What remains unknown or needs another authority |
|---|---|---|
| User intent | Explicit run request, chosen files, source/fixture digest | Whether UI selection actually bound the exact bytes unless captured |
| Policy | Local UI can display selected restrictions | No trusted policy-at-dispatch boundary against hostile code |
| Authorization | User gesture and app permission state | No server/provider authorization unless that path exists |
| Dispatch | Worker creation and message acceptance | Worker creation is not proof that Python started |
| Execution | Worker-originated events, output, task result | Untrusted code can forge its own printed claims; only host-captured events are runner evidence |
| Deadline | Parent can request termination while alive | iOS suspension can delay timers; browser time is not a durable supervisor |
| Result | Worker response and captured files/streams if complete | Lost worker/page or missing terminal message means UNKNOWN, not FAIL/PASS |
| Cleanup | Parent called terminate; worker no longer accepts messages | No per-run filesystem wipe proof if persistence was mounted; no host/process resource reconciliation |
| Artifact release | Parent validates filenames/bytes and creates user download | Browser storage lifecycle and durable retention remain separate; never release partial/unverified output as complete |
| Report | Host can serialize observed fields and explicit unknowns | A report cannot upgrade browser-local observations into trusted OS/provider evidence |

Keep these independent fields in the report: execution outcome, lifecycle/disposition, exit code, duration, runtime/version, stdout/stderr and truncation, artifact inventory/integrity, cleanup/termination evidence, and artifact-release state. Unknown remains unknown. A worker's own stdout or JSON claim is not authoritative lifecycle evidence.

## 5. Acceptance mapping and required future falsification

No canonical IDs are added or redefined.

- **LOOP-01 / LOOP-10:** prove phone file selection, exact input bytes, generated file retrieval, and no path/filename confusion on supported iOS/Android devices.
- **LOOP-02 / LOOP-03 / LOOP-04 / CASE-01..03:** capture real worker start/terminal events, exact stdout/stderr, exit evidence and output bytes. Synthetic receipts do not count.
- **LOOP-05 / CASE-04..06:** test CPU-bound infinite loop, blocked event loop, worker crash, page background/suspension, parent reload, and explicit user cancel. Distinguish worker termination confirmed from deadline expired and from unknown page loss.
- **LOOP-07 / CASE-07:** enforce stream/output caps in the trusted parent; test huge stdout, many files, oversized files, malformed encodings and output-expansion pressure.
- **LOOP-11 / LOOP-12:** adversarially attempt access to `js`, `pyodide_js`, `_api`, `_module`, `FS`, fetch, IndexedDB, Cache API, storage, service workers, message ports, and re-registration through FFI. Verify CSP network denial from the worker, not merely absence of network calls in the fixture. This is mandatory before describing any attenuation as effective.
- **LOOP-13 / LOOP-14:** prove manual handoff is explicit and no service/account/cost claim is implied.
- **CASE-11 / CASE-12:** disconnect, background, reload and recovery must preserve UNKNOWN/INCOMPLETE where terminal evidence was lost.

A successful fixed-task run is not a sandbox test. A successful capability scrub test is not a resource-limit test. A worker termination test is not proof that a durable timeout fired while iOS suspended the page.

## 6. Next work order

1. **Do not implement the attenuation shim now.** Record it as a rejected MVP security strategy, not a permanent statement that capability reduction is impossible.
2. Continue the product-value experiment design using the same frozen source/input/result facts across Pyodios, browser Pyodide and manual workflow. No installs or runs until owner-authorized target-device access exists.
3. If a browser-local experiment is later authorized, limit it to user-approved code and a disposable worker on a dedicated origin. Before any hostile-code claim, require an independent security review and the adversarial capability matrix above.
4. Continue Linux/VM boundary research only where it closes concrete gaps: immutable input snapshot, no host secrets, network namespace/egress denial, memory/swap/process/CPU/disk limits, absolute deadline, supervisor separation, process-tree reconciliation, and artifact publication integrity.
5. When PC access returns, first perform read-only inventory of the PC/runtime and existing RevDev state. Do not assume historical paths, binaries or queue state.

## 7. Sources

Pinned source:
- [Pyodide 314.0.7 api.ts](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/api.ts)
- [Pyodide 314.0.7 pyodide.ts](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/pyodide.ts)
- [Pyodide 314.0.7 import hook](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/_pyodide/_importhook.py)
- [Pyodide 314.0.7 package loader](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/_package_loader.py)
- [Pyodide 314.0.7 package manager](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/load-package.ts)
- [Pyodide 314.0.7 CSP test](https://github.com/pyodide/pyodide/blob/314.0.7/src/tests/test_pyodide.py)
- [Pyodide 314.0.7 CSP fixture](https://github.com/pyodide/pyodide/blob/314.0.7/src/templates/test_csp.html)

Official browser/runtime documentation:
- [Pyodide 314.0.7 overview](https://pyodide.org/en/314.0.7/)
- [Pyodide 314.0.7 Python FFI API](https://pyodide.org/en/314.0.7/usage/api/python-api/ffi.html)
- [Pyodide 314.0.7 JavaScript API](https://pyodide.org/en/314.0.7/usage/api/js-api.html)
- [MDN Worker.terminate()](https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate)
- [WebKit: background-page power management](https://webkit.org/blog/8970/how-web-content-can-affect-power-usage/)

**Final status:** Pyodide stock runtime is NOT APPROVED as a hostile-code sandbox. Trusted-bootstrap attenuation is NOT PROVEN and is not an MVP priority. Browser-local execution remains a possible convenience path, not selected. Fixed-task product comparison and all browser/device/adversarial tests remain NOT RUN.
