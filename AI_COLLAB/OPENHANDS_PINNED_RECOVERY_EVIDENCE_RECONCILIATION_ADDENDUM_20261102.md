
# OpenHands Pinned Recovery Evidence Reconciliation Addendum

**Date:** 2026-11-02  
**Review target:** OpenHands/software-agent-sdk at 98849457621881ae2414719b82b8bc1cf535b4ab  
**Project continuity branch:** pocketcode-execution-boundary-crosswalk-2026-11-01  
**Review type:** source and repository-history inspection; no upstream test execution

This is an additive correction to the OpenHands crash/recovery sections in OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md and the current new-chat handoff. It does not rewrite their historical record. Where this addendum conflicts with earlier tentative language, use this newer evidence reconciliation while retaining the original review trail.

No OpenHands source or tests were changed or run. No PocketCode source, tests, schema, canonical acceptance IDs, owner decisions, PRs or main-branch files were changed. PR #2 and PR #3 remain untouched. No provider workload, Actions run, installation, merge, deployment, host operation or spending occurred.

---

## 1. Executive verdict

| Gemini item | Reconciled verdict | Qualification |
|---|---|---|
| A/C. Multiple unmatched actions at startup | **CONFIRMED SOURCE-LEVEL DEFECT** | Only the first unmatched action receives a recovery error. A later action chain can be detached from the active ancestry. Full multi-action crash regression remains NOT RUN. |
| B. Stale observation suppression | **CONFIRMED SOURCE-LEVEL BRANCH-SCOPE DEFECT PATH** | Supported navigation can put the original action back on the active branch while its old observation remains on an abandoned branch. Recovery scans the full log, while pending-action detection scans the active branch. Provider-generated cross-response ID reuse is not needed. Full crash/restart reproduction remains NOT RUN. |
| D. PAUSED startup recovery | **CONFIRMED NARROW RACE / NOT CONFIRMED IN THE TOOL-ALREADY-RUNNING CASE** | Ordinary /pause while a tool is executing waits for that step and its observation. But pause can complete while the agent's LLM request is in flight; the returned tool-call response is dispatched without a PAUSED recheck. A crash during that newly dispatched tool leaves PAUSED + unmatched action, and startup recovery skips it. Full deterministic race test remains NOT RUN. |
| E. Recovery wording / EventLog durability | **WORDING QUALIFICATION CONFIRMED; POWER-LOSS DURABILITY UNPROVEN** | Missing result persistence does not prove no external side effect. Gemini's claim that there is no file fsync is incorrect: local string writes flush and fsync the temporary file before replace. Parent-directory fsync was not found, so rename durability after power loss is not established. |
| F31. Local zero-cost test | **LOCAL STUB ROUTE DOCUMENTED; MINIMAL STANDALONE ENTRYPOINT UNRESOLVED** | F31 uses local llm-stub endpoints for the crash scenario. The larger setup invokes the DeepSeek preset; the preset's dispensability in a reduced standalone harness is plausible but not proven by the current recipe. Do not accept the proposed mock/stub-model configuration without source or executable-test evidence. |
| Historical fixes | **RECONCILED** | #2298/#2300, #3045/#3063 and #4591/#4932 are merged fixes. #6289/#6290 remains a separate open issue/PR at this check. |

All “confirmed” labels mean confirmed by source topology and/or existing test evidence, not that ChatGPT executed upstream tests or independently observed a real provider side effect.

---

## 2. A/C. Multi-action recovery loses part of the active ancestry

### 2.1 Source proof

Pinned source:

- response_dispatch.py, tool-call handling: https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/agent/response_dispatch.py#L160-L255
- agent.py, async action batch preparation/emission: https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/agent/agent.py#L228-L385
- state.py, tree stamping and append: https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/conversation/state.py#L322-L365
- event_service.py, startup recovery: https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-agent-server/openhands/agent_server/event_service.py#L1424-L1468

The response dispatcher converts every tool call in one LLM response to an ActionEvent in response order before calling the batch executor. State append stamps each new event to the current active leaf and advances the leaf. The action records therefore form a parent chain for a multi-call response.

The async batch path executes the tool calls concurrently, waits for the batch, and emits results in original action order. A crash during execution can therefore leave every ActionEvent persisted while none of that batch's ObservationEvents has yet been emitted.

