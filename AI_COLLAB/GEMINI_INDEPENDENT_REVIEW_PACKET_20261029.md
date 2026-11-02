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


### EventLog marker crash boundaries — 2026-11-02

One further source detail for your challenge: EventLog append writes the event JSON, updates in-memory maps/length, then advances the length marker. Marker advancement deletes the previous marker before writing the new one. LocalFileStore string writes use atomic_write_text. Please challenge whether the proposed kill points cover these transitions and whether fresh EventLog construction/index scan handles a missing marker correctly. Do not conflate process-kill survival with power-loss durability. Existing F31 integration recipe and mocked unit tests are already mapped in the plan; focus on the remaining parent_id/active-ancestry proof.


### Higher-priority OpenHands recovery challenges added — 2026-11-02

Please review the newly added Section 13 of `OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md`. Two important source facts materially change the priority:

1. Multi-tool responses are supported. `event/base.py` lines 181–200 describes multiple ActionEvents from parallel tool calls. `response_dispatch.py` lines 224–255 emits each ActionEvent before `_aexecute_actions`; `agent.py` lines 695–716 and `parallel_executor.py` lines 128–191 run the complete batch, and `_ActionBatch.emit` emits observations only after batch completion. `get_unmatched_actions` returns all unmatched actions, but startup recovery chooses only `[0]`. Contrast this with `LocalConversation._emit_orphaned_action_errors` lines 2777–2805, which loops over all active-branch orphans after an interrupt. Challenge whether startup recovery leaves a normal multi-tool batch incomplete or cuts later tool calls off the active branch. Please inspect actual parent ordering and model reconstruction before judging.

