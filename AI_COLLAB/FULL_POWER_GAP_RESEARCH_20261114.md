# Full-power gap research and red-team delta — 2026-11-14

**Scope:** PocketCode only. Research/specification deliverable; no application or test changes. No provider, runtime, database, transport, storage engine, hosting origin or dependency selected. No implementation/adapter authorization implied.

**Pinned repository start:** `c3972a07a4546e08c41b87ec48bc2645ae9906e4` on `pocketcode-ai-workflow-director-research-2026-10-28`. Source blobs rechecked at this start: `scripts/event_journal.py` `371a175739b9cb65cd4d59bb4cd5b3c1c4953564`; `scripts/result_receipts.py` `0d1588f8590b57e0bf7447c7d5c519186ff0f39d`; `scripts/release_grant_conformance.py` `f9107fe46d60bbb5cd7115daf2513cd751221986`; `scripts/report_contract.py` `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`; `scripts/execution_projection.py` `f32237c8c5ee5d62b0416b3dd867515ce567c21b`.

## 1. Ranked gaps

| Rank | Gap | Why it is high value | Required proof |
|---|---|---|---|
| 1 | Journal conflict attribution and receipt watermark | A quarantined conflict consumes a journal sequence but is omitted from accepted events and can disappear from a receipt. | Immutable conflict attribution, separate observed/accepted watermarks, receipt snapshot and successor-receipt tests. |
| 2 | Grant event parity, relay fencing and consumer inbox | Aggregate versions can advance without matching events; a stale publisher can acknowledge after lease loss; first-delivery digest is sender-supplied. | Atomic aggregate+outbox, enforced relay fence at write boundary, authenticated canonical bytes, atomic inbox+projection. |
| 3 | Lifecycle termination and verdict provenance | Worker termination, native child exit, cleanup and client receipt are different facts. | Same-attempt authority for each lifecycle fact, contradictions retained, no PASS/FAIL from wrapper-only evidence. |
| 4 | Browser artifact durability and recovery | Browser storage is evictable and origin-private storage is not a user-owned backup. | Staged write/read-back, immutable manifest commit, eviction/restart recovery and explicit verified export. |
| 5 | Report-v2 compatibility boundary | Format 1's exit-code precedence can misclassify timeout/cancel/wrapper outcomes. | Versioned projection input, v1 golden compatibility and a separately authorized v2 regression suite. |

## 2. Current source findings and exact corrections

### 2.1 Journal conflicts need first-class evidence

**VERIFIED:** `EventJournal.append()` increments `_sequence` when the same `(source,event_id)` arrives with conflicting producer/payload details, then stores a `QuarantinedConflict` in `_conflicts`. It does not append that conflict to `_events`. `last_sequence` therefore covers accepted events and conflict observations, while `events` covers accepted events only.

**VERIFIED:** The current `QuarantinedConflict` carries sequence, source, producer event ID, accepted digest, conflicting digest and reason. It does not carry the attempted producer issuer/subject/key ID, credential fingerprint, audience, effect/attempt, fence, occurred time or observed time. The append path has those values available, but drops them when constructing the conflict record.

**VERIFIED:** `ResultReceipt` carries evidence refs/digests and free-form uncertainty strings. Its creation API has no journal observation high-water, accepted-event high-water or structured conflict references. A receipt can therefore be internally immutable yet fail to state which journal observations it includes.

**Decision: split two cursors.**
- `journal_observation_high_water`: highest sequence allocated to any accepted event or quarantined conflict in the snapshot.
- `accepted_event_high_water`: highest sequence of an accepted domain event in that snapshot.
- Never treat the first as proof that every sequence is an accepted domain event. Never derive it from the accepted-event list alone.
- Keep conflict observations outside the domain-event stream. Do not fabricate a domain event to fill a conflict sequence.
- A receipt snapshot must bind both cursors and a deterministic list of unresolved conflict references (or a canonical digest of that exact list plus retrievable immutable references). If a conflict is observed after the snapshot, append/reconcile it and create a successor receipt; never rewrite the old receipt.

