# PocketCode: Evidence Boundary and Replay Design — 2026-11-15

## Purpose and scope

This is a model-level engineering decision record for the active branch `pocketcode-ai-workflow-director-research-2026-10-28`. It does not select a runtime, provider, database, transport, storage engine or host. It does not reopen P39 adapter conformance, change acceptance IDs, or authorize workflow, PR, device, deployment or infrastructure work. Budget remains $0.

Evidence labels: **VERIFIED** means the cited primary source was opened or the stated repository ref/API response was read; **INFERRED** means a design consequence; **UNKNOWN** means not established.

## Ranked gaps

1. **Receipt provenance/freshness (critical).** A receipt can be constructed from a detached snapshot captured before a later journal conflict. The private sentinel and frozen dataclass do not establish authenticity or freshness.
2. **Exact-tree verification (critical).** A green historical run cannot establish that current source and tests execute together.
3. **Grant/outbox replay (high).** In-memory atomicity does not establish crash durability, retry safety, deduplication or ordering across processes.
4. **Journal trust/concurrency (high).** Producer identity is supplied model input; a coherent snapshot under concurrent append is not established.
5. **Lifecycle/termination (high, gated).** Supervisor termination is not native child/renderer teardown proof. Keep report format 1 and CASE-04 unchanged.

## Research findings and adoption decisions

### 1. Receipt freshness and snapshot authority

- **VERIFIED — Python 3.12 documentation:** `frozen=True` emulates read-only behavior; Python explicitly says truly immutable dataclass instances are not possible. This is a mutation-resistance convenience, not an authenticity primitive.
- **VERIFIED — CloudEvents specification repository:** the currently opened `main` specification identifies itself as **1.0.3-wip**. It requires the producer to make `source + id` unique for each distinct event and allows the same pair on redelivery. The opened page is a working draft, not a pinned released dependency; PocketCode should pin a released spec version in any future conformance document rather than silently tracking `main`.
- **INFERRED — decision:** receipt evidence must be captured from the exact live journal at the receipt operation's linearization point. A module-private object, constructor guard, frozen value or caller-supplied tuple is not proof that evidence came from the authoritative journal.

**Target contract**
- Public receipt creation accepts the exact `EventJournal` object, not `JournalReceiptSnapshot`, a serialized snapshot, a seal or caller-supplied high-water/conflict claims.
- Inside the receipt-creation critical section, the journal captures one coherent immutable value: global observation high-water, global accepted-event high-water, exact effect/attempt conflict sequence references, and the journal identity/scope needed by the model.
- Validate: all sequence values are positive non-bool integers; accepted high-water is no greater than observation high-water; conflict refs are ordered, unique and no greater than observation high-water; effect and attempt match the requested receipt scope.
- Receipt fingerprint binds the derived snapshot values. A later append does not mutate the predecessor; it is visible to a successor receipt.
- If the journal is deliberately single-threaded, state that explicitly and make serialized access an adapter obligation. If concurrent use is supported, append and snapshot capture must share one lock/transaction. Do not claim both without a test.

**Required regressions**
1. Append accepted event seq 1 and scoped conflict seq 2; create receipt from live journal; assert observation high-water 2, accepted high-water 1 and scoped refs `(2,)`.
2. Capture an old snapshot, append scoped conflict seq 3, then attempt receipt creation from old snapshot; reject detached input or derive fresh live evidence. The result must not omit seq 3.
3. Append conflicts for two effect/attempt pairs; each receipt includes only its exact pair's refs while journal-global high-waters remain global.
4. Create successor after a late conflict; predecessor fingerprint/refs remain unchanged and successor includes the conflict.
5. Reject bools, zero/negative refs, duplicates, unsorted refs and refs above the observation high-water at the validation boundary.
6. If concurrency is supported, use a barrier-controlled append/snapshot test and prove the snapshot is a coherent prefix. Otherwise test/document the non-thread-safe contract.

### 2. Exact-tree CI

- **VERIFIED — GitHub Actions event documentation:** for `push`, `GITHUB_SHA` is the tip commit pushed to the ref. The workflow must deliberately override checkout if it intends to test another revision.
- **VERIFIED — repository evidence:** recorded run #63 reports 266/266 but checked out historical SHA `319cffef121e327331aeaff59522ae279b112ecc`; it does not test the newer snapshot/grant commits. Pass-start HEAD `050958e41fea27f059e41d81f8e3497efe9ed537` has no associated workflow run or status context.
- **INFERRED — decision:** preserve the pinned historical P40 lane as historical evidence. If owner later authorizes workflow changes, add a separate current-push lane whose checkout SHA is the event SHA and whose output prints source SHA, test SHA, Python version, command and totals. Never combine the two lanes into one PASS label.
- **NOT AUTHORIZED:** no workflow file edit in this pass.

### 3. Grant/outbox retries and delivery

- **VERIFIED — AWS Prescriptive Guidance:** the transactional outbox addresses the dual-write gap by committing business state and the outbox record together. It explicitly warns of duplicate notifications and recommends idempotent consumers and preserving update order. Its service-specific examples are not a PocketCode dependency recommendation.
- **VERIFIED — Temporal documentation:** Activities may execute more than once when a worker completes an operation but crashes before reporting completion. The docs recommend idempotent Activities and stable idempotency keys. Temporal is a pattern reference only.
- **VERIFIED — CloudEvents draft:** source plus event ID is the event identity; same identity on redelivery is duplicate detection, not permission to accept changed bytes.
- **INFERRED — decision:** preserve one stable logical event identity across delivery retries. A retry must not mint a second aggregate transition. Exact duplicate bytes return the original disposition; same identity with changed canonical bytes is a conflict. Consumers must not advance state on malformed, future, out-of-order or identity-conflicting input.

