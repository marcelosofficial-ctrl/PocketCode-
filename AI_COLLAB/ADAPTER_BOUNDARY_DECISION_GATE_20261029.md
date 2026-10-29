# PocketCode adapter-boundary decision gate — 2026-10-29

**Status:** Research aid only. No adapter selected, no provider run, no code/tests, and no canonical contract or PR changes.

## Why this gate exists

The report-provenance question cannot be settled in the abstract. Different execution locations expose different process boundaries. Do not assume that an on-device Python app, browser-local Pyodide, and a future server-side provider have the same wrapper/child process model.

## Candidate paths from existing research

| Path | Evidence already documented | Critical unknowns before it can support the PocketCode proof |
|---|---|---|
| Existing iPhone Python app (Pyodios comparator) | Prior public-source review says its documentation describes local CPython/Pyodide, project folders, CSV/JSON preview, real files, and iOS Files/share-sheet import/export. | Whether it provides authoritative per-run lifecycle/exit evidence, structured bounded stdout/stderr, collector-failure provenance, and a machine-readable timeout/termination state. No hands-on test was run. |
| Browser-local Pyodide | Existing research treats it as conditional on practical iPhone Safari file import/export. | Actual iOS file flow, runtime termination/control limits, output-file creation/export, and authoritative evidence. Not demonstrated. |
| Provider-neutral server execution contract | The proposed contract defines lifecycle, bounded output, explicit unknown states, fixed limits, authenticated output access, and provider-neutral adapter goals. | Provider and adapter are deliberately unselected; no live provider, security boundary, timeout termination, report mapping, or recovery behavior has been verified. |

These are not equivalent implementation options. The first is a comparator for whether an existing local app already meets the user need; the third is a future product architecture. Do not blend their assumptions or treat documentation as execution evidence.

## Decision sequence

1. **Clarify the product proof:** is the immediate target to validate whether an existing iPhone app already solves the fixed CSV task, or to design a PocketCode-owned execution service? Keep the first comparator cheap and separate from the hosted API proposal.
2. **Inspect the real boundary:** identify which component launches user code, which component observes its exit, and whether any wrapper/collector can fail independently.
3. **Prove the evidence source:** identify who authoritatively reports terminal status, child exit, timeout/termination, stdout/stderr completeness, and output files. Unknown remains unknown.
4. **Only then map fields:** if wrapper and child are the same process boundary, do not add separate wrapper/child fields. If separate, preserve independent observations. If partial diagnostic collection is possible, model that explicitly rather than inferring it from empty/unavailable strings.
5. **Run the fixed success and malformed-input cases only after a path is explicitly authorized and actually available.** Fresh workspace per case; verify exported file bytes and report evidence, not merely printed JSON.

## Existing constraints retained

- Budget remains $0. No accounts, billing, provider workload, Actions, deployment, or installs under this research-only step.
- Do not modify PR #2, PR #3, or the canonical contract without explicit authorization.
- Do not claim a test or runtime comparison was executed. Current status remains NOT RUN.
- The FAILED-versus-INCOMPLETE disposition question stays unresolved; artifact release remains an independent fail-closed gate.

## Sources within this repository

