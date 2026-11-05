# PocketCode Chat Continuity and Multi-Chat Operating Protocol

**Created:** 2026-11-06  
**Purpose:** keep PocketCode resumable across months and hundreds of temporary ChatGPT conversations without relying on transcript memory or end-of-context handoffs.

## 1. Governing principle

GitHub is PocketCode's durable project memory. Every ChatGPT conversation is a replaceable worker. Preserve project state, tested facts, decisions, owner constraints, and next actions, not the full transcript. Never assume a new Free chat can recall every earlier chat.

PocketCode remains a distinct product and repository from RevDev. Reuse the continuity process, not implementation, runtime, schemas, clients, adapters, security boundaries or acceptance suites.

## 2. Boundaries are revisable

Do not turn temporary safeguards or old chat instructions into permanent limitations. The owner explicitly permits changing operating boundaries when evidence shows a benefit to PocketCode. Evaluate the product/security impact, reversibility, budget, affected acceptance contracts and verification path; record changed authority and remaining guardrails in GitHub. Routine implementation does not require repeated permission. The $0 default budget and genuinely reserved owner decisions remain in force until changed by the owner.

## 2. Three continuity layers

1. **Live entrypoint:** `AI_COLLAB/CHAT_START_HERE.md`. First file read by every new chat. It carries current branch, current product phase, active task, constraints, test evidence, and links to canonical documents.
2. **Append-only work log:** `AI_COLLAB/CHAT_WORK_LOG.md`. One short entry per meaningful pass, including unique pass key, changed paths, commit, tests and exact result, unknowns, and next action.
3. **Canonical detailed records:** existing project requirements, architecture, test contracts, research, decisions, source, reports and release gates. The live entrypoint links to only the records needed for the current task.

Do not duplicate LOOP/CASE/D acceptance wording in handoffs. Canonical suite files remain the authority.

## 3. New-chat startup

1. Read `AI_COLLAB/CHAT_START_HERE.md`.
2. Fetch the live PocketCode branch, relevant PRs and current CI/check state.
3. Read only the task-specific source/docs linked by the entrypoint. Do not scan every historical handoff by default.
4. Verify what the prior chat actually changed. Separate a proposal, source change, executed test, external review and product/device result.
5. Continue the highest-value bounded task without repeating discovery or asking the owner to reconstruct history.
6. Keep $0 default budget, no provider/runtime decision, and all security boundaries intact.

## 4. Work-pass checkpoint

At the end of every meaningful pass:
- read back changed files and record exact commit/blob/path;
- record exact test command and output, or NOT RUN/BLOCKED;
- update `CHAT_START_HERE.md` if live state or next action changed;
- append one concise `CHAT_WORK_LOG.md` entry;
- state the next one to three actions.

Do not save long transcripts in the work log. Link the full audit or report. Use unique pass keys such as `PC-2026-11-06-P01`.

## 5. Rotation rule

Rotate before context exhaustion, never after it. Trigger a checkpoint after two or three meaningful passes, a source/test milestone, an owner decision, an independent AI review, a major research conclusion, or early signs of repetition/context strain. Do not use a guessed fixed message count: user messages and assistant replies both consume the conversation context and there is no fixed number of messages.

The owner should not need to say "create a handoff" at the 100% point. The assistant owns keeping the live entrypoint current and can provide a short new-chat prompt whenever rotation is useful.

## 6. Multi-chat coordination

- One lead writer per PocketCode branch/work item at a time.
- Other chats and AIs can perform read-only review; disjoint changes require explicit scope and later reconciliation.
- Re-fetch the current blob SHA before updating a file and read back after the update. Serialize writes to the same path/branch.
- Keep each task bounded: objective, non-goals, inputs, invariants, outputs, verification, stop conditions.
- Claude = lead developer/architecture reviewer; Gemini = co-developer and independent security/spec auditor; ChatGPT = continuity holder, evidence reconciler, acceptance architect and cross-project coordinator. The owner forwards reports manually.
- Never infer implementation from a commit count or documentation from a product test.

## 7. Evidence vocabulary

- **IMPLEMENTED:** source exists at a named commit.
- **TESTED:** named tests ran against named source and exact result is recorded.
- **VERIFIED:** an authoritative observation proves the stated property.
- **NOT RUN:** no execution evidence.
- **BLOCKED:** required environment/capability/permission/input is unavailable.
- **UNKNOWN:** evidence cannot distinguish possible states.
- **PROPOSED:** design only.

Keep advertised, documented, source-audited, test-executed and device-verified claims separate. An execution fact such as process exit is not automatically a PASS/FAIL verdict if evidence collection, teardown, artifact persistence or receipt construction degraded.

## 8. PocketCode product boundaries that must survive chat rotation

- Phone-first iOS + Android product; no PC requirement.
- $0 default budget; no paid provider, hosted runner, workload, account or subscription without a separate budget decision.
- No execution runtime/provider has been selected.
- Preserve explicit paste-to-context. No clipboard polling or intrusive overlays.
- Remote SSH/Tailscale and optional future cloud execution are adapters/research directions, not assumed MVP capabilities.
- Browser WASM/Pyodide/JSC may be light/trusted convenience paths only where appropriate. Stock Pyodide is not approved as a hostile-code sandbox.
- Execution, observation, immutable receipt, artifact, cleanup and AI-correction lineage remain distinct boundaries.
- No unsafe inference of success from missing evidence, timeout UI, stale receipt, lost process or degraded collector.
- Preserve PocketCode's own canonical LOOP/CASE/D suites; do not borrow RevDev's AEC/AWC/P8U/P0-D verdicts.

