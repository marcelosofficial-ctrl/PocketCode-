# Full-power gap research and red-team pass — 2026-11-12

**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Baseline HEAD:** `6b28b5afd59e404b8d2bda9d7cf4a99001a6cd34`  
**Status:** research/design deliverable; no application implementation or canonical acceptance change  
**Scope:** PocketCode only. Preserve D-005/D-006 ($0), OD-01..OD-13, LOOP-01..14, CASE-01..16 and all D-IDs.

## 1. Ranked gaps

| Rank | Gap | Why it is high value |
|---|---|---|
| 1 | Untrusted execution isolation and Pyodide bridge boundary | A same-origin Pyodide worker can inherit application browser authority; a 2026 high-severity advisory demonstrates the exact failure mode. |
| 2 | Grant aggregate/event/outbox consistency and relay fencing | The pinned model permits aggregate-version advancement without a matching event and has no grant-event relay lease/fence. |
| 3 | Browser-origin trust and durable local artifacts | PocketCode and portfolio Pages URLs share one origin; browser storage is best-effort and Safari can proactively evict inactive-origin data. |
| 4 | Typed execution, termination and client-receipt evidence | Existing receipt/projection code is in-memory/pure; it cannot prove worker termination, cleanup, browser persistence or client receipt. |
| 5 | Exact-SHA P40 execution and evidence closure | Owner approved a read-only model run, but the runner route was blocked; historical CI cannot substitute for current results. |

## 2. Research and finished design deliverables

Research performed 2026-11-12 using opened official specifications, maintained project documentation, project advisories and upstream repositories. No source code was copied.

### 2.1 Untrusted execution: Pyodide is a runtime, not an origin boundary

**VERIFIED:** Pyodide is a browser/Node Python distribution based on WebAssembly with a JavaScript↔Python FFI. Its upstream repository identifies MPL-2.0 licensing and remains active; current docs surfaced 314.1.0.dev0. Runtime capability does not establish an isolation boundary.

**VERIFIED:** GitHub-reviewed GHSA-4r2p-27mh-5m22 / CVE-2026-59214 describes Open WebUI versions below 0.10.0. A same-origin Pyodide worker exposed `pyfetch` and the `js` bridge; code run by a user could make authenticated same-origin requests with the victim's session. The advisory rates it High, CVSS 7.3, published 2026-06-29 and updated 2026-07-24. Open WebUI 0.10.0's fix runs Pyodide in a sandboxed iframe with `sandbox="allow-scripts"` and without `allow-same-origin`, creating an opaque origin. The sandbox cannot access the parent DOM, cookies, tokens or localStorage through that bridge.

**VERIFIED:** Open WebUI follow-up discussion documents the trade-off: opaque-origin execution changes network reach, and opting into persistent storage restores the same-origin worker risk. Current Open WebUI docs describe Pyodide as suitable for basic analysis and point to Open Terminal for heavier work; a project discussion calls Pyodide legacy. This is competitor evidence, not a PocketCode stack recommendation.

**VERIFIED:** OWASP says workers can make in-domain/CORS requests, consume excessive CPU, and must not be created from user-supplied worker scripts. It recommends validating worker messages. OWASP's sandboxed-frame guidance supports unique-origin isolation for untrusted content. MDN documents worker message serialization and separate global contexts.

**PocketCode design contract (proposed, not implemented):**
1. Treat imported/user-supplied code as untrusted, including Python and WASM.
2. Never execute it in the application page's origin with ambient credentials, DOM, local storage, IndexedDB, service-worker control or authenticated API access.
3. If browser execution is retained, isolate it behind a distinct opaque-origin sandbox. The Open WebUI pattern is a reference, not code to copy. Keep network disabled by default; do not grant `allow-same-origin`.
4. Use a narrow, versioned parent↔sandbox message protocol. Validate exact message type, schema, size, attempt ID, sequence and allowed operation. Treat every message as hostile data. Never eval message content, pass arbitrary JS snippets or expose a generic fetch/API bridge.
5. Transfer input files as bounded explicit copies after user import. Return output only as staged bytes with size limit, digest, attempt binding and parent-side validation. The sandbox cannot write directly into privileged app storage.
6. Separate origin isolation from CPU/memory containment. A browser sandbox does not establish hard resource quotas or guarantee a hostile task can be interrupted. If those are required, report browser-only execution as insufficient until a separately constrained environment is approved.
7. Preserve OD-01: no live/incremental artifact streaming in MVP. Fully stage, hash and authorize before bounded download/share.