**Required model regressions**
- Identical transition: no aggregate version change, event or outbox row.
- Changed legal transition: exactly one version advance and one matching event/outbox record.
- Same source+event ID and same canonical bytes twice: one state application; second delivery returns original disposition.
- Same source+event ID with changed canonical bytes/digest: quarantine/conflict; no state or accepted-watermark advance.
- Future/out-of-order version: no silent skip; behavior follows explicit buffer/reject contract.
- Lost delivery acknowledgement: retry same outbox identity; no second logical event.
- Deliver N+1 before N: consumer does not apply an invalid transition or silently skip N.

**Boundary:** these are deterministic model semantics. Durable transactionality, sender leases/fences, crash recovery and consumer inbox atomicity remain adapter obligations and are not proven by this model.

### 4. Producer trust and concurrency

- **VERIFIED — source/model ledger:** `AuthenticatedProducer` is supplied input, not cryptographic verification. No producer signature/key verification has been established.
- **INFERRED — decision:** name the field as an assertion/claim at this layer; do not call it authenticated identity unless a trusted adapter verifies it. Bind verified principal, key/version, scope and authorization decision in a future adapter receipt. Reject replayed or revoked authority at the enforcement boundary.
- **UNKNOWN:** whether concurrent journal access is required by the current execution topology. Until decided and tested, claim no thread-safety or atomic snapshot behavior.

### 5. Lifecycle and termination

- **VERIFIED — existing project ledger:** wrapper termination currently proves the supervisor called `terminate()` on its Worker and closed the channel; it does not prove native child exit or OS/renderer teardown.
- **INFERRED — decision:** keep execution outcome, job/evidence disposition, artifact disposition and termination proof separate. A timeout/cancel/rejection/infrastructure error cannot be overwritten by a nonzero integer exit in a later report projection. Do not change format 1 without a separately approved migration and compatibility tests.
- **UNKNOWN:** authoritative platform-level child/renderer termination proof for the future runtime. CASE-04 remains INCOMPLETE / `timed_out`; P39 implementation/adapter conformance remains CLOSED.

## Red-team corrections to prior work

1. **Sentinel overstated:** a module-private sentinel is importable by code with module access. It can catch accidental construction only; it is not an authenticity boundary. Corrected design: accept the live journal and derive the snapshot internally.
2. **Freshness omitted:** proving that a snapshot object stays unchanged after append does not prove that a receipt created later from that snapshot is fresh. Added the stale-snapshot-after-conflict regression above.
3. **CI success overstated:** 266/266 was a successful historical-checkout run, not verification of the later source tree. Corrected classification: historical PASS only; exact current tree NOT RUN.
4. **Repository-wide commit search misattributed:** a global commit search returned an older commit from a different history line. Only the branch-specific ref and branch-scoped commits establish the active branch head. Discarded the global result as branch evidence.
5. **Draft spec version risk:** the opened CloudEvents `main` page is labelled 1.0.3-wip. Do not cite it as a released 1.0.3 conformance baseline; pin a released version before adopting conformance language.

## Source register (opened 2026-11-15)

- Python 3.12 dataclasses: https://docs.python.org/3.12/library/dataclasses.html — official language documentation; opened. No Python implementation code copied.
- CloudEvents specification: https://github.com/cloudevents/spec/blob/main/spec.md — official project repository; opened; page identifies itself as 1.0.3-wip. Used for event identity semantics only; no code copied. Release/licence details for this draft were not relied on.
- AWS transactional outbox: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html — official AWS guidance; opened. Pattern only; no AWS service or sample adopted.
- Temporal error handling/idempotence: https://github.com/temporalio/documentation/blob/main/docs/best-practices/error-handling.mdx — official documentation repository; opened. Pattern only; no Temporal dependency or code adopted.
- GitHub Actions event semantics: https://github.com/github/docs/blob/main/content/actions/reference/workflows-and-actions/events-that-trigger-workflows.md — official GitHub documentation source; opened. Used to define current-push SHA verification. No workflow changed.
- actions/checkout: https://github.com/actions/checkout — official action repository surfaced in search. Release/version and licence were not independently pinned in this pass; no upgrade or code copied.

## Current evidence ledger

- **VERIFIED:** active branch head at pass start was `050958e41fea27f059e41d81f8e3497efe9ed537`; latest five branch commits are `050958e`, `7267c53`, `a786a2b`, `b882acb`, `041b136`.
- **VERIFIED:** pass-start exact-head combined status had no contexts; associated workflow-runs query returned no runs.
- **NOT RUN:** exact-head tests and CI.
- **NOT IMPLEMENTED:** live-journal receipt API change and new regressions. GitHub write interface still requires complete-file replacement; no safe bounded patch route or local network-capable execution path was established. Large source/test files were not rewritten.
- **UNCHANGED:** P39 adapter gate CLOSED; CASE-04 INCOMPLETE / `timed_out`; report format 1; $0; provider-neutrality; explicit paste/import; all LOOP/CASE/D/OD IDs; PRs and workflows untouched; Pyodios `summary.json` preserved.

## Next implementation contract

The next source pass should be limited to `scripts/event_journal.py`, `scripts/result_receipts.py` and `scripts/test_result_receipts.py`. First establish a safe patch/local execution path. Then implement the live-journal API, add the six receipt regressions, run focused tests and the full suite on the exact commit, and only then update STATE/NEXT_TASK. Do not expand to grant, adapters, workflow, lifecycle or device work until that receipt slice has exact-tree evidence.
