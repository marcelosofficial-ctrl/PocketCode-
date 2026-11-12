# P39 supplemental model-to-canonical traceability

Date: 2026-11-12  
Status: traceability addendum only; no canonical acceptance change, no tests run.  
Authority: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and `AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md` remain canonical.

## 1. Purpose and rule

The local labels A1–A8, B1–B9, C1–C9, D1–D7 and R2-01–R2-14 organize proposed model tests. They are not LOOP IDs, CASE IDs or D-IDs. They support narrower invariants needed to implement the canonical product safely. A passing local model case cannot close a canonical CASE, prove an adapter, establish device behaviour or authorize release.

## 2. Grant-event model plan: supporting coverage only

| Local group | Canonical obligations it supports | What it still cannot prove |
|---|---|---|
| A1–A8: grant transition parity, reservation atomicity, progress, receipt/artifact binding | LOOP-02/07/10 (honest lifecycle, bounded evidence and safe output); CASE-07/14 (bounded output and unsafe/oversized artifact handling); CASE-13 (idempotent recovery of the same operation) | Real byte transfer, policy authority, durable storage, artifact availability on a device or client receipt |
| B1–B9: canonical envelope, digest, producer and scope validation | LOOP-11/12 (privacy and isolation/security); CASE-13/15 (replay/scope integrity and security boundary evidence) | Cryptographic producer authentication, key revocation, actual egress enforcement or multi-tenant isolation |
| C1–C9: relay lease, fence, stale-ack, retry and order | LOOP-02 (truthful lifecycle); CASE-11/13/16 (reconnect/recovery, ambiguous retry, out-of-order completion) | Real broker delivery, concurrent durable workers, provider state or end-to-end exactly-once transport |
| D1–D7: consumer inbox, gap recovery and restore high-water | LOOP-07/10 (truthful report/artifact recovery); CASE-11/13/16 (same-operation recovery, duplicate handling and order) | Real backup/restore, device persistence, durable inbox transactions or client acknowledgement |

These are inferred support relationships, not a claim that every local case maps one-to-one to a canonical requirement. The 33-case grant plan is primarily a control-plane/event-consistency suite.

## 3. Report projection v2: direct semantic coverage

| Local case family | Canonical traceability |
|---|---|
| R2-01/02: trusted success and program failure | LOOP-03/04; CASE-01/02/03/09/10 |
| R2-03/04/05/08: timeout, cancellation, wrapper-only and lifecycle contradiction | LOOP-02/03/05; CASE-04/05/06/11/13/16 |
| R2-06/07/09: contradictory natural exit and embedded interpreter evidence | LOOP-03/04/05; CASE-02/03/04/06/10 |
| R2-10/11: wrong producer/attempt/tenant/policy binding and missing security barrier | LOOP-11/12; CASE-08/11/13/15 |
| R2-12/13: collection, cleanup, artifact integrity and client acknowledgement | LOOP-07/10/11; CASE-07/12/14 |
| R2-14: legacy format-1 compatibility | Protects existing report semantics and regression compatibility; no standalone canonical CASE is asserted |

The report projection suite is closer to canonical verdict and evidence semantics, but still cannot prove that an authenticated coordinator, process controller, durable receipt store or real browser/host boundary exists.

## 4. Canonical acceptance constraints preserved

- LOOP-01..14 and CASE-01..16 retain their existing wording and meanings.
- CASE-04 remains INCOMPLETE / timed_out until its authoritative same-attempt timeout/termination evidence is proven.
- CASE-13 idempotency and ambiguous-dispatch rules do not imply blind retry; recovery may return the same identity without authorizing bytes.
- CASE-14 safe output-file handling does not mean an artifact is present or releasable.
- CASE-15 egress denial requires enforced boundary evidence, not only a model envelope or CSP declaration.
- Execution verdict, overall evidence/job disposition, artifact disposition and client-confirmed receipt remain separate.
- All local case suites are proposals until separately authorized and executed at exact source/test SHAs.

## 5. Evidence status

- VERIFIED: canonical criteria and existing traceability rows were read from the active branch. Local scenario ranges are present in the two indexed acceptance plans.
- INFERRED: the mapping above identifies which canonical obligations the model scenarios support.
- UNKNOWN: adapter, provider, durable database, authenticated producer/clock, browser-device, transport and client receipt conformance.
- NOT RUN: all supplemental model tests. No canonical LOOP/CASE acceptance is closed by this document.
