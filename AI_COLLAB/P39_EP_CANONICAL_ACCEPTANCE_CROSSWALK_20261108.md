# P39 and exit-provenance canonical acceptance crosswalk

**Date:** 2026-11-08  
**Authority:** PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md blob c6714c27db52b2962fe8d1c7e6a16829d46a8338. This document maps proposals to unchanged LOOP-01..14 and CASE-01..16; it creates no canonical IDs and does not imply implementation or test completion.

## 1. Mapping rule

- **Direct:** canonical requirement states substantially the same product-level behavior.
- **Supporting:** lower-level model/adapter test supplies evidence needed for a canonical scenario but is not itself a product acceptance criterion.
- **No direct mapping:** implementation, storage or operational detail with no distinct product requirement. Keep it in adapter conformance.
- A supporting test must not be reported as passing its canonical CASE. The canonical acceptance remains NOT RUN unless the actual controlled product evidence exists.

## 2. P39 source findings and Claude refinements

| Finding | Closest canonical trace | Relationship and boundary |
|---|---|---|
| P39-S1 / RG-B1 event/version/outbox atomicity, no-op versioning, terminal transitions | CASE-11, CASE-13, CASE-16; LOOP-07 | Supporting. Same-run recovery, idempotent retry, correct run/result association and trustworthy report evidence. Transactional event-chain correctness is adapter-only. |
| P39-S2 / RG-B2 canonical event bytes and digest recomputation | CASE-12, CASE-14, CASE-15; LOOP-07, LOOP-10, LOOP-11 | Supporting. Protects report/artifact integrity and trusted evidence. Hash binding is not producer authentication or proof of safe execution. |
| P39-S3 / RG-H1 grant-event relay claim, lease/fence, ordered delivery | CASE-11, CASE-13, CASE-16 | Supporting. Recovery/idempotency and correct result association. Relay ownership/fencing is adapter-only. |
| P39-S4 / RG-H2 stream enforcement and resumable capability | CASE-04, CASE-05, CASE-11; LOOP-10, LOOP-12 | Supporting only if streaming is in MVP. CASE-04/05 require trusted termination/cancellation evidence; CASE-11 requires same-run recovery. Transport chunk enforcement and capability epochs are adapter details. |
| P39-S5 event-to-existing-grant, tenant/source/effect/attempt binding | CASE-13, CASE-15, CASE-16; LOOP-11, LOOP-12 | Supporting security and identity boundary. Canonical acceptance does not specify a grant-event schema. |
| P39-S6 producer authentication and atomic fence+append | CASE-15; LOOP-12 | Supporting. Authentication and durable atomic append are adapter/security obligations, not directly stated as journal APIs in canonical acceptance. |
| P39-S7 P37/P39 identifier collision | None | No direct product mapping. Documentation/test-governance hygiene only; canonical LOOP/CASE/D IDs stay unchanged. |
| P39-S8 post-commit revocation before claim/during transfer/resume | CASE-05, CASE-11, CASE-15; LOOP-10, LOOP-12 | Supporting and unresolved policy. Canonical CASE-05 concerns cancellation confirmation, not the product's grant-revocation policy. Owner must define in-flight semantics. |
| RG-B3 trusted lease clock | CASE-04, CASE-05, CASE-11 | Supporting. Prevents false lease expiry/takeover during timeout, cancellation and recovery. Trusted time authority is adapter-only. |
| RG-H3 pre-commit revocation epoch | CASE-15; LOOP-12 | Supporting security gate. Strict cross-store revocation linearization is not defined in canonical acceptance; requires owner policy and architecture. |
| RG-H4 non-reused grant IDs/fence continuity | CASE-11, CASE-13, CASE-16 | Supporting identity/recovery. Durable uniqueness and restore-safe fencing are adapter-only. |
| RG-O1 receipt-head historical ID reuse | CASE-13, CASE-16 | Supporting immutable history/run binding. Exact head algorithm is adapter/model detail. |
| RG-O2 compact ReceiptHead digest/quarantine representation | CASE-12, CASE-14; LOOP-07, LOOP-10 | Supporting. Rich ResultReceipt already includes receipt/artifact digests and quarantine; whether compact head duplicates them is a contract decision. |
| RG-O3 stable-intent fingerprint/replay ordering | CASE-13; LOOP-09 | Direct product intent for no accidental duplicate execution; exact fingerprint fields and replay-before-new-head ordering are supporting adapter rules. |
| RG-O4 stored-grant assertion test hygiene | CASE-13, CASE-16 | Supporting test quality only. |
| RG-O5 model crash injection before mutation | CASE-11, CASE-13 | Supporting. Model-only tests do not establish crash atomicity. |
| RG-O6 poison event / head-of-line quarantine | CASE-11, CASE-13, CASE-16; LOOP-07 | Supporting recovery/evidence. HOLD, retry threshold and audited repair are adapter operations. |
| RG-O7 SQLite version/WAL-reset pin | None | No direct mapping. Conditional storage-specific due diligence only; no database selected. |
| RG-O8 journal sequence/quarantine edge cases | CASE-11, CASE-16; LOOP-07 | Supporting evidence integrity; detailed sequence semantics adapter-only. |
| RG-O9 authentication-vs-authorization test naming | None | Test clarity only. |
| RG-O10 Redis fencing reference | None | Research citation only; not a product requirement. |

