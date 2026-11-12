# Browser artifact storage and recovery contract

Date: 2026-11-12
Status: proposed contract; no storage engine or persistence technology selected.
Contract version: browser-artifact-recovery/v1. This is a document version, not a new canonical LOOP, CASE or D-ID.
Scope: phone-first PWA origin trust, local artifact staging, metadata integrity, restart recovery, eviction, export and acceptance evidence.

## 1. Ranked gap and current evidence

Rank 3 for this pass: a successful browser write is not equivalent to durable user data. A PWA must report the difference between locally staged, verified, recoverable, exported and client-received work.

VERIFIED from repository state and opened browser sources:
- PocketCode Pages and the portfolio Pages URLs share the same scheme, hostname and port. Their URL paths do not create a browser-origin boundary.
- Same-origin JavaScript can access the origin's IndexedDB, localStorage, Cache API and service-worker-visible data according to the granted browser model. Stored bytes and metadata must be treated as untrusted when read back.
- MDN's storage guide describes browser storage as best-effort by default, with quota differences and eviction. navigator.storage.estimate() is an estimate, not reserved capacity.
- navigator.storage.persist() may be denied. A successful persistence request is not a backup and cannot protect against user clearing data, device loss or application removal.
- WebKit's Tracking Prevention describes a seven-day inactivity cap for script-writable storage under its applicable conditions, including IndexedDB, localStorage, service-worker registrations and Cache API data.
- IndexedDB durability options distinguish strict and relaxed commit expectations, but are not an external backup guarantee.
- SQLite's official WASM persistence guide describes OPFS worker constraints and browser-specific VFS trade-offs. No browser or storage technology has been selected.

INFERRED: relying on a single browser-origin store as the only copy of a result is incompatible with a trustworthy phone-first workflow. An app that says “saved” without naming the durability level invites the user to assume more than the browser guarantees.

## 2. Artifact and evidence state vocabulary

Keep these states distinct. A later state must not be inferred from an earlier one.

| State | Meaning | What it does not prove |
|---|---|---|
| produced_in_memory | Worker/supervisor reported bytes in memory | local write, integrity, durability or release |
| staging_write | Parent is writing a bounded copy to local storage | complete object |
| locally_stored | Storage API reported write/transaction success | read-back integrity or future availability |
| integrity_verified | Parent read back exact bytes and verified length + SHA-256 | persistence against eviction or device loss |
| manifest_committed | Immutable receipt/artifact manifest references that exact verified object version | external backup or current release authorization |
| exported | User explicitly saved/shared a verified copy to an external user-controlled destination | recipient received or retained it |
| transport_emitted | Browser/network API reports bytes handed to transport | client observed or acknowledged them |
| client_observed | A client-side observation is available | client accepted/retained the artifact |
| client_acknowledged | Authenticated client acknowledgement binds exact digest/object/range | future retention beyond that system's evidence |

No generic “durable”, “saved forever” or “received” badge is permitted. The UI should say “saved on this device” only when manifest_committed and read-back verification succeeded, and should disclose that browser/device storage can still be cleared. The app may recommend exporting a separate copy, but must not label export complete until the explicit save/share action reports success.

These states map to OD-08 and OD-13. An artifact missing after restart is missing evidence, not a zero-byte artifact or successful empty result.

## 3. Origin trust and secret handling

- Until a separate origin is approved and independently verified, PocketCode and portfolio pages on the same Pages hostname are one trust domain.
- Never store access tokens, provider credentials, session identifiers, signing keys, secrets, authorization grants or other security authority in localStorage, IndexedDB, Cache API or OPFS on this shared origin.
- Treat every stored string, row, manifest, cached response, byte object and service-worker message as untrusted. Revalidate schema, digest, byte length, exact object version, receipt ID/revision, EffectId and DispatchAttemptId on read.
- Do not infer isolation from URL path, filename, JavaScript module, Worker, IndexedDB database name or service-worker scope alone.
- A future dedicated origin may be a stronger boundary, but no domain, hosting, DNS or extra spend is selected or authorized by this contract.
- Service workers are request-interception authority for their scope. The implementation must prove exact scope, script version/update, cache ownership and recovery behaviour before enabling artifact authority in a service worker.

## 4. Technology-neutral write protocol

