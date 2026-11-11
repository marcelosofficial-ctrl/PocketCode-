# NEXT TASK: PocketCode

## Goal
Close owner-gated P39 decisions and prepare a correctly scoped P40 model-only run. Implementation remains blocked.

## Current evidence
- Claude/Gemini P39 reviews reconciled. Await additional Claude artifact from owner; do not create a competing request while Claude's strategy assignment remains OPEN.
- OD-01..OD-13 all OPEN. CASE-04 remains INCOMPLETE / timed_out.
- P40 protocol revised to six source-pinned lanes. Known model gaps: equal-progress aggregate/event parity; first-delivery event trust; separate grant-event relay fencing; policy revalidation; Worker/receipt/storage boundaries. NOT AUTHORIZED / NOT RUN.
- **Scope clarification added to the owner register:** OD-01 is about live/incremental streaming. A NO decision does not exclude bounded download/share of a fully staged artifact. If bounded release remains in MVP, OD-02..05 still need explicit pre-claim, in-flight revocation, interruption/recovery and policy/grant consistency semantics. If all artifact release is excluded, state that separately. OD-13 applies to claims of client receipt.
- Last verified Pages workflow deploy: run 39433670146, main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`, URL `https://marcelosofficial-ctrl.github.io/PocketCode-/`. Automatic deploy is main/path filtered.
- Public `portfolio` repo also has Pages enabled at `https://marcelosofficial-ctrl.github.io/portfolio/`, same browser origin as PocketCode. No exploit confirmed; no sensitive browser storage.
- Live Pages response/headers and generated portfolio script behavior UNKNOWN. Pyodios worker topology UNKNOWN.

## Ranked next actions
1. **Claude artifact arrives:** pin exact repo, branch, source/test/docs SHA and blob hashes; reconcile evidence-backed findings into the existing matrix. Do not assume it covers exit provenance.
2. **Owner gate:** obtain OD-01..OD-13 decisions or explicit deferrals. Resolve OD-01 first, explicitly distinguishing live streaming from bounded artifact download/share; then resolve OD-02..05 as one revocation lifecycle, OD-06..07 clock/identity, OD-08 receipt binding, OD-09..12 verdict/termination/cleanup, and OD-13 client-byte evidence.
3. **After gate clearance only:** obtain explicit authorization for the six-lane model run in `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md`. Pin source/test SHA and environment. Keep model results separate from canonical CASE acceptance.
4. **Origin follow-up:** verify current Pages deployment, response headers and service-worker scope; inspect the `portfolio` generated output for origin-scoped storage access. Do not change hosting/domain or store secrets.
5. **Separately:** run the full Python suite on an exact SHA in real checkout/CI. Historical 266/266 is not current evidence.

## Hard constraints
- P39/P40 CLOSED; OD-01..OD-13 OPEN until owner responds.
- No source/test edits, schema freeze, runtime/provider/database/transport selection, spend, deployment, device test or PR #2/#3/#4 modification before explicit gate clearance.
- Preserve VERIFIED / INFERRED / UNKNOWN / NOT RUN and PASS / FAIL / NOT RUN.
- Python CI path filter covers `scripts/**` and its workflow only, plus manual dispatch; docs-only commits do not trigger it. Static prototype checker does not execute JS or Python.
- Keep RevDev evidence separate.

## Done when
Reviews are reconciled; owner decisions are explicit or explicitly deferred; model/adapter/product acceptance boundaries are clear; and owner authorizes a bounded slice or remaining blockers are documented.