Startup recovery calls ConversationState.get_unmatched_actions(state.events), but selects only unmatched_actions[0]. It emits at most one AgentErrorEvent, with parent_id=first_action.id. That creates a branch from the first action and makes that new error the leaf. Later action descendants are no longer on the active ancestry.

### 2.2 Three-action example

Assume the response contains A1, A2, A3, and the state tree is:

    P -> A1 -> A2 -> A3
                      ^ current leaf

A crash occurs after the three action events have been persisted but before any result event is emitted.

Current recovery:

    P -> A1 -> E1
         |
         +-> A2 -> A3       (now outside active ancestry)

The resumed agent receives the active branch, not all EventLog records. A2 and A3 are therefore absent from resumed model history. This is not just “one error per action” coverage: the parent topology must be correct.

### 2.3 Candidate ordering for Claude to challenge

Gemini's reverse-result order proposal (E3, E2, E1) can preserve the action ancestry, but it reverses the result order relative to the original tool-call batch. The pinned _ActionBatch.emit() deliberately emits results in original action order.

For one contiguous batch A1 -> A2 -> A3, a candidate that preserves both ancestry and result order is:

1. Append E1 first, explicitly parented to A3, the last action node in the batch.
2. Append E2 as the child of E1 (normal active-leaf stamping).
3. Append E3 as the child of E2.

Resulting chain:

    P -> A1 -> A2 -> A3 -> E1 -> E2 -> E3

This is a topology proposal, not an approved fix. It must be challenged for batch grouping, multiple LLM responses, branches, gaps in persisted actions, action/result provider ordering, and partial recovery writes. Do not mechanically anchor every unmatched action batch to the global last action if unmatched actions can span separate turns or branches.

### 2.4 Existing test boundary

Existing test: tests/agent_server/test_event_service.py::TestEventServiceStartWithRunningStatus::test_start_sets_error_status_when_running_from_disk.

The test uses one unmatched ActionEvent. It does not prove recovery of multiple action events, exact parent IDs, or final active ancestry.

Required future regression test (not executed):

- Create one scripted LLM response containing three parallel tool calls.
- Use local blocking tools and persist all three ActionEvents.
- Terminate the worker process after all tool actions are persisted and before observations are emitted.
- Restore through the real persistence/EventService path.
- Assert all three ActionEvents and their matching recovery results occur on the active ancestry.
- Assert each recovery result has the correct tool_call_id and the serialized model history preserves the original action/result order.
- Assert there are no unmatched actions left on the active branch.
- Include a crash during partial recovery emission to establish the next-start behavior.

---

## 3. B. Stale-observation suppression is a branch-scope mismatch

### 3.1 The provider-ID-reuse concern is not the only path

Gemini's initial qualification focused on whether a provider may reuse a tool_call_id across separate responses. The inspected OpenHands model stores the identifier as a plain string and does not impose a cross-turn uniqueness validator, but provider-wide uniqueness is not established by the inspected evidence.

That question is now secondary. A concrete route exists without asking a provider to reuse an identifier in a later response: the same stored ActionEvent can be made pending again by supported conversation-tree navigation.

### 3.2 Source proof

- LocalConversation.navigate_to(): https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/conversation/impl/local_conversation.py#L988-L1010 moves the HEAD to any existing event ID. It does not delete the old branch.
- ConversationState.active_branch(): https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/conversation/state.py#L322-L329 returns only the path to the active leaf.
- Agent._step() and Agent._astep(): https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/agent/agent.py#L749-L756 check unmatched actions on the active branch and execute them before asking the model for a new response.
- Startup recovery: https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-agent-server/openhands/agent_server/event_service.py#L1430-L1468 checks unmatched actions across the full state.events EventLog and searches that full log for a matching observation.
- Conversation tree regression test: https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/tests/sdk/conversation/local/test_conversation_tree.py#L117-L141, test_navigate_then_emit_creates_sibling_branch, proves that a navigated-away branch remains in the EventLog but is excluded from the active view.

The current pinned server also exposes remote navigation through EventService.navigate_to(), the conversation router and RemoteConversation.navigate_to(). The startup comment saying remote branching is unsupported because of #3749 is stale or at least too broad for the checked-in API. Distinguish concurrent multi-writer branching from the supported in-place navigation API; do not use that comment to dismiss abandoned branches.