## 3. Receipt subsystem findings

| Finding | Closest canonical trace | Relationship and boundary |
|---|---|---|
| RCP-01 process-local receipt/grant/event IDs and sequence | CASE-11, CASE-13, CASE-16 | Supporting recovery/idempotency/run identity. Durable identity and sequence authority are adapter-only. |
| RCP-02 transfer resume lacks current-policy gate | CASE-05, CASE-11, CASE-15; LOOP-10, LOOP-12 | Supporting security/recovery. Exact post-commit policy semantics remain owner decision. |
| RCP-03 caller-supplied timestamps | CASE-04, CASE-05, CASE-11 | Supporting trusted lifecycle/lease evidence. Store-owned time is adapter-only. |
| RCP-04 server progress/digest does not prove client receipt | CASE-04, CASE-05, CASE-11; LOOP-10 | Supporting distinction between server and client evidence. Transport observations are adapter-only. |
| RCP-05 no concurrent/durable proof | CASE-11, CASE-13, CASE-16 | Supporting adapter acceptance. The canonical cases need real recovery/retry behavior, but transaction isolation and storage-engine tests are not separate product IDs. |

## 4. Exit-provenance EP-01..EP-25 crosswalk

| EP | Closest canonical trace | Disposition |
|---|---|---|
| EP-01 natural child exit 0 + all gates | LOOP-03; CASE-01 | Direct semantic match. Existing helper test is only SOURCE-COVERED, not product VERIFIED. |
| EP-02 natural child nonzero | LOOP-04; CASE-02/03/10 | Direct semantic match when trusted child identity is established. |
| EP-03 trusted program_failed without child code | LOOP-04; CASE-02/03 | Direct semantic match only if program/runtime failure is independently trusted. |
| EP-04 program_failed + natural child zero contradiction | LOOP-03/04/05; CASE-02/03/06 | Supporting contradiction/reconciliation refinement. Legacy formatter cannot render proposed INCOMPLETE; needs typed projection boundary. |
| EP-05 succeeded + natural child nonzero contradiction | LOOP-03/04/05; CASE-02/03/10 | Supporting contradiction/reconciliation refinement. Same formatter limitation as EP-04. |
| EP-06 timed_out + wrapper 137, child absent | LOOP-05; CASE-04/06 | Direct timeout/infrastructure semantic match. CASE-04 must remain INCOMPLETE/timed_out. |
| EP-07 cancelled + wrapper 143 | LOOP-05; CASE-05 | Direct cancellation semantic match; wrapper exit is not child exit. |
| EP-08 running + wrapper nonzero, child absent | LOOP-05; CASE-06/11 | Supporting infrastructure/uncertain-terminal evidence. |
| EP-09 infrastructure_failed, no child result | LOOP-05; CASE-06 | Direct semantic match. |
| EP-10 trusted child nonzero plus separate infrastructure failure | LOOP-04/05; CASE-03/06 | Supporting two-axis projection; canonical acceptance does not define all combined job dispositions. |
| EP-11 child zero but mandatory gate missing | LOOP-03/06/07; CASE-01/09/15 | Direct no-PASS requirement where a required gate is absent; exact gate-specific outcome may need owner mapping. |
| EP-12 child nonzero plus cleanup unknown | LOOP-04/07/10/11; CASE-03/12/14 | Supporting separation of execution verdict from cleanup/artifact release. |
| EP-13 rejected but child purportedly started/exited | LOOP-02/05; CASE-06/11/13 | Supporting lifecycle/dispatch contradiction. |
| EP-14 wrong tenant/job/attempt binding | LOOP-07/11/12; CASE-11/13/15/16 | Supporting security and same-run binding; coordinator/adapter identity checks. |
| EP-15 malformed/bool/stale exit value | LOOP-03/04/05; CASE-04/05/06 | Supporting input/provenance validation; malformed value alone is not child evidence. |
| EP-16 late unbound exit after timeout | LOOP-05; CASE-04/05/11 | Direct incomplete/recovery semantics; late event reconciliation is adapter detail. |
| EP-17 timeout plus purported natural child exit | LOOP-03/05; CASE-04/05/06 | Direct timeout guard plus ordering refinement. |
| EP-18 child zero but policy/egress barrier absent | LOOP-12; CASE-15 | Direct security requirement, but exact verdict and artifact disposition need owner decision. Minimum: no PASS and security violation recorded. |
| EP-19 collector truncation after child zero | LOOP-06/07/11; CASE-07/09/12 | Direct bounded diagnostics/truncation and script-check separation; exact verdict depends on whether required output is missing. |
| EP-20 wrapper restart reports code without child identity continuity | LOOP-02/03/05/07; CASE-11/13/16 | Supporting identity/recovery refinement. |
| EP-21 termination requested but not confirmed | LOOP-05; CASE-04/05/06 | Direct. Keep INCOMPLETE; do not mark cleanup complete where process may still run. |
| EP-22 wrapper exits zero, child unknown | LOOP-03/05; CASE-06/11 | Direct no-fabricated-success rule; wrapper success is not child success. |
| EP-23 signal/resource termination (e.g. shell 137/143) | LOOP-05; CASE-04/05/06 | Direct timeout/cancel/infrastructure distinction; never reinterpret as natural child failure without trusted evidence. |
| EP-24 child zero, wrapper fails during collection/cleanup | LOOP-03/07/10/11; CASE-09/12/14 | Supporting separation of execution verdict, collection and artifact disposition. Owner must decide whether required collection/cleanup gates make overall result INCOMPLETE. |
| EP-25 timeout/resource limit plus purported natural child nonzero | LOOP-04/05; CASE-04/05/06 | Direct failure-vs-timeout provenance refinement. Trusted ordering required; otherwise INCOMPLETE. |

