# PocketCode — complete continuation handoff
**Prepared:** 2026-10-29  
**Purpose:** Transfer project state, decisions, evidence, AI roles, constraints, and the exact next work to a fresh ChatGPT conversation.  
**Status:** Continuity/research handoff only. This document does not authorize implementation, provider selection, workloads, spending, merging, deployment, or changes to canonical acceptance contracts.

## 1. Read this first: operating context and rules

The user is working from an iPhone and has no access to their PC/local development environment for approximately four months beginning October 2026. Treat all local files, installed binaries, runtime state, queues, and PC-only test results as UNKNOWN unless backed by explicit current evidence. The user uses ChatGPT Free, so conversations can hit length/usage limits and file intake is constrained. Optimize for substantive work per pass, concise questions only at the end, and durable GitHub continuity rather than relying on chat memory.

**Standing constraints**
- Keep using regular chat; do not route the user into ChatGPT Work mode.
- Work efficiently: do useful multi-step work in each pass, think ahead, avoid repeatedly rediscovering facts, and leave a precise checkpoint.
- Evidence over assumption. Distinguish **implemented**, **specified/proposed**, **statically inspected**, **test executed**, and **runtime/hosted verified**.
- Do not claim tests passed unless the exact identified source/test pair was actually run. No tests have been run in the current research-only pass.
- No paid services, account creation, provider selection, provider workloads, billing changes, GitHub Actions, merge, deployment, secrets, installation, elevated permissions, host integration, or execution-queue mutation without explicit authorization.
- Do not edit PR #2 or PR #3, or canonical product execution contract/acceptance documents, without explicit approval.
- Research-only documentation updates on the current research branch are authorized for continuity.
- Never conflate Gemini/Claude proposals with integrated implementation.
- Do not rename/reinterpret canonical acceptance IDs. Preserve the meanings of LOOP-01..14 and CASE-01..16.
- Do not treat mock/fake adapter results as evidence of hosted isolation, egress denial, enforced resource limits, process termination, provider-side policy synchronization, or durable recovery.
- Avoid duplicate or obsolete missions. Before starting a task, check whether a prior research artifact already answers it.
- Ask the user for a missing artifact/action only when truly necessary, and state the exact request briefly at the end.

## 2. Project and product direction

Repository: `marcelosofficial-ctrl/PocketCode-` (the trailing hyphen is part of the repository name).

PocketCode is intended to be a phone-first AI coding/workflow product for people who do not have a PC available. The product should help a user prepare code and input, run a bounded task through a controlled execution boundary, inspect trustworthy results/artifacts, copy a bounded report into an AI chat, and correct/re-run. Manual copy/paste is acceptable and should be treated as a valid fallback.

The direction has evolved from the original idea of running arbitrary scripts on the phone into a more realistic **Agentic Orchestration Control Plane**:
- Remote execution through an explicitly configured remote boundary (for example SSH/Tailscale) or an eventual cloud fallback may be considered later, but no provider or architecture has been selected.
- Local WASM/JSC may suit light tasks, but is not evidence that arbitrary Python execution, system-level access, or secure multi-tenant isolation is available.
- Do not assume a public arbitrary shell or unrestricted Python runtime.
- Reject system-wide overlays, silent cross-app control, background clipboard polling, private chat scraping, or quota-evasion mechanisms.
- Prefer an accessory symbol bar and explicit user-controlled paste-to-context over intrusive overlays or hidden clipboard access.
- User budget is $0. No paid provider, account, workload, or spend should be introduced without explicit approval.
- A potential naming collision with Catrobat's “Pocket Code” remains an unresolved product/branding concern.

### MVP execution boundary (proposed, not implemented)
- One bounded Python run per attempt.
- Mobile-facing API/UI.
- Server-pinned runtime.
- Fixed resource limits.
- No arbitrary public shell.
- No unrestricted package installation or network access.
- No persistent project workspace or multi-user collaboration in MVP.
- Provider not selected.
- No claims of production security until the actual boundary is selected and independently tested.

### Fixed smoke fixtures
Valid CSV:
```csv
id,quantity,unit_price
notebook,2,3.50
pen,3,1.25
```
Expected semantic result: `grand_total: "10.75"`, `line_items: 2`, `totals_by_item.notebook: "7.00"`, `totals_by_item.pen: "3.75"`.

Malformed CSV:
```csv
item,quantity
notebook,2
pen,3
```
Expected: clear failure because `unit_price` is missing; non-success if status is exposed; no valid summary.

For future actual execution tests, use a fresh workspace per case and verify the actual file creation/export—not only printed JSON. These fixtures do not prove a provider or secure runtime.

## 3. Three-AI collaboration model

Latest working division:
- **Claude:** lead developer / RelayRef; can perform deep implementation or research tasks when authorized. Ask for evidence-backed, self-contained deliverables and explicit limitations.
- **Gemini:** co-developer and independent spec/security auditor. Treat its findings as review input, not unquestionable truth. Reconcile IDs and source claims against repository evidence; recent review contained stale/invented IDs.
- **ChatGPT:** continuity holder, evidence reconciler, test architect, cross-branch conformance auditor, and eventual deployment coordinator (deployment only when explicitly authorized).

Earlier drafts varied on roles; use this latest division. The three AIs must not silently overwrite one another's decisions. Claude's specification is not integrated code; Gemini's audit is not proof of runtime behavior; ChatGPT's static inspection is not a test run.

When delegating to Claude or Gemini, give one bounded task with:
1. objective and non-goals;
2. exact source files/commit/branch to inspect;
3. required evidence and output format;
4. no-write/no-merge/no-provider constraints;
5. explicit handling of unknowns;
6. ask for one consolidated artifact when practical;
7. request a concise result plus exact file/line/function references and test status.