**Trade-off:** opaque-origin execution deliberately makes same-origin persistence and authenticated requests unavailable. Do not quietly re-enable a same-origin worker to regain persistence. Persistence must be a separate parent-owned capability with explicit file transfer and integrity checks. This aligns with user-controlled context and no clipboard polling.

**Reuse/licensing:** Pyodide is MPL-2.0. Open WebUI's post-v0.6.5 code has a branding-restricted Open WebUI License; earlier history differs. Cite the advisory/pattern, do not transplant Open WebUI code. OWASP Cheat Sheet Series is CC BY-SA 4.0; attribution/share-alike applies when adapting its text. No code copied.

### 2.2 Grant events: outbox atomicity is not relay fencing or producer authentication

**VERIFIED:** AWS transactional-outbox guidance says business state and its outbox event must commit atomically, consumers must tolerate duplicates, and event order must follow aggregate update order. Debezium's maintained Outbox Event Router uses immutable INSERT-only outbox rows, unique event IDs and aggregate IDs as message keys to preserve per-aggregate ordering. These are established patterns, not a mandate to adopt a database, Kafka or Debezium.

**VERIFIED:** CloudEvents v1.0.2 requires `source`+`id` uniqueness and permits consumers to treat identical pairs as duplicates. It standardizes event context/interoperability; those identity fields do not authenticate a producer or prove payload integrity. Upstream README lists v1.0.2 as latest released core and the next draft as WIP. CloudEvents is a CNCF graduated project; repository license is Apache-2.0.

**VERIFIED:** NATS JetStream documents at-least-once delivery, redelivery when acknowledgement is absent, and explicit acknowledgement semantics. This reinforces idempotent consumers and durable acknowledgement state. It does not solve PocketCode's local relay contract and does not imply NATS is selected.

**Pinned PocketCode source facts (revalidated in the previous source-pinned audit):**
- `ReleaseGrantContractModel.record_progress()` increments `aggregate_version` even when progress is equal, without a matching grant event/outbox record.
- `consume_event()` checks duplicate identity/digest and sequence gaps but does not recompute a first-delivery digest from canonical semantic bytes or verify grant/source/producer authority.
- Grant-event `mark_outbox_delivered()` is an unguarded marker; no grant-event relay claim, lease, fence, ordered cursor or stale-ack rejection exists in the model.
- `FakeOutboxStore` protects effect dispatch only. Its tests do not prove grant-event relay fencing.
- `EventJournal.AuthenticatedProducer` is typed adapter input; the model verifies no key, credential, certificate or signature.

**Next-gate design contract (proposed, not implemented):**
- A committed aggregate transition atomically persists the new aggregate version and exactly one immutable event/outbox record for that version. A semantic no-op does not advance aggregate version or create an event. If no-op audit events are required, define separate event/version semantics rather than accidental increments.
- Minimum envelope: `event_id`, `source`, `event_type`, `schema_version`, `tenant_id`, `grant_id`, `attempt_id`, `aggregate_version`, `object_version`, `policy_epoch`, `fence`, immutable canonical payload bytes and payload digest. Commit/observation time is adapter/coordinator-owned; caller time is metadata only.
- Trusted ingress authenticates producer and binds authority to allowed source, tenant and event type before acceptance. Consumer recomputes digest from exact canonical bytes, validates grant/attempt/tenant and expected predecessor version, then atomically records inbox identity with resulting state change.
- Relay claim, lease expiry, takeover and delivered-marker commit are fenced. A marker is accepted only from the current lease generation for the exact event ID/version. Reject stale acknowledgements. Preserve per-aggregate order; do not mark N+1 delivered while N is unresolved unless an explicit gap/quarantine disposition exists.
- At-least-once publication is acceptable only with immutable event identity, idempotent receiver and durable retry/reconciliation. Never claim exactly-once transport.
- Keep effect-dispatch and grant-event outboxes as separate responsibilities and separate acceptance evidence.

