# Shared Contract Golden Fixture Catalogue

**Date:** 2026-11-01  
**Status:** Provisional design and test-data catalogue. NOT a frozen schema, executable fixture set, implementation approval, or acceptance result.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Purpose:** Define reusable cross-project scenarios for the PocketCode/RevDev result-evidence boundary while preserving each product's canonical acceptance suite and native state semantics.

## 1. Decision and scope

Create a shared *semantic* fixture catalogue before defining a shared JSON schema. The fixtures describe observable facts and required invariants, not a universal mutable status object.

Every fixture has two layers:

1. **Shared semantic fixture:** the invariant both projects should preserve where the scenario exists.
2. **Product binding:** the native identifiers, adapter evidence, state labels and acceptance IDs each product uses to prove that invariant.

The shared fixture ID is not a replacement for LOOP, CASE, COORD, DR, P8U, P0-D, RelayRef, AEC or AWC IDs. A conceptual mapping is not acceptance equivalence.

This catalogue deliberately does not prescribe a database, provider, event bus, queue, transport, runtime, or final field names. It does not select an implementation.

## 2. Evidence and interpretation rules

- **Observed fact** means a value supported by an identified trusted source. A client timer, UI label, worker memory, script output or AI assertion is not automatically authoritative.
- **Unknown** is a valid state. Missing evidence must not be filled with a guessed terminal outcome, exit code, publication success or transfer receipt.
- **Execution outcome** describes what happened to one execution attempt.
- **Job disposition** describes what the coordinator is doing with the logical job and its attempts.
- **Evidence capture** describes whether required execution facts were collected and durably retained.
- **Publication state** describes publication of the result/evidence/manifest to a destination.
- **Release decision** describes current authorization to disclose a particular immutable artifact.
- **Transfer state** describes delivery of exact bytes and any verifiable receipt.
- **User-facing verdict** is a derived projection under product-specific acceptance policy. It is not a storage authority for the other axes.
- Every retry/replay must retain the original logical and operation identities. A new execution attempt must have its own identity and evidence.
- Fixtures are test vectors, not proof. Passing pure/fake tests does not establish persistence, provider, Windows runtime, HTTP transfer or device behavior.

## 3. Fixture record template

A future machine-readable fixture should carry, at minimum:

| Field | Meaning |
|---|---|
| `fixture_id` | Stable catalogue identifier, e.g. `SCF-001` |
| `fixture_version` | Version of fixture semantics, independent of contract version |
| `scenario` | Human-readable fault/setup |
| `input_facts` | Minimal facts and source/provenance labels |
| `expected_axes` | Expected execution, coordination, evidence, publication, release and transfer facts |
| `expected_verdict` | Product-specific projection or explicitly unresolved |
| `required_evidence` | Exact observations/identities needed to establish the expectation |
| `forbidden_behaviour` | Unsafe or semantically incorrect transitions |
| `shared_invariant` | The cross-project rule being exercised |
| `product_bindings` | Native acceptance IDs and adapter-specific proof |
| `proof_level` | Pure, fake, persistence, provider, host/runtime, HTTP/artifact or device |
| `status` | Proposed / implemented / run / verified, with evidence reference |

Do not put real secrets, private paths, live credentials, user code, or real provider tokens in golden fixtures. Use deterministic synthetic identities and payloads.

## 4. Golden fixture catalogue

The terms below are semantic expectations. They are not yet serialized enum values. Where an axis is not applicable, record explicit not-applicable semantics rather than inventing a state transition.

### SCF-001: Accepted, not started

**Scenario:** A request is validated and durably accepted, but no provider/process start is confirmed.

