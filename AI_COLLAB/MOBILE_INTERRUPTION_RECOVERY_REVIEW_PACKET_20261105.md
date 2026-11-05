# Three-AI review packet: mobile interruption recovery — 2026-11-05

**Status:** READY TO SEND / REVIEWS NOT RECEIVED. Research/design review only. No implementation authorization is implied.

## Authority and project constraints

PocketCode remains the phone-first execution/evidence product. RevDev remains a separate Windows product. Shared concepts do not authorize shared runtime/code or acceptance-suite merging.

- Canonical PocketCode acceptance: LOOP-01..14, CASE-01..16. Do not change IDs or expected wording.
- Owner decisions D-01..D-08 remain as recorded. Do not close decisions on the owner's behalf.
- $0 budget. No provider, execution host, app stack or runner selected.
- Current architecture document states there is no client framework/runtime selected; first useful proof remains the narrow phone-browser fixed-task workflow.
- No product code/test edits or provider/device workloads authorized by this review packet.
- Research-only source findings are not integration proof.

## Exact inputs

1. `RESEARCH/MOBILE_INTERRUPTION_RECOVERY_AND_OPEN_SOURCE_SYNC_AUDIT_20261105.md` (latest blob after acceptance crosswalk: `4e8cfafb4563f7e8948e73ec10b4d519e51e27ff`).
2. `RESEARCH/CLINE_WORKSPACE_CHECKPOINT_AND_RESTORE_AUDIT_20261105.md` (backend-neutral checkpoint contract; blob `5260729e4af0bd8ef9fe0f09dc9fc0a5825e49aa`).
3. `AI_COLLAB/PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md` (blob `7a1de12f1faafea8d630c851f28ac3bf9a554aeb`).
4. `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` (blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`).
5. `PRODUCT/EXECUTION_CONTRACT.md` and `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md` as supporting, proposal-only contracts.

## Claude assignment: architecture and recovery review

Act as lead developer/architecture reviewer. Review for missing lifecycle boundaries, over-specification, unsafe assumptions and the smallest feasible implementation path.

1. Separate app lifecycle, connectivity lifecycle, transport delivery and authoritative execution lifecycle. Is the proposed split complete? What states or transitions are redundant or missing?
2. Challenge persist-before-dispatch. Enumerate every crash point from local request+outbox commit through remote acceptance, lost acknowledgement, terminal observation and local report persistence. For each, state the exact safe action. Distinguish a replay of the same idempotent request from a second execution.
3. Review cursor/snapshot atomicity. Is event ID + monotonic sequence/cursor enough? How should the client handle duplicates, gaps, retention expiry, out-of-order events, server compaction, clock skew and contradictory terminal observations?
4. Review offline optimistic overlay versus canonical run history. What can be coalesced safely? Which mutations/commands must never be coalesced? Can any acknowledgement clear a newer intent?
5. Review local-only work on iOS, Android and browser/WASM. Which workload classes can continue, resume from checkpoint, or only report interrupted/unknown? Avoid claiming more than OS APIs support.
6. Review transfer state separately from execution state. How should file-backed iOS background upload, Android WorkManager/UIDT transfer, digest/read-back and interrupted transfer retry be bound to one run?
7. Review cancellation. Define request, acknowledgement, confirmed termination and unknown outcome, without treating app suspension as cancellation.
8. Reconcile the proposed G0-G6 sequence with the actual first MVP and $0 constraints. Identify unnecessary scope and the smallest valuable proof.
9. Verify each reuse statement against pinned Happy/OpenHands source. Identify code that can be copied verbatim only if a native Swift/Kotlin or Expo stack is chosen; do not recommend a large framework import without cost/maintenance justification.
10. Map each useful correction to existing LOOP/CASE requirements. Do not add acceptance IDs or make owner decisions.

Return a numbered finding set with severity, source/line anchor, counterexample, exact correction, applicable existing acceptance requirement and proof layer. Each section: ACCEPT / ACCEPT WITH CHANGES / REJECT / NOT PROVABLE.

## Gemini assignment: adversarial security and lifecycle audit

Act as independent security/spec auditor. Assume malicious clients, buggy hosts, storage faults, stale workers, network ambiguity and OS termination.

1. Attack run/attempt/request identity reuse with changed code, inputs, target, policy, host, tenant or schema version.
2. Attack idempotency: duplicate POST, lost response after accepted execution, expired server dedupe record, retry with changed payload, host restart, and simultaneous devices.
3. Attack outbox coalescing. Find cases where a later intent could erase an earlier non-idempotent effect or a stale acknowledgement could erase a newer user action.
4. Attack cursor persistence: commit projection before cursor, cursor before projection, crash mid-transaction, event ID collision, sequence reuse, replay after retention expiry, signed/unsigned event confusion, duplicate terminal event and stale attempt.
5. Attack identity across phone account switch, pairing/re-pairing, remote host replacement, server version change, revoked credentials, local database restore and multi-device takeover.
6. Attack cancellation and timeout. Show sequences where UI could claim cancelled/timed_out without process termination, and define the minimum evidence needed.
7. Attack local storage failures: corrupt DB, disk full, permission denied, transaction failure, cleanup failure, failed acknowledgement write. Make sure these cannot become empty queue, completed, PASS or silent data loss.
8. Attack iOS/Android background assumptions, including user force quit, reboot, OS suspension, device-vendor policy, background task expiration and network unavailability. Identify any unsupported claim.
9. Review secrets and user data in durable request digests, logs, reports, telemetry and AI handoff packets. Do not let a fingerprint become a secret oracle.
10. Distinguish fake tests from OS/device/runner/remote-provider evidence. Recommend minimal crash-injection scenarios without creating new canonical IDs.

Return an attack tree plus numbered findings: severity, exact failing sequence, violated invariant, minimal fail-closed correction, existing LOOP/CASE mapping, proof layer and confidence (SOURCE-CONFIRMED / DESIGN GAP / CONDITIONAL HYPOTHESIS / UNPROVEN).

## ChatGPT reconciliation rules

After the user forwards both reviews:
- compare exact claims and source evidence; do not resolve by majority vote;
- retain disagreements and classify evidence;
- preserve canonical LOOP/CASE and owner decisions;
- do not call this a runtime/device validation;
- update the design only after the exact corrections are mapped and justified.

## Non-actions

No source code or test file changed. No Happy/OpenHands source copied or installed. No runtime, provider, job, host or account selected. No device or provider test run. No acceptance ID or expected string changed.