# Research delta and red-team corrections — 2026-11-13

**Scope:** PocketCode only; supplement to `FULL_POWER_GAP_RESEARCH_20261112.md`. No code copied, no dependency selected, and no implementation authorization implied.

## 1. Ranked gaps

| Rank | Gap | Why it matters | Acceptance evidence required |
|---|---|---|---|
| 1 | Untrusted execution isolation | User code must not inherit app-origin credentials, DOM, storage or ambient network authority. A Worker is not an origin boundary. | Opaque-origin sandbox, CSP, default-deny network, validated narrow protocol, bounded I/O, adversarial and exact-device tests. |
| 2 | Aggregate/event/outbox atomicity and relay fencing | Aggregate version can advance without an event; delivered marker is unguarded. Crash or stale publisher can lose/order events. | One transaction for aggregate+immutable outbox; no-op semantics; ordered lease claim; fencing at protected write; stale-ack rejection; crash/restore tests. |
| 3 | Authenticated producer and atomic consumer inbox | Event ID and caller-supplied digest do not authenticate producer or first-delivery payload. | Authenticated producer/scope, canonical-byte digest recomputation, replay/key/time policy, atomic inbox+state mutation, conflict/quarantine evidence. |
| 4 | Lifecycle, termination and client receipt | Worker stop action, child exit, cleanup, transport acceptance and client receipt are different facts. | Authenticated same-attempt lifecycle, separate verdict/evidence/artifact projections, authoritative termination, client ack bound to digest/version/range. |
| 5 | Browser origin and artifact durability | Pages and portfolio share one origin; browser storage can be evicted and is not a backup. | Approved origin boundary or accepted threat model; target-device quota/eviction/restart tests; explicit verified export/recovery; no secrets on shared github.io. |

## 2. Primary-source research and reuse

### 2.1 Atomicity and fencing

