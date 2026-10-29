# PocketCode — Implementation Readiness Backlog

**Date:** 2026-10-29  
**Status:** Planning artifact only — SPECIFIED ONLY / NOT RUN.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Authority:** This backlog orders work; it does not approve design decisions, freeze schemas, select infrastructure, authorize workloads, or change canonical acceptance.

## Objective

Convert the existing boundary research into a short dependency-ordered backlog so implementation can begin only where semantics are stable and the required proof boundary is available. Avoid writing a new implementation spec for every unresolved question.

## Current gate summary

| Gate | Current state | Can proceed now? | Closure evidence |
|---|---|---|---|
| G0 — owner semantics D-01..D-04 | OPEN | Review and decision preparation only | Explicit owner decisions recorded; canonical LOOP/CASE IDs and meanings preserved |
| G1 — boundary / policy / cost D-05 | BLOCKED | Contract review only | Selected boundary, explicit cost/account approval, enforceable policy-at-dispatch proof |
| G2 — pure contract helpers | NOT STARTED / NOT RUN | Design/test inventory may proceed; implementation needs authorization | Pinned source, schemas, reproducible unit tests, strict evidence labels |
| G3 — durable reservation and dispatch recovery | BLOCKED on store/provider semantics | No real implementation claim | Persistence concurrency/restart evidence plus provider-specific lookup/idempotency evidence |
| G4 — trusted evidence and report history | BLOCKED on identity decisions/store | Test design only | Authenticated scope binding, immutable events, atomic monotonic versions, restart/concurrency evidence |
| G5 — artifact publication/release | BLOCKED on store/API and owner semantics | Threat-model/test design only | Actual store/API/HTTP evidence for current auth, immutable bytes, integrity, limits and reconciliation |
| G6 — phone workflow | NOT RUN | UX/prototype planning only if clearly simulated | Supported-device acceptance; no misleading real-execution/download claims |
| G7 — canonical acceptance | NOT RUN | Test traceability only | LOOP-01..14 and CASE-01..16 results with pinned revisions and evidence-level labels |

## Work packages

### WP-00 — Independent design review
**State:** READY FOR REVIEW; no reviewer response recorded in this checkpoint.

- **Inputs:** `BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md`, provider-neutral sketch, coordinator fake-adapter plan, owner register, D-06/D-07/D-08 checklists, cross-decision audit.
- **Actions:** Claude performs implementation-readiness review; Gemini performs independent adversarial audit. Use the copy-ready briefs in the checklist.
- **Output:** one finding per item with source path/section, concrete counterexample or missing proof, severity/gate affected, and whether it changes owner semantics.
- **Exit:** findings reconciled against pinned sources; disagreements and unproven claims remain explicit. No code changes required.
- **Stop:** do not treat a reviewer assertion as proof without checking it against source and evidence boundaries.

### WP-01 — Owner decision packet (D-01..D-04)
**State:** BLOCKING semantic/schema freeze; owner confirmation not recorded.

Prepare a compact decision table, not a unilateral decision:
- D-01: verdict for trusted limit-caused termination vs collection-only cap vs display truncation.
- D-02: projection when provider fails without child exit evidence; preserve UNKNOWN exit.
- D-03: required output streams/artifacts per canonical case and acceptable partial collection.
- D-04: event identity scope, exact replay vs conflict, sequence collision behavior, immutable payload snapshot.

For each, show canonical wording, proposed default, counterexample, affected LOOP/CASE cases, and tests that distinguish alternatives.

**Exit:** explicit owner-approved choice for each item, or a clearly marked unresolved choice with dependent tasks blocked. Never change canonical acceptance to fit a proposed implementation.

### WP-02 — Pure contract and reducer test inventory
**Dependency:** WP-01 must settle any semantics that affect expected verdict/event identity.  
**State:** test inventory can be prepared; execution/implementation not authorized by this backlog.

- Strict boolean/integer/string validation; reject truthiness coercion and invalid caps.
- Canonical request/fingerprint determinism and schema-version binding.
- Scoped source-event replay, changed-content conflict, sequence-collision diagnostics.
- Deep immutable accepted-payload snapshot.
- Outcome/disposition/verdict/cleanup/collection/release projection separation.
- Runtime limit vs collection cap vs display truncation.
- Safe expiry-boundary and filename/path normalization helpers where still in scope.

**Exit evidence:** exact source revision, test command, test output, fixture IDs, and explicit UNIT TESTED label. Unit tests do not prove trust, durability, provider semantics, or HTTP behavior.

