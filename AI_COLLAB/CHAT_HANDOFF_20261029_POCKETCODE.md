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
- The coordinator plan now contains COORD-01..12; COORD-12 covers immutable event snapshots.
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

Historical note (superseded by section 23): earlier semantic and transition matrix versions used an overly broad INCOMPLETE mapping for enforced limits. The current research note distinguishes limit-caused termination, collection-only truncation with independently confirmed EXIT_ZERO, and display-only truncation. D-01 remains owner-open: a confirmed limit-caused runtime failure is a candidate FAIL under canonical wording, with `LIMIT_EXCEEDED` disposition; do not amend canonical acceptance silently.

Other open decisions: provider failure without child exit; output completeness as a PASS gate; event ID scope; policy revision barrier; ambiguous acknowledgement recovery; release-time artifact checks; durable report history. No tests or code changes; PR #2/#3 and canonical acceptance remain untouched.


## 22. Cross-document semantic map added — 2026-10-29

Created `AI_COLLAB/SEMANTIC_DECISION_CROSSWALK_20261029.md` (commit `f5d3fbecc2ada66841fc7259bead8347ec52fa81`). This indexes the current state of PASS, nonzero exit/cleanup, provider failure, execution limits, output completeness, event identity, policy revision, ambiguous acknowledgement, artifact release, report history, and runtime/device evidence across the existing docs.

Priority: D-01 remains owner-open even though the test documents now distinguish the three limit cases. D-03 remains owner-open pending confirmation of case-specific required-output/accepted-partial-capture rules. No canonical acceptance or implementation change is authorized or implied.

## 23. Output-limit and collection-state reconciliation — 2026-10-29

This pass reconciled D-01/D-03 across the semantic decision note, transition matrix, adapter envelope, coordinator test plan, owner register, and crosswalk. The intent is to distinguish three cases rather than assign one verdict to every form of truncation:

1. **Limit-caused termination/failure:** trusted evidence says the runtime stopped/failed execution because a configured limit was exceeded. Candidate user verdict is FAIL if this is a confirmed program/runtime failure under canonical wording, with `LIMIT_EXCEEDED` retained as the richer disposition. The exact mapping remains owner-open under D-01; do not claim the owner approved it.
2. **Collection/retention cap only:** output capture is capped, but independent trusted process evidence says EXIT_ZERO. Verdict follows that terminal evidence and the specific acceptance case's output requirements. PASS is possible only when partial collection is accepted for that case and all other required gates pass; optional diagnostics must not become an accidental universal gate. Required incomplete evidence still blocks PASS where the case requires it.
3. **Report/UI-only truncation:** preserve the process verdict and record presentation truncation; do not infer runtime limit enforcement.

Updated research artifacts:
- `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` — commit `7753694106f0ee47792c53ffdbfaac60dec1a313`, blob `d204e459d02a123f6693ae1c1c42aac40edb3b3d`; COORD-01 now says output requiredness is case-scoped, and COORD-10 tests three distinct limit/truncation cases.
- `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md` — commit `c2bdbb79d6b0efc5baf3c6e6d7d06ade068e3d1e`, blob `a237e882128865ce6a47651a1f9c6da6901f4994`.
- `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md` — commit `12593e94b74acc64d272b079068bd10986625f87`, blob `c4166ad1447e5628c4f4aadd34c864c878d5f795`.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` — commit `41601e9945a27c289d38b7b59f2f300434ddb6cf`, blob `ba5c1e2fb408e648ddf2867131ddda30eb33e9e3`.
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` — commit `858c5dcd5102aff7e6f25edb37f174047414145d`, blob `aba80a8a2322a2e5fe267af30c13bad3a9b332bf`.
- `AI_COLLAB/SEMANTIC_DECISION_CROSSWALK_20261029.md` — commit `eb68a5d754ec79d7f597618691a2d78e4b988f1a`, blob `55f7be2a07f7a548173983aea3f6a9e2b9ccdb15`.

Next passes, in order:
1. Re-fetch the six documents and mechanically check that old broad wording about runtime limits/output completeness does not survive in another research doc.
2. Review CASE-07 and LOOP-07 traceability: canonical acceptance requires external cap enforcement and explicit truncation/rejection, but does not itself specify the verdict for every limit implementation. Keep verdict mapping conditional on observed terminal facts and D-01.
3. Then do one focused event-identity/replay reconciliation (D-04 / FLA-04/06/07/08) against the adapter envelope and COORD-05/11; avoid starting another broad audit.

No tests were run. No implementation changed. Canonical acceptance/contract and PR #2/#3 remain unchanged. No provider/runtime selection, workload, account, billing, merge, or deployment.
## 24. CASE-07 traceability and event identity/replay reconciliation — 2026-10-29

### CASE-07 / LOOP-07 audit sweep
A targeted phrase scan was run across the 45 Markdown files currently in `AI_COLLAB/`. The only older research table found that gave a blanket `LIMIT_EXCEEDED -> INCOMPLETE` mapping was `AI_COLLAB/EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md`; it now marks that mapping as a superseded conservative candidate and points to D-01. The old source-level PR #3 behavior (`output_truncated=True` -> `LIMIT_EXCEEDED`) remains documented as a verified-in-source conformance gap, not as the approved product rule.

CASE-07 and LOOP-07 traceability now explicitly separate limit-caused termination, collection-only cap with independently confirmed EXIT_ZERO, and report/UI-only truncation. The canonical criteria remain unchanged: CASE-07 requires enforcement and explicit truncation/rejection, but does not define one verdict for every implementation of an output cap. D-01 remains open. Output requirements must be case-specific under D-03, not silently universal.

Updated traceability files:
- `AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md` — commit `b16e13fbd675ee5b1161f2f8e0c556cf4ff07b07`, blob `d236962b3a58b98e96fad22ef5c2c23a7a61d54b`.
- `AI_COLLAB/CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md` — commit `9cca8d4c9201ae964de7b5b936490ed03208b31d`, blob `193eada4971b03661376130866cc4841acb1c2eb`.
- `AI_COLLAB/TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md` — commit `885e835214b9349352aeee01f9e2987e5d856e97`, blob `b03c5810599e4a893272dea01d0dd91fed58ea33`.
- `AI_COLLAB/EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md` — commit `d237bc9c84b892815e88dbd60b60daa1ec7455b5`, blob `3aebbb856c9fe6fc5a993c277ba9ace7f1816e00`.

### Event identity/replay proposal
Static re-fetch confirmed PR #3 source remains pinned at `scripts/lifecycle_contract.py` blob `ba8d4d0b217c90513bed020e298029ef4e16f164`. `reduce_terminal_events()` uses duplicate signature `(sequence, kind, payload)` and has no expected job/attempt argument; nested payloads are only shallow-copied. The helper cannot establish complete event authenticity, source namespace, tenant/job/attempt/policy binding, or immutable snapshots by itself.