**Reuse decision:** adapt Debezium's immutable outbox row/event ID/aggregate key/order model; adapt AWS atomic-write and duplicate-consumer rules; use CloudEvents only as an interoperability envelope if needed. Do not import broker, CDC connector, schema registry, database or vendor dependency before the stack gate.

### 2.3 Browser origin and durable artifacts: path namespaces do not isolate storage

**VERIFIED:** OWASP says same-origin applications share localStorage, URL path does not isolate keys, IndexedDB is readable/writable by same-origin JavaScript, and stored data must be treated as untrusted. Do not store session identifiers or credentials in localStorage. Service workers have broad request-interception effects and need restricted scope and recovery procedures.

**VERIFIED:** prior Pages audit established PocketCode and portfolio project URLs share scheme, host and port. They are the same browser origin despite different URL paths. This is shared browser authority/storage, not proof portfolio code is malicious or an exploit occurred.

**VERIFIED:** MDN storage guide (last modified 2026-01-05) says browser storage is best-effort by default; `navigator.storage.persist()` may be denied. Safari proactively evicts script-created data for an origin with no user interaction in the last seven days of browser use when tracking-prevention conditions apply. Quotas are browser-specific; `estimate()` is approximate and writes can fail with `QuotaExceededError`. Private browsing may reduce quota or delete storage at session end.

**VERIFIED:** SQLite's official WASM persistence guide is maintained and detailed. OPFS VFS runs in a Worker. The current guide warns standard OPFS VFS is incompatible with Safari versions below 17 due to a sub-worker storage bug; SAH-pool and WASMFS alternatives have different compatibility/concurrency trade-offs. OPFS VFS may require COOP/COEP for SharedArrayBuffer. SAH-pool avoids those headers but does not support multiple simultaneous connections to one database without additional client coordination. SQLite Wasm releases show 3.54.1-build1 on 2026-10-19. The wrapper repo is Apache-2.0; SQLite core code is public domain. Research only, not a selected engine.

**PocketCode storage contract:**
- Until a separate origin is approved and verified, treat PocketCode and portfolio as one trust domain. Do not persist credentials, provider tokens, session identifiers, secrets or security authority in localStorage, IndexedDB, Cache API or OPFS.
- Persist only recoverable, non-secret artifacts and metadata. Treat reads as untrusted; revalidate digest, schema, attempt identity, receipt identity and authorization before display/release.
- Keep a receipt manifest separate from raw bytes: artifact ID, immutable object/version, length, SHA-256, attempt ID, receipt ID/revision, lifecycle disposition, collection state, cleanup state and uncertainty list. Missing artifact or digest mismatch is INCOMPLETE, not empty success.
- Use transactional state transitions for receipt-head CAS and outbox/inbox if a durable store is later selected. Never assume multiple browser stores form one atomic transaction.
- Request persistent storage only after user-visible explanation and record whether granted. Handle quota failure and eviction as recoverable states. A positive `persist()` result is not a backup; user deletion/device loss remain possible.
- Provide explicit export/backup of completed reports/artifacts. A PWA local store alone is not the sole durable copy of important work.
- Do not select SQLite-WASM/OPFS now. First collect iOS Safari and Android target-device evidence for versions, Pages headers, worker topology, storage availability, quota/persist outcomes, multi-tab behavior and restart recovery.

### 2.4 Execution, termination and receipt semantics

