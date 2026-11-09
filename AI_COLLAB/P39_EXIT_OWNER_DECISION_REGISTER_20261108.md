# P39 / exit-provenance owner decision register

**Date:** 2026-11-08  
**Status:** DECISION REQUIRED / NO OWNER DECISIONS INFERRED  
**Scope:** Consolidates unresolved product-policy and contract decisions after Claude's P39 review, the receipt-subsystem audit and the EP-01..25 crosswalk. It does not authorize source/test changes, select an adapter/runtime/database/provider/transport, or amend canonical LOOP/CASE/D IDs.

## 1. Decision protocol

- The owner must explicitly choose or amend each proposal. Silence, review delivery, and a model test are not approval.
- Each decision is split into product semantics, model obligations, adapter obligations and evidence needed to close it.
- Recommendations below are conservative proposals, not adopted decisions.
- Until resolved, use the safe operational default stated in each row: do not claim the unsupported capability, do not release/continue bytes on ambiguous authority, and do not turn unknown evidence into PASS.
- Claude's C1-C7 are **CLAUDE-REPORTED VERIFIED-BY-RUN** against a byte-identical copy of the pinned sequential model. The repository suite was not run by Claude. ChatGPT findings are **VERIFIED STATIC** at pinned blobs unless otherwise stated. Production adapter, concurrent-process, durable-store and transport behavior remain **UNKNOWN / NOT RUN**.

## 2. Owner decision table

| ID | Decision required | Options / recommended default | Consequence if unresolved |
|---|---|---|---|
| OD-01 | Is live streaming of result/artifact bytes in MVP? | **Recommend NO for first MVP** unless a concrete phone workflow requires it. Use bounded artifact handoff/download only after a complete, authorized artifact is staged and verified. If YES, explicitly include transport enforcement, revocation, cancellation acknowledgement, resume capability and client-observation evidence. | Keep streaming claims and stream-resume behavior out of MVP acceptance. P39-S4 remains a contract/MVP scope gate, not a sequential-model defect. |
| OD-02 | What happens when authorization is revoked after a grant is committed but before worker claim? | **Recommend re-check current policy before claim; deny claim if revoked/expired and transition through an explicit, fenced non-success state.** Preserve the original reservation/idempotency record for audit and replay; do not silently create a replacement grant. | No claim/resume implementation may assume the reservation is irrevocable. P39-S8 / P39-POLICY-02 remains open. |
| OD-03 | What happens when revocation occurs during an active transfer/stream? | **Recommend stop issuing new bytes at the next enforceable boundary, cancel the transport, require termination/cancellation acknowledgement, and report INCOMPLETE until confirmed.** Bytes already emitted cannot be recalled. Preserve emitted/accepted/client-observed/client-acknowledged counters separately. | No claim of immediate revocation or complete cancellation. If streaming is out of MVP, defer the transport behavior and capability claims rather than pretending worker fencing retracts bytes. |
| OD-04 | What happens on retry/resume after takeover or revocation? | **Recommend idempotent lookup recovers the same grant/receipt but never authorizes bytes.** A fresh current-policy decision and new capability bound to current fence, object version, operation and range are required before transfer resumes. | Recovered grant status alone cannot authorize transfer. RCP-02 / P39-POLICY-06 remain blocking adapter obligations. |
| OD-05 | What consistency guarantee applies if policy revocation and grant commit use separate authorities? | **Recommend fail closed on stale/unknown policy epoch and require a linearizable epoch check at the grant-commit boundary, or a documented equivalent protocol with a proven race bound.** Do not claim atomicity across independent stores without evidence. | P39 pre-commit revocation (RG-H3) remains unresolved. No database/adapter choice can be made from this proposal alone. |
| OD-06 | How is lease/observation time trusted? | **Recommend adapter-owned monotonic/authoritative time for lease expiry and commit/observation timestamps.** Caller/worker occurrence timestamps may be retained as untrusted claims but cannot control expiry or takeover. | Caller-controlled clock remains a model oracle defect (RG-B3) and production time authority UNKNOWN. |
| OD-07 | How are grant/receipt/event IDs and fence epochs kept unique across restart/restore? | **Recommend globally unique IDs plus durable, restore-safe monotonic fence/sequence authority and explicit collision handling.** Never derive durable identity solely from in-memory list length or resettable row counts. | Process-local models cannot claim restart safety. RG-H4 and RCP-01 remain open. |
| OD-08 | What is required in compact ReceiptHead: digest/quarantine copy or immutable receipt reference? | **Recommend immutable receipt ID + revision + digest binding (or an authenticated immutable reference that resolves to the same exact values).** Avoid duplicating large manifest state, but reservation must verify the exact receipt content and artifact digest/quarantine before authorization. | RG-O2 / P39-RECEIPT-02 remains a contract decision. Do not add redundant fields without deciding the binding invariant. |
| OD-09 | EP-18: child exits zero but required policy/egress barrier is absent or mismatched. | Minimum invariant: **never PASS** and record a security-boundary violation. **Recommend INCOMPLETE** unless trusted evidence proves the child was prevented from executing, in which case use the separately defined rejected-before-execution semantics. Artifact retention/release must be separately denied or quarantined pending review. | Verdict and artifact disposition remain owner-unresolved; no implementation test should freeze a more specific result. |
| OD-10 | EP-24: natural child exit zero, then wrapper fails during required collection/cleanup. | **Recommend separate execution verdict from overall job/evidence disposition.** Child execution fact remains succeeded/exit-zero; overall result is INCOMPLETE if required evidence/cleanup gates are missing, while optional cleanup degradation may preserve execution PASS with a degraded artifact disposition. Owner must define which operations are required gates. | Formatter must not collapse these axes. No EP-24 expected verdict until required-vs-optional gate policy is explicit. |
| OD-11 | EP-04/05: how can contradictory child/lifecycle facts render INCOMPLETE? | **Recommend typed, coordinator-resolved projection** retaining raw lifecycle, child exit, wrapper exit, termination cause/acknowledgement and provenance; renderer displays the supplied resolved verdict without authenticating or reclassifying. Keep legacy two-field helper unchanged until a versioned report contract is approved. | Current format_report()/classify_verdict() cannot produce proposed INCOMPLETE for these contradictions. No precedence-only patch. |
| OD-12 | What confirms termination and cleanup after timeout/cancellation? | **Recommend authoritative process/transport termination acknowledgement tied to the same attempt and execution identity.** A request, wrapper exit, disconnect or signal-shaped code alone is not proof. If acknowledgement is absent, termination and cleanup remain UNKNOWN; block artifact release where required. | EP-21/23 cannot be closed; CASE-04 remains INCOMPLETE / timed_out. |
| OD-13 | What evidence is required to say the client received bytes? | **Recommend distinguish server staged, transport accepted/emitted, client-observed and client-acknowledged bytes.** Only client acknowledgement proves the client confirmed receipt; do not infer it from server progress or matching a caller-supplied digest. | RCP-04/P39-S4 remain transport evidence limitations. Do not describe model completion as proof of client receipt. |