## 4. Repository branches and pull requests

### Current research branch
`pocketcode-ai-workflow-director-research-2026-10-28`

This branch contains research-only continuity and specification artifacts. It is safe to continue updating documentation here under the current authorization. Do not infer that the branch is merged or canonical.

### PR #2
Branch: `chat-continuity-report-regressions-2026-10-26`  
Draft/open/unmerged. Do not modify without approval.

- `scripts/report_contract.py`, blob SHA `e9d944a722c2fac5279952696528da72a7011af3`.
- `scripts/test_report_contract.py`.
- A prior result of 25 tests passed applied to an **offline reconstructed tree**, Python 3.13.5; it was not app/backend/provider/runtime validation.
- Static review: `classify_verdict` maps lifecycle `succeeded` plus an integer exit code to PASS/FAIL and uncertain lifecycle state to INCOMPLETE. It has no collector-quality, cleanup, policy, or artifact gate inputs. Its docstring describes a formatter and says production callers must supply authoritative evidence. Therefore the helper alone cannot enforce the full acceptance gate; caller-side trusted checks remain essential.

### PR #3
Branch: `pocketcode-pass0-audit-2026-10-26`  
Draft/open/unmerged. Do not modify without approval.

- `scripts/lifecycle_contract.py`, blob SHA `ba8d4d0b217c90513bed020e298029ef4e16f164`.
- `scripts/test_lifecycle_contract.py`.
- Test source contains 24 test methods, but the exact checked-in helper/test pair and full suite have **NOT RUN**.
- Static review found:
  1. `derive_disposition` maps `output_truncated=True` directly to `LIMIT_EXCEEDED`, without distinguishing runtime-enforced truncation from report/UI presentation truncation.
  2. It has no output-collection-state input, so it cannot enforce the new rule that required `UNAVAILABLE`/`PARTIAL_FAILURE` collection blocks PASS even with exit code zero.
  3. `artifact_release_allowed` checks cleanup, digest, job association, and tenant authorization booleans, but does not itself validate safe path/name, media type, size/count, current per-request authorization, or quarantine state.
- These are static conformance gaps, not proof that all surrounding callers fail. Keep the PR untouched until explicit authorization.

### Canonical main-branch product documents — unchanged
- `PRODUCT/EXECUTION_CONTRACT.md`, blob `3861e51ae4f9e45a263b677402f26c41b240959d`.
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- Canonical criteria remain LOOP-01..14 and CASE-01..16. Never replace them with invented aliases.
- The contract and acceptance criteria are the authority. Research supplements are additive only. Any change to canonical contract/acceptance requires explicit user approval.

## 5. Current research artifacts and exact links

All the following are on the research branch unless otherwise stated. They are design/research artifacts, not implementation or test evidence.

1. **Gemini review reconciliation**  
   `AI_COLLAB/GEMINI_REVIEW_RECONCILIATION_20261029.md`  
   https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/GEMINI_REVIEW_RECONCILIATION_20261029.md  
   Blob `353b9527fc3958977c8fcf6d988b9173bc8e1d87`.  
   Reconciles Gemini's ACCEPT WITH REQUIRED CHANGES verdict against current docs/source. It records valid, stale, and partially valid findings, and cross-branch helper gaps.

2. **Transition matrix / canonical acceptance coverage audit**  
   `AI_COLLAB/TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md`  
   https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md  
   Blob `ab7f92c16ed89fb1bbd29991d9e5bdc09f45d594`.  
   Audits TPM-01..16 against LOOP-01..14 and CASE-01..16. Identifies coverage gaps. All proposed cases NOT RUN.

3. **Provider-neutral adapter result envelope and fake protocol**  
   `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`  
   https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md  
   Current fetched blob at handoff: `ee2cc296fc34bc14b55e3e093ea1c95c72dfe2d2`. Earlier reconciliation mentions another revision `ffbf9dd600e9fad43990cdd39c68fab5c8adf392`; check current branch before citing a particular hash.
   Core rules: preserve raw execution facts separately from disposition; required output collection failure can block PASS without rewriting the exit fact; runtime output truncation differs from UI display truncation; policy barrier must close TOCTOU; no blind redispatch after ambiguous acknowledgement; artifact release must be revalidated at the actual download/export boundary.

4. **Semantic decisions and report projection**  
   `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md`  
   Blob `d7715e9095117c08ed4ad909d13a24ba1564fa1a`.  
   Decision notes on status projection and evidence semantics.

5. **Supplementary canonical acceptance tests**  
   `AI_COLLAB/CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md`  
   https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md  
   Blob `08265fcf91339dbdb08f518e3988fd661301bd56`.  
   Fourteen proposed tests, all NOT RUN: SUP-UX-01..02; SUP-REPORT-01..03; SUP-RUN-01..04; SUP-FILE-01..02; SUP-SEC-01; SUP-REC-01; SUP-GOV-01. The count was corrected in commit `94f165d39ecb41c5143baff0bc50560336994c6c`. Do not repeat Gemini's stale claim that the current file says 12. Do not rename these as SUPP-01..14.

6. **Gemini independent review packet**  
   `AI_COLLAB/GEMINI_INDEPENDENT_REVIEW_PACKET_20261029.md`, blob `6ca6d2960dd1144a66e77be5ce7dcf06d16012c5`.

7. **Transition and report projection matrix**  
   `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`, blob `ab570d38958193238494a4bdac3e9d022e03e9e0`.  
   TPM-01..16; all NOT RUN.