A stored artifact is immutable and versioned. The exact storage API is selected only after target-device evidence and an implementation gate.

Stage:
1. Parent accepts an output only from the current execution session and only after the complete output bytes are available. OD-01 excludes incremental artifact streaming in MVP.
2. Validate maximum byte length, allowed artifact type, attempt identity, filename and parent-computed SHA-256.
3. Allocate a new ArtifactId and immutable object version. Never overwrite an existing object version.
4. Write bytes to a non-releasable staging location. If writing fails, retain an explicit incomplete/quarantined status; do not create a releasable receipt reference.
5. Read back the stored bytes from the actual storage location. Recompute byte length and digest. A digest of the input buffer alone does not verify the stored copy.
6. After read-back matches, commit the immutable manifest reference and receipt revision. The manifest binds artifact ID, object version, byte length, SHA-256, EffectId, DispatchAttemptId, ResultReceiptId/revision and collection/lifecycle disposition.
7. A fresh release grant and current policy check are still required before any download/share. Local presence is not authorization.

Atomicity:
- If the chosen store can keep bytes and metadata within one transaction, document exactly which object stores participate and test crash/abort semantics.
- If bytes and manifest live in different APIs or stores, do not claim one atomic transaction. Use staging then read-back then a manifest commit pointer. A crash between these steps leaves an orphan staged object, not a published artifact.
- The separate `ReceiptHead` must bind `ResultReceiptId` + revision to the exact canonical receipt SHA-256, or to an authenticated immutable reference that resolves to that digest. Define the exact canonical receipt bytes being hashed; do not hash a representation that includes its own derived digest. The receipt's artifact manifest binds each `ArtifactId` + object version to byte length, artifact SHA-256, integrity state and quarantine state.
- Grant reservation and recovery must compare the full receipt-head tuple (receipt ID, revision and receipt digest) and verify the exact artifact digest/length from the immutable receipt manifest. Only `integrity_state=verified` and `quarantined=false` are eligible. Identifier equality alone is insufficient.
- Use compare-and-swap against the expected receipt-head tuple, including its digest. Two concurrent tabs must not create conflicting successors or silently rebind the same ID/revision to different content.
- Persist sequence and fence high-water values without rollback after restore, consistent with OD-07. Local tab counters are not authoritative.
- A temporary cache is never the canonical artifact store. Cache eviction must not erase the only manifest or evidence pointer.

Read/recovery:
1. On startup or restore, identify the current application/manifest schema and the exact local origin. Do not migrate unknown versions by guessing.
2. Enumerate committed manifests and verify object version, byte length, digest, receipt binding and attempt identity. Read the bytes back before offering an artifact.
3. If a committed object is absent, inaccessible, truncated or mismatched, mark artifact disposition MISSING/QUARANTINED and overall evidence INCOMPLETE. Never regenerate or rerun the task as if it were the original artifact.
4. Keep old receipt revisions immutable. A local store restore does not make an old receipt current; re-check the receipt head and policy before release.
5. Unreferenced staging objects can be cleaned only after a conservative recovery scan establishes that no committed manifest or pending transaction references them. Cleanup itself is an observation, not proof of task termination.
6. Preserve the exact recovery failure and user-visible next action. Do not silently reset the local project to an empty state.

## 5. Browser persistence signals and limits

- navigator.storage.estimate() is advisory. Record available usage/quota as a time-stamped observation; do not reserve it or promise a write will fit.
- navigator.storage.persist() is a request whose result must be reported as granted/denied/unsupported/failed. Denial is not a task failure; it means automatic eviction remains a relevant risk. A grant does not cover user-cleared data, lost devices, profile removal, application removal or physical failure.
- For IndexedDB, record the requested durability mode and whether the transaction committed. strict is a stronger persistence hint than relaxed; it is still not backup, cross-origin protection or an absolute physical-media guarantee.
- QuotaExceededError, transaction abort, unavailable storage, browser private mode, tab discard, OS termination and storage eviction are normal failure modes. Each must preserve or reconstruct an explicit INCOMPLETE/recovery state where evidence permits.
- Browser APIs and quotas differ by engine and version. The product must report capability detection per current browser session, not infer iOS or Android support from desktop test results.
- WebKit's seven-day script-writable-storage eviction condition means the user can return after inactivity and find local browser data missing. A PWA install icon or service-worker registration is not an offline backup.
- Local retention and export policy remain owner/product decisions. Do not invent a storage duration or silently delete a user's only recoverable copy.

