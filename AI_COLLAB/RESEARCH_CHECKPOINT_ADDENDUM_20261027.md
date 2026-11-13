# Research Checkpoint Addendum — 2026-10-27

**Checkpoint ID:** PC-RESEARCH-CP-ADD-2026-10-27-001  
**Branch:** pocketcode-pass0-audit-2026-10-26  
**Scope:** Follow-up after the original checkpoint; source/version coherence, lifecycle semantics, and Gemini handoff.  
**Status:** Static research and document review only. No tests run, no provider workloads, no accounts, no spend, no deployment, no merge.

## Canonical updates since the original checkpoint

- [Contract coherence audit](CONTRACT_COHERENCE_AUDIT.md) — static audit of lifecycle, evidence, cleanup, limits, capability freshness, artifact safety, tenant authorization, egress, and report integrity.
- [Contract coherence resolution](PASS1_CONTRACT_COHERENCE_RESOLUTION.md) — proposal to separate execution-outcome facts from overall job disposition. **Proposal only; not an accepted API decision.**
- [Offline acceptance-test matrix](OFFLINE_ACCEPTANCE_TEST_MATRIX.md) — proposed deterministic tests, including LC-01 through LC-12. **Not run.** Fake adapters cannot establish provider isolation, real termination, effective egress enforcement, or billing behavior.
- [Source/version coherence audit](PASS1_SOURCE_VERSION_COHERENCE_AUDIT.md) — records provider-document version and source-integrity follow-ups.
- [Runtime/provider gate](PASS1_RUNTIME_PROVIDER_GATE.md) — provider-neutral gate; no provider approved for live tests under the current strict $0 budget.
- [Gemini Pass 1 review integration](GEMINI_PASS1_REVIEW_INTEGRATION_20261027.md) — received review triage, verified provider-source corrections, and non-adopted recommendations.
- [Gemini review request](GEMINI_REVIEW_REQUEST.md) — prepared for external copy/paste. Gemini's independent review was subsequently returned by the user and integrated in [Gemini Pass 1 review integration](GEMINI_PASS1_REVIEW_INTEGRATION_20261027.md). ChatGPT has no direct Gemini messaging connector; the review was relayed by the user.

## Source/version corrections to preserve

1. **Daytona v0 and v2 alpha are different documentation contexts.** Do not transfer v0 tier-based override claims into v2 alpha. Review both pages separately:
   - v0 network limits: https://www.daytona.io/docs/en/network-limits/
   - v2 alpha network limits: https://www.daytona.io/docs/en/v2/network-limits/
   - v2 alpha limits: https://www.daytona.io/docs/en/v2/limits/
   The v2 alpha network documentation says egress is open by default and requested policy may differ from applied policy; the current official page exposes desired/applied policy, pending/applied/failed status and revisions. User code must not start until the exact required policy is confirmed applied. ETag is a revision/concurrency token, not itself proof of enforcement. These are documentation findings, not runtime verification.

2. **E2B security/testing permission:** current reviewed page is https://e2b.dev/security. It says to contact E2B before running tests because prior written consent is required. No testing was attempted.

3. **Modal networking:** https://modal.com/docs/guide/sandbox-networking. Direct page retrieval returned an upstream 502, but the current official search-indexed result was rechecked on 2026-10-27: public outbound access is allowed by default; DNS is unrestricted except when all outbound traffic is blocked; `block_network=True` drops all outbound traffic; domain allowlisting is Beta/TLS 443. This is documentation, not runtime proof; re-open the primary page before a provider decision. Pricing: https://modal.com/pricing. Included credits are not a guaranteed hard $0 ceiling.

4. **Cloudflare Containers pricing:** https://developers.cloudflare.com/containers/platform/pricing/ lists the Workers Paid base plan at $5/month. That conflicts with the current strict $0 constraint absent an explicit owner-approved budget change.

5. **Do not equate official documentation with verified behavior.** Provider claims remain unvalidated until an explicitly authorized, controlled proof is conducted. No such proof is currently authorized.

## Lifecycle decision still open

The draft contract's sequence can be read as SUCCEEDED followed by cleanup, while other prose implies success requires cleanup success. The proposed resolution is to distinguish:

- **Execution outcome:** observed process facts (for example zero exit, non-zero exit, timeout, cancellation, or termination unconfirmed).
- **Overall job disposition:** the policy-governed final report status after evidence, artifact, and cleanup gates.

This separation is a candidate model, not an approved schema. Before implementation, choose explicit semantics for cancellation/timeout races, cleanup failure, retries, duplicate events, missing evidence, and partial artifact publication. No PASS may be reported if mandatory evidence or cleanup requirements are unmet.

## Product validation and limits

- The prototype remains simulated; no real execution backend exists.
- Gemini's review has been received; its recommendation to adopt Modal by default and to reject local Android execution is not adopted. Neither is justified under current evidence and strict $0 constraints.
- The Python+CSV quick-run verifier remains a hypothesis, not validated demand.
- No representative interviews or hands-on task benchmark has been completed.
- PocketCode naming collision risk remains unresolved; no legal conclusion or rename decision.
- Strict $0: no accounts, credentials, provider workloads, billing changes, deployment, or merge.

