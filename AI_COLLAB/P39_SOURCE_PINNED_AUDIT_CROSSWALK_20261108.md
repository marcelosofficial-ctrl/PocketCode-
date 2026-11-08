# P39 source-pinned audit crosswalk

**Date:** 2026-11-08  
**Scope:** Complete the ChatGPT static audit slice against immutable source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540` and P37 contract semantics.  
**Status:** Documentation and test-design reconciliation only. P39 review gate remains OPEN. No source/test changes or execution occurred.

## 1. Evidence pins and boundaries

- Grant model: `scripts/release_grant_conformance.py`, blob `f9107fe46d60bbb5cd7115daf2513cd751221986`.
- Grant tests: `scripts/test_release_grant_conformance.py`, blob `e3bbe94838807a1f9214042af262a2497c057fd7`.
- Event journal: `scripts/event_journal.py`, blob `371a175739b9cb65cd4d59bb4cd5b3c1c4953564`.
- Event journal tests: `scripts/test_event_journal.py`, read at the same source SHA.
- Concurrency/crash contract: `AI_COLLAB/RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md`, pinned in the P39 documentation snapshot `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0`.
- P39 source audit/addendum and interim reviewer dispositions: `P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md` and `P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md`.

**Evidence rule:** These are VERIFIED properties or omissions of the pinned sequential Python reference models. They are not proof of production exploitability. No durable adapter, concurrent multi-process implementation, grant-event relay or streaming transport is established by these files.

## 2. Finding reconciliation

| Finding | Source-pinned observation | Contract relationship | Disposition |
|---|---|---|---|
| P39-S1 | `record_progress()` (269–293) increments `aggregate_version` and changes progress but appends no `GrantEvent` or `OutboxItem`. Reservation creates only v1 (around 225–240). | P37 §§5 and 8A require atomic state/event/outbox and contiguous per-grant event order. | **ACCEPT, VERIFIED model gap.** Either emit each versioned transition atomically or separate a progress cursor from event aggregate version. |
| P39-S2 | `GrantEvent` (51–59) stores metadata plus a digest string, not canonical payload bytes. `consume_event()` (295–313) compares the supplied digest and does not recompute it. | P37 §5 requires immutable event identity and changed-payload conflict detection. | **ACCEPT, VERIFIED model gap.** Canonicalize all semantic fields, hash inside trusted boundary, and compare canonical bytes/digest. |
| P39-S3 | Grant-event `mark_outbox_delivered()` (315–321) accepts only source/event identity and sets delivered. No relay owner, lease or fence exists in this model. | P37 §§5, 7 and FENCE-02 require fenced relay acknowledgement and at-least-once duplicate handling. | **ACCEPT, VERIFIED model gap.** Add claim/lease/fence and conditional delivered mark. Do not conflate with `fake_outbox.py`, a separate effect-dispatch state machine. |
| P39-S4 | No stream/transport implementation exists in the reviewed source. A worker fence protects later model writes, not bytes already emitted on an open stream. | P37 §6 explicitly says state fencing cannot retract bytes; transport must independently enforce scoped capability/revocation. | **ACCEPT AS BOUNDARY, VERIFIED absence in reviewed scope.** Adapter/transport behavior UNKNOWN. Define chunk/range checks, cancellation acknowledgement, in-flight bound and distinct byte observations. |
| P39-S5 | `consume_event()` does not look up an existing grant or verify tenant/principal/effect/attempt binding. A fabricated next-version event for an unknown grant can be accepted. | P37 §5 requires source-scoped identity, ordered application and grant/event integrity. | **ACCEPT, VERIFIED model gap.** Bind event to an existing grant and tenant/scope; reject or quarantine unknown/cross-tenant/wrong-source events. Distinct from S2: digest-to-metadata integrity does not prove grant authorization/binding. |
| P39-S6 | `event_journal.py` declares producer authentication adapter-supplied. `AuthenticatedProducer` is caller-constructible data; `advance_fence()` and `append()` are separate in-memory operations. | P37 §§2, 5 and 6 require trusted authority and atomic durable fencing where applicable. | **ACCEPT AS ADAPTER OBLIGATION.** The model is explicit about its limit; production authentication and atomic fence+append remain UNKNOWN. |
| P39-S7 | Existing research matrix reuses bare IDs: P39 `RACE-03` means two first-head initializers, while P37 `RACE-03` means concurrent same-key/same-intent requests. P39 `FENCE-02` means expired transfer worker, while P37 `FENCE-02` means stale outbox relay. | P37 and P39 suites must remain independently traceable. | **ACCEPT, VERIFIED traceability collision.** Prefix every P39 adapter test ID with `P39-`; keep canonical LOOP/CASE/D IDs unchanged. Crosswalk below. |
| P39-S8 | Grant stores initial authorization ID/revision. `claim_worker()` (231–268) and `record_progress()` (269–293) do not check current policy revision, revocation epoch, authorization expiry or trusted revocation decision. No revocation transition/interface exists. | P37 §§4, 7 and 9 explicitly leave post-commit/in-flight revocation policy to a separate decision. | **ACCEPT AS OPEN POLICY/MODEL GAP.** Do not assume irrevocable grants or immediate revocation. Define pre-claim, active-stream, takeover and resume semantics before implementation. |

## 3. Test-ID namespace correction

P37 keeps its existing bare identifiers unchanged. All P39 additions use the `P39-` prefix. This prevents accidental collisions and does not alter canonical LOOP/CASE/D identifiers.

| Earlier P39 label | Correct P39 label | Purpose |
|---|---|---|
| RACE-03 (two first-head creators) | P39-RACE-03 | Concurrent initial head/receipt bootstrap |
| FENCE-02 (expired transfer worker) | P39-FENCE-02 | Expired transfer worker stale-write attempt |
| EVENT-01..04 | P39-EVENT-01..04 | Atomic version/event/outbox; canonical digest; identity binding; unknown/cross-tenant/wrong-source rejection |
| OUTBOX-01..03 | P39-OUTBOX-01..03 | Fenced relay; duplicate publication; ordered gap resolution |
| STREAM-01..02 | P39-STREAM-01..02 | Open-stream revocation/cancellation; distinct byte observations |
| RECOVERY-01 | P39-RECOVERY-01 | Durable rebuild without gaps or duplicate logical effects |
| POLICY-02..04 | P39-POLICY-02..04 | Post-commit revocation before claim, during stream, and resume after takeover |
| STREAM-01..03 (new refinement) | P39-STREAM-01..03 | Stale chunk rejection; unacknowledged cancellation remains incomplete; four byte counters remain distinct |

The last row refines the earlier two STREAM cases. Merge overlapping assertions rather than creating duplicate test executions. P39-STREAM-01..03 are the canonical P39 names for the refined transport slice.

## 4. Exact test obligations by model finding

- **P39-S1:** reserve v1, record multiple progress transitions, verify every externally versioned transition has one immutable event/outbox row; verify consumer rebuild and crash atomicity. If progress is intentionally coalesced, test the separate cursor and event version independently.
- **P39-S2:** replay same source/event ID and digest while mutating grant ID, version, state and event type; reject. Also reject a first-delivery arbitrary digest inconsistent with canonical bytes.
- **P39-S3:** relay A claims and publishes; lease expires; B takes over and marks delivered; A's late mark must fail. Crash after publish/before mark may redeliver but must create one logical consumer effect.
- **P39-S4 / S8:** test revocation between bounded chunks, cancellation requested but not acknowledged, connection loss, resume under a new fence, old capability rejection and late acknowledgement from an old stream. Record transport-accepted, emitted, client-observed and client-acknowledged bytes separately.
- **P39-S5:** reject unknown grant, cross-tenant grant reference, wrong source, mismatched effect/attempt and metadata changed under reused event identity.
- **P39-S6:** prove adapter authenticates issuer/subject/key/audience/source and revocation status before constructing trusted producer context; prove fence validation/advance and append are atomic in the chosen durable adapter.
- **P39-S7:** automated traceability check must reject duplicate bare IDs across P37/P39 suites and require explicit namespace prefixes.
- **P39-S8:** owner must choose post-commit policy. Tests assert the chosen policy at grant commit, before worker claim, during transfer, after takeover and on retry/resume. No test may infer the policy from idempotent grant recovery.

## 5. Existing coverage and non-coverage

**VERIFIED existing sequential coverage:** tenant/principal/request-key idempotency namespace; unauthenticated replay rejection via the supplied false allow value; same-key stable-intent replay after receipt successor; sequential stale-head rejection; progress monotonicity/bounds; stale worker state-write rejection; event-journal payload-byte duplicate detection; source-scoped journal identity; sequential fence checks.

**VERIFIED missing from the reviewed model/tests:** aggregate version/event parity after progress; digest recomputation from event metadata; grant/tenant binding in grant-event consumer; grant-event relay lease/fence; post-commit policy revocation; stream transport enforcement; cryptographic producer authentication; atomic durable fence+append; true concurrent first-head creation; process restart durability.

**NOT RUN:** no tests were executed during this audit unit. The earlier 266/266 result remains tied to source/test SHA `744cb4d`, not a fresh run on current documentation HEAD.

## 6. Reviewer reconciliation template and gate

For every Claude/Gemini finding, record: reviewer ID and exact quoted claim; pinned file/line/blob; independent reproduction or counterexample; relationship to P37; overlap with P39-S1..S8; disposition (**ACCEPT / REJECT / NEEDS-OWNER**); required test ID using the P39 namespace; owner decision; implementation gate status.

P39 remains **OPEN**. Claude's committed report reviewed the research packet only. Gemini's supplied plan is not a complete independent source-pinned P39 report. Neither is represented here as having completed the source/model review. Do not edit source/tests, select an adapter/provider/database/runtime, or close the gate until both independent reviews and owner decisions are reconciled.