## 6. Export and user-owned recovery

MVP recovery should not depend exclusively on browser persistence:
- Offer explicit export of the verified report and completed artifacts through the phone's available browser save/share flow, where that flow is supported.
- Export only the exact manifest-bound object version. Recompute digest immediately before export; record the user action and browser result separately from receipt delivery acknowledgement.
- Keep export user initiated. No silent background upload, clipboard polling, automatic third-party destination, or provider credential export.
- An export failure leaves the on-device artifact state unchanged and records a separate failed export attempt. It does not invalidate a previously verified local artifact unless the local bytes also fail verification.
- On import/restore, treat the bundle or files as untrusted. Verify manifest schema, all byte lengths and digests, receipt/attempt links, duplicate IDs and incompatible schema versions before making the artifacts visible.
- A restored file is not automatically the current receipt head or authorized for release. Require fresh policy and the exact grant protocol.
- Bundle/container format, encryption, compression, share sheet API, backup destination and cloud sync are NOT selected. No external host or provider is introduced by this contract.

## 7. Storage candidate evaluation, not a selection

| Candidate | Useful properties | Risks/conditions to prove |
|---|---|---|
| IndexedDB | Structured records and transactions; can coordinate manifest and small/medium byte objects in a database transaction | browser quota/eviction, async lifecycle, schema upgrades, transaction abort semantics, multi-tab coordination, platform-specific behaviour |
| OPFS | Origin-private file API for larger byte objects; can stage and read back files | worker-only access patterns, quota/eviction, file write/read recovery, browser-version constraints, separate metadata transaction |
| SQLite WASM over OPFS | SQL transactions and familiar integrity constraints; official project maintains multiple persistence VFS paths | wrapper and VFS choice, worker constraints, Safari version compatibility, concurrency limits, COOP/COEP and SharedArrayBuffer implications |
| Cache API | Useful for disposable application resources and offline shell caching | cache is evictable application cache, not canonical artifact/evidence storage; service-worker scope and update behaviour |

No candidate is approved. In particular:
- SQLite core is public domain; sqlite-wasm wrapper is Apache-2.0. This is a licence fact, not a recommendation.
- SQLite's current OPFS docs distinguish the standard OPFS VFS from SAH-pool and WASMFS paths. The standard VFS has a documented Safari-below-17 incompatibility; alternative VFS paths have separate concurrency and platform trade-offs.
- These source facts do not prove compatibility with the user's installed Pyodios app, embedded WebView, current iOS or Android version.

## 8. Acceptance and recovery matrix

| Test scenario | Required result |
|---|---|
| Complete output written | Parent read-back digest and length match before manifest commit |
| Crash during staging write | No manifest points to partial bytes; explicit incomplete staging record or recoverable orphan |
| Crash after byte write, before manifest commit | Object remains unreferenced and is not releasable |
| Crash after manifest commit | Reopen verifies exact object/version/length/digest and receipt link |
| Input digest differs from stored read-back | Quarantine; no release grant |
| Manifest exists but object is missing | MISSING/INCOMPLETE; no rerun or silent empty success |
| Object exists but manifest is missing | Orphan; no implicit reconstruction of authority |
| Receipt head advanced in another tab | Old revision cannot be made current by restore |
| Two tabs race a receipt successor | One compare-and-swap wins; other must re-read and reconcile |
| Same receipt ID/revision presented with different canonical bytes/digest | Conflict and quarantine; never rebind an immutable receipt identity |
| Same artifact ID/object version presented with different bytes/digest | Immutable-object conflict; reject and preserve original object |
| Grant request matches IDs but receipt/artifact digest differs or manifest is quarantined | Deny before grant/event/outbox commit; no authorization by identifier equality alone |
| navigator.storage.persist() denied | Continue with disclosed best-effort storage and explicit export option |
| persist() granted then user clears site data | Data-loss recovery; do not claim persist() was a backup |
| Quota estimate changes between check and write | Write error handled; no manifest points to incomplete bytes |
| IDB transaction aborts | No partial metadata transition |
| Safari inactivity eviction occurs | Missing state becomes explicit; external export remains a recovery path if user made one |
| Private browsing or storage unavailable | Feature reports unsupported/ephemeral state; no false saved claim |
| Same-origin portfolio script reads/writes app origin storage | Treat as same trust domain; no secrets present; integrity/recovery checks detect altered data |
| Service worker update or scope mismatch | Fail closed for artifact authority; preserve evidence and require revalidation |
| Imported recovery files altered | Hash/schema/reference mismatch quarantined |
| Restored artifact is from superseded receipt | Historical artifact only; new grant denied unless current receipt head binds it |
| User exports a verified artifact | Record export attempt separately; do not claim client-acknowledged receipt |