8. **Staged acceptance gates**  
   `AI_COLLAB/STAGED_ACCEPTANCE_GATES_20261029.md`, blob `6898d2af55b70ba950c64b1e350250670fe6c170`.  
   Gate 0 boundary selection; Gate 1 smoke; Gate 2 execution loop; Gate 3 hosted safety/service acceptance. CSV cases are smoke fixtures only. No provider selected, tests/workloads not run.

9. **Current handoff history**
   - Previous PocketCode handoff context in chat: latest branch was `pocketcode-ai-workflow-director-research-2026-10-28`.
   - PR #2 and #3 remain separate, draft, and untouched.
   - The latest reconciliation commit mentioned is `1f205b10a6c10272531a2369e72fb3bee0e3340f`.
   - Prior research commits:
     - Policy-race clarification: `ca360f36ae78eb816b5d92c674254c1f4c55e7cd`.
     - Supplement count correction: `94f165d39ecb41c5143baff0bc50560336994c6c`.
     - Collector-integrity/truncation clarification: `717a5061fb7ee170b7ef33cbe41b08f5c7218ac3`.
     - Release-time artifact checklist + proposed FAKE-17: `34e6aee275f50d4ad162e0d819ce6e0a8f488cf4`.
     - Reconciliation document: `1f205b10a6c10272531a2369e72fb3bee0e3340f`.
   These hashes are historical evidence; verify branch/file state before acting.

## 6. Gemini review: what was right and wrong

Gemini returned `ACCEPT WITH REQUIRED CHANGES`. Its actionable findings:
- Degraded required output collection must block PASS even when trusted exit code is zero.
- A policy sync/read alone is insufficient if a time-of-check/time-of-use race remains.
- Artifact authorization/safety must be checked at the actual release boundary, not inherited from historical PASS.

Already addressed in research docs:
- Adapter envelope says required `UNAVAILABLE`/`PARTIAL_FAILURE` collection blocks PASS (or required policy truncation without accepted partial-output semantics), while preserving raw exit facts and keeping collection state separate from cleanup.
- Policy barrier requires immutable per-attempt policy revision binding or atomic/conditional dispatch rejection if revision changed. Otherwise the boundary is unacceptable for untrusted code.
- Artifact release must revalidate current authorization, safe normalized path/name, media type, size/count, stored-byte integrity, and job/attempt/tenant association at download/export; deny/quarantine if required checks fail. Proposed FAKE-17 covers historical PASS but failed release-time validation.
- Secret scanning/redaction is an open policy choice, not a selected or verified mechanism.

Gemini review reliability issues:
- It introduced invented criteria IDs (ACC-MOB-01, ACC-SEC-02, ACC-OUT-03, ACC-REL-01, ACC-COST-01). These are not canonical.
- It used `SUPP-01..14`, but actual supplement IDs are `SUP-...`.
- It claimed a 12-vs-14 count discrepancy although the current research branch had already been corrected to 14 before the response.
- It acknowledged direct HTTP access to the review packet was unavailable; provider-specific claims were not all independently verified.
- Its suggestion to mark collector failure as `CLEANUP_FAILED` is rejected: collection and cleanup are separate dimensions.
Always reconcile reviewer claims against exact files, current branch revisions, and canonical IDs.

## 7. Core semantic requirements to preserve

1. **Outcome and disposition are separate axes.** A child process exit zero does not itself mean the task is PASS.
2. **PASS requires all mandatory trusted gates.** At minimum: trusted terminal evidence, exit zero, required output collection complete under the acceptance case, policy barrier confirmed, cleanup/termination requirements met, artifact integrity/association as applicable, current authorization, no contradictory evidence, no disqualifying limit event.
3. **Raw facts are immutable.** Preserve the observed exit code even when collection fails. Add evidence/report versions rather than silently rewriting prior reports.
4. **Unknown is a first-class state.** Lost acknowledgements, uncertain termination, failed authoritative lookup, stale/missing/contradictory terminal evidence must remain UNKNOWN/INCOMPLETE; never guess.
5. **No blind retries.** After ambiguous dispatch acknowledgement, look up the same attempt. If authoritative lookup cannot resolve it, remain UNKNOWN and do not automatically dispatch again. Durable idempotency reservation alone does not guarantee exactly-once execution.
6. **Policy race is a security boundary.** A read-then-dispatch check is not sufficient unless policy is immutable for that attempt or dispatch atomically rejects policy revision changes.
7. **Collection quality is independent from cleanup.** Empty COMPLETE output differs from UNAVAILABLE, PARTIAL_FAILURE, and policy truncation.
8. **Runtime truncation differs from display truncation.** A UI shortening a report must not be interpreted as the runtime having enforced a resource cap.
9. **Artifact release is a separate, current decision.** Historical PASS cannot authorize download if current auth, safe path/name, media type, size/count, stored-byte integrity, job/attempt/tenant binding, quarantine state, or required cleanup/integrity evidence fails.
10. **User output is untrusted.** Printed “PASS”, generated JSON, filenames, task content, and client-supplied trust booleans cannot set authoritative lifecycle/policy/ownership facts.
11. **Report formatter is not trusted coordinator.** PR #2's helper only formats/classifies supplied evidence; its callers must enforce trust and gates.
12. **Local tests cannot prove hosted security.** Isolation, egress, resource enforcement, process termination, policy application, multi-tenant separation, and durable recovery require the actual selected boundary and specific evidence.

## 8. Canonical acceptance coverage gaps already identified

