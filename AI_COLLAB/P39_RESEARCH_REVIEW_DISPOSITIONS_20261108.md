# P39 research-review dispositions (interim)
**Date:** 2026-11-08  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Review base HEAD:** `2c8dee79e2e0ef6988f2134f327fb8a046fcec59`  
**Research/documentation pin:** `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0`  
**Reference source/tests:** `744cb4dc7cd4994647c84ac7476d0c78a21f0540`

## Scope and authority
This note decides the nine findings in `CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md`. That report explicitly reviewed only `RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md`; it did not review the source model, model tests, P37 concurrency contract or ChatGPT static audit addendum. These dispositions therefore do not close P39.

The Gemini response supplied in chat is a research/implementation plan, not a complete independent P39 review: it contains no source-pinned finding table, adversarial schedules, verified line references or executed test evidence. The repository's Gemini review request remains open. No reviewer input is fabricated or inferred.

## Finding-by-finding disposition

| ID | Severity in review | Disposition | Decision |
|---|---|---|---|
| F-01 | High | **ACCEPT** | A policy decision fetched before the transaction can be revoked before grant commit. The contract needs a commit-time authoritative revocation/policy epoch or an explicit bounded-staleness rule. |
| F-02 | High | **ACCEPT WITH CHANGES** | The research recipe's latest-head read can conflict with same-key recovery after head advancement. P37 already says replay looks up the committed grant before a new reservation. Harmonize the recipe and fingerprint semantics with that rule. |
| F-03 | High | **ACCEPT** | Expiry cannot be judged by a caller-controlled or worker-local clock. Use an authoritative store/authority clock for expiry, and make the current monotonic fence the decisive write authority. |
| F-04 | Medium | **ACCEPT WITH CHANGES** | Grant identity must never be recycled and fence state must survive deletion/restore. Random 128-bit IDs reduce collision probability but do not by themselves guarantee uniqueness or preserve a fence epoch. |
| F-05 | Medium | **ACCEPT** | A poison predecessor can block an aggregate forever. Define bounded detection, aggregate HOLD/quarantine, operator-visible repair and no silent sequence skip. |
| F-06 | Medium | **ACCEPT** | "Single-use or stream-scoped" is underspecified for reconnect/resume. Define a resumable capability bound to grant, fence epoch, immutable object version, operation and byte range, reissued under current policy on resume. |
| F-07 | Medium | **ACCEPT WITH CHANGES** | The withdrawn SQLite 3.52.0 makes "3.51.3 and later" too broad. SQLite writer serialization also means adapter tests must explicitly assert stale expected-version/CAS rejection, not merely observe serialized writes. |
| F-08 | Low | **REJECT** | The research claim is supported: Redis's official distributed-lock guidance explicitly says to implement fencing tokens and warns that a live client must not assume its lease remains valid. This does not make Redis itself the fencing authority. |
| F-09 | Low | **ACCEPT WITH CHANGES** | Add an explicit crash schedule where the consumer has durably applied an event but the relay's delivered marker is not durable. Verify redelivery is deduplicated before acknowledgement and produces one logical effect. |

## Detailed corrections required

### F-01: authorization revocation linearization
**Verified specification gap.** The adapter recipe obtains fresh authorization before beginning the transaction, then validates a snapshot. If revocation occurs after that decision but before grant commit, the recipe does not define an authoritative re-check that makes POLICY-01 true.

Add POLICY-03 with a deterministic schedule: obtain allow at policy epoch P; pause before commit; revoke to P+1; resume. The result must be denied if the product promises "revocation before grant commit: denied". The adapter must compare a monotonic policy/revocation epoch inside the same authority/transaction boundary, or explicitly define and test a bounded-staleness window if the policy authority cannot participate in that boundary. Do not claim strict atomic revocation across independent stores without a protocol. Revocation after grant commit/in-flight remains a separate owner policy decision.

### F-02: stable intent versus latest-head resolution
**Partly covered elsewhere, but the research recipe is ambiguous.** P37 §4 says a lost-response retry looks up the committed grant before attempting a new reservation and does not reinterpret the request against a later receipt. The P39 research recipe's step 4 re-reads latest head before step 6 claims the key, which can be read as applying the new-head gate to retries.

