# Lifecycle Contract Regression Plan

**Date:** 2026-11-01  
**Purpose:** Turn the static review findings OBS-01 through OBS-06 and Claude's engineering review into a staged, evidence-layered regression plan.  
**Status:** Proposed test design only. No source or tests changed; all tests NOT RUN.

## 1. Scope and evidence pins

This plan targets the pure helper snapshot on branch `pocketcode-lifecycle-fingerprint-audit-2026-10-27`:

- `scripts/lifecycle_contract.py`, blob `316345341603848c4a86a6a82e533daa796c7695`.
- Existing test snapshot, blob `ef9a68de632be30c091afe57f0724fd030a513f9`.
- Owner decision register `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`, blob `e67b2659cf2d71ef77d8e4619c91143e71062470`.

The helper snapshot is a pure provider-neutral model. Its module docstring expressly says it does not launch processes, contact providers, or claim runtime security. The lifecycle-fingerprint branch is separate and unmerged. This plan does not imply that its helper is integrated into main, PR #3, or a live host.

## 2. Priority and required proof layers

| Priority | Finding | First appropriate layer | Why |
|---|---|---|---|
| P0 | OBS-02 malformed negative flags can permit false PASS | Pure helper | PASS is the release-enabling disposition; strict input typing is locally testable. |
| P0 | OBS-01 missing terminal evidence conflated with provider error | Pure helper, then authenticated boundary | Deterministic state mapping is testable locally; source authenticity is not. |
| P1 | OBS-05 cross-attempt event contamination | Pure helper with expected attempt context, then coordinator integration | The reducer needs an explicit expected identity to compare against. |
| P1 | OBS-04 event producer authority | Pure helper schema tests, then authenticated adapter/boundary | Role labels can be validated locally; authenticity requires a trusted channel or signature. |
| P1 | OBS-06 truncation cause conflated with runtime limit | Pure helper | Distinct evidence causes and outcomes must not be collapsed. |
| P2 | OBS-03 streaming redaction carry and token-length gaps | Pure helper plus adversarial chunk tests | Deterministic byte-stream behavior is locally testable; redaction remains defense-in-depth only. |
| P1 at integration stage | Ambiguous dispatch and retry identity | Fake adapter, persistence/concurrency, provider | Pure decisions are insufficient to prove atomic reservation or provider idempotency. |
| P1 at integration stage | Exact-result persistence and queue liveness | Persistence and runtime/fake-queue tests | Restart durability and liveness are external to a pure helper. |

Priority is risk-oriented, not a claim that the corresponding test currently exists or fails in a running product.

## 3. Pure-helper regression matrix

### PC-LC-01: strict negative-polarity booleans (OBS-02)

For each field `contradictory_evidence`, `limit_violated`, and `output_truncated`, exercise values `0`, `None`, and `""` against an otherwise valid EXIT_ZERO/PASS candidate.

Expected: reject malformed input or return INCOMPLETE. It must never return PASS by interpreting a falsy non-boolean as False.

Also test `True`, `False`, `1`, and `"false"` explicitly. Literal booleans must have documented semantics; malformed truthy values must not become a PASS or be silently treated as valid evidence. Keep the existing positive-gate malformed-input tests, but do not mistake them for coverage of negative-polarity flags.

### PC-LC-02: terminal evidence state separation (OBS-01)

Inputs:
1. Empty event stream.
2. Nonterminal-only stream.
3. `provider_error` event with no source identity.
4. `provider_error` event with an untrusted or mismatched source.
5. Provider-boundary event with an authenticated producer identity and confirmed cause.

Expected: cases 1–4 do not become confirmed PROVIDER_ERROR. Only case 5 may support that disposition. The pure helper can test the state mapping when given a trusted/untrusted classification; a separate authenticated boundary test must establish how that classification is produced.

### PC-LC-03: event identity and attempt correlation (OBS-05)