The existing coverage audit says TPM-01..16 are not enough to close these:
- LOOP-01 phone-first workflow: no mobile UX/selected-input test.
- LOOP-02 UI simulation honesty: semantic projection does not test UI labels/state.
- LOOP-03 PASS evidence: missing/stale gate and real trusted-source checks.
- LOOP-04 wrapper vs child outcome: conditional on architecture having independent wrapper.
- LOOP-05 timeout/cancel/rejection/unknown: cancellation, rejection, infrastructure-unknown cases missing.
- LOOP-06 structured checks: no PASS/FAIL/SKIP/WARN fidelity/source labels.
- LOOP-07 diagnostics/file metadata: need required fields/bounds/metadata/collector failure.
- LOOP-08 actual copy action and selectable-text fallback: missing.
- LOOP-09 correction/rerun UX and report identity: projection/versioning is not full UX.
- LOOP-10 safe bounded file listing/download: release booleans are not path/name/size/list/download validation.
- LOOP-11 privacy: copied report must exclude secrets, unrelated files, and unbounded content.
- LOOP-12 actual isolation, externally enforced limits, egress denial: unproven.
- LOOP-13 audit of unsupported background/cross-app automation claims: missing.
- LOOP-14 zero-cost/governance gate: missing.
- CASE-02 syntax-error fixture and diagnostic.
- CASE-03 runtime exception after partial output.
- CASE-04 enforced deadline and confirmed termination.
- CASE-05 cancellation while active, including terminal and unknown cases.
- CASE-06 provider/worker failure before program result.
- CASE-07 externally enforced output cap and bounded actual output; display truncation separate.
- CASE-08 missing input / unsafe path rejection.
- CASE-09 named failed structured check despite exit zero.
- CASE-11 reconnect/backfill and same-run state lookup, not just event replay.
- CASE-13 idempotent dispatch after ambiguous network acknowledgement.
- CASE-14 path traversal and oversized file enforcement.
- CASE-15 egress and secret-read attempt enforcement.
- CASE-16 out-of-order completion with attempt/report/artifact binding.
TPM-07/08 only partially cover CASE-11/13; TPM-14 only partially covers CASE-16; TPM-16 does not prove file security/isolation/egress; report cases do not prove actual clipboard; TPM-03/04 are not syntax/partial-output fixtures; TPM-15 is not full structured-check/privacy coverage.

## 9. Current task state and what the last assistant was doing

The previous assistant had just started a further pass after the reconciliation. It re-fetched three research files through GitHub:
- Reconciliation blob `353b9527fc3958977c8fcf6d988b9173bc8e1d87`.
- Coverage audit blob `ab7f92c16ed89fb1bbd29991d9e5bdc09f45d594`.
- Adapter envelope at that moment blob `ee2cc296fc34bc14b55e3e093ea1c95c72dfe2d2`.

It attempted GitHub file search for an “Offline Evaluation Kit” and “AI workflow director task packet”; search returned no results. No repository write or implementation occurred in that attempt. The best next work is to avoid creating more generic docs and instead deliver a focused, actionable implementation-conformance backlog against the existing PR #2/#3 helpers and canonical IDs, or delegate a bounded deeper audit to Claude while independently continuing the highest-value static work. Do not assume an offline evaluation kit exists until verified.

## 10. Recommended next work — priority order

**Priority 1 — Make a precise conformance backlog (research-only; no code edits).**
- Re-fetch the exact PR #2/#3 helper and test files from their named branches.
- Identify exact function/branch conditions, current behavior, required behavior, missing test case, canonical LOOP/CASE IDs, and severity.
- Prioritize:
  A. Required stream collection state blocks PASS; preserve child exit fact.
  B. Runtime-enforced truncation versus UI/report display truncation.
  C. Release-time checks: path/name, media type, size/count, current auth, stored-byte integrity, attempt/job/tenant association, quarantine.
  D. Policy revision race closure.
  E. Ambiguous acknowledgement and no blind redispatch.
- Separate what belongs in the pure helper from trusted coordinator/adapter/release-boundary responsibilities. Do not bloat a pure helper with evidence it cannot authoritatively obtain.
- No test execution claim unless the exact source pair is run. The user has no PC; if the connected GitHub tools permit reading files only, label the work static inspection.

**Priority 2 — Consider a bounded Claude delegation.**
Ask Claude to independently review only the existing PR #2/#3 helper source plus the adapter envelope and canonical acceptance, produce one Markdown report with a function-level conformance matrix and proposed tests, and no edits. Require exact line/function references and explicit “NOT RUN” labels. Ask Gemini later to audit that report if worthwhile. Do not wait indefinitely; continue work while Claude is busy.

**Priority 3 — Preserve the product architecture choice as OPEN.**
Do not select a provider, deploy a hosted sandbox, or launch real workloads merely to satisfy a test matrix. First establish a provider-neutral boundary selection checklist and $0/authorization gate. Any hosted security acceptance stays BLOCKED until the owner approves a concrete architecture and cost/account impact.

**Priority 4 — Stop documentation sprawl.**
Use existing artifacts. Create another file only if it records new, specific, reusable evidence that prevents repeat work. If a new file is needed, write to the research branch and link it from the handoff/index; do not change PR #2/#3 or canonical documents.

## 11. Exact status statement for future chats

As of this handoff:
- Product direction and MVP boundary are proposals; provider not selected.
- Canonical execution contract and acceptance docs are unchanged.
- Research branch includes semantic decision, adapter envelope, transition matrix, acceptance coverage audit, supplementary acceptance tests, staged gates, Gemini review packet/reconciliation.
- PR #2 and PR #3 are open draft/unmerged and must remain untouched absent explicit approval.
- Static inspection identified helper conformance gaps.
- All TPM and supplementary test cases remain NOT RUN.
- PR #3 exact checked-in helper/test suite not run; PR #2's old 25-pass report applies only to an offline reconstructed tree.
- No actual app/backend/provider/runtime/hosted workload/security behavior has been verified.
- No provider, paid service, account, workload, merge, deployment, or canonical acceptance change has been approved.

