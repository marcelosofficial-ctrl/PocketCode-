# P39 owner-delegated policy decisions (OD-01..OD-13)

**Date:** 2026-11-11  
**Authority:** The owner explicitly delegated product decisions to ChatGPT in this conversation ("You are the boss. Make the decisions that fit our project best"). This record adopts conservative defaults from the existing P39 register, reviews and canonical crosswalk.  
**Status:** POLICY DECISIONS ADOPTED; IMPLEMENTATION / P40 EXECUTION NOT AUTHORIZED BY THIS RECORD.  
**Scope:** PocketCode only. No canonical LOOP/CASE/D ID changes; no stack, provider, runtime, database, host, transport or storage selection.

## Decisions

| ID | Decision | Rationale / boundary |
|---|---|---|
| OD-01 | **NO live/incremental result or artifact streaming in first MVP.** Keep bounded artifact download/share in MVP only after the complete artifact is staged, integrity-verified and authorized. | Avoid chunk-level revocation/resume complexity. NO streaming does not mean NO artifact release. No streaming progress/resume claims. |
| OD-02 | Re-check current authorization and policy immediately before worker claim. If revoked, expired or unknown, deny claim and record a fenced, explicit non-success state. Preserve the original reservation/idempotency record for audit; do not silently replace it. | A committed grant reservation is not irrevocable permission to transfer. |
| OD-03 | For an already-started bounded transfer, stop issuing further bytes at the next enforceable boundary, request transport cancellation, and require acknowledgement tied to the same transfer/attempt. Until confirmed, report transfer INCOMPLETE and block success/release claims. Already emitted bytes cannot be recalled. | No claim of instantaneous revocation. Distinguish emitted, accepted and acknowledged bytes. |
| OD-04 | Recovery lookup returns the same grant/receipt identity but never authorizes bytes. Resume/retry requires a fresh current-policy decision and a new capability bound to current fence, exact object version, operation and range. | Idempotent recovery is not renewed authorization. |
| OD-05 | Grant commit must perform a linearizable current-policy-epoch check at its commit boundary, or use an independently reviewed equivalent protocol with a proven race bound. Stale/unknown epoch fails closed. Never claim atomicity across independent authorities without proof. | Preserve revocation ordering without selecting a database or policy service. |
| OD-06 | Lease expiry, takeover and authoritative commit/observation timestamps use adapter/coordinator-owned authoritative time. Worker/caller timestamps remain untrusted observations and cannot extend or steal leases. | Prevent caller-clock manipulation. Exact clock service remains unselected. |
| OD-07 | Grant/event/receipt identities are globally unique; sequence and fence high-water are durable and restore-safe, with explicit collision detection. In-memory counters or resettable row counts are insufficient. | Require restart/restore continuity without choosing an implementation. |
| OD-08 | Compact ReceiptHead binds an immutable receipt ID and revision to its digest, or an authenticated immutable reference that resolves to those exact values. Reservation verifies exact receipt content and artifact digest/quarantine before authorization. | Avoid copying large manifests while preserving exact-content binding. |
| OD-09 | Child exit zero with a missing/mismatched required policy or egress barrier is **INCOMPLETE**, never PASS, and records a security-boundary violation. Artifact is blocked/quarantined pending trusted reconciliation. Use rejected-before-execution only when trusted evidence proves execution never began. | Missing barrier is not a successful run. |
| OD-10 | Keep child execution verdict separate from overall evidence/job disposition and artifact disposition. Required collection/integrity/security gates missing or unknown make the overall result INCOMPLETE even if child exit was zero. Optional telemetry/housekeeping may be degraded without erasing a proven execution result. Cleanup needed to prove containment or safe release is required, not optional. | Preserve facts without collapsing execution and evidence quality. |
| OD-11 | Use a typed, coordinator-resolved projection retaining raw lifecycle, child exit, wrapper exit, termination cause/acknowledgement and provenance. Renderer displays the resolved projection; it does not authenticate or reclassify. Keep the legacy two-field helper unchanged until a separately reviewed versioned report contract is approved. Contradictions render INCOMPLETE. | No precedence-only formatter patch. |
| OD-12 | Termination/cleanup is confirmed only by authoritative process/transport acknowledgement bound to the same attempt and execution identity. Request, wrapper exit, disconnect or signal-shaped code alone is not proof. Without acknowledgement, termination/cleanup remain UNKNOWN and artifact release is blocked where safety requires it. | Preserve CASE-04 as INCOMPLETE / timed_out until trusted evidence supports another result. |
| OD-13 | Distinguish server-staged, transport-accepted/emitted, client-observed and client-acknowledged bytes. Claim client-confirmed receipt only from a client acknowledgement bound to the exact artifact digest/object version and byte range. | Server progress or matching caller-supplied digest does not prove client receipt. |

## Dependency and implementation boundary

1. OD-01 excludes live streaming from MVP; it does not remove bounded artifact download/share.
2. OD-02..05 govern the full bounded-transfer authorization lifecycle: pre-claim, active transfer, retry/resume and pre-commit policy consistency.
3. OD-06..07 are adapter invariants before any persistence/time technology choice.
4. OD-08 is the receipt-head content-binding rule.
5. OD-09..12 govern security-barrier verdicts, evidence completeness, projection and termination/cleanup.
6. OD-13 governs any client-receipt wording or metric.

**Gate:** These decisions resolve the product-policy questions OD-01..OD-13. They do not prove the models or adapters conform. P39/P40 implementation remains gated pending a separately scoped, source-pinned model-only authorization and explicit execution approval. No source/test edits or test runs are authorized here. No provider calls, spending, deployment, device tests, PR changes, or runtime/provider/database/transport/storage selection. CASE-04 remains INCOMPLETE / timed_out. Preserve LOOP-01..14, CASE-01..16 and all D-IDs.

**Evidence:** VERIFIED that the owner delegated these decisions in the 2026-11-11 conversation and that the recommendations are recorded in the P39 decision register. INFERRED policy choices adopted as conservative defaults. UNKNOWN whether any implementation or production adapter conforms. Tests NOT RUN.