Supply an expected context containing tenant, job, attempt, source and policy identity. Include:
- Correctly bound terminal event.
- Event from another tenant.
- Event from another job.
- Stale event from an earlier attempt.
- Mismatched source or policy identity.
- Reused event ID with changed payload or sequence.
- Duplicate identical event ID and payload.

Expected: mismatched events are rejected or quarantined and cannot win reduction. Identical duplicates are idempotent only within the same expected context. Conflicting identity reuse produces an explicit conflict/incomplete state. A pure helper cannot prove IDs are globally unique or unforgeable across restarts.

### PC-LC-04: producer-role contract (OBS-04)

For each event kind, test missing, unknown, wrong-role and allowed producer roles. Define the allowed observation owner for exit code, cleanup confirmation, provider failure, policy authorization and artifact digest.

Expected: a syntactically valid event kind from the wrong producer role cannot establish the corresponding fact. This checks role policy, not cryptographic or channel authenticity.

### PC-LC-05: truncation taxonomy (OBS-06)

Keep execution outcome, limit enforcement, termination evidence and presentation/collection truncation as separate inputs. Test:
- Display-only truncation plus independently confirmed EXIT_ZERO.
- Collector/retention cap plus independently confirmed EXIT_ZERO.
- Trusted runtime-enforced limit with confirmed termination.
- Runtime limit requested but termination unconfirmed.
- Truncation with no reliable terminal evidence.

Expected: display/collector truncation alone does not rewrite a confirmed EXIT_ZERO to LIMIT_EXCEEDED. LIMIT_EXCEEDED requires trusted evidence of an enforced limit under the contract. Unconfirmed termination remains INCOMPLETE/UNKNOWN rather than being inferred from truncation. A new model must not simply rename the existing boolean without defining the evidence producer and cause.

### PC-LC-06: redactor adversarial stream tests (OBS-03)

Test chunked inputs around:
- Separator lengths 755–763 after `Bearer`, with zero to seven token bytes present when the carry cutoff is crossed.
- Bearer-like token lengths 255, 256, 257, 300 and over 600.
- Alphanumeric-only and punctuation-containing tokens.
- Padding/delimiter cases, including equals, period and hyphen.
- Mixed-case scheme text.

Expected: no portion of the secret is emitted, including a suffix. Assert across every emitted chunk and final flush, not only against a full-token substring. Test chunk partitions that place each relevant boundary on either side of a feed call.

The source pattern is case-insensitive and caps the bearer token at 256 characters. The carry algorithm retains 768 bytes and only backs up the cutoff when a complete regex match crosses it. The separator threshold is chunk-dependent. This test is defense-in-depth, not a security guarantee; secret minimization and prevention remain primary.

## 4. Adapter, persistence and runtime matrix

### PC-AD-01: ambiguous dispatch with fake adapter

Script provider outcomes:
- Dispatch acknowledged.
- Dispatch accepted but acknowledgement lost.
- Lookup returns authoritative same-attempt result.
- Lookup returns UNKNOWN.
- Lookup returns a result for a different attempt.
- Same idempotency key with changed request fingerprint.

Expected: UNKNOWN lookup never causes a second dispatch while the first attempt remains unresolved. Authoritative same-attempt result is adopted. Changed fingerprint under the same key conflicts before dispatch. Different-attempt results cannot be adopted.

### PC-AD-02: repair retry identity and workspace exclusion

A repair retry changes task content and therefore creates a new task/attempt identity. Test both:
- New attempt with new idempotency key.
- New attempt reusing the old key with changed fingerprint.

Expected: the latter conflicts. A repair must not execute concurrently in a workspace whose previous dispatch remains unresolved. The workspace exclusion guarantee requires coordinator/integration tests, not only a pure helper.

### PC-DB-01: durable reservation and exact-result replay

Inject process crashes:
1. Before reservation.
2. After reservation but before dispatch.
3. After result computation but before publication.
4. During result write.
5. After durable publication but before acknowledgement.

