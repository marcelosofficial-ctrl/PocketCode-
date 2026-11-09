# P39 gate closure and implementation readiness plan

**Date:** 2026-11-09  
**Status:** WORK PLAN / NO IMPLEMENTATION AUTHORIZED  
**Scope:** PocketCode P39 release-grant, event/relay and exit-provenance work only. RevDev evidence and decisions are excluded.

## 1. Current gate

- **Gemini independent review:** received and reconciled in `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`.
- **Claude P39 review:** received and reconciled in `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`. C1-C7 are Claude-reported runs against a byte-identical copy, not the repository suite.
- **Additional Claude review:** await the owner's supplied artifact when ready. Current `INBOX_claude.md` has an OPEN strategy-program assignment; do not create a competing request or assume an EP review has been performed.
- **Owner decisions:** OD-01..OD-13 remain OPEN. No recommendations are adopted by silence.
- **Implementation:** P39/P40 gate CLOSED. No source/tests, adapters, schemas, canonical IDs, runtime, provider, database or transport may change under this plan.
- **Tests:** Gemini NOT RUN; ChatGPT NOT RUN; repository suite NOT RUN in these review passes. Historical 266/266 applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.

## 2. Reconciled technical worklist

| Priority | Finding family | Required model/contract proof | Layer |
|---|---|---|---|
| P0 | RG-B1 / corrected Gemini S1 | Every aggregate version maps to exactly one immutable event/outbox; no-op progress does not advance; terminal transitions are explicit; replay reconstructs the same aggregate | Sequential model first, durable adapter later |
| P0 | RG-B2 / corrected Gemini S2 | Trusted consumer recomputes digest over canonical semantic event envelope; metadata mutation and forged first delivery are rejected | Sequential model |
| P0 | P39-S5 | Event must bind to an existing tenant-scoped grant and authorized producer/source; digest validity is not authorization | Model + adapter identity boundary |
| P0 | RG-H1 / corrected Gemini S3 | Grant-event relay has claim, lease, monotonic fence, per-grant order and conditional delivered mark; stale worker cannot mark after takeover | Model then multi-process adapter |
| P0 | RG-B3 | Authoritative store/coordinator time controls lease expiry; caller-supplied future/backdated time cannot steal or extend a lease | Model oracle + adapter |
| P1 | RG-H4 | Grant/event IDs and fence high-water do not repeat across instances, restart, deletion, restore or migration | Model semantics + durable adapter |
| P1 | RG-O6 | Poison/missing predecessor causes bounded visible HOLD/quarantine; no silent version skip; audited resolution retains evidence | Model + operations/adapter |
| P1 | RG-H3 | Pre-commit policy epoch race is defined; strict cross-authority atomicity is not claimed without a proven protocol | Owner policy + adapter |
| P1 | RG-O1..O4 | Receipt-head history, immutable intent replay, compact receipt binding and non-vacuous assertions are resolved against the canonical receipt contract | Model/tests |
| P1 | EP-01..25 | Typed child/wrapper/host termination observations, provenance, contradiction handling, cleanup and artifact disposition remain separate | Projection contract + adapter |
| Conditional | RG-H2 / P39-S4 | If streaming is MVP, define chunk capability, active cancellation, acknowledgement and client-byte evidence; otherwise explicitly defer streaming claims | Owner decision + transport adapter |
| Conditional | RCP-04 / OD-13 | Distinguish staged, transport-accepted, emitted, client-observed and client-acknowledged bytes | Owner decision + adapter |

The Gemini headline corrections are important: its S1 location was wrong (`event_journal.py` is not the aggregate/outbox model); its S2 named `verify_receipt()` does not exist in the checked receipt module, while the grant consumer does trust a caller-provided digest; its S3 claim about `fake_outbox.py` is contradicted by its lease/fence code, while the separate grant-event relay is unfenced; S4 is a transport/MVP boundary, not a defect in the sequential model. Full source pins and secondary-claim dispositions are in the Gemini reconciliation.