Research-only proposed default, still owner-open under D-04:
- The trusted coordinator assigns a unique canonical event ID; source/provider event IDs are kept separately and deduplicated within an explicit authenticated source + tenant/job/attempt namespace.
- Bind the expected tenant/job/attempt/source (and relevant policy revision) before reduction.
- Coordinator sequence is unique within the event stream for one attempt; provider timestamps are retained observations, not ordering authority.
- Exact replay means all immutable event identity and observation fields match. Reuse of a scoped source ID with changed identity, sequence, kind, policy binding, payload/schema, or canonical payload is a conflict.
- Accepted payloads are immutable snapshots; sequence collision diagnostics identify every colliding event, including nonterminal events.

Test architecture update: `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` now defines COORD-11 for exact scoped replay, conflicting source-ID reuse, and sequence collisions; COORD-12 covers nested-payload mutation after acceptance. Its current blob is `04cc9dd41496e734d005fdb487bd6cedc8529bf4`. The adapter-envelope latest blob is `5a46ffba5a455a8dcd832dbd6c84c223c2a039bc`; owner register latest blob is `263f09366a4cbc60605201246fda672f50e68ebe`; semantic crosswalk latest blob is `c3679b612ef1c5b8c624f615832fd3634412392c`. No PR source was modified.

Next highest-value passes:
1. Verify the latest versions of the handoff, owner register, adapter envelope, coordinator test plan and crosswalk against the current branch head; fix any stale COORD count or decision status.
2. Inspect the policy-revision/dispatch boundary in the same way: turn D-05 into an explicit falsification checklist while keeping real provider enforcement BLOCKED/unverified.
3. Keep D-01 and D-03 explicitly owner-open; do not change canonical acceptance to avoid asking for a product decision.

No tests or implementations were run. Canonical `PRODUCT/EXECUTION_CONTRACT.md` / `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, PR #2 and PR #3 remain unchanged. No provider/runtime, account, billing, workload, merge or deployment action.
## 25. Policy revision / dispatch falsification checklist — 2026-10-29

Added PBR-01..07 to `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` (commit `8983a3e2f9bf6a4e54c3b0ddc3b25610909861f0`, blob `7327ec53c18a9bf074585865e380c3c526a85839`). The checklist covers: contract/primitive inspection; missing/stale/pending/unknown revisions; R1-to-R2 race; revision-token changes/ABA-style races where supported; missing or mismatched applied-revision evidence; concurrent dispatch/policy updates; and lost acknowledgement followed by same-attempt lookup.

Core gate: a request fingerprint or policy read is not proof that the same policy revision was applied at task start. The chosen boundary must bind an immutable policy to the attempt or enforce an atomic/conditional start. A fake can test coordinator decisions and expected dispatch counts but cannot prove a real provider closes the race. If the applied revision cannot be established, the barrier is BLOCKED/unverified; no PASS or safety claim is justified.

Also linked D-05 from `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` (commit `52e1255eb2f7d0bbc954b9c71873ecdbaa4aeb17`, blob `032390cc57eb29e1a0ed378daab5d26ccbe57de1`) and updated `AI_COLLAB/SEMANTIC_DECISION_CROSSWALK_20261029.md` (commit `b96085305bbc3892f6149c6f436ee06489c21830`, blob `5eccf7914b5a93b23c00de4d0f689359d9696608`).

Status remains SPECIFIED ONLY / NOT RUN: no provider/runtime has been selected, and no account, billing, workload or actual race test was authorized. D-05 remains a blocking architecture/security decision.

## Current next-pass ordering

1. Re-fetch and verify the latest handoff, owner register, adapter envelope, boundary gate, coordinator plan, crosswalk, and current branch head. Ensure the updated COORD-11/12 references and PBR-01..07 links resolve.
2. Close remaining documentation-only contradictions between the proposed policy fingerprint (`effective_policy`) and the policy revision actually bound to dispatch, using FLA-11 and the adapter envelope; preserve D-05 as BLOCKED until a real boundary is selected and verified.
3. Keep D-01, D-03, and D-04 explicitly owner-open; no canonical acceptance change, implementation change, or provider action is implied.
## 26. Fingerprint semantics versus actual policy application — 2026-10-29

This pass addressed FLA-11 and the D-05 integration gap. The pinned lifecycle helper `canonical_request_fingerprint()` serializes `effective_policy` into its hash document with `json.dumps(sort_keys=True, allow_nan=False)`, but source inspection does not establish strict recursive JSON-value/key validation at this helper boundary, and a request fingerprint cannot prove that an execution boundary applied the same policy to an attempt.

Key distinction:
- **Request fingerprint:** identifies canonical, validated request semantics for idempotency/conflict handling.
- **Applied-policy binding:** authoritative evidence that the exact required policy revision/configuration is bound to the specific attempt at start.
A correct hash does not prove that the policy was applied. A revision token alone does not prove a retry had identical request semantics. Both must be linked to the same authenticated tenant/job/attempt.

Added PF-01..PF-05 to `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` — commit `7a384ae6743d1ce6f9a4a98be7dbe85037c401a4`, blob `df51e68346f4ec7b36ded484e6f7a8d0c477ea3c`. Cases cover recursive policy JSON validation; deterministic fingerprinting for valid canonical values; changed policy/key conflict before second dispatch; policy revision changing after fingerprint and before start; and missing/mismatched applied-revision evidence blocking PASS/release.

Linked this clarification from:
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` — commit `49e95404018983779f479b41167749f7b975a727`, blob `e14f7d52d25fe232041c36c4d5f27893addda664`.
- `AI_COLLAB/SEMANTIC_DECISION_CROSSWALK_20261029.md` — commit `88d8bea9480d5b47fd5cc3d467a02531c2576421`, blob `a3a477512bf0fcbc938765a6956895662119f569`.
- `AI_COLLAB/CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md` — commit `d042c6e2f81d169afd92bbecb21ddbcb7d3014d7`, blob `d52cc82e39e9e3806da78d480f2505b449738f6e`.

All are research/spec updates only. No code changed, no tests ran, no provider/runtime was selected, and no policy race was executed against a real boundary. D-05 remains BLOCKED/NOT RUN pending provider-boundary proof; D-01, D-03, and D-04 remain owner-open.

## Immediate next pass

Perform a read-only branch/continuity verification: fetch the latest five decision/test artifacts plus this handoff, confirm their latest blobs and current branch HEAD, check that COORD-01..12 and PBR-01..07/PF-01..05 are referenced consistently, and recheck PR #2/#3 plus the canonical blobs. Do not do further broad rewrites unless a concrete conflict is found.
## 27. Final static verification and PF-01 precision correction — 2026-10-29