**Required conflict attribution fields:** journal sequence; source and producer event ID; accepted and conflicting payload digests; attempted producer issuer, subject and key ID; credential fingerprint or immutable credential reference; audience; effect ID and attempt ID when supplied; fence when supplied; occurred and observed timestamps; conflict reason; and disposition state. Do not store credentials, tokens or signing secrets. A verified identity record is still not a cryptographic proof unless trusted ingress actually verified it.

**Acceptance:** (J-01) conflict increments observation high-water but not accepted-event high-water; (J-02) receipt records both watermarks; (J-03) conflict ref is included and retrievable; (J-04) same ID/same bytes remains duplicate without sequence allocation; (J-05) same ID/different bytes remains quarantined and cannot overwrite accepted evidence; (J-06) a late conflict creates a successor receipt; (J-07) restore cannot lower/reuse the journal high-water. These are proposed model/adapter cases, not canonical CASE IDs.

### 2.2 Grant event: bind the bytes, signer, scope and fence

**VERIFIED:** In `release_grant_conformance.py`, `record_progress()` increments `aggregate_version` on every accepted call and changes progress, but creates no matching `GrantEvent` or outbox item. An equal-progress call also advances the version. `consume_event()` trusts `event.payload_sha256` and records it on first delivery without recomputing a digest from canonical event bytes. `mark_outbox_delivered()` is an unguarded boolean update without owner, lease or fence comparison.

**Decision:** every semantic grant transition advances exactly one version and atomically writes exactly one immutable event/outbox record. An equal-value progress request is a no-op: no version increment and no transition event. If repeated progress observations are useful for telemetry, they belong in a separate observation stream and must not masquerade as aggregate transitions.

