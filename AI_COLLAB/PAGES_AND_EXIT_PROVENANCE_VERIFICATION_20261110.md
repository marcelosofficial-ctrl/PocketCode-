# Pages deployment evidence and runtime exit-provenance crosswalk

**Date:** 2026-11-10  
**Status:** Verified repository facts + platform research; no implementation or owner decision.  
**Authority:** D-006 and canonical LOOP-01..14 / CASE-01..16 remain unchanged. This note does not select a runtime, database, host, provider or transport.

## 1. Ranked work addressed

1. **Actual Pages deployment evidence:** determine what the repository proves and what the public deployment settings still do not prove.
2. **PWA execution evidence:** distinguish a browser worker's runner-level completion from an operating-system child-process exit.
3. **Output finalization:** separate process exit from completion of output-stream collection and artifact publication.
4. **Owner-gate hygiene:** keep PocketCode's O-5 exit-provenance task distinct from the unrelated RevDev O-5 decision described in a separate project.

## 2. Pages deployment: verified facts and remaining unknowns

### 2.1 Repository evidence

- **VERIFIED:** GitHub repository metadata for `marcelosofficial-ctrl/PocketCode-` reports `has_pages: true`, `homepage: null`, and `default_branch: main`. The metadata response does not contain a Pages URL.
- **VERIFIED:** the workflow `.github/workflows/preview-prototype.yml` at blob `58b1bb968aa8e6a2ae824079046e5968a140ab16` runs automatically on pushes to `main` when `prototypes/mobile-runner/index.html` or the workflow itself changes. It also permits manual `workflow_dispatch`.
- **VERIFIED:** that workflow uses `actions/configure-pages@v5`, uploads `prototypes/mobile-runner` as the Pages site root, and deploys with `actions/deploy-pages@v4`. Its GitHub Actions environment is named `github-pages`, and the environment URL is populated from the deploy step's `page_url` output.
- **VERIFIED:** the inspected `main` tree at commit `03e65ef35d8b22cb4337ac7097b2a31247c3721e` contains `prototypes/mobile-runner/index.html` and the workflow, but no file named `CNAME`.
- **VERIFIED:** the active research branch is `pocketcode-ai-workflow-director-research-2026-10-28`, HEAD `fa4abae9b62f8eb8ed9ae19ba36d7e870d0def39`. The automatic push trigger is main-only; a manual dispatch may select a branch, but no run proving such a dispatch was inspected.

### 2.2 What cannot be concluded

- **UNKNOWN:** the exact GitHub Pages URL and effective hostname.
- **UNKNOWN:** whether a custom domain is configured in repository Pages settings, whether an inherited user/organization custom domain applies, and whether DNS/TLS redirects are correct.
- **UNKNOWN:** the actual deployment commit, latest deployment environment URL, deployed response headers, deployed HTML/meta CSP and service-worker scope.
- **UNKNOWN:** whether any other independently maintained site is served from the eventual same-origin hostname.

No `CNAME` file in the inspected main tree is useful evidence, but it is not a substitute for reading the Pages settings and deployment environment. `homepage: null` is also not proof that Pages is disabled or that no custom domain exists. The repository's `has_pages: true` flag proves Pages is enabled at the repository level, not which URL it serves.

The conventional project-site URL pattern is `https://<owner>.github.io/<repository>`, but that is only a candidate until the Pages settings or the workflow's deployed `page_url` output confirms it. The candidate URL was not confirmed by the available live-page check. Do not write it into product copy or treat it as a verified origin.

### 2.3 Required evidence collection