## 12. Copy/paste prompt for the new ChatGPT conversation

You are continuing the PocketCode project. First read the GitHub handoff and existing research artifacts below; do not ask me to repeat the context. Work efficiently from my phone and preserve continuity in GitHub.

**Primary handoff:**  
https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CHAT_HANDOFF_20261029_POCKETCODE.md

**Then read these in order:**
1. Reconciliation: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/GEMINI_REVIEW_RECONCILIATION_20261029.md
2. Coverage audit: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md
3. Adapter envelope: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md
4. Canonical acceptance on main, IDs must remain LOOP-01..14 and CASE-01..16: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` (blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`).
5. Canonical contract on main: `PRODUCT/EXECUTION_CONTRACT.md` (blob `3861e51ae4f9e45a263b677402f26c41b240959d`).
6. Supplement: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md

Continue with a **function-level, static conformance audit** of PR #2 (`chat-continuity-report-regressions-2026-10-26`) and PR #3 (`pocketcode-pass0-audit-2026-10-26`) without changing either PR. Build one concise but precise matrix containing: requirement, exact helper/function and existing branch behavior, missing condition/evidence, proposed regression test, canonical LOOP/CASE IDs, severity, and whether it belongs in a pure helper or trusted coordinator/release boundary.

Prioritize:
- required output collection `UNAVAILABLE`/`PARTIAL_FAILURE` must block PASS even if exit code is zero, while preserving the raw exit fact;
- distinguish runtime-enforced truncation from report/UI display truncation;
- release-time validation of path/name, media type, size/count, current authorization, stored-byte integrity, job/attempt/tenant binding, quarantine;
- policy revision TOCTOU barrier;
- ambiguous dispatch acknowledgement, authoritative same-attempt lookup, and no blind retry.

Do not create redundant generic documentation. If you find new durable evidence, update only the authorized research branch, preferably by adding a concise section to an existing research artifact. Do not change canonical contract/acceptance, PR #2/#3, merge/deploy, choose a provider, create accounts, spend money, or run hosted workloads. Do not claim tests passed unless the exact checked-in source/test pair was executed. If tool access only supports reading, call the work static inspection and leave runtime/security unverified.

Remember the product is phone-first and $0. Our direction is an Agentic Orchestration Control Plane, not a system-wide overlay, hidden clipboard poller, chat scraper, or quota-evasion tool. Manual copy/paste is a valid fallback. Claude is lead developer when implementation is authorized, Gemini is independent security/spec auditor, and ChatGPT is continuity/evidence/test architect. Keep proposals, static inspection, test execution, and runtime verification explicitly separate.

At the end, provide: (1) what you actually inspected or changed; (2) evidence and exact links/SHAs; (3) what remains NOT RUN/BLOCKED/UNKNOWN; and (4) the single highest-value next step. Ask me for input only if truly necessary, and make any request specific and brief.


---

## Continuation update — 2026-10-29: reducer audit extended (Claude unavailable)

This is an additive continuity note. It does not replace the earlier handoff, change canonical acceptance, or authorize implementation. Claude is currently unavailable due to timeout; proceed from pinned source evidence and reconcile Claude's independent review later.

### New commits and verified artifacts

1. **Function-level conformance audit extended**
   - File: [AI_COLLAB/FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md)
   - Latest commit: `01456e9666e8d358c9543d416dc867714954df2b`
   - Latest blob: `e78ac6b849593a8c9502f11130f3b08672786832`
   - Adds FLA-07 and FLA-08 to prior FLA-01..06:
     - **FLA-07:** duplicate-event equivalence compares only sequence/kind/payload. If job/attempt/tenant/policy/source identity fields are part of the event contract, changed identity can be silently ignored as a duplicate. Contract-dependent; do not claim a live cross-attempt vulnerability without a defined event schema.
     - **FLA-08:** sequence collisions set contradiction but do not consistently place colliding nonterminal events in the conflict diagnostics. Verdict can be conservative while diagnostics are incomplete.

2. **Coordinator/fake-adapter test plan extended**
   - File: [AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md)
   - Latest commit: `2f7663fbceedde49ac9d439050b25a7254c90692`
   - Latest blob: `78b45b75824f05fae6fe8318e388cb7a59cc0ffa`
   - Adds **COORD-11**, testing identity-changing duplicate events and duplicate-sequence diagnostics.

### Current evidence status

- The pinned source files were read statically from PR #2 and PR #3 branches; no test suite was run in this pass.
- FLA-07 is conditional on the final event schema and event-ID scope; resolve that contract before implementing the expected behavior.
- FLA-08 is a source-level diagnostic-completeness gap.
- Existing findings FLA-01..06 remain in the audit. FLA-04 (attempt binding), FLA-06 (shallow-copy payload mutability), FLA-07 (duplicate signature fields), and FLA-08 (sequence collision diagnostics) are distinct.
- The coordinator plan now contains COORD-01..11.
- PR #2, PR #3, and canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` remain unchanged.
- No provider/runtime selected; no workload, account, billing action, merge, or deployment.

### Next highest-value work

Continue static review of lifecycle helper invariants and regression coverage, then update this handoff with only novel, source-grounded findings. Before implementation, resolve the event schema (event ID scope, identity fields, payload canonicalization) and the output-collection PASS gate. When Claude returns, reconcile against these exact findings and pinned blobs rather than restarting the audit.


## 11. Continuation update — 2026-10-29 (idempotency validation pass)

Latest audit continuation commit: `51c88a8370f4d109450836cd562ed96daff71700`. Updated audit blob: `c0ab7d961880ef5c3f2dff595307cda70eb70261`.