Clarify the order: authenticate caller; resolve same-key replay against the immutable original intent and current authorization binding; return the original grant without authorizing bytes; only a genuinely new key proceeds through current-head validation and new reservation. The stable fingerprint must not include a server-resolved moving "latest" value. If the API accepts "latest", persist its first resolved immutable receipt reference as the request's canonical intent. Add IDEMP-01 for retry after head advancement.

### F-03: trusted time and fencing
Add CLOCK-01. A client-supplied `now` or worker-local wall clock is not an authority for lease expiry. Use the authoritative persistence/coordinator clock for expiry eligibility. Regardless of expiry, every protected mutation must atomically compare the presented fence with the current durable fence. Expiry is a takeover/liveness condition; the monotonic fence is the stale-writer safety condition.

### F-04: identity and fence continuity
Add ID-01 covering delete, restore, backup rollback and migration. Require non-reusable grant identity enforced by a durable uniqueness constraint and collision handling, plus a fence namespace/high-water mark that cannot reset when a grant row is deleted or restored. Random 128-bit IDs are a useful collision-resistant identifier, not a proof of mathematical uniqueness and not a substitute for durable fence continuity. Specify tombstone retention and recovery horizon explicitly.

### F-05: poison-event handling
Add ORDER-04. If event N is permanently malformed or unavailable, do not publish/apply N+1 as if the gap did not matter. After a bounded retry/age threshold, place the aggregate in an operator-visible HOLD/quarantine state, retain the original event and evidence, and provide an audited repair/replay path. Any authorized skip must be an explicit, durable, versioned resolution event, never an implicit timeout skip.

### F-06: resumable stream capability
Add STREAM-02. A resume capability should bind at least grant ID, current fence epoch, immutable object version/digest, operation scope, stream identity and permitted byte range. The authority reissues it after authenticating the caller and checking current policy/fence; takeover invalidates the old epoch. Define whether concurrent streams are forbidden and how cancellation/revocation reaches an established transport. Already-emitted bytes cannot be recalled.

### F-07: SQLite version and race evidence
The official SQLite release history marks 3.52.0 as **Withdrawn**, lists the WAL-reset fix in 3.51.3 and 3.53.0, and later lists 3.54.x releases. Replace the broad "3.51.3 and later" phrase with explicit known fixed release lines and require pinning the exact SQLite library actually bundled by the app/runtime. Do not select SQLite here.

Add RACE-08 (or extend the existing matrix): use independent connections/processes and barriers; submit the same stale expected head/version after one writer commits; prove the second operation fails/reloads rather than creating a fork or overwriting the winner. Separately test SQLITE_BUSY handling and retry. State honestly that SQLite's single-writer serialization does not simulate overlapping database writers from engines with different concurrency models.

### F-08: Redis fencing reference
Reject as a defect. The official Redis distributed-lock page says "You should implement fencing tokens" for long-running processes and warns that lock validity can be compromised by clock shifts. Keep the citation, but phrase the limitation precisely: Redis documents the fencing pattern; a PocketCode adapter still needs a monotonic token from its chosen authority and enforcement at the protected resource. Redis TTL locks alone are not that authority.

### F-09: consumer-commit / relay-marker crash
Add CRASH-04 as an explicit end-to-end schedule: publish event; consumer durably applies it and records source/event identity; relay's delivered-marker write is lost or crashes; event is redelivered after restart; consumer returns duplicate without repeating the logical effect; relay then marks delivered under its current fence. This supplements, rather than replaces, CRASH-03.

## Independent source audit cross-check at source SHA 744cb4d
These are ChatGPT's source-pinned findings, not findings from Claude's partial review:

- **P39-S1, VERIFIED model gap:** `scripts/release_grant_conformance.py`, `record_progress()` lines 269–293, increments `aggregate_version` and updates progress without appending a matching `GrantEvent` or `OutboxItem`. This creates a permanent event-version gap after progress.
- **P39-S2, VERIFIED model gap:** `GrantEvent` lines 51–59 and `consume_event()` lines 295–313 store/trust a caller-provided digest string without canonical payload bytes or recomputation. `test_consumer_rejects_same_event_identity_with_changed_payload` lines 209–218 changes only the digest; it does not change grant/version/state metadata while preserving the digest.
- **P39-S3, VERIFIED model gap:** grant-event `mark_outbox_delivered()` lines 315–321 checks only event existence and flips `delivered`; it has no claim, owner, lease or fence. Do not confuse this with `scripts/fake_outbox.py`, whose separate effect-dispatch state machine has claim/lease/fence checks (including `claim()` and `_require_current_lease()`).
- **P39-S4, VERIFIED boundary limitation:** the reviewed grant model has no streaming transport. State fencing can reject later state writes but cannot terminate bytes already being emitted on an established socket. Transport capability validation, cancellation and byte-observation semantics remain adapter/transport obligations and UNKNOWN until implemented and tested.
- **Journal trust boundary:** `scripts/event_journal.py` explicitly says producer authentication is supplied by a trusted adapter; `AuthenticatedProducer` is a data value, not cryptographic verification performed by the module. `advance_fence()` and `append()` are separate in-memory operations, so a durable adapter must make fence validation/advance and append atomic where required.

### Additional source audit slice: idempotency, bootstrap, event binding and test traceability

**VERIFIED: principal/tenant/request-key idempotency is correctly scoped in the sequential model.** `reserve()` constructs the identity as `(tenant_id, principal_id, request_key)`, validates caller authorization before lookup, and compares the stable-intent fingerprint on replay. Tests cover different tenant/principal namespaces and reject unauthenticated replay. `test_same_key_same_intent_replay_survives_refreshed_authorization_and_successor` confirms that an exact replay returns the original grant after the receipt head advances. This means F-02 is a recipe/document-order ambiguity, not a demonstrated defect in this model's replay order.

**VERIFIED: first-head bootstrap is only specified, not concurrency-tested.** `seed_head()` checks for an existing key and inserts into a Python dictionary; it cannot model two concurrent initializers. P37 requires a stable head anchor and unique, atomic first-anchor/first-receipt creation, but the P37 minimum adapter matrix does not include a distinct two-initializer case. The P39 research matrix does. This remains a durable-adapter acceptance obligation, not evidence that a concurrent adapter exists.

**P39-S5 — Event consumer does not bind event identity to an existing tenant-scoped grant.**  
**Severity:** HIGH for a future trusted consumer boundary; production exploitability UNKNOWN.  
**Source:** `GrantEvent` fields at `scripts/release_grant_conformance.py:51-59`; `consume_event()` at `:295-313`; `Grant` fields at `:27-39`. The event carries source, event ID, grant ID, version, state and a digest string, but no tenant/principal/effect/attempt binding. The consumer does not verify an allowed source, look up an existing grant, or compare event tenant/scope with grant metadata. A fabricated next-version event for an unknown grant can be accepted by the sequential consumer.  
**Correction:** canonical event envelope must bind source, event ID, tenant, principal where relevant, grant, effect/attempt, aggregate version, event type/state and immutable payload. Trusted ingestion must authenticate producer/source, recompute digest from canonical bytes, verify the grant and tenant relationship, and enforce contiguous order. Add tests for unknown grant, cross-tenant reference, wrong source and metadata mutation with the original digest.

**P39-S6 — Producer authentication and fence append are adapter-supplied, not established by the journal model.**  
**Severity:** HIGH boundary requirement; actual production adapter UNKNOWN.  
**Source:** `scripts/event_journal.py:1-7` and `:14-25`; `advance_fence()` and `append()` are separate methods. The module explicitly says it does not verify keys, signatures, certificates, sessions or external credentials. `AuthenticatedProducer` is caller-constructible data, not proof that authentication occurred.  
**Correction:** only a trusted adapter may construct the value after credential/issuer/audience/source/revocation checks. In a durable implementation, fence validation and append must share the required atomic transaction. Never accept an app/provider-supplied `AuthenticatedProducer` object as authority.

