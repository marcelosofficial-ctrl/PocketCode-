# PocketCode — Gemini review reconciliation

**Date:** 2026-10-29  
**Status:** Research-only reconciliation; no canonical acceptance change and no implementation authorization.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Review input:** Gemini's independent review returned in the coordinating chat.  
**Purpose:** Separate valid findings from stale references, unsupported claims, and issues already addressed in the research branch.

## Executive result

Gemini's overall `ACCEPT WITH REQUIRED CHANGES` is directionally useful, but its response is not fully reliable as a repository audit. It includes invented acceptance IDs and test IDs, reports a count discrepancy that was already corrected in the branch it was asked to review, and overstates some source claims. The actionable semantic gap around collector integrity is now clarified in the research-only adapter envelope. The policy-race concern is also addressed more explicitly there. Canonical product documents remain untouched.

No tests were run, no provider was selected, and no hosted execution or security behavior was verified.

## Finding-by-finding disposition

### G1 — Raw exit fact versus verdict when collection is degraded

**Disposition: VALID GAP; RESEARCH SPEC CLARIFICATION COMMITTED.**

The canonical contract already says a success requires exit code zero and a complete provider result, and the adapter envelope already models per-stream states including `PARTIAL_FAILURE` and `UNAVAILABLE`. However, the interaction between degraded required output collection and verdict projection was not explicit enough in the decision table.

The adapter envelope now states that:
- trusted child exit facts remain preserved as observed facts;
- a required stream that is unavailable or partially collected prevents an otherwise zero exit from being projected as PASS;
- the result must expose collection state/reason and remain INCOMPLETE (or a justified specific non-success disposition);
- artifact release remains denied when required evidence/integrity gates are unresolved;
- collector failure is not a cleanup status and must not be mislabeled as `cleanup_state`;
- runtime-enforced truncation and UI/report display truncation must remain distinct.

This is a research-document clarification, not a canonical contract amendment. Gemini's suggested `CLEANUP_FAILED` for a collector problem is not accepted: collection and cleanup are separate evidence dimensions.

### G2 — Synchronous policy barrier and policy-change race

**Disposition: VALID CONCERN; CORE CLARIFICATION ALREADY COMMITTED BEFORE THIS REVIEW RESPONSE.**

The adapter envelope was updated in commit `ca360f36` to say that a read-then-dispatch sequence alone does not close a time-of-check/time-of-use race. A real boundary must bind an attempt to an immutable policy revision or provide an atomic/conditional dispatch guarantee that rejects a changed revision. If neither is available, the policy barrier remains unproven and the boundary is not acceptable for untrusted code.

The review correctly identifies a possible danger from asynchronous policy propagation, but the cited Daytona behavior and any provider-specific guarantees were not independently established by this reconciliation. No provider has been selected. The correct requirement is provider-neutral: no untrusted process launch until enforcement of the required policy is authoritatively established, with a mechanism that closes the race; a mock policy read alone is not proof.

### G3 — Supplement test count and invented IDs

**Disposition: REVIEW CLAIM IS STALE/INCORRECT; COUNT ALREADY CORRECTED; TRACEABILITY CLAIM NOT SUPPORTED.**

The current supplement states **14 proposed supplementary test cases**, and its table contains 14 rows:
- SUP-UX-01..02 (2)
- SUP-REPORT-01..03 (3)
- SUP-RUN-01..04 (4)
- SUP-FILE-01..02 (2)
- SUP-SEC-01 (1)
- SUP-REC-01 (1)
- SUP-GOV-01 (1)

Total: 14. The count was corrected in commit `94f165d3`. The actual IDs use the `SUP-...` prefixes shown above, not `SUPP-01` through `SUPP-14`. The repository copy reviewed here does not contain the claimed header statement “12 supplementary test cases.”

Gemini's coverage table also introduces `ACC-MOB-01`, `ACC-SEC-02`, `ACC-OUT-03`, `ACC-REL-01`, and `ACC-COST-01`. These are **not canonical IDs** in `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`; canonical criteria remain LOOP-01..14 and CASE-01..16. Do not add these invented aliases or remap the original IDs. The existing coverage audit already records the relevant gaps using canonical IDs.

