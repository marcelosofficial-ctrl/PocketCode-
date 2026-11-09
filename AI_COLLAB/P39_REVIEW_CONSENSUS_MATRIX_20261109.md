# P39 independent-review consensus and conflict matrix

**Date:** 2026-11-09  
**Status:** WORKING RECONCILIATION / OWNER GATE OPEN  
**Pins:** Gemini and Claude source review target source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`; supplemental `scripts/result_receipts.py` blob `0d1588f8590b57e0bf7447c7d5c519186ff0f39d`.  
**Authority:** this matrix reconciles review claims. It does not authorize code, amend canonical LOOP/CASE/D IDs, or adopt owner recommendations.

## 1. Consensus matrix

| Topic | Claude P39 position | Gemini position | Reconciled disposition | Layer / priority | Tests / owner gate |
|---|---|---|---|---|---|
| Aggregate version, progress and event/outbox parity | RG-B1 / C1: no-op progress advances version; progress has no matching event/outbox; terminal transitions incomplete | S1 agrees in principle but names `event_journal.py` and describes crash between DB writes | **ACCEPT WITH CORRECTION.** Actual gap is in `release_grant_conformance.py`; `event_journal.py` is an in-memory append-only journal and has no aggregate/outbox. Do not claim a database crash was observed. | Model defect, BLOCKING | P39-EVENT-05 |
| Canonical event digest | RG-B2 / C2: same digest with altered metadata and forged first delivery can be accepted | S2 alleges `result_receipts.verify_receipt()` hashes payload only | **ACCEPT WITH CORRECTION.** Gemini's named function does not exist in the checked receipt module. The grant consumer's `consume_event()` trusts the supplied digest instead of recomputing canonical semantic bytes. Keep receipt integrity and event-envelope integrity distinct. | Model defect, BLOCKING | P39-EVENT-06 |
| Event-to-grant / tenant / source binding | RG-B2 and P39-S5: unknown grant/source and cross-scope binding are not sufficiently checked | Gemini flags caller-supplied producer/principal identity and tenant isolation | **ACCEPT.** Digest integrity is not authentication or authorization. Consumer must bind to an existing tenant-scoped grant, expected source, effect and attempt. Producer identity verification belongs at trusted adapter ingress. | Model + adapter, HIGH | P39-S5; P39-EVENT-06 |
| Grant-event relay ownership, lease and ordering | RG-H1 / C3: delivered marker has no relay claim/fence/order | S3 claims `fake_outbox.py` lacks lease/fence | **ACCEPT WITH CORRECTION.** The claim about `fake_outbox.py` is contradicted by its lease expiry and monotonic fence. The separate grant-event relay in `release_grant_conformance.py` lacks relay claim/fence/order. | Model defect, HIGH | P39-OUTBOX-04/05 |
| Lease clock authority | RG-B3 / C4: caller-supplied `now` can steal/extend a lease | Gemini says fake outbox lacks wall-clock lease expiry | **ACCEPT WITH CORRECTION.** Correct defect is caller-controlled time in grant model and missing grant-event relay lease. FakeOutbox has lease expiry. Use authority-owned time; retain worker time only as an untrusted observation. | Model oracle + adapter, BLOCKING | P39-CLOCK-01 |
| Grant/event IDs and restore continuity | RG-H4 / C5: process-local grant counter repeats across fresh instances | Gemini says event IDs are random UUIDs and restore can reset fences | **ACCEPT PARTIALLY.** Grant-ID reuse is Claude-reported and model-level. Gemini's UUID assertion is unsupported by the reviewed grant model. Restore-safe fence high-water is an adapter obligation; restore behavior is not implemented or tested in the in-memory model. | Model + adapter, HIGH | P39-ID-01 |
| Producer authentication and journal fencing | P39-S6: caller-constructible producer and separate fence/append are explicit model limits | Gemini flags unverified caller-supplied principal headers | **ACCEPT AS ADAPTER OBLIGATION.** Authenticate issuer/subject/audience/source and atomically check fence with append in the chosen durable adapter. Do not pretend the sequential journal authenticates credentials. | Adapter, HIGH | P39-JOURNAL-01 if journal contract requires it |
| Poison predecessor and event gaps | RG-O6: permanent missing/malformed predecessor can block later versions | Gemini says out-of-order events are dropped | **ACCEPT WITH CORRECTION.** The grant consumer returns `deferred_gap`, not silent drop. Durable bounded quarantine, HOLD, operator visibility and audited repair remain unspecified. | Model/operations contract, HIGH | P39-ORDER-04 |
| Idempotency key / changed request payload | RG-O3: immutable client intent and same-key replay ordering need clarification | Gemini's req_101 example says changed payload under same ID returns old result | **REJECT GEMINI'S EXAMPLE FOR THESE TARGETS.** FakeOutbox compares request fingerprint and immutable request bytes; grant reservation binds principal/tenant/request key and immutable intent. Keep RG-O3's narrower server-resolved-head replay question open. | Model contract, MEDIUM | P39-IDEMP-01 |
| Receipt-head identity and digest binding | RG-O1/O2/O4: historical receipt ID reuse, compact head digest/quarantine contract and vacuous assertion | Gemini's receipt verifier claim is misattributed | **ACCEPT CLAUDE'S NARROW FINDINGS; REJECT GEMINI'S NAMED EXPLOIT.** Resolve compact head against the canonical receipt contract. The supplemental receipt source was checked outside Gemini's six-file manifest. | Model/test contract, MEDIUM | P39-RACE-06B; P39-RECEIPT-01; P39-TEST-HYGIENE-01; OD-08 |
| Pre-commit authorization revocation | RG-H3: allow snapshot may become stale before grant commit | Gemini's secondary report does not establish this exact race | **RETAIN CLAUDE FINDING WITH OWNER/ARCHITECTURE QUALIFICATION.** Define policy epoch/linearization; do not claim atomicity across independent authorities without proof. | Owner policy + adapter, HIGH | P39-POLICY-05; OD-05 |
| Post-commit revocation, takeover and resume | P39-S8 / RG-H2: grant recovery is not byte authorization; active transfer needs separate policy | S4: DB fence does not close open streams | **ACCEPT AS POLICY/ADAPTER BOUNDARY, NOT SEQUENTIAL MODEL DEFECT.** Revalidate current policy before claim/resume. If streaming is in MVP, require active transport cancellation and acknowledgement. | Owner + adapter, HIGH / conditional | P39-POLICY-02..04; P39-STREAM-01..03; OD-01..04 |
| Client receipt of bytes | RCP-04: server progress/digest does not prove client receipt | S4 secondary claim says residual buffers may reach client after cancellation | **ACCEPT LIMITATION.** Separate staged, transport-accepted/emitted, client-observed and client-acknowledged counters. Client acknowledgement alone proves client-confirmed receipt. | Owner + adapter, conditional | OD-13; P39-STREAM-01..03 |
| Exit provenance and termination | Existing EP crosswalk and static audit define child/wrapper/termination distinctions; additional Claude EP artifact not yet inspected | Gemini flags open sockets and post-revocation buffers | **KEEP SEPARATE.** A transport concern does not resolve EP-04/05/18/21/24. Typed coordinator projection, termination acknowledgement and cleanup evidence remain owner-dependent. | Model contract + adapter + owner | EP-01..25; OD-09..12; CASE-04 unchanged |
| Event parent/root chain | No independently confirmed defect in the Claude reconciliation | Gemini says UUIDs are not bound to aggregate version/parent IDs | **UNCONFIRMED SPEC QUESTION.** Existing grant event identity is deterministic by grant/version; no cryptographic root-chain requirement has been accepted. Do not promote this claim to a defect without a pinned contract requirement. | Specification question | No new ID until required semantics are agreed |
| Cross-process, crash and restore proof | Claude's model tests do not prove durable atomicity; C1-C7 were on byte-identical copy | Gemini all tests NOT RUN | **NOT PROVEN.** Sequential model tests, even if rerun, cannot establish two-process races, real crash rollback, durable relay or restore behavior. | Adapter acceptance | Exact-SHA unit suite plus separately designed fault/concurrency/restore tests |

## 2. Evidence quality and scope limits

- **VERIFIED STATIC:** the six Gemini-pinned source/test blobs at SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`; supplemental receipt module blob `0d1588f8590b57e0bf7447c7d5c519186ff0f39d`.
- **CLAUDE-REPORTED VERIFIED-BY-RUN:** C1-C7 against a byte-identical copy under Python 3.12.3/Linux. This reconciliation did not rerun them or independently reproduce the output.
- **NOT RUN:** Gemini's test matrix, full repository suite in these review passes, device tests, live provider tests, concurrent durable adapter tests, streaming transport tests and backup/restore tests.
- **Historical PASS:** Actions run 42365455316, 266/266, applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- **UNKNOWN:** production authentication, durable storage/atomicity, real multi-process fencing, stream cancellation, client byte acknowledgement, restore continuity and deployed runtime behavior.

## 3. Owner decision dependencies

- **OD-01** decides whether streaming and its transport test family are MVP scope.
- **OD-02..05** must be resolved as one lifecycle: pre-claim revocation, active transfer, retry/resume and pre-commit cross-authority consistency.
- **OD-06..07** decide time/identity invariants before persistence technology selection.
- **OD-08** decides compact receipt-head binding.
- **OD-09..12** decide EP-18, EP-24, contradictory projection and termination/cleanup acknowledgement.
- **OD-13** decides the user-visible claim supported by client byte evidence.

All OD-01..OD-13 remain OPEN. Recommendations in either review are not approvals.

## 4. Canonical acceptance and implementation gate

Supporting P39 tests map to the existing CASE/LOOP requirements in `P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md`. They do not pass canonical acceptance by themselves. Preserve LOOP-01..14, CASE-01..16 and all D-IDs. CASE-04 remains **INCOMPLETE / timed_out**.

P39/P40 implementation remains **CLOSED**. No source/test change, dependency, schema, adapter, provider, runtime, database or transport selection is authorized. The next permitted work is review reconciliation and explicit owner decisions. A bounded model-only P40 slice may be proposed only after those gates clear.
