# Gemini Open-Source Research Review — PocketCode + RevDev

**Date:** 2026-11-01  
**Input:** Owner-pasted Gemini four-stage research report (full text supplied in chat).  
**Review status:** Desk review plus targeted primary-source checks. NOT a complete source-code audit.  
**Decision status:** Research triage only. No dependency, provider, runtime, architecture, licence exception, implementation or integration approved.

## 1. Executive verdict

Gemini's report is a useful discovery catalogue, but it does not meet the evidence standard required for adopting code or selecting an architecture. Its largest weakness is the gap between a list of project names and verified reuse instructions: the report contains incomplete section details, generic `[1]...[5]` citations, repeated uploaded-file references that are not accessible as source evidence here, few exact source paths/revisions, and no reproducible module-level review. Its confident "P1/P2" rankings and four-phase convergence roadmap are therefore not accepted.

The report also proposes more architecture than the current product proof needs. PocketCode's first useful proof remains one bounded phone-first code task, a truthful run result, and an effective correction loop. The execution location remains undecided. The current proposed contract explicitly excludes autonomous LLM loops, arbitrary shell, persistent workspace, multi-user collaboration, arbitrary runtime images and guaranteed network access from the first proof. RevDev remains a separate Windows mission/automation system. Shared protocols may be considered later; a unified graph engine/runtime is not a current requirement.

**Administrative ruling:** treat every Gemini project as a candidate to investigate, not an adopted dependency. Keep the existing architecture-neutral contracts and acceptance criteria authoritative. Do not change canonical LOOP/CASE IDs, report schema, PRs, source, tests, provider selection or execution boundary on the basis of this report.

## 2. Highest-value findings to carry forward

| Candidate | Provisional value | Current disposition |
|---|---|---|
| CodeMirror 6 | Strong candidate for the browser/PWA editor layer; its source contains deliberate Android Chrome and iOS/Safari composition/input handling. | **KEEP / inspect deeper.** Do not assume it makes the entire mobile UX solved; test on target iPhone and Android devices. |
| Pyodide | Strong candidate for a browser-local Python path and a fair comparator on the fixed standard-library CSV task. | **KEEP / compare, not select.** Browser WASM is not a general-purpose server sandbox or proof of safe access to all browser APIs. |
| wasmsh | Interesting shell/VFS capability design; current project README claims standalone WASM, Pyodide integration, allowlisted brokered networking and step budgets. | **INVESTIGATE.** Small/young project; claims are upstream claims, not independently verified. Do not make shell part of MVP by default. |
| Tailscale tsnet | Potential way to embed a tailnet node in a Go service without a separate tailscaled daemon or system network configuration. | **CONDITIONAL / architecture mismatch.** It is Go, while RevDev is currently PowerShell/.NET-oriented. Requires a Go sidecar/service or substantial interop, tailnet identity/auth and operational design. |
| Aider repository map | Useful pattern for extracting compact symbol-level repository context and reducing repeated source dumps. | **KEEP AS PATTERN / optional utility.** Not needed for the first run-loop proof; inspect API and dependency/licence details before copying code. |
| LangGraph | Mature graph/checkpoint/human-in-the-loop orchestration capability. | **DEFER.** The first proof does not need an autonomous multi-step agent graph. Checkpoint persistence is not exactly-once external execution, provider state recovery or idempotency. |
| Piston | Useful reference for an established Linux execution API and status/output model. | **REFERENCE ONLY / no hosted dependency.** Public API is no longer freely available as of 2026-02-15; self-hosting requires Linux/Docker/Isolate operations and a security review. |
| OpenHands editor | Targeted file-editing interface may be useful later. | **DO NOT adopt archived ACI repo.** The `openhands-aci` repository is archived (2026-05-15); upstream says the editor moved to the OpenHands Agent SDK. Review the current SDK, not archived source. |
| FlaUI | Potential Windows UI Automation library for C# if RevDev has a demonstrated UIA automation gap. | **CONDITIONAL / defer.** Not a generic mission runner; no current evidence that it solves a priority RevDev problem. |
| Watchdog | Cross-platform Python filesystem event abstraction. | **PATTERN ONLY.** RevDev's known watcher/runtime is PowerShell. Do not introduce a Python observer just to replace an existing Windows watcher. Filesystem events must be treated as hints, with reconciliation/rescan and idempotent processing. |