## 9. ChatGPT Project usage

Keep PocketCode chats inside a dedicated ChatGPT Project when available and add concise project instructions. Do not upload all research files. On Free, project file capacity is five files and automatic reference to previous project chats should not be assumed. GitHub's live entrypoint remains authoritative. Chat search is a lookup aid; export is a backup, not routine chat rotation.

## 10. OpenAI help facts checked 2026-11-06

The current Free Tier FAQ says context-full refers to the total current conversation content, including user and assistant messages; it is not a fixed message count and starting a new chat is the recommended response to a long conversation. ChatGPT Projects keep chats/files/instructions together. Sidebar search works on Free, including archived conversations. Data export is available on Free but may take up to seven days.

Official references:
- https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq
- https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- https://help.openai.com/en/articles/10056348-finding-your-chats-projects-and-files-in-chatgpt
- https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data

## 11. Bootstrap prompt

```text
Continue PocketCode from GitHub. First read AI_COLLAB/CHAT_START_HERE.md on branch pocketcode-ai-workflow-director-research-2026-10-28, then verify live branch/PR/CI state and read only the evidence needed for the active task. GitHub is durable project memory; this conversation is replaceable. Do not restart discovery or ask me to reconstruct a handoff. Continue the highest-value bounded task, implement and test where possible, and distinguish IMPLEMENTED, TESTED, VERIFIED, NOT RUN, BLOCKED, UNKNOWN and PROPOSED. Update CHAT_START_HERE.md and append CHAT_WORK_LOG.md after meaningful work so future chats can resume without this transcript. Keep PocketCode independent from RevDev and preserve the $0 budget, no-runtime-selected status, security boundaries and canonical LOOP/CASE/D suites.
```


## 12. Atomic multi-file writes and failure recovery

When several related PocketCode docs or source/test files need to change together, prefer a single Git Data API checkpoint: create blobs, build one tree on the verified current tree, create one commit with the live head as parent, update the branch with an expected-head ref lease, and read back all changed files. This avoids extra branch commits and prevents CI from observing an intermediate source/test mismatch. Use the Contents API for appropriate single-file edits. Never blind-retry a rejected ref lease; re-fetch and reconcile.

If a tool/script fails, fetch the exact branch/file state and determine whether the write occurred before continuing. Recover from the last confirmed commit and still close the user-facing response with exact changed/not-changed state. Never silently stop or imply background work. Parallelize independent reads, serialize shared-branch writes.

## 13. ChatGPT implementation authority and concise rotation packet

ChatGPT may be the lead writer for a bounded PocketCode task when it has the necessary source and tools, while retaining continuity/evidence/acceptance responsibilities. Claude/Gemini remain available for independently scoped review or disjoint work. Keep only one lead writer per branch/work item.

The owner should not need to request a giant handoff at the context limit. Maintain the live entrypoint and append-only work log throughout the work. When a chat is rotated, the minimum packet is: repo, branch, entrypoint, last verified commit, active bounded task, exact next action, test evidence/status and any owner action. The new chat fetches its own current source. The transcript is optional.

Close each meaningful pass with: **Completed**, **Evidence**, **Still open**, **Next exact action**. If the task spans multiple turns, checkpoint after two or three meaningful passes or sooner when context strain is visible.

### CI run discovery when the connector view is partial

For push-triggered or scheduled workflows, query the repository Actions run collection directly: `GET /repos/{owner}/{repo}/actions/runs?branch={branch}&per_page=...`. Match the workflow path/name, event, head branch and exact SHA; inspect job summaries and download the relevant logs. Some commit-run connectors expose only pull-request-triggered runs, so an empty result is not proof that push CI did not run. Record the run URL, exact head SHA, job conclusion and test counts.

## 14. Streaming interruption and long-operation resilience

A client message such as “Streaming interrupted” is not proof that model reasoning, a tool call, or a GitHub write failed. It is also not proof that the operation succeeded. Treat the displayed response as potentially incomplete and GitHub/tool read-back as the authority.

**Recovery sequence:**
1. Re-fetch the exact branch head and the files involved in the last attempted write.
2. If the expected commit exists, verify every changed file and its blob/content; do not repeat the mutation.
3. If it does not exist, inspect the current head and rebuild the change from that live state. Never blindly replay a stale write or overwrite another worker.
4. Query CI by workflow run, event, branch and exact head SHA. Do not infer status from a missing/partial connector response.
5. Append the work log and refresh the entrypoint with completed, failed, pending and not-run distinctions.
6. Reply with the last confirmed state, exact recovery action and remaining work. Do not claim that a background operation will finish after the response.

**Reduce interruption exposure:** use bounded work passes; one repository at a time for write batches; parallelize independent read-only fetches; avoid oversized multi-repo scripts; checkpoint after each material implementation/test/decision event; keep user-visible updates concise and independently useful. Do not let the need for a polished final handoff delay durable commits. The compact entrypoint and append-only log are the handoff.

**Client diagnosis:** the assistant cannot inspect the ChatGPT iOS app's internal streaming logs or guarantee that a higher-thinking request will stream reliably. Do not claim Think mode is the cause without diagnostics. For repeated failures, record timestamp/time zone, exact error text, model/thinking selection, whether Wi-Fi or cellular was used, whether the same prompt works in a new chat or on chatgpt.com, and any request ID shown. Check status.openai.com. Follow current OpenAI Help Center guidance and contact Support if it persists across networks/devices. Never ask the owner to share passwords or unrelated private data.

**Product boundary:** this protocol is process-only. It does not import RevDev code, runtime assumptions, schemas, or acceptance suites into PocketCode.