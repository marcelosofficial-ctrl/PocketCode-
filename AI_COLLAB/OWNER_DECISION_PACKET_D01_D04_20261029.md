# PocketCode — Owner Decision Packet D-01..D-04

**Date:** 2026-10-29  
**Status:** Decision aid only. No choice in this document is approved unless the owner explicitly confirms it.  
**Canonical authority:** main: PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md (blob c6714c27db52b2962fe8d1c7e6a16829d46a8338); main: PRODUCT/EXECUTION_CONTRACT.md (blob 3861e51ae4f9e45a263b677402f26c41b240959d).  
**Research branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Purpose:** Make the four semantic decisions small enough for explicit owner review, showing the consequences of each choice. This packet does not change canonical LOOP/CASE IDs, freeze an API schema, authorize implementation, or select infrastructure.

## Decision summary

| ID | Question | Proposed default for review | Status |
|---|---|---|---|
| D-01 | How should a confirmed runtime-enforced limit affect verdict? | A confirmed limit-caused termination is a candidate FAIL only when trusted evidence establishes a confirmed program/runtime failure under canonical wording. Collection-only and display-only truncation do not themselves imply runtime failure. | OPEN |
| D-02 | What if provider failure leaves child exit evidence unavailable? | INCOMPLETE verdict; execution outcome UNKNOWN; no fabricated exit code. PROVIDER_ERROR disposition only when the infrastructure cause is confirmed. | Proposed default; owner confirmation recommended before schema freeze |
| D-03 | Must every output stream be complete for PASS? | Only case-required streams/artifacts gate PASS or release; partial capture is acceptable only where that case permits it. Optional diagnostics are not universal gates. | OPEN |
| D-04 | What defines an event replay versus conflict? | Coordinator-owned canonical event identity; source IDs retained in a documented namespace; exact replay requires the same scoped identity and immutable observation fields. | OPEN |

## D-01 — Limit-caused termination versus truncation

### Canonical anchor
Canonical PASS requires trusted completion and exit code 0. Canonical FAIL requires a non-zero exit code or confirmed program/runtime failure. INCOMPLETE applies when success or program failure is not confirmed. Canonical CASE-04 expects INCOMPLETE / timed_out when trusted execution control confirms the timeout outcome. These requirements must be interpreted together; this packet does not rewrite them.

### Proposed decision
Keep three different observations distinct:

1. **Runtime-enforced limit ended execution:** If trusted evidence proves the limit actually terminated the program, record the exact limit cause and enforcement source. Choose FAIL only if this is a confirmed program/runtime failure within the canonical FAIL definition; otherwise retain INCOMPLETE. Preserve LIMIT_EXCEEDED as disposition and keep cleanup independent. The explicit CASE-04 timeout expectation remains in force.
2. **Collector/output-retention cap only:** If trusted process evidence independently confirms exit 0, the execution observation remains EXIT_ZERO. Whether PASS is allowed depends on whether the affected stream is mandatory for that acceptance case and whether partial capture is permitted.
3. **Display/report truncation only:** Keep the verdict derived from execution evidence; mark presentation truncation without inventing a runtime limit or execution failure.

### Owner choice needed
- [ ] Approve the distinction above, retaining the specific CASE-04 timeout expectation.
- [ ] Request a different explicit mapping for limit-caused termination (name which confirmed limits are FAIL versus INCOMPLETE and why).
- [ ] Leave unresolved; do not freeze verdict tests/schema.

**Counterexample test:** Exit-zero evidence plus renderer truncation must not become FAIL; a collector cap must not be represented as process termination; a trusted confirmed timeout must still meet CASE-04's explicit expectation.

**Traceability:** LOOP-03..05, LOOP-07, CASE-04, CASE-07, CASE-09, CASE-10, CASE-12.  
**Required proof:** Pure projection tests for mapping; trusted runtime/provider evidence for whether the limit actually ended execution. A fake limit event cannot prove enforcement.

## D-02 — Provider failure without child exit evidence

### Canonical anchor
LOOP-05 and CASE-06 prohibit treating uncertain infrastructure outcomes as success. The execution contract says never fabricate an exit code and requires explicit provider/infrastructure uncertainty.

### Proposed decision
- User verdict: INCOMPLETE.
- Execution observation: UNKNOWN when no trustworthy child terminal result exists.
- Job disposition: PROVIDER_ERROR only when an infrastructure/provider cause is itself confirmed; otherwise INCOMPLETE.
- Exit code: absent/unknown, never synthesized.
- If an independently trusted nonzero child exit is already established, preserve FAIL even if cleanup later becomes unknown/failed; keep cleanup and artifact-release eligibility separate.

### Owner choice needed
- [ ] Approve this projection rule.
- [ ] Require a different disposition split (state which provider facts justify it).
- [ ] Leave unresolved; preserve UNKNOWN and block schema freeze.

**Counterexample tests:** Provider fails before start; partial stdout then exit evidence is lost; nonzero child exit is trusted but cleanup confirmation fails; provider returns an error message that does not establish whether the child ran.

**Traceability:** LOOP-03..05, LOOP-07, CASE-03, CASE-06, CASE-11, CASE-12, CASE-13.  
**Required proof:** Pure projection tests can test mapping; adapter integration must prove which provider facts are trustworthy. A fake error cannot establish the real provider's terminal semantics.