## 3. Material technical corrections

### 3.1 Pyodide is not a complete security boundary by itself

Pyodide is CPython compiled to WebAssembly/Emscripten and runs in browsers or Node. Its Python environment can access browser Web APIs through the JavaScript/Python interface. The browser/WASM boundary prevents ordinary direct host OS access, but it does not mean that all network calls are forced through a PocketCode-controlled broker or that code cannot access browser-origin capabilities exposed to its execution context.

The default Pyodide filesystem is in-memory MEMFS and is lost on reload. IDBFS persistence requires explicit synchronization. Pyodide's documented native browser filesystem mount is experimental and Chromium-only; this is not equivalent to direct iOS Files-folder access. Browser workers can protect UI responsiveness and be terminated by the host, but this does not establish all server-style resource limits, durable lifecycle evidence, or a trusted execution receipt.

**Correction:** describe Pyodide as a promising browser-local Python runtime with browser-specific capability and lifecycle limits. Any untrusted-code design must isolate origins/contexts, avoid exposing secrets or privileged JS bridges, control network/browser APIs, and test resource/termination behavior on supported devices. Do not label it a fully isolated secure sandbox without that boundary analysis.

### 3.2 wasmsh is promising but unverified

The current upstream README describes a Rust Bash-compatible shell compiled to WASM, an in-memory capability-based VFS, host-mediated hostname allowlisting for network commands, step budgets, and optional scalable Kubernetes deployment. It states Apache-2.0. These are useful design claims, but Gemini did not provide exact pinned commit, test evidence, independent threat-model review, supported command semantics, mobile browser measurements, or an integration spike.

**Correction:** keep it on the investigation list. Verify the exact repository revision, source implementation of budgets and network broker, VFS escape assumptions, dependency tree, licence notices, browser/worker integration and resource behavior before considering reuse. It does not justify exposing arbitrary shell in the first PocketCode MVP.

### 3.3 tsnet does not drop into RevDev as proposed

`tsnet` is a Go library embedding a Tailscale node in a Go process. It can provide tailnet-scoped network listeners and uses a userspace networking stack. It does not provide a drop-in C# or PowerShell library. Adopting it in RevDev means operating a Go component/sidecar or designing a different interop boundary. Tailscale network ACLs are not a substitute for application authorization: the application must still decide which peer identity may invoke which operation.

Gemini's pairing of embedded Go `tsnet` with Python AsyncSSH is not a demonstrated integration. Tailscale's Go package itself documents an SSH listener API; alternatively, a small authenticated HTTPS/gRPC service may be simpler than exposing a general shell over SSH. Any route needs explicit pairing, identity lifecycle, least privilege, revocation, audit, PC availability and zero-cost review.

**Correction:** keep remote-PC execution as a possible path. Do not approve tsnet, AsyncSSH or an SSH execution API until the fixed-task experiment shows remote-PC value and the transport/authorization boundary is designed.

### 3.4 LangGraph persistence is not execution recovery

LangGraph checkpointers persist graph-state snapshots and support thread continuation, human-in-the-loop flows and graph-level fault tolerance. That does not make an external execution side effect exactly once, prove provider process termination, reconcile a lost dispatch acknowledgement, or prevent a graph node from repeating a non-idempotent operation after restart.

**Correction:** defer LangGraph. If multi-step agent orchestration later becomes a real requirement, compare it with smaller state-machine approaches and the existing proposed coordinator/event contracts. External side effects still need stable attempt identity, authoritative lookup, idempotency and reconciliation independent of graph checkpoints.

### 3.5 Piston facts are version/configuration-specific and hosted access is not free

