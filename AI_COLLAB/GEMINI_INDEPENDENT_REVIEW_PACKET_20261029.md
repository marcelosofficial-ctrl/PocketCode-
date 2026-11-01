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


## Additional source-level challenge topics — 2026-11-01

When resuming this independent review, challenge the following without proposing schema changes:

1. **Codex ACL concerns:** inspect the exact pinned Codex ACL/setup source and test whether target-only deny ACEs can be bypassed through parent FILE_DELETE_CHILD, whether any-overlap deny detection is sufficient, and whether Ok(false) masks ACL API failures. Distinguish code defect from Windows runtime exploit.
2. **srt WFP:** independently verify current-main partial-filter status logic, IPv4-only readiness probing, issue #723 reproduction scope, open PR #716 repair semantics, and the explicitly unfenced ICMP/DNS Client service path. Do not describe PR #716 as merged or as containing the separate IPv6 probe branch.
3. **OpenHands EventLog:** challenge the event-file append then separate base_state HEAD update crash window. Determine whether the current restore logic can leave an appended event inactive after a crash. This is a hypothesis until fault-injection proves it.
4. **OpenHands lease:** confirm guarded_write holds the lease lock across generation check and disk write, and state precisely what it does not fence (external side effects).
5. **Happy pairing:** validate the Android client crypto/transcript and human confirmation, but do not infer server replay/expiry/rate-limit guarantees from FakeDaemon tests. Locate daemon-side route source or classify server guarantees UNKNOWN.
6. **Product fit:** explain whether any pattern materially improves PocketCode's remote-first, $0, phone-first architecture without creating a mobile terminal, selecting a provider, or changing owner decisions.

For each finding provide pinned repo SHA, file path, symbol/line range, observed behavior, inference, unknowns, and a concrete falsification test. Keep this review documentation-only.


### OpenHands crash-window falsification plan — 2026-11-02

ChatGPT has prepared [OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md](OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md). Please independently challenge its test validity and assumptions, especially:
- whether the proposed kill hooks truly occur after durable event-file commit but before leaf assignment/save;
- whether the restore path accepts a still-existing old leaf and therefore leaves the new event outside active ancestry;
- whether EventLog index/marker refresh could make E1 discoverable even when the active HEAD remains E0;
- whether the base_state atomic-write test correctly distinguishes pre-replace and post-replace crashes;
- whether duplicate-ID retry, changed-payload conflict, delayed replay and branch ancestry cases are sufficient without claiming provider idempotency;
- whether the lease-takeover test correctly models lock scope and avoids claiming external side-effect fencing.

The plan is a future falsification specification only. Do not report it as executed, do not create acceptance IDs or schema changes, and keep source/environment-specific conclusions separate from PocketCode owner decisions.


### OpenHands agent-server recovery path discovered — 2026-11-02

A further pinned-source read found that the agent-server explicitly handles the stale-HEAD interrupted-tool case. At `openhands-agent-server/openhands/agent_server/event_service.py` lines 1424–1467, a restored RUNNING conversation is marked ERROR, the full event log is scanned for unmatched actions, and a non-retryable internal AgentErrorEvent is appended with parent_id=first_action.id if no ObservationBaseEvent exists for that tool_call_id. SDK state.py lines 268–320 show a still-existing stale leaf remains active; only a missing leaf is repaired.

Please challenge whether this recovery is sufficient and identify its gaps: RUNNING-status gate, first-unmatched-action selection, log-wide tool_call_id observation suppression (including a potentially non-active observation), multiple unmatched actions, and ambiguity after an external side effect but before observation persistence. The updated plan adds OH-HEAD-FI-09..14. Distinguish the SDK's non-atomic persistence boundary from the agent-server recovery behavior and from external side-effect outcomes. Do not treat the interruption error as proof that the side effect did not happen or as authorization to retry.


### Existing OpenHands crash-recovery tests to avoid duplicating — 2026-11-02

Pinned source review found existing coverage:
- `tests/agent_server/test_event_service.py` blob `fc6e589f71318ac36df92b72c1fd0225549d1436`, lines 2419–2678: RUNNING with unmatched action, no unmatched action, non-RUNNING skip, and observation suppression by tool_call_id despite different action_id. These are mocked-state unit tests; inspected assertions do not check error_event.parent_id or restored active ancestry.
- `tests/sdk/conversation/test_get_unmatched_actions.py` blob `35798b1bccb60b0976cf0785682ef17181e4450b`: helper matching by tool_call_id.
- Feature map F31 crash-tool-call, blob `5082730e1ba1d333daeaf321c21214ad4924cd12`, lines 191–220: documented SIGKILL integration scenario checks ERROR, one AgentErrorEvent, no ObservationEvent and resumed model delivery, but not parent_id/active ancestry; broad recipe preconditions include a DeepSeek key/model.

Please assess the smallest missing assertion/test rather than duplicating these cases. Priority: parent_id assertion plus a real LocalFileStore crash/restore test proving action → recovery error active ancestry. Then challenge log-wide observation suppression, multiple unmatched actions, non-RUNNING stale state, and external side-effect ambiguity. These sources are test/spec presence only; ChatGPT did not execute them.