Expected: reservation is atomic; torn/partial writes are detectable; restart resolves the same attempt; published result bytes are replayed exactly rather than recomputed; duplicate requests do not create a second execution. A later evidence update creates an explicit immutable version and does not silently rewrite an already-issued result.

### PC-RT-01: queue quarantine and liveness

With a fake queue first, then a real isolated runtime:
- Poison item ahead of valid work.
- Crash during quarantine.
- Repeated poison item.
- Later valid item after quarantine.
- Diagnostic record and source identity preserved.

Expected: poison item is quarantined without deletion of its evidence; later work proceeds; recovery is idempotent; poison item cannot retry forever. A pure classifier cannot prove queue liveness.

### PC-RT-02: termination and trusted observation

At the actual process/provider boundary, test:
- Exit code observed by supervisor.
- Cleanup observed independently of child output.
- Timeout/limit signal with confirmed termination.
- Timeout/limit signal with unconfirmed termination.
- Forged or wrong-channel terminal event.

Expected: terminal facts are attributed to the trusted observer; missing or unauthenticated evidence stays UNKNOWN/INCOMPLETE. No synthetic helper test is a substitute for this boundary evidence.

## 5. Crosswalk boundaries

These tests belong to the lifecycle helper/RevDev engineering workstream. They do not automatically become PocketCode LOOP/CASE tests, AWC fixtures, or P0-D canaries.

- AWC tests assistant behavior and remains PROPOSED_NOT_RUN.
- LOOP/CASE tests PocketCode execution acceptance and remains proposed/NOT RUN.
- P0-D tests RevDev publisher/mission obligations.
- The helper's unit tests establish only pure-model behavior.
- Fake adapter, persistence and runtime tests are separate evidence classes.

Do not merge the suites or claim cross-project coverage because two tests use similar words such as retry, handoff, truncation or report.

## 6. Exit criteria for claiming progress

A finding can be marked **pure-helper verified** only when:
1. The exact source and test commit are pinned.
2. The test is present in the committed suite.
3. The suite is actually executed in a named environment.
4. The complete result and skipped count are recorded.
5. The result is explicitly scoped to the helper.

A finding can be marked **adapter/persistence/runtime verified** only with the corresponding executed test and exact implementation/evidence producer pinned. Never promote a pure-helper PASS into a provider, durability, security, host or queue-liveness claim.

## 7. Current status

All rows in this plan are proposed. No source code, tests, canonical acceptance, provider adapter, persistence layer, runtime, queue, PR or main branch was changed. No test was run. PC state remains UNKNOWN. This document is a sequencing and acceptance-design artifact only.
## 8. Supplementary regression cases from Gemini's review (2026-11-01)

These are new test-design identifiers only. They do not rename, extend, or replace AWC, AEC, LOOP, CASE, P8U, P0-D, CYC, or OBS IDs. They are retained because the engineering ideas are useful after correcting Gemini's crosswalk errors.

### PC-EXT-01: applied-policy barrier before process launch

**Traceability:** PocketCode D-05, LOOP-12, CASE-15.  
**Proof layer:** adapter plus provider/runtime evidence; pure checks can test state decisions only.

Test policy supplied at sandbox creation and policy mutation on an existing sandbox. For an update, cover desired revision ahead of applied revision, pending status, stale read, mismatched policy contents, concurrent update/ETag conflict, provider read failure, and exact desired/applied match. The adapter must not dispatch the untrusted process while the policy is pending, stale, missing, or mismatched. A create/update API success, HTTP 2xx, ETag value, or self-reported adapter flag alone is not proof of effective egress enforcement. Require authoritative applied-policy state before launch, then actual provider/runtime egress evidence for the relevant protocols and routes. A probe is corroboration, not exhaustive proof. If the provider cannot guarantee a safe pre-execution barrier, the provider is not eligible for untrusted code.

### PC-EXT-02: actual resource boundary and host containment

**Traceability:** LOOP-12 and the resource/termination semantics in the transition matrix; no AWC mapping.  
**Proof layer:** provider/runtime evidence, with adapter evidence for the configured policy.