Piston's README documents Isolate inside Docker, Linux namespaces, cgroups, unprivileged users, default network disablement and configurable resource/output limits. The familiar 3-second CPU default and 1024-character output default are documented defaults, not immutable security guarantees. Actual deployment configuration, kernel, Docker/Isolate versions, host hardening, resource accounting, termination and cleanup must be independently verified.

Most importantly, Piston's own README states that its public API has not been freely available to the public since 2026-02-15 and requires authorization; it suggests self-hosting the open-source engine instead. That makes it unsuitable as an assumed free hosted provider under our $0 constraint.

**Correction:** retain Piston as a reference implementation for Linux runner API/status concepts only. Do not depend on its public API. Self-hosting is not $0 operationally by definition and would reopen the blocked provider/resource/teardown gates.

### 3.6 OpenHands ACI is archived

The exact `OpenHands/openhands-aci` repository reports that it was archived on 2026-05-15 and that the file editor moved to the OpenHands Agent SDK. Gemini's P2 recommendation points at an archived repository and does not pin the current replacement.

**Correction:** do not adopt `openhands-aci`. If file-editing becomes a priority, inspect the current Agent SDK implementation and licence at a pinned revision, compare it to the narrow edit operations PocketCode actually needs, and evaluate path confinement, patch validation, diff review and rollback.

### 3.7 CodeMirror's mobile handling is real, but not a solved UX

CodeMirror 6's input source contains explicit composition state handling, Android Chrome key/input workarounds, and iOS/Safari behavior. This supports investigating it as a browser editor. It does not prove a finished mobile coding experience, correct accessory bar, viewport/keyboard behavior, selection, external keyboard handling, or native app integration.

**Correction:** candidate for the PWA/browser editor, followed by device acceptance. Do not infer that a native React Native/Compose editor is needed or that CodeMirror solves it all.

### 3.8 FlaUI and Watchdog are conditional and stack-specific

FlaUI wraps Windows UI Automation APIs for .NET desktop application automation. It is useful only if RevDev needs reliable UIA2/UIA3 interaction that its existing automation stack does not provide. Watchdog is a Python cross-platform filesystem event library, not a drop-in replacement for RevDev's PowerShell watcher. Native file notification streams can duplicate, coalesce, overflow or miss events; robust queue behavior still needs authoritative directory reconciliation, stable file readiness, deduplication and idempotent processing.

**Correction:** retain both as conditional references. First identify a concrete gap in RevDev and compare integration cost against its existing PowerShell/.NET architecture.

### 3.9 Judge0 GPL-3.0 is not an automatic rejection

Gemini describes GPL-3.0 as a blanket source-disclosure risk. That is too broad. GPL obligations depend on what is copied/modified, how components are combined, and whether copies are conveyed/distributed; merely offering network access to a GPL program is not automatically the same as conveying it. AGPL has a distinct network-interaction provision. This is not legal advice.

**Correction:** Judge0 remains a poor current fit primarily because it is a hosted/server execution platform with operational and security costs, not because GPL-3.0 automatically forces disclosure of all PocketCode source. Any future use requires a component-level licence and distribution review.

## 4. Security-contract reconciliation

Gemini identifies several real invariants but overstates or universalizes them:

1. **Exit vs verdict:** preserve raw child exit facts separately from the user-facing verdict and safety/cleanup gates. However, the existing proposed semantic decision says a trusted, non-contradictory nonzero child exit remains a user-facing FAIL even if cleanup is UNKNOWN/FAILED; cleanup uncertainty is independently visible and artifacts remain blocked. A confirmed zero exit cannot become PASS when a mandatory case-specific evidence/safety gate is unsatisfied. A stream collection failure is not universally fatal if that stream is optional for the case. Do not make all collector disruptions automatically `INCOMPLETE`.
2. **Policy barrier:** exact applied policy before dispatch is a serious remote/hosted boundary requirement already present in the proposed adapter design. ETag is one possible revision-binding mechanism, not a universal mandated implementation. The real requirement is an authoritative revision match bound to dispatch so a read-then-dispatch race cannot change policy between check and execution. This requirement is path-dependent; do not impose a provider policy ETag on local browser execution as though it were the same boundary.
3. **Acceptance counts:** Gemini's statement about reconciling "all 14 supplementary acceptance scenarios" is not traceable to named pinned sources or exact IDs. Canonical acceptance remains LOOP-01..14 and CASE-01..16; supplementary design IDs live in their own source documents. Never merge counts or remap IDs without a pinned crosswalk.
4. **Artifact release:** current proposed design already requires rechecking authorization, safe normalized path/name, media type if policy-selected, size/count, final stored-byte integrity and job/attempt/tenant association at the actual release boundary. Historical execution PASS is not sufficient. Secret scanning/redaction may be an additional policy gate if selected, but it is not a chosen or verified universal mechanism. Do not claim it is mandatory or implemented.