## Current repository/PR snapshot

At checkpoint creation, PR #3 was open, draft, unmerged, with branch head c7c1a6601c4635f12aefa1c6d164a1d248bea8ed. Re-check live PR metadata before relying on that SHA. PR #2 must remain untouched.

## Next actions

1. Continue static internal-link/source freshness verification; the current indexed Modal guide's DNS statement is recorded in the later source-clarification section below, but re-open the primary page before any provider decision.
2. Resolve the remaining two-axis lifecycle semantics, idempotency conflict behavior, output/secret-redaction policy, and provisional artifact handling before freezing the contract.
3. Add deterministic offline tests for policy-application barrier, cancel/timeout race, process-tree handling, streaming limits, artifact hash failure, and cost telemetry. All remain NOT RUN.
4. Perform low-cost, behavior-based user validation only when the owner can recruit participants; no trial has yet occurred.
5. Keep provider selection, accounts, live tests, spending, deployment and merge blocked without separate approval. PR #3 remains draft/unmerged; PR #2 untouched.


## 2026-10-27 continuation — lifecycle/idempotency/artifact policy

The older PR-head SHA and next-action list above are historical checkpoint values, not current branch status. The latest live PR metadata should be used for the current head.

- New proposal: [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md).
- Matrix expanded with LIFE-SEM, RACE-SEM, IDEM-SEM, ART-SEM, STREAM-SEM, COST-SEM, and NET-SEM cases; all remain NOT RUN.
- Proposed default: keep artifacts quarantined until cleanup confirmation and validation gates pass. This is not yet an owner-approved product/API decision.
- Still unresolved: event reconciliation policy; idempotency fingerprint and retention; stream overflow behavior; whether provisional artifact exposure is ever allowed.
- No provider, account, workload, spend, code/test execution, merge, or deployment. PR #3 remains draft/unmerged and PR #2 untouched.
- Next: static internal-link and source freshness review, then owner review before any schema freeze or offline test implementation.


## 2026-10-27 continuation — Modal networking documentation clarified

The official search-indexed Modal networking guide was rechecked after direct page retrieval returned 502. It explicitly states DNS traffic is unrestricted except when all outbound traffic is blocked, and block_network=True drops all outbound traffic. Domain allowlisting is Beta/TLS 443; dynamic policy updates are Alpha.

The related provider research, runtime gate, source-integrity note, and source/version audit now reflect this wording. This closes the documentation wording gap only; it does not establish runtime enforcement, metadata/private-path behavior, exact-plan suitability, or a hard $0 cap. Re-open the primary page before a provider decision.


## Delegated decision status — 2026-10-27

The owner subsequently delegated the six lifecycle decisions to ChatGPT. The earlier owner-review next-action lists above are historical and superseded by this section. The selected baseline and rationale are in [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md) and [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md); the draft contract and lifecycle proposal have been aligned. The acceptance matrix records additional tests now required by these choices. None of those tests has been run yet.

**Current next step:** implement provider-neutral schema/state-machine/report tests with synthetic inputs and fake adapters, then run and record exact commands/results if the available tooling permits. No provider accounts, workloads, spend, production implementation, merge, or deployment. PR #3 remains draft/unmerged; PR #2 remains untouched. The existing PR description may still contain the older next-action text; do not treat this checkpoint update as proof the PR body was changed.


## Implementation checkpoint — provider-neutral contract helpers

Added `scripts/lifecycle_contract.py` and `scripts/test_lifecycle_contract.py` as pure provider-neutral decision helpers and synthetic regression tests. Coverage includes evidence-derived disposition, coordinator-sequence event replay, canonical request fingerprints, idempotency replay/conflict, artifact release gates, byte-bounded output, and configured-pattern redaction across chunk boundaries. These files do not launch submitted code or contact providers. **The repository test suite has not been run**; the next step is offline syntax/test execution and review. A focused isolated check of the redaction pattern across a chunk boundary succeeded, but that is not a full test run. PR #3 remains draft/unmerged, PR #2 untouched, strict $0 unchanged.


## Temporary offline test result — 2026-10-27

A temporary Python run of 8 synthetic tests using a reconstructed copy of the current helper and test module reported **8 passed, 0 failures, 0 errors**. This was not run from a repository checkout, and the complete repository test suite remains unrun. No GitHub Actions, provider, submitted program, or live workload was used. Re-run the exact checked-in files in an offline checkout before treating this as branch-level test evidence.


## Current coherence status — 2026-10-27

The earlier lifecycle-open statements in this checkpoint are historical and superseded by the delegated decision record. The selected baseline and rationale are in [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md); the draft execution contract, lifecycle policy, acceptance matrix, decision register, project status, and PR description have been aligned.