2. Navigation/re-root is supported and leaves abandoned events in the full log. `local_conversation.py` lines 988–1011, `remote_conversation.py` lines 1914–1943, EventService lines 2358–2372, and F10 feature map lines 34–38/295–328 establish this. Yet startup recovery scans full log and suppresses recovery when any ObservationBaseEvent matches tool_call_id. Challenge whether a prior-branch observation can suppress recovery for an action pending on the current branch. Reconcile this with the code comment that remote branching is unsupported (#3749); do not equate unsupported concurrent branching with supported navigate/re-root.

F31's crash-tool-call scenario creates an inline agent using local `llm-stub` (`openai/qa-stub`, placeholder key, local base_url); the wider F31 setup also calls `llm preset deepseek` for the broader family. Please verify whether the isolated crash subfeature can be run without a DeepSeek key/provider call. Do not claim the whole F31 suite is provider-free.

New plan cases FI-15..18 cover multi-action crash recovery; FI-19..22 cover navigation/rewind suppression. Treat them as test proposals, not executed evidence. Do not modify source/tests or make PocketCode owner decisions.


### Recovery error wording and side-effect ambiguity — 2026-11-02

Startup recovery's AgentErrorEvent text says “The tool execution was interrupted and did not complete” (`event_service.py` lines 1458–1462), with INTERNAL / retryable=False classification. Challenge whether that statement is supportable. A multi-tool batch can have one external side effect complete while another tool remains blocked; because results are emitted only after the full batch returns, a crash may leave completed effects without observations. Please assess whether the error text overstates what is known and what a more accurate evidence/outcome representation would be. Distinguish no persisted result from no side effect. Do not equate retryable=False with proof of non-execution.


### Important citation contradiction: OpenHands issue #3749 — 2026-11-02

The recovery comment cites #3749 for “remote branching is unsupported.” I fetched issue #3749 itself: it is CLOSED and titled “[Feature] Conversation history tree: agent-server HTTP exposure (fork/navigate/schema) (3/3)”. Its body specifies the HTTP `/navigate` route and acceptance that `/events/search` still returns all branches after navigation. This appears inconsistent with the recovery comment and the pinned `navigate_to` source/F10 feature map. Please inspect the issue's linked PR/merge commit and clarify whether “remote branching unsupported” means only concurrent/multi-writer branching, while in-place navigate/re-root is supported. Explicitly distinguish concurrency, forked conversations and abandoned branches within one conversation. Do not let the comment citation override the actual route/API behavior.


Follow-up on #3749: the SDK foundation PR's description says RemoteConversation navigation was initially NotImplemented until the agent-server HTTP surface. The #3749 agent-server PR description explicitly adds POST `/api/conversations/{id}/navigate` and wires `RemoteConversation.navigate_to()` to that endpoint. Thus the pinned revision's remote navigate/re-root is supported; the recovery comment's “remote branching unsupported” cannot mean navigate is unavailable. Please determine whether it instead means concurrent/multi-writer branching and whether that narrower invariant prevents stale-observation suppression. The abandoned branch remains on disk by design.


### Historical issue #2298 context: avoid a false positive

OpenHands issue #2298 is CLOSED and documents the earlier duplicate-execution bug caused by get_unmatched_actions not matching AgentErrorEvent. The pinned code now matches AgentErrorEvent by tool_call_id (`state.py` lines 713–752), and the SDK tests cover it. Do not claim that historical bug remains.

Our distinct concern is that startup recovery calls get_unmatched_actions on the full EventLog, while normal pending-action detection uses active_branch (`agent.py` lines 747–756). After supported navigate/re-root, a matching observation can remain on an abandoned branch. It may suppress startup recovery even though the action is still pending on the active branch. Please falsify the exact sequence in crash-window plan Section 16: A→O, navigate HEAD back to A, send a new message, re-execute pending A, crash before new result persistence, restart, then compare full-log recovery matching with active-branch pending-action matching. Establish whether RUNNING status and the exact lifecycle make this reachable, and whether user intent makes replay expected. The existing #2298 fix does not automatically resolve this branch-context mismatch.


Direct test evidence for navigation: pinned `tests/sdk/conversation/local/test_conversation_tree.py`, blob `9086af335ea59d267939ba0302d524f0594df3c1`, lines 117–141, `test_navigate_then_emit_creates_sibling_branch` explicitly creates root→A1→A2, navigates to root, appends B1, and asserts A1/A2 remain in EventLog but are absent from active view while A1/B1 are siblings. Please incorporate this concrete test, then challenge the remaining RUNNING/recovery lifecycle and same-tool-call observation suppression. It proves abandoned events persist, not by itself that FI-19 is fully reachable.

### New upstream issue/fix reconciliation — 2026-11-02

Before concluding the OpenHands recovery review, inspect these upstream issue/PR histories and compare them to the exact pinned commit 98849457621881ae2414719b82b8bc1cf535b4ab:

- Issue #3045 was closed by PR #3063 (merged 2026-05-05, merge commit b6c63d0). The PR says restart recovery now skips synthesizing AgentErrorEvent if an ObservationBaseEvent already exists for the unmatched action's tool_call_id. Determine whether the pinned event_service contains this guard and its exact test. This qualifies the earlier full-log suppression concern: an already-present matching observation is intentionally treated as a result marker. Still assess active-branch ancestry and pending-action semantics.
- Issue #4591 was closed by PR #4932 (merged 2026-09-23, merge commit dd8d9f6). The SDK fix makes manipulation-index calculation tolerate orphan observations whose ActionEvent is absent from the view, while preserving duplicate-result enforcement through ObservationUniquenessProperty. Verify the pinned source includes the final merged change, not merely an intermediate PR head.
- PR #4932 review history notes a remaining raw incremental-view path where duplicate observations could reach serialization before a full enforcing rebuild. Challenge this independently; do not assume full-rebuild enforcement covers incremental appends.
- Issue #6289 was opened 2026-10-28 against SDK 1.58.2 / main commit 46b1fa5. It reports [FinishTool, tool] leaving the later ActionEvent unmatched and executing it on the next user turn. Determine whether the pinned commit predates or includes the behavior. Keep this separate from crash recovery and multi-action batch crash analysis.

Required distinctions:
1. Observation already present before restart recovery (expected suppression under #3063).
2. Original tool completes after recovery has already appended AgentErrorEvent (late-result duplicate path).
3. AgentErrorEvent survives in a reconstructed view after its ActionEvent is absent (orphan observation, #4932).
4. Duplicate observation appended through a live incremental view before enforcement/rebuild.
5. Post-Finish tool call left unmatched and executed on a later turn (#6289).
6. Active-branch pending-action detection after navigation/rewind versus full-log duplicate suppression.

Please return exact pinned source/test evidence for each, plus whether the issue/fix is present at the pinned revision. State which are fixed, remaining, post-pin, or unresolved. Do not run or change upstream source/tests. Do not make PocketCode owner decisions or change canonical acceptance IDs.

### #6289 linked PR status update — 2026-11-02

Issue #6289 links to PR #6290, which is OPEN/unmerged at the time of this review. Its proposed change emits one AgentErrorEvent for each tool call truncated after FinishTool, so discarded calls do not remain pending and execute on a later turn. It includes a two-turn regression test and sync/async coverage. The author reports local test results, but ChatGPT has not run or independently verified them.

Please inspect PR #6290's diff/test design and verify whether pinned commit 988494... contains the unfixed behavior. Do not describe PR #6290 as merged or as a fix already present in the pinned source.