## 3. Review and owner-decision sequence

1. **Ingest any additional Claude artifact supplied by the owner.** Pin repository, branch, exact source/test/docs SHA, blob hashes and line ranges. Record what Claude did and did not read/run. Reconcile each claim against Gemini, existing Claude P39 findings, source and canonical crosswalk. Do not infer that the additional artifact is an exit-provenance review until its scope is inspected.
2. **Build one conflict/consensus matrix.** Each row must have finding ID, exact source pin, independent reviewer position, ChatGPT disposition, severity, model/adapter/owner classification, canonical LOOP/CASE support, proposed P39 test ID and evidence status. Merge overlaps; do not duplicate runs or rename IDs.
3. **Obtain OD-01..OD-13 explicitly.** Resolve OD-01 first; OD-02..05 as one revocation lifecycle; OD-06..07 clock/identity; OD-08 receipt binding; OD-09..12 exit verdict/termination/cleanup; OD-13 client receipt evidence. Unanswered rows stay OPEN.
4. **Freeze a versioned model contract only after decisions.** Specify event/version semantics, canonical digest fields and encoding, grant/source binding, relay ordering/fencing, trusted time, ID continuity, poison handling and receipt replay rules. Preserve LOOP-01..14, CASE-01..16 and D-IDs.
5. **Authorize a bounded model-only P40 slice only after gate clearance.** Proposed order: event/version parity and no-op semantics; canonical consumer envelope and grant binding; trusted clock and relay fencing/order; poison-gap behavior and ID semantics. Keep pre-commit policy, receipt-head and exit-projection work in separate slices if dependencies allow.
6. **Prove the model, then the adapter.** Run targeted P39 tests and the complete Python suite on exact source/test SHAs. Separately test two-process races, crash before/after commit, relay redelivery, restore/fence continuity, real policy revocation and any selected transport. A sequential model test never proves durable adapter behavior.
7. **Reconcile product evidence.** Run canonical CASE scenarios only in a real controlled product boundary. Supporting P39 tests do not make canonical CASEs PASS. Keep CASE-04 INCOMPLETE / timed_out until trusted termination provenance proves otherwise.

## 4. Exit-provenance acceptance guardrails

- The pure renderer displays a trusted coordinator projection; it does not authenticate or infer process facts.
- Child natural exit, wrapper exit, embedded-runtime outcome, worker termination request, termination acknowledgement, cleanup and artifact release remain distinct.
- Contradictory, stale, malformed or unbound observations remain INCOMPLETE pending reconciliation.
- OD-09 and OD-10 decide EP-18 and EP-24 mappings. Do not hard-code their recommendations.
- A browser worker abort is not a native child exit or cleanup acknowledgement.
- Keep CASE-04 exactly INCOMPLETE / timed_out. Do not patch precedence-only behavior into the legacy two-field formatter.

## 5. Non-goals and stop conditions

- No provider/database/runtime/host/transport selection, paid service, cloud deployment, device test or PWA storage implementation.
- No source/test edit, dependency change, schema migration, canonical ID change or PR #2/#3/#4 modification.
- No use of RevDev test results or acceptance evidence.
- Stop before implementation if owner decisions conflict, canonical semantics are ambiguous, source pins differ, the branch moves unexpectedly, or a proposed fix crosses the no-spend/security boundary.
- Keep all unverified behavior UNKNOWN / NOT RUN. Reviewer agreement is not owner authorization.

## 6. Completion criteria

The gate can be reconsidered only when: all supplied independent reviews are reconciled; the consensus/conflict matrix is complete; OD-01..OD-13 have explicit owner dispositions or explicit deferrals; model and adapter obligations are separated; canonical traceability is preserved; the owner authorizes a bounded implementation slice; and the test/evidence plan is pinned to exact sources and environments.
