# NEXT TASK: PocketCode

## Goal
Close the highest-value model-level evidence gaps without reopening P39 adapter conformance or changing the $0/provider-neutral product constraints.

## Ranked gaps and decisions (2026-11-15)
1. **Receipt snapshot provenance and freshness — critical.** The prior `JournalReceiptSnapshot` uses a frozen dataclass plus a module-global sentinel. Python documents that frozen dataclasses only emulate immutability; the sentinel is importable and can be supplied by caller code. The public receipt API accepts a detached snapshot, so an older snapshot can omit a conflict appended before receipt creation. Decision: treat current seal only as an accidental-misuse check, not authentication. Preferred model API: accept the exact `EventJournal` instance and derive the snapshot inside `create_receipt`; do not accept detached snapshots as receipt provenance. Preserve journal-global observation/accepted-event high-waters and exact effect/attempt conflict refs.
2. **Exact-tree CI — critical for evidence integrity.** Actions run #63 (`43627117644`) reports SUCCESS and 266/266, but its job checked out fixed historical SHA `319cffef121e327331aeaff59522ae279b112ecc`, not the push SHA. Decision: do not count it as evidence for snapshot or grant source commits. Workflow changes were not authorized; retain the historical lane and prepare a separate current-head lane proposal.
3. **Grant transition/outbox replay semantics — high.** The model updates aggregate/event/outbox together only at one in-memory commit point. It does not prove crash durability, sender retries, or consumer atomicity. Decision: test deterministic model semantics only; leave relay leases/fences and inbox persistence gated.
4. **Producer trust and journal concurrency — high, adapter-gated.** `AuthenticatedProducer` is an input assertion, not signature verification. Snapshot methods have no demonstrated lock/transaction around multi-field reads. Decision: no cryptographic or concurrency guarantees in this model; specify them as adapter obligations and avoid PASS claims.
5. **Lifecycle/termination and report projection — high but gated.** Wrapper termination is not native-child/renderer teardown proof; report format 1 remains unchanged until a separately approved format-2 migration. CASE-04 remains INCOMPLETE / timed_out.

## Research: primary sources opened (2026-11-15)
| Topic | Verified source findings | Maintenance / licence | PocketCode disposition |
|---|---|---|---|
| GitHub Actions checkout | GitHub says a push event's `GITHUB_SHA` is the tip commit pushed to the ref; checkout defaults to that triggering SHA when no alternate ref is supplied. `actions/checkout` currently lists v7.0.1 as latest and its repository licence is MIT. | Official workflow docs and action release/changelog were current when checked; MIT. | Keep the explicit historical P40 checkout only as a historical lane. Add a separate current-head lane using the event SHA only after workflow-edit authorization. No action upgrade or workflow edit in this pass. |
| Python dataclasses | Python docs explicitly state frozen dataclasses cannot be truly immutable; `frozen=True` emulates immutability by adding setter/deleter guards. | Official Python 3.15 docs; no dependency adopted. | Do not use `frozen=True`, underscore names or a module sentinel as authentication, provenance or unforgeability. |
| CloudEvents | Core spec requires `source` + `id` uniqueness for distinct events; the same pair may be reused on redelivery so consumers can detect duplicates. Latest published core specification shown is v1.0.2; working draft exists. | Official spec repo/release page opened; licence not confirmed in this research, so no spec text or code copied. | Existing source-scoped producer event identity is directionally consistent. Preserve the exact source+event ID key; treat changed payload/producer/scope under that identity as a conflict, not a duplicate. |
| AWS transactional outbox | AWS guidance identifies the dual-write failure, recommends writing aggregate and outbox in one transaction, idempotent consumers for duplicates, and publication in aggregate-update order. Official sample demonstrates relational outbox and CDC variants. | AWS sample README states MIT-0, but its reference deployment uses CloudFront/WAF/ALB/ECS/Fargate/SQS and is not a $0 PocketCode option. | Reuse the pattern only: one commit point, deterministic sequence, at-least-once send, stable dedupe, ordered relay. Do not copy its infrastructure or select AWS. |
| Temporal retries | Temporal docs describe the lost-completion-ack case: an Activity may complete but be retried if the Worker crashes before reporting completion; external side effects need stable idempotency keys. | Official docs repo is MIT and GitHub showed it updated 2026-11-11. Temporal is a reference, not a proposed dependency. | Preserve stable event/effect/attempt identity and explicit retry/replay tests. Do not add Temporal or adopt its runtime. |

