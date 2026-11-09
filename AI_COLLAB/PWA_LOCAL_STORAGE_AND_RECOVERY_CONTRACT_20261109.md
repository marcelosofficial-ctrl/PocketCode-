# PWA local storage, lifecycle and recovery contract

**Date:** 2026-11-09  
**Status:** source-verified research / proposed product contract / NOT IMPLEMENTED / NOT RUN  
**Applies to:** owner-approved no-spend GitHub Pages installable-web-app path.  
**Does not authorize:** source/test changes, service-worker deployment, native app, storage-engine selection, runtime/provider/backend choice, remote execution, spending, or any change to D-001..D-006 or canonical LOOP/CASE/D IDs.

## 1. Highest-value gaps

1. **The existing PWA storage claim is too broad.** Home Screen web apps are exempt from ITP's seven-day script-writable-storage purge, but they are not immune to storage pressure, quota failures, explicit user clearing or every future browser policy.
2. **Local metadata and artifact bytes can fail at different points.** IndexedDB transactions cannot include OPFS file writes in one browser transaction. A file can exist without a committed manifest or a manifest can point to missing/corrupt bytes unless staging and reconciliation are explicit.
3. **PWA background work is opportunistic.** Service workers can be stopped; Background Sync is not Baseline and a WebKit support bug remains NEW. The app cannot promise a long-running task continues after the user closes or backgrounds the PWA.
4. **Multi-tab coordination needs a durable fence.** Web Locks are useful same-origin coordination, but the authoritative generation and every state mutation still belong in the local database transaction.
5. **The storage implementation should reuse browser primitives first.** IndexedDB, Web Locks, Storage API and optionally OPFS already exist. idb and Dexie are maintained wrapper candidates, not prerequisites and not durability guarantees.

## 2. Verified WebKit policy and correction to the no-spend PWA plan

### 2.1 Home Screen ITP exemption

**VERIFIED:** WebKit's current Tracking Prevention page explicitly says the first-party domain of a Home Screen web application is exempt from ITP's seven-day cap on script-writable storage. It also says Home Screen web-app data is isolated from Safari and is not affected by Safari's ITP tracking classification. The affected script-writable types include IndexedDB, LocalStorage, SessionStorage, Service Worker registrations and Cache storage. Primary sources: [WebKit Tracking Prevention](https://webkit.org/tracking-prevention/) and [Full Third-Party Cookie Blocking and More](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/).

**Decision correction:** the earlier statement in `NO_SPEND_PWA_PATH_20261108.md` that this was only secondary evidence should be updated: the ITP exemption is now **VERIFIED from WebKit primary documentation**. A Home Screen app is a distinct web-app context, not just a Safari tab with an icon.

### 2.2 The exemption is not a permanent-data promise

**VERIFIED:** WebKit's storage-policy guide says storage can be evicted under overall quota pressure, system storage pressure and inactivity rules; eviction is normally origin-wide and LRU. It says best-effort storage is evictable, while an origin may request persistent mode. WebKit's Storage API guidance says `persist()` approval is heuristic (including whether the site is opened as a Home Screen web app), and `estimate()` provides estimates, not a guarantee that the reported quota can be filled. `QuotaExceededError` must still be handled. Sources: [WebKit Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/) and [MDN storage quotas/eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria).

**Required product wording (PROPOSED):**
- Installed Home Screen web app: “Your work is saved on this device. The Home Screen app avoids Safari's seven-day inactive-site purge, but local data can still be lost if you clear website data, storage fails, or the device/browser removes data. Export important projects and reports.”
- Not installed / opened as ordinary Safari tab: “This page may lose locally stored work after prolonged inactivity or storage pressure. Install as a Home Screen web app and export important work.”
- Persistent storage request granted: “Browser eviction protection requested and granted for this origin. This is not a backup and does not protect against manual clearing, device loss, corruption or every platform failure.”
- Persistent storage denied/unsupported: show “Best-effort local storage”; never imply durable backup.

### 2.3 Safari 26 installation behavior

**VERIFIED:** WebKit's Safari 26.0 release notes (15 September 2025) say that on iOS 26/iPadOS 26 every site added to the Home Screen opens as a web app by default. The Add to Home Screen UI contains an **Open as Web App** switch; the user can turn it off to add a browser bookmark instead. A Web App Manifest is no longer required for the site to open as a Home Screen web app, but manifest features and defined icons are still used. Source: [WebKit Features in Safari 26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/).