Exercise the actual selected provider's configured memory, CPU, process-count, disk/file, wall-time, and output limits as applicable. Show the authoritative enforcement source and exact sandbox/job/attempt identity. A workload exceeding its memory boundary must not kill or destabilize the orchestration worker or unrelated workloads. Where cgroup v2 is the actual mechanism, record the exact hierarchy, limit-owning cgroup, mount options, PID membership, and pre/post hierarchical plus local counters. memory.events.local can undercount descendants; memory.events is hierarchical by default unless memory_localevents is enabled. Neither oom nor oom_kill alone proves cause. Capture OOM/timeout race evidence and counters before cgroup removal. Use provider-specific proof where cgroups are not exposed. Distinguish throttling, allocation failure, file-size rejection, process termination, and output collection caps.

### PC-EXT-03: immutable artifact publication and release-time revalidation

**Traceability:** D-07, proposed execution contract's execution-outcome/artifact-release separation, LOOP-10, CASE-14, and the security implications of CASE-15.  
**Proof layer:** persistence plus adapter and provider/storage boundary evidence.

Inject interrupted writes, partial manifests, digest mismatch, bytes changed after validation, stale policy/authorization, wrong tenant/job/attempt, quarantine, and cleanup-not-confirmed states. A manifest becomes publishable only after the complete immutable object is written and its digest/size/type/path metadata is verified. A partial or digest-mismatched object is never exposed. Re-evaluate current authorization and the exact immutable bytes immediately before release. If policy requires content scanning, test the explicitly versioned scanner and its failure/unknown behavior; do not assume an unspecified scanner exists. Artifact denial must not rewrite the historical execution outcome.

### PC-EXT-04: teardown failure, orphan reconciliation, and separate cleanup state

**Traceability:** lifecycle transition matrix and proposed execution contract; preserve execution outcome separately from cleanup/disposition.  
**Proof layer:** provider/runtime plus durable persistence and reconciliation.

Test confirmed child EXIT_ZERO followed by provider delete timeout, HTTP 500, ambiguous response, delayed termination, and late cleanup confirmation. Preserve the exact child outcome and exit code. Record cleanup as UNKNOWN/pending or ORPHANED_TEARDOWN_REQUIRED when the provider cannot confirm deletion; never mark cleanup complete from a local database close alone. Reconcile the same sandbox/job/attempt idempotently, retain the failure evidence, and prevent a stale cleanup event from changing another attempt. Prove eventual provider-side termination/deletion and ensure a leaked resource cannot silently continue accruing cost. No provider call or workload is authorized by this test design.

### PC-EXT-05: delayed usage and billing reconciliation

**Traceability:** future cost-observability requirement, distinct from OBS-03 and not equivalent to LOOP-14.  
**Proof layer:** adapter plus persistence, only after explicit provider/budget approval.

Represent usage quantity, estimate, provider-reported charge, currency/rate-card version, observation time, and reconciliation state separately. Candidate states include ESTIMATED, PENDING, RECONCILED, and UNKNOWN. Delayed billing data must not appear as final zero cost. A local vCPU-second estimate is not a provider invoice and is valid only when its rate source/version is recorded. This remains BLOCKED under the current $0/no-provider/no-workload constraint.

### PC-EXT-06: stdout cannot forge lifecycle events

**Traceability:** transition matrix trust rule; CASE-09/10 are related report-honesty cases, not equivalent producer-authentication tests.  
**Proof layer:** pure helper and adapter boundary.

Have untrusted code print JSON shaped like a terminal event, including fake `verdict`, `exit_code`, `attempt_id`, `provider_error`, or cleanup fields. Confirm these bytes remain ordinary untrusted stdout and cannot mutate terminal state, disposition, release authorization, or event history. Only an authenticated trusted producer on the accepted event channel can supply the relevant observation.

### PC-EXT-07: tenant-scoped semantic idempotency fingerprint