| ID | Exact evidence to collect | Closure rule |
|---|---|---|
| PAGES-01 | Repository Settings → Pages: publishing source, custom domain, enforcement and site URL | Save exact URL and source branch/folder or workflow source |
| PAGES-02 | GitHub Actions run for `preview-prototype.yml`: commit SHA, conclusion, environment URL | Tie deployment URL to exact deployed SHA |
| PAGES-03 | Main/user-site custom-domain configuration and same-host project inventory | Classify same-origin sites as trusted or independently maintained |
| PAGES-04 | Live HTTPS response, redirect chain, headers and HTML meta policy | Record observed values, not intended settings |
| PAGES-05 | Actual deployed service-worker registration and scope | Confirm scope and distinguish it from storage-origin isolation |
| PAGES-06 | Synthetic same-origin sibling test for IndexedDB and OPFS | Demonstrate or refute cross-path storage access in the target browser |
| PAGES-07 | Repeat origin test on supported iOS and Android browser engines | Keep engine/device evidence separate |
| PAGES-08 | Owner decision on accepting shared-host same-origin trust or choosing a distinct origin | No host/domain spend or migration without explicit approval |

**No deployment settings were changed.** No new workflow run was triggered. The owner can provide the published URL, but settings/run evidence is still preferable because a URL alone does not prove which commit or headers are deployed.

## 3. Runtime exit provenance: a PWA worker is not a child process

### 3.1 Browser worker facts

- **VERIFIED:** the HTML Living Standard opened 2026-11-10 was last updated 2026-11-09. Its worker termination algorithm sets the worker closing flag, discards queued tasks, aborts the currently running script, and empties the dedicated worker's message queue.
- **VERIFIED:** MDN documents that `Worker.terminate()` immediately stops the worker without giving it an opportunity to finish, and its return value is `undefined`. The API has no termination-acknowledgement event or returned process exit code.
- **VERIFIED:** a worker's `error` event is an error observation, not a normal child-process exit record. A missing terminal message after worker failure/termination is not evidence of success or a specific nonzero exit.
- **INFERRED:** in a Pyodide-in-a-worker PWA, a trusted bootstrap may observe that its Python invocation returned or raised and send a runner-level terminal observation. That is not an OS child exit. Its trust depends on the wrapper/guest boundary and message channel, which have not been implemented or tested here.

**PocketCode consequence:** do not populate a generic `child_exit_code` from a browser worker's normal return, `error` event, timeout, page close or `terminate()` call. Keep a separate `runner_terminal_observation` (or equivalent future typed fact), including source, attempt identity, sequence, and whether it was a normal wrapper observation, exception, error event, termination request or unknown disappearance. The label is conceptual, not a frozen schema.

### 3.2 Python subprocess facts and mobile applicability

- **VERIFIED:** current Python 3.15.2 `subprocess` documentation explicitly lists Android, iOS and WASI as unsupported platforms. It says the module is not supported on mobile platforms or WebAssembly platforms.
- **VERIFIED:** in a supported native environment, `Popen.returncode` starts as `None`; a negative value `-N` indicates termination by signal `N` on POSIX. When `shell=True`, the reported PID and return code describe the shell process; shells may map signal termination to values such as `128+N`.
- **VERIFIED:** Python `subprocess.run(..., timeout=...)` kills and waits for the child when the timeout expires, then raises `TimeoutExpired`; initial process creation itself may not be interruptible.
- **INFERRED:** a phone-first Pyodide deployment cannot rely on Python's standard `subprocess` API to create a native child process or obtain its exit status. A different explicitly selected runtime/host boundary would need its own evidence contract.

### 3.3 Native-process reference pattern, not a product stack choice

Node.js v26.13.0 documentation provides a useful example of keeping facts separate:
- `exit` means the process ended; stdio streams may still be open.
- `close` occurs after the process ended and its stdio streams have closed.
- the event carries either a natural exit code or a signal field; signal termination is not a natural child return code.

This is a reusable semantic pattern, not a proposal to add Node.js to PocketCode. It demonstrates why process completion and output collection completion must be separate observations.

## 4. Proposed acceptance additions

These IDs extend the EP research proposal only. They do not alter canonical CASE IDs.