### 3.3 Concrete lifecycle

Let A be one ActionEvent with event ID X and tool_call_id C. Its first execution emits O1 with action_id X and tool_call_id C.

1. Initial branch: ... -> A -> O1.
2. The user navigates HEAD back to A. O1 remains stored, but is now outside the active ancestry.
3. A later run checks get_unmatched_actions(active_branch()). O1 is absent from that branch, so A is pending and the agent re-executes the stored action record. The ActionEvent's original X/C identifiers are reused; no provider-generated cross-turn ID collision is required.
4. The tool begins a second execution. A crash happens before its second observation is persisted.
5. Startup recovery scans the full EventLog. The first observation O1 is still present and matches A by action_id X; consequently A does not appear in the full-log unmatched-action list. Recovery does not append an AgentErrorEvent for the in-flight second execution.
6. After resume, the active branch still excludes O1. The active-branch pending-action scan sees A as unmatched and can execute it again.

This is a source-confirmed mismatch between the full-log recovery predicate and active-branch replay predicate. The #3063 guard is a deliberate duplicate-result protection and should not be removed casually. The correction needs to determine which observation belongs to the currently active execution attempt/branch, while retaining the protection against duplicate recovery results.

### 3.4 Existing test boundary and required test

Existing test test_navigate_then_emit_creates_sibling_branch proves branch separation but not action replay or crash recovery. Existing EventService test test_start_skips_error_event_when_observation_already_exists tests a same-tool_call_id/different-action_id observation in the full log, but it does not put that observation on an abandoned branch.

Required future regression test (not executed):

- Create A and O1 through the real conversation event pipeline.
- Navigate to A and assert O1 is in the EventLog but not active_branch().
- Start a second execution of the pending A using a deterministic blocking local tool.
- Terminate the process after the side effect begins but before a second result event is persisted.
- Restore through EventService startup.
- Assert startup does not mistake O1 on the abandoned branch for the result of the second attempt.
- Assert the recovery record and subsequent active-branch model history are internally consistent.
- Assert the old O1 remains on its historical branch and is not deleted.
- Explicitly document that the external side effect of the killed execution is UNKNOWN, not “did not happen.”

---

## 4. D. PAUSED recovery: distinguish pause-during-tool from pause-during-LLM

### 4.1 The simple in-flight-tool scenario is not reachable through ordinary pause

Pinned LocalConversation.pause() at local_conversation.py:2807-2835 acquires the conversation state lock and sets PAUSED plus a PauseEvent. In the normal async conversation loop, the lock surrounds the agent step except for deliberately released I/O. The F05 documentation explicitly says that when /pause is requested during a blocking tool, the request returns only after the tool ends and its observation is recorded.

Evidence:

- tests/sdk/conversation/local/test_conversation_pause_functionality.py::test_pause_while_running_continuous_actions.
- .agents/skills/verify-agent-server/references/feature-map/F05-run-pause-interrupt.md, section F05.pause-tool-step: command completes, observation is present, then status is PAUSED. The pause route waits for the tool step.
- event_service.py:2108-2116: EventService delegates pause to LocalConversation.pause() in an executor and publishes the state after it returns.

Therefore Gemini's exact sequence “normal pause lands during an already executing blocking tool; status persists PAUSED before its result” is not supported by this lifecycle.

### 4.2 A different, reachable PAUSED race exists during LLM I/O

The qualification above does not falsify every PAUSED recovery gap.

- Agent._astep() at agent.py:1030-1042 deliberately releases the state lock while awaiting self.llm.agenerate(...).
- The lock is therefore available to the separate thread calling LocalConversation.pause(). It can set and persist PAUSED while the LLM request is still outstanding.
- Once the model returns, Agent._astep() classifies the response and dispatches TOOL_CALLS through _ahandle_tool_calls() at agent.py:1120-1144.
- The inspected path contains no execution-status recheck between receiving the LLM response and dispatching its tool calls.
- response_dispatch.py:203-250 creates and appends ActionEvents, then invokes _aexecute_actions(). Thus a tool can start after PAUSED has been persisted.
- If the process dies during that tool, the state remains PAUSED with an unmatched ActionEvent.
- Startup recovery at event_service.py:1424-1436 only enters the recovery block for RUNNING. It skips PAUSED.
- On a later explicit resume, the pending-action path uses the active branch and can re-execute the unmatched action.

