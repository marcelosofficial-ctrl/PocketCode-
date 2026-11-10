# P40 model-only execution protocol

**Date:** 2026-11-10  
**Status:** PREPARED / NOT AUTHORIZED TO EXECUTE / NOT RUN  
**Target:** `marcelosofficial-ctrl/PocketCode-`, branch `pocketcode-ai-workflow-director-research-2026-10-28`  
**Authority:** P39 gate plan, owner decision register, reconciled Claude/Gemini findings, canonical crosswalk and the 2026-11-10 gap research. This protocol does not authorize source/test edits, schema freeze, adapter selection, device tests, deployment, spend, or changes to canonical LOOP/CASE/D IDs.

## 1. Purpose and boundary

This is the next useful engineering-preparation unit while Claude's additional material is pending. It converts the already reconciled findings into an executable sequence for the existing sequential reference model. It is deliberately not a new review lane and does not duplicate Claude's Apple design, website, context-engineering or provider-cache work.

**Gate remains CLOSED.** The protocol may be reviewed and refined, but it must not be run against or used to modify scripts/tests until the owner gate is explicitly cleared. Existing P39 test-family names are retained. No new canonical or P39 test IDs are created here.

A passing sequential model test would prove only that the model implements the selected semantics. It would not prove database atomicity, cross-process fencing, durable identity, browser storage recovery, transport cancellation, client receipt or production authentication.

## 2. Preconditions and evidence contract

Before an authorized run, pin all of the following in the run record:

1. Repository, branch, commit SHA, source blob SHAs and test blob SHAs.
2. Python version, OS, command, dependency lock/environment and test runner version.
3. Owner dispositions for the relevant OD rows, including explicit deferrals. Silence is not a decision.
4. Canonical mapping and exact existing test-family names from the P39 crosswalk.
5. Initial model state and deterministic authority clock/ID sources used by the fixture.

Every assertion must identify the state before, operation, injected fault, state after, and observable evidence. A test must fail if its critical precondition is absent; do not let an empty collection or skipped branch satisfy a security assertion vacuously.

Record outcomes as PASS, FAIL or NOT RUN. Tag source facts VERIFIED, model expectations INFERRED and unavailable runtime/adapter facts UNKNOWN. Preserve the original event, receipt and conflict evidence on failure.

## 3. Ordered model-only sequence

### Slice A: aggregate/event parity and canonical envelope

**Existing families:** P39-EVENT-05, P39-EVENT-06.  
**Canonical support:** CASE-11, CASE-12, CASE-13, CASE-14, CASE-15, CASE-16; LOOP-07, LOOP-10, LOOP-11.

**A1. Atomic semantic transition**
- Start from a known aggregate version N and its matching event/outbox high-water.
- Apply one state-changing progress transition.
- Assert exactly one version increment and exactly one immutable event/outbox identity for N+1.
- Replay the exact request and assert the original transition/event identity is returned.
- Apply a semantic no-op and assert no version increment, event, outbox item or new terminal transition.
- Inject failure before the model's commit boundary and assert no partial aggregate/event/outbox state is visible.
- Inject failure after commit but before the caller receives the response; replay must recover the committed identity, not create a second transition.

**A2. Terminal transition and replay**
- Exercise each allowed terminal transition from a valid non-terminal state.
- Attempt a second conflicting terminal transition and a post-terminal progress update.
- Assert no silent overwrite, duplicate terminal event or version gap. If the current model does not define the transition, record a specification conflict, not a guessed expected value.

**A3. Canonical event integrity and scope**
- Build a valid first-delivery event with canonical semantic fields and digest.
- Mutate one semantic field while retaining the original digest; consumer must reject/quarantine it.
- Submit a forged first-delivery event with a self-consistent digest but unknown grant, wrong tenant, source, effect or attempt; digest validity must not authorize it.
- Replay the exact producer/event identity and exact canonical bytes; return the original accepted event.
- Reuse that identity with changed bytes or scope; preserve the original and record a conflict.
- Verify canonical serialization is deterministic across key order and rejects ambiguous types/encodings.

**Stop condition:** if the model has no explicit canonical byte encoding or trusted producer boundary, do not invent one in this test plan. Mark the corresponding assertion BLOCKED pending owner/contract decision.

### Slice B: relay ordering, fencing and trusted time

**Existing families:** P39-OUTBOX-04/05, P39-CLOCK-01, P39-ID-01, P39-ORDER-04, P39-CRASH-04.  
**Canonical support:** CASE-11, CASE-13, CASE-16; LOOP-07, LOOP-11, LOOP-12.

**B1. Stale relay worker**
- Worker A claims aggregate sequence N with fence F.
- Advance authority time beyond the lease and let worker B claim with F+1.
- A attempts publish acknowledgement and delivered-marker mutation after takeover.
- Assert both protected mutations reject A atomically; B can complete only the current sequence.
- Assert a worker-provided future or backdated timestamp cannot change lease expiry or take ownership.

**B2. Duplicate delivery and ambiguous acknowledgement**
- Relay publishes event N, then simulate loss of the relay's response before the delivered marker commits.
- Redeliver N. Consumer must deduplicate by stable event identity and semantic digest.
- Assert no duplicate external effect or duplicate terminal event is inferred from delivery.
- Keep publish accepted, consumer processed, external effect completed, delivered marker committed and receipt committed as separate facts.