| ID | Setup / fault | Required assertion |
|---|---|---|
| EP-26 | PWA worker completes a Python invocation normally | Record runner-level terminal observation; never label it OS child exit |
| EP-27 | PWA worker raises an uncaught error before terminal message | INCOMPLETE / worker-error evidence; no fabricated exit code |
| EP-28 | User cancels and host calls `Worker.terminate()` | Record cancel request and terminate invocation separately; no invented child code or cleanup receipt |
| EP-29 | Worker disappears or page closes before terminal observation is persisted | Attempt remains unresolved/INCOMPLETE; recovery does not infer PASS/FAIL or auto-rerun |
| EP-30 | Pyodide guest attempts Python `subprocess` on iOS/Android/WASI | Capability is reported unsupported; no simulated child process or exit code |
| EP-31 | Native Python runner uses `shell=True` | Record shell PID/return code as wrapper/shell evidence, not target-program child evidence |
| EP-32 | POSIX child is signal-terminated; shell may expose 128+N | Preserve raw return code, signal and termination cause separately; no cross-platform numeric inference |
| EP-33 | Native process emits exit before stdio closes | Execution exit may be known while output collection remains pending; do not finalize artifact/receipt before stream close and digest verification |
| EP-34 | Late terminal message arrives for a prior attempt after a retry starts | Reject cross-attempt binding; retain late evidence on original attempt only |
| EP-35 | Guest sends a forged terminal message or reuses an attempt ID | Host validates message channel, schema, identity and sequence; guest-controlled claims alone cannot establish trusted completion |

### Required evidence layers

| Layer | Valid evidence | Not established by it |
|---|---|---|
| Guest/program | Program output, return value, exception text | Process identity, OS exit, trusted policy or termination |
| PWA runner wrapper | Completion/exception observed by trusted wrapper | OS child process or durable receipt |
| Browser Worker API | Worker error event or host terminate invocation | Native exit code, cleanup of unrelated resources or durable artifact |
| Native process supervisor | Bound child exit code/signal and process identity | Stdio fully drained, artifact durable or policy satisfied |
| Output collector | Streams closed, bounded bytes captured and digest computed | Artifact manifest committed or client received bytes |
| Durable receipt | Exact artifact/version bound to attempt and committed metadata | Client receipt unless separately acknowledged |

## 5. Corrections and red-team findings

1. **Do not overgeneralize "child exit" to a PWA.** The canonical model uses child-process language, but the no-spend PWA path runs browser workers/Pyodide. Add a runtime adapter distinction before implementing a report field called `child_exit_code`.
2. **Do not treat `terminate()` as an exit event.** It returns no value and exposes no completion event. Record the control invocation, then retain INCOMPLETE unless independent trusted terminal evidence exists.
3. **Do not treat worker `error` as a process exit.** It identifies a worker error, not a child return code or cleanup acknowledgement.
4. **Do not assume Python `subprocess` exists in mobile/WASM.** Official Python documentation explicitly excludes Android, iOS and WASI. A Pyodide design cannot silently rely on it.
5. **Do not finalize artifacts on process `exit` alone.** Node's documented `close` event occurs after stdio closes; a future native runner must separately track output completion.
6. **Do not interpret numeric signal conventions cross-platform.** Python's negative signal return code is POSIX-specific, and `shell=True` may map a signal to 128+N. Keep signal and wrapper/shell status distinct.
7. **Do not mistake repository Pages enablement for verified deployment.** `has_pages=true`, null homepage and no main-branch CNAME do not establish the effective hostname, deployed SHA or response headers.
8. **Do not conflate O-5 labels across projects.** PocketCode O-5 concerns typed child exit, wrapper exit and termination provenance. Any RevDev O-5 decision belongs only to RevDev and must not be copied into this repo or used to close a PocketCode decision.

## 6. Source quality and reuse

