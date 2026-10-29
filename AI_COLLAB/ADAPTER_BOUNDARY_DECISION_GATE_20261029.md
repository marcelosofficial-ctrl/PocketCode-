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