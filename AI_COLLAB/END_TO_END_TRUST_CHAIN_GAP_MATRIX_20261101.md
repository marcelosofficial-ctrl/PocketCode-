# PocketCode — End-to-End Trust-Chain Gap Matrix

**Date:** 2026-11-01  
**Status:** Read-only architecture synthesis. SPECIFIED ONLY / NOT IMPLEMENTED / NOT RUN.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Purpose:** Reconcile the provider-neutral boundary, policy-barrier checklist, lifecycle/event model, output/report projection, persistence and artifact-release rules into one end-to-end chain. This document adds no canonical acceptance IDs, does not close owner decisions, and does not authorize source changes, provider/store selection, workloads, spend, merge or deployment.

## 1. Executive verdict

The current specifications are directionally consistent, but there is no verified end-to-end trusted execution path. The pieces are separate:
- PR #2 report formatter: a pure formatting/classification helper for caller-supplied values, not an authenticated evidence producer.
- PR #3/lifecycle descendant: pure lifecycle/event helpers, not a trusted provider ingress, durable event log or coordinator.
- Redaction/output-budget helpers: not proven to be wired through every field rendered by the PR #2 formatter.
- Provider-neutral boundary sketch: proposed interfaces and state transitions, not a selected provider/store or implementation.
- Canonical product contract: target requirements, not evidence that those requirements are implemented.

**Decision:** retain the three source histories separately. Do not integrate helpers by copying them together and calling the result a trusted boundary. The next implementation-ready design must establish one coordinator-owned attempt record and a sequence of authenticated, durable transitions from reservation through release. Each transition must preserve identity and evidence provenance.

## 2. End-to-end trust chain

| Stage | Authoritative producer / input | Required binding and invariant | Current evidence | Gate / status |
|---|---|---|---|---|
| 0. Request admission | Authenticated API session; validated request | Derive tenant from authenticated principal. Validate source/input/runtime/entrypoint and bounds. Client IDs never establish ownership. | Canonical contract describes this; no API implementation verified. | API/auth integration NOT RUN |
| 1. Request identity | Trusted coordinator canonicalizer | Versioned semantic fingerprint binds source/input identity, runtime, effective policy semantics and schema. Strict JSON policy tree; no key coercion. | Fingerprint helper/design exists; policy-map recursive key validation remains proposed. | Pure validation first; durable identity later |
| 2. Reservation | Durable store transaction | Atomic uniqueness on authenticated tenant + idempotency key; same fingerprint returns same job/attempt; changed fingerprint conflicts. | In-memory helpers and boundary sketch only. | D-06 OPEN; persistence NOT RUN |
| 3. Dispatch intent | Coordinator + durable store | Persist stable job/attempt/provider token and expected policy revision before external start. Reservation and dispatch-intent states must be transactionally distinguishable. | Specified in boundary sketch and DR crash matrix. | Persistence integration NOT RUN |
| 4. Policy barrier | Actual provider/runtime dispatch boundary | Bind the required immutable policy revision to this exact attempt at actual start, or atomically reject stale revision. A request fingerprint or read-then-dispatch is insufficient. | PBR-01..07 and PF-01..05 are specifications; no provider selected. | D-05 BLOCKED |
| 5. Start / acknowledgement | Provider operation | Preserve provider token, operation ID and trusted applied-policy evidence. Lost acknowledgement means reconcile the original attempt, never blind redispatch. | Fake protocol/design only; no real provider contract verified. | Provider integration NOT RUN; D-06 OPEN |
| 6. Event ingress | Authenticated provider/coordinator source | Validate tenant, job, attempt, source namespace and relevant policy binding before reduction. Assign coordinator event ID/sequence. | Reducer has shallow-copy and collision-diagnostic gaps; no authenticated ingress verified. | D-04 OPEN; COORD-11/12 |
| 7. Terminal reconciliation | Trusted coordinator + authoritative lookup | Preserve all terminal observations; exact replay differs from changed-content conflict. Unknown or contradictory terminal state cannot become PASS. | Pure helper/research only; no provider lookup proof. | Fake logic and provider evidence NOT RUN |
| 8. Cleanup | Trusted runtime/provider cleanup evidence | Record cleanup independently from program outcome. A confirmed nonzero exit remains FAIL even if cleanup is unknown; artifacts remain blocked. | Semantic proposal; no cleanup producer or integration verified. | Runtime/provider NOT RUN |
| 9. Output collection | Trusted collector | Per-stream state, byte accounting, provenance, runtime limit vs collector cap vs display truncation. Requiredness is case-specific. | Output vocabulary specified; current formatter does not carry full typed state. | Collector NOT RUN; D-03 OPEN |
| 10. Redaction / report projection | Trusted collection boundary and typed coordinator projection | Prevent secrets entering execution; minimize collection; apply bounded redaction before any rendered field. Formatter must not accept arbitrary provider dictionaries as authoritative. | PR #3 redactor exists separately; PR #2 formatter has no verified redaction path. | Integration gap; tests NOT RUN |
| 11. Report publication | Durable report/evidence store | Immutable versions, monotonic atomic version allocation, stable append operation ID, immutable evidence references, crash/concurrency recovery. | In-memory history/helper is not durable proof. | D-08 OPEN; persistence NOT RUN |
| 12. Artifact publication | Trusted publisher + object/manifest store | Manifest binds tenant/job/attempt, evidence, immutable object version, digest, size and safe metadata. Cross-store partial commit remains pending/unknown. | Proposed only; no store or publisher selected. | D-07 OPEN; cross-store NOT RUN |
| 13. Artifact release | Authenticated release API at time of transfer | Reauthorize current principal; verify exact tenant/job/attempt, manifest/lifecycle/quarantine, safe identity/path/type/size and exact immutable bytes immediately before release. | Release checklist and predicate design only; no HTTP/store proof. | D-07 OPEN; API/store integration NOT RUN |
| 14. Device presentation | Mobile client | Show execution outcome, verdict, collection state, report version, release state and UNKNOWN distinctly. Reconnect reconciles; it does not infer completion. | Static prototype and canonical acceptance only. | Device acceptance NOT RUN |

## 3. Non-negotiable identity spine

A single attempt must be traceable without treating all identifiers as interchangeable:

1. Authenticated tenant/principal scope.
2. Logical job identity.
3. Attempt identity (one intended external execution).
4. Versioned semantic request fingerprint.
5. Expected policy revision and its authority.
6. Applied policy revision with trusted evidence tied to the actual start operation.
7. Provider idempotency token and provider operation identity.
8. Source namespace + source event identity, separately from coordinator event identity.
9. Coordinator sequence and immutable accepted evidence IDs.
10. Report append operation ID + immutable report version.
11. Artifact ID + manifest version + immutable object version + digest/size.
12. Current authorization decision for each release.

A request fingerprint identifies accepted request semantics. It does not prove the applied policy. A provider operation ID does not prove tenant ownership unless bound by authenticated ingress. A historical report PASS is not an artifact release token.

## 4. Cross-stage failure rules

| Failure window | Required behavior | Prohibited shortcut |
|---|---|---|
| Before reservation commit | Revalidate and compete for atomic reservation. | Assume a local in-memory reservation survived. |
| After reservation, before dispatch intent | Resume only if durable ordering proves no external call was allowed. | Infer safety from a missing acknowledgement row. |
| After dispatch intent, before/during/after provider call | Reconcile same attempt/token. UNKNOWN means no automatic second start. | New attempt after timeout, lease expiry or lookup outage. |
| Policy changes between preparation and start | Actual atomic/immutable policy barrier rejects stale revision, zero starts. | Two reads, cached ETag, or fingerprint as proof. |
| Provider event has wrong scope or altered replay content | Reject/quarantine; retain conflict evidence. | Trust client-supplied trust flags or compare only payload. |
| Duplicate coordinator sequence | Preserve every colliding record and explicit diagnostics. | Deterministic sort tie-break presented as authority. |
| Terminal evidence conflicts | Preserve both observations; derive UNKNOWN/INCOMPLETE. | Choose whichever event arrived last. |
| Child exit is known but cleanup unknown | Preserve program verdict; show cleanup UNKNOWN; block release. | Rewrite known nonzero exit as unknown program outcome. |
| Collector cap reached | Preserve raw exit fact and collection state; apply case-specific output rule. | Claim process termination from collection truncation. |
| Report/manifest commit acknowledgement lost | Reconcile by same stable operation identity. | Blind append or expose partial publication. |
| Authorization/quarantine changes before download | Re-evaluate at release boundary and deny if unresolved. | Reuse historical PASS or cached authorization. |

## 5. Owner decisions and exact blockers

| Decision | Current status | What must be resolved before contract freeze |
|---|---|---|
| D-01 limit verdict | OPEN; canonical working default is CASE-04/LOOP-05 INCOMPLETE / timed_out for confirmed timeout | Keep runtime-enforced timeout separate from collector/display truncation. Do not silently change canonical wording. |
| D-02 infrastructure uncertainty | OPEN; working default UNKNOWN/INCOMPLETE absent trustworthy program result | Define evidence threshold for provider failure vs confirmed program result. |
| D-03 output completeness | OPEN; no universal complete-output/artifact gate | Define required streams/artifacts per acceptance case and retain COMPLETE/PARTIAL/UNAVAILABLE/EMPTY/RUNTIME_LIMIT/DISPLAY_TRUNCATED. |
| D-04 event identity | OPEN | Define authenticated source namespace, scope binding, immutable fields, replay/conflict and sequence collision semantics. |
| D-05 policy binding | BLOCKED | Select a real boundary with immutable per-attempt policy or atomic conditional dispatch, then prove applied revision at start. |
| D-06 idempotency/recovery | OPEN proposal | Select durable reservation and provider idempotency/lookup semantics; prove crash, concurrency and lost-ack recovery. |
| D-07 artifact release | OPEN proposal | Select object store/API and prove current auth, quarantine, exact immutable bytes and release race behavior. |
| D-08 report history | OPEN proposal | Select durable store and prove append identity, monotonic versions, concurrency, crash recovery and retention. |

Do not confuse D-01..D-08 in the execution/lifecycle owner register with identically numbered decisions in the separate AI Workflow Director register.