These corrections preserve the existing proposed [execution contract](../PRODUCT/EXECUTION_CONTRACT.md), [execution-loop acceptance](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md), and [adapter result envelope](ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md). Gemini's report does not authorize a new result schema or acceptance IDs.

## 5. Licensing and evidence quality

Gemini lists several licences, but does not provide pinned commit SHAs, full dependency/asset/model licence inventories, copyright/notice obligations, or exact source files for many recommendations. The report's final numbered source list does not support the broad [1]...[5] references throughout the text; repeated "uploaded master implementation plan" references are not public-source citations and are not independently available to this review.

Before any code reuse, require:
- exact upstream repository and immutable commit SHA/tag;
- current licence file and SPDX identifiers for the chosen files;
- dependency, generated-code, asset, font, model and binary licence inventory as applicable;
- exact files/modules/functions and a bounded proposed reuse surface;
- platform/runtime support and transitive native dependencies;
- upstream maintenance/release/security posture;
- tests actually inspected and independently run only if later authorized;
- threat model, trust boundaries, limitations, and required wrapper/adaptation;
- attribution/notice and modification obligations;
- replacement/exit strategy if upstream is abandoned.

A GitHub repository being public is not sufficient permission to reuse its code.

## 6. Administrative decisions

These decisions govern planning until explicitly revised:

1. **No architecture convergence decision.** PocketCode and RevDev remain distinct systems with distinct runtime/security/acceptance boundaries. Shared envelope/protocol compatibility remains a future possibility, not an implementation instruction.
2. **No LangGraph adoption for MVP.** Revisit only if a validated product requirement demonstrates multi-step durable agent orchestration that a smaller state machine cannot satisfy.
3. **No hosted Piston dependency.** Public API access is no longer generally free; self-hosting is a separate operational/security project.
4. **No tsnet/AsyncSSH integration approval.** Remote-PC path must first prove user value and then justify a transport design that fits RevDev's actual stack.
5. **No Watchdog/FlaUI dependency addition.** Require a demonstrated gap in RevDev before considering either.
6. **No wasmsh shell feature in MVP.** Keep it as a promising research candidate; the first proof is bounded Python/file workflow, not a general shell.
7. **CodeMirror 6 and Pyodide remain leading candidates, not selected technologies.** The fixed-task comparison and mobile-device behavior decide whether they fit.
8. **Aider repo-map remains a low-cost pattern candidate.** Do not import all of Aider or couple the product to a particular model/provider.
9. **OpenHands ACI is rejected as a direct reuse target because it is archived.** Current Agent SDK may be re-evaluated separately.
10. **Judge0 is not rejected solely for GPL.** If reconsidered, perform a proper component/distribution licence review and operational fit review.
11. **No new canonical LOOP/CASE IDs, result-envelope fields, or public API fields are created by this review.**
12. **No implementation, tests, accounts, provider workloads, spending, PR edits, Actions, merge or deployment are authorized.** $0 budget remains; PC/source/runtime/queue state remains UNKNOWN while PC access is unavailable.

## 7. Updated priority queue