This is a distinct, source-supported race. It is not the normal pause-while-tool-running test case. The source behavior is confirmed; a deterministic test for the entire race and restart sequence has not been run.

### 4.3 Interrupt remains distinct

LocalConversation.interrupt() cancels the tracked async run and sets a cancellation token. The CancelledError handler in LocalConversation.arun() calls _emit_orphaned_action_errors() before setting PAUSED and emitting InterruptEvent. This is not equivalent to normal pause and should remain a separate path in the state-transition matrix.

### 4.4 Required deterministic test (not executed)

- Use a scripted LLM that blocks inside acompletion/the equivalent async call.
- While the LLM call is blocked, call the normal pause API from a separate thread and assert the persisted state is PAUSED.
- Release the scripted model with a valid tool-call response.
- Observe whether the pinned agent dispatches the ActionEvent and starts a blocking local tool despite PAUSED.
- Terminate the process while that tool is blocked.
- Restore with EventService and assert startup skips the PAUSED state.
- Resume explicitly and observe whether the unmatched active-branch action is executed again.
- Keep separate tests for pause during an already executing tool and interrupt during a tool.

The test should assert exact status/event ordering and persistence, not merely in-memory final state.

---

## 5. E. Recovery wording and EventLog durability

### 5.1 Side-effect language

A persisted ActionEvent with no persisted observation establishes only that the coordinator did not record a result before interruption. It does not establish whether a local process, network request or external API side effect completed. Recovery text must not tell the user the tool definitely “did not complete” unless the tool itself provides a reliable reconciliation guarantee.

For a generic tool, the accurate outcome is UNKNOWN / NOT OBSERVED. Retry safety is a separate property and must not be inferred from an AgentErrorEvent.

### 5.2 Correct local write-path trace

Gemini's file-fsync statement was incorrect for the pinned local filesystem implementation.

- EventLog.append(): https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/conversation/event_store.py#L241-L300 serializes the event and passes its JSON string to the configured FileStore.
- LocalFileStore.write(): https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/io/local.py#L63-L76 sends string content through atomic_write_text().
- atomic_write_text(): https://github.com/OpenHands/software-agent-sdk/blob/98849457621881ae2414719b82b8bc1cf535b4ab/openhands-sdk/openhands/sdk/utils/files.py#L21-L45 writes to a temporary file in the same parent directory, calls file.flush(), calls os.fsync(file.fileno()), closes the file, then calls os.replace(temporary_path, path).
- The EventLog advances a sidecar length marker after updating the in-memory index. _advance_length_marker() deletes the previous marker before writing the new marker. On interruption, the implementation is designed to leave no marker rather than a stale marker claiming the wrong length; the count/rescan path is the fallback.

### 5.3 Durability classification

| Failure class | What source establishes | Verdict |
|---|---|---|
| Process termination | Temporary file content is flushed/fsynced and closed before atomic replace; an interrupted marker update has a fallback rescan path. | Strong process-crash design, but do not claim every multi-file state transition is transactionally atomic. |
| OS crash / kernel panic | File contents are fsynced before rename. No parent-directory fsync was found after os.replace(). | Full namespace/rename durability is not established. |
| Sudden power loss | No power-cut test or storage/hardware guarantee was inspected. | UNPROVEN; do not label a confirmed data-loss defect. |

The exact FileStore matters. This analysis is specifically the pinned local string-write path. It should not be generalized to every custom/remote FileStore implementation.

---

## 6. F31. Local zero-cost recovery test feasibility

Pinned reference: .agents/skills/verify-agent-server/references/feature-map/F31-persistence-and-limits.md, especially the setup/preconditions block and F31.crash-tool-call.

The documented setup creates local llm-stub services and configures the target conversation with an inline LLM endpoint at the local stub URL, a fake test API key, zero retries, and a local terminal tool running sleep 300. The documented crash case SIGKILLs the agent-server while the tool is active, restarts it, checks ERROR plus a matching AgentErrorEvent and zero ObservationEvents, then changes the local stub response to Finish and resumes.

Important qualifications:

1. The top-level F31 setup block includes control-agent-server llm preset deepseek, but the crash-test conversation's inline TOOL_AGENT points at the local qa-f31-tool stub.
2. The global DEEPSEEK_API_KEY precondition is explained by a separate F31 no-plaintext-at-rest test requiring one real model request; it is not evidence that the crash-tool-call conversation itself uses DeepSeek.
3. The current documented setup nevertheless invokes the preset, so the claim that it can be omitted from a reduced standalone harness has not been demonstrated by the documentation alone.
4. The exact local stub command is a documented server-fixture approach, not a proof that the scenario was executed by ChatGPT or that all prerequisites are optional.
5. Gemini's proposed LLM(model="mock/stub-model", api_key="mock-key") is not grounded in the inspected pinned test seam. A scripted TestLLM may be appropriate for a pure SDK-level test, but that is not interchangeable with proving the EventService startup path across a real process restart.

Verdict: **zero-cost local-stub testing is feasible in principle and already documented for the one-action F31 path**. The smallest standalone command sequence, exact dependency list, DeepSeek-preset omission, and an updated local-stub test covering PAUSED/multi-action/stale-branch scenarios remain unresolved. Do not run a provider workload to close them.

---

## 7. Historical upstream fixes: status and separation

Checked against the GitHub issue/PR records and the pinned source on 2026-11-02.

| Issue / PR | Current PR status | What was fixed | What it does not prove |
|---|---|---|---|
| #2298 / #2300: https://github.com/OpenHands/software-agent-sdk/pull/2300 | **Merged** 2026-03-04 | get_unmatched_actions() treats AgentErrorEvent as a result by tool_call_id, preventing the historical crash-recovery error from being followed by an implicit re-execution that emits a second observation. Regression coverage was added. | Does not help when recovery emits no AgentErrorEvent because a stale observation on another branch suppresses it. |
| #3045 / #3063: https://github.com/OpenHands/software-agent-sdk/pull/3063 | **Merged** 2026-05-05 | Startup recovery skips synthesizing an error if an ObservationBaseEvent with the action's tool_call_id already exists. Test: test_start_skips_error_event_when_observation_already_exists. | Does not establish that the observation belongs to the active branch or the latest execution attempt. |
| #4591 / #4932: https://github.com/OpenHands/software-agent-sdk/pull/4932 | **Merged** 2026-09-23 | ToolCallMatchingProperty.manipulation_indices() tolerates orphan observation-like events by using set discard semantics; separate enforcement handles duplicate/orphan cleanup. Regression test: test_orphaned_observation_does_not_restrict_indices. | Does not make active-branch/full-log recovery predicates consistent and does not prove all incremental view paths enforce uniqueness before every consumer reads. |
| #6289 / #6290: https://github.com/OpenHands/software-agent-sdk/pull/6290 | **OPEN / UNMERGED** at check | Proposed result events for calls discarded after FinishTool, preventing them from remaining unmatched and running on a later turn. Proposed regression: test_tool_call_after_finish_never_runs_on_a_later_turn. | This fix is not part of pinned commit 9884945 and is separate from startup recovery. |

Do not regress or relabel #2298 as open. Preserve the distinction between the three merged fixes and #6289/#6290.

---

## 8. Updated review priorities and Claude challenge

The next independent pass should be implementation-level and narrowly targeted. Do not repeat the broad product review, change PocketCode direction, freeze schemas, remap acceptance IDs, or implement anything.

### Copy-ready prompt for Claude

