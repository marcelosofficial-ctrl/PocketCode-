# PocketCode evidence-boundary research and red-team packet
Date: 2026-11-18
Scope: model-level receipt provenance, exact-tree CI evidence, and grant/outbox replay semantics. Research only; no runtime, provider, database, workflow, adapter, or acceptance-gate change.

## Ranked unfinished items

1. **Live-journal receipt provenance and freshness — critical.** A detached snapshot can become stale between capture and receipt creation; the current private sentinel is not authentication. This can make a receipt omit a conflict already present in the journal.
2. **Exact-tree test evidence — critical.** A green historical workflow run is not evidence for later commits. The current workflow's pinned checkout must remain historical-only until an authorized second lane tests the intended current tree.
3. **Outbox/grant replay and ordering — high.** The in-memory model demonstrates a commit point, not durable atomicity, relay retry safety, or receiver-side deduplication.
4. **Producer authenticity and concurrent journal mutation — high, adapter-gated.** AuthenticatedProducer is asserted input; a multi-collection snapshot needs an explicit synchronization contract.
5. **Lifecycle and report projection — high, gated.** Preserve child verdict, job/evidence disposition and artifact disposition separately; keep report format 1 and CASE-04 status unchanged.

## Primary research opened

### Receipt provenance, immutability and concurrency
- Python dataclasses documentation says frozen dataclasses only emulate immutability; truly immutable Python objects are not possible. This confirms that frozen values and module-private sentinels are not provenance or security controls: https://docs.python.org/3/library/dataclasses.html
- CPython thread-safety documentation describes some individual list operations as atomic in current CPython, but traversal methods may be affected by concurrent modification and per-object locks do not create an atomic snapshot across multiple collections: https://docs.python.org/3/library/threadsafety.html
- CloudEvents Core requires producer uniqueness of source + id for distinct events and permits reuse for redelivery; consumers may treat the same pair as duplicates: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- No code or licence text copied. Python/CloudEvents are references, not dependencies. Exact CloudEvents licence was not re-verified in this pass.

### Exact-tree CI and checkout semantics
- GitHub's event documentation says push GITHUB_SHA is the tip commit pushed; for pull_request it is the last merge commit on the PR merge ref. To test only the PR head, use github.event.pull_request.head.sha: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- The GitHub Actions contexts reference identifies github.sha, github.ref, github.event_name and github.head_ref: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts
- actions/checkout README says checkout defaults to the triggering event ref/SHA for the repository that triggered the workflow, and currently documents v7 / Node 24. Its README says the project is not taking contributions but continues security updates; its licence is MIT: https://github.com/actions/checkout/blob/main/README.md
- The action's input metadata independently confirms default ref behavior: https://github.com/actions/checkout/blob/main/action.yml
- Exact latest patch release was not verified; do not infer it from the moving main branch README.

### Outbox and retries
- AWS Prescriptive Guidance says aggregate and outbox writes must share one transaction; consumers must be idempotent because duplicate delivery can occur; notifications must preserve aggregate update order: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Debezium's current Outbox Event Router documentation uses a unique event id for duplicate detection and aggregate id as the message key, which supports partition ordering. Its repository licence is Apache-2.0: https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html and https://github.com/debezium/debezium/blob/main/LICENSE.txt
- Temporal's Activity documentation warns that an Activity may execute multiple times, including partial completion, even though Workflow history observes completion once. Its documentation licence is MIT: https://github.com/temporalio/documentation/blob/main/docs/encyclopedia/activities/activity-definition.mdx and https://github.com/temporalio/documentation/blob/main/LICENSE.md
- These are pattern references only. No AWS, Kafka, Debezium, Temporal, or paid infrastructure is selected or proposed for PocketCode.

## Concrete model correction packet

### A. Journal-to-receipt boundary
1. Replace detached snapshot provenance with a receipt API that accepts the exact EventJournal object and derives the effect/attempt snapshot internally at receipt creation.
2. Reject legacy detached journal_snapshot and caller-supplied scalar watermarks/conflict refs as provenance. Do not treat a module sentinel, underscore name, object identity or frozen dataclass as authentication.
3. If the journal is intended to support concurrent writers, one journal-owned lock must cover every append mutation and the complete snapshot read across observation high-water, accepted-event high-water and exact scoped conflict refs. A lock only around snapshot creation is insufficient if append paths do not use the same lock.
4. If concurrency is not supported, explicitly document EventJournal as single-threaded/not thread-safe and leave synchronization as an adapter obligation. Do not imply CPython list atomicity gives a coherent multi-list snapshot.
5. Keep global high-waters journal-global; keep conflict references exact to EffectId + DispatchAttemptId. Capture once and bind the derived snapshot into the canonical receipt fingerprint. A later conflict requires a successor receipt revision; never mutate a predecessor.
6. Preserve the existing no-journal compatibility path only if zero watermarks are explicitly described as “no journal evidence supplied,” never “proof that no events/conflicts exist.”