## 6. Highest-priority unresolved design questions

These are concrete blockers, not new canonical acceptance IDs:

- **Policy binding location:** What exact call/transaction is the atomic start boundary, and what authenticated evidence binds applied revision to attempt ID? If no such provider primitive exists, the hosted execution design is not acceptable for untrusted code.
- **Provider “not created” semantics:** Does lookup distinguish definitive rejection from eventual-consistency not-found? What is the idempotency-token scope, retention horizon and concurrent-start behavior?
- **One durable authority:** Which store owns reservation, dispatch intent, accepted event identity and report version allocation? If multiple stores are unavoidable, define outbox/reconciliation and visible pending states.
- **Event canonicalization:** Which fields are immutable, and which delivery metadata may vary on replay? Ensure tenant/job/attempt/source/policy scope is bound before reduction.
- **Collector contract:** Which stream states are required per case? Which component can authoritatively say runtime enforcement occurred, versus collector-only truncation?
- **Report trust boundary:** Can every displayed field be traced to a typed projection, with no raw provider mapping or unclassified metadata bypass?
- **Artifact bytes:** Does the release API stream the exact immutable version whose digest and size were checked, without a lookup/open TOCTOU gap?
- **Retention dependency:** Can an artifact/report remain actionable after the identity, policy, evidence or tombstone needed to validate it expires? Publish one retention matrix across all stores.

## 7. Implementation and evidence order

1. Owner resolves D-01..D-04 sufficiently to freeze relevant semantics; keep proposed helper-only work separate.
2. Refresh exact source branch/file/test pins. Do not use stale patch packets as source authorization.
3. Harden pure lifecycle/fingerprint helpers and tests independently. These tests prove helper behavior only.
4. Define trusted ingress and fake coordinator ordering, including policy refusal and no-blind-redispatch.
5. Select and test durable reservation/event/report storage with concurrency, crash injection and acknowledgement-loss recovery.
6. Select provider and prove actual policy binding, start idempotency, authoritative lookup, terminal evidence and termination behavior.
7. Integrate one trusted output collector, typed projection and bounded redaction path; test all report fields.
8. Prove artifact publication consistency and release-time authorization/byte integrity against the actual store/API.
9. Run supported-device acceptance for reconnect, UNKNOWN, history, copy and download.
10. Only after evidence review, prepare a minimal integration plan for source histories. No blanket merge/cherry-pick.

A fake can prove coordinator branching. A pure helper test cannot prove authenticated ingress. A mock transaction cannot prove durability. A release predicate cannot prove HTTP returns the exact checked bytes. Desktop tests cannot prove phone behavior.

## 8. Current evidence ledger

| Claim | Evidence now | Verdict |
|---|---|---|
| Canonical product requires truthful outcomes, bounded outputs, isolation and honest reconnect | `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | SPECIFIED |
| Request/policy fingerprint and applied-policy barrier are distinct | Adapter boundary decision gate and provider-neutral sketch | SPECIFIED |
| Durable idempotency and no-blind-replay design exists | DR-01..12 and boundary sketch | SPECIFIED |
| Current lifecycle reducer has complete trusted event ingress | Not demonstrated; static source review found gaps | NOT PROVEN |
| PR #2 formatter receives fully redacted typed evidence | No integrated path found | NOT PROVEN |
| Report history is durable and append-only | In-memory model only; no selected store | NOT PROVEN |
| Artifact release checks current authorization and exact bytes | Checklist only; no store/API | NOT PROVEN |
| Provider policy, isolation, egress, limits and cleanup are enforced | No provider/runtime selected | NOT PROVEN |
| Device execution workflow is accepted | Static prototype only | NOT PROVEN |

## 9. Source pins used

All source files below were fetched from `pocketcode-execution-boundary-crosswalk-2026-11-01` during this review:

- `PRODUCT/EXECUTION_CONTRACT.md` — `128a00a9b2a335514814cab76fb5781fe8f9f858`
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` — `c6714c27db52b2962fe8d1c7e6a16829d46a8338`
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` — `7d75b6844815570dd9faf1cd75791ba0abac33c1`
- `AI_COLLAB/OUTPUT_STATE_AND_VERDICT_RELEASE_CROSSWALK_20261029.md` — `0f5fb8f772941c25ae7db590c9b5b86012c5ad99`
- `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md` — `a237e882128865ce6a47651a1f9c6da6901f4994`
- `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` — `083123e764a35f761d6d8a779272b07b5a0c8d45`
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` — `e67b2659cf2d71ef77d8e4619c91143e71062470`
- `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md` — `16985f50a0302ac5c55798445705971807eb5661`
- `AI_COLLAB/BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md` — `2fba0c980a9644a7e9e40e03c2adb19b45399843`
- `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md` — `534ba2b67ee7227b3e02a7a27d74ff6b2ba9e158`
- `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md` — `8d665bd5b650fe00dd8133a729b13cca7cb523eb`

**Method and limits:** static document/source review and cross-reference reconciliation only. No tests were executed, no runtime/provider/store was selected, and no implementation or canonical acceptance file was changed.