**B3. Poison predecessor and order**
- Place valid N, malformed/poison N+1 and valid N+2 in one aggregate stream.
- Assert N+2 is not delivered/accepted past the unresolved predecessor.
- Assert visible HOLD/quarantine includes the missing/poison sequence and original evidence.
- Resolve only through an explicit audited repair path; never rewrite the original event or silently skip a sequence.

**B4. Fence continuity**
- Simulate restart, restore, deletion/tombstone and a second instance.
- Assert grant/event identity and fence high-water do not reset or repeat.
- If the sequential model uses process-local counters, mark adapter-level continuity UNKNOWN; do not claim the model proves durable uniqueness.

### Slice C: policy/revocation and receipt binding

**Existing families:** P39-POLICY-02..06, P39-RECEIPT-02, RCP-01..05.  
**Canonical support:** CASE-05, CASE-11, CASE-12, CASE-13, CASE-14, CASE-15, CASE-16; LOOP-07, LOOP-10, LOOP-12.

This slice is conditional on explicit owner choices for OD-02..08. Keep each policy phase separate:
- Revocation before grant commit.
- Revocation after grant commit but before claim.
- Revocation during transfer, only if streaming is selected for MVP.
- Recovery/resume after takeover or revocation.
- Policy change across separate authorities before grant commit.

For each phase, assert the selected policy outcome, current policy epoch, grant identity, fence, receipt revision and artifact object version. A recovered grant lookup is not a fresh authorization to send bytes. A stale or unknown policy epoch must not be treated as allow.

For receipt binding, race a receipt successor against a release-grant reservation in the model's sequential orderings. If successor commits first, an old-receipt request must not obtain a new grant. If grant commits first, it remains pinned to its exact historical receipt/object version. Same idempotency key plus same stable intent recovers the same grant; changed intent conflicts. Rotating authorization proof metadata must not mutate historical grant provenance.

### Slice D: typed exit, output and receipt projection

**Existing families:** EP-01..25, EP-26..35, PYO-CTRL-01..15.  
**Canonical support:** CASE-01..06, CASE-09, CASE-11, CASE-12, CASE-14, CASE-15; LOOP-03..07, LOOP-10..12.

Use a table-driven set of facts, not a precedence-only formatter test. Keep guest outcome, wrapper outcome, host Worker observation, native child exit, termination request, termination acknowledgement, cleanup, output finalization, artifact readback and receipt commit distinct.

Required adversarial cases:
- Guest reports success but trusted wrapper rejects or never completes.
- Worker sends a wrapper-shaped message through a guest-accessible default channel.
- Worker errors or is terminated without a trusted termination acknowledgement.
- Natural child exit is zero but a mandatory policy/egress gate is absent or mismatched.
- Child exits zero, then required output collection or cleanup fails.
- Output callbacks close, but OPFS readback or IndexedDB receipt commit fails.
- Terminal observation arrives, then the process crashes before receipt commit.
- Stale, contradictory or wrong-attempt observations arrive after timeout.

Assert the coordinator projection never derives native child exit from guest/Worker messages, never converts missing evidence to PASS, and never equates cancellation request with completed termination. Execution verdict, lifecycle disposition, collection status, cleanup status, artifact disposition and receipt commit remain separate. Preserve CASE-04 as INCOMPLETE / timed_out until trusted boundary evidence resolves it.

## 4. Cross-layer acceptance and non-vacuity rules

| Layer | What a PASS may establish | What it cannot establish |
|---|---|---|
| Sequential reference model | Deterministic state transition and rejection behavior in the tested model | Atomic database commit, real races, crash durability |
| Adapter conformance | Selected adapter's transactions, conditional writes, fencing and recovery under named build/configuration | Hostile guest isolation or client receipt unless actually exercised |
| Browser/device | Behavior on named browser, OS, origin and device under tested faults | Other devices, permanent backup or physical-media guarantees |
| Transport | Server/transport/client observations actually measured | Client acknowledgement from server-side progress alone |
| Canonical product CASE | End-to-end behavior in the real controlled product boundary | Unexecuted scenarios or supporting model tests |

Do not report supporting P39/EP/PYO tests as canonical CASE passes. A test that only checks a digest against a caller-supplied digest does not prove producer authentication. A lock test that does not attempt a stale write after takeover does not prove fencing. A crash test that does not restart and inspect state does not prove recovery.

## 5. Exit criteria and handoff

A model-only slice is ready to be proposed for execution only after:
- The relevant OD decisions are explicit or explicitly deferred by the owner.
- Existing model APIs can express the scenario without adding semantics by assumption.
- Test assertions map to existing families and preserve canonical IDs.
- The source/test SHA and environment are pinned.
- The owner explicitly opens the P39/P40 gate and authorizes the bounded run.

After a model run, publish exact command/output and source/test pins. Any adapter, browser, device or transport claim remains NOT RUN until separately tested. Claude's additional artifact, when supplied, must be ingested by exact repo/branch/SHA/blob pins and reconciled into the existing matrix before it changes this sequence.

## 6. Current status

- **VERIFIED:** current gate plan and owner register prohibit implementation; OD-01..OD-13 are OPEN; canonical crosswalk distinguishes supporting tests from product acceptance.
- **INFERRED:** the four-slice ordering above minimizes dependency overlap and exposes the highest-risk semantic gaps before adapter work.
- **UNKNOWN:** selected policy outcomes, actual installed Pyodios worker topology, live Pages origin/deployment, durable adapter and target-device behavior.
- **NOT RUN:** all scenarios in this protocol. No code or tests were changed.