| Source | Opened/version evidence | Maintenance/licence/reuse |
|---|---|---|
| HTML Living Standard, workers | Living Standard updated 2026-11-09; opened 2026-11-10 | Normative web standard; no code copied |
| MDN Worker.terminate | Page last modified 2024-07-26; opened 2026-11-10; Baseline API | Maintained reference docs; no code copied |
| Python subprocess docs | Python 3.15.2 docs; opened 2026-11-10 | Official CPython docs; PSF project; no code copied |
| Node.js child_process docs | Node.js v26.13.0 docs opened 2026-11-10; upstream LICENSE blob `ec72f56e16fb19944a55acdbff67727d2bfadb8a` opened | Official Node docs; MIT license verified; semantic reference only, no code copied |

Primary references:
- [HTML Living Standard: Web Workers](https://html.spec.whatwg.org/multipage/workers.html)
- [MDN: Worker.terminate()](https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate)
- [Python 3.15: subprocess](https://docs.python.org/3/library/subprocess.html)
- [Node.js v26.13.0: child_process](https://nodejs.org/api/child_process.html)
- [PocketCode Pages workflow](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/.github/workflows/preview-prototype.yml)
- [PocketCode canonical execution acceptance](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md)

No code copied, dependencies added or stack selected. No source/tests, deployment, Pages settings, canonical LOOP/CASE/D IDs or owner decisions changed.

## 7. Verification status

- **VERIFIED:** repository Pages enabled flag, null homepage, main default branch, main-only automatic workflow trigger, artifact root path, main tree's lack of CNAME, worker termination API/algorithm, Python subprocess mobile/WASI unavailability, Python POSIX/shell return-code semantics, Node exit/close distinction.
- **INFERRED:** the no-spend PWA path cannot use Python `subprocess` as its child-process supervisor; a worker result is runner-level evidence, not OS process exit.
- **UNKNOWN:** exact Pages URL/custom domain, actual deployment SHA/environment URL, live headers/meta CSP, sibling origin inventory, target iOS/Android engine behavior, future runtime's process/termination contract.
- **NOT RUN:** live deployment verification, ORIGIN/PAGES tests, worker crash/termination tests, Pyodide subprocess capability probe on the owner's device, native process adapter tests, output-close/crash tests, device tests.
- P39/P40 implementation gate remains CLOSED; OD-01..OD-13 remain OPEN. No implementation authorization is implied.


## 8. Current-branch execution inventory (2026-11-10 follow-up)

- **VERIFIED:** the active branch tree contains the Pages prototype at `prototypes/mobile-runner/index.html`, its README, the static checker/tests and the Pages workflow. The prototype README explicitly says it is simulation-only and does not execute Python, import files, create artifacts, select a runtime or call a provider.
- **VERIFIED:** the prototype HTML labels itself “SIMULATED EXAMPLE — NOT AN EXECUTION”, and its visible controls switch between expected examples and copy simulated report/prompt text. It contains no Pyodide import, Worker construction, MessageChannel, runtime bridge or execution dispatch.
- **VERIFIED (bounded inventory):** a recursive current-branch tree search for worker, Pyodide, bridge, runner and execution paths found no PocketCode implementation file for a Pyodide worker or runtime bridge. This does not prove no external/installed app implementation exists.
- **INFERRED:** the conditional PYO-CTRL spoofing scenario is not exploitable through the committed Pages prototype because that prototype does not execute guest code or instantiate a worker. It remains a design requirement for any future real execution path.
- **UNKNOWN:** whether the owner's separately installed Pyodios app has a worker/runtime implementation matching the conditional threat model. No app bundle or device was inspected.
- **NOT RUN:** browser interaction, worker construction, Pyodide execution, exploit reproduction, live Pages deployment, and device tests.

This narrows the finding: do not describe the current prototype as vulnerable or as an execution runtime. Preserve the private-control-channel acceptance tests as future implementation gates, and inspect the actual execution source only when that implementation is available and authorized for review.