**P39-S7 — Adapter acceptance IDs collide across P37 and P39 documents.**  
**Severity:** MEDIUM traceability risk.  
**Evidence:** P39 research matrix uses `RACE-03` for two initial-head creators; P37 uses `RACE-03` for N same-key/same-fingerprint requests. P39 uses `FENCE-02` for an expired transfer worker writing before takeover; P37 uses `FENCE-02` for an old relay marking delivered after takeover. The same bare identifiers therefore name different acceptance cases.  
**Correction:** give each matrix a distinct namespace (for example, `P37-RACE-03` and `P39-RACE-03`) or assign globally unique test IDs and maintain a crosswalk. Do not alter canonical LOOP/CASE/D identifiers.

**Negative evidence preserved:** the existing model tests do cover tenant/principal idempotency namespace, unauthenticated replay rejection, same-key replay after successor, and sequential stale-head rejection. They do not provide concurrent multi-process evidence, producer authentication, tenant-bound event consumption, or first-head race proof. No new test was run.

### Additional trust-boundary verification: authorization, time and durable fencing

**Authorization is structurally checked, not authenticated by the reference model.** `reserve()` receives `auth_allowed`, tenant/principal/scope fields, authorization ID and policy revision as arguments. It checks that the allow flag is true and that the supplied fields match the requested intent, but it does not verify a signature, issuer, audience, credential status, expiry or live revocation state. The negative replay test sets `auth_allowed=False`; it does not prove that an untrusted caller cannot construct `auth_allowed=True`. This is an intentional model boundary, not evidence of a production authorization flaw. A durable adapter must obtain these claims from a trusted policy/authentication authority and must never deserialize caller-provided booleans or claim objects as proof. Add AUTH-01 for forged allow, wrong issuer/audience, expired proof, revoked policy epoch and exact tenant/scope mismatch.

**Lease time is caller-supplied in the model.** `claim_worker()` and `record_progress()` accept `now` as an argument. The expiry check is therefore only a deterministic model rule, not trusted time. A caller that supplies a backdated `now` can make an expired lease appear live before another worker takes over. The existing expiry test supplies the expected boundary time; it does not test a forged/backdated clock. This reinforces F-03 and CLOCK-01: production expiry decisions must use the authoritative persistence/coordinator clock, while current-fence comparison remains the decisive stale-writer safety check.

**Fence and grant-ID durability are not modeled across restart.** `fences`, `leases` and `_next_grant` are in-memory dictionaries/counters initialized in `__init__()`. Reconstructing the model resets them. That is acceptable for a sequential semantic reference, but it cannot prove durable fence continuity, non-reuse, restore safety or idempotency retention. The adapter must persist these authorities outside deletable grant rows and test backup/restore and process restart.

### Additional source audit: post-commit revocation and transport enforcement

**P39-S8 — Post-commit policy revocation has no defined enforcement transition in the reference model.**  
**Severity:** HIGH as an unresolved authorization boundary; production exploitability UNKNOWN.  
**Source:** `Grant` stores the initial `authorization_id` and `policy_revision` (`scripts/release_grant_conformance.py:27-39`). `reserve()` receives caller-supplied `auth_allowed` and policy metadata (`:118-225`). `claim_worker()` checks grant state and worker lease/fence (`:231-268`); `record_progress()` checks fence, expiry and byte bounds (`:269-293`). Neither worker method checks current policy revision, a revocation epoch, authorization expiry, or a trusted revocation decision. The model has no grant-revocation transition or policy-authority interface.  
**Existing specification boundary:** P37 §4 explicitly says replay is not a fresh allow and transfer continuation/resume must independently apply the selected current-policy rule. P37 §7 says revocation after grant commit requires a separately selected in-flight policy. P37 §9 lists that choice as still required. F-01 addresses revocation between authorization fetch and grant commit; it does not decide post-commit/in-flight behavior.  
**Conclusion:** This is a verified omission in the reference model and an unresolved product/adapter decision, not proof of a production bypass. Do not silently assume either “grant is irrevocable” or “all existing grants stop immediately.”  
**Required decision/tests:** define behavior for revocation (a) after grant commit but before worker claim, (b) during an active transfer, (c) after worker takeover, and (d) on retry/resume. Bind the decision to a trusted policy epoch and record the effective policy revision. If revocation must stop work, specify the linearization point and propagation guarantee; if an in-flight grace period is allowed, bound it explicitly. Add separate pre-commit and post-commit tests. Never treat idempotent grant recovery as authorization to send more bytes.