PF-01 was tightened to avoid listing ordinary Python lists as mapping keys (lists are unhashable in a normal `dict`). The test now targets non-string keys such as integer, boolean, and null keys, custom Mapping implementations, unsupported/non-finite values and invalid nested values. It explicitly includes `{1: "x"}` versus `{"1": "x"}` as a serialization-coercion regression: separately supplied policy mappings of those shapes can serialize to the same JSON key/value shape unless non-string keys are rejected recursively.

Latest `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` blob after this correction: `c1057fe74fd77bd6ae1783e0d024b6cad94bbd16`, commit `ce534e85c64b7108629c12eb43815a5fb87a197f`.

Static verification at the current branch head confirmed:
- Research branch name remains `pocketcode-ai-workflow-director-research-2026-10-28`.
- Latest head before this handoff append was `83aef486461113cde3f8a8cdcdfdacd1b09cf27b`; this final handoff update advances it.
- COORD-01..12 and PBR-01..07 / PF-01..05 were present in the intended research files.
- PR #2 remains open/draft/unmerged at `eb8b7ea83cb0e8fe1880351276c485b761431791`; PR #3 remains open/draft/unmerged at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- Canonical `PRODUCT/EXECUTION_CONTRACT.md` is still blob `3861e51ae4f9e45a263b677402f26c41b240959d`; `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` is still blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- The research tree currently has 45 `AI_COLLAB/*.md` files; the recursive tree fetch was not truncated.

Current truthful state: these are specification/source-audit documents only. No implementation changes, no tests executed, no policy-race integration test, no provider/runtime selection, no account/billing/workload, merge, or deployment. D-01/D-03/D-04 remain owner-open; D-05 remains blocked until the actual policy application/dispatch boundary can be selected and proven.
## 28. D-06 idempotency and ambiguous-dispatch recovery — 2026-10-29

### Work completed

Created `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md` — commit `42ae403928c2aa697bcd4c1927cfe67750bfd358`. It specifies proposed invariants, an illustrative recovery state model, a crash-point matrix, storage/provider questions, stop conditions and DR-01..DR-12 falsification cases. It is SPECIFIED ONLY / NOT RUN and does not freeze a schema.

Updated and linked it from:
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` — verified current blob `d7f48aeb433e2e23e17a4d7b8cfed70815bd8d3f`.
- `AI_COLLAB/CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md` — verified current blob `f86ff2d75959dfee9fa51a55eb1eaf5a4f955abe`.
- `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` — commit `0b21e1a765a814f0bad30673f992f232c46dc473`, blob `37c25137b972427771de0d53054b6cd57e211e57`.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` — commit `13701de8440012b841a3b21e7952b1f368af41f4`, blob `e9e856d220b3c934867bd147447d0d051c22e776`.

### D-06 proposed core contract

- Atomic durable tenant-scoped reservation; a versioned fingerprint binds the execution-affecting request semantics.
- Same tenant/key/fingerprint resolves to the original job/attempt; changed semantics conflict before dispatch.
- Persist dispatch intent before crossing the external start boundary.
- After a provider call may have been accepted, lost acknowledgement, timeout, process crash, or lease expiry cannot authorize blind redispatch.
- Reconcile the original identity via authoritative lookup or provider-enforced idempotent start. If lookup is UNKNOWN/unavailable and provider semantics cannot prove whether the operation started, remain UNKNOWN and require reconciliation; no exactly-once claim.
- Persistent uniqueness, crash recovery, retention and report history require store integration tests. Fake dispatch counters only prove coordinator branch behavior.

DR-01..DR-12 cover concurrent duplicate submissions, changed fingerprints, tenant isolation, crash windows before/after dispatch intent, accepted-but-unacknowledged start, UNKNOWN/definitive lookup, lease expiry, restart recovery, result identity mismatch and tombstone retention.

### Evidence and next work

No implementation was changed, no tests were run, and no provider/store was selected. No account, billing, workload, merge, deployment or canonical acceptance change occurred. PR #2/#3 remain untouched.

Next passes: (1) verify the new D-06 references and current branch head after this handoff update; (2) build D-07 artifact release-time validation checklist; (3) build D-08 durable report-history/append concurrency checklist. Keep owner decisions and real boundary guarantees explicitly open.
## 29. D-07 artifact release and D-08 report history — 2026-10-29

### D-07 artifact release

Created `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md` — commit `329eb1306676d82a0675d59f2717aa7508b62a72`. AR-01..AR-14 cover authorization revocation, cross-tenant/job/attempt access, byte mutation, TOCTOU/symlink paths, malformed manifests, quarantine/expiry, limits/type mismatch, active content, streaming mutation, ranges/retries, existence side channels, unsafe names, revocation races, and concurrent quarantine/replacement.

Updated links:
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` — current blob `fc33e1ceeb533af0825a5370ff4ebe15e3fe1e9f` at the point D-07 was linked; it was updated again for D-08 below, so re-fetch current blob before citing.
- `AI_COLLAB/CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md` — current blob `dcc8b663481b101086f50bb25c2f3cbf40da783f` at the point D-07 was linked; it was updated again for D-08 below, so re-fetch current blob before citing.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` — commit `852000546f820a7d8accdee9997210c2d26d2101`, blob `c4655541c5b86b2a573316ae086e11fd3e4e1ca8`.

Key rule: a historical execution PASS does not grant permanent download authorization. Revalidate current caller, exact tenant/job/attempt, trusted manifest, quarantine, immutable object version, exact bytes/digest/size, safe response policy, bounded delivery, and non-disclosure at the actual release boundary. No artifact store/API is selected or tested.

### D-08 durable report history

Created `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md` — commit `a228b598183e5bc4aa524c8a347446805061fdbe`. RH-01..RH-14 cover restart persistence, concurrent appends, same-ID retries versus conflicting reuse, cleanup reconciliation, late contradictory terminal events, partial writes, lost commit acknowledgements, version races, cross-tenant evidence, projection-schema changes, report/artifact cross-store failures, and authorization/retention races.