## 5. True product gaps vs adapter-only details

**Potential product/acceptance decisions requiring owner resolution:**
1. Is streaming part of MVP? If yes, transport revocation/cancellation and client-observation evidence must be accepted; if no, defer stream capability claims.
2. What is the post-commit revocation policy for reserved, not-yet-started, active, taken-over and resumed transfers?
3. What is the pre-commit revocation consistency promise when policy and grant state may live in separate authorities?
4. For EP-18, what exact verdict/disposition follows a missing or mismatched policy/egress barrier? No PASS is mandatory.
5. For EP-24, can execution verdict remain PASS while collection/cleanup disposition is degraded, or are those required gates?
6. Does compact ReceiptHead need a copied digest/quarantine binding, or is a verified immutable receipt reference sufficient?

**Adapter-only conformance (do not create new LOOP/CASE IDs):**
- Atomic aggregate/event/outbox append; canonical envelope digest; consumer tenant/grant/source binding; relay claim/fence/order.
- Trusted clock, non-reused identities, restore-safe fence epochs, cross-process receipt-head/grant races.
- Producer authentication and atomic fence+append.
- Stream chunk capability, cancellation acknowledgement and separate transport/client byte observations, if streaming selected.
- Durable crash recovery, outbox redelivery, poison-event HOLD/quarantine, SQLite/storage version pinning.
- Test-ID namespace checks and model-only test hygiene.

## 6. Current evidence status

- Canonical LOOP/CASE definitions are unchanged. No new canonical ID is proposed.
- Claude's C1-C7 are CLAUDE-REPORTED VERIFIED-BY-RUN against a byte-identical source copy; full repository suite NOT RUN by Claude.
- ChatGPT's source audit and this crosswalk are static reads at immutable pins; no tests run in this unit.
- Previous 266/266 CI remains tied to source/test SHA 744cb4d. Latest documentation HEAD has no workflow run.
- Durable adapter, real multi-process races, production authorization, stream transport, client receipt and database behavior remain UNKNOWN / NOT RUN.
- P39 review gate remains OPEN pending Gemini's complete independent source-pinned review and owner policy decisions.

