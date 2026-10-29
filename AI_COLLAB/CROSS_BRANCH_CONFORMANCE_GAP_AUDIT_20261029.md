# PocketCode — cross-branch conformance gap audit

**Review date:** 2026-10-29  
**Status:** Static source/document audit only. No tests run in this pass, no runtime/provider selected, and no production behavior verified.  
**Purpose:** Identify integration gaps between the existing report-contract work (PR #2), lifecycle/idempotency work (PR #3), and canonical acceptance criteria without changing either PR or canonical contract.

## Executive assessment

The project is making useful progress: the canonical acceptance set is preserved, PR #2 has focused report-formatting regression coverage, and PR #3 has provider-neutral lifecycle/idempotency/artifact models with explicit limitations. The main remaining risk is **not a lack of more broad research documents; it is the missing, explicit conformance boundary between those pieces**.

The two branches are separate drafts. No runner/adapter currently connects them. Therefore the mismatched vocabularies documented below are an integration gap to resolve before wiring, not evidence of a production defect in an integrated service.

**Priority recommendation:** before selecting a runtime or provider, define and test one provider-neutral adapter/result envelope that preserves (1) immutable execution observations, (2) cleanup/evidence state, and (3) derived user-facing disposition. Then prove status mapping, provenance, lost-response recovery, and artifact/report binding with synthetic fakes. Keep provider-specific security tests blocked until an affordable, explicitly authorized test boundary exists.

## Evidence reviewed

Repository and draft links are pinned to the refs below so this review is reproducible.

| Area | Exact source | Evidence status |
|---|---|---|
| Canonical execution contract | [PRODUCT/EXECUTION_CONTRACT.md](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PRODUCT/EXECUTION_CONTRACT.md), blob `3861e51ae4f9e45a263b677402f26c41b240959d` | Proposed contract; unchanged |
| Canonical acceptance | [PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md), blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338` | 14 LOOP criteria and 16 CASE scenarios; proposed, NOT RUN |
| PR #2 report helper | [scripts/report_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/chat-continuity-report-regressions-2026-10-26/scripts/report_contract.py), blob `e9d944a722c2fac5279952696528da72a7011af3` | Pure formatter/classifier; no execution |
| PR #2 report tests | [scripts/test_report_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/chat-continuity-report-regressions-2026-10-26/scripts/test_report_contract.py), blob `39f3a3ef865ed55f333a1edc208096d99197d023` | PR description records 25 passing tests in an offline reconstructed tree for the tested Python files; not UI, runner, backend, or provider validation |
| PR #3 lifecycle helper | [scripts/lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py), blob `ba8d4d0b217c90513bed020e298029ef4e16f164` | Pure provider-neutral model; no process/provider execution |
| PR #3 lifecycle tests | [scripts/test_lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/test_lifecycle_contract.py), blob `39db87d9f44f5e8474f33cff60136e529364199a` | Source contains synthetic assertions; exact checked-in pair and full suite explicitly reported NOT RUN |
| Existing acceptance crosswalk | [AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md), blob `d9df15a3c3a676c02b11fbd2ecc931c6aea4e0c1` | All 14 LOOP and 16 CASE IDs represented; this audit adds an integration-level layer, not a replacement |
| PR #3 offline matrix | [AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md), blob `3a9b214a9ccde9f3abad8dba2d7f14d6c97632ad` | Extensive proposed cases; source/tests not run |

PR #2 and PR #3 remain draft/open/unmerged. This review does not change either PR or the canonical files on `main`.

## Confirmed seams and gaps

### G1 — Report vocabulary and lifecycle vocabulary have no explicit adapter contract (HIGH)

PR #2 recognizes report-level `execution_status` values: `accepted`, `queued`, `running`, `succeeded`, `program_failed`, `timed_out`, `cancelled`, `rejected`, and `infrastructure_failed`. It derives a verdict from `execution_status` and an optional integer `exit_code`.

PR #3 separately models execution outcomes (`NOT_STARTED`, `EXIT_ZERO`, `EXIT_NONZERO`, `TIMED_OUT`, `CANCELLED`, `LIMIT_EXCEEDED`, `UNKNOWN`) and derived job dispositions (`REJECTED`, `PASS`, `FAILED`, `TIMED_OUT`, `CANCELLED`, `LIMIT_EXCEEDED`, `INCOMPLETE`, `PROVIDER_ERROR`). Its `derive_disposition()` requires confirmed cleanup plus policy, termination, artifact, and tenant/job gates for `PASS`.

There is no adapter in these source files that maps one model to the other. A direct mapping of `EXIT_ZERO` to report status `succeeded` would be unsafe if it bypassed the derived disposition and its gates. This is a pre-integration gap, not proof that either isolated helper is wrong.


#### Proposed semantic mapping matrix (not a frozen public schema)

| PR #3 execution outcome | PR #3 disposition / evidence | PR #2 legacy status candidate | Legacy report verdict | Safe interpretation |
|---|---|---|---|---|
| `EXIT_ZERO` | `PASS`; cleanup and every required gate confirmed | `succeeded`, exit code `0` | `PASS` | Allowed only after the trusted coordinator has derived PASS. |
| `EXIT_ZERO` | `INCOMPLETE` because cleanup, policy, termination, artifact, tenant, or contradiction evidence is missing/uncertain | **No safe one-field mapping** | Must remain `INCOMPLETE` | Mapping to `succeeded` + `0` would incorrectly render PASS; mapping to `infrastructure_failed` would misstate the observed execution. The envelope must preserve both raw outcome and disposition. |
| `EXIT_NONZERO` | `FAILED`, with trusted child exit evidence | `program_failed`; include the observed nonzero code if available | `FAIL` | Correct only when the nonzero exit is truly the program outcome, not stale evidence from a timeout/cancelled attempt. |
| `TIMED_OUT` | `TIMED_OUT` only when the contract's termination condition is confirmed; otherwise `INCOMPLETE` | `timed_out`; exit code optional and observation-only | `INCOMPLETE` | A nonzero/zero-looking code must not override timeout uncertainty. |
| `CANCELLED` | `CANCELLED` only when termination is confirmed; otherwise `INCOMPLETE` | `cancelled`; exit code optional | `INCOMPLETE` | A cancellation request alone is not proof of termination. |
| `NOT_STARTED` | `REJECTED` | `rejected`, no fabricated exit code | `INCOMPLETE` | Preserve rejection as the execution state; do not imply program execution. |
| `LIMIT_EXCEEDED` | `LIMIT_EXCEEDED` | No exact PR #2 known status | Normally non-PASS; preserve the specific limit outcome | PR #2 currently normalizes unrecognized statuses to `unknown`, which loses the specific outcome. Extend a trusted envelope deliberately rather than mapping a limit event to `program_failed`. |
| `UNKNOWN` | `PROVIDER_ERROR` / uncertain infrastructure result | `infrastructure_failed` only when that label is supported by authoritative evidence; otherwise `unknown` | `INCOMPLETE` | Never fabricate an exit code or infer that the program failed. |
| Any outcome | Contradictory terminal evidence | No clean legacy status mapping | `INCOMPLETE` | Keep the contradiction visible; do not present the nominal winner as an unqualified terminal success. |

**Design consequence:** extending the legacy status allowlist alone is insufficient. The eventual trusted result envelope must preserve execution outcome, cleanup state, derived disposition, evidence/provenance, and optional exit code as distinct facts; the report projection then renders them without inventing equivalence. Exact field names remain open until the API/schema is deliberately selected.

**Required contract/test:** specify one translation table before wiring. Preserve the raw execution outcome and the derived disposition separately. Only a disposition that has passed the required trusted gates may project to report verdict `PASS`; `EXIT_ZERO` by itself is not sufficient. Timeout/cancel/unknown/contradictory evidence must not be translated into a clean success or program failure merely because an exit-code-like value exists.

### G2 — The report formatter documents, but does not enforce, the trusted-input boundary (HIGH)

PR #2 explicitly says the formatter does not verify input trustworthiness and production callers must provide authoritative runner evidence. Its helper is intentionally a formatter/classifier, not an execution engine, adapter, or API. That separation is valid, but the caller-side guarantee is not yet implemented/tested because no real runner exists.

**Required contract/test:** define which component is allowed to construct the trusted result envelope. Test that client/script-controlled fields cannot set terminal status, exit code, disposition, or artifact authority. Simulated results must remain visibly simulated and never yield PASS. Do not add a boolean like `trusted=true` as a substitute for a real trust boundary; the trusted producer/validation path must establish authority.

Relevant anchors: LOOP-03, LOOP-11, CASE-09, CASE-10, CASE-12.

### G3 — “Unavailable” and “empty” output are distinguishable, but partial collection failure is not structured (MEDIUM)

The report helper distinguishes `None` (rendered as unavailable) from an empty string (rendered as empty), and reports truncation flags. It does not define a per-stream collection state such as complete / unavailable / partial / collector-failed, nor a reason for missing output. A captured prefix followed by collector failure can therefore be confused with complete output unless the caller encodes the distinction in free-text notes.

**Required contract/test:** only if the selected runner/adapter can fail while collecting output, define structured collection metadata independently of stream content and output-limit truncation. Include a case where a prefix is known but the remainder is unknown; preserve the prefix and disclose the collection failure without claiming the stream is complete. Keep “truncated because policy cap was reached” distinct from “collector failed.”

Relevant anchors: LOOP-07, CASE-03, CASE-07, CASE-12, STREAM-01.

### G4 — Existing idempotency tests do not test the ambiguous-acknowledgement scenario in CASE-13 (HIGH for a remote run API)

The PR #3 helper reserves a `(tenant_id, key)` against a fingerprint and returns the original job ID for an in-memory replay. The tests cover same-key replay, changed-fingerprint conflict, and tenant scope. These are useful pure-function cases, but they do not simulate a request being dispatched, the response being lost, a reconnect/retry, an authoritative state lookup, or a second dispatch being prevented. The helper's in-memory dictionary is not durable or atomic storage.

**Required contract/test:** with a fake adapter and durable-store interface at the boundary, simulate (1) reservation, (2) dispatch, (3) response loss, and (4) retry with the same tenant/key/fingerprint. Assert the same run reference is returned and dispatch count remains exactly one. If the original state cannot be resolved, preserve UNKNOWN/INCOMPLETE and do not blindly dispatch again. Same key with a changed fingerprint must conflict before another dispatch; same textual key across tenants must not disclose or collide.

Relevant anchors: canonical Idempotency and retries section, CASE-13, IDEM-01/02, IDEM-SEM-01..04. The exact HTTP `Idempotency-Key` header is not selected here.

### G5 — Reconnect recovery (CASE-11) is a contract target, not an implemented path (HIGH for remote execution)

The lifecycle reducer can deterministically process supplied synthetic events and mark contradictory terminal evidence. It is not a status endpoint, durable event store, or reconnect/backfill mechanism. The current traceability matrix correctly classifies CASE-11 as remote-only.

**Required contract/test:** reconnect must query authoritative state for the same run ID (or recover a documented event cursor); it must not create a fresh run or infer completion from connection loss. Test queued/running/terminal/unknown responses and stale/missing event history. A local iPhone comparator can test UI resilience, but cannot pass the hosted recovery criterion.

Relevant anchors: CASE-11, CASE-13, LOOP-02/09.

### G6 — Artifact gates are modeled, but actual artifact publication and run association are absent (HIGH before any hosted download)

PR #3's `artifact_release_allowed()` checks cleanup state, digest validity, job association, and tenant authorization. This is a useful fail-closed predicate. It does not itself write/read stored bytes, verify a digest against final stored content, atomically publish a manifest, authenticate a download, or prove an artifact belongs to the displayed run. PR #2 can render supplied file names and sizes but does not establish those facts.

**Required contract/test:** keep the pure gate test and add store/adapter acceptance only when a concrete store boundary exists. Test interrupted writes and digest mismatch, no manifest publication before validation, cross-job/cross-tenant access denial, generated opaque storage IDs rather than filename-derived paths, and correct run/artifact binding when two runs finish out of order. Until then, artifact release remains unverified and no real download/security claim is permitted.

Relevant anchors: LOOP-10/11/12, CASE-14/16, ART-SEM-01..03.

### G7 — Policy confirmation is a boolean in the pure lifecycle helper; revision and chronology must be enforced at the execution barrier (HIGH before hosted untrusted code)

The offline matrix includes `NET-BARRIER-01` and `NET-SEM-01`, which require the exact required policy revision to be confirmed as applied before task start and revalidated if it changes between prepare and execute. `derive_disposition()` receives only `policy_confirmed: bool`; that is suitable for a pure decision rule but cannot itself prove the policy revision, source, freshness, or ordering relative to dispatch.

**Required contract/test:** the orchestration boundary must validate the expected policy revision and authoritative applied state immediately before dispatch. A pending, missing, failed, stale, or mismatched policy must produce zero task-start calls. Assert event order in the fake adapter; a caller-supplied boolean or ETag by itself is not evidence that enforcement took effect. Provider-specific runtime enforcement remains blocked until the provider and approved test boundary exist.

Relevant anchors: LOOP-12, CASE-15, NET-BARRIER-01, NET-SEM-01.

### G8 — Wrapper/coordinator failure versus child-program exit remains conditional on the selected execution boundary (MEDIUM)

The report contract has one `execution_status` and one optional `exit_code`. PR #3's execution outcome/disposition separation is better, but it does not create separate wrapper and child-process exit fields. Whether those fields are needed depends on the eventual architecture: a direct interpreter integration may not have a separate wrapper process; a process supervisor/provider adapter may.

**Required decision/test:** do not add schema fields speculatively. At boundary selection, answer whether wrapper and child can fail independently. If yes, test child exit nonzero + wrapper exit zero, wrapper failure after child exit zero, and missing child exit. Preserve both observations and never let a wrapper success imply program success. If no independent wrapper exists, document that fact and avoid redundant fields.

Relevant anchors: LOOP-04, LOOP-07, CASE-02/03/06.

## Integration conformance test inventory (specification only; NOT RUN)

These rows are additions to the existing 14-LOOP/16-CASE crosswalk. They do not replace or narrow canonical acceptance.

| ID | Acceptance anchor | Fixture / action | Minimum assertion | Boundary | Status |
|---|---|---|---|---|---|
| INT-01 | LOOP-03; CASE-04/05/06/10 | Map every PR #3 execution outcome + disposition into the PR #2 report envelope | No raw exit-zero alone can produce PASS; timeout/cancel/unknown/contradiction stays non-PASS; observed execution facts remain distinct from disposition | Pure mapping seam | NOT IMPLEMENTED / NOT RUN |
| INT-02 | LOOP-03/11; CASE-09/10/12 | Attempt to inject forged status/exit/disposition/artifact metadata from user-controlled task output | Only trusted runner/control-plane evidence sets lifecycle fields; script text remains diagnostic data | Trust boundary | NOT IMPLEMENTED / NOT RUN |
| INT-03 | LOOP-07; CASE-03/07/12 | Empty stream; unavailable stream; prefix then collector failure; source truncation; formatter cap truncation | Each state is distinguishable and truthful; no prefix is described as complete after collector failure | Adapter/report schema if applicable | NOT IMPLEMENTED / NOT RUN |
| INT-04 | CASE-13; IDEM-01/02 | Dispatch accepted, response dropped, same-key retry, status unavailable | Same job reference; one dispatch; unresolved state is UNKNOWN/INCOMPLETE and no blind redispatch; changed payload conflicts | Remote coordinator/storage seam | NOT IMPLEMENTED / NOT RUN |
| INT-05 | CASE-11/13; LOOP-09 | Disconnect during active execution, reconnect with original run ID | Status comes from authoritative lookup/replay; reconnect does not create a second run | Remote coordinator/API | NOT IMPLEMENTED / NOT RUN |
| INT-06 | LOOP-10/12; CASE-14/16; ART-SEM-01..03 | Partial artifact write, bad digest, wrong tenant/job, two runs completing out of order | Invalid artifacts remain unpublished/quarantined; authorized artifacts remain bound to the right job; filenames never become storage paths | Artifact-store seam | NOT IMPLEMENTED / NOT RUN |
| INT-07 | LOOP-12; CASE-15; NET-BARRIER-01/NET-SEM-01 | Policy missing/pending/wrong/stale/revised between prepare and dispatch | Zero task-start calls unless the exact required policy is authoritatively confirmed immediately before start | Coordinator/adapter seam; runtime tests later | NOT IMPLEMENTED / NOT RUN |
| INT-08 | LOOP-04; CASE-02/03/06 | Wrapper exits zero but child fails; wrapper fails after child success; child exit unknown | Preserve independent observations if the chosen boundary has both; never infer child success from wrapper success | Conditional on boundary selection | DECISION NEEDED AT BOUNDARY |
| INT-09 | LOOP-06/07/08; CASE-09/12 | Bounded report with checks, missing metadata, malformed values, empty/unavailable/truncated streams | Complete report fits defined bound, check provenance is explicit, unknowns and truncation survive copy/paste | Report helper + eventual UI | PARTLY SOURCE-COVERED; NOT RUN HERE |
| INT-10 | LOOP-13/14 | Review copy, labels, onboarding, pricing/provider claims and planned actions | No unsupported background/AI-capture claims; no provider account, billing, paid job, or live security workload without explicit approval and verified $0 conditions | Governance/UI review | DOCUMENTED; RECHECK BEFORE RELEASE |

## External protocol research relevant to G4

As of 2026-10-29, the IETF HTTPAPI working group has an active **Internet-Draft**, `draft-ietf-httpapi-idempotency-key-header-08`, updated 2026-10-22 and expiring 2027-04-25; it is **not a finalized RFC**. It describes an `Idempotency-Key` field, says a key must not be reused for a different payload, calls for a documented expiry policy where applicable, recommends that a completed duplicate produce a response consistent with the original operation, and discusses a 409 response for a concurrent duplicate. See the [IETF datatracker record](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) and [draft text](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header).

[RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods) explains that HTTP method idempotence concerns the intended effect, and cautions against automatically retrying non-idempotent requests unless their semantics are known to be idempotent or the client can detect that the original request was not applied.

**Application to PocketCode:** these protocol sources reinforce—not replace—the project’s stronger run-level requirements. An HTTP header cannot by itself guarantee durable single-dispatch semantics, recover a lost acknowledgement, create an atomic key reservation, or prove provider state. Keep the project key tenant-scoped and fingerprinted; define expiry; separate retry from explicit rerun; and require an authoritative existing-run lookup or conservatively preserve unknown state. Do not declare conformance to an Internet-Draft or adopt its exact wire format before API/schema selection.

## Follow-on specification created

The next provider-neutral step has now been written as [`ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`](ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md). It proposes the typed semantic envelope, conservative disposition table, fake-adapter operations, and 16 synthetic conformance cases. This is a specification only: it is not implemented or run, and it does not freeze the public schema.

## Next work order

1. **Review the proposed semantic mapping:** specifically settle how a trusted nonzero program exit is presented when cleanup evidence is also uncertain. Preserve both facts; do not collapse them into a misleading single status.
2. **If implementation is later authorized:** implement a small pure envelope validator/mapping and fake-adapter tests first, with dispatch call counts and event order asserted. Prioritize false-PASS prevention, lost-acknowledgement recovery, and policy revision barrier.
3. **At boundary selection:** decide if wrapper and child exit observations are separate; define structured output-collection state only if the selected collector can partially fail.
4. **Later, explicitly gated:** execute the full first-useful-proof workflow and hosted-security cases only when a real test environment is available and all strict $0/authorization constraints can be met.


### Stop conditions

- No provider selected, account created, billing enabled, workload run, deployment, merge, or production implementation is authorized by this audit.
- Do not claim PR #3 tests passed: the exact checked-in helper/test pair and full suite are explicitly NOT RUN in its current project status.
- Do not treat the PR #2 reconstructed-tree test result as evidence of app interaction, execution, backend behavior, or security.
- Do not treat a documented test, source-covered assertion, synthetic fake, or checkbox as observed runtime evidence.
- Keep all 14 LOOP criteria and all 16 CASE scenarios in force. The CSV proof remains a workflow smoke test, not the first-useful-proof milestone.