**VERIFIED:** `execution_projection.py` calls itself a pure helper and says callers must authenticate producers, authorize attempts, deduplicate events, validate policy and persist observations first. `result_receipts.py` calls itself an in-memory model, not durable storage or a production release service.

**VERIFIED:** OD-09..OD-13 already decide that child execution verdict, overall evidence/job disposition and artifact disposition remain separate; missing policy/egress barriers are INCOMPLETE; termination/cleanup require authoritative acknowledgement bound to the same attempt/execution; client-confirmed receipt requires acknowledgement bound to exact artifact digest/object version/range.

**Three separate projections:**
1. **Execution verdict:** only authenticated direct-child wait or trusted runtime evidence can establish child exit/program failure. Wrapper exit, embedded `SystemExit`, UI toast or bridge label is not child exit.
2. **Evidence/job disposition:** requires lifecycle provenance, required security barriers, collection/integrity and contradiction checks. Missing/unknown required evidence yields INCOMPLETE.
3. **Artifact disposition:** staged, integrity-verified, authorized, quarantined, released, transport-emitted, client-observed and client-acknowledged are distinct states. Do not collapse them into one "done" flag.

A termination request is not an acknowledgement. An untrusted worker's own message that it stopped is not authoritative. Keep CASE-04 INCOMPLETE / timed_out until trusted parent/coordinator same-attempt acknowledgement and canonical acceptance criteria are met. No precedence-only formatter patch.

### 2.5 Exact-SHA P40 execution

**VERIFIED:** target `319cffef121e327331aeaff59522ae279b112ecc` is the P40 pinned target. Ten source/test blob pins were re-fetched and matched in the prior attempt. The active branch is documentation-only ahead; tests must execute at target SHA, not current HEAD.

**VERIFIED:** active-branch workflow supports push on this branch when `scripts/**` or `.github/workflows/pocketcode-python-tests.yml` changes. It checks out triggering SHA by default, uses `ubuntu-latest`, Python 3.12 and full scripts unittest discovery. It does not print Python/SQLite versions. Workflow is absent from default branch `main`, so manual dispatch is unavailable under GitHub's default-branch requirement. Connected GitHub tools expose no workflow-dispatch action; local checkout previously failed DNS.

**Execution contract:** if workflow-only route is used, explicitly checkout immutable P40 target SHA; print Python, SQLite and OS versions; run lane commands for 1,2,3,5,6 and full scripts discovery. No source/test changes, provider calls, device tests, Pages deployment or spend. Lane 4 stays BLOCKED. Preserve run ID, triggering commit, checked-out target SHA, job log, environment, exit codes and test totals. Green workflow summary alone is insufficient.

## 3. Red-team corrections

1. **Manual dispatch:** previous analysis treated the workflow's `workflow_dispatch` key as if it made it dispatchable from the active branch. GitHub requires the workflow file on default branch; verified default `main` lacks this Python workflow. Manual dispatch is unavailable; active-branch push-filter route is viable.
2. **Browser eviction:** previous local-storage work did not make eviction a first-class recovery failure. MDN documents Safari's proactive seven-day inactive-origin eviction condition and all-origin-data eviction. A local receipt index can disappear with Cache/IndexedDB state. Browser storage is not durable backup.
3. **Worker isolation:** previous worker-channel analysis could be read as if a dedicated Worker were a security sandbox. OWASP confirms workers can make same-origin requests; CVE-2026-59214 demonstrates the impact for Pyodide's JS bridge. A Worker thread is not an origin boundary.
4. **OPFS compatibility:** previous discussion risked treating OPFS as uniform. SQLite distinguishes Safari <17 incompatibility for standard OPFS VFS, alternatives with different trade-offs, worker requirements, COOP/COEP and concurrency constraints.
5. **Event identity:** CloudEvents source+id and digests must not be described as producer authentication. Trusted producer verification and canonical payload integrity remain adapter/security responsibilities.
6. **Acceptance scope:** P40 model PASS, if obtained, cannot close production adapter or CASE acceptance. Lane 4 remains not testable; CASE-04 remains INCOMPLETE.