## Red-team findings and corrections
- **Mistake 1 — false strength claim:** the previous pass described a module-private sentinel as rejecting forged snapshots. It rejects only ordinary constructor calls with a missing field; the sentinel is importable (`event_journal._JOURNAL_SNAPSHOT_SEAL`). Correction: this is not a trust boundary; direct journal-derived receipt construction is the preferred next model fix.
- **Mistake 2 — stale snapshot timing omitted:** the previous pass proved that a snapshot object itself does not change after later appends, but did not test whether a stale snapshot could be used to create a receipt after new evidence exists. Correction: add a test that captures a snapshot, appends a scoped conflict, then attempts receipt creation using the old snapshot; desired API must derive fresh evidence and include the new sequence (or explicitly reject stale snapshot).
- **Mistake 3 — CI success overstated:** the prior summary highlighted 266/266 without foregrounding that workflow run #63 checked out SHA `319cffef`, not the triggering SHA `9f0ade8`. Correction: the result is historical P40 verification only; all snapshot/grant changes after that pin remain NOT RUN on their exact tree.
- **Mistake 4 — stale durable ledger:** STATE/NEXT_TASK/CHECKPOINT referenced three different heads and contained a literal escaped-newline artifact. Recovery commit `0807077` records the intervening commits and paths; this pass corrects the stale CI/head claims and replaces the malformed NEXT_TASK content.

## Exact regression packet (model-only; no canonical LOOP/CASE ID changes)
### Receipt/journal
- `test_receipt_creation_derives_snapshot_from_live_journal`: append accepted seq 1, append conflict seq 2, create receipt from journal; expect observation high-water 2, accepted high-water 1, conflict refs `(2,)`.
- `test_receipt_includes_conflict_arriving_after_detached_snapshot`: capture a snapshot, append same-attempt conflict, attempt to create a receipt with the old snapshot; detached snapshot must be rejected or fresh state must be derived; expected receipt must not omit seq 3.
- `test_receipt_conflict_refs_are_exact_effect_attempt`: append conflict for effect A/attempt A and effect B/attempt B; receipt A includes only A's conflict refs while high-waters remain journal-global.
- `test_receipt_snapshot_highwaters_are_consistent`: accepted-event high-water never exceeds observation high-water; bools are rejected as integers; captured conflict refs are ordered, unique, positive and not above the captured observation high-water.
- `test_receipt_successor_binds_late_conflict_without_mutating_predecessor`: late conflict creates version N+1; predecessor fingerprint and conflict tuple remain unchanged.
- `test_receipt_api_rejects_detached_snapshot_or_scalar_claims`: no public receipt path accepts a caller-created snapshot or user-supplied watermark/ref tuple as provenance.
- `test_snapshot_capture_is_atomic_under_concurrent_append`: if concurrent behavior is claimed, coordinate append and snapshot with a lock/transaction; assert the snapshot is a coherent prefix. If not supported, explicitly mark EventJournal not thread-safe and keep adapter locking obligation.
### Grant/outbox
- `test_identical_transition_is_semantic_noop`: same aggregate state/version and same canonical payload do not add event or outbox rows.
- `test_changed_transition_advances_once_and_emits_matching_event`: one legal change increments aggregate version once; event sequence/version/payload digest match; outbox contains one corresponding record.
- `test_duplicate_delivery_is_idempotent`: send the same source+event ID and exact bytes twice; consumer applies the effect once and returns the original disposition.
- `test_same_identity_changed_digest_quarantines`: same source+event ID with different canonical bytes/digest is a conflict; consumer state and accepted-event watermark do not advance.
- `test_future_or_out_of_order_version_does_not_mutate_consumer`: future version is buffered/rejected according to the explicit contract; stale duplicate is no-op; malformed envelope leaves state unchanged.
- `test_lost_delivery_ack_replays_same_outbox_identity`: retry publication with the same stable outbox event identity; do not mint a second aggregate transition or new logical event.
- `test_outbox_order_tracks_aggregate_order`: deliver version N+1 before N and verify the consumer does not apply an invalid transition or silently skip N.

## CI evidence and authorization boundary
- Run #63: SUCCESS, 266/266, Python 3.12.16 / Ubuntu; the job's checkout step used historical SHA `319cffef121e327331aeaff59522ae279b112ecc`. This is NOT current-head verification.
- Latest branch before this pass's checkpoint commits was `15ea602a5264a2878d78d65eb78c7b2c7086b898`; it had zero Actions runs and zero status contexts. Local test execution was previously blocked by DNS failure.
- Do not change `.github/workflows/pocketcode-python-tests.yml` without separate authorization. Proposed design only: keep a pinned historical P40 job and add a second exact-trigger-SHA job for focused and full suites; report both SHAs independently.

## Completed this pass
- Recovered the interrupted checkpoint after checking the latest 10 commit messages and aggregate changed-path set.
- Opened primary sources from GitHub Actions, Python, CloudEvents, AWS and Temporal; checked available release/maintenance and licence evidence; copied no code.
- Corrected the false security and CI claims in the durable state and task records.
- No source/test, workflow, provider, runtime, adapter, device, PR, infrastructure, budget or canonical acceptance IDs changed.

## Constraints carried forward
- $0; preserve D-005/D-006, phone-first, explicit paste/import, default-deny, disposable externally constrained untrusted execution, and provider neutrality.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. PocketCode remains the adopted project name; PoCo is not adopted.
- P39 implementation/adapter conformance CLOSED; CASE-04 INCOMPLETE / timed_out; report format 1 retained; successful Pyodios `summary.json` preserved.
- No workflow edits, adapter/provider integrations, device/browser acceptance, deployments, secrets, PR #2/#3/#4 changes or artifact reruns.