**P39-S4 refinement — worker-state fencing is not stream fencing.**  
The pinned model only protects a later `record_progress()` mutation. A stale worker may have already emitted data before its stale progress write is rejected. There is no stream ID, stream-scoped capability, chunk/range revalidation, cancellation acknowledgement, transport close, or byte-observation accounting in the model. P37 §6 already states that a durable worker fence cannot retract bytes already sent; the transport must independently enforce revocation.  
**Adversarial schedule:** A claims fence n and opens a stream; A emits chunk k; B takes over with fence n+1; policy is revoked; A resumes and attempts chunk k+1 while its next state write is pending or rejected. The adapter must prove the transport rejects or bounds that chunk independently of the later progress write. Also test cancellation request delivered but not acknowledged, connection loss, reconnect/resume under a new fence, and late client acknowledgement from the old stream.  
**Minimum transport evidence:** define the enforcement point (per bounded chunk or range), maximum in-flight bytes after revocation, cancellation propagation and acknowledgement, stream capability binding to grant/fence/object version/operation/range, and separate counters for bytes accepted by transport, emitted, observed by client, and client-acknowledged. No one counter proves another.

**Proposed adapter tests (new P39-prefixed IDs; no canonical IDs changed):**
- `P39-POLICY-02`: revoke after grant commit but before worker claim; assert the explicitly selected policy.
- `P39-POLICY-03`: revoke during an open stream between bounded chunks; assert the documented post-revocation byte bound.
- `P39-POLICY-04`: revoke, then retry/resume after worker takeover; old capability rejected and any new capability reissued only after current-policy authorization.
- `P39-STREAM-01`: stale worker attempts next chunk after fence takeover; transport enforcement rejects it even if state mutation is delayed.
- `P39-STREAM-02`: cancellation requested but not acknowledged; report termination as unconfirmed and keep execution state incomplete.
- `P39-STREAM-03`: compare transport-accepted, emitted, client-observed and client-acknowledged byte counts; never infer client receipt from server progress.

**Negative evidence:** no production transport exists in the reviewed source; no revocation or stream test was run. The current model remains a sequential reference, not proof of adapter behavior.

## Gemini plan assessment
The response supplied by the owner is **ACCEPT WITH CHANGES as research direction only**, not as a completed P39 review or implementation authorization. Its target paths need correction before any work:
- P39-S1/S2 belong to `scripts/release_grant_conformance.py` and `scripts/test_release_grant_conformance.py`, not `result_receipts.py` and `test_result_receipts.py`.
- P39-S3 is the grant-event outbox in `release_grant_conformance.py`; `fake_outbox.py` is a different effect-dispatch state machine that already has lease/fence mechanics.
- P39-S4 cannot be solved by editing the sequential model alone; it needs a defined transport authority and cancellation/revalidation boundary.
The proposed provider/runtime comparisons and mobile platform claims are not independently re-verified in this note. No provider, runtime, database or hosted service is selected.

## Gate and next action
**P39 remains OPEN / BLOCKED for final reconciliation.** Claude's committed review covers only the research packet. Gemini's supplied plan is not the required independent source-pinned report. ChatGPT's source audit verifies S1–S4 and the journal boundary, but does not substitute for the two reviewer reports. No source code was changed; no tests were run in this pass.

Next bounded task: finish the source audit of policy-revocation and transport stream/cancellation obligations against the pinned P37 contract and tests. Reconcile complete reviewer reports when available. Do not modify source code or select an adapter before the P39 gate clears.

## Primary sources
- SQLite release history: https://www.sqlite.org/changes.html
- Redis distributed-lock guidance: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/
- Exact source/test pin: https://github.com/marcelosofficial-ctrl/PocketCode-/tree/744cb4dc7cd4994647c84ac7476d0c78a21f0540
- Claude partial review: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/2c8dee79e2e0ef6988f2134f327fb8a046fcec59/AI_COLLAB/CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md