The crosswalk confirmed that named inputs are an unordered mapping sorted by normalized canonical name for fingerprint v1; a future order-sensitive workflow needs a new contract/fingerprint version. It also aligned timeout/cancel reconciliation and the provisional 30-day tombstone language. A static helper review corrected disposition precedence so contradictory evidence yields `INCOMPLETE` even when the nominal outcome is `NOT_STARTED`. The checked-in synthetic lifecycle test module now has 21 test methods, including aggregate-only output overflow.

**Verification remains NOT RUN** for the exact checked-in helper/test pair and full repository suite. The earlier 8/8 reconstructed-copy run is historical only. No GitHub Actions, provider, account, live workload, spend, deployment, or merge. PR #3 remains open/draft/unmerged; PR #2 remains untouched. Next safe step: use [CONTRACT_CODE_TEST_TRACEABILITY_20261027.md](CONTRACT_CODE_TEST_TRACEABILITY_20261027.md) to finish requirement-to-code-to-test traceability, then run exact checked-in tests offline when an interpreter is available.

## 2026-10-27 — Input identity and PASS-report gate hardening

Static review found two additional contract gaps. First, the fingerprint helper described names as safe basenames but allowed Windows-reserved characters/device names, trailing dots/spaces, and blank media types. It now rejects these portable-name hazards and blank media types before producing a fingerprint; negative fixtures cover traversal/drive syntax, reserved names, trailing characters, normalized collisions, and blank media type. Second, `ReportHistory` could append a PASS report after cleanup confirmation alone. It now requires confirmed cleanup plus explicit true values for exit-zero, policy confirmation, termination confirmation, artifact validity, and tenant/job authorization; synthetic negative subcases exercise each missing gate.

The traceability document and acceptance matrix now record these cases. The helper/test pair and full repository suite remain **NOT RUN**; this is static source/test-fixture review, not runtime verification. No Actions, provider, account, workload, spend, deployment, or merge. PR #3 remains draft/unmerged and PR #2 untouched.


## 2026-10-27 — Output-cap disposition precedence

Another static consistency pass found that `derive_disposition` checked timeout/cancellation/provider-error outcomes before the output-limit flags. A confirmed output cap breach could therefore be hidden by a concurrent timeout observation, despite the selected rule that cap overflow yields `LIMIT_EXCEEDED`. The reducer now checks contradiction first, preserves `NOT_STARTED` as rejection when there is no contradiction, then prioritizes an explicit cap breach before ordinary timeout/cancel/provider-error outcomes. A combined timeout-plus-output-truncation assertion and matrix case OUT-02 were added.

The exact checked-in tests and full repository suite remain **NOT RUN**. This is static source/test-fixture review only; no Actions, provider, account, workload, spend, deployment, or merge. PR #3 remains draft/unmerged; PR #2 remains untouched.


## Follow-on static audit — malformed evidence types (2026-10-27)
A PASS-gate review found that truthy non-boolean values (for example, `"false"` or integer `1`) could satisfy Python's prior `all(...)` check. The helper now requires identity with literal `True` for PASS gates and for timeout/cancel termination confirmation. Added `test_malformed_truthy_gate_values_never_produce_pass`, matrix case LC-15, and a traceability update. The lifecycle test module contains 23 test methods. Exact checked-in tests and full repository suite remain NOT RUN.


## Follow-on artifact-release gate review — 2026-10-27
Static review found that artifact release authorization also relied on truthiness for digest, job-association, and tenant-authorization flags. It now requires literal boolean `True` for all three flags; added a synthetic negative test and acceptance case ART-SEM-02. The lifecycle test module contains 24 test methods. This change is not test-executed; exact checked-in helper/test pair and full repository suite remain NOT RUN.


## Master workflow continuity update — 2026-10-27
The owner's research-backed operating workflow has been summarized into the final section of `AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md`, preserving the existing project specifications as higher authority. It records repo-first verification, coherent risk-proportionate passes, reuse-first research, bounded three-AI roles, product/security discipline, honest test reporting, owner-control/$0 constraints, and durable handoffs. This is an operating-method addendum, not a product/architecture decision.

Current lifecycle state: strict literal-boolean PASS and artifact-release gates are implemented in the pure helper; negative synthetic tests and matrix rows LC-15 and ART-SEM-02 are recorded. The checked-in lifecycle module contains 24 test methods; exact checked-in tests and full suite remain NOT RUN.


## Complete chat handoff + workflow master saved — 2026-10-27
Added `AI_COLLAB/CHAT_HANDOFF_20261027.md` and `AI_COLLAB/MASTER_WORKFLOW_EFFICIENCY_RULES_20261027.md` to the working branch. The handoff directs future chats to verify current repository state, preserve the existing product/security/roadmap authority, respect owner constraints and the three-AI role split, continue the lifecycle audit, and never overclaim test execution. It tells future chats to ask the owner to repost the original workflow only if the durable file is inaccessible or its meaning is uncertain. Exact checked-in tests/full suite remain NOT RUN.