### B. Required receipt regressions
- Live journal receipt includes accepted sequence 1 and later same-attempt conflict sequence 2: observation high-water 2, accepted high-water 1, conflict refs (2,).
- Capture a snapshot, append a scoped conflict, then create a receipt: detached snapshot is rejected or fresh journal evidence includes the new sequence.
- Two effects/two attempts: conflict refs include only the exact receipt effect/attempt while global high-waters remain global.
- Reject caller-supplied snapshot and scalar watermark/ref claims.
- Successor revision binds late conflict while predecessor fingerprint and refs remain unchanged.
- Replaying the same revision key after the journal advances conflicts on fingerprint; it must not silently return stale evidence.
- If thread safety is claimed, coordinate append and snapshot with the same lock and test a coherent prefix; otherwise test/document single-thread-only contract.

### C. Exact-tree CI proposal (NOT AUTHORIZED TO IMPLEMENT)
- Preserve the existing historical pinned P40 lane and label its checked-out SHA as historical.
- Propose a separate current-tree lane only after workflow-edit authorization. For push events, test the triggering tip SHA (GITHUB_SHA). For pull_request, decide explicitly whether the lane tests the synthetic merge result (GITHUB_SHA) or PR head (github.event.pull_request.head.sha); record event name, ref, selected SHA and checked-out HEAD in logs/artifacts.
- Fail the lane if checked-out HEAD differs from the selected SHA. Run focused model suites and the full suite on that exact checkout. Report historical and current lanes independently.
- Do not change .github/workflows/pocketcode-python-tests.yml in this pass. A green historical run never upgrades current-source status.

### D. Grant/outbox replay packet
- Keep aggregate transition + event + outbox insertion in one storage transaction in any future durable adapter.
- Stable event identity is source + id (or the existing PocketCode canonical identity); same identity and same bytes is duplicate delivery, same identity with changed digest is conflict/quarantine.
- Preserve aggregate sequence order. A later sequence must not be applied while an earlier required sequence is missing.
- Retry after ambiguous publication reuses the same logical event/effect/attempt identity; do not mint a new logical event merely because acknowledgement was lost.
- Required tests: identical transition semantic no-op; one changed transition creates exactly one matching event/outbox record; duplicate delivery applies once; same identity/different digest quarantines without advancing consumer state; future/out-of-order version does not mutate consumer; lost acknowledgement replays same identity; order N+1 before N cannot silently skip N.
- These tests validate model semantics only. They do not prove crash durability, cross-process fencing, sender lease safety or atomic receiver inbox persistence.

## Red-team corrections to prior project notes and chat claims

1. **Overstatement: “frozen snapshot + private sentinel” rejects forged provenance.** Correction: Python documents frozen dataclasses are only emulated immutability; a module attribute can be imported. Treat the sentinel as an ordinary-misuse guard only.
2. **Missing TOCTOU case: snapshot immutability was mistaken for freshness.** Correction: a snapshot may remain immutable and still be stale when used later. The regression must append a conflict after snapshot capture but before receipt creation.
3. **CI success was too easy to overread.** Correction: run #63's 266/266 result checked out historical SHA 319cffef, not the later source commits. It is historical-only evidence; current source remains NOT RUN.
4. **“Use github.sha” is not a complete PR CI rule.** Correction: for pull_request, github.sha is the synthetic merge commit; use pull_request.head.sha when testing the branch head. State which tree the lane is intended to verify.
5. **Git blob/tree APIs were described too optimistically as patch-capable.** Correction: Git object composition still requires the complete replacement blob. Without a checkout or patch-application interface, reconstructing a large source file from excerpts is unsafe. Do not do it.

## Status and boundaries
- VERIFIED: source pages above were opened in this pass.
- INFERRED: the proposed API/lock boundary is the narrowest safe model-level correction consistent with the observed design; it is not implemented.
- UNKNOWN: exact current runtime/threading deployment semantics, exact latest actions/checkout patch release, and any durable adapter's transaction/isolation behavior.
- NOT RUN: source tests, exact-head CI, device/browser acceptance.
- No source/test/workflow/provider/runtime/adapter changes; no PR edits, merge, deployment, spend, secret changes, or canonical LOOP/CASE/D/OD changes.
- Existing implementation packets for the outbox timestamp guard and live-journal receipt provenance remain separate and must not be duplicated or silently superseded.