**VERIFIED:** AWS Prescriptive Guidance says aggregate state and outbox event must commit atomically; publication may duplicate; consumers must be idempotent; event order should follow aggregate update order. Rolled-back state must not publish. [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

**VERIFIED:** PostgreSQL 18 documents transaction blocks as a unit of related changes, with COMMIT making the changes visible and durable after crash. This is an atomicity reference, not a database choice. [BEGIN](https://www.postgresql.org/docs/current/sql-begin.htm), [COMMIT](https://www.postgresql.org/docs/current/sql-commit.htm).

**VERIFIED:** etcd v3.5 supports atomic compare-and-swap transactions. Its lease guidance warns that lease expiry alone does not ensure mutual exclusion: the client may still believe it owns an expired lease. Revision/lease comparisons protect etcd keys; an external resource must itself validate a monotonically increasing fence to reject stale writers. This is the crucial adaptation for PocketCode's relay. [etcd transaction API](https://etcd.io/docs/v3.5/learning/api/), [lease/fencing explanation](https://etcd.io/docs/v3.5/learning/why/).

**VERIFIED:** SQLite WAL improves reader/writer concurrency, but official docs state WAL requires processes on the same host and does not work over a network filesystem. [SQLite WAL](https://www.sqlite.org/wal.html).

**Reuse:** adapt AWS outbox/idempotency/order and etcd compare/revision/fencing principles. Do not adopt PostgreSQL, etcd, SQLite, a broker or CDC. No code copied.

### 2.2 Event identity, canonical bytes and authenticity

**VERIFIED:** CloudEvents Core v1.0.2 is the latest released core listed by the official CNCF-hosted repo; next core text is WIP. `source`+`id` identifies duplicates. It does not authenticate producer authority or prove payload integrity. [Release/status](https://github.com/cloudevents/spec), [Core v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md).

**VERIFIED:** RFC 8785 (June 2020, Informational) defines JSON Canonicalization Scheme for repeatable cryptographic operations. It uses I-JSON/IEEE-754-compatible numbers, rejects duplicate property names, sorts properties deterministically and does not Unicode-normalize strings. Large integers needing exact cross-language representation should be strings. Python sorted JSON alone is not proof of JCS. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html).

**VERIFIED:** RFC 9421 (February 2024, IETF Standards Track) defines signatures/MACs over selected HTTP components. Each application must specify required covered components, key/algorithm rules and time bounds. It does not directly sign message content; a content digest is needed when body integrity matters. A valid signature still does not decide tenant/grant authorization or replay policy. [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421.html).

**Reuse:** CloudEvents only as an optional envelope; JCS as a canonicalization candidate after schema profiling; RFC 9421 only with a selected transport and explicit signature profile. CloudEvents repo is Apache-2.0; RFCs are standards texts. No code copied.

### 2.3 Browser storage and worker termination

**VERIFIED:** WHATWG Storage Standard is a living standard last updated 2026-10-19; it defines origin-keyed buckets, persistence requests and quota estimates. An API does not guarantee persistence against user deletion or device loss. [Storage Standard](https://storage.spec.whatwg.org/).

**VERIFIED:** WebKit's 2023-08-10 Safari storage-policy article describes origin quotas and origin-level eviction under storage pressure or inactivity. It predates current Safari releases, so exact behavior requires target-iPhone testing. [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/).

**VERIFIED:** MDN says IndexedDB transactions are short-lived and may abort on shutdown; relaxed durability can report completion after the OS is told to write but before physical flush. Transactional local state is not a backup. [IndexedDB terminology](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology), [Using IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB).

**VERIFIED:** HTML and MDN define Worker `terminate()` as immediate termination without an opportunity to finish. The call itself supplies no native-child or OS acknowledgement. CSP `sandbox` without `allow-same-origin` gives an opaque origin, but does not provide CPU/memory quotas or prove hostile code can always be interrupted. [HTML worker model](https://html.spec.whatwg.org/multipage/workers.html), [Worker.terminate](https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate), [CSP sandbox](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/sandbox).

**Reuse:** browser transactions only for local atomic metadata, paired with explicit export and eviction recovery. Retain opaque-origin isolation as a constraint, not a selected stack. Keep `worker_termination_action_acknowledged` distinct from OD-12 proof.

## 3. Red-team corrections

1. **Continuity:** the previous atomic update made records agree on parent `676cc03`, but branch HEAD was `dcf76c8`. A coherent stale snapshot is still stale. This pass records its verified start parent and requires a fresh branch fetch on every resume.
2. **Event trust:** CloudEvents `source+id` is deduplication identity, not authentication. A digest is useful only when recomputed over trusted canonical bytes. Require producer authentication and scope binding.
3. **Storage durability:** IndexedDB transaction completion and WebKit persistence do not establish independent backup or guaranteed survival of shutdown, eviction, power loss or device loss. Require explicit export and recovery tests.
4. **Termination:** Worker `terminate()` is a stop action, not proof of native child exit or OS teardown. Keep the narrow acknowledgement and require execution-model-specific OD-12 authority.

## 4. Maintenance, versions, licences and reuse boundary

| Source | Checked 2026-11-13 | Licence / reuse |
|---|---|---|
| AWS Prescriptive Guidance | Official current guidance opened; no version number surfaced | Pattern reference; no sample copied |
| CloudEvents | Core v1.0.2 latest released; next is WIP; CNCF graduated | Apache-2.0 repo; envelope pattern only |
| RFC 8785 / RFC 9421 | June 2020 Informational / February 2024 Standards Track | Standards referenced; no code copied |
| etcd | Versioned v3.5 docs; docs list newer v3.6-v3.8; releases page surfaced v3.6.15 | Apache-2.0; fencing concept only |
| PostgreSQL | Current docs PostgreSQL 18 | PostgreSQL License; no code copied |
| SQLite | Official site lists 3.54.1 (2026-10-16) | Core code public domain; no code copied |
| WHATWG / HTML | Living standards; Storage last updated 2026-10-19 | Standards references |
| WebKit | Storage post dated 2023-08-10 | Documentation reference; target device still required |
| MDN | IndexedDB, Worker and CSP pages opened | MDN content CC BY-SA 2.5; paraphrased with links |

No source code or substantial documentation text was transplanted. No runtime, provider, database, transport, storage engine or host is selected. D-004 and $0 constraints remain unchanged.

## 5. Acceptance packet

- **Grant:** crash before/after commit, publish duplicate, out-of-order event, equal-progress no-op, version mismatch, restore sequence reuse, stale lease ack and stale fence write.
- **Producer/inbox:** wrong/revoked key, wrong tenant/source/grant/attempt, modified canonical bytes, duplicate ID, same ID/different digest, replay, sequence gap, crash between inbox and state writes.
- **Browser:** shared-origin read, opaque-origin denial, CSP regression, quota/persist failure, eviction, shutdown mid-transaction, export restore, corrupt artifact digest.
- **Lifecycle:** Worker stop without child exit, child/wrapper disagreement, timeout/cancel race, missing policy barrier, cleanup unknown, unacknowledged transport cancellation, no client ack, wrong artifact digest/version/range.

These are future model/adapter acceptance candidates, not canonical LOOP/CASE changes. CASE-04 remains INCOMPLETE / timed_out. Research complete; code/tests NOT RUN; P39 implementation/adapter gate CLOSED.