- Input facts: authenticated request; accepted job record; no dispatch intent; no provider operation ID; no process-start observation.
- Expected execution: no attempt outcome; `NOT_RUN` or product-native equivalent.
- Expected coordination: accepted/queued, not running.
- Expected evidence: acceptance record only; no terminal execution evidence.
- Expected publication/release/transfer: not attempted; no release.
- Expected verdict: INCOMPLETE / pending, never PASS.
- Required evidence: request/job identity, validation result, durable acceptance evidence, absence of a start authorization in the authoritative record.
- Forbidden: treating accepted/queued as running or succeeded; fabricating exit code 0; exposing an artifact as if generated.
- Shared invariant: acceptance is not execution.
- Product bindings: PocketCode LOOP-02/03 and CASE-06/13 where applicable; coordinator DR reservation cases; RevDev P8U is not the acceptance authority for pre-execution acceptance.
- Proof level: pure + fake coordinator; persistence proof required for durable acceptance claims.

### SCF-002: Dispatch intent committed, provider start acknowledgement unknown

**Scenario:** Durable dispatch intent exists and the provider Start request may have reached the provider, but the caller lost the acknowledgement.

- Input facts: stable job/attempt/provider-token identity; dispatch intent committed; Start call outcome ambiguous; no authoritative lookup result.
- Expected execution: UNKNOWN, not NOT_RUN and not RUNNING unless separately confirmed.
- Expected coordination: reconciliation required for the original attempt.
- Expected evidence: preserve dispatch intent, request fingerprint and provider-call ambiguity.
- Expected publication/release/transfer: not eligible absent terminal evidence.
- Expected verdict: INCOMPLETE.
- Required evidence: durable intent identity, exact attempt and token namespace, call timestamp/trace, lookup evidence or explicit unknown.
- Forbidden: blind second Start; new attempt/token merely because a timeout occurred; interpreting a transient not-found as definitive non-creation.
- Shared invariant: uncertain dispatch is reconciled against the original operation.
- Product bindings: PocketCode CASE-13, DR-05..08, COORD-07..08; future provider integration must prove token semantics. RevDev P8U publication retry is not this scenario.
- Proof level: fake call-order tests, then persistence and provider integration.

### SCF-003: Duplicate request or event, same identity and same content

**Scenario:** The same logical request, provider event or publication operation is delivered more than once with identical immutable content.

- Input facts: same typed identity namespace, same scope and same canonical content/fingerprint.
- Expected execution: unchanged; no additional attempt.
- Expected coordination: idempotent replay or return of the existing record.
- Expected evidence: one logical accepted fact; replay observation may be counted diagnostically without changing the original fact.
- Expected publication/transfer: same operation result, not a second logical publication or transfer unless explicitly modeled as a separate transfer attempt.
- Expected verdict: unchanged.
- Required evidence: identity namespace, scope, canonical content comparison and original durable result.
- Forbidden: duplicate execution, duplicate terminal notification, new report version solely due to retry, or silently replacing original evidence.
- Shared invariant: same-identity/same-content replay is idempotent.
- Product bindings: PocketCode CASE-13 and COORD replay tests; RevDev P8U-04 for identical exact-result collision; P8U-12 for duplicate terminal/audio protection.
- Proof level: pure/fake first; persistence/provider-specific guarantees need their own integration tests.

### SCF-004: Same identity, conflicting content or metadata

**Scenario:** An event, request or artifact is replayed using an existing identity but with changed payload, scope, policy revision or digest.

- Input facts: identity collides; at least one immutable bound field differs.
- Expected execution: no new execution inferred.
- Expected coordination: typed conflict/quarantine/manual reconciliation; original record retained.
- Expected evidence: both observations and conflict diagnostics retained without overwriting the original.
- Expected publication/release/transfer: no publication/release of the conflicting object.
- Expected verdict: derived only from original trusted evidence; conflict itself cannot manufacture PASS.
- Required evidence: both payload digests, identity namespace, scope metadata, policy binding and conflict reason.
- Forbidden: last-write-wins; treating changed payload as a harmless duplicate; replacing a valid result at the same mission/result identity.
- Shared invariant: identity reuse cannot mutate immutable meaning.
- Product bindings: PocketCode DR changed-fingerprint and COORD collision tests; RevDev P8U-05; RelayRef scoped event identity rules. Native IDs remain separate.
- Proof level: pure + fake, then persistence/concurrency.