**Traceability:** D-06 and PC-DB-01 / PC-AD-01; related to CASE-13 but not a replacement for provider dispatch proof.  
**Proof layer:** durable persistence/concurrency, then adapter/provider.

Test same tenant/key/same semantic request, same tenant/key/changed source or input file, changed runtime/entrypoint/limits/policy revision, concurrent reservations, crash after reservation but before dispatch, crash after dispatch but before acknowledgement, and same textual key used by two different tenants. The reservation is atomic and tenant-scoped. The semantic fingerprint covers every execution-relevant normalized field and file digest. Same key and same fingerprint resolves to the original identity; changed fingerprint conflicts before dispatch; cross-tenant keys do not alias. UNKNOWN lookup never triggers blind redispatch. Provider exactly-once execution remains unclaimable unless the provider supplies idempotent-start semantics or authoritative reconciliation.

### PC-LC-05 clarification: do not label a full pipe as a truncation event

Retain the existing separation between execution limit, stream capture, collector/retention, and display truncation. Add a stream-reader interruption/backpressure case. A full Linux pipe ordinarily blocks a writer, or fails under nonblocking I/O; it does not inherently discard bytes at a universal 1 MB threshold. Record whether bytes were never read, deliberately dropped by a collector cap, lost during transport/storage, or omitted by display rendering. Keep process terminal evidence independent.

### Evidence order and hard stop

1. Pure-helper and fake-adapter cases can validate deterministic decisions and protocol mapping only.
2. Persistence cases must prove atomic reservation, crash/restart behavior, immutable publication, and release decisions on the actual chosen store.
3. Provider/runtime cases must prove pre-execution policy enforcement, resource containment, child termination, cleanup, and egress at the actual execution boundary.
4. No level inherits the proof of a later level. A provider API response is not host enforcement evidence; a unit test is not persistence evidence; a mock is not a provider test.

All PC-EXT cases are proposed and NOT RUN. No provider, database, scanner, runtime, or billing system is selected. No source or test implementation is authorized by this plan.


## 9. Alignment with existing falsification checklists

The PC-EXT labels in Section 8 are a review traceability index, not a second normative test suite. Where an established checklist already owns the detailed falsification cases, implement and report against that checklist's original IDs. Do not create duplicate tests, acceptance requirements, or competing expected outcomes merely to satisfy a PC-EXT label.

| Section 8 item | Existing authoritative research/test specification | What remains useful from the Gemini review | Disposition |
|---|---|---|---|
| PC-EXT-01 applied-policy barrier | `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md`: D-05, PBR-01..07 and PF-01..05 | Provider-specific desired-versus-applied state examples and the reminder that an ETag is not proof of data-plane enforcement | Existing PBR/PF are authoritative. PC-EXT-01 is a pointer and provider-specific test-design note, not a duplicate barrier contract. |
| PC-EXT-02 resource boundary/host containment | `SECURITY.md`, LOOP-12, `RESEARCH/EXECUTION_PROVIDER_RESEARCH.md` evaluation proof | Actual selected-provider evidence for memory/CPU/process/disk/output limits and isolation from the orchestration worker | This is still a gap in detailed falsification coverage. Expand the provider proof plan after a provider and its enforcement telemetry are selected. No cgroup-specific requirement unless cgroup v2 is actually the enforcement mechanism. |
| PC-EXT-03 artifact publication/release | `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md`: D-07 and AR-01..14; `PRODUCT/EXECUTION_CONTRACT.md`; `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md` §6 | Use partial-write/digest-mismatch examples as test data against AR-03/05/09/14; keep current authorization and exact immutable bytes at the release boundary | AR-01..14 is authoritative and already covers these requirements. PC-EXT-03 must not become a duplicate release suite. |
| PC-EXT-04 teardown/orphan reconciliation | `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`; `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md`; `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md` RH-05/06/12; PC-RT-02 | Explicit provider delete timeout/500, ambiguous deletion, orphan reconciliation and eventual confirmed termination | This remains a useful integration-level gap. Keep execution outcome, cleanup state, job disposition and artifact release distinct. Add a provider teardown case to the later selected-provider implementation plan; no generic CASE ID is created. |
| PC-EXT-05 delayed cost reconciliation | `SECURITY.md` launch/budget constraints; LOOP-14; `RESEARCH/EXECUTION_PROVIDER_RESEARCH.md` cost evaluation | Distinguish measured usage, estimate, pending provider charge, reconciled charge and unknown | Future observability work only, not current lifecycle acceptance. Blocked until explicit budget/provider approval. |
| PC-EXT-06 forged stdout control JSON | `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md` TPM-15; `PRODUCT/EXECUTION_CONTRACT.md` trust/report rules; PC-LC-04 and PC-RT-02 | Expand the negative fixture beyond printed PASS to fake exit, attempt, provider-error and cleanup fields | Add these cases inside the existing producer-authority/terminal-observation tests. Do not treat CASE-09/10 as producer-authentication acceptance. |
| PC-EXT-07 tenant-scoped semantic idempotency | `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md`: D-06 and DR-01..12; `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` PF-01..05; PC-AD-01 and PC-DB-01 | Make the full execution-relevant fingerprint field list obvious to implementers | DR/PF are authoritative and already cover tenant isolation, semantic changes, concurrency, dispatch intent and crash/ack recovery. PC-EXT-07 is a pointer, not a duplicate test suite. |

