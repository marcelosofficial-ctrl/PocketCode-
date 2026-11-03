# Shared Contract Golden Fixture Catalogue — ChatGPT Preliminary Review

**Date:** 2026-11-01  
**Status:** Independent preliminary review only. PROVISIONAL / NOT OWNER-APPROVED / NOT A SCHEMA FREEZE / NOT EXECUTABLE ACCEPTANCE.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Catalogue reviewed:** `AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_20261101.md`, blob `6b27791356ecf34d28e457030dd04a2b796cc6ca`.  
**Companion authority:** `AI_COLLAB/SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md`, blob `5d3fa6068f4979d404739cc5cedebd36452bea05`.  
**Related adversarial review:** `AI_COLLAB/UNIFIED_COORDINATOR_ADVERSARIAL_REVIEW_20261101.md`.  
**Purpose:** Record one independent semantic/acceptance review before Claude and Gemini provide their own reviews. This document does not amend the catalogue or any canonical acceptance suite.

## 1. Executive verdict

The 18-fixture catalogue is a sound provisional semantic baseline. Its strongest design choice is to describe cross-product invariants while preserving product-specific identity, execution authority, persistence, authorization, acceptance and proof requirements. The seven state/evidence axes are materially better than a universal status field.

I found no reason to discard the catalogue or change the shared product direction. I do recommend tightening several fixture preconditions and proof boundaries before serialization or schema freeze.

**Disposition: retain SCF-001..018 unchanged as provisional IDs; request clarifications and supplemental subcases; obtain Claude and Gemini reviews before drafting a shared schema.**

## 2. What is already strong

1. The catalogue distinguishes execution outcome, job disposition, evidence capture, publication, release authorization, transfer/delivery and user-facing verdict.
2. It treats UNKNOWN as a valid result and forbids fabricated exit codes, terminal evidence, release and receipt.
3. It distinguishes same-identity/same-content replay from changed-content conflict.
4. It preserves the no-rerun rule when publication or report acknowledgement is ambiguous.
5. It correctly identifies that leases/fencing do not stop an external process or provider call.
6. It makes artifact expectation explicit, including NOT_REQUIRED.
7. It distinguishes runtime-enforced limits, collector truncation and report-display truncation.
8. It orders evidence capture before destructive cleanup.
9. It distinguishes release authorization from transfer and client-verified receipt.
10. It keeps shared fixture IDs supplemental and does not claim equivalence with LOOP/CASE, COORD/DR, P8U/P0-D, RelayRef, AEC or AWC.

These properties should be preserved in all follow-up revisions.

## 3. Fixture-by-fixture review

