# PocketCode — Pyodide Attenuation Decision, Execution-Boundary Comparison and Lifecycle Evidence Matrix

**Date:** 2026-11-03  
**Status:** Source-level research and contract crosswalk only. No product implementation, runtime/device test, provider workload, or canonical acceptance change.  
**Authority:** Research addendum. Canonical LOOP-01..14 and CASE-01..16 remain unchanged. D-01..D-08 remain owner-open/proposed as recorded in the owner decision register.  
**Pyodide pin:** pyodide/pyodide tag 314.0.7.  
**Linux reference pin:** slopus/happy-agent commit fb9f68ff10333068b87436bd1d531d6d353f5c93.

## 1. Executive decisions

1. **Do not adopt Pyodide 314.0.7 as a hostile/untrusted-code sandbox through a trusted-bootstrap attenuation patch.** The public API does not provide a supported capability-revocation mode. Initialization leaves Python-visible JavaScript proxies and module references; FFI exposes JavaScript-module registration; source itself says it cannot generally track module global state. Safari's restrictive-CSP incompatibility adds a material cross-platform blocker. A fork or recurring internal patch/audit would be disproportionate.
2. **Do not discard Pyodide entirely.** The fixed synchronous CSV-to-JSON task is standard-library-only and does not inherently require JavaScript interop, networking, package installation, or async execution. Pyodide may remain a trusted/small-task browser convenience candidate, provided product claims do not imply hostile-code isolation, hard resource quotas, or trusted termination.
3. **Retain Happy Agent Linux strict-service as a source reference, not an adopted dependency/provider.** It is the strongest inspected containment pattern, but it fails PocketCode's current CASE-04 deadline requirement and lacks CPU quota and complete storage/output controls. Other source-level gaps remain.
4. **Treat a user-owned remote PC as a future execution option, not a present capability.** The PC, checkout, runtime, credentials, network, and queue state remain UNKNOWN until the owner returns and supplies fresh evidence. Remote access by itself is not a sandbox.
5. **Keep manual copy/paste as the first workflow baseline, not an execution path.** It can validate task-packet usability, report readability, and the AI correction loop. It cannot establish execution, exit status, file creation, isolation, or runtime evidence.
6. **Keep execution outcome, job disposition, cleanup, artifact release, and report publication separate.** Unknown at any boundary must remain unknown. A known program failure is not rewritten because cleanup is uncertain; cleanup uncertainty blocks artifact release where relevant.

## 2. Pyodide 314.0.7 attenuation feasibility

### 2.1 Source findings

Pinned source inspected:

- [Import hook](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/_pyodide/_importhook.py)
- [FFI exports](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/ffi/__init__.py)
- [Package loader](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/_package_loader.py)
- [Webloop](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/webloop.py)
- [State save/restore](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/_state.py)
- [JavaScript API construction and bootstrap](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/api.ts)
- [Package-manager loadedPackages object](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/load-package.ts)
- [JavaScript evaluation helper](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/code.py)
- [JsProxy and to_js documentation](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/_pyodide/_core_docs.py)
- [Safari CSP test](https://github.com/pyodide/pyodide/blob/314.0.7/src/tests/test_pyodide.py#L1856-L1865) and [CSP fixture](https://github.com/pyodide/pyodide/blob/314.0.7/src/templates/test_csp.html)

Findings:

- jsglobals supplies the Python js module; it does not suppress the separately registered pyodide_js module.
- The public pyodide_js object exposes FS, PATH, ERRNO_CODES, _module, and _api. FS includes filesystem backends such as IDBFS.
- unregister_js_module(name) deletes the name from the import finder's jsproxies mapping. It does not revoke already imported module objects or clear sys.modules; Pyodide documents that callers must separately delete imported entries.
- pyodide.ffi exports both register_js_module and unregister_js_module. Registration requires a JsProxy, but the FFI intentionally supports JS object proxies and conversion of Python values to JS objects.
- _package_loader.py imports pyodide_js.loadedPackages during initialization and retains that reference in a module global. Deleting pyodide_js from sys.modules does not remove this separate reference.
- loadedPackages is initialized as a normal JavaScript object by the package manager. The Python package loader also mutates it while initializing package metadata.
- pyodide.webloop imports pyodide_js._api.scheduleCallback into a module global. This is another surviving JS-backed reference after normal bootstrap.
- pyodide._state.save_state() captures JS modules in sys.modules, the import-finder registry, and __main__ globals, but explicitly states that there is no general way to track all module global state.
- pyodide.code.run_js() imports eval from js. Hiding js can block this particular route, but does not prove that every other reference to privileged JS objects has been removed.
- The FFI's documented JsProxy surface exposes a JavaScript object's constructor; to_js() creates JS object proxies. This makes it unsafe to treat FFI as a harmless one-way data conversion. Whether a constructor-based code-generation route is executable is CSP-dependent; no exploit was executed in this audit.
- Pyodide 314.0.7 marks its restrictive-CSP test expected-fail on Safari because Safari does not support wasm-unsafe-eval. The fixture uses wasm-unsafe-eval rather than JavaScript unsafe-eval. Do not silently weaken CSP to make the runtime load.

### 2.2 What the fixed task needs

The frozen CSV-to-JSON fixture uses standard-library CSV, Decimal arithmetic, JSON, and filesystem operations. Its task logic does not inherently need:

- js or pyodide_js;
- JavaScript evaluation;
- browser fetch/network;
- package installation;
- Pyodide's asynchronous webloop;
- direct access to the Emscripten FS object from user Python.

A trusted wrapper could stage bounded input files into a fresh in-memory filesystem, invoke a synchronous Python entrypoint, capture bounded output, and retrieve bounded output files. That is a plausible functional execution path, not a demonstrated secure one. The exact post-attenuation bootstrap, standard I/O, exception path, file staging, and worker termination have not been tested.

### 2.3 Decision and stop rule

**Reject the trusted-bootstrap attenuation experiment as a maintainable hostile-code sandbox candidate without a fork.** A correct proof would need to control not only import names but every cached JS proxy, package-loader reference, webloop reference, FFI route, module-global reference, and browser code-generation path. Pyodide does not expose a stable public switch for disabling this capability surface. Its own state snapshot implementation does not promise complete tracking of module globals. Every upgrade would require a new private object-graph audit and adversarial test campaign.

A fork or recurring internal patch is not justified under the current phone-only, $0, no-runtime-selection constraints. Keep Pyodide only as an optional trusted/small-task convenience comparator. If future product requirements demand hostile Python in a browser, reopen only with a separately funded/maintained security design and target-device proof. Do not call the current proposal a sandbox.

**Evidence limit:** pinned source inspection only. No runtime, exploit, browser, Safari, PWA, or device test was performed.

## 3. Execution-boundary comparison

The four paths are not equivalent. The relevant question is not simply whether Python code runs, but who controls the boundary, what the code can reach, how it is stopped, and what evidence survives failure.

| Dimension | Browser Pyodide | Isolated Linux service reference | User-owned remote PC | Manual copy/paste |
|---|---|---|---|---|
| Execution location | Browser worker/WASM in a separate static execution origin | Linux host/service with namespaces and cgroup v2 | Owner's Windows/Linux PC reached remotely; current PC state UNKNOWN | No execution in PocketCode |
| Trust boundary | Browser origin, worker, CSP, iframe/message bridge, Pyodide FFI | Kernel namespaces/cgroups, private root, supervisor, optional egress broker | Depends entirely on a separately designed sandbox/VM/low-privilege worker; SSH/Tailscale alone is transport | User and external tools; no PocketCode execution boundary |
| Files | MEMFS by default; browser persistence requires explicit backend; direct user Files access is platform-specific | Private root, selected read-only mounts, private scratch; inspected reference uses live mounts, not immutable snapshots | Can stage files, but host paths and permissions are dangerous unless constrained | Attach/paste files and outputs manually; no verified artifact provenance |
| Secrets/network | Worker is not inherently network-disabled; CSP and origin isolation narrow access. Pyodide API/FFI attenuation is not established | Egress-off posture is structurally represented; Windows adapter unsuitable as-is. Egress-on has filter/L7 gaps | Must explicitly remove credentials and deny egress in the sandbox. Host user credentials must not enter child environment | No execution secrets exposed by PocketCode, but manually pasted content may disclose whatever the user includes |
| CPU/memory/time | No hard OS CPU quota; browser memory/worker lifecycle limits are not PocketCode-enforced quotas. Interrupt is cooperative; Worker.terminate is separate and needs device proof | Memory and PID cgroup limits present; no service-level absolute deadline or CPU quota; storage/output limits incomplete | Potentially enforceable with VM/job supervisor and kernel limits, but no design or current evidence | Not applicable |
| Stop/cleanup | Parent can request Worker.terminate; actual stop, browser lifecycle and resource recovery require target Safari/PWA proof | Process/cgroup reconciliation patterns present; no absolute deadline, and egress-child parent-death race remains | Must use independent watchdog, process-tree/VM termination and recovery; currently unverified | No run to stop |
| Result evidence | Browser-observed result only; worker message is untrusted. Parent disappearance or timeout is not proof of stop | Stronger host-side process identity and cgroup evidence patterns, but missing deadline and collector semantics | Could provide authoritative host result if trusted agent persists observations and reconciles after disconnect | User-provided transcript/output only; not execution attestation |
| Cost/availability | Could be local and avoid provider spend; payload/startup/device performance NOT RUN | Self-operated host cost and operations are unknown; no host selected | Requires reachable owner PC and connectivity; no PC available now | $0 and immediately available |
| Product status | Candidate only for trusted/small tasks; hostile-code sandbox rejected | Strongest inspected Linux reference, not selected or adapted | Future option after PC return and separate security design | Valid first workflow baseline, not a product execution backend |

### 3.1 Mapping to LOOP-01..14

| Criteria | Browser Pyodide | Linux service reference | Remote PC | Manual copy/paste |
|---|---|---|---|---|
| LOOP-01 phone code/input | Possible with explicit paste/file picker; NOT RUN | Requires phone client + remote host; not demonstrated | Requires phone client + remote access; unavailable now | Supports manual code/input handoff |
| LOOP-02 honest state | Must distinguish worker messages from trusted observations | Host supervisor could provide lifecycle evidence; reference incomplete | Requires durable remote agent/coordinator | Can label manual stages, not execution states |
| LOOP-03/04 PASS/FAIL | Possible only with trustworthy terminal evidence; NOT RUN | Process evidence patterns exist, but no PocketCode adapter | Possible if host agent is authoritative | Cannot establish |
| LOOP-05 INCOMPLETE | Must treat worker/page loss as unknown until stop/reconciliation | Deadline and provider-loss semantics still incomplete | Requires watchdog/reconciliation | Can honestly state not executed |
| LOOP-06 structured checks | Task/report layer can preserve checks | Task/report layer can preserve checks | Task/report layer can preserve checks | Can preserve pasted checks with provenance labels |
| LOOP-07 diagnostics | Browser-captured output requires strict bounds and honest truncation | Caller must implement collector limits; service alone does not prove them | Agent must implement bounded collectors | Manual transcript can be bounded but not independently verified |
| LOOP-08 copy result | Yes as UI workflow; report truth still depends on execution | Yes via client | Yes via client | Strong fit |
| LOOP-09 correction loop | Yes in principle; per-run evidence must persist | Yes with durable run identity/history | Yes with durable remote history | Strong fit |
| LOOP-10 artifacts | Browser download possible; provenance/storage/release gates NOT RUN | Private output staging possible; output and release gates incomplete | Possible with authenticated, immutable run-scoped artifacts | Manual file transfer only |
| LOOP-11 privacy | Separate origin, bounded copy and no credentials required; browser capability risk remains | Clean environment pattern; no credentials and egress-off required | Must isolate from PC user files/secrets | User controls what is pasted |
| LOOP-12 isolation | **Not accepted for hostile code**; no verified sandbox or hard quotas | Strong reference, but CASE-04 and resource/output gaps block acceptance | Could satisfy only with independently verified sandbox | No code execution |
| LOOP-13 automation honesty | No clipboard polling or background claims without device proof | Not relevant to server boundary; mobile UX still needs proof | Remote control is not automatic AI capture | Explicit manual handoff is honest |
| LOOP-14 zero-cost | Potentially local, but device/payload costs unmeasured | Host/operations cost unknown | User-owned host cost unknown; no spend authorized | $0 baseline |

### 3.2 Mapping to CASE-01..16

- **CASE-01..03 (valid run, syntax error, runtime exception):** all three execution paths could produce these observations in principle. None has been validated through the PocketCode product path. Manual copy/paste cannot independently establish them.
- **CASE-04 (enforced deadline):** browser worker termination is not yet target-device evidence; Linux strict-service lacks an internal absolute deadline; remote PC would need an independent trusted watchdog and confirmed whole-job stop. Manual path does not execute.
- **CASE-05 (cancellation):** same stop distinction. A request or client timeout is not termination confirmation.
- **CASE-06 (infrastructure failure):** all execution adapters need to preserve UNKNOWN when no trustworthy terminal result exists. Remote disconnect is not a program exit.
- **CASE-07 (output limit):** each execution path needs a bounded streaming collector and explicit overflow evidence. The Linux service layer does not supply PocketCode's collector contract; browser and remote paths are NOT RUN.
- **CASE-08 and CASE-14 (unsafe inputs/outputs):** Linux reference has useful path/mount controls but needs regular-file-only input policy, immutable snapshots, output caps and release checks. Browser/remote implementations need equivalent tests. Manual transfer does not prove safe path handling.
- **CASE-09 and CASE-10 (program-reported check versus process exit):** adapter-independent report semantics. Never trust text printed by the program as terminal proof.
- **CASE-11 (browser/client disconnect):** a local browser worker may continue after UI loss; a remote service needs authoritative reconciliation. Never infer stopped/completed from a disconnected client.
- **CASE-12 (copy report after failure):** all paths must preserve actual state and uncertainty. Manual copy/paste can test report readability, not the truth of unexecuted results.
- **CASE-13 (ambiguous retry):** requires durable idempotency reservation and reconciliation at the coordinator boundary. A remote host or local worker alone does not establish it.
- **CASE-15 (network/secrets):** Pyodide is not accepted as hostile-code sandbox; Linux egress-off and clean-environment patterns are useful but not a full PocketCode proof; remote PC must remove ambient credentials and enforce egress externally.
- **CASE-16 (out-of-order concurrent runs):** requires stable run/attempt identity and durable result/artifact association. No path has been validated through PocketCode.

## 4. Lifecycle and evidence matrix

The lifecycle is a chain of independent decisions. Each stage records its own state and evidence. Do not collapse the chain into one status or infer a later stage from an earlier one.

| Stage | Distinct state vocabulary (proposed projection, not canonical enum) | Required authoritative evidence | If evidence is absent, conflicting or stale |
|---|---|---|---|
| 1. User intent | absent / received / malformed / ambiguous / superseded | Explicit user request, source/input references, requested operation, constraints, stable client submission identity | Do not infer consent, policy approval or authorization. Preserve malformed/ambiguous intent and ask for correction only when required. |
| 2. Policy decision and application | pending / approved / denied / applied / application_unknown / stale | Versioned policy decision; exact policy revision bound to this attempt; trusted boundary acknowledgement or effective configuration proving the required policy is applied before code starts | No dispatch while required policy application is unknown, stale or unconfirmed. Request acknowledgement/ETag alone is insufficient. |
| 3. Authorization | not_required / pending / authorized / denied / expired / unknown | Authenticated subject/tenant, scoped permission, operation and artifact scope, current authorization revision, required user confirmation | User intent is not authorization. Unknown/expired authorization denies the protected action without pretending the user never requested it. |
| 4. Reservation and dispatch | not_started / reserved / dispatch_intent_persisted / acknowledged / dispatch_unknown / reconciled / rejected | Durable tenant-scoped idempotency reservation, versioned canonical request fingerprint, attempt identity, persisted dispatch intent, provider/host acknowledgement or authoritative lookup | Lost acknowledgement or ambiguous start means UNKNOWN. Reconcile the same identity. Do not automatically create a new attempt. Same key/same fingerprint replays; same key/different fingerprint conflicts before allocation. Exactly-once execution is not claimed without boundary support. |
| 5. Execution | not_started / starting / running / terminal_observed / execution_unknown | Trusted process/worker identity, start observation, monotonic start/deadline, applied resource/network policy, process/worker liveness, termination cause and trusted terminal observation | A client timeout, closed socket, missing message or page loss is not proof of termination. Preserve UNKNOWN. A browser worker's own terminal message is untrusted until corroborated by the parent boundary. |
| 6. Program result and job disposition | raw outcome: exit_zero / nonzero / runtime_error / timed_out / cancelled / no_terminal / conflicting; disposition: accepted / queued / running / succeeded / program_failed / timed_out / cancelled / rejected / infrastructure_failed; user verdict: PASS / FAIL / INCOMPLETE | Trusted terminal observation and actual exit code where available; source and authority of each event; required case-specific evidence; stable run/attempt association | PASS only with trusted completion and exit zero plus evidence required by that case. Confirmed program failure remains FAIL even if cleanup is unknown. Timeout follows CASE-04: INCOMPLETE / timed_out. Provider loss without child result remains INCOMPLETE / UNKNOWN. Contradiction or missing terminal evidence remains INCOMPLETE. |
| 7. Cleanup and teardown | not_started / pending / confirmed / failed / unknown / not_applicable | Trusted worker/process-tree or cgroup-empty evidence; scratch/volume teardown; resource release; orphan reconciliation; cleanup event source and timestamp | Never infer cleanup from process exit or client disconnect. Cleanup uncertainty is independently visible and blocks artifact release where applicable; it does not rewrite a known program verdict. |
| 8. Artifact integrity and release | absent / quarantined / integrity_verified / eligible / released / denied / unknown | Trusted manifest; exact immutable object/digest; run/attempt/job/tenant association; safe path/type/size; cleanup/quarantine state; current release-time authorization | No artifact is not a universal execution failure. Existing artifact remains quarantined until all applicable gates pass. Unknown or stale authorization, identity or integrity denies release. Release denial does not rewrite historical execution result. |
| 9. Report creation and publication | not_created / assembling / issued(version) / partial / failed / superseded | Immutable evidence references, monotonic report version, source/provenance labels, bounded output and explicit capture states, publication acknowledgement | Report is a projection of evidence, not evidence of execution and not an authorization token. Missing fields remain UNKNOWN/UNAVAILABLE; contradictory or late evidence creates a new version rather than silently rewriting an issued report. |

### 4.1 Evidence vocabulary that must remain distinct

- **Execution outcome:** what the program demonstrably did.
- **Job disposition:** what the coordinator/provider did with the attempt.
- **Cleanup state:** whether the execution environment and descendants are confirmed gone and resources reconciled.
- **Artifact state:** whether output exists, is intact, is associated with the correct attempt, and may currently be released.
- **Report state:** whether an immutable evidence projection was successfully assembled and issued.

For stdout/stderr and diagnostics, preserve COMPLETE, PARTIAL, UNAVAILABLE, EMPTY, RUNTIME_LIMIT, and DISPLAY_TRUNCATED as distinct facts. A collector/runtime cap is not display clipping. Optional diagnostics do not become universal PASS gates; each canonical case determines its required evidence.

### 4.2 Owner-open decisions retained

- **D-01:** owner-open for any canonical change. Current canonical CASE-04 working default remains INCOMPLETE / timed_out for trusted timeout; record limit cause separately.
- **D-02:** owner-open before schema/test freeze. Working default: provider failure without child exit means INCOMPLETE and execution outcome UNKNOWN; only label PROVIDER_ERROR when cause is confirmed.
- **D-03:** owner-open before schema/gate freeze. No universal complete-output or artifact-presence requirement; only evidence explicitly required by the case gates PASS.
- **D-04:** owner-open. Scoped event identity, replay/conflict semantics and coordinator ordering remain proposals.
- **D-05:** proposed policy-revision binding / applied-policy barrier; owner review remains required.
- **D-06:** proposed durable idempotency and ambiguous-dispatch recovery; owner review remains required.
- **D-07:** proposed release-time authorization and immutable artifact-integrity gate; owner review remains required.
- **D-08:** proposed append-only, crash-safe report history and publication reconciliation; owner review remains required.

No canonical LOOP or CASE ID is added, removed, merged or remapped by this matrix.

## 5. Cross-agent reconciliation

The current source evidence does not justify changing the existing decisions. Claude's and Gemini's prior reports remain useful review inputs, but their claims are subordinate to exact pinned source and explicit acceptance wording. The present Pyodide conclusion is based on the 314.0.7 source graph, not on a claim that either AI executed a sandbox escape. No new direct communication with either AI occurred. The owner continues to forward reports manually.

The Linux service conclusion remains consistent with the earlier review: useful kernel-boundary patterns, but missing absolute deadline/CPU quota/storage-output completeness prevents adoption as-is. No AI review changes that source-level gap.

## 6. Current project gates and next work

- Canonical LOOP-01..14 and CASE-01..16: unchanged; NOT RUN except the separately recorded isolated fixture sanity check.
- Fixed-task product-path comparison: NOT RUN.
- Paired AI correction experiment: designed, NOT RUN; differentiator UNVALIDATED.
- Browser Pyodide: hostile-code sandbox rejected as a maintainable no-fork candidate; trusted/small-task convenience remains a comparator only.
- Linux service: source reference only; no PocketCode adaptation or runtime verification.
- Remote PC: unavailable; all local state UNKNOWN until owner returns.
- Manual copy/paste: available as the workflow baseline, not execution evidence.
- Provider/runtime/framework/dependency: NONE selected.
- Budget: $0.
- PR #2/#3: protected, untouched, open/draft/unmerged.
- Product source/tests, Actions, runtime, queues, accounts, secrets, deployment, installation and host state: unchanged.

Next work should prioritize refining the first useful manual workflow and keeping the PC-return checklist actionable. Reopen execution-boundary selection only when a concrete $0-capable environment and its real security/resource/termination evidence can be evaluated. Do not repeat broad provider or framework surveys.