### SCF-005: Execution confirmed PASS, publication pending retry

**Scenario:** A valid local execution terminal result exists, but remote publication fails transiently.

- Input facts: trusted terminal success; authoritative exit code 0 where required; exact local result identity/hash retained; publication attempt has transient failure.
- Expected execution: PASS remains PASS.
- Expected coordination: execution terminal; publication/reconciliation work pending separately.
- Expected evidence: exact original result and hash remain available and indexed.
- Expected publication: PENDING_RETRY (or product-native equivalent).
- Expected release/transfer: no release/transfer unless separately authorized and published.
- Expected verdict: PocketCode PASS only if its LOOP-03 evidence predicate is met; RevDev P8U execution remains PASS.
- Required evidence: exact terminal result, result path/hash or immutable ref, publication operation identity, original remote error and retry metadata.
- Forbidden: rewriting execution to FAIL/NOT_RUN because publication failed; rerunning the product mission; duplicate terminal audio; replacing the exact result with a new run.
- Shared invariant: post-execution publication failure does not rewrite execution outcome or trigger execution replay.
- Product bindings: RevDev P8U-01..04 and P8U-07; PocketCode shared projection only if an equivalent publication adapter exists. LOOP-03 is the verdict authority, not a publication retry test.
- Proof level: RevDev isolated Windows/runtime P8U gate; PocketCode persistence/publication integration if implemented. Current RevDev host/runtime evidence remains UNKNOWN.

### SCF-006: Execution confirmed FAIL, publication pending retry

**Scenario:** A program failure is confirmed and the failure report cannot yet be published.

- Input facts: trusted terminal program failure or non-zero exit; immutable failure evidence; transient publication failure.
- Expected execution: FAIL / PROGRAM_FAILED under the native execution vocabulary.
- Expected coordination: execution terminal; publication retry pending.
- Expected evidence: actual error, exit code if observed, bounded partial output and original failure identity retained.
- Expected publication: PENDING_RETRY.
- Expected verdict: PocketCode FAIL only on confirmed failure; RevDev execution FAIL remains FAIL.
- Required evidence: terminal source, actual failure detail, exact report/result identity and publication error.
- Forbidden: converting failure to INCOMPLETE solely because publication is pending; converting it to PASS; rerunning merely to make the report publish; losing partial diagnostics.
- Shared invariant: publication state is orthogonal for both successful and failed executions.
- Product bindings: PocketCode LOOP-04/07 and CASE-02/03/12; RevDev publication retry design should mirror P8U-01's no-rerun invariant without claiming P8U explicitly covers this exact failure fixture.
- Proof level: pure projection + publication fake; persistence and product-specific runtime integration.

### SCF-007: Cancellation requested, execution still active

**Scenario:** User requests cancellation, but the provider/process has not confirmed termination.

- Input facts: cancellation request accepted; authoritative latest observation still says active or no termination acknowledgement exists.
- Expected execution: RUNNING or UNKNOWN according to authoritative observations; not CANCELLED yet.
- Expected coordination: CANCEL_REQUESTED / reconciliation pending.
- Expected evidence: request identity/time and subsequent termination observations separately retained.
- Expected publication/release/transfer: no terminal report claiming cancellation until proof; no release based on presumed completion.
- Expected verdict: INCOMPLETE while unresolved.
- Required evidence: cancellation operation ID, attempt/provider operation ID, authoritative process/provider observation and termination proof when available.
- Forbidden: marking CANCELLED from button press, browser abort or client timeout; silently starting a replacement attempt while the old one may still run.
- Shared invariant: cancellation intent is not termination.
- Product bindings: PocketCode LOOP-05 and CASE-05; coordinator cancellation and DR recovery semantics. RevDev process-tree termination acceptance remains a separate native host test.
- Proof level: fake + persistence; actual provider/Windows process integration required.

### SCF-008: Stale worker resumes after ownership/fencing takeover

**Scenario:** Worker A loses its lease; worker B obtains a newer durable fencing epoch; A resumes and attempts state mutation.