## D-03 — Output completeness required for PASS

### Canonical anchor
LOOP-07 asks for bounded stdout/stderr, truncation markers and output-file metadata. LOOP-10 concerns output files/downloads. CASE-07 requires limits/truncation or rejection to be explicit. Canonical PASS wording requires trusted completion and exit 0 but does not explicitly require every possible diagnostic stream to be complete.

### Proposed decision
Define requirements **per acceptance case and output class**, not as a universal “all streams complete” boolean:
- An explicitly required stream or artifact must satisfy that case's collection/integrity rule; otherwise withhold PASS or release as applicable, while preserving raw terminal facts.
- Optional diagnostic output may be unavailable or capped without automatically converting every run to INCOMPLETE.
- Keep COMPLETE, PARTIAL, UNAVAILABLE, EMPTY, RUNTIME_LIMIT, and DISPLAY_TRUNCATED distinct. Do not confuse empty output with unavailable output.
- Artifact release remains a separate decision: a PASS verdict does not authorize unsafe or incomplete artifact delivery.

### Owner choice needed
- [ ] Approve per-case required-stream rules and no universal optional-diagnostic gate.
- [ ] Require a universal completeness gate (identify exactly which streams and why).
- [ ] Leave unresolved; do not freeze PASS gates/schema.

**Counterexample test:** Exit 0 with complete required stdout and unavailable optional stderr may pass if the case permits it; the same result must not pass if the acceptance case explicitly requires the missing stream. No implementation may quietly redefine the case.

**Traceability:** LOOP-03, LOOP-06..08, LOOP-10..11, CASE-07, CASE-09, CASE-12, CASE-14.  
**Required proof:** Owner-approved case matrix + pure projection tests + collector integration for actual truncation/availability. A renderer's display limit is not collector evidence.

## D-04 — Event identity, replay, ordering, and immutable observations

### Canonical anchor
The canonical plan requires authoritative terminal facts and forbids missing/ambiguous evidence from becoming PASS. It does not fully define a provider-neutral event identity namespace; the implementation must not infer ordering from untrusted timestamps or merge unrelated attempts.

### Proposed decision
- Assign each accepted canonical event a coordinator-owned unique event_id.
- Retain the external/provider event ID separately with a documented source namespace.
- Scope source replay identity to source namespace plus tenant/job/attempt and source event ID (exact tuple to be frozen only after source/auth model is selected).
- Validate authenticated producer and tenant/job/attempt/policy bindings before reducing an event.
- Treat a replay as identical only when scoped source identity and all immutable observation fields match: event kind, sequence, canonical payload/schema version, relevant binding and policy revision. Permit differences only in explicitly enumerated transport-delivery metadata.
- Treat changed identity, attempt, event kind, sequence or payload as conflict/contradictory evidence, not an idempotent retry.
- Coordinator sequence is unique/monotonic in its defined stream; provider timestamps alone do not establish order. Distinct event IDs with the same coordinator sequence remain visible in diagnostics.
- Snapshot accepted payloads immutably; later mutation of a caller-owned nested object must not change accepted evidence.

### Owner choice needed
- [ ] Approve this as the semantic default, with exact tuple/schema deferred until the source/auth boundary is selected.
- [ ] Request a different replay identity rule (provide intended namespace and conflict behavior).
- [ ] Leave unresolved; do not freeze event schema/reducer tests.

**Counterexample tests:** Exact replay; same source ID with changed payload; cross-tenant/job/attempt replay; same sequence with distinct event IDs; late contradictory terminal event; nested-payload mutation after acceptance.

**Traceability:** LOOP-03..07, CASE-06, CASE-11..13, CASE-16.  
**Required proof:** Pure tests prove deterministic reducer behavior; coordinator/fake tests prove call paths; authenticated producer and durable persistence integration prove actual trust, scope binding, replay persistence and late-event history.

## Dependencies and stop rules

- D-01 and D-03 affect verdict and collection gates; do not freeze expected verdicts while unresolved.
- D-02 affects UNKNOWN/provider-error projection; do not fabricate exit codes to simplify the schema.
- D-04 affects event schema, replay, reducer, report history and idempotency; do not claim provider event IDs are globally unique without a provider contract.
- D-05 remains independently BLOCKED until actual policy-at-dispatch enforcement is proven. Resolving D-01..D-04 does not close D-05.
- D-06..D-08 remain proposals requiring selected persistence/provider/artifact boundaries.
- No owner response is implied by the existence of this packet. Until explicitly confirmed, the checkboxes remain unchecked and decisions remain open/proposed.

## Response template for owner review

Copy and fill only the lines you wish to decide:

    D-01: APPROVE / CHANGE / OPEN — [specific mapping or question]
    D-02: APPROVE / CHANGE / OPEN — [specific projection]
    D-03: APPROVE / CHANGE / OPEN — [required streams and partial-capture rule]
    D-04: APPROVE / CHANGE / OPEN — [replay identity and conflict rule]
    Constraints or examples: [optional]

## Provenance

- Derived from the owner decision register, semantic crosswalk, transition/report projection matrix, and canonical acceptance/contract listed above.
- Static documentation review only. No tests, workloads, implementation, provider/store selection, account, billing, merge, or deployment performed.
- Canonical acceptance on main, PR #2 and PR #3 remain untouched.