- `PRODUCT/EXECUTION_CONTRACT.md` on `main`: provider-neutral proposal; provider-specific adapter remains an open decision.
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` on `main`: truthful PASS/FAIL/INCOMPLETE and diagnostic requirements.
- `AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md` on the research branch: Pyodios and browser-local Pyodide comparator status.
- `AI_COLLAB/OPEN_SOURCE_REUSE_AUDIT_20261029.md` on the research branch: wrapper/child and diagnostic provenance truth table.

## D-05 — Policy-revision/dispatch falsification checklist (specified only; NOT RUN)

### Invariant
A run may start only when the exact policy revision approved for the attempt is bound to that attempt at the trusted dispatch boundary. A policy read, local cache flag, request fingerprint, or second read by itself does not prove that the same revision was applied when execution starts. An acceptable future boundary must provide either an immutable per-attempt policy configuration or a provider/runtime-enforced atomic/conditional start that rejects a changed revision (for example, a documented revision/ETag precondition). These are alternatives to evaluate, not claims about any currently selected provider.

### Minimal falsification cases

| ID | Setup | Required result | Evidence level if executed only with a fake |
|---|---|---|---|
| PBR-01 | Inspect chosen boundary contract/API for an immutable per-attempt policy binding or atomic conditional dispatch primitive | If neither exists or its guarantee is undocumented, mark policy barrier BLOCKED; a pair of reads is not enough | SPECIFIED ONLY / design review |
| PBR-02 | Expected policy revision missing, stale, pending, unknown, or mismatched before dispatch | Reject before start; dispatch count is exactly zero; preserve reason without exposing secrets | Coordinator behavior only |
| PBR-03 | Prepare captures R1, then policy changes to R2 in the dispatch race window | The actual conditional-start primitive rejects R1; no workload starts; dispatch count is zero | Fake proves only the coordinator branch, not real atomicity |
| PBR-04 | Policy content appears equivalent but the authoritative revision/ETag changes (including an R1 → R2 → R1-style race where supported) | Follow the contract's exact revision semantics; never infer the captured token still applies from a stale cached value | Fake can model the state transition only |
| PBR-05 | Attempt record is missing the expected/applied revision, or authoritative applied revision differs from the required revision | Do not claim the barrier is verified or project PASS; if the execution boundary may already have started, quarantine artifacts and treat the control as a blocker/incident requiring reconciliation | Fake validates projection only |
| PBR-06 | Two concurrent dispatch attempts race with a policy update | Each start is atomically bound to one allowed immutable revision or rejected; no attempt starts under an unapproved/mixed revision | Requires concurrency test against actual primitive for integration evidence |
| PBR-07 | Start may have been accepted but acknowledgement is lost | Lookup the original job/attempt and its bound policy revision; if lookup is UNKNOWN, do not redispatch and do not claim policy application or PASS | Fake proves reconciliation logic only |

### Evidence required before a hosted safety claim

- Exact selected provider/runtime/API version and the documented semantics of the conditional/immutable-policy primitive.
- Code/configuration showing the expected revision is bound to the specific attempt at the actual start boundary, not merely checked earlier by the client/coordinator.
- Authoritative evidence linking the started attempt to the applied policy revision, with authenticated provenance.
- A deterministic fake test for coordinator branching plus a separate integration/race test against the selected boundary. Record dispatch counts, observed started attempts, expected/applied revision IDs, and failure modes.
- Negative cases for missing/stale/mismatched revision and ambiguous acknowledgement; any unknown result remains UNKNOWN/INCOMPLETE and cannot be reinterpreted as a successful barrier.

### Stop conditions

Stop and mark BLOCKED if the boundary only supports read-then-dispatch without an enforceable revision condition; if the attempt cannot prove which revision it ran under; if the revision can change outside the guarded transaction; or if the only evidence is a unit/fake test, a configuration claim, or an untrusted program-reported value. No provider is selected and no real boundary test is authorized by this checklist.

Related anchors: D-05 in `OWNER_DECISION_REGISTER_20261029.md`; COORD-06; LOOP-12/14; CASE-15. This checklist specifies future falsification work and does not implement or verify the policy barrier.
## D-05 companion — policy-content fingerprint vs applied-revision binding (specified only; NOT RUN)

These are two distinct invariants and must not be substituted for one another:

- **Semantic request fingerprint:** canonically identifies the request as accepted for idempotency/conflict detection, including the effective policy content under a strict, versioned policy-value schema.
- **Applied-policy binding:** proves which immutable policy revision/configuration the particular execution attempt actually ran under at the trusted dispatch boundary.

A SHA-256 fingerprint of a request or `effective_policy` value proves only which canonical inputs were hashed. It does **not** prove that the execution boundary applied that policy. Conversely, an applied revision token does not alone prove that a retry with changed request semantics is the same idempotent request. The request fingerprint and applied-revision evidence must be linked to the same authenticated job/attempt without conflating their meanings.

### PF-01..PF-05 — minimal falsification cases

| ID | Setup | Required result | Evidence boundary |
|---|---|---|---|
| PF-01 | Pass nested effective-policy values with integer/bool/null/list keys, non-string keys, unsupported object types, non-finite numbers, or keys that collide after any specified normalization | Reject at validation before fingerprint/reservation/dispatch; never rely on JSON serialization coercion to define meaning implicitly. Valid recursively string-keyed JSON values remain accepted. | Pure validation/fingerprint test; does not prove applied policy |
| PF-02 | Equivalent valid policy mappings with different insertion order, plus semantically different mappings/values | Canonical fingerprint is stable for equivalent accepted policy objects and differs for changed effective policy values under the documented schema/version. Preserve the exact policy schema/fingerprint version. | Pure helper test; does not prove provider enforcement |
| PF-03 | Reuse tenant + idempotency key with changed policy content, required policy revision, runtime/source/input semantics, or policy-schema version | Conflict; no second dispatch and no substitution of the previous job/report/artifacts for a changed request. | Coordinator + persistent idempotency integration needed for durability/concurrency |
| PF-04 | Fingerprint request with policy content P1, then the authoritative policy revision changes before the run starts (P1 content but revision R1 becomes stale, or policy content changes to P2/R2) | Actual dispatch boundary must bind the attempt to an immutable allowed revision or reject atomically; expected/applied revision mismatch yields zero start. A successful fingerprint check must not waive this barrier. | Fake can test coordinator branch; actual atomicity requires chosen-boundary race test |
| PF-05 | Attempt record contains request fingerprint but applied revision is missing/mismatched, or says R1 while authoritative source says R2 | Policy barrier remains UNKNOWN/BLOCKED or failed; no PASS and no artifact release. Preserve both request fingerprint and applied-revision evidence and reconcile the attempt; do not reconstruct the missing applied revision from the fingerprint. | Coordinator projection plus authenticated integration evidence |

### Required attempt linkage

Before a future implementation is called conformant, the trusted record for one attempt must be able to associate, at minimum:

- request fingerprint + fingerprint/schema version;
- normalized effective policy content or an immutable reference to that exact policy object;
- required policy revision/token and its source/authority;
- applied policy revision/token bound to the actual attempt/start operation;
- tenant/job/attempt identity and dispatch acknowledgement/ambiguity evidence;
- authenticated evidence provenance and coordinator sequence/version.

This list is a conceptual acceptance contract, not a frozen public schema. Do not store secrets or credentials in the fingerprint record; use a bounded, validated policy schema and non-secret revision/reference metadata.

### Stop rule

If only the request fingerprint is known, report **request semantics identified; applied-policy binding NOT PROVEN**. If only a revision label is present without evidence tying it to the started attempt, likewise mark the barrier NOT PROVEN. A fake test can validate deterministic hashing and coordinator refusal rules, but it cannot prove that a real runtime/provider applied the policy. No provider is selected and no implementation or runtime test is authorized here.

Related: FLA-11 in `FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md`; D-05 in `OWNER_DECISION_REGISTER_20261029.md`; PBR-01..07 above; COORD-06; LOOP-12/14; CASE-15.