| Fixture | Verdict | Required clarification before schema/test freeze |
|---|---|---|
| SCF-001 Accepted, not started | Retain; tighten proof precondition | Absence of dispatch intent/provider operation is evidence of NOT_RUN only if every possible external-start path is authoritatively gated by durable intent-before-call. Otherwise retain UNKNOWN. An empty coordinator record cannot prove no out-of-band start. |
| SCF-002 Dispatch intent, start acknowledgement unknown | Retain | Explicitly bind the original attempt, operation ID, provider-token namespace and fingerprint. A transient NOT_FOUND is not definitive non-creation unless the provider contract proves it. Preserve the same token across reconciliation. |
| SCF-003 Same identity/content replay | Retain; split variants | Request reservation, provider event, report append and publication are different identity namespaces with different canonicalization and retention rules. Keep one shared replay invariant but define namespace-specific variants rather than one generic idempotency oracle. |
| SCF-004 Same identity/conflicting content | Retain; split variants | State exactly which immutable fields are bound for each identity type: request fingerprint, event source/scope/payload digest/sequence, report append content, artifact digest/object version. Conflict handling may differ (reject, quarantine, manual reconciliation) but must never be last-write-wins. |
| SCF-005 Execution PASS, publication retry | Retain | Require durable exact result identity/hash and trusted terminal/child-exit provenance. A wrapper exit or publication success must not substitute for child terminal evidence. RevDev P8U is the closest native proof; PocketCode has no equivalent publication adapter established. |
| SCF-006 Execution FAIL, publication retry | Retain | Clarify that failure requires trusted child/program evidence, not merely a wrapper/coordinator error. Preserve partial diagnostics and original result identity. Keep the explicit caveat that RevDev P8U does not directly cover this exact failed-result fixture. |
| SCF-007 Cancellation requested, still active | Retain | Distinguish cancellation request, provider acknowledgement, cancellation accepted, process-stop observation and confirmed termination. If latest trusted evidence says active, outcome remains RUNNING; if there is no authoritative status, UNKNOWN. Neither browser abort nor cancellation acknowledgement alone proves termination. |
| SCF-008 Stale worker after takeover | Retain; expand | Require both fencing epoch and expected state-version/CAS checks for every protected mutation. Add the delayed external Start race: a worker can pause after its last local check and call the provider after takeover. Database fencing alone cannot retract that call. Preserve authenticated late evidence while rejecting stale projections/writes. |
| SCF-009 Out-of-order attempts | Retain | State whether attempts belong to the same logical job or independent jobs in each variant. Bind every output/report/artifact to its own attempt. Define latest-pointer ordering independently of publication time; exact result identity must not be a mutable pointer. |
| SCF-010 Missing/contradictory terminal evidence | Retain | Preserve all source observations and scope. Contradictory terminal evidence blocks PASS, but do not erase a separately confirmed nonzero child exit merely because cleanup is UNKNOWN. Keep execution verdict and release eligibility distinct. |
| SCF-011 Runtime vs collector vs display truncation | Retain; narrow terminology | The current “output/resource limit” wording can accidentally combine output, CPU, memory, disk and time limits. Keep this fixture specifically about output limits, and use separate policy facts for other resource limits. Collector caps must not imply process termination; drain/discard behavior must avoid pipe deadlock. |
| SCF-012 Artifact-free success | Retain | Bind NOT_REQUIRED to the trusted, versioned task/acceptance definition. An empty output listing or untrusted client flag is insufficient. Report publication may still be required even when artifact publication is not applicable. |
| SCF-013 Cleanup before durable evidence | Retain | Define the required evidence manifest per task class. Preserve a trusted raw terminal outcome if already known; missing required evidence may block the user-facing PASS, but optional diagnostics/streams must not become universal gates. If cleanup already happened, record exact evidence loss/unknown rather than inventing it. |
| SCF-014 Release authorized, transfer not started | Retain | Bind decision to principal, scope, policy revision, exact immutable object version/digest and validity interval. Explicitly state that authorization does not imply first-byte disclosure or transfer start. |
| SCF-015 Partial/interrupted transfer | Retain; expand | Distinguish bytes sent, server-side stream completion, client receipt and client digest verification. Define range/retry semantics and authorization revocation during an in-flight transfer. Revocation cannot recall bytes already sent. |
| SCF-016 Report append acknowledgement lost | Retain; expand | Bind append operation ID to immutable canonical content and expected report version. Same ID/same content is idempotent; same ID/changed content conflicts. A new evidence watermark or projection schema/rules version may require a new immutable report version even when job ID is unchanged. |
| SCF-017 Publication partially commits | Retain | Define the required consistency set for each publication type. Track each store/object/manifest/report commit independently; orphan objects remain unservable/quarantined. Garbage collection must coordinate with pending publication and reconciliation. Do not imply cross-store atomicity. |
| SCF-018 Newer result vs older republish | Retain | Define the authoritative monotonic ordering key for the latest pointer. Publication retry time must not make an older execution “newer”. Exact historical results remain addressable independently of the pointer. |

## 4. Cross-cutting additions already identified elsewhere

The catalogue should not receive duplicate canonical SCF IDs merely to absorb every adversarial case. The following proposed labels already exist in `UNIFIED_COORDINATOR_ADVERSARIAL_REVIEW_20261101.md` and should remain supplemental:

- **CAS-01:** same-epoch concurrent writes require expected-version compare-and-swap.
- **DISPATCH-01:** a delayed provider Start may arrive after worker takeover despite an earlier valid local dispatch authorization.
- **CANCEL-01/02:** cancellation request/acknowledgement is not proof of termination.
- **EVENT-01..05:** provider event identity, payload digest, sequence scope and conflict handling.
- **PROJECTION-01:** projection commit binds an immutable accepted-event-set watermark.
- **PUB-03:** garbage collection must coordinate with pending artifact publication.
- **TOKEN-05:** provider idempotency retention must cover the full job/outage/delayed-request uncertainty horizon.
- **REL-04:** transfer revocation cannot recall bytes already sent.

These labels are proposals, not canonical LOOP/CASE/P8U/P0-D acceptance IDs, and remain NOT RUN. Reuse existing COORD/DR/LOOP/CASE/P8U IDs where exact semantics match; do not renumber them.

## 5. Native acceptance mapping cautions

The catalogue's mapping is generally conservative. Keep these qualifications explicit:

- SCF-001's CASE-06/CASE-13 links are contextual only; neither alone proves durable acceptance with no start.
- SCF-003's P8U-04/P8U-12 links cover specific exact-result and duplicate-terminal/audio behaviors, not every request/event/report idempotency namespace.
- SCF-005 maps strongly to RevDev P8U publication recovery, but LOOP-03 is an execution-verdict authority, not a publication-retry test.
- SCF-006 is a useful extension; do not claim an existing P8U case proves failed-result publication retry.
- SCF-008 has no canonical LOOP/CASE equivalent proving fencing.
- SCF-010's script-reported PASS/nonzero-exit cases are related evidence-trust scenarios, not automatically equivalent to two authenticated contradictory provider terminal events.
- SCF-017's P8U-04/05 links are exact-result identity/conflict analogies, not proof of cross-store transactionality.
- SCF-018's CASE-16 link is partial; P8U-08 is the closer latest-pointer publication invariant.

All product bindings must retain the original suite ID and exact scenario/assertion meaning. A shared fixture pass never promotes a native acceptance result.

## 6. Required owner decisions and schema blockers

The exact owner decision register remains authoritative. The following are current research defaults/statuses, not owner approvals:

- **D-01 — confirmed execution limit verdict:** preserve the canonical CASE-04 working default: a trusted enforced timeout remains INCOMPLETE / timed_out, with the limit cause recorded separately (candidate disposition LIMIT_EXCEEDED). Do not silently reclassify timeout as FAIL. Collector-only and display-only truncation remain distinct. D-01 remains OPEN for any future canonical change.
- **D-02 — provider failure without child exit evidence:** working default is user-facing INCOMPLETE and execution outcome UNKNOWN; use PROVIDER_ERROR disposition only when the infrastructure cause itself is confirmed. Never invent an exit code. A separately trusted nonzero child exit remains FAIL even if cleanup is UNKNOWN. Owner confirmation remains OPEN before schema/test freeze.
- **D-03 — output completeness:** working default is no universal complete-output/artifact gate. Only streams/artifacts explicitly required by the particular acceptance case can block that case's PASS; optional diagnostics may be PARTIAL/UNAVAILABLE without automatically invalidating a trusted exit-zero result. D-03 remains OPEN before schema/gate freeze.
- **D-04 — event identity scope:** proposed source replay scope is source namespace + tenant + job + attempt + source event ID, with coordinator-owned canonical event identity, authenticated scope/policy binding before reduction, and immutable observation comparison. This is not frozen. D-04 remains OPEN.
- **D-05 — applied-policy binding:** BLOCKED until an actual execution boundary proves an immutable per-attempt policy revision or equivalent atomic/conditional dispatch barrier. A request fingerprint, acknowledgement or ETag alone is not proof of applied enforcement.
- **D-06 — idempotency and ambiguous dispatch:** proposed durable tenant-scoped reservation plus versioned semantic fingerprint; same key/same fingerprint resolves to the original job/attempt; changed fingerprint conflicts before dispatch; persist intent before external start; reconcile the same identity after ambiguity. UNKNOWN lookup means no automatic redispatch. Exactly-once execution remains unclaimable without provider semantics and persistence proof.
- **D-07 — artifact release:** proposed separate, current authorization bound to principal, tenant/job/attempt, trusted manifest, quarantine, exact immutable object identity/digest and safe bytes at release. Execution PASS is not a download permission.
- **D-08 — report history:** proposed immutable issued versions, atomic monotonic version allocation, idempotent append identity, immutable evidence references and crash-safe reconciliation. In-memory ReportHistory is not durable proof; tombstone expiry requires a trusted-time and atomic replacement rule.

