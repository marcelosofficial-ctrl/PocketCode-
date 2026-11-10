# NEXT TASK: PocketCode

## Goal
Finish owner-gated P39 reconciliation and prepare a bounded, non-duplicative P40 model-only run. Implementation remains blocked.

## Current evidence
- Claude/Gemini P39 reconciliations and consensus matrix are committed. Await any additional Claude artifact supplied by the owner; do not create a competing Claude request while the strategy assignment remains OPEN.
- OD-01..OD-13 all OPEN. CASE-04 remains INCOMPLETE / timed_out.
- Pages enabled; workflow deploys `prototypes/mobile-runner`; actual URL/deployment/headers/sibling-origin evidence UNKNOWN.
- Pyodide worker-channel spoofing is conditional; installed Pyodios topology UNKNOWN.
- `FULL_POWER_GAP_RESEARCH_20261110.md` records outbox, fencing, PWA recovery and execution-evidence research.
- `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md` is prepared. It defines four slices and preserves existing P39/EP/PYO and LOOP/CASE IDs. It is NOT AUTHORIZED / NOT RUN.

## Ranked next actions
1. **Claude artifact arrives:** pin exact repo, branch, source/test/docs SHA and blob hashes; inspect its actual scope; reconcile only evidence-backed findings into the existing consensus matrix. Do not assume it covers exit provenance.
2. **Owner gate:** obtain explicit OD-01..OD-13 decisions or explicit deferrals. Resolve OD-01 first, OD-02..05 as one revocation lifecycle, OD-06..07 clock/identity, OD-08 receipt binding, OD-09..12 verdict/termination/cleanup, OD-13 client-byte evidence. Silence is not approval.
3. **After gate clearance only:** request explicit authorization for the bounded four-slice model-only sequence in `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md`. Pin source/test SHA and environment; run exact existing test families; keep supporting tests distinct from canonical CASE outcomes.
4. **Evidence-dependent only:** complete PAGES-01..08 / ORIGIN-01..10 if owner supplies actual URL/settings or a reachable deployment identifier. Do not guess URL or headers.
5. **Separately:** run full Python suite on an exact SHA in a real checkout/CI; historical 266/266 is not current evidence.

## Hard constraints
- P39/P40 CLOSED; OD-01..OD-13 OPEN until owner responds.
- No source/test edits, schema freeze, runtime/provider/database/transport selection, spend, deployment, device test or PR #2/#3/#4 modification before explicit gate clearance.
- Preserve VERIFIED / INFERRED / UNKNOWN / NOT RUN and PASS / FAIL / NOT RUN.
- Python CI path filter covers `scripts/**` and its workflow only, plus manual dispatch; docs-only commits do not trigger it. Static prototype checker does not execute JS or Python.
- Keep RevDev evidence separate.

## Done when
Supplied reviews are reconciled; owner decisions are explicit or explicitly deferred; model/adapter/product acceptance boundaries are clear; and the owner authorizes a bounded slice or remaining blockers are documented.