- Input facts: same job/attempt; A has epoch n; B has epoch n+1; A attempts dispatch, terminal projection, cleanup, report or publication mutation.
- Expected execution: authentic late execution evidence may still be ingested through trusted ingress; stale worker authority does not change the execution facts.
- Expected coordination: A's protected mutations rejected; B remains current coordinator.
- Expected evidence: stale-write conflict and any authentic late source evidence retained distinctly.
- Expected publication/release/transfer: stale A cannot publish or release artifacts.
- Expected verdict: no stale projection may replace the current derived view.
- Required evidence: durable epoch/version, conditional write result, source-event authentication and mutation audit.
- Forbidden: treating lease expiry as proof old process stopped; dropping authentic late evidence merely because worker is stale; accepting stale writes; permitting direct provider Start outside coordinator gate.
- Shared invariant: fencing protects coordinator authority but does not itself terminate an external process/provider call.
- Product bindings: PocketCode STALE-01..05 proposed extensions, COORD-05/11/12 and DR-09/10; RevDev host process/watcher tests require separate source/runtime evidence. No canonical LOOP/CASE equivalent proves fencing.
- Proof level: fake + real persistence concurrency; provider integration if external Start is in scope.

### SCF-009: Out-of-order completion for distinct attempts

**Scenario:** Two distinct runs/attempts finish in an order different from their start order.

- Input facts: distinct native run/attempt identities; trusted terminal observations; completion order reversed.
- Expected execution: each outcome remains bound to its own attempt.
- Expected coordination: each job/attempt reaches its own disposition; no cross-binding.
- Expected evidence: outputs, exit codes, reports and artifacts remain attached to correct attempt.
- Expected publication/release/transfer: exact result for each attempt; no mutable latest pointer used as identity.
- Expected verdict: each verdict independently derived.
- Required evidence: start identities, attempt/run IDs, terminal observations and exact result refs.
- Forbidden: crossing outputs, overwriting prior result, regressing a latest pointer, or assuming sequence/start order equals completion order.
- Shared invariant: identity binding survives concurrency and reordering.
- Product bindings: PocketCode CASE-16; RevDev P8U-08 for older exact result publication while newer mission advances LATEST_RESULT; product-specific queue/run tests remain separate.
- Proof level: pure/fake plus persistence; host/runtime for RevDev.

### SCF-010: Terminal evidence missing or contradictory

**Scenario:** No trusted terminal observation exists, or multiple trusted-looking observations conflict for the same attempt.

- Input facts: missing exit/terminal result, or conflicting terminal events with authenticated scope but inconsistent outcome/time/policy.
- Expected execution: UNKNOWN until deterministic trusted reconciliation resolves it; preserve all raw observations.
- Expected coordination: reconciliation/manual review, not silently terminal success.
- Expected evidence: missing-evidence reason or immutable conflict set and provenance.
- Expected publication/release/transfer: no success publication/release based on incomplete evidence.
- Expected verdict: INCOMPLETE unless product-specific policy has confirmed failure evidence.
- Required evidence: attempt binding, source namespace, source event IDs, sequence/timestamp semantics, terminal provenance and conflict diagnostics.
- Forbidden: inventing exit code; accepting script-printed PASS; last-write-wins; discarding contradictory events; using arrival order as authority without contract.
- Shared invariant: terminal truth requires trusted, scoped, reconciled evidence.
- Product bindings: PocketCode LOOP-03/05, CASE-06/09/10/11; COORD-01..05/11/12 and D-04; RevDev P8U-09 covers no-local-terminal fallback but not PocketCode verdict semantics.
- Proof level: pure reducer tests + authenticated ingress + persistence/reconciliation.

### SCF-011: Runtime limit versus collector truncation versus report display truncation

**Scenario:** Three superficially similar short-output cases have different causes.

A. Runtime-enforced output/resource limit terminates or rejects execution.  
B. Collector captures only a bounded prefix/suffix while execution itself completes.  
C. Report formatter shortens already-collected evidence for display/copy size.