### WP-03 — Policy-at-dispatch barrier (D-05 / PBR-01..07 / PF-01..05)
**Dependency:** selected execution boundary and explicit cost/account approval.  
**State:** BLOCKED.

- Define where policy revision is bound atomically or conditionally to start.
- Define trusted evidence proving the applied policy for the specific attempt.
- Include a stale-revision race test and assert zero dispatch when the barrier fails.
- Separate request fingerprint evidence from applied-policy evidence.

**Exit:** actual boundary integration demonstrates the barrier under race/failure conditions. A fake ETag or a second policy read is not sufficient. Until then D-05 stays BLOCKED.

### WP-04 — Durable reservation and dispatch reconciliation (D-06 / DR-01..12)
**Dependency:** WP-01 identity semantics, selected store, selected provider semantics, WP-03 policy barrier.  
**State:** BLOCKED.

- Reserve tenant-scoped idempotency key atomically with versioned semantic fingerprint.
- Persist dispatch intent before external start.
- Handle acknowledgement loss, process crash, lease expiry, duplicate concurrent request and provider lookup outage.
- Reconcile using the same reservation/job/attempt identity.
- Prohibit automatic redispatch when outcome is UNKNOWN.
- Specify provider token scope, retention, concurrent same-token behavior and authoritative “not created” evidence.

**Exit:** persistence tests prove uniqueness/restart behavior; provider integration proves actual lookup/idempotency semantics. Exactly-once execution is not claimed unless the selected provider contract supports it.

### WP-05 — Trusted evidence and durable report history (D-04/D-08 / COORD-04/05/11/12 / RH-01..14)
**Dependency:** WP-01 D-04, authenticated producer boundary, selected store.  
**State:** BLOCKED for durability claims.

- Authenticate and bind tenant/job/attempt/source/policy before reduction.
- Deduplicate exact replay; preserve conflicting reuse as contradiction evidence.
- Commit immutable accepted events and evidence references.
- Allocate per-job report versions atomically and monotonically.
- Make append-operation identity distinct from event identity and report-version identity.
- Reconcile commit acknowledgement loss with the same append ID.
- Ensure late evidence creates a new version; never mutate issued history.

**Exit:** actual persistence integration covers concurrency, restart, lost acknowledgement and immutable-version retrieval. In-memory history is not durable evidence.

### WP-06 — Artifact publication and release (D-03/D-07 / AR-01..14)
**Dependency:** required-artifact decisions, report/evidence contract, selected artifact store and release API.  
**State:** BLOCKED for real release claims.

- Bind manifest to tenant/job/attempt, accepted evidence, immutable object version, digest and exact size.
- Define cross-store publication/reconciliation states and when availability can be exposed.
- Re-check current authorization, quarantine/lifecycle, scope and limits at release.
- Define authorization snapshot/lease/revocation behavior during transfer.
- Distinguish bytes sent, transfer completion and integrity verification.
- Test path/TOCTOU, object replacement, integrity mismatch, ranges/retries and partial transfer.

**Exit:** actual store/API/HTTP integration demonstrates safe bytes and honest transfer status. Execution PASS is not download authorization.

### WP-07 — Device workflow and canonical acceptance (G6/G7)
**Dependency:** integrated execution/report/release path; no hidden server guarantee inferred from UI.  
**State:** NOT RUN.

- Test reconnect/reconciliation, UNKNOWN/conflict/denied/quarantined/partial states, report copy, result history and download states on supported phones.
- Keep simulation clearly labeled and do not imply background clipboard monitoring or unsupported cross-app automation.
- Run LOOP-01..14 and CASE-01..16 with exact source/build/runtime versions and boundary-specific evidence.

**Exit:** all mandatory cases have evidence or are honestly NOT RUN/BLOCKED; no criterion weakened to accommodate implementation gaps.

## Critical sequencing and stop rules

1. WP-00 review can proceed now and in parallel; it does not approve a design.
2. WP-01 is required before freezing verdict or event-identity tests. Pure tests for already-settled validation helpers can be prepared separately but must not encode unresolved policy.
3. WP-03 is a hard prerequisite for real dispatch claims and WP-04.
4. WP-04 and WP-05 require actual persistence/provider evidence, not fake-only tests.
5. WP-06 requires current release-boundary and immutable-byte evidence; it cannot inherit trust from execution PASS.
6. WP-07 is last for end-to-end acceptance, though UX prototyping can be separately labeled as simulation.
7. If a provider/store/account/cost boundary is unavailable or not explicitly approved, record BLOCKED/NOT RUN. Do not create an account, launch a workload, enable billing, merge, deploy, or run Actions as a workaround.