## 3. Proposed dependency order

1. Resolve OD-01 first. It determines whether transport stream obligations are MVP requirements or explicit deferrals.
2. Resolve OD-02 through OD-05 as one policy lifecycle: pre-commit race, pre-claim revocation, active transfer, takeover and retry/resume. Do not decide each phase inconsistently.
3. Resolve OD-06 and OD-07 as adapter invariants before selecting or testing a persistence technology.
4. Resolve OD-08 compact receipt binding without weakening the richer ResultReceipt integrity guarantees.
5. Resolve OD-09/10/11/12 together as the report projection and termination evidence contract. Preserve CASE-04.
6. Resolve OD-13 if any transfer path exposes progress or completion to the user.

## 4. Gate and implementation authorization

**Current decision:** P39/P40 implementation gate remains **CLOSED**.

The following can be prepared after owner decisions, but are not yet authorized:
- a model-only P40 test plan with P39-prefixed IDs;
- a typed projection contract and pure tests for EP-04/05;
- model tests for canonical event bytes, metadata mutation, event-to-grant binding, relay fencing, trusted time and ID reuse;
- adapter acceptance scenarios for two-process races, crash/restart/restore and atomic commit.

The following remain unauthorized:
- changes under scripts/ or tests;
- a durable adapter or database/provider/runtime/transport selection;
- any claim of production revocation, durable atomicity, stream cancellation or client receipt;
- changes to canonical LOOP/CASE/D IDs or PR #2/#3.

## 5. Review status and evidence pins

- Claude P39 review: reconciled in `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`; Claude did not read the receipt subsystem/durable adapter contract and did not run the repository suite.
- Receipt subsystem: bounded static audit in `P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md`, source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`; no tests run by ChatGPT.
- Canonical mapping: `P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md`; canonical LOOP/CASE definitions remain unchanged.
- Exit provenance: `EXIT_PROVENANCE_RESOLUTION_20261108.md` and `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md`; an additional Claude exit-provenance artifact is not currently a separate OPEN inbox assignment. Await any further review supplied by the owner or later reprioritization.
- Gemini's independent P39 source-pinned review is received and reconciled in `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`. Its test matrix is NOT RUN; reconciliation corrects multiple source/module misattributions. The review does not close owner decisions.
- CI: latest branch HEAD must be checked separately. Previous 266/266 PASS is tied only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.

## 6. Owner response template

The owner can reply with decision IDs and short choices, or amend any recommendation. Unanswered rows remain OPEN.

| ID | Owner decision |
|---|---|
| OD-01 | OPEN |
| OD-02 | OPEN |
| OD-03 | OPEN |
| OD-04 | OPEN |
| OD-05 | OPEN |
| OD-06 | OPEN |
| OD-07 | OPEN |
| OD-08 | OPEN |
| OD-09 | OPEN |
| OD-10 | OPEN |
| OD-11 | OPEN |
| OD-12 | OPEN |
| OD-13 | OPEN |

**Verification:** documentation only. No source/tests changed or run. No canonical identifier changed.