- Input facts: separate flags and provenance for runtime enforcement, collector completeness, and presentation truncation.
- Expected execution: case A follows the still-open product policy for limit-caused termination; case B preserves the actual terminal outcome if trusted completion exists; case C never changes execution outcome.
- Expected coordination: only A may alter execution disposition; B/C are evidence/report conditions.
- Expected evidence: explicit per-stream collection state and separate runtime/collector/display truncation facts.
- Expected publication/release/transfer: no claim of complete evidence where capture is partial; report projection identifies what was omitted.
- Expected verdict: do not infer a universal verdict for A until D-01 is decided; B/C do not automatically turn a trusted exit-0 run into FAIL.
- Required evidence: configured runtime cap, enforcement source, observed bytes, collector cap/completeness, report cap and exact truncation markers.
- Forbidden: one generic `truncated=true` field; calling report-display truncation a runtime failure; claiming complete stdout/stderr when only a prefix was captured.
- Shared invariant: truncation dimensions must not be collapsed.
- Product bindings: PocketCode LOOP-07 and CASE-07/12, D-01 and D-03; RevDev report/evidence capture and P0-D native acceptance. No automatic equivalence.
- Proof level: pure formatter/collector tests; runtime integration for A and collector integration for B.

### SCF-012: Artifact-free success because artifacts are not required

**Scenario:** The trusted task definition requires no generated files; execution succeeds and no artifacts exist.

- Input facts: trusted task definition says artifact expectation NOT_REQUIRED; terminal success and exit 0 observed; artifact list empty.
- Expected execution: PASS/succeeded.
- Expected coordination: terminal success.
- Expected evidence: execution evidence present; artifact expectation explicitly NOT_REQUIRED.
- Expected publication/release/transfer: artifact publication/release/transfer not applicable; report publication may still occur independently.
- Expected verdict: PASS where task acceptance is satisfied.
- Required evidence: trusted task requirement, terminal evidence, exit code and explicit artifact expectation.
- Forbidden: inferring NOT_REQUIRED solely from empty artifact list; turning valid success into failure because there is no file; creating a dummy artifact.
- Shared invariant: artifact existence is conditional on trusted task requirements.
- Product bindings: PocketCode LOOP-10 and artifact-release checklist; coordinator artifact semantics; RevDev P8U does not make artifacts universally required.
- Proof level: pure contract/projection + adapter tests.

### SCF-013: Evidence cleanup attempted before durable capture

**Scenario:** Temporary workspace/process cleanup runs before required output, exit status or metadata have been durably captured.

- Input facts: execution terminal or believed terminal; required evidence remains only in ephemeral workspace/worker memory; cleanup request begins.
- Expected execution: preserve observed terminal fact if trustworthy; do not invent missing data.
- Expected coordination: cleanup blocked or held pending evidence capture; if cleanup already occurred, record evidence loss/unknown explicitly.
- Expected evidence: capture state NOT_CAPTURED/PENDING/FAILED/UNKNOWN, with exact missing fields and cleanup operation identity.
- Expected publication/release/transfer: no publication represented as complete if required evidence is absent; no artifact release from unverified bytes.
- Expected verdict: INCOMPLETE if required terminal evidence is missing; otherwise derive only from captured trusted evidence.
- Required evidence: cleanup intent/ack, evidence manifest, capture timestamps, durable object references and missing-evidence record.
- Forbidden: destructive cleanup before required capture; treating worker memory as durable evidence; claiming complete report after evidence loss.
- Shared invariant: evidence preservation precedes destructive cleanup.
- Product bindings: PocketCode coordinator cleanup/output/report sequence, LOOP-07/10; RevDev P8U-09 fallback and reliability P0 recovery plans. P8U's exact local terminal condition is distinct.
- Proof level: fake call-order, then persistence/crash and host/runtime integration.

### SCF-014: Release authorized, transfer not started

**Scenario:** A current release decision authorizes a specific immutable artifact, but no transfer has begun.