Updated links:
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` — commit `235de76bdb72e3e8af7bd96ba7723d6b5a55392e`, blob `6120d639621ae053f0719bc29603c4b67bc1ad5c`.
- `AI_COLLAB/CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md` — commit `7ebe8bcdcbd3a0200e398f788ec863de7c52b2cf`, blob `b50ba9b2673c4c065d6ca5eabe523ce0746bd1f4`.
- `AI_COLLAB/SEMANTIC_DECISION_CROSSWALK_20261029.md` — commit `9564c269c63b06ead8e6de9292e5636728752d2c`, blob `107113d725e283782ffd10a5bf57269756952af7`.

Key rule: issued report versions remain immutable; concurrent/late evidence creates a new durable version; append IDs are idempotent; publication is atomic or explicitly reconciled. In-memory ReportHistory is not durability or tamper-proof evidence.

### Combined D-06..D-08 status

- D-06: durable reservation, ambiguous dispatch, crash/restart, lease expiry and provider lookup/idempotency — DR-01..DR-12.
- D-07: release-time authorization, exact object integrity and bounded safe download — AR-01..AR-14.
- D-08: durable append-only report history, concurrency and cross-store consistency — RH-01..RH-14.

These checklists complement rather than replace COORD/FAKE cases. Fake tests establish coordinator decisions only; storage/provider/HTTP guarantees require integration evidence at the selected boundary. No implementation changed, no tests ran, no provider/store selected, and no account/billing/workload/merge/deployment action occurred. Canonical acceptance and PR #2/#3 remain untouched.

## Next pass

Read-only verification of current branch head, latest blobs for D-06/D-07/D-08 documents and crosslinks, plus PR #2/#3 and canonical acceptance blobs. Then do one targeted gap scan for any contradiction between the owner register, falsification matrix, and crosswalk. Do not add implementation until owner decisions and selected boundaries are available.
## 30. D-06..D-08 final static verification — 2026-10-29

Read-only re-fetch at branch head `874be9ee84e69761d785774eb083d0fcdafdb0f7` verified the latest files and cross-links:

- Handoff (this file before this section): blob `4f042e3bad0953eb5b82921aea87fc888e0d91d0`.
- Owner decision register: blob `6120d639621ae053f0719bc29603c4b67bc1ad5c`; includes D-06/DR-01..12, D-07/AR-01..14, D-08/RH-01..14.
- Control ownership/falsification matrix: blob `b50ba9b2673c4c065d6ca5eabe523ce0746bd1f4`; includes all three checklists.
- Semantic decision crosswalk: blob `107113d725e283782ffd10a5bf57269756952af7`; includes all three traceability rows.
- D-06 recovery checklist: blob `f6346dbc3dba9f97a431043612e5e17d17bfbfc8`.
- D-07 artifact release checklist: blob `9bea4083b9381271fe952bc108b3a13cb9b97fdb`.
- D-08 report history checklist: blob `4e5af07b640f23bf0ce8c37d9001709676ecbd52`.
- Adapter envelope cross-reference: blob `c4655541c5b86b2a573316ae086e11fd3e4e1ca8`.
- Coordinator/fake test plan cross-reference: blob `37c25137b972427771de0d53054b6cd57e211e57`.

Canonical acceptance remains unchanged: `PRODUCT/EXECUTION_CONTRACT.md` blob `3861e51ae4f9e45a263b677402f26c41b240959d`; `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.

PR #2 remains open/draft/unmerged at `eb8b7ea83cb0e8fe1880351276c485b761431791`; PR #3 remains open/draft/unmerged at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`. No changes to either PR.

Current status: D-06/D-07/D-08 requirements and falsification cases are documented only. No tests run, no implementation changes, no store/provider/runtime selected, and no account/billing/workload/merge/deployment action. D-01..D-05 and the D-06..D-08 owner proposals remain unresolved until owner decisions and selected boundary evidence exist.

## 31. Cross-decision contradiction audit and implementation gate sequence — 2026-10-29

Added [CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md), commit `7ff52d0fbca3477b3773945d1b6fca8083be345e`. It reviews D-06 idempotency/ambiguous dispatch, D-07 artifact release, D-08 durable report history, the adapter envelope, coordinator/fake test plan, and D-05 policy-boundary gate.

Result: no direct logical contradiction was found in the inspected documents. Seven residual interface/owner ambiguities are explicitly listed: authoritative provider “not created” semantics; authorization revocation during long downloads; integrity failure after streaming begins; report/artifact publication order; retention-horizon alignment; append/evidence/report-version identity separation; and separate execution verdict vs release status. The new document maps proposed G0-G7 gates from owner semantics and $0/boundary approval through pure validation, durable dispatch recovery, report history, artifact release, device acceptance, and full canonical regression.

Status is SPECIFIED ONLY / NOT RUN. No tests or workloads ran, no provider/store/runtime was selected, and no implementation changed. PR #2/#3 and canonical acceptance remain untouched. Current research branch HEAD at time of the new audit commit: `7ff52d0fbca3477b3773945d1b6fca8083be345e`; subsequent continuity-link commits may advance it. Next step: verify all new links and the final branch head, then keep work focused on the highest-value unresolved boundary contract rather than creating another broad checklist.


## 32. Provider-neutral boundary contract sketch — 2026-10-29

Added [PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md](PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md), commit `e1f9239ee7103579210ac83cd02f9b08e0055e1b`. The document turns D-05..D-08 into a proposed interface sketch for reserve/dispatch/reconcile, trusted evidence acceptance, immutable report publication, artifact publication/release, retention alignment, typed outcomes, proof levels and hard stops. It explicitly distinguishes request fingerprint from applied-policy evidence, UNKNOWN from definitive rejection, historical execution verdict from release authorization, and fake-test evidence from real boundary proof. Status remains SPECIFIED ONLY / NOT RUN; no provider/store/runtime selected, no implementation/tests/workloads, and no PR/canonical acceptance change. All D-01..D-04 remain owner-open and D-05 remains blocked pending actual boundary proof.


## Boundary proof-level review checklist — 2026-10-29

Latest follow-up: [BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md](BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md). This is a focused review aid mapping each guarantee to what pure tests, fake coordinator tests, persistence integration, provider integration, artifact store/API/HTTP integration, or device acceptance can actually prove. It identifies six implementation/audit blockers: authoritative provider “not created” semantics; actual dispatch policy barrier; report/artifact publication recovery; aligned retention and separate identity namespaces; release-time authorization and byte-integrity behavior; and owner resolution of D-01..D-04 before semantic/schema freeze. It specifies a staged test order and explicitly leaves all decisions and implementation gates unchanged. SPECIFIED ONLY / NOT RUN; no provider/store/runtime selected; canonical acceptance and PR #2/#3 remain untouched.


## Implementation-readiness backlog — 2026-10-29

Added [IMPLEMENTATION_READINESS_BACKLOG_20261029.md](IMPLEMENTATION_READINESS_BACKLOG_20261029.md). It converts the current research into WP-00..WP-07: independent review; owner decision packet D-01..D-04; pure contract/reducer tests; actual policy-at-dispatch barrier; durable reservation/recovery; trusted evidence/report history; artifact publication/release; and phone/canonical acceptance. It states dependencies, closure evidence, and hard stops, with a small reviewer reconciliation ledger that must only be populated from concrete review output. No decisions are approved by this backlog. D-01..D-04 remain owner-open, D-05 remains blocked, D-06..D-08 remain proposals. No tests/workloads ran; provider/store/runtime unselected; canonical acceptance and PR #2/#3 untouched.