> We need a targeted implementation-level challenge of Gemini's six-point OpenHands recovery audit. Review the pinned repository OpenHands/software-agent-sdk at commit 98849457621881ae2414719b82b8bc1cf535b4ab. ChatGPT independently inspected the source and prepared AI_COLLAB/OPENHANDS_PINNED_RECOVERY_EVIDENCE_RECONCILIATION_ADDENDUM_20261102.md in the PocketCode continuity repository.
>
> Do not modify source, tests, branches, issues, or pull requests. Do not run a provider workload. Do not make PocketCode product decisions or alter acceptance IDs. Return evidence only.
>
> Challenge these exact claims:
>
> 1. **Multi-action recovery:** prove the parent chain for a 3-action response, the fact that all ActionEvents are emitted before parallel execution completes, and the final active ancestry after current startup recovery emits only one error for the first unmatched action. Evaluate the candidate result ordering that appends E1, E2, E3 in original tool-call order, with E1 explicitly parented to A3 and later errors chained after it. Determine whether this is valid for one batch, what grouping metadata is required for multiple responses/branches, whether provider history ordering stays correct, and how partial recovery crashes behave. Compare against Gemini's reverse-order proposal.
> 2. **Stale observation / branches:** validate or falsify this concrete sequence: A with observation O1; navigate HEAD back to A; O1 stays on an abandoned branch; a run re-executes the same stored A; process crashes before the second result; startup full-log matching treats O1 as satisfying A; resumed active-branch matching still sees A as pending. Reconcile the deliberate #3063 guard and the actual #3749 in-place remote navigation support. Do not substitute a synthetic new tool_call_id collision for the branch scenario.
> 3. **PAUSED race:** verify whether normal pause can land while Agent._astep() awaits llm.agenerate(), and whether the returned tool-call response is dispatched without checking PAUSED. Confirm whether a tool can therefore begin after PAUSED is persisted, and whether startup then skips it because recovery only handles RUNNING. Keep this distinct from ordinary pause while a tool is already executing, which F05 says waits for the observation, and from interrupt, which cancels and emits orphan errors.
> 4. **Recovery semantics and durability:** confirm missing observation means outcome UNKNOWN, not proof of no side effect. Verify the full local FileStore write path, including flush/fsync of the temporary file, close, replace, and any parent-directory fsync. Separate process kill, OS crash, and sudden power loss; do not infer a power-loss defect solely from the missing directory fsync.
> 5. **F31:** produce the smallest exact zero-cost local test entrypoint using a local LLM stub and local blocking tool to exercise the EventService persistence/restore path. Separate the global DeepSeek preset/API-key setup from the crash-tool-call conversation's explicit local stub config. Prove whether the preset can be omitted, or label it unresolved. Do not use a real provider.
> 6. **Historical boundaries:** keep #2298/#2300, #3045/#3063 and #4591/#4932 classified as merged historical fixes. Keep #6289/#6290 separate and unmerged unless fresh GitHub evidence proves otherwise. Do not regress #2298's fixed classification.
>
> For every item, return exact pinned file paths, symbols, line ranges, relevant test names, and the commit SHA. Separate SOURCE PROOF, TEST PROOF, INFERENCE and NOT RUN. Where you disagree with the addendum, show the exact source or test that falsifies it. In particular, do not overstate whether a combined branch/crash scenario is fully proven until an integration test covers it.
>
> No code changes or PR work. The objective is to close the remaining evidence gaps so ChatGPT can reconcile your implementation-level challenge with Gemini and produce one final consolidated verdict.

### ChatGPT next steps after Claude responds

1. Reconcile Claude against this addendum, Gemini's response and the exact pinned source. Resolve disagreements by evidence strength, not reviewer seniority or report length.
2. If source-level claims survive, produce the final test matrix for the three high-value scenarios: (a) 3+ parallel actions and crash recovery; (b) old observation on abandoned branch and crash during replay; (c) pause during LLM completion followed by tool dispatch and crash.
3. Keep EventLog process-crash testing separate from OS/power-loss durability claims.
4. Preserve existing documents and add a concise final verdict/handoff once the Claude challenge is available. Do not modify PocketCode source/tests or any canonical acceptance record as part of the OpenHands investigation.
5. Continue fixed-task PocketCode local-execution feasibility research independently. Do not select a runtime/provider from this OpenHands review.
6. RevDev machine/source/binary/runtime/watcher/queue/publication state remains UNKNOWN until the user's PC returns and fresh evidence is available.

---

## 9. Operating constraints retained

- PocketCode remains in discovery/product definition; execution location is not selected.
- RevDev and PocketCode remain related through the shared execution/evidence/continuity principles but retain separate authority, host, queue and acceptance boundaries.
- Phone-only coordination; no PC evidence can be refreshed from memory.
- Budget $0. No paid provider, workload, Actions, install, source/test change, queue mutation, mission replay, PR modification, merge, deployment or host operation without explicit owner authorization.
- PR #2 and PR #3 remain untouched.
- Documentation-only continuity updates on this isolated research branch are permitted.
- Parsed != policy-approved != authorized. Preserve execution outcome, job/coordination disposition, evidence persistence, publication, artifact release, transfer and user-facing verdict as separate concepts.
- The shared 18 fixtures remain provisional and do not replace canonical acceptance.
- Do not invent missing evidence, source refs, test results, or owner decisions.