## Compact reviewer reconciliation ledger

Use one row per finding; do not close a finding by paraphrasing it away.

| ID | Finding / counterexample | Source section | Canonical criterion(s) | Owner decision affected? | Required evidence boundary | Disposition |
|---|---|---|---|---|---|---|
| REV-001 | Awaiting independent review | Checklist §6 | Preserve all LOOP/CASE meanings | Unknown | Source reconciliation | OPEN |
| REV-002 | Awaiting independent review | Checklist §6 | LOOP-03/05/09/12; CASE-11/13/15/16 | Unknown | Depends on finding | OPEN |

Replace/add rows only when concrete reviewer output exists. Do not invent findings in advance.

## State and provenance

- This backlog is a planning artifact, not an implementation contract.
- D-01..D-04 remain owner-open; D-05 remains BLOCKED pending actual boundary proof; D-06..D-08 remain proposals.
- No provider, store or runtime selected.
- No tests or workloads run in this pass.
- Canonical acceptance on `main`, PR #2 and PR #3 remain untouched.
- No account, billing, merge, deployment or GitHub Actions operation performed.

## References

- [Boundary proof-level review checklist](BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md)
- [Provider-neutral boundary contract sketch](PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md)
- [Coordinator/fake-adapter test plan](COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md)
- [Owner decision register](OWNER_DECISION_REGISTER_20261029.md)
- [Cross-decision contradiction audit and gates](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md)
- [Canonical acceptance traceability](CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md)


## Owner decision packet pointer

The review-ready decision table and response template for D-01..D-04 are in [OWNER_DECISION_PACKET_D01_D04_20261029.md](OWNER_DECISION_PACKET_D01_D04_20261029.md). This packet frames choices and dependencies only; no checkbox is approved by its creation. Use it before freezing verdict, output-gate or event-identity schemas.


## Pure test inventory pointer

The detailed candidate suite and evidence ladder are in [PURE_CONTRACT_TEST_INVENTORY_20261029.md](PURE_CONTRACT_TEST_INVENTORY_20261029.md). It separates test properties that can be specified without D-01..D-04 from verdict/replay expectations blocked on owner decisions, and explicitly separates pure, fake-coordinator, persistence, provider, artifact/API/HTTP and device proof. It is test design only; NOT RUN.


## Pinned-test coverage reconciliation

The gap-only static comparison is [PURE_TEST_COVERAGE_GAP_AUDIT_20261029.md](PURE_TEST_COVERAGE_GAP_AUDIT_20261029.md). It re-fetched the exact PR #2/#3 helper and test blobs and distinguishes existing test-source coverage from missing fixtures. Top concrete candidates are malformed limit flags, strict output-budget cap types, whitespace-only fingerprint identity fields, nested event payload mutation, reserved Windows superscript filename aliases, tombstone re-add retention behavior and redaction boundary cases. Tests remain NOT RUN; source changes, if authorized, belong on their own PR branches—not this research branch.


## G-01..G-03 patch-ready specification

See [G01_G03_PATCH_READY_TEST_SPEC_20261029.md](G01_G03_PATCH_READY_TEST_SPEC_20261029.md) for the exact proposed test matrices and behavior choices for malformed limit flags, OutputBudget cap types, and whitespace-only fingerprint identity fields. It identifies which behavior requires a decision before assertions are written. Design only; no PR branch or source/test file was changed.


### G-01..G-03 behavior recommendation

See [G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md](G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md). Recommendation is validation-focused and intentionally preserves valid disposition semantics and existing fingerprint normalization. It is not an owner decision or patch authorization; tests remain NOT RUN.


### G-07/G-08 patch-ready follow-up

See [G07_G08_PATCH_READY_TEST_SPEC_20261029.md](G07_G08_PATCH_READY_TEST_SPEC_20261029.md) for bounded regression matrices and proposed tombstone semantics. This remains a design artifact, not implementation; owner approval is needed before changing PR #3.


### Consolidated owner decision and patch gate

Use [CONSOLIDATED_OWNER_DECISION_AND_PATCH_GATE_20261029.md](CONSOLIDATED_OWNER_DECISION_AND_PATCH_GATE_20261029.md) as the current compact owner-facing entry point for D-01..D-04 and G-01/G-02/G-03/G-07/G-08. It preserves the distinction between approving semantics and authorizing source edits, recommends splitting patches by concern, and lists required proof gates. It does not close decisions or authorize code changes.


Implementation-level clarifications are in [G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md](G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md), including G-01 validation precedence and G-08 expired-key reuse. Resolve the G-08 retention/reuse rule before implementing tombstone changes.