- Input facts: valid release decision bound to exact artifact/object version/digest; no transfer ID/start event.
- Expected execution: unchanged historical execution outcome.
- Expected coordination: terminal; no execution retry.
- Expected evidence/publication: artifact and manifest are published/verified as required.
- Expected release: authorized for the stated principal/scope/time.
- Expected transfer: NOT_STARTED.
- Expected verdict: historical execution verdict unchanged; UI must not say downloaded/received.
- Required evidence: principal, policy revision, release decision ID, exact object version/digest and absence/presence of transfer start.
- Forbidden: equating release authorization with bytes sent, download started or client receipt; treating PASS as a bearer token.
- Shared invariant: authorization is distinct from transfer.
- Product bindings: PocketCode artifact-release checklist and proposed REL-01..03; no LOOP criterion alone proves release authorization.
- Proof level: persistence + authenticated API boundary.

### SCF-015: Partial transfer or interrupted client delivery

**Scenario:** Transfer starts for an authorized immutable artifact but connection fails before the expected byte count/digest receipt is verified.

- Input facts: transfer ID; exact immutable object version; bytes sent/acknowledged; interruption; no complete client receipt.
- Expected execution: unchanged.
- Expected coordination: terminal; transfer recovery is separate from execution.
- Expected evidence: transfer marked PARTIAL/ABORTED/UNKNOWN as supported; byte count and retry linkage preserved.
- Expected publication/release: remains published; authorization rechecked for any resumed transfer under the chosen policy.
- Expected transfer: not CLIENT_VERIFIED without a valid receipt/integrity check.
- Expected verdict: execution verdict unchanged; delivery shown incomplete.
- Required evidence: transfer ID, object version/digest, expected/actual bytes, range/retry data and receipt verification if available.
- Forbidden: claiming complete download from server-side stream completion alone; resuming a mutable path; silently changing artifact bytes during range retry.
- Shared invariant: partial delivery is not verified receipt.
- Product bindings: PocketCode artifact-release checklist and proposed REL-02/03; device acceptance is separate from server HTTP proof.
- Proof level: HTTP/artifact integration, then device test for client-side receipt.

### SCF-016: Report append acknowledgement lost

**Scenario:** Immutable report append may have committed, but caller lost acknowledgement.

- Input facts: stable append operation identity; evidence snapshot/version; append response ambiguous.
- Expected execution: unchanged.
- Expected coordination: report reconciliation pending; query original append identity.
- Expected evidence: one immutable report version or explicit unresolved commit state.
- Expected publication: no duplicate report version from a retry of the same append operation.
- Expected verdict: same projection for same evidence snapshot; later evidence requires a new version.
- Required evidence: append operation ID, report/job identity, expected version and durable lookup result.
- Forbidden: generating a new append ID after timeout; mutating an issued report; claiming durable history from in-memory append.
- Shared invariant: report append retries are idempotent and report versions immutable.
- Product bindings: PocketCode report-history checklist and coordinator COORD tests; RevDev exact-result JSON publication is not the same as PocketCode report history.
- Proof level: fake + persistence concurrency/crash injection.

### SCF-017: Publication partially commits across stores

**Scenario:** Artifact object write succeeds but manifest/report publication fails, or one side commits while acknowledgement is lost.

- Input facts: stable publication operation ID; object and manifest/report stores have independent commit outcomes.
- Expected execution: unchanged.
- Expected coordination: publication PENDING/RECONCILING until all required references are consistent.
- Expected evidence: exact object version/digest and per-store commit/lookup evidence.
- Expected publication: not PUBLISHED until required object/manifest/report consistency predicate is met.
- Expected release/transfer: denied while publication is partial or quarantined.
- Expected verdict: execution verdict unchanged.
- Required evidence: operation ID, immutable object identity, manifest/report versions and reconciliation trace.
- Forbidden: assuming cross-store atomicity; exposing orphan object or partial manifest; overwriting a conflicting object.
- Shared invariant: publication requires a verified consistent durable set.
- Product bindings: PocketCode PUB-01/02 proposed and artifact checklist; RevDev P8U-04/05 exact-result idempotency/conflict cases, noting its GitHub publication path is product-specific.
- Proof level: persistence + artifact-store integration.

### SCF-018: Newer result advances latest pointer while older exact result is republished

**Scenario:** A newer independent execution completes while an older result is being republished after transient publication failure.

- Input facts: older exact result identity/hash and newer independent result identity; both valid; older publication retried.
- Expected execution: both outcomes unchanged.
- Expected coordination: separate job/attempt histories.
- Expected evidence: each result remains immutable and individually addressable.
- Expected publication: older exact result may be published without moving a latest pointer backwards.
- Expected verdict: each result's verdict remains bound to its own evidence.
- Required evidence: exact per-run result refs, ordering/creation metadata and latest-pointer update policy.
- Forbidden: overwrite newer LATEST_RESULT/HANDOFF with stale older content; treating latest pointer as exact result identity.
- Shared invariant: immutable historical results are not interchangeable with mutable latest pointers.
- Product bindings: RevDev P8U-08; PocketCode CASE-16 is related only in identity preservation, not the same publication scenario.
- Proof level: RevDev isolated Windows/runtime publication recovery; PocketCode persistence if it introduces latest pointers.

## 5. Fixture-to-native-acceptance crosswalk

This table is deliberately many-to-many and conservative. “Related” means the native test exercises part of the invariant, not that it proves the whole shared fixture.

| Shared fixture | PocketCode native references | RevDev native references | Main proof boundary |
|---|---|---|---|
| SCF-001 | LOOP-02/03; CASE-06/13 | DR reservation/intent cases, where applicable | Durable coordinator |
| SCF-002 | CASE-13; DR-05..08; COORD-07..08 | No direct P8U equivalent | Provider dispatch/idempotency |
| SCF-003 | CASE-13; COORD replay | P8U-04, P8U-12 | Idempotency + exact identity |
| SCF-004 | DR fingerprint conflict; COORD collision | P8U-05 | Immutable identity/conflict |
| SCF-005 | LOOP-03 only for execution verdict; no current native publication-retry CASE | P8U-01..04, P8U-07 | Publisher recovery |
| SCF-006 | LOOP-04/07; CASE-02/03/12 | Proposed analogous publisher behavior; no direct P8U exact match | Failure evidence + publisher |
| SCF-007 | LOOP-05; CASE-05 | Native process cancellation/termination tests, not P8U | Provider/host termination |
| SCF-008 | COORD-05/11/12; DR-09/10; proposed STALE-01..05 | Host/watcher concurrency and guard tests; not established by P8U | Fencing/persistence/host |
| SCF-009 | CASE-16 | P8U-08 | Run/result identity |
| SCF-010 | LOOP-03/05; CASE-06/09/10; COORD-01..05/11/12 | P8U-09 only for no-local-terminal fallback; RelayRef event scope | Terminal evidence trust |
| SCF-011 | LOOP-07; CASE-07/12; D-01/D-03 | Report capture and P0-D | Runtime/collector/formatter |
| SCF-012 | LOOP-10 and artifact checklist | No universal artifact requirement in P8U | Task artifact expectation |
| SCF-013 | LOOP-07/10; coordinator cleanup ordering | P8U-09 and P0 reliability plan, distinct conditions | Evidence persistence/cleanup |
| SCF-014 | Artifact-release checklist; proposed REL-01 | No direct P8U release authorization proof | Current authorization |
| SCF-015 | Artifact-release checklist; proposed REL-02/03 | No direct P8U client receipt proof | HTTP/device transfer |
| SCF-016 | Report-history persistence checklist | Not equivalent to exact-result publisher | Durable append |
| SCF-017 | PUB-01/02 proposed; artifact checklist | P8U-04/05 cover GitHub exact-result collision only | Cross-store publication |
| SCF-018 | CASE-16 partial relation only | P8U-08 | Immutable result vs latest pointer |

## 6. Product-specific proof requirements

### PocketCode

- Keep LOOP and CASE IDs unchanged.
- Add shared fixture IDs as supplemental references in test metadata, not as replacements.
- A local iPhone/browser comparator can prove workflow, report formatting and user-facing honesty; it cannot prove hosted provider idempotency, durable reservation, multi-tenant isolation, server-enforced limits or artifact-store guarantees.
- CASE-13 requires the selected backend/provider to establish idempotency semantics. A fake adapter can prove call ordering only.
- D-01 remains open: do not freeze the verdict mapping for runtime-limit-caused termination.
- D-03 remains open: required streams and acceptable partial capture are case-specific.
- D-04 remains open: authenticated event identity/scope/replay contract.
- D-05 remains blocked: applied-policy binding at actual dispatch.
- D-06..D-08 remain unproven at real durable/provider/report boundaries.
- Current provider/runtime remains unselected; $0 and explicit approval gates remain in force.

### RevDev

- Keep P8U-01..12, P0-D, RelayRef and native host/runtime acceptance unchanged.
- P8U's execution/publication vocabulary is authoritative for that acceptance plan: execution `NOT_RUN/RUNNING/PASS/FAIL`; publication `NOT_ATTEMPTED/PENDING_RETRY/PUBLISHED/PERMANENT_ERROR`; remediation remains separate.
- SCF-005 maps closely to P8U-01..04/07. SCF-006 is a useful extension, not an assertion that P8U currently covers failure-result publication retry.
- P8U is `SPEC_ONLY_NOT_IMPLEMENTED` in the retrieved authority. Windows/PowerShell/runtime acceptance remains NOT RUN/BLOCKED until PC access and fresh evidence.
- Never replay or mutate the recovered original P8U result as a test fixture.
- The local exact result and hash, not LATEST_RESULT alone, are the recovery identity for P8U.

## 7. Proposed fixture execution ladder

1. **Semantic review:** confirm each fixture is internally consistent; no schema or implementation decision implied.
2. **Pure golden vectors:** derive verdicts and typed projections from supplied trusted/untrusted facts; test malformed, missing and contradictory inputs.
3. **Fake adapter:** assert exact call order, stable operation identities, no duplicate start, and fail-closed publication/release behavior.
4. **Persistence:** prove atomic reservation, fencing CAS, idempotent append, immutable versions, restart and crash recovery.
5. **Provider/host:** prove real Start idempotency, authoritative lookup, cancellation/termination, Windows process behavior and policy binding.
6. **Artifact/API:** prove exact object identity, authorization races, partial transfer and integrity receipts.
7. **Device/product:** prove iPhone/browser workflow, report copy, file import/export and truthful presentation.
8. **Operational governance:** separately authorize any account, provider, workload, spend, deployment or host mutation.

A fixture may pass one level without passing any higher level. Report the proof level every time.

## 8. Open decisions intentionally not settled here

- Whether PocketCode exposes one result envelope or separate job, attempt and report resources. Current crosswalk recommends a task-linked result/evidence envelope referencing separate job/attempt records.
- Exact field names, enum strings, nullability, unknown representation and schema version policy.
- Which evidence streams are mandatory for each task class.
- D-01 runtime-limit verdict projection; D-03 partial output requirements.
- Event authentication, source namespaces and ordering semantics under D-04.
- Provider token scope/retention and definitive-not-created semantics under D-06.
- Durable report append/version model under D-08.
- Release authorization lifetime, revocation and transfer receipt requirements.
- Whether any common code is justified after independent validators consume the same fixtures.

## 9. Current status and non-actions

- This catalogue is proposed documentation only.
- No JSON Schema, fixture JSON, production API, implementation or executable tests were created.
- No test was run and no evidence level was promoted.
- No provider, account, store, runtime, queue or architecture was selected.
- No source code, PR #2, PR #3, default branch, Actions workflow, deployment, PC state or live queue was changed.
- No spending or workload was authorized.

**Recommended next review:** Claude should assess feasibility and native identity binding; Gemini should red-team omissions, unsafe transitions and fixture-to-acceptance mapping. Their review must preserve the explicit distinction between shared semantic coverage and product-specific proof.