New audit entry **FLA-09**: the pinned PR #3 `reserve_idempotency()` and `reserve_idempotency_batch()` use truthiness-only checks for tenant ID, key, fingerprint, and proposed job ID. They do not enforce runtime string types or reject whitespace-only values; unhashable tenant/key inputs may produce incidental dictionary `TypeError` instead of a deliberate validation error. This is a helper-level validation gap, not proof that a real API accepts malformed requests and not evidence of durable/concurrent idempotency.

Tombstone review: on the pinned PR #3 source, repeated `DeletionTombstones.add()` calls overwrite the stored fingerprint and expiry for the same tenant/key. The current test covers tenant scoping and the exact expiry boundary, but not duplicate-add behavior. This is recorded as a cross-branch regression check rather than a new FLA ID because an earlier separate lifecycle/fingerprint branch was reported to contain tombstone overwrite/retention work; that branch's current source was not verified in this pass. Reconcile exact source revisions before treating it as an unresolved cross-branch defect.

Output-budget cap-type gap corroborates FLA-03; do not duplicate it as a new finding.

**Source pins rechecked:** PR #3 lifecycle source `ba8d4d0b217c90513bed020e298029ef4e16f164`; test source `39db87d9f44f5e8474f33cff60136e529364199a`. Static inspection only; no tests run. PR #2, PR #3, and canonical acceptance remain untouched. No provider, workload, account, billing, merge, Actions, or deployment action was taken.

**Next:** verify the exact current source on `pocketcode-lifecycle-fingerprint-audit-2026-10-27` before resolving tombstone status; inspect canonical request fingerprint validation and policy serialization only for genuinely new gaps beyond FLA-02; then audit batch idempotency and report-history semantics for contract-level type/aliasing gaps. Keep findings conditional where no caller/coordinator is implemented. Claude results remain pending and should be reconciled later without blocking static research.


## 12. Cross-branch reconciliation — follow-up completed

Latest audit reconciliation commit: `1c7578e57091842be471f8bf2be50a6d685473f4`. Latest audit blob: `02962190dba372bf67f868f9dc94371d50798651`.

I verified the separate branch `pocketcode-lifecycle-fingerprint-audit-2026-10-27` rather than leaving the tombstone and idempotency findings unresolved by assumption:

- Updated source `scripts/lifecycle_contract.py`, blob `316345341603848c4a86a6a82e533daa796c7695`.
- Updated test source `scripts/test_lifecycle_contract.py`, blob `ef9a68de632be30c091afe57f0724fd030a513f9`.
- FLA-02 fingerprint blank-field validation has a source-level fix and test cases on that branch.
- FLA-09 idempotency validation has a source-level fix requiring nonblank strings and test cases for empty/whitespace/None/integer values on that branch.
- Tombstone retry behavior has a source-level fix: same key + changed fingerprint conflicts; same fingerprint preserves the maximum expiry so retries do not shorten retention. Test source covers these cases.
- None of those tests were run in this pass, and no fixes are assumed merged or integrated. The pinned PR #3 blob `ba8d4d0b217c90513bed020e298029ef4e16f164` still exhibits the older behavior described in the original audit.
- FLA-03 remains open in static review: the newer branch's `OutputBudget.__init__()` still appears to accept positive non-integer caps because it only checks `<= 0`.

Updated audit link: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md

**Next best step:** inspect the newer lifecycle/fingerprint branch's remaining validation and report-history contracts, especially strict output-cap typing and whether `ReportHistory.append()` rejects whitespace-only job/evidence identifiers. Keep findings source-specific; do not treat the branch as merged or its tests as passed. No PR #2/#3 or canonical acceptance changes; no workloads, billing, Actions, merge, or deployment.


## 13. Additional helper-boundary finding — ReportHistory identifiers

Added **FLA-10** to the function-level audit. On the separate lifecycle/fingerprint branch, `ReportHistory.append()` checks that `job_id` and `evidence_ref` are non-empty strings but permits whitespace-only values. The disposition and cleanup allowlists later reject whitespace-only values for those fields, but not for the job/evidence identifiers. This is a source-level helper validation gap, not evidence of a live API issue; the exact contract and upstream validation still matter.

Latest audit commit: `fc33a42933899547f0e7d97f5354641dfb56e83d`. Latest audit blob: `527634a119b184296318faa22ab0ab92cbab2122`.

Current focused audit status:
- FLA-01: malformed output-limit flags in pinned PR #3 helper.
- FLA-02: fingerprint blank-field gap on pinned PR #3; candidate fix/test exists on separate lifecycle/fingerprint branch, NOT RUN.
- FLA-03: output-cap strict integer validation still appears missing in both inspected lifecycle revisions; NOT RUN.
- FLA-04: coordinator must bind events to the expected job/attempt.
- FLA-05: report input processing may not be bounded before display truncation.
- FLA-06: shallow-copy event payload mutability.
- FLA-07: duplicate-event equivalence may omit identity-bearing fields; depends on final event schema.
- FLA-08: duplicate sequence contradiction lacks complete collision diagnostics.
- FLA-09: idempotency input-validation gap on pinned PR #3; candidate fix/test exists on separate branch, NOT RUN.
- FLA-10: ReportHistory accepts whitespace-only job/evidence identifiers on separate branch, NOT RUN.
- Tombstone repeated-add overwrite/retention issue on pinned PR #3 has a candidate source fix and tests on the separate lifecycle/fingerprint branch, NOT RUN.

No implementation changes were made. Research branch only received documentation updates. PR #2, PR #3, canonical acceptance, provider selection, runtime selection, and account/billing/workload state remain unchanged/unauthorized.