1. Await Claude's independent review of Gemini's candidate list and this review's disputed claims. Reconcile disagreements against exact upstream source.
2. Continue the existing fixed-task comparison design. Do not start a real run until the approved path, device, test inputs, evidence capture and $0 conditions are explicit.
3. Deep-inspect only the most plausible candidates: CodeMirror 6, Pyodide, wasmsh and Aider repo-map. For each, obtain pinned source revision, exact modules, dependency/licence details, and limitations.
4. Keep Tailscale remote-PC, Piston/self-hosting, LangGraph, FlaUI, Watchdog and OpenHands SDK as conditional follow-up candidates tied to demonstrated requirements.
5. When Claude's report arrives, create a single reconciled candidate register with statuses: ADOPT PATTERN, SPIKE LATER, REFERENCE ONLY, DEFER, REJECT, and UNKNOWN. Do not copy code until that register and a narrow integration boundary are approved.

## 8. Primary sources checked for this review

- [CodeMirror input handling source](https://github.com/codemirror/view/blob/main/src/input.ts)
- [Pyodide browser usage](https://pyodide.org/en/stable/usage/index.html)
- [Pyodide FAQ: local files and browser restrictions](https://pyodide.org/en/stable/usage/faq.html)
- [Pyodide filesystem documentation](https://pyodide.org/en/stable/usage/file-system.html)
- [wasmsh upstream repository and README](https://github.com/mayflower/wasmsh)
- [Tailscale tsnet documentation](https://tailscale.com/docs/features/tsnet)
- [Tailscale tsnet Go package](https://pkg.go.dev/tailscale.com/tsnet)
- [Aider repository map documentation](https://aider.chat/docs/repomap.html)
- [LangGraph persistence documentation](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Piston upstream README, public API and security defaults](https://github.com/engineer-man/piston)
- [OpenHands ACI archived repository and migration notice](https://github.com/OpenHands/openhands-aci)
- [FlaUI upstream README](https://github.com/FlaUI/FlaUI)
- [Watchdog supported platforms and caveats](https://python-watchdog.readthedocs.io/en/stable/installation.html)
- [GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)

**Review limitation:** This review checked project documentation/source entry points, not every line of each candidate repository. No candidate was built, installed, benchmarked, executed or penetration-tested. The source list above is not a substitute for pinned revision and dependency/licence review before adoption.


## 9. Follow-up source-level candidate audit — 2026-11-01

A pinned source-level triage of the four most plausible candidates is now recorded in [OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md](OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md), commit `49a288bb52a0b234c30713f980d63a3c1bf84586`.

This follow-up found an important CodeMirror source-location issue: Gemini's `github.com/codemirror/CodeMirror` link resolves to the legacy CodeMirror 5 repository. The old CodeMirror 6 GitHub package repositories were archived on 2026-04-15 because development moved to `code.haverbeke.berlin`; the old `codemirror/view` GitHub commit `fbff59ba004d80d8c914f64c42586387b08706ac` is only a forwarding commit, not the current source pin. This is **not** evidence of abandonment: npm currently lists `@codemirror/view@6.43.15` under MIT, with recent publication and current 6.43.x mobile fixes. The Forgejo source host returned 403 in this review environment, so current upstream source commit remains NOT VERIFIED. Pin the published package version/integrity until the active source can be fetched.

The deeper review also confirms:
- Pyodide's default MEMFS is ephemeral; IDBFS persistence requires explicit synchronization; native directory mounting is experimental and Chromium-only; browser Python lacks normal `threading`, `multiprocessing` and `subprocess` process creation.
- wasmsh is a constrained shell interpreter, not a general OS shell: no host filesystem, no arbitrary `fork/exec`, no job control; background syntax parses but browser execution is synchronous. Its step/output/pipe/recursion limits use zero for unlimited. The threat model itself warns of embedder OOM and network side-channel risk when hosts are allowlisted.
- Aider's `repomap.py` is coupled to Aider-specific model/I/O/cache modules and several dependencies, so the map concept is more reusable than the module itself.

No candidate was built, installed, benchmarked, executed or adopted. Exact repository commit and source blob pins, open questions and narrow reuse directions are in the deep-dive document.