Do not resolve any decision by silently selecting an enum or writing a test that assumes one proposal. In particular, keep D-01..D-04 open where the register says OPEN, and keep D-05 BLOCKED. The owner decision register and packet distinguish lifecycle D-01..D-04 from the separate AI Workflow Director D-01..D-08 namespace.

## 7. Claude and Gemini independent review request

Both reviews should use the exact catalogue blob above and the current companion crosswalk. Return findings against SCF-001..018 individually, even when the verdict is “no issue”.

### Claude — lead developer / architecture and implementation feasibility

1. For each fixture, identify the authoritative producer and native identity required to prove it.
2. Identify where the invariant can be enforced: client, coordinator, durable store, provider adapter, host process, artifact store or delivery API.
3. Distinguish what can be proved by pure helper, fake adapter, persistence test, provider/host test and device test.
4. Challenge whether each proposed state transition can be implemented without losing native RevDev/PocketCode semantics.
5. Identify migration, concurrency, recovery and operational complexity; propose the smallest clarifications.
6. Do not implement, change PRs, select a provider/store, freeze a schema or replace product goals.

### Gemini — independent security/spec/adversarial audit

1. For each fixture, attempt a concrete false-PASS, false-FAIL, cross-tenant, replay, stale-worker, data-loss, disclosure or false-receipt counterexample.
2. Challenge trust assumptions, missing/contradictory evidence, identity scope, policy revision, event provenance, output/report injection, cleanup and authorization races.
3. Identify omitted transitions and prove whether each is already covered by a canonical or proposed test.
4. Audit every product-native mapping for false acceptance equivalence.
5. Return minimal synthetic inputs, expected vs actual behavior if source evidence exists, and the exact additional assertion required.
6. Do not implement, change PRs, select a provider/store, freeze a schema or replace product goals.

### Required format from both reviewers

For every finding provide:
- SCF ID and exact subsection;
- severity and confidence;
- source/branch/blob or explicit “design-only” basis;
- minimal counterexample or implementation constraint;
- expected invariant and failure mode;
- existing canonical IDs that already cover it;
- proposed supplemental test label only if necessary;
- whether it blocks semantic approval, schema design, implementation or a higher proof level.

Keep disagreements visible. “No issue found” is an acceptable per-fixture result when supported. Do not turn a proposed test into a passed test.

## 8. Fixed-task alignment discovered during this review

The existing `PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md` already defines the canonical synthetic `items.csv` → `summary.json` success/failure experiment, exact expected values, Decimal arithmetic, fresh-workspace protocol, alternative paths and measurement rules.

The newer execution-boundary crosswalk previously suggested a different CSV-cleaning/CSV-to-CSV task “for example”. That is not adopted as a replacement. The crosswalk's Section 11 has been aligned to the existing worksheet so the project has one canonical fixed task. A second task should be introduced only if the first task reveals a material gap and the owner approves it.

The iPhone/Safari LOC-01..24 cases refine the browser-local test conditions; they do not change the canonical task or establish that it has run.

## 9. Evidence status and non-actions

- Catalogue review: ChatGPT preliminary static semantic review only.
- Claude review: NOT RECEIVED in the current branch snapshot.
- Gemini catalogue review: NOT RECEIVED in the current branch snapshot; the existing Gemini open-source research audit is not a substitute for this specific fixture review.
- Shared schema: NOT FROZEN.
- Canonical LOOP/CASE/P8U/P0-D/RelayRef/AEC/AWC acceptance: UNCHANGED.
- Owner decisions D-01..D-08: NOT RESOLVED by this review.
- Tests, provider workloads, device execution and runtime security acceptance: NOT RUN.
- No source/test implementation, PR #2/#3, default branch, provider, account, workflow, Actions, billing, deployment, merge, PC host or queue was changed or exercised.

**Recommendation:** retain the 18 fixtures, apply the clarifications only after Claude and Gemini have independently reviewed them, then build a field dictionary and traceability matrix. Do not draft/freeze a shared schema yet.