Acceptance work must include real iOS Safari/WKWebView and Android tests for cold launch, force-close, browser termination, offline reopen, quota pressure, persistence permission, multi-tab writes, export/import, seven-day inactive-origin recovery and service-worker update. Versions must be recorded. None of those tests ran in this pass.

## 9. Research, maintenance and licence review

Official sources opened 2026-11-12:
- MDN Storage quotas and eviction: https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria. Updated 2026-01-05 when opened; best-effort quota, persistence request, eviction and browser-specific limits. MDN content CC BY-SA 2.5; design requirements paraphrased, no code copied.
- WebKit Tracking Prevention: https://webkit.org/tracking-prevention/. Maintained WebKit policy documentation; seven-day inactive-origin cap for script-writable storage under the documented conditions. No code copied.
- MDN IDBTransaction durability: https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability. strict/relaxed/default durability hints; no absolute backup guarantee. MDN content CC BY-SA 2.5; no code copied.
- SQLite WASM persistence: https://sqlite.org/wasm/doc/tip/persistence.md. Official maintained SQLite project guide; OPFS worker model, browser caveats and alternative VFS trade-offs. SQLite core public domain; sqlite-wasm wrapper Apache-2.0; no source copied.
- OWASP HTML5 Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html. Same-origin storage and service-worker/security guidance. CC BY-SA 4.0; no text/code copied.
- Existing PocketCode origin and storage audits: GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md and FULL_POWER_GAP_RESEARCH_20261112.md. Re-read by section, not treated as proof of current deployed headers.

Reuse decision: reuse browser-standard IndexedDB/OPFS/StorageManager concepts only as candidates. No database, file system, encryption, backup, runtime, provider or host selected; no code/dependency imported.

## 10. Red-team corrections to prior storage work

1. Earlier work described persistence and storage APIs but did not make a clear “save” vocabulary. Fix: state machine separates locally stored, read-back verified, manifest committed, exported, transport emitted, client observed and client acknowledged.
2. Earlier work could overstate navigator.storage.persist() as durability. Fix: record grant/denial and keep user-cleared data, device loss and profile removal outside its guarantee.
3. Earlier work mentioned Safari eviction but did not tie it to explicit recovery acceptance. Fix: include seven-day inactive-origin eviction and return-after-inactivity case with external export as the only independent copy.
4. Earlier OPFS analysis risked treating metadata + bytes as one transaction. Fix: use a staged object/read-back/manifest commit protocol when stores differ; an orphan staged object is never releasable.
5. Earlier work did not make the same-origin portfolio boundary an explicit storage trust assumption for all APIs. Fix: treat both Pages paths as one trust domain and store no credentials or security authority there.
6. A successful browser write or CI model test was too easily read as production durability. Fix: require exact target-device cold-start, crash, quota, eviction, restore and export evidence before any durability claim.

## 11. Gate and evidence boundary

VERIFIED: official MDN, WebKit, SQLite and OWASP source pages listed above were opened on 2026-11-12; current origin and OD policy facts are recorded in branch documents.
INFERRED: manifest-first staged storage plus explicit user export is a conservative product contract under the $0/no-cloud constraint.
UNKNOWN: live Pages headers/scripts, current Safari/WKWebView and Android target behaviour, persist() result, quota, iOS OPFS support in the installed app, service-worker state, origin integrity and actual local artifact durability.
NOT RUN: device tests, browser storage tests, crash/reopen, quota/eviction, multi-tab, export/import and service-worker tests.

No runtime, database, storage API, host or distribution choice is made. No canonical LOOP, CASE, OD or D identifier changed. P39 implementation/adapter gate remains CLOSED. CASE-04 remains INCOMPLETE / timed_out.