## D-01..D-04 owner decision packet — 2026-10-29

Added [OWNER_DECISION_PACKET_D01_D04_20261029.md](OWNER_DECISION_PACKET_D01_D04_20261029.md). It translates the four unresolved/proposed semantic choices into explicit owner choices with canonical anchors, counterexamples, affected LOOP/CASE IDs, proof boundaries and a response template. D-01/D-03/D-04 remain OPEN; D-02 remains a proposed default requiring owner confirmation before schema freeze. The packet does not alter canonical acceptance or authorize implementation.


## Pure contract test inventory — 2026-10-29

Added [PURE_CONTRACT_TEST_INVENTORY_20261029.md](PURE_CONTRACT_TEST_INVENTORY_20261029.md). It lists PURE-01..PURE-12 candidate validation/canonicalization/output/file/report tests, SEM-01..SEM-10 tests blocked wholly or partly on D-01..D-04, the coordinator/fake boundary, evidence labels and a gap-only next task. This is design only: tests NOT RUN. Next pass should reconcile each pure candidate against the exact pinned test files and mark existing coverage, missing coverage, or source-change/decision-needed—without modifying PR #2/#3 from this research branch.


## Pinned-test coverage reconciliation — 2026-10-29

Added [PURE_TEST_COVERAGE_GAP_AUDIT_20261029.md](PURE_TEST_COVERAGE_GAP_AUDIT_20261029.md) after re-fetching the exact PR #2/#3 source and test blobs. The audit identifies specific missing test-source coverage while preserving the distinction between source-level findings and live vulnerability claims. Recommended next task: review G-01..G-09, confirm each intended validation/retention contract, then propose any bounded patch only on the corresponding isolated PR branch after a fresh SHA check. This research branch only holds the audit; PR #2/#3 remain unchanged and tests remain NOT RUN.


## G-01..G-03 patch-ready specification — 2026-10-29

Added [G01_G03_PATCH_READY_TEST_SPEC_20261029.md](G01_G03_PATCH_READY_TEST_SPEC_20261029.md). It narrows the first three coverage gaps to exact parameter matrices, proposed strict validation behavior, and acceptance conditions. G-01's malformed-input policy and G-03's surrounding-whitespace normalization need explicit contract choices before assertions can be finalized. G-02 proposes strict positive integer caps excluding bool. No source/test edits or tests were run; PR #2/#3 remain unchanged. Next, owner can authorize a bounded PR #3 patch or request more review; if authorized, re-fetch exact branch/file SHAs before editing.


## G-01..G-03 recommended behavior and proof gates — 2026-10-29

Added [G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md](G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md) as a technical recommendation, not an owner decision. Recommended minimal policy: malformed limit flags raise TypeError rather than being truthiness-coerced; output caps reject bool/non-int with TypeError and nonpositive integers with ValueError; required fingerprint fields reject whitespace-only strings while preserving nonblank values and existing field-specific normalization. The document includes an illustrative snippet, exact regression matrix, and bounded test/verification sequence. Not implemented; tests NOT RUN; PR #2/#3 and canonical acceptance untouched.


## G-07/G-08 patch-ready test specification — 2026-10-29

Added [G07_G08_PATCH_READY_TEST_SPEC_20261029.md](G07_G08_PATCH_READY_TEST_SPEC_20261029.md). G-07 covers the six Windows superscript device-name aliases (COM¹/²/³, LPT¹/²/³) with extension variants. G-08 covers tombstone repeated-add behavior: same-fingerprint idempotency without shortened expiry, conflicting fingerprint rejected without mutation, tenant isolation and exact expiration. Recommendation only; no source/test edit or test run. Re-fetch source SHAs before any authorized patch.


## Consolidated owner decision and patch gate — 2026-10-29

New single entry point: [CONSOLIDATED_OWNER_DECISION_AND_PATCH_GATE_20261029.md](CONSOLIDATED_OWNER_DECISION_AND_PATCH_GATE_20261029.md). It consolidates D-01..D-04 semantic choices and G-01/G-02/G-03/G-07/G-08 bounded helper fixes, recommends a patch grouping, and provides one copy-ready response template. This is a decision aid only. A behavior approval is not code-edit authorization; owner must specify exact scope and branch. No tests/source changes, PR #2/#3 untouched, canonical acceptance unchanged.


Follow-up static source review: [G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md](G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md). It records exact implementation observations (validation precedence in G-01; bool/float cap acceptance in G-02; whitespace runtime normalizing to empty in G-03; exact superscript alias gap in G-07) and adds a necessary G-08 owner choice: whether an expired tombstone may be replaced when no lookup has lazily removed it. Still no source/test changes and no tests run.


G-08 nuance: the add API receives `deleted_at`, which may be event time rather than current acceptance time. Do not treat it as proof that a previous tombstone is expired unless the contract guarantees that clock. Owner must choose the authoritative-time rule before coding; the existing `IdempotencyConflict` is the natural conflict exception to reuse.


---

## 33. Current-chat final handoff addendum — unified product direction and documentation reconciliation (2026-10-29)

**Authority note:** This section records the newest verified state and supersedes any older, conflicting wording in earlier sections of this long handoff. Older detailed audits/checklists remain useful unless explicitly superseded here. Do not interpret this addendum as proof of implementation or tests.

### Current live PocketCode branch

- Repository: `marcelosofficial-ctrl/PocketCode-`
- Research branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- This handoff has since been updated with the cross-project wording reconciliation; fetch the branch's live HEAD before starting rather than relying on historical SHAs embedded in older sections.
- This is an isolated research branch, not main. Refresh live refs before further edits.
- PR #2 remains open/draft/unmerged: `chat-continuity-report-regressions-2026-10-26`, head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PR #3 remains open/draft/unmerged: `pocketcode-pass0-audit-2026-10-26`, head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- Main was last checked at `555840d8d83342513d9cd353d4d1522d46a5c82d`. Do not assume it has not moved since this check.
- Do not modify PR #2/#3, main, canonical acceptance/contract files, source/tests, provider/store/runtime, budgets, security/execution boundaries, or deployment/Actions without explicit authorization.

### Settled product direction — not an integration-topology decision

RevDev and PocketCode are intended to converge toward **one coherent PC-and-phone product/program**. RevDev is the PC-side guarded developer-operations/control-plane path; PocketCode is the phone-first path. Separate repositories, roadmaps, implementations, clients, adapters, acceptance suites, evidence, and release gates remain appropriate during development.

This direction does **not** authorize a repository merge, shared-code migration, shared runtime, frontend rewrite, or change to either execution/security boundary. Integration topology remains undecided until the fixed-task PocketCode comparison and verified RevDev artifacts justify a separately reviewed, evidence-backed plan. PC/runtime/installed binary/queue/publication behavior remains UNKNOWN while the owner lacks PC access.