### Required sequencing correction

The detailed owner-approved research checklists remain proposed and require owner decisions where marked. Sequence any future work as follows:

1. Resolve D-01..D-04 before freezing verdict and event-replay expectations.
2. Resolve D-05 and use PBR/PF before any dispatch or hosted-execution safety claim. Request fingerprint equality is not applied-policy proof.
3. Use DR-01..12 for durable reservation and ambiguous-dispatch recovery; then prove the chosen provider's idempotent-start or authoritative lookup semantics. Do not claim exactly-once provider execution from database idempotency alone.
4. Use RH-01..14 for durable append-only report history and AR-01..14 for artifact release. RH-12 is the cross-store report/artifact publication case; AR-03/05/09/14 cover immutable-object and mutation races.
5. Keep PC-EXT-02 and PC-EXT-04 as identified provider/runtime evidence gaps to refine only after the actual boundary is selected. PC-EXT-05 remains future and budget-blocked.
6. Include PC-EXT-06 as additional hostile stdout fixtures in PC-LC-04/PC-RT-02, not as a separate producer-authentication mechanism.

**No implied approval:** this alignment does not close D-01..D-08, select a provider/store, authorize implementation, or promote any test from SPECIFIED/NOT RUN. The source checklist IDs are the traceability anchors; the PC-EXT labels are navigation aids only.


## 10. Detailed resource-containment and teardown evidence contract

The summary cases PC-EXT-02 and PC-EXT-04 are now expanded in [RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md](RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md). That review defines RES-01..09 and TDN-01..08 as local test-design labels only. They are not canonical LOOP/CASE IDs and do not supersede any existing checklist.

Key clarifications:
- A configured resource request is not necessarily a hard limit. Record the effective per-attempt limit and its authoritative enforcement source.
- CPU bandwidth throttling is not wall-clock termination.
- cgroup `io.max` limits I/O throughput, not disk capacity; `RLIMIT_FSIZE` is per-file, not total workspace quota.
- For cgroup v2, use exact target identity and local event counters; `cgroup.events: populated=0` is process-subtree evidence, not remote-provider resource-deletion proof.
- Keep process-tree empty, provider sandbox destroyed, attached resources released, and billing reconciled as separate observations.
- A delete request accepted or a delete API returning before teardown completes must not produce CLEANUP_CONFIRMED. Reconcile the same stable provider-resource identity until its authoritative terminal state is observed.
- Firecracker's Jailer does not remove the operator's cleanup responsibility. Provider documentation is not independent runtime evidence.