## 14. Policy fingerprint serialization pass — 2026-10-29

Added FLA-11 to the function-level audit. On the separate lifecycle/fingerprint branch, canonical_request_fingerprint serializes effective_policy with json.dumps(sort_keys=True, allow_nan=False) but does not recursively validate mapping key types. Python JSON serialization can convert some non-string keys to strings; for example, a mapping with integer key 1 and value x can serialize identically to a mapping with string key 1 and value x. If malformed policy objects are accepted and mean different things to the eventual consumer, the fingerprint may fail to distinguish them. This is conditional on the intended schema and upstream validation, not proof of a product-level collision.

Recommended regression: define the accepted policy value grammar, reject non-string keys recursively, reject unsupported/non-finite values deliberately, preserve deterministic fingerprints for valid reordered string-keyed mappings, and ensure the coordinator fingerprints the exact effective policy applied. Static inspection only; no tests run; not assumed merged or integrated.

Latest audit commit: 688a6b181e68cf36d9d37c6641d4c41bf0f8a55d. Latest audit blob: be719ad6aa3f87c0238bb40b2ae23318715651a7. Output-cap validation remains FLA-03; report-history whitespace identifiers remain FLA-10. Candidate fixes for FLA-02, FLA-09, and tombstone retries remain separate-branch source only and untested.

Next: inspect canonical input-name normalization and StreamingRedactor/OutputBudget together for byte-bound and configured-redaction guarantees. Do not claim broad secret protection: the redactor covers configured patterns only.


## 15. Output redaction boundary review — FLA-12

Added FLA-12 to the function-level audit after inspecting the newer lifecycle/fingerprint branch and its tests. `StreamingRedactor` has fixed maximum lengths in its configured patterns: 256 for Bearer and generic key/value values, and 128 for several provider-token forms. No overlength-candidate policy is defined. Long Bearer/provider-like tokens can fail to match if no word boundary occurs before the regex maximum; generic key/value patterns can redact the first 256 bytes while leaving the suffix visible. Existing redaction tests cover short representative tokens and chunk-boundary behavior, not overlength values.

This is a source-level redaction coverage gap, conditional on output sink and input format. It is not evidence of a live leak or comprehensive-secret-protection promise. Proposed tests cover maximum + 1, much longer candidates, chunk/carry boundaries, and a deliberate whole-value suppression/redaction policy. Do not claim regex redaction replaces runtime limits or secret isolation.

Audit latest commit before this pass: `53fa0103addc1f8a8c356c3876f7b9ec3d8a4e35`; audit blob before this pass: `3a416a67d58e2fffd60084fee4cb23603c6fa9b1`.

Source pins inspected: lifecycle source `316345341603848c4a86a6a82e533daa796c7695`; test source `ef9a68de632be30c091afe57f0724fd030a513f9`. No tests run. PR #2/#3 and canonical acceptance untouched.

Next: inspect input-name canonicalization and the exact byte-accounting invariants of `OutputBudget` (especially bytearray retention after redaction and aggregate accounting), then decide whether any further finding is genuinely distinct from FLA-03/FLA-12. Keep source-level observations separate from actual runtime security claims.


## 16. Input-name portability review — FLA-13

Static review of `_canonical_input_name()` found that it rejects common Windows device stems and ASCII `COM1`–`COM9` / `LPT1`–`LPT9`, but misses Windows superscript-digit aliases `COM¹`/`COM²`/`COM³` and `LPT¹`/`LPT²`/`LPT³`. Those aliases can pass the helper despite its stated cross-platform basename intent. Existing tests include `COM1.csv` but not superscript aliases. This is a narrow source-level portability gap, not evidence of path traversal or a live exploit; downstream behavior depends on target platform and file operations.

Regression proposal: reject the six superscript aliases with/without extensions and case variation; retain neighboring valid names. Latest audit commit is to be confirmed from the verification below; audit source pin remains lifecycle blob `316345341603848c4a86a6a82e533daa796c7695`. No tests run and no implementation/acceptance changes.


## 17. Output-budget accounting pass — no additional FLA assigned

Reviewed `OutputBudget.add()` and `finish()` in lifecycle source blob `316345341603848c4a86a6a82e533daa796c7695`, plus the existing output-budget tests in test blob `ef9a68de632be30c091afe57f0724fd030a513f9`. The helper increments observed-byte counters before retention, computes the allowed input prefix against per-stream and aggregate observed-byte caps, and after any overflow stops retaining further data and clears pending redactor tails. The configured redactor replacements preserve byte length, so in the no-overflow path retained bytes should remain bounded by the same caps; finish flushes pending tails in deterministic stdout-then-stderr order.

No separate accounting defect was established from this static pass. Strict positive-integer/non-boolean cap validation remains FLA-03. Pattern coverage for overlength credential-like values remains FLA-12. Existing tests exercise exact aggregate-cap allowance and post-overflow retention stability, but were not executed here; they do not prove runtime collection, cancellation, or external output enforcement. Next audit pass should focus on whether input-name portability and fingerprint schema constraints are enforced at the actual request/file-creation boundary, without assuming this helper is integrated.


## 18. Cross-branch boundary verification — 2026-10-29 follow-on

Latest audit update commit: `aeaf6f63f6e979b391058546ea824c277c63386a`; updated audit blob: `956816ee4f462a232096d28b0f5e5b079b9c11bb`.

The research branch's `scripts/` directory was checked directly and contains only `check_mobile_prototype.py`, `report_contract.py`, and their test modules. It does not contain the lifecycle helper or its tests. The lifecycle source reviewed for FLA-01..FLA-13 remains pinned to the separate `pocketcode-lifecycle-fingerprint-audit-2026-10-27` branch: source blob `316345341603848c4a86a6a82e533daa796c7695`; test blob `ef9a68de632be30c091afe57f0724fd030a513f9`. Treat those as branch-specific pure-helper observations, not integrated product behavior.