**VERIFIED external patterns:**
- AWS transactional-outbox guidance explicitly treats publication as at-least-once and requires idempotent consumers; aggregate state and outbox event must share one transaction. PostgreSQL 18 describes transactions as all-or-nothing and invisible until commit. These are patterns, not product database selections. [AWS outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html).
- etcd v3.6 transactions provide atomic compare/then/else operations. etcd's lease explanation warns that a lease can expire while a paused client still believes it owns the resource; revision/lease comparisons protect etcd keys, while an external resource must itself validate a monotonic fencing token. Apply this to the relay acknowledgement write, not just to worker-side lease timers. [etcd v3.6 transactions](https://etcd.io/docs/v3.6/learning/api/), [etcd lease/fencing explanation](https://etcd.io/docs/v3.5/learning/why/).
- CloudEvents Core v1.0.2 defines `source + id` duplicate identity. It does not authenticate the producer, authorize a tenant or prove payload integrity. The official repo lists v1.0.2 as latest release and working draft as WIP. [CloudEvents releases](https://github.com/cloudevents/spec/releases), [Core spec](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md).

**Concrete ingress profile if HTTP is ever selected:** RFC 9530 `Content-Digest` represents a digest of actual HTTP message content; RFC 9421 requires an application profile to specify covered components and explicitly discusses covering `Content-Digest`. The verifier must both verify the signature and recompute/compare the digest against received body bytes. Cover method, authority/target, content-digest and the security-critical tenant/grant/attempt/event identity fields used for authorization. Enforce key status, issuer/audience/scope, created/expiry bounds and nonce/replay handling. A valid signature does not itself authorize a grant or prevent a valid signed request from being replayed. No HTTP signature mechanism is selected. [RFC 9530](https://www.rfc-editor.org/rfc/rfc9530.html), [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421.html), [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html).

**Required acceptance:** (G-01) semantic no-op creates no version/event; (G-02) changed progress creates one event at the new version in the same commit; (G-03) crash before commit exposes neither aggregate nor event; (G-04) crash after commit recovers the same event ID/bytes; (G-05) stale relay fence cannot mark delivery acknowledged; (G-06) duplicate publication is harmless; (G-07) first delivery recomputes digest over exact canonical bytes; (G-08) same source/ID with different bytes is quarantined; (G-09) inbox identity and consumer projection commit atomically; (G-10) a version gap is deferred, not consumed.

### 2.3 Lifecycle and report verdict

**VERIFIED:** `execution_projection.py` is a pure helper whose caller must authenticate, authorize, deduplicate and persist observations. It separates direct-child natural exit, wrapper exit, signal termination and embedded-interpreter observations. It is not a coordinator or teardown authority.

**VERIFIED:** HTML's worker termination algorithm aborts the worker's currently running script and discards queued work; MDN describes `Worker.terminate()` as immediate, without an opportunity for the worker to finish. Neither statement proves a separate native child process, OS resource tree, remote provider job or browser renderer has terminated. [HTML worker model](https://html.spec.whatwg.org/multipage/workers.html), [MDN terminate](https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate).

**Decision:** retain distinct facts: termination requested; supervisor invoked worker termination; worker channel closed; direct child naturally exited or was signal-terminated; external process/job termination authoritatively acknowledged; cleanup completed; collection completed; artifact integrity verified; transport emitted; client acknowledged exact object/digest/range. A browser Worker acknowledgement cannot be promoted to native-child or OD-12 proof. A missing acknowledgement stays UNKNOWN/INCOMPLETE.

**VERIFIED red-team recheck:** `report_contract.py` still returns FAIL for any nonzero integer `exit_code` before checking lifecycle. Thus `timed_out + wrapper 137`, `cancelled + wrapper 143`, and a nonterminal status with stale exit metadata can become FAIL. The typed projection's timeout/cancel handling does not repair format 1 because the renderer is not wired to that projection.

**Decision:** preserve format 1 as legacy. Do not fix it by swapping condition order. The proposed format 2 consumes a trusted, immutable, already-resolved execution projection plus separate job/evidence and artifact dispositions. Contradictions remain INCOMPLETE. Keep CASE-04 INCOMPLETE / timed_out until canonical acceptance evidence exists.

### 2.4 Browser artifact durability

**VERIFIED:** MDN documents that IndexedDB transactions can abort on browser shutdown and that unload handlers are not a reliable place to commit state. The transaction durability property distinguishes `strict`, `relaxed` and `default` hints; these do not constitute independent backup. OPFS is origin-private, quota-bound, cleared with site data and not visible like the user's normal file system. [IndexedDB shutdown behaviour](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), [transaction durability](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability), [OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system).

**VERIFIED with age caveat:** WebKit's storage-policy article is dated 2023-08-10. It describes origin-level eviction under storage pressure/quota/inactivity and persistent-mode exceptions. It is useful platform guidance, not proof of current iOS device behaviour. The WHATWG Storage Standard is a living standard; its repository history surfaced a March 15, 2026 update. [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/), [WHATWG Storage Standard](https://storage.spec.whatwg.org/), [WHATWG repository history](https://github.com/whatwg/storage/commits).

**Decision:** retain the existing staged-write contract: immutable object version; write to staging; read back actual stored bytes; recompute byte length and digest; commit manifest pointer only after read-back; export only by explicit user action; verify digest again before export; import/restore as untrusted; missing or mismatched bytes become MISSING/QUARANTINED and evidence INCOMPLETE. OPFS/IndexedDB are candidates only, not selected. Local persistence is not backup, export success is not client receipt, and a GitHub Pages origin shared with the portfolio remains one trust domain.

### 2.5 Compatibility and reuse boundary

**VERIFIED maintenance/licence check (2026-11-14):**
- CloudEvents repository reports Core v1.0.2 as latest release and WIP for next work; its `LICENSE` is Apache-2.0. Use source/id semantics only, not as authentication.
- etcd documentation is versioned v3.6 for transactions; the repository `LICENSE` is Apache-2.0. Use the CAS/fencing explanation only; no etcd dependency.
- SQLite repository `LICENSE.md` says core SQLite source is public domain, with separate BSD-style build/configuration exceptions. Its WAL documentation says all database processes must be on one host, and `synchronous=NORMAL` can lose committed transactions after power loss/hard reset. No SQLite selection.
- RFC 8785 is an Informational RFC from June 2020; RFC 9421 and RFC 9530 are IETF Standards Track documents from February 2024. They are standards references, not software dependencies.
- WHATWG Storage/HTML are living standards. WebKit storage guidance cited above is from 2023 and must not be represented as current target-device testing.
- No source code was copied. No third-party code or documentation text was transplanted. Licences were checked to understand reuse boundaries, not to imply a dependency decision.

## 3. Red-team corrections to previous work

1. **Conflict attribution was underspecified.** Prior research called for conflict/quarantine evidence but did not spell out that the current conflict record drops the attempted producer, attempt/fence and timestamps even though append has those inputs. Fixed above with a complete immutable attribution record.
2. **The cursor semantics were underspecified.** `last_sequence` includes quarantined conflicts while `events` excludes them. A single “event high-water” would be ambiguous and could either hide conflicts or create false missing-event gaps. Fixed by two explicitly named watermarks and separate conflict references.
3. **HTTP signature/body integrity was too compressed.** A signature does not automatically authenticate a body just because a digest field exists. RFC 9421 requires the application profile to cover the digest field; RFC 9530 requires the recipient to validate the digest against actual content. Fixed by specifying both operations and their order.
4. **Storage evidence age was not prominent enough.** WebKit's 2023 article cannot settle current iPhone/iOS behaviour. Fixed by marking it as aged guidance and requiring exact-device tests.
5. **Worker stop wording could be over-read.** The browser standard does abort the worker's script, but that does not establish native child, remote job or OS teardown. Fixed by separating each acknowledgement and its authority.
6. **Report-v1 risk is a concrete source defect, not only a migration concern.** Rechecked the exact current blob and confirmed nonzero exit precedence remains. The format-2 plan must test timeout/cancel wrapper codes and contradictory terminal evidence.

## 4. Future acceptance packet

These are additional proposed model/adapter cases, not new canonical LOOP/CASE identifiers:

| ID | Scenario | Required result |
|---|---|---|
| JR-01 | Conflict arrives after accepted event sequence N | Observation high-water N+1; accepted-event high-water remains N |
| JR-02 | Receipt created with unresolved conflict | Receipt binds conflict ref and both watermarks |
| JR-03 | Late conflict after receipt | Old receipt unchanged; successor receipt captures new high-water |
| JR-04 | Conflict producer differs from original event producer | Both accepted and attempted identities retained without secret material |
| GR-01 | Equal progress repeated | No aggregate version or transition event increment |
| GR-02 | Progress changes | One new aggregate version and one immutable outbox event atomically |
| GR-03 | Old relay worker acknowledges after newer fence | Stale acknowledgement rejected at protected write |
| GR-04 | Signature valid but content-digest does not match body | Reject/quarantine; no state application |
| GR-05 | Same source/ID, different canonical bytes | Quarantine conflict; preserve first accepted event |
| LC-01 | Worker terminate called, no child/OS acknowledgement | Worker action recorded; native termination UNKNOWN |
| LC-02 | Timeout + wrapper exit 137 | INCOMPLETE / timed_out |
| LC-03 | Succeeded + natural child nonzero | INCOMPLETE contradiction |
| AR-01 | Browser shuts down during IndexedDB transaction | Abort/recovery state; no false committed manifest |
| AR-02 | OPFS object missing after restart | Artifact MISSING/QUARANTINED; no rerun as original attempt |
| AR-03 | Export reports success but bytes digest differs | Export not verified; preserve original local state |
| R2-01 | Legacy format-1 golden input | Compatibility retained until explicit migration decision |

## 5. Gate and evidence status

- **VERIFIED:** source findings above are present in the pinned blobs.
- **VERIFIED:** primary-source documents opened for AWS outbox, PostgreSQL transactions, etcd v3.5/v3.6, CloudEvents, RFC 8785/9421/9530, HTML workers, MDN IndexedDB/OPFS and WebKit storage policy.
- **INFERRED:** two journal watermarks plus structured conflict attribution are the minimum safe receipt model for the current sequence allocation semantics.
- **UNKNOWN:** production authentication, durable adapter, exact browser/device storage and worker topology, OS/renderer teardown and client receipt.
- **NOT RUN:** no source/test changes, no model tests, no device/browser tests, no artifact rerun.
- P39 implementation/adapter conformance gate remains CLOSED. Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. CASE-04 remains INCOMPLETE / timed_out. D-005/D-006 remain $0. No PR #2/#3/#4 changes.
