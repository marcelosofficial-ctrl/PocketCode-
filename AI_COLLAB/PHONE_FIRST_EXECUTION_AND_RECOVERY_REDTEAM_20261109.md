# Phone-first execution and recovery: deep research and red-team correction

**Date:** 2026-11-09  
**Status:** Research and contract refinement only. NOT IMPLEMENTED / NOT DEVICE-TESTED.  
**Scope:** No-spend GitHub Pages PWA, browser-local execution, local persistence, task recovery and evidence claims.  
**Authority:** Does not change D-001..D-006, select a runtime/database/host/provider, authorize source/test edits, or change canonical LOOP/CASE/D IDs.

## 1. Ranked gaps

| Rank | Gap | Why it is high value | Disposition |
|---|---|---|---|
| 1 | GitHub Pages origin and response-header boundary | A path-based deployment may share storage with every same-host project page; the approved host cannot currently set arbitrary response headers | Corrected threat model and deployment checks |
| 2 | Hostile-code execution vs app/worker isolation | The app must not advertise a worker or WebAssembly runtime as a separate hostile-code sandbox | Defined honest execution modes and browser-isolation experiment boundary |
| 3 | IndexedDB/OPFS crash consistency | Metadata and bytes have separate commit domains; false “saved” or “complete” states can corrupt receipts | Added precise two-phase artifact publication and crash matrix |
| 4 | P39 lifecycle and client receipt | Revocation, termination, server emission and client receipt are distinct facts; model tests do not prove transport behavior | Reaffirmed owner gate and added adapter acceptance |

## 2. Topic 1: GitHub Pages origin isolation and header limits

### 2.1 Verified platform facts