**Compatibility consequence:** do not give one timeless install instruction. For iOS 26+, instruct the user to use Share → Add to Home Screen and leave **Open as Web App** enabled. For earlier versions, retain the manifest `display: standalone` / legacy iOS meta-tag compatibility path where required. Keep a manifest and icons regardless because they improve app identity/launch configuration. The owner's exact iOS/Safari version remains UNKNOWN until device verification.

## 3. IndexedDB: local transactional authority

**VERIFIED:** IndexedDB 3.0 is published as a W3C Working Draft dated 30 October 2026. Its transaction model defines active/inactive/committing/finished states; transactions become inactive when control returns to the event loop outside a request event, and new requests cannot be issued while inactive. Transactions are expected to be short-lived. Overlapping read-write transactions with overlapping object-store scopes cannot run concurrently. Sources: [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB-3/) and [MDN transaction lifetime guide](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB).

### 3.1 Required object-store transaction boundary

A single IndexedDB database transaction should contain the local metadata that must move together:
- command and immutable user input manifest;
- DispatchAttempt and execution-boundary declaration;
- monotonic local attempt/event sequence;
- append-only observation records;
- derived lifecycle projection;
- artifact manifest and receipt revision metadata;
- local outbox items and idempotency lookup index;
- fencing generation / current owner generation;
- recovery marker and migration/schema version.

**INFERRED contract:** any state transition that claims “committed” must atomically write all related records in this store set. The application must wait for the transaction's `complete`/resolved completion signal before presenting a committed state. A request success is not transaction commit. Transaction abort, quota failure, version change, browser close or uncertain completion must be reconciled by rereading canonical records on next launch.

### 3.2 Keep transactions short

Never keep an IndexedDB transaction open while waiting for:
- a network request or provider response;
- user input or a modal;
- long-running Python/WASM/worker execution;
- large file hashing or streaming;
- an arbitrary timer or unrelated Promise.

Persist intent first, commit. Perform the external operation outside the transaction. Then open a new transaction, reread exact identity and current fencing generation, and append the resulting observation. If the response is lost, mark/recover ambiguity using the same EffectId/attempt; do not resend merely because the JavaScript Promise rejected or the tab disappeared.

This is not a stylistic recommendation. The browser transaction can become inactive after the event loop returns and automatically commits once the pending requests have completed.

### 3.3 Durability hint