The new audit section 15 records these distinctions:
- Input-name canonicalization/fingerprint generation does not prove the eventual filesystem boundary uses the same names or rejects collisions before creation.
- The fingerprint helper serializes an `effective_policy` mapping but does not recursively enforce a strict JSON schema; FLA-11 already captures non-string-key serialization ambiguity. No verified coordinator/worker binding proves that the fingerprinted policy is the exact policy actually applied.
- The terminal-event reducer checks basic fields but does not establish full event authentication/schema or tenant/job/attempt/policy-revision binding. FLA-04/07 cover identity binding; FLA-06 covers nested-payload mutability. Avoid duplicate findings without new source evidence.

Next work: inspect the adapter/coordinator specification for who owns request normalization, policy revision/ETag barrier, event authentication, and job/attempt binding. Create a boundary-by-boundary evidence table labeled VERIFIED IN SOURCE / SPECIFIED ONLY / ABSENT / NOT RUN. Add new findings only if a distinct behavior is source-grounded after reconciliation.

No tests were run. No implementation code changed. PR #2/#3, canonical acceptance, provider selection, deployment, merge, account/billing, and workload state remain untouched/unauthorized.


## 19. Adapter-boundary evidence reconciliation — 2026-10-29

Latest audit commit: `7588ae47ba64e5038c0d6ccec0eaa32f69c6b835`; audit blob: `40bca9bfd0076b1d555d69afe690fa4292956c26`. The audit now has section 16, an explicit evidence-state table based on the adapter decision gate and result-envelope specification.

Key status distinctions:
- **VERIFIED IN SOURCE, separate helper branch only:** basic pure reducer checks and fingerprint/input-name helper behavior. This is not an integrated coordinator.
- **SPECIFIED ONLY:** request/file boundary normalization, policy revision barrier, authenticated event provenance and attempt binding, runtime output enforcement, and artifact validation/release.
- **NOT RUN:** test suites, fake-adapter cases, policy-race checks, coordinator/replay tests, artifact-release tests, and runtime/security trials.
- **ABSENT from the audited research branch:** `lifecycle_contract.py` and its test module. The source pins remain on `pocketcode-lifecycle-fingerprint-audit-2026-10-27`.

The adapter specification is explicit that read-then-dispatch is insufficient for the policy TOCTOU barrier: the real boundary must bind the attempt to an immutable policy revision or provide atomic/conditional rejection if the revision changes. It also proposes authenticated-producer provenance, event/attempt identity, append-only evidence, fail-closed artifact release, and release-time authorization/integrity checks. None of these requirements has been verified in a live or implemented boundary.

Do not add a new FLA solely for these missing integration proofs: current overlaps are captured by FLA-04/06/07/11, while the remaining items are design-vs-implementation evidence gaps. Next pass should map each control to a future owner/interface and write minimal falsification tests for false-PASS, policy TOCTOU, cross-attempt evidence, ambiguous retry/replay, and unsafe artifact release.

No tests or workloads run. No implementation changed. PR #2/#3 and canonical acceptance remain untouched; no provider, account, billing, merge, or deployment action taken.


## 20. Control ownership and falsification matrix added — 2026-10-29

Created `AI_COLLAB/CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md` on the research branch. Commit: `da9e6fe2b671bef83302353643fed103249703ff`.

The matrix maps 11 control areas to proposed owner boundaries, required invariants, minimal falsification tests, current plan/acceptance anchors, and evidence needed before claiming satisfaction. Areas: request/input validation; fingerprint-to-applied-policy binding; event authentication; job/attempt/tenant/policy binding; immutable event evidence and collision diagnostics; verdict projection; output collection/redaction; idempotency/ambiguous dispatch; durable report history; artifact release; runtime isolation/resource limits; phone-first workflow and $0 gate.

It also defines evidence labels (VERIFIED IN SOURCE, UNIT TESTED, FAKE-ADAPTER TESTED, INTEGRATION TESTED, DEVICE ACCEPTED, SPECIFIED ONLY, NOT RUN/UNKNOWN, BLOCKED), an implementation-authorized test order, and hard stop conditions. This is intended to prevent the common mistake of treating helper tests or a fake adapter as proof of provider enforcement, durable persistence, device behavior, or security isolation.

Verified after creation: [control ownership/falsification matrix](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md).

No tests run. No implementation code changed. No provider/runtime chosen. PR #2/#3 and canonical acceptance untouched; no account, billing, workload, merge, or deployment action.


## 21. Owner decision register — 2026-10-29

Created `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` (commit `37d1ba24fd8d9c9e9515b3f27eb792fecf23d12c`). It records eight unresolved decisions, proposed defaults, and tests needed before implementation.

Important consistency check: canonical acceptance defines FAIL as a confirmed program/runtime failure. The semantic and transition matrices lean toward INCOMPLETE for enforced limits unless an owner decides otherwise. A trusted limit event that terminates execution may be a confirmed runtime failure; review this against canonical wording before freezing tests. Proposed for review: confirmed limit-triggered termination -> FAIL verdict plus `LIMIT_EXCEEDED` disposition; collector-only truncation and display-only truncation remain distinct. Do not amend canonical acceptance silently.

Other open decisions: provider failure without child exit; output completeness as a PASS gate; event ID scope; policy revision barrier; ambiguous acknowledgement recovery; release-time artifact checks; durable report history. No tests or code changes; PR #2/#3 and canonical acceptance remain untouched.
