# PocketCode — Gemini independent review packet

**Date:** 2026-10-29  
**Purpose:** Ask Gemini to act as an independent security/spec auditor for the current acceptance coverage and lifecycle/report semantics. This packet is a review request, not an implementation task.  
**Repository:** `marcelosofficial-ctrl/PocketCode-`  
**Branch under review:** `pocketcode-ai-workflow-director-research-2026-10-28`

## Copy/paste review request

You are the independent security/spec auditor for PocketCode. Review the linked documents as a set, prioritizing correctness, acceptance traceability, trust boundaries, and testability. Do not implement code, choose a provider, weaken acceptance, or infer runtime behavior that was not tested.

### Product context and constraints

PocketCode aims to provide a phone-first AI coding loop: prepare code and input → run in a controlled boundary → capture trustworthy evidence and artifacts → copy a bounded report to an AI → correct and rerun. A reliable manual copy/paste loop is sufficient for the first useful UX; automatic interception of other apps is not a requirement.

Constraints: $0 budget; user is phone-only for several months; local PC source/runtime/binary state is unavailable and must be treated as UNKNOWN. No provider/runtime has been selected. No account, billing enablement, workload, deployment, merge, or implementation is authorized. Canonical acceptance remains proposed and unchanged. PR #2 and PR #3 are separate drafts; do not conflate source-covered tests with tests actually run.

### Review these documents

1. Canonical acceptance, unchanged: [PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md)
2. Lifecycle/report matrix: [TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md](TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md)
3. Semantic decisions: [SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md](SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md)
4. Provider-neutral envelope/fake protocol: [ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md](ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md)
5. Coverage audit: [TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md](TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md)
6. Acceptance supplement: [CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md](CANONICAL_ACCEPTANCE_SUPPLEMENT_20261029.md)

### Specific review questions

**A. Semantic correctness**
- Are verdict (PASS/FAIL/INCOMPLETE), execution observation, job disposition, evidence quality, cleanup state, and artifact release separated consistently?
- Is “trusted, non-contradictory nonzero child exit => user verdict FAIL even if cleanup is UNKNOWN/FAILED; artifact release stays denied” consistent with canonical definitions? Identify any counterexample.
- Is the proposed handling of zero exit with missing gates, contradictory terminal events, timeout/cancellation with uncertain termination, runtime limit, and report-only truncation sound?
- Does any table accidentally allow a false PASS, erase a known failure, or treat a report field/program output as authoritative?

**B. State machine and idempotency**
- Are event identity, sequence ordering, duplicate replay, conflicting event ID, attempt binding, late evidence/report versioning, and release-time re-evaluation coherent?
- Does the proposed lost-ack recovery actually specify enough to prevent duplicate dispatch? What exact guarantees remain impossible without a durable atomic reservation/state lookup?
- Are CASE-11 (reconnect), CASE-13 (ambiguous retry), and CASE-16 (out-of-order runs) correctly distinguished? Propose minimum distinct tests, not duplicate names for the same behavior.

**C. Security boundary**
- Are tenant authorization, exact policy revision before dispatch, egress denial, resource enforcement, cleanup, artifact integrity/association, and secret absence assigned to evidence sources that could actually prove them?
- Which assertions are only model/unit-test properties versus live service properties?
- Does any design mistakenly trust client-supplied booleans, program output, browser timers, or mock results as authoritative?
- Are artifact release and report PASS correctly independent?

**D. Coverage accuracy**
- Check all 14 LOOP and 16 CASE IDs against the coverage audit and supplement. Identify false direct-coverage claims, missing cases, incorrect links, or accidental scope reduction.
- Ensure UI/report formatting tests are not presented as execution/security proof.
- Flag any unnecessary duplication or tests that cannot be executed until an architecture exists.

**E. Smallest safe next step**
- Recommend the smallest next documentation-only change that improves correctness or testability.
- Explicitly separate required-before-implementation decisions from choices that can wait until boundary/provider selection.
- Do not recommend provider selection merely to close a coverage-table gap.

### Required response format

Return one review with these sections:

1. **Verdict:** ACCEPT / ACCEPT WITH REQUIRED CHANGES / BLOCK.
2. **Critical findings:** each with severity, document/section, exact issue, consequence, and smallest fix.
3. **Coverage corrections:** exact canonical IDs and proposed direct/partial/gap label, with one-line rationale.
4. **Semantic decision check:** confirm or challenge the nonzero-exit/uncertain-cleanup rule and explain why.
5. **Implementation blockers vs deferrable decisions:** explicit lists.
6. **Minimal next change:** documentation-only recommendation.
7. **Evidence limits:** what you reviewed versus anything you actually executed. Do not claim tests passed unless you ran them and report the exact environment/command.

Be adversarial but precise. Separate definite defects from architecture-dependent questions. Cite file paths and section headings. Do not invent code, test results, providers, or hidden repository facts.

## ChatGPT coordination notes

This review is intended for Gemini to return to the PocketCode coordinating chat. ChatGPT should reconcile the response against repository evidence and Claude's implementation perspective. Disagreement should be recorded with evidence and disposition; do not silently overwrite canonical acceptance or treat Gemini's report as execution evidence.

## Evidence and authorization status

- Review packet only; no implementation or tests.
- No provider/runtime selected.
- No workload, account, billing change, merge, or deployment.
- Canonical acceptance and PR #2/#3 remain untouched.