## 4. Source register: opened, maintenance and licence

| Source | Opened evidence / maintenance | Licence and reuse |
|---|---|---|
| AWS Prescriptive Guidance, Transactional outbox | Official AWS docs opened 2026-11-12; atomic state+outbox, duplicates, order | Documentation reference; no code copied |
| Debezium Outbox Event Router | Official maintained docs opened 2026-11-12; immutable INSERT, event ID, aggregate key | Apache-2.0 project; pattern only, no dependency |
| CloudEvents Core v1.0.2 | Official CNCF project; v1.0.2 latest released core, next draft WIP; opened 2026-11-12 | Apache-2.0 repository; identity model only |
| NATS JetStream acknowledgements | Official maintained docs opened 2026-11-12; at-least-once, ack/redelivery | Apache-2.0 project; reference only |
| Pyodide docs/repository | Current docs surfaced 314.1.0.dev0; active upstream; opened 2026-11-12 | MPL-2.0; no code copied |
| Open WebUI advisory GHSA-4r2p-27mh-5m22 / CVE-2026-59214 | Published 2026-06-29; reviewed/updated 2026-07-24; patched 0.10.0 | Security reference; no code reused |
| Open WebUI docs/discussion | Current docs and project discussions opened 2026-11-12; Pyodide basic-analysis/legacy direction | Current license has branding restrictions after v0.6.5; no code reused |
| OWASP HTML5 Security | OWASP project page reports 121 sheets/456 contributors; opened 2026-11-12 | CC BY-SA 4.0; attribute/share-alike if adapting text |
| MDN Storage quotas/eviction | Last modified 2026-01-05; opened 2026-11-12 | MDN CC BY-SA 2.5; requirements paraphrased |
| SQLite WASM persistence | Official SQLite docs include 2026-03 concurrency updates and SQLite 3.53+ features; opened 2026-11-12 | SQLite core public domain; sqlite-wasm wrapper Apache-2.0 |
| GitHub Actions manual workflow docs | Official GitHub docs checked in runner-path investigation | Documentation reference only |

## 5. Acceptance-ready follow-up matrix (no new canonical IDs)

| Work item | Required proof | Stop condition |
|---|---|---|
| P40 model run | Exact target checkout, ten pins, five lane logs, full-suite log, Python/SQLite/OS versions | Pin mismatch, wrong checkout, deployment/billing risk or unavailable runner |
| Grant event model revision | No-op parity, version/event parity, first-delivery envelope validation, separate relay fencing/takeover/stale-ack tests | No canonical envelope or trusted ingress authority |
| Browser sandbox contract | Parent/sandbox message schema, no ambient authority, network denial, bounded I/O, teardown and adversarial tests | Browser-only resource isolation cannot meet threat model |
| Browser storage recovery | iOS Safari/Android matrix, persist/quota/error/eviction/relaunch/export/readback, same-origin sibling review | Assumes persistent storage or path-based isolation |
| Receipt and lifecycle | Authenticated observations, same-attempt termination acknowledgement, durable receipt-head CAS, client digest/range acknowledgement | Caller/worker-supplied evidence treated as authority |

## 6. Evidence boundary

- **VERIFIED:** source facts above were read from pinned PocketCode files or prior source-pinned audit; external sources were opened as listed.
- **INFERRED:** opaque-origin sandbox plus narrow parent capabilities is the strongest browser-only starting pattern for untrusted code, but does not prove resource containment or finalize architecture.
- **UNKNOWN:** actual Pyodios worker topology, iPhone browser engine details for the user's app, current Pages headers, portfolio deployed scripts, target-device OPFS/persist support and durable production adapter.
- **NOT RUN:** new PocketCode tests, browser/device tests, live Pages probe, adversarial iframe tests and storage eviction/recovery tests.
- No canonical LOOP/CASE/D IDs changed. No provider, runtime, database, transport, storage engine or new host selected. No spending, deployment, DNS, PR or RevDev change.