### G4 — Artifact release-time validation

**Disposition: PARTLY VALID; REQUIREMENT NEEDS MORE PRECISE BOUNDARY DEFINITION.**

The semantic decision note already says a historical report must not be silently changed and that artifact release must be recomputed at the release boundary from current trusted evidence and authorization. The adapter envelope also says release is not authorized by a caller-supplied `artifact_release_allowed` flag and requires stored-byte integrity, job association, tenant authorization, and cleanup requirements.

The adapter envelope has now been refined to require release-time validation of the artifact's safe normalized path/name, allowed media type, size/count limits, stored-byte integrity, job/attempt/tenant association, and current authorization at the actual export/download boundary. A new proposed FAKE-17 regression denies/quarantines export despite historical PASS when current validation or authorization fails. Those checks are distinct from a historical PASS verdict.

Gemini's example of scanning for a token newly flagged by a scanner is plausible, but “real-time secret scanning” is not automatically the only or best control. Secret scanning/redaction policy, false-positive handling, and whether an artifact is blocked or quarantined need a deliberate decision. Keep this as an open release-policy detail rather than claiming a scanner is already selected or verified.

## Coverage and terminology corrections

- `SUP-RUN-04` already explicitly distinguishes runtime-enforced caps from report-display truncation and includes a collector-failure fixture where possible. The envelope now makes the verdict consequence explicit as well.
- `SUP-REC-01` already calls for a lost-acknowledgement fault injection, authoritative lookup, at most one automatic dispatch, UNKNOWN remaining unknown, and reconnect recovery. These remain proposed and NOT RUN.
- `LOOP-14` is the canonical zero-cost gate; `SUP-GOV-01` supplies a proposed governance test. No test has been executed.
- The canonical acceptance document remains the authority. The supplement is additive and does not replace any LOOP or CASE criterion.
- A phone comparator cannot prove hosted isolation, egress blocking, process termination, resource enforcement, provider-side policy synchronization, or durable storage semantics.

## Evidence checked

Fetched the current branch versions of:
- `PRODUCT/EXECUTION_CONTRACT.md` — blob `3861e51ae4f9e45a263b677402f26c41b240959d` (unchanged).
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` — blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338` (unchanged).
- `AI_COLLAB/CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md` — blob `08265fcf91339dbdb08f518e3988fd661301bd56`.
- `AI_COLLAB/TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md` — blob `ab7f92c16ed89fb1bbd29991d9e5bdc09f45d594`.
- `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md` — blob `d7715e9095117c08ed4ad909d13a24ba1564fa1a`.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` — updated to blob `ffbf9dd600e9fad43990cdd39c68fab5c8adf392`.
- `AI_COLLAB/GEMINI_INDEPENDENT_REVIEW_PACKET_20261029.md` — blob `6ca6d2960dd1144a66e77be5ce7dcf06d16012c5`.

The prior policy-race clarification is commit `ca360f36ae78eb816b5d92c674254c1f4c55e7cd`; the supplementary test-count correction is commit `94f165d39ecb41c5143baff0bc50560336994c6c`. The collector-integrity/truncation clarification is commit `717a5061fb7ee170b7ef33cbe41b08f5c7218ac3`. The release-time artifact checklist and FAKE-17 case are commit `34e6aee275f50d4ad162e0d819ce6e0a8f488cf4`.

These checks establish document contents and revision identifiers only. They do not establish that code exists or tests pass.

## Next step

The research-only clarification pass is complete. The updated adapter proposal now covers degraded required collection, runtime-vs-display truncation, the policy-change race, and release-time artifact validation. Before touching canonical product documents, obtain explicit owner approval for any canonical-contract amendment. Next, compare these proposed rules against the existing PR #2/#3 source only if the relevant repository files can be inspected without changing those PRs; otherwise keep implementation conformance UNKNOWN. No canonical document was changed.