**VERIFIED:** IndexedDB exposes `strict`, `relaxed` and `default` durability hints. `strict` allows the user agent to consider a transaction successfully committed only after verifying outstanding changes reached persistent storage; the specification notes that typical implementations may flush OS I/O buffers before firing completion. This can increase latency and battery use. `relaxed` may consider writes committed after they reach the OS without subsequent verification. Source: [W3C IndexedDB durability](https://www.w3.org/TR/IndexedDB-3/#transaction-durability) and [MDN IDBTransaction.durability](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability).

**PROPOSED policy:**
- Request `strict` for command/attempt reservation, event append, receipt commit, outbox intent, fencing-generation changes and artifact-manifest publication when the browser supports the options.
- Allow `relaxed` for reconstructible UI caches, search indexes, previews and disposable downloads.
- Record whether strict was requested and the actual `transaction.durability` value when available.
- If unsupported or rejected, fall back explicitly to `default`, record the downgraded guarantee and do not display “power-loss durable”.
- Verify by device crash/force-close tests. A durability hint is not a cross-device backup, a transactional guarantee across OPFS, or protection from user clearing.

## 4. Large artifacts: OPFS staging, IndexedDB commit and recovery

**VERIFIED:** OPFS is a private, origin-scoped file system, available in workers and subject to browser quota/eviction. Clearing site data deletes OPFS. Synchronous access handles are available in workers; their `flush()` method ensures that writes through the handle have been flushed to the file. OPFS data is not a user-visible local filesystem. Sources: [MDN OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) and [WebKit OPFS introduction](https://webkit.org/blog/12257/the-file-system-access-api-with-origin-private-file-system/).

**Important boundary (INFERRED):** OPFS operations and IndexedDB transactions are separate APIs. No cross-API atomic transaction is specified. Never describe a file write plus a database manifest write as one ACID commit.

### 4.1 Staging protocol

1. Allocate a new immutable ArtifactId/object version and a unique staging path. Do not reuse an old path for different bytes.
2. Persist an artifact record with disposition `staging` and bind it to CommandId, DispatchAttemptId and ExecutionId in IndexedDB.
3. Write bytes to the OPFS staging file. Check every write's returned byte count; handle short/failed writes.
4. Flush and close the access handle. Read the stored file back and calculate SHA-256 over those stored bytes, not only the producer's in-memory buffer.
5. Verify exact byte length and digest against the expected result. A producer-supplied digest remains a claim until readback succeeds.
6. In one IndexedDB transaction, re-check attempt identity and current fence; append the artifact-integrity observation; set the immutable artifact manifest to `verified_staged`; create the next receipt revision; append the corresponding event/outbox record. Commit this transaction before the artifact can be released.
7. Release/read/export only by resolving the committed receipt manifest to that exact immutable object version and rechecking existence, length and digest.

### 4.2 Crash matrix

| Failure point | Durable state expected | Recovery |
|---|---|---|
| Before staging record | No artifact entry | Nothing to recover |
| After staging record, before file creation | `staging`, file absent | Mark interrupted staging; safe to remove record only through audited cleanup |
| During write | `staging`, partial bytes possible | Quarantine; never attach to a receipt |
| After flush/close, before readback | `staging`, file may be complete | Read back and verify; do not assume success |
| After readback, before manifest transaction | Complete orphan staging object | Retry verification or quarantine; no release |
| During IndexedDB manifest/receipt transaction | Transaction commits all records or aborts | Reread transaction outcome; do not infer from an in-memory flag |
| After receipt commit | Manifest points to verified object version | Verify file on every release/export; if missing or digest differs, quarantine and create a new receipt revision |
| During explicit user export | Existing receipt/artifact unchanged | Retry export of same immutable receipt; do not rerun execution |

### 4.3 Fallback when OPFS is missing

Use IndexedDB Blob storage for bounded artifacts if measured device/browser tests show acceptable memory, quota and performance. Otherwise mark that artifact export mode as unsupported/degraded and ask the user to export smaller chunks. Do not silently use an undocumented native filesystem or a third-party CDN. Regardless of local storage choice, provide an explicit user-controlled export/backup path. OPFS alone is not backup because it is origin-private and cleared with site data.

## 5. Multi-tab and worker coordination

**VERIFIED:** Web Locks is broadly supported in modern browsers, works in workers, and coordinates tabs/workers within the same origin. It queues lock requests while a lock is held and releases the lock when the callback completes. It is a coordination primitive, not a persistent business-state ledger. Sources: [MDN Web Locks API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API) and [Web Locks specification](https://www.w3.org/TR/web-locks/).

**PROPOSED local ownership pattern:**
1. Request a named exclusive origin lock such as `poco:local-dispatcher` when Web Locks exists.
2. Inside a short IndexedDB read-write transaction, read and increment a durable generation/fence for the operation being claimed; store the owner context and attempt binding.
3. Before each protected state mutation, re-read the current generation within the same transaction as the mutation. A stale generation cannot append an observation, publish a receipt or advance an outbox row.
4. Release the Web Lock when the work callback ends or context disappears. The next owner must re-read and reconcile persisted state, not trust the prior tab's memory.
5. If Web Locks is unavailable, rely on IndexedDB transaction serialization plus compare-and-swap/generation checks. Feature detection changes the optimization, not the safety rule.

Do not use a local wall-clock lease expiry as the only safety check. The durable generation is the stale-writer fence. Local clocks can inform liveness/UX but do not authorize a stale writer.

## 6. Worker, service-worker and background constraints

**VERIFIED:** The W3C Service Workers Candidate Recommendation Draft dated 29 October 2026 states that user agents may terminate service workers at any time when there is no event to handle or when operation is abnormal/over time limits. MDN says the service worker's global state is not persisted across termination/restart and that browsers terminate idle workers. `waitUntil()` extends an event's lifetime, but MDN's PWA guide says it is not a guarantee: an overlong operation may be stopped, aborted and rerun from the start on a later sync event. Sources: [W3C Service Workers 2026 CRD](https://www.w3.org/TR/2026/CRD-service-workers-20261029/), [MDN ServiceWorkerGlobalScope](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope) and [MDN offline/background guide](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation).

**VERIFIED:** Background Sync is labelled “Limited availability” and “not Baseline” by MDN. WebKit bug 201866, requesting Safari iOS Background Sync support, still displays status NEW in the fetched bug record. That bug's last visible update is old, so it is supporting evidence of a compatibility risk, not a timeless proof of current support. Sources: [MDN Background Synchronization](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API) and [WebKit bug 201866](https://bugs.webkit.org/show_bug.cgi?id=201866).

**Required design:**
- Never promise an execution continues after tab/app closure, screen lock, OS suspension, worker termination or process kill.
- Persist command and attempt intent before starting execution. Persist bounded progress/observations as the operation proceeds. A lost context leaves the attempt unresolved until reconciled.
- On next foreground launch, reconcile the last committed state. If the attempt was `running` without a trusted terminal observation, project it as interrupted/unknown/incomplete; do not invent success, failure or termination.
- A retry must be a distinct authorized attempt, unless the exact-effect reconciliation rules prove the previous effect did not happen or a downstream idempotency contract safely deduplicates it.
- Foreground recovery triggers may include app start, `pageshow`, `visibilitychange` and `online`. These are wake-up opportunities, not evidence that the network or provider is ready.
- Background Sync/Push may be feature-detected as optional adapters. They must not be required for local persistence, execution completion, retry safety or final report publication.
- Do not start arbitrary user code from an unattended service-worker event. A worker can be killed, has no durable global memory, and must not be treated as an independently trusted execution host.

## 7. Open-source reuse and licence/maintenance review

| Candidate | Current source checked 2026-11-09 | Licence | Decision |
|---|---|---|---|
| Native IndexedDB API | W3C IDB 3.0 Working Draft 2026-10-30; browser built-in | Web standard; no third-party runtime dependency | Baseline candidate. Use for bounded metadata/atomic local record transitions, subject to mobile browser conformance tests. |
| `idb` by Jake Archibald | Package metadata reports v8.0.4; small Promise wrapper | ISC in current package.json | Accept as a low-level wrapper candidate only. It simplifies request/transaction Promises but inherits IndexedDB lifecycle, quota and durability limits. Check exact release/source pin before adoption. |
| Dexie.js | Latest release page shows v4.4.7; 2,960 repository commits; release includes query, transaction lifecycle and Safari-like environment fixes | Apache-2.0 | Accept as a higher-level candidate if schema/query ergonomics materially reduce code. Do not use Dexie Cloud or paid sync products under D-006. It does not remove OPFS/IDB cross-store crash windows. |

Sources: [idb repository and package.json](https://github.com/jakearchibald/idb), [Dexie releases](https://github.com/dexie/Dexie.js/releases), [Dexie repository/licence](https://github.com/dexie/Dexie.js). This is not a transitive dependency audit. No library is selected or added.

**Reuse rule:** prefer the native browser platform or the smallest wrapper that solves an observed code-quality problem. Keep the app's persistence interface provider-neutral and keep transaction/recovery semantics in PocketCode's own contract. Do not outsource EffectId, attempt identity, durable fencing, evidence provenance or product policy to an ORM or sync service.

## 8. Proposed PWA persistence interface and state rules

Names here are proposed internal contract labels, not canonical LOOP/CASE IDs or a frozen schema.

| Operation | Atomic local write | External work allowed between writes? | Required recovery |
|---|---|---|---|
| `create_command` | CommandId + canonical input manifest + initial event | No | Same identity resolves exact original command |
| `start_attempt` | New DispatchAttemptId + ExecutionId intent + fence generation + start event | Execution begins only after commit | Unclosed start becomes unresolved on next launch |
| `record_observation` | Bound raw observation + ObservationSequence + projection update | No | Exact duplicate deduped; changed content under same identity quarantined |
| `stage_artifact` | Staging intent + ArtifactId/version | File writes outside IDB tx | Orphan/partial stage is quarantined or re-verified |
| `commit_receipt` | Verified manifest + receipt version + predecessor + event/outbox | No | Retry returns same revision if canonical content identical |
| `queue_publication` | PublicationAttemptId + outbox identity + immutable receipt reference | Actual copy/share/network outside tx | Retry publication of same receipt; never rerun command |
| `claim_local_work` | Owner generation/fence + claim event | Work outside tx | Every later write compares generation in its transaction |
| `recover_launch` | Recovery observation + state projection update | Read-only scans outside tx; each fix committed separately | Never auto-dispatch an ambiguous prior effect |

### Commit protocol pseudocode

The database call should be shaped as a short local transaction; any network or user-code step belongs outside it.

```js
async function persistStart(db, command, attempt, execution) {
  const tx = db.transaction(
    ["commands", "attempts", "events", "outbox", "fences"],
    "readwrite",
    { durability: "strict" }
  );

  const currentFence = await tx.objectStore("fences").get(attempt.effectId);
  const nextFence = (currentFence?.generation ?? 0) + 1;

  await tx.objectStore("commands").add(command);
  await tx.objectStore("attempts").add({
    ...attempt,
    executionId: execution.executionId,
    status: "running",
    fenceGeneration: nextFence
  });
  await tx.objectStore("fences").put({
    effectId: attempt.effectId,
    generation: nextFence
  });
  await tx.objectStore("events").add(makeAttemptStartedEvent(command, attempt, execution, nextFence));
  await tx.objectStore("outbox").add(makeLocalObservationOutbox(command, attempt, execution, nextFence));

  await tx.done; // transaction commit, not merely successful individual requests
  return { generation: nextFence, committed: true };
}
```

This illustrates the transaction boundary, not production-ready code. It assumes the selected IndexedDB wrapper exposes `tx.done` like `idb`; with native IndexedDB, wait for the transaction `complete` event and handle `abort`/error. Before finalization, the transaction must also check unique identity and idempotent replay, not overwrite an existing CommandId/attempt. Feature-detect strict durability and record any fallback. Do not carry an IDB transaction across execution or network awaits.

## 9. Acceptance and adversarial tests

These are proposed `PWA-*` tests, not additions to canonical LOOP/CASE/D or P39 IDs. Run on actual supported iOS Safari/Home Screen and Android browsers; no device result is claimed.

| ID | Scenario | Expected result |
|---|---|---|
| PWA-STOR-01 | Commit command, attempt, start event and outbox in one transaction; inject a request failure | Entire transaction aborts; no partial start projection |
| PWA-STOR-02 | Close/reload immediately after transaction completion | Exact committed records read back with original identities |
| PWA-STOR-03 | Request strict durability where supported; inspect actual transaction durability | Record actual hint; unsupported path falls back without a durability claim |
| PWA-STOR-04 | Quota exceeded while writing command/receipt metadata | Transaction fails closed; no partial PASS/receipt claim; user sees export/cleanup guidance |
| PWA-STOR-05 | Quota exceeded in OPFS mid-write | Partial object remains staging/quarantined; no manifest release |
| PWA-STOR-06 | iOS Safari normal tab idle beyond seven days | Verify documented ITP deletion behavior separately from Home Screen; no assumption from a recent tab test |
| PWA-STOR-07 | iOS Home Screen web app idle beyond Safari seven-day window | Confirm WebKit ITP exemption and app/Safari data separation; also test storage pressure separately |
| PWA-STOR-08 | Call `persist()` and inspect `persisted()` | Record grant/denial; denial remains best-effort; no guarantee based on install alone |
| PWA-STOR-09 | Force-close app between OPFS write, flush, readback and manifest commit | Apply crash matrix; no unverified artifact becomes released |
| PWA-STOR-10 | Manifest points to absent/truncated/mutated OPFS bytes | Readback fails; quarantine and create successor receipt, never repair old receipt silently |
| PWA-TXN-01 | Await network fetch inside an IndexedDB transaction | Test demonstrates inactive/aborted transaction risk; code path prohibited |
| PWA-TXN-02 | Two tabs write overlapping stores concurrently | Transaction serialization and identity constraints prevent a fork |
| PWA-LOCK-01 | Two tabs request the same Web Lock | One callback owns coordination at a time |
| PWA-FENCE-01 | Tab A holds generation n; tab B commits generation n+1; A resumes | A's stale write is rejected by generation check inside the transaction |
| PWA-FENCE-02 | Web Locks unsupported/throws | Database compare-and-swap still prevents stale mutation |
| PWA-LIFE-01 | Worker/service worker is terminated while task is running | New launch reconstructs from committed state; attempt is unresolved/incomplete absent terminal evidence |
| PWA-LIFE-02 | `waitUntil()` event exceeds browser time limit and replays | Handler is idempotent; committed steps are not duplicated; ambiguous external effect reconciles |
| PWA-SYNC-01 | Background Sync missing or registration rejected | Foreground recovery still works; no feature-critical flow blocked |
| PWA-SYNC-02 | Replayed sync event is delivered after prior attempt sent but ack was lost | Same EffectId is reconciled; no unsafe duplicate dispatch |
| PWA-EXPORT-01 | User exports project and exact receipt after local persistence | Export contains manifest, version, identities, hashes and artifacts; import verifies hashes before accepting |
| PWA-MIG-01 | Upgrade database schema with old open tab still connected | Blocked versionchange is visible; no silent schema partial migration or data loss |
| PWA-REC-01 | Attempt persisted running; user closes app before terminal observation | Next launch marks outcome unresolved; no synthesized PASS/FAIL/termination |
| PWA-REC-02 | Publication interrupted after receipt commit | Re-export/re-publish same receipt; no rerun or new execution attempt |

## 10. Red-team corrections and decision status

1. **Corrected stale PWA evidence status:** Home Screen exemption from Safari's seven-day ITP cap is VERIFIED in WebKit primary documentation, not merely secondary reporting.
2. **Removed overbroad persistence claim:** Home Screen exemption is not equal to permanent durability. Quota/storage pressure, manual clearing, user-agent failures and device loss remain real risks.
3. **Corrected iOS 26 installation guidance:** manifest is no longer required to make a site open as a Home Screen web app in iOS 26; the user-facing `Open as Web App` switch is now the important choice. Keep manifest/icons for app metadata and older platform behavior.
4. **Reframed OPFS atomicity:** large artifact bytes and IndexedDB metadata cannot be assumed to commit atomically together. Staging, readback, manifest commit and orphan recovery are required.
5. **Removed background completion assumptions:** service workers can be terminated; `waitUntil()` does not provide unbounded runtime; a retried event begins its handler again. Persist each logical step and reconcile.
6. **Rejected Background Sync as an MVP dependency:** MDN says not Baseline; the current WebKit issue record still shows NEW. Feature-detect only.
7. **Narrowed Web Locks' role:** it coordinates same-origin tabs/workers but does not replace database generation checks or durable fences.
8. **Narrowed strict-durability claims:** IndexedDB's strict option is a hint with performance/power costs, not a backup or cross-API transaction.
9. **Preserved product boundaries:** no provider, runtime, database, hosting, cloud service, signing scheme, framework or sync engine is selected; no new acceptance canonical IDs introduced.

**Gate:** P39/exit provenance implementation gate remains **CLOSED**. This PWA research does not resolve Gemini's independent P39 review or owner OD-01..OD-13. No product source/tests were changed. No tests or device experiments were run.

## 11. Primary-source and maintenance register

All factual platform statements above are tied to primary/specification sources opened 2026-11-09. Publication dates are included to distinguish current platform behavior from older release notes.

1. W3C, [Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB/) (latest published snapshot opened 2026-10-30, Working Draft): transaction lifecycle/scopes/durability hints.
2. W3C, [Service Workers](https://www.w3.org/TR/2026/CRD-service-workers-20261029/) (Candidate Recommendation Draft 2026-10-29): worker lifetime and termination.
3. WebKit, [Tracking Prevention](https://webkit.org/tracking-prevention/): current shipped behavior including seven-day storage purge and explicit Home Screen origin exemption.
4. WebKit, [Full Third-Party Cookie Blocking and More](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/) (2020-03-24): seven-day script-storage deletion and Home Screen counter/isolation behavior.
5. WebKit, [CNAME Cloaking and Bounce Tracking Defense](https://webkit.org/blog/11338/cname-cloaking-and-bounce-tracking-defense/) (2020-11-12): explicit Home Screen ITP storage exception.
6. WebKit, [Updates to Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/) (2023-08-10): quota, storage pressure, LRU eviction and persistent-storage heuristics.
7. WebKit, [Safari 26.0 Features](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) (2025-09-15): iOS/iPadOS 26 Home Screen web app behavior and manifest role.
8. MDN, [IndexedDB transaction use](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), [durability property](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability), and [storage quotas/eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria): implementation guidance and browser quota failure handling.
9. MDN, [Origin Private File System](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system): worker-only synchronous handles, flush, quota and site-data deletion.
10. MDN, [Web Locks](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API): same-origin coordination.
11. MDN, [Background Synchronization](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API), [ServiceWorkerGlobalScope](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope), and [offline/background operation](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation): limited availability and service-worker lifecycle.
12. WebKit Bugzilla, [Background Sync API request 201866](https://bugs.webkit.org/show_bug.cgi?id=201866): fetched current status NEW; old issue history, therefore only a risk indicator.
13. Jake Archibald, [idb](https://github.com/jakearchibald/idb) and package metadata (v8.0.4, ISC).
14. Dexie, [release history](https://github.com/dexie/Dexie.js/releases) (latest visible v4.4.7) and [Apache-2.0 licence](https://github.com/dexie/Dexie.js/blob/master/LICENSE).

**Not verified:** the owner's current iOS version, current Safari/WebKit build, exact quota on the owner's iPhone, Storage API persistence result on that device, browser-specific durability implementation details, crash/power-loss behavior on physical hardware, current Background Sync support on every browser/engine variant, or OPFS atomicity across browser APIs. These require device/engine tests before any release guarantee.
