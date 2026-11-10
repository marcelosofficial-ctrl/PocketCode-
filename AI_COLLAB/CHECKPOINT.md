# CHECKPOINT — 2026-11-10

**Unit:** Gated P40 model-only execution protocol prepared.  
**Starting HEAD:** `4adf2c14ea39c6f62d67da0d8784b13d35c83053`.  
**Protocol commit:** `c23c2b671a79b978be5a602c91d270543ccedd0c`.  
**Checkpoint metadata base:** `188f98b4dd80bfcaf139f83b878949e4f9a014be`; this refresh creates a docs-only descendant. Use the live branch ref for the resulting tip SHA.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`.

## Mandatory resume and branch evidence
- Read in order: BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md, INBOX_chatgpt.md.
- Branch API confirms HEAD `4adf2c14ea39c6f62d67da0d8784b13d35c83053`. The commit-search endpoint returned stale results; branch-specific commit list is authoritative for this check.
- Latest five before work:
  1. `4adf2c14` docs(checkpoint): record exact-SHA CI boundary
  2. `493a5d20` docs(checkpoint): record full-power gap research pass
  3. `f2cd5f0b` docs(next): prioritize full-power gap findings
  4. `f9ea145f` docs(state): record full-power research
  5. `e50fcfe3` index Apple spec and research
- The previous STATE/CHECKPOINT had stale HEAD/checkpoint references; corrected in this unit.

## Work completed
- Created `AI_COLLAB/P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md` (1,708 words). It provides four ordered slices:
  1. Aggregate/event parity, no-op/terminal semantics and canonical envelope integrity.
  2. Relay ordering, duplicate delivery, stale-worker fencing, trusted time, poison predecessor and ID continuity.
  3. Owner-gated revocation phases and immutable receipt/grant binding.
  4. Typed exit, worker control-channel, output finalization, artifact readback and receipt projection.
- Mapped to existing P39-EVENT, OUTBOX, CLOCK, ID, POLICY, RECEIPT, RCP, EP and PYO-CTRL families and existing LOOP/CASE traces. No new canonical or P39 IDs.
- Explicitly separates sequential-model evidence from adapter, browser/device, transport and canonical product CASE evidence. Added non-vacuity requirements and stop conditions.
- Updated INDEX, STATE and NEXT_TASK to index the protocol and establish the next ranked work. CHECKPOINT overwritten with this unit's evidence.

## Gate and red lines
- P39/P40 remain CLOSED. OD-01..OD-13 remain OPEN. Protocol is PREPARED only, NOT AUTHORIZED / NOT RUN.
- No source/test edits, schema freeze, runtime/provider/database/transport choice, dependency, spend, deployment, device test, PR change or RevDev work.
- Claude's additional material remains awaited; this work deliberately does not duplicate Claude's Apple design, website, context-engineering or provider-cache lane.

## Verification
- **VERIFIED:** GitHub read/write permissions available; branch update succeeded for protocol commit.
- **VERIFIED:** exact HEAD before work was `4adf2c14...`; protocol commit is `c23c2b671a79b978be5a602c91d270543ccedd0c`.
- **NOT RUN:** source tests, P40 model scenarios, browser/device/transport/adapter tests.
- **VERIFIED:** exact-SHA query for metadata base `188f98b4dd80bfcaf139f83b878949e4f9a014be` returned zero Actions runs, zero check runs and zero statuses. CI NOT RUN. This checkpoint-only descendant also requires its own live exact-SHA query. Historical 266/266 PASS remains tied only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.

## Final branch evidence
Latest five commits:
1. `188f98b4` docs(checkpoint): index gated P40 execution protocol
2. `c23c2b67` docs(p40): prepare gated model-only execution protocol
3. `4adf2c14` docs(checkpoint): record exact-SHA CI boundary
4. `493a5d20` docs(checkpoint): record full-power gap research pass
5. `f2cd5f0b` docs(next): prioritize full-power gap findings

## Next
1. Ingest Claude artifact by exact pins if/when supplied.
2. Obtain OD-01..OD-13 decisions/deferrals.
3. Only after gate clearance, request bounded P40 model-only execution authorization.