## 7. Independent Claude and Gemini review requests — 2026-11-03

The next useful reviewer pass is a **fixture-by-fixture adversarial review of the existing 18-item catalogue**, not another broad architecture review. The catalogue remains PROVISIONAL / NOT OWNER-APPROVED / NOT A SCHEMA FREEZE. Preserve SCF-001..SCF-018 exactly. Do not draft or freeze a schema, modify canonical acceptance, or edit repository files.

Exact current review inputs on branch `pocketcode-execution-boundary-crosswalk-2026-11-01`:
- `AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_20261101.md`, blob `6b27791356ecf34d28e457030dd04a2b796cc6ca`.
- `AI_COLLAB/SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md`, blob `5d3fa6068f4979d404739cc5cedebd36452bea05`.
- `AI_COLLAB/STATE_AND_IDENTITY_MAPPING_PREPARATION_20261101.md`, blob `783907a5a93443f440fbb11c88e55352341ffb32`.
- This preliminary review, prior to this append, blob `cdb0e6b9fd15373eacb6ebf05950542d1662be7b`.

### Assignment to Gemini: independent security and false-PASS red team

> Review every existing fixture SCF-001 through SCF-018 in the exact catalogue and its companion state/identity crosswalk. Your job is to find realistic false-PASS, false-FAIL, authorization, identity, replay, evidence-provenance, stale-write, recovery, cleanup, publication, release, transfer/receipt, and projection errors.
>
> For every SCF ID, return PASS / QUALIFIED / GAP as a review verdict, the strongest counterexample or reason no material issue was found, the exact evidence that would distinguish the states, and the minimum additional assertion/precondition needed. Prioritize the most severe cross-fixture gaps; do not inflate small wording preferences into security defects.
>
> Explicitly challenge: whether UNKNOWN is preserved; whether absence is backed by a complete oracle; whether identity scope and content digest are sufficient; whether late external side effects survive takeover/cancellation; whether event/report/artifact identities are in separate namespaces; whether policy/authorization is bound to the actual operation; whether exact result publication is distinguished from release and client receipt; whether stale/out-of-order evidence can regress mutable projections.
>
> Keep SCF IDs unchanged. Any supplemental case labels must be clearly proposed and must not replace AEC, LOOP/CASE, COORD/DR, P8U/P0-D, AWC or RelayRef acceptance. Do not edit or commit. Do not claim tests ran unless they actually ran; no provider call, spend, deployment or Actions.

### Assignment to Claude: architecture and implementation-feasibility challenge

> Independently review the same exact 18-fixture catalogue plus the state-domain and identity mapping documents. Focus on whether each fixture has an implementable, observable acceptance oracle and whether the state/identity boundaries can be represented without flattening distinct lifecycle domains.
>
> For each SCF ID, return PASS / QUALIFIED / GAP, the responsible conceptual component(s), required durable facts and transition order, evidence source needed, and smallest regression-test shape. Challenge atomicity assumptions, retry/replay, fencing and compare-and-swap, branch/attempt correlation, multi-store publication, retention/garbage collection, cleanup ordering, receipt verification, and monotonic latest-pointer behavior.
>
> Identify cases where the same event/result can mean different things in PocketCode versus RevDev, and cases where shared wording would conceal a different trust/authorization boundary. Do not map an SCF fixture to a canonical native acceptance ID unless the exact semantics match; explain partial mappings.
>
> Keep all 18 IDs and current owner decisions unchanged. No schema freeze, code changes, test modifications, PR actions, provider workloads, spending, deployment or Actions. Do not report implementation claims without exact pinned source. Return a ranked evidence-based challenge, including an explicit list of issues that should remain unresolved pending owner decisions.

### Consolidation rule

ChatGPT will compare both reviews against the exact catalogue/crosswalk and current native acceptance sources. Preserve the preliminary review's clarifications unless source evidence disproves them. Any disagreement must be resolved by concrete counterexample and observable proof, not reviewer seniority. Only after both reviews should we update the existing catalogue/preliminary review. The shared fixture catalogue remains provisional; no shared schema or field mapping is frozen.
