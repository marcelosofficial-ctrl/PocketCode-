# PocketCode programme progress and next execution gates

**Checkpoint:** 2026-11-05  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Status:** Research and architecture baseline; no functional end-to-end product proof.

## Executive assessment

**PocketCode progress: approximately 20% toward a dependable first MVP.** This is a qualitative programme estimate, not a code-completion metric or test result. Requirements, acceptance semantics, competitor research and failure analysis are ahead of implementation and integration.

The repository has a static/simulated UI prototype and a substantial research/contract baseline. It does not yet demonstrate a selected real execution backend, a mobile runner, a durable execution receipt, artifact integrity/release, or the complete run -> inspect -> report -> AI correction -> reviewed rerun loop. The first usable MVP is therefore **not close yet**. The next milestone is a narrow real vertical slice, not another broad feature set.

Progress is smooth in discovery and specification. Delivery is not yet smooth because the environment is phone-first, the execution path is not selected, and there is no real runner integration or device evidence. This is a real bottleneck, not a reason to inflate the estimate.

## What exists versus what remains

### Evidence-backed progress
- Product goals and hard boundaries documented.
- LOOP-01..14 and CASE-01..16 preserved; D-01..D-08 remain owner decisions.
- Mobile process-death, reconnect, receipt-sourceability and workspace checkpoint risks researched.
- Happy Coder offline-first outbox and cursor patterns inspected.
- Cline SSH remote-environment and SQLite claim/lease scheduler inspected.
- OpenHands same-ID lost-create-ack retry and event-store patterns inspected.
- Two small reference utilities are already in the research vendor area; they are not integrated into the product.
- Competitor audit recommends an evidence-first task runner, not a mobile IDE or hosted-agent clone.

### Not demonstrated
- A selected, affordable, authorized execution backend.
- Real code execution on a supported device or remote host.
- Enforced sandbox/network/resource boundary.
- Durable command outbox with same-ID deduplication and authoritative lookup.
- Ordered event replay with explicit gap detection.
- Honest process-death/timeout/cancel/termination semantics.
- Immutable receipt, artifact hash verification and separately authorized release.
- AI handoff, reviewed correction and linked rerun.
- Physical iOS/Android acceptance.

## Architecture decisions to carry forward

1. Keep command outbox, remote execution, local runner, observation sync, immutable result receipt and workspace checkpoint as distinct identities/state machines.
2. A lost dispatch acknowledgement must become `DISPATCH_UNKNOWN`. Reconcile the same command ID. Never mint a replacement or blindly replay a non-idempotent command without a host dedupe/query guarantee.
3. Require versioned adapter capabilities: command dedupe, command lookup, ordered replay, gap detection, cancellation, termination confirmation, resumable artifact transfer and snapshot references. Missing capability means no assumed behavior.
4. OpenHands conversation-create idempotency is not command idempotency. Its event-store failure-to-empty and missing-ancestor bridging behaviors are explicitly rejected for authoritative execution evidence.
5. Cline SSH is a future optional user-owned-host adapter, not a mobile runner or sandbox proof. Cline's SQLite leases are a design/test reference, not distributed exactly-once coordination.
6. Do not add scheduling, multiple agents, IDE breadth or cloud execution before one vertical slice is proven.

## Ordered delivery gates

**Gate 0, decision and feasibility**
- Complete the already-designed fixed-task execution-path comparison using available $0/free-tier options.
- Score each candidate for device compatibility, availability without a PC, isolation, network policy, resource limits, interruption, idempotency, event replay, artifact transfer, privacy and ongoing cost.
- Choose one path only if evidence supports it. If no candidate passes, explicitly narrow the first slice rather than imply execution is solved.

**Gate 1, minimum vertical slice**
- Create/import one tiny project and explicit input.
- Bind exact command, target, workspace and policy to explicit user authorization.
- Execute one bounded deterministic task.
- Capture actual runtime, exit/termination, stdout/stderr and stage provenance without fabricating unavailable fields.
- Hash and inspect one output artifact.
- Persist a receipt and recover it after app restart.
- Export a compact report.

**Gate 2, correction loop**
- Send the report to an external AI through explicit paste/share.
- Accept a proposed correction only after diff and exact-scope review.
- Create a linked new attempt, preserving prior receipt and artifacts.
- Demonstrate that failed, incomplete, timed-out and unknown outcomes remain distinct.

**Gate 3, reliability**
- Test lost acknowledgement, duplicate delivery, event gap, stale cursor, process death, force quit, OS expiration, reconnect, account switch, low storage, artifact-transfer interruption and cancellation uncertainty.
- Run physical iOS and Android acceptance. A UI simulator is not a substitute.

## Scope and governance
- No provider, host, cloud runtime, spend, secret access, app install, product source/test edit, CI/Actions or deployment is authorized by this research checkpoint.
- Keep LOOP/CASE/D IDs unchanged.
- Do not modify protected PR #2 or #3.
- No upstream code was copied in the latest Cline/OpenHands audit; upstream tests were inspected, not run.
- Treat the upstream MIT/Apache sources as patterns. Any later code adoption needs exact pinned commit, license/notice retention, source closure, security review, adaptation record and project tests.

## Current GitHub snapshot
- Research branch: **690 ahead / 0 behind** `main`; merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- Branch head observed: `27a89fbed6a5b1c4d3a44e5398026fc220f918d6`.
- PR #2 and #3 are OPEN / DRAFT / UNMERGED. Untouched.
- Ahead count is accumulated research-branch divergence, not feature completion.

## Next chat instruction
Start with this checkpoint and the linked competitor audit `RESEARCH/REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md`. Do not restart broad competitor discovery. Work next on the fixed-task comparison and a minimum provider-neutral command/receipt contract, then stop at the authorization boundary.