### Documentation reconciliation completed and verified

Latest relevant blobs on the research branch:

- `DECISIONS.md` — `8d54d361546b31a58fb1aee48f4678afc4699856`. D-001 already records the unified product destination, separate engineering boundaries, and the requirement for a separately reviewed integration plan; this wording predated the final three edits below.
- `PROJECT_STATUS.md` — `30be7d4988db26fcb5c72b3d52e5bd669676365e`. Replaced the stale “convergence remains a goal to evaluate” statement and the assertion that PocketCode is separate from RevDev.
- `PRODUCT_SPEC.md` — `524479c2b64e47d892de64ace617c84f9e452c59`. It already reflected the clarified direction; no further edit was needed in the final pass.
- `PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md` — `35344d54cd7864862797c424686de885a217c70d`. Introduction states the intended unified destination and preserves topology/security boundaries; Stage 4 now selects an evidence-backed integration topology rather than treating convergence itself as undecided.
- `AI_COLLAB/MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md` — `7b3e7c0f357c979db83a8ec2863621447ed4954a`. Identified as the primary AI Workflow Director research reference on this branch; links the historical [AI Efficiency Coach & Handoff proposal](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-continuity-recovery-2026-10-27/PRODUCT/AI_EFFICIENCY_COACH_HANDOFF_PROPOSAL_2026-10-28.md) as source material for AEC-001–AEC-012; says its older product-boundary wording is not authoritative. The master also states the unified direction in §7.
- Historical source material remains preserved. Do not rewrite the old AEC proposal merely to erase its historical wording.

Recent documentation commits made in this session:
1. `eaff2f013d6ecebd592f0d8dd62a88a1b474f0af` — shared-core convergence stage.
2. `3cc5b9b53085c0ee426e2d2bb21dc8afd2e8b703` — research master role and AEC source.
3. `bfb38d1c85e9b9f7b750fd816369beb1b3c28b7e` — Project Status clarification.

Other commits already present before those include `d8c9c244336a1200c214339326364d5cf479189d` (D-001 direction), `38d661e1bcf25830461197808e2da3ecf50e88ef` (shared-core vision), `9bb7f532d2914ebd944ea4cc4e88a4d1b52ac158` (Product Spec), and `e13043b125828cbfb85a36a6f7d594a4257765d8` (research-master wording). Fetch live branch state before using any older SHAs as current.

### Acceptance suites and evidence boundaries

Keep the suites separate and preserve their original meanings:
- PocketCode canonical: `LOOP-01–LOOP-14` and `CASE-01–CASE-16`; canonical acceptance blob checked: `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- PocketCode AI Efficiency Coach historical/source definitions: `AEC-001–AEC-012`.
- RevDev: `AWC-001–AWC-018`, `P8U-01–P8U-12`, and `P0-D 1–10`.
- Never claim a shared concept, one suite, fake adapter, static inspection, or another project's passing test proves the other project's implementation.
- No tests were run in this final documentation pass. No source/test code, provider/store/runtime, workload, spending, merge, deployment, or Actions changes occurred.

### Cross-repository wording reconciliation — completed

The PocketCode product-direction documents and the RevDev workflow-efficiency master have now been reconciled in place. The RevDev file was re-fetched at its prior blob SHA, edited with five targeted paragraph replacements, and read back in full.

- RevDev repository: `marcelosofficial-ctrl/DevRelay-Missions`
- Review branch: `review/revdev-adaptive-ai-workshare-2026-10-27`
- Master wording-change commit: `893266b52ac83388b7f1796bc443f85aa4011768`.
- Latest RevDev branch HEAD subsequently checked: `cf07a4fc61528ff1eaccf660338c66ce19fa9179` — refreshes the convergence handoff after the timeout-precedence review.
- Changed master: `resume/revdev/AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md`; previous blob `057e623248314214b7a35c296de811f27bd3a1f2`, resulting blob `ea832fa61c826724bc8281edb23b4cfa46bde942`.
- New RevDev handoff: `resume/revdev/NEW_CHAT_HANDOFF_2026-10-29_REVDEV_POCKETCODE_CONVERGENCE.md`, current blob `14e88707d34773ca156fe028735bfe2f0ec57e14`.
- [Inspect the wording-change commit](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/commit/893266b52ac83388b7f1796bc443f85aa4011768)
- [Read the RevDev convergence handoff](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/NEW_CHAT_HANDOFF_2026-10-29_REVDEV_POCKETCODE_CONVERGENCE.md)

The edit corrected legacy language around §3.5 / lines 241, 319, 327, 392 and 400. It now states the unified PC-and-phone product direction, preserves separate repositories/implementation streams/acceptance suites/release gates during development, and explicitly does not authorize merge, shared-code migration, shared runtime, or execution/security-boundary changes. The old statement that PocketCode's direction changes were still pending was updated.

RevDev cross-project references:
- Alignment note: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/REVDEV_POCKETCODE_CROSS_PROJECT_ALIGNMENT_2026-10-29.md
- Draft semantic crosswalk: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/REVDEV_POCKETCODE_SEMANTIC_CROSSWALK_DRAFT_2026-10-29.md
- Updated workflow-efficiency master: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md

### Timeout verdict precedence — exact cross-branch status

A fresh read-only comparison found that the earlier timeout-precedence finding must be described by branch, not as a blanket claim about every revision:

| Ref | Helper blob | Static behavior |
|---|---|---|
| PocketCode `main` and research branch | `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817` | Any valid nonzero exit code returns FAIL before terminal-state handling. Thus `timed_out` + 137 can incorrectly become FAIL relative to canonical CASE-04. Test blob `85109f056009d65a274e9306deb39b68e1fefbd2` lacks that combination. |
| PR #2 branch `chat-continuity-report-regressions-2026-10-26` | `e9d944a722c2fac5279952696528da72a7011af3` | Candidate fix: nonzero exit influences verdict only when lifecycle status is `succeeded`; other states remain INCOMPLETE unless status is `program_failed`. Test blob `39f3a3ef865ed55f333a1edc208096d99197d023` explicitly tests timeout/137, cancellation/143, infrastructure failure, rejection, running and unknown with nonzero codes. |
| PR #2 status | Head `eb8b7ea83cb0e8fe1880351276c485b761431791`; open/draft/unmerged | Candidate source/test change exists but is not merged. Tests NOT RUN; no PR changes made in this pass. |

The candidate fix appears to address the specific precedence mismatch, but it does not add explicit exit-code provenance to the helper interface. The next bounded review must decide whether the caller contract adequately guarantees that `exit_code` is the authoritative child-program code when paired with `succeeded`, or whether contradictory/wrapper evidence needs a distinct representation. Do not edit PR #2, tests, canonical acceptance, or implementation.

Research note with this exact comparison: [Execution Verdict Crosswalk Follow-up](EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md), current blob after static assessment `a57aa70254d70bd373bf150af85c1682ec34e8b9`, commit `52bee593149fd426414f4e649ec2788e40a26dc7`.

### Exact next work for the new chat

1. Read this addendum first, then the [PocketCode current checkpoint](POCKETCODE_CURRENT_CHECKPOINT_20261028.md), [primary Workflow Director research master](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md), [shared-core proposal](../PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md), [owner decision register](OWNER_DECISION_REGISTER_20261029.md), and [timeout verdict crosswalk follow-up](EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md). Use the RevDev convergence handoff linked above for the other repository's latest continuity state.
2. Re-fetch live PocketCode branch/main, RevDev review branch, and PR #2/#3 refs before making claims. Branches have advanced during this pass.
3. The narrow timeout-precedence static review is complete and documented in §8 of the crosswalk follow-up. The PR #2 candidate appears to fix the CASE-04 precedence mismatch; exit-code provenance remains a caller-contract invariant to verify at any future integration. Independent Claude/Gemini review has not been obtained. Do not edit PR #2, tests, canonical acceptance, or implementation.
4. Next, perform a bounded **draft semantic crosswalk** only: map shared concepts against the exact PocketCode canonical LOOP/CASE contracts and RevDev's own AWC/P8U/P0-D suites. Keep it draft until actual artifacts from both sides have been compared. PC source/runtime/queue/publication evidence remains unavailable, so do not claim implementation equivalence or that one project's acceptance proves the other.
5. Keep execution-location research separate: PocketCode's fixed-task comparison (local phone, browser/WASM, user-owned remote PC, hosted, manual copy/paste) remains NOT RUN; $0 default remains binding. No provider selection, account creation, billable workload, or runtime claim.
6. Then checkpoint the highest-value unresolved question. Do not start a broad research sweep or implement the proposed contract without explicit authorization.

### Copy/paste prompt for the new ChatGPT conversation

You are continuing the existing PocketCode project, not starting a new project. First read `AI_COLLAB/CHAT_HANDOFF_20261029_POCKETCODE.md`, especially its final §33 addendum, then read the current checkpoint, primary Workflow Director research master, shared-core proposal, and owner decision register on the live research branch. Re-fetch live GitHub branch/commit/blob refs before making claims or edits.

Owner direction: RevDev and PocketCode are intended to converge toward one coherent PC-and-phone product/program. Keep repositories, implementations, clients/adapters, acceptance suites, evidence and release gates separately managed during development. This does not authorize a merge, shared-code migration, shared runtime, frontend rewrite, or any execution/security-boundary change. Topology requires a separately reviewed, evidence-backed plan. PC/runtime/installed binary/queue/publication state is UNKNOWN while the owner lacks PC access. Budget is $0; no provider/account/workload/spend, deployment/Actions, merge, or security-boundary change. Do not touch PR #2 or PR #3, canonical acceptance, source/tests, or execution queues.

Three-AI roles: Claude is lead developer/RelayRef; Gemini is co-developer and independent security/spec auditor; ChatGPT is continuity holder, evidence reconciler, test architect and cross-branch conformance auditor (eventual deployment coordination only if explicitly authorized). Treat proposals as proposals, static inspection as static inspection, and unrun tests as NOT RUN. Preserve acceptance IDs exactly: PocketCode LOOP-01–14 and CASE-01–16; historical AEC-001–012; RevDev AWC-001–018, P8U-01–12 and P0-D 1–10. No suite proves another project's implementation.

Current PocketCode research branch: `pocketcode-ai-workflow-director-research-2026-10-28`; fetch its live HEAD before starting, because this handoff has itself been updated since the earlier checkpoint. D-001, Project Status, Product Spec and shared-core proposal now express the unified direction while preserving separate engineering boundaries. The Workflow Director research master is the primary research reference and links the older Coach proposal as historical/source material for AEC-001–AEC-012. PR #2 remains draft/open/unmerged at `eb8b7ea83cb0e8fe1880351276c485b761431791`; PR #3 remains draft/open/unmerged at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.

The timeout-precedence static review is now documented in §8 of `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md` (blob `a57aa70254d70bd373bf150af85c1682ec34e8b9`, commit `52bee593149fd426414f4e649ec2788e40a26dc7`). It found the PR #2 candidate fixes the specific CASE-04 mismatch; child-exit versus wrapper-code provenance remains a caller-contract invariant for future integration. Independent Claude/Gemini review has not been obtained. Do not edit PR #2, source/tests, or canonical acceptance. Next do a bounded draft semantic crosswalk across PocketCode LOOP/CASE and RevDev AWC/P8U/P0-D; do not claim implementation equivalence while PC artifacts are unavailable.


---

## 34. Latest verified checkpoint — bounded verdict-precedence recheck (2026-10-29, newest)

This section supersedes stale HEAD statements and describes the latest verified live branch state. Do not treat any static inference below as executed test evidence.

### Live refs rechecked

- PocketCode research branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Current HEAD: `74cc7a4297df0b7ebf6dc51bcb67ca5c5194044c` — `docs: record bounded verdict precedence recheck`
- New document: `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_RECHECK_20261029.md` (81 lines; added in that commit).
- Main HEAD: `555840d8d83342513d9cd353d4d1522d46a5c82d` at this check.
- PR #2 remains open/draft/unmerged: `chat-continuity-report-regressions-2026-10-26`, head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PR #3 remains open/draft/unmerged: `pocketcode-pass0-audit-2026-10-26`, head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- RevDev review branch `review/revdev-adaptive-ai-workshare-2026-10-27` currently points to `cf07a4fc61528ff1eaccf660338c66ce19fa9179` — `Update convergence handoff after timeout review`.
- The RevDev workflow master remains blob `ea832fa61c826724bc8281edb23b4cfa46bde942`. The RevDev handoff was updated in the newest RevDev commit; fetch it before assuming details are unchanged.

### Latest verdict-precedence findings

The read-only recheck fetched exact canonical acceptance, execution contract, helper, tests and decision register. Current key blobs at that check:
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`: `c6714c27db52b2962fe8d1c7e6a16829d46a8338`
- `PRODUCT/EXECUTION_CONTRACT.md`: `128a00a9b2a335514814cab76fb5781fe8f9f858`
- `scripts/report_contract.py`: `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`
- `scripts/test_report_contract.py`: `85109f056009d65a274e9306deb39b68e1fefbd2`
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`: `e67b2659cf2d71ef77d8e4619c91143e71062470`
- `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md`: `a57aa70254d70bd373bf150af85c1682ec34e8b9`
- `AI_COLLAB/EXECUTION_VERDICT_ARTIFACT_RELEASE_RECONCILIATION_20261029.md`: `8f0d592995a625f9bf47ac15848c92008e15f855`

Static finding: `classify_verdict(execution_status, exit_code)` returns FAIL for a valid nonzero integer exit code before considering lifecycle status. Thus `timed_out + nonzero code` statically maps to FAIL, while canonical LOOP-05 / CASE-04 require a trusted timeout to remain INCOMPLETE / `timed_out`. Existing timeout tests pass `None` as the exit code and do not cover this combination. This is static analysis, not an executed test result.

The separate crosswalk follow-up concludes the PR #2 candidate appears to fix this specific CASE-04 precedence mismatch, but child-exit versus wrapper/termination-code provenance remains a caller-contract invariant to verify at future integration. Independent Claude/Gemini review has not been obtained. Do not change PR #2, source/tests, canonical acceptance or implementation. Do not treat an apparently relevant PR patch as proof that the entire report contract or product is accepted.

### Immediate next work

1. Read `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_RECHECK_20261029.md` and `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md`, then inspect the exact relevant PR #2 diff read-only if needed. Confirm what the existing PR candidate actually changes; do not edit it.
2. Resolve the narrow semantic question at the contract/documentation level: what is the provenance and meaning of `exit_code` (child program exit versus wrapper/termination code)? Keep canonical CASE-04 authoritative. If source contract does not distinguish provenance, record that limitation rather than inventing semantics.
3. After that, continue the bounded draft cross-project semantic crosswalk across PocketCode LOOP/CASE and RevDev AWC/P8U/P0-D. Preserve each suite's IDs and semantics. Keep it draft because RevDev PC/runtime/queue/publication evidence is unavailable; shared concepts or static source review do not prove implementation equivalence.
4. Re-fetch all refs before further claims. Do not modify PR #2/#3, main, source/tests, canonical acceptance, provider/runtime/queue, or security boundaries. Tests were NOT RUN in the latest read-only verdict-precedence recheck.

### Continuity update to the earlier copy/paste

Use the current HEAD above, not the older `bfb38d1c...` checkpoint. The prior handoff sections remain useful for product direction, three-AI roles, the $0 budget, PC-access limitation, acceptance-suite separation and the completed PocketCode/RevDev wording reconciliation. This §34 addendum is the latest authority where branch status or the next task differs.


---

## 35. Final handoff correction — live refs and exit-code provenance (2026-10-29)

This section supersedes any older branch-HEAD statement above. The previous §34 correctly records the bounded analysis, but its stated HEAD was the parent commit that added that checkpoint, not the newest live branch head.

### Live refs checked immediately before handoff

- PocketCode repository: `marcelosofficial-ctrl/PocketCode-`
- Research branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- **Current branch HEAD:** `493b0f1dafdc5ef4ecace42491d84cd18f00330d` — `Add latest verdict-precedence checkpoint to handoff`.
- Handoff file blob: `3834a48a8d318ac76393db28cc73e6d3d86e4db9`.
- Parent commit: `74cc7a4297df0b7ebf6dc51bcb67ca5c5194044c` — `docs: record bounded verdict precedence recheck`.
- Main HEAD checked: `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PR #2 remains open/draft/unmerged: branch `chat-continuity-report-regressions-2026-10-26`, head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PR #3 remains open/draft/unmerged: branch `pocketcode-pass0-audit-2026-10-26`, head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- RevDev review branch: `review/revdev-adaptive-ai-workshare-2026-10-27`, current HEAD `cf07a4fc61528ff1eaccf660338c66ce19fa9179`.
- RevDev workflow-efficiency master blob remains `ea832fa61c826724bc8281edb23b4cfa46bde942`; live readback found no targeted stale product-boundary phrases.

The handoff was read back at the exact blob above. The newest checkpoint is this §35 plus §34 and the execution-verdict crosswalk documents linked there. Refresh all refs again before further work.

### Narrow provenance conclusion

Read-only reinspection compared the canonical PocketCode acceptance/contract with the main/research helper and the PR #2 candidate:

- Canonical acceptance `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`: blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`; CASE-04 requires a trusted timeout to remain `INCOMPLETE / timed_out`.
- Execution contract `PRODUCT/EXECUTION_CONTRACT.md`: blob `128a00a9b2a335514814cab76fb5781fe8f9f858`; describes `succeeded` as program exit 0 plus complete provider result, `program_failed` as nonzero exit or language/runtime failure, and `timed_out` as trusted server/provider deadline enforcement. It does **not** define a separate field or rule distinguishing child-program exit codes from wrapper/termination codes.
- Main/research helper `scripts/report_contract.py`: blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`; a valid nonzero integer wins before lifecycle-state handling, statically allowing `timed_out + 137 => FAIL`, contrary to CASE-04.
- PR #2 candidate helper: blob `e9d944a722c2fac5279952696528da72a7011af3`; it makes `program_failed` an explicit FAIL and uses exit-code PASS/FAIL only when status is `succeeded`, leaving uncertain statuses INCOMPLETE. PR #2 test source blob `39f3a3ef865ed55f333a1edc208096d99197d023` includes `timed_out/137` and related uncertain-state regressions.
- This is a **static code/documentation comparison only**. No tests were run, and no production caller/integration path has been established.

**Conclusion:** The narrow expected precedence is clear from canonical CASE-04, but the precise provenance of the `exit_code` field remains unspecified by the execution contract. Do not invent a child-versus-wrapper distinction. Record it as an open contract ambiguity. The PR #2 candidate appears to avoid the specific timeout-precedence mismatch, but it has not been merged or tested in this review, and does not establish the entire report contract as accepted.

### Immediate next task for the new chat

1. Re-fetch current branch/main and PR #2/#3 refs and read the two specialist documents:
   - `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_RECHECK_20261029.md`
   - `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md`
2. Inspect the exact PR #2 diff read-only to confirm the candidate's scope; do not modify the PR. Keep the main/research helper finding and the PR candidate finding distinct.
3. Resolve the contract question narrowly: should `exit_code` mean only an authoritative child-program exit code, with wrapper/termination codes represented separately, or is a provenance field required? If existing contract evidence cannot answer it, leave it OPEN and formulate the minimal proposed contract wording—do not freeze schema or edit source/tests.
4. Then continue the bounded draft semantic crosswalk between PocketCode canonical LOOP/CASE and RevDev AWC/P8U/P0-D. Do not claim implementation equivalence; RevDev PC/runtime/queue/publication state remains UNKNOWN.
5. Preserve all restrictions: no PR #2/#3 changes, no source/tests/acceptance edits, no provider/runtime/account/workload/spend, no Actions/merge/deploy, no queue mutation, no security-boundary change. Tests remain NOT RUN.