- **VERIFIED:** GitHub Pages project sites default to https://<owner>.github.io/<repository>; user/organization sites use https://<owner>.github.io. GitHub also supports custom domains. [GitHub Pages site types](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
- **VERIFIED:** A browser origin is scheme + host + port. Different paths on the same host remain same-origin. [MDN same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy).
- **VERIFIED:** IndexedDB databases are associated with an origin, not a repository path. [MDN IndexedDB terminology](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology). OPFS is also origin-private storage. [MDN File System API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API).
- **VERIFIED:** GitHub Pages can apply a user/organization custom domain to project sites by default unless an individual project overrides it. The actual host cannot be inferred from the repo name or default URL alone. [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages).
- **VERIFIED with date qualification:** A GitHub staff response in the official Pages discussion says custom HTTP headers were not supported and a meta tag was the available route (2023-05-02). The discussion still contains feature requests in September 2026; the current GitHub Pages documentation opened for this pass describes static publishing and custom domains but no configurable response-header feature. This is strong evidence of a limitation, not a direct read of PocketCode's deployed response headers. [GitHub Pages custom-header discussion](https://github.com/orgs/community/discussions/54257).
- **VERIFIED:** CSP's sandbox directive is ignored when delivered in a meta element. It cannot replace an iframe's own sandbox attribute. [W3C CSP Level 3](https://www.w3.org/TR/CSP/) and [MDN CSP sandbox](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/sandbox).
- **VERIFIED:** WebKit storage quota and eviction are origin-scoped. Eviction can occur under overall quota pressure, device storage pressure and inactivity; default best-effort storage is evictable. A Home Screen web app's ITP exemption is not an exemption from these general storage failure modes. [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/).

### 2.2 Consequence for PocketCode

If the app is actually served from https://marcelosofficial-ctrl.github.io/PocketCode-/, any other content served from a different path on that exact host has the same origin. A script executing there can attempt to access the same IndexedDB and OPFS storage. Separate repositories, path prefixes, database names and service-worker scopes do not create a browser-origin boundary.

This is a conditional deployment risk, not an observed exploit. It requires same-origin script execution, for example a compromised sibling project, injected content or compromised dependency. It does not mean an arbitrary unrelated GitHub user can read this origin's data.

**UNKNOWN:** PocketCode's actual Pages URL, Pages enabled state, custom-domain override, sibling project inventory, live CSP/response headers and service-worker scope. The Pages settings endpoint was not accessible through the connected GitHub actions in this pass, and public search did not verify a live PocketCode URL. No URL is inferred as fact.

### 2.3 Corrective deployment policy

1. Before storing user work, record the actual published URL and compute its origin tuple. Inspect repository Pages settings and any root/user-site custom domain configuration.
2. Inventory all independently maintained pages under the same exact host. Treat every same-origin script as part of the app's trusted computing base.
3. If D-006 keeps the shared GitHub Pages origin, explicitly accept the shared-origin trust boundary. Do not store reusable provider credentials, GitHub tokens, passwords, signing keys or long-lived bearer tokens in browser storage.
4. Do not claim a CSP response header, frame-ancestors, X-Frame-Options, Permissions-Policy or CSP sandbox directive is configured unless the live response proves it. GitHub Pages' meta CSP is only a partial mitigation; meta CSP cannot express all header-only controls.
5. A different path, service-worker scope or random database name is not a mitigation for same-origin script access. A genuinely different hostname is a different origin, but obtaining/operating one must respect D-006 and requires owner approval if it changes hosting.
6. Do not migrate hosting, buy a domain, add a proxy/CDN or use a paid service as an unapproved fix.

### 2.4 Origin acceptance tests

These are proposed research IDs, not canonical LOOP/CASE/D IDs.

| ID | Setup | Required result |
|---|---|---|
| ORIGIN-01 | Read actual Pages settings and live URL | Record enabled state, exact URL, scheme/host/port, project/user/custom-domain type |
| ORIGIN-02 | Inventory same-host Pages paths under the owner | Classify each as owner-controlled/trusted or separately maintained/untrusted |
| ORIGIN-03 | Use synthetic data in a controlled sibling path on the same host | Demonstrate same-origin IndexedDB access; never use production user data |
| ORIGIN-04 | Repeat with OPFS test directory | Record actual browser behavior; do not infer path isolation |
| ORIGIN-05 | Inspect worker scope and storage key | Confirm scope is path control, not storage isolation |
| ORIGIN-06 | Fetch actual deployed response headers and HTML meta policies | Record what is truly enforced; mark absent headers as absent |
| ORIGIN-07 | Inject a controlled script into a test build | Verify CSP/dependency controls and record what meta CSP cannot enforce |
| ORIGIN-08 | Test quota pressure and origin eviction with synthetic data | No false saved/backup claim; recovery and export path remains explicit |

## 3. Topic 2: execution boundary, Pyodide and browser sandboxing

### 3.1 Verified findings and competitor patterns

- **VERIFIED:** WebAssembly modules execute in a sandboxed environment, but the embedding environment defines the APIs and capabilities imported by the module. [WebAssembly security model](https://webassembly.org/docs/security/).
- **VERIFIED:** Pyodide's runPython evaluates code and returns values across a JavaScript integration boundary. Its API supports Python/JavaScript objects and proxy/module registration. Every JS object, proxy, callback, filesystem shim, fetch bridge or native bridge exposed by the app is part of the guest's effective authority. [Pyodide JS API](https://pyodide.org/en/stable/usage/api/js-api.html).
- **VERIFIED:** Pyodide in a Web Worker runs in a separate global context and improves UI responsiveness. That is not process-level containment or a guarantee of CPU/memory quotas. [Pyodide worker guide](https://pyodide.org/en/stable/usage/webworker.html).
- **VERIFIED:** Deno documents that code on the same thread shares the same privilege level, that allow-run can invalidate the permission sandbox, and that untrusted code should use multiple layers including OS controls or VM/microVM isolation. [Deno security guidance](https://docs.deno.com/runtime/fundamentals/security/).
- **VERIFIED:** OpenHands documents Docker as its recommended local sandbox provider for agent execution. This is a host/container deployment pattern, not a no-host browser feature. [OpenHands Docker sandbox](https://github.com/OpenHands/docs/blob/main/openhands/usage/sandboxes/docker.mdx).
- **VERIFIED:** Wasmtime can enforce guest linear-memory/table/instance limits and fuel/epoch interruption, but its ResourceLimiter does not account for all host-side allocations. Existing project research records Wasmtime 50.0.1 and Apache-2.0 / LLVM-exception licensing metadata; no dependency is selected here.

### 3.2 Honest product execution modes

| Mode | Allowed behavior | Claims prohibited |
|---|---|---|
| Local bounded task | User explicitly selects/imports code and inputs; run a supported light task with no secrets, no privileged app bridge, bounded input/output, visible resource caveats and recoverable attempt identity | Hostile-code sandbox, hard CPU/memory quota, guaranteed background completion, OS process isolation |
| Browser-isolated experiment | Test a sandboxed iframe with sandbox="allow-scripts" and deliberately omit allow-same-origin; communicate only through a narrow versioned postMessage protocol; synthetic data only | Production security certification, complete network/CPU/memory containment, immunity to browser/engine vulnerabilities |
| Untrusted/public execution | Disabled until a separately isolated disposable runner proves OS/process-level CPU, memory, wall-time, process, disk, output, egress, credential, teardown and per-user controls | Any production availability or safety claim before the boundary is independently tested |

A sandboxed iframe without allow-same-origin is assigned an opaque origin and cannot use the app origin's storage. The iframe must not receive parent DOM references, application objects, credentials, project APIs or broad callbacks. The parent validates message schema, message size, attempt identity and allowed message types. Do not combine allow-scripts and allow-same-origin for same-origin content: MDN warns that the embedded document can remove its sandbox attribute. [MDN iframe sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe).

**Important limits:** an iframe sandbox is a browser isolation layer, not a separate OS process guarantee. It does not establish strict CPU or memory ceilings, and navigation/exfiltration, browser bugs, denial of service and implementation-specific behavior still need testing. CSP meta policies can restrict some resource classes, but CSP sandbox is not valid in a meta element. A sandboxed iframe is an experiment to reduce ambient access, not a substitute for the separate disposable execution boundary required by SECURITY.md.

### 3.3 Concrete local execution contract

Before a local task starts:
- Persist CommandId, DispatchAttemptId, input manifest digest, execution mode, runtime identity, requested limits and explicit user action.
- Create a fresh worker/iframe context per attempt where supported. Do not reuse a privileged long-lived JS context for unrelated user programs.
- Give the guest only serialized input bytes and a small message protocol. Never pass app objects, DOM nodes, IndexedDB handles, credentials, signing keys, fetch wrappers or project mutation callbacks.
- Default network access to unavailable. Do not silently enable package installation or arbitrary network access.
- Bound source/input bytes, stdout/stderr bytes, result bytes and wall-clock observation. Treat browser-enforced limits as best-effort unless the engine provides and tests a hard bound.
- Terminate the worker/frame on user cancellation or observed timeout, but record termination_requested separately from termination_confirmed. If the host cannot confirm termination, status remains UNKNOWN/INCOMPLETE.
- Sanitize terminal output before rendering; never interpret guest output as HTML.
- Do not start code in a service worker or unattended background event.
- Keep secrets outside the guest. Same-origin local persistence is not a secret vault.

### 3.4 Reuse decision

Deno's model is useful for default-deny permissions and narrowly scoped host capabilities, but its own docs say same-thread modules share privileges and recommend OS/VM layers for arbitrary untrusted code. OpenHands' Docker sandbox demonstrates a separate execution environment with host mounts and runtime configuration. It is not directly reusable as a $0 phone-only PWA execution host. Wasmtime demonstrates guest-level fuel, memory and capability controls, but host allocations and deployment isolation remain separate.

No code was copied and no new dependency was added. Existing project rules already reject wildcard auto-approval and stock Pyodide as a hostile-code sandbox. No license obligations were introduced.

### 3.5 Execution boundary acceptance tests

Proposed IDs only.

| ID | Adversarial case | Required result |
|---|---|---|
| EXEC-01 | Guest enumerates JS globals and attempts to access app bridge | No privileged app object or secret is reachable |
| EXEC-02 | Guest attempts IndexedDB/OPFS access from sandboxed iframe | Opaque origin cannot read/write app-origin storage |
| EXEC-03 | Guest attempts fetch, WebSocket, image, form, popup and top navigation | Each capability is denied or explicitly observed and recorded; no silent egress |
| EXEC-04 | Guest sends forged, oversized, reordered and cross-attempt postMessage | Parent rejects it without state mutation |
| EXEC-05 | Infinite loop / memory growth | UI remains responsive where worker isolation works; termination/resource behavior recorded without claiming hard quota |
| EXEC-06 | User requests cancel during computation | Record request, host action, termination acknowledgement and final evidence separately |
| EXEC-07 | Worker or iframe crashes/disappears | Attempt remains unresolved until trusted terminal evidence; no inferred PASS/FAIL |
| EXEC-08 | Guest emits HTML/script/terminal escape sequences | Rendered output remains inert and bounded |
| EXEC-09 | App attempts to start public/untrusted execution without external runner | Reject as unsupported; do not downgrade to local Pyodide |
| EXEC-10 | Runtime package/version changes | Record exact runtime build, package set and capability manifest in receipt |

## 4. Topic 3: local persistence and crash-consistent artifact publication

### 4.1 Platform facts

- **VERIFIED:** IndexedDB transactions provide atomic commit/abort over the stores in their transaction scope. A successful transaction fires complete after database changes have been written. A failed commit aborts and rolls back its transaction. [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/).
- **VERIFIED:** IndexedDB 3.0 remains a W3C Working Draft in the latest published snapshot opened for this pass (2026-10-30), not a final Recommendation. Its strict durability is a hint; the spec describes a typical implementation flushing OS buffers before complete. It is not a universal device-loss/eviction/backup guarantee.
- **VERIFIED:** OPFS sync access handle flush attempts to transfer cached file modifications to the underlying storage device. The spec notes this can be a no-op on some filesystems, such as in-memory filesystems. close releases the file lock; it does not itself guarantee immediate persistence. [WHATWG File System Standard](https://fs.spec.whatwg.org/).
- **VERIFIED:** WebKit can evict origin data under quota pressure and storage pressure; persist() is heuristic and quota estimates are not guarantees. [WebKit Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/).
- **VERIFIED:** Service workers are event-lifetime-bound and may be terminated by the user agent when idle or when abnormal/overlong work occurs. [W3C Service Workers CRD 2026-10-29](https://www.w3.org/TR/2026/CRD-service-workers-20261029/).

### 4.2 Required two-domain artifact protocol

IndexedDB and OPFS do not share one atomic transaction. Use a staged protocol; do not claim cross-API atomicity.

1. **Reserve:** In one short IndexedDB read-write transaction, create ArtifactId, immutable attempt binding, unique staging key, expected size/digest policy, current fence generation and staging status. Commit and await transaction complete.
2. **Write:** Write bytes only to the unique staging key for that attempt and fence generation. Never write directly to a final published path. Handle quota, I/O and cancellation errors.
3. **Flush request:** Call OPFS flush where supported. Record that the flush operation returned. Do not describe this alone as power-loss-proof durability.
4. **Readback:** Reopen/read the staged file; recompute exact byte length and digest from the bytes read back. Producer-supplied digest is only a claim.
5. **Publish metadata:** In one short IndexedDB transaction, re-read the current fence and attempt state; reject stale writers; verify the artifact is still authorized for this attempt; append the artifact-verified observation; create immutable manifest/receipt revision; and update publication/outbox reference. Await transaction complete.
6. **Use/release:** Before copy/share/download, verify that the manifest still references the exact artifact version and latest authorized receipt revision. Recheck byte length/digest. If verification fails, quarantine and create a successor receipt; never rewrite a historical receipt.
7. **Recover:** On launch, reconcile staging records, orphan files, manifest references and missing/corrupt bytes. Never auto-dispatch an ambiguous prior execution.

The fence protects the metadata publication boundary. It does not stop a stale worker from writing its own staging object. Unique, never-reused staging keys prevent stale writes from corrupting the current artifact; only a current-fence IndexedDB transaction can publish a reference.

### 4.3 Crash matrix

| Crash point | Possible durable state | Recovery action |
|---|---|---|
| Before reservation commit | No reservation | No artifact exists; safe to retry reservation |
| After reservation, before bytes | Staging record, no file | Mark abandoned; no manifest/release |
| During file write | Partial staging file | Quarantine/delete after inspection; never publish |
| After write, before flush | File may be incomplete at storage boundary | Reopen/readback; if absent or mismatch, quarantine |
| After flush, before readback | Staging file may exist; no verified manifest | Read back exact bytes and recompute digest |
| After readback, before metadata transaction | Verified orphan stage, no manifest | Re-read; re-check fence/authorization; then publish or quarantine |
| During metadata transaction | Transaction either commits all scoped metadata or aborts all | Read database state; do not infer from request success callbacks |
| After metadata commit | Manifest references exact staged object | Verify object on recovery/use; missing or changed bytes quarantine with successor receipt |
| After receipt commit, before report copy | Receipt exists, copy may not | Retry publication of same receipt; never rerun task |
| Stale writer resumes after takeover | Old staging key may be written | Current fence rejects metadata publication; old key remains orphan only |

### 4.4 Local recovery state rules

- A committed running attempt without a trusted terminal observation becomes interrupted/unknown/incomplete on next foreground launch.
- App suspension, browser closure, worker disappearance, lost connection and a timeout in the UI are not proof of program termination.
- A user retry is a new DispatchAttemptId unless exact-effect reconciliation proves the prior effect did not happen or a downstream idempotency contract guarantees deduplication.
- A report/copy failure retries the same immutable receipt publication, not execution.
- If IDB metadata is missing, corrupt or references missing OPFS bytes, show recovery-required. Do not silently show an empty workspace as a successful clean state.
- Provide explicit export/import and verify archive paths, manifest, byte lengths, digests, schema version, attempt identity and receipt links before accepting a restore.
- Storage API persistent mode is eviction protection, not backup. Manual clearing, device loss, corruption and app deletion remain outside the guarantee.

### 4.5 Additional PWA acceptance tests

These extend the existing PWA-STOR/PWA-LIFE/ORIGIN matrix as proposed IDs only.

| ID | Scenario | Required result |
|---|---|---|
| PWA-ART-01 | Crash after reservation but before file write | Staging record recovered; no artifact manifest |
| PWA-ART-02 | Crash during OPFS write | Partial object quarantined; no release |
| PWA-ART-03 | Crash after flush but before readback | Readback and digest recomputed before publication |
| PWA-ART-04 | Crash after readback but before IndexedDB manifest commit | Orphan is revalidated; current fence required to publish |
| PWA-ART-05 | Crash during manifest/receipt transaction | All scoped metadata commits or none; inspect transaction state |
| PWA-ART-06 | Stale worker writes after newer fence | Old staging key cannot publish or overwrite current manifest |
| PWA-ART-07 | Manifest references missing or mutated OPFS bytes | Quarantine and successor receipt; no silent repair |
| PWA-ART-08 | Copy/share interrupted after receipt commit | Retry same receipt publication; no execution rerun |
| PWA-ART-09 | Restore archive contains traversal paths, duplicate IDs or digest mismatch | Reject/quarantine before importing records |
| PWA-ART-10 | Origin storage eviction or manual clearing | Clear recovery warning; do not claim cloud backup or success |

## 5. Topic 4: P39 lifecycle, revocation and client receipt

The existing OD-01..OD-13 register remains the authority for owner choices. This research does not close any decision.

| Evidence layer | What it proves | What it does not prove |
|---|---|---|
| Authorization checked | A principal was authorized at a specific decision point | Authorization remains valid after revocation |
| Dispatch accepted | Provider/adapter accepted a request | Program started or completed |
| Server emitted bytes | Server handed bytes to transport | Client received or persisted them |
| Client observed bytes | Client reports observing a byte count/digest | Client durably stored the bytes unless protocol says so |
| Client acknowledged receipt | Client acknowledged exact transfer identity and digest | Artifact is safe or authorized for later reuse |
| Cancellation requested | Control plane requested cancellation | Worker/stream actually stopped |
| Termination confirmed | Trusted supervisor confirms execution stopped | Cleanup completed |
| Cleanup confirmed | Required resources were released/isolated | Artifact is safe to release |
| Artifact verified | Exact bytes match expected size/digest | Producer is authentic or execution was correct |

Required rule: retain distinct transfer identity, emitted/observed/acknowledged byte counts, cancellation request, termination acknowledgement and cleanup evidence. Reauthorization after takeover/revocation must bind the latest receipt revision and exact object version. A stale grant/receipt may remain a valid historical record but must not authorize new bytes.

**Owner gate:** OD-01..OD-13 remain OPEN. P39/P40 implementation remains CLOSED. CASE-04 remains INCOMPLETE / timed_out. No source/test edits are authorized by this document.

## 6. Red-team corrections to earlier work

1. **Origin mitigation overstated:** the previous origin note said to apply restrictive CSP/response headers “where GitHub Pages configuration permits.” That wording implied response-header control might be available in the approved static host. GitHub's own Pages discussion records staff saying custom headers were unsupported; meta CSP is partial, and CSP sandbox is ignored in meta. **Correction:** verify live headers, never claim server-header protections on Pages, and do not use meta CSP as an iframe sandbox.
2. **OPFS durability overstated:** the prior note said flush “persists writes.” The WHATWG algorithm only attempts to transfer cached modifications and explicitly permits a no-op on some filesystems. **Correction:** record successful flush invocation, independently read back bytes, and avoid a power-loss guarantee.
3. **WASM/worker language was too easy to overread:** saying “worker sandbox” can imply containment. Pyodide's official worker guide describes a separate thread/global context for responsiveness. **Correction:** worker is a responsiveness and termination primitive; capabilities, origin, host bridge, resource ceilings and process isolation remain separate.
4. **IndexedDB standard status needed refreshing:** earlier material cited the 2025 Working Draft. The latest published snapshot opened here is 2026-10-30 and remains a Working Draft. **Correction:** update reference date/status; atomic transaction guarantees are within IDB's own transaction scope only.
5. **The live Pages risk was never confirmed:** project URL and custom domain were UNKNOWN, and custom-domain inheritance can alter the hostname. **Correction:** keep the risk conditional and require actual Pages settings/live URL before asserting PocketCode is exposed to sibling content.
6. **Service-worker recovery must not imply background execution:** a service worker may be terminated by the user agent. **Correction:** execution completion is foreground/runner-owned; background events are optional wake-up triggers only.
7. **OpenHands licence was misstated in an earlier summary:** its core repository LICENSE is MIT, not Apache-2.0. The Docker sandbox documentation is a pattern reference; no code was copied. Verify enterprise and separately packaged component terms before any future reuse.

## 7. Source quality, maintenance and licence notes

| Source | Opened/version/date evidence | Licence or reuse status | Use |
|---|---|---|---|
| GitHub Pages documentation | Current docs opened 2026-11-09 | Documentation only; no code copied | URL/site types/custom domains |
| GitHub Pages header discussion | GitHub staff response 2023-05-02; thread has 2026 activity | Discussion, not formal product contract | Header limitation qualified by date |
| MDN same-origin/iframe/IndexedDB | Current pages opened 2026-11-09 | Documentation only | Origin, storage and iframe semantics |
| WebKit storage policy | 2023-08-10 primary WebKit article, still linked by MDN | Documentation only | Quota/eviction/persist caveats |
| W3C IndexedDB 3.0 | Latest opened snapshot 2026-10-30, Working Draft | W3C document terms; no code copied | Atomic transaction and durability hints |
| WHATWG File System | Living Standard updated 2026-10-19 | Standard; no code copied | OPFS flush/close semantics |
| W3C Service Workers | Candidate Recommendation Draft 2026-10-29 | Draft; no code copied | Worker termination |
| Pyodide | Stable API docs opened for API semantics | Upstream MPL-2.0, no code copied | JS bridge and worker distinction |
| Deno | Security docs opened 2026-11-09 | MIT, no code copied | Default-deny and layered isolation pattern |
| OpenHands | Docker sandbox docs opened 2026-11-09; core LICENSE opened 2026-11-09 | MIT for core repository; verify enterprise/component-specific terms separately; no code copied | Separate host/container sandbox pattern |
| WebAssembly | Official security overview opened 2026-11-09 | Standard/documentation; no code copied | Engine vs embedder capabilities |

No source code was copied, no dependency was added, and no runtime, database, hosting provider or architecture was selected.

## 8. Verification boundary

- **VERIFIED:** GitHub Pages default project URL pattern; origin tuple excludes path; IndexedDB/OPFS are origin-scoped; GitHub Pages header limitation is supported by an official staff response and current docs lack a header configuration feature; CSP sandbox is not supported in meta; IndexedDB transaction atomicity/durability-hint semantics; OPFS flush semantics; service-worker termination; Pyodide worker purpose; Deno layered isolation guidance.
- **INFERRED:** a PocketCode Pages project on the same exact hostname as another project shares browser storage origin with that project.
- **UNKNOWN:** actual Pages deployment URL/settings, custom domain, same-host sibling inventory, live response headers, browser/device-specific iframe/worker behavior and app bridge surface.
- **NOT RUN:** sibling-origin test, iframe isolation test, egress test, iOS/Android worker/iframe stress test, crash/power-loss tests, export/restore tests, real durable-adapter concurrency tests.
- No source/tests, canonical IDs, owner decisions, PRs, hosting settings, runtime/provider/database choices or spending changed.