All RES/TDN cases remain SPECIFIED ONLY / NOT RUN. See the detailed review for the source-by-source provider comparison and bounded-test safety rules.


### PC-EXT-02 attribution clarification

The detailed resource review's Section 8 refines RES-02: `memory.events.local:oom_kill` counts processes in the cgroup killed by any OOM killer, so it is not by itself proof that the target cgroup's own `memory.max` caused the kill. Capture effective memory/swap limits, target-local `max`/`oom`/`oom_kill` counter deltas, exact cgroup identity and process membership, trusted termination evidence, and supervisor/sibling health. Do not require an OOM kill for every memory-limit hit because some failures return `-ENOMEM`. Interpret correlated evidence, not one counter.


## 11. Claude review reconciliation: canonical gaps and proof boundaries (2026-11-02)

Claude explicitly reported that the new resource review, lifecycle regression plan and readiness backlog were inaccessible during its review attempt. Its response is therefore a set of adversarial challenges, not a review verdict on those three files. This section records the findings reconciled against the exact canonical acceptance and research-branch sources in this pass.

### Canonical acceptance is not expanded by the supplementary plan

1. There is no canonical cleanup-confirmed LOOP/CASE ID. CASE-05 concerns user cancellation and whether termination is confirmed; CASE-06 concerns provider/worker failure before a trustworthy program result. The first-useful-proof paragraph also names cleanup as a gate, but that is not a standalone teardown acceptance case. TDN remains a supplementary integration-test namespace.
2. The lifecycle status list has no resource-limit status. Do not add resource_limit_exceeded as a canonical status. Preserve resource cause, enforcement layer and terminal evidence separately. OOM, ENOSPC, per-file-size enforcement, PID limit and I/O throttling must not be silently remapped.
3. CASE-07 concerns the configured output limit. CASE-14 concerns output-file path/size safety. Neither proves a total workspace disk quota or I/O throughput boundary.
4. Canonical verdicts remain PASS, FAIL and INCOMPLETE. Mapping a particular resource event to a confirmed program/runtime failure versus infrastructure failure depends on the actual ownership of the limit and trusted terminal evidence; D-01/D-02 remain open wherever the source does not decide this. No verdict rule is approved by this note.
5. LOOP-14 remains a hard cost/authorization gate. Provider-account billing claims, including that charges have stopped, require real provider-boundary evidence after explicit approval. A mock, local estimate, or missing billing telemetry cannot establish a zero charge or stopped billing.

### Review additions mapped to existing supplementary cases

- RES-08 already owns worker/sibling containment and is sharpened to include worker memory/output buffers, namespace/filesystem/credential separation, and a second concurrently running attempt.
- RES-09 already owns descendant termination and is sharpened to include daemonized descendants, escalation beyond graceful termination, independent observation, and exact process-subtree emptiness.
- TDN-01..08 remain the original provider teardown matrix. The resource review now adds TDN-09 (lost create acknowledgement with durable pre-call intent and scoped orphan discovery) and TDN-10 (warm/reused sandbox contamination and stale child/state). TDN-06 additionally rejects cross-attempt resource sharing and stale cleanup observations.
- The source-specific detailed additions and cgroup event interpretation are in [RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md](RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md).

### Required evidence-layer order

Pure-helper semantics → fake-adapter protocol → durable persistence/restart → local Linux cgroup enforcement where that is the actual approved host mechanism → selected-provider/runtime proof. A lost-create-ack orphan-reconciliation test cannot be claimed at the persistence layer until a pre-call intent is durably committed. No fake or pure test proves host isolation or provider teardown. Provider execution remains gated by LOOP-14 and the current $0 constraint.

All PC-LC, PC-AD, PC-DB, PC-RT, RES and TDN cases remain SPECIFIED ONLY / NOT RUN. This reconciliation does not authorize implementation or host tests, select a provider, change canonical acceptance, or close D-01..D-08.
