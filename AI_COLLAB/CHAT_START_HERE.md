# PocketCode Chat Start Here

**Purpose:** compact live entrypoint for every PocketCode chat. GitHub is the durable project record; chats are replaceable workers. Fetch live state before acting.

## First 5 minutes
1. Read this page.
2. Fetch the live branch head and compare; inspect PR #2/#3 and relevant CI runs.
3. Read only the task-specific source, tests and canonical docs linked below.
4. Continue the active task. Do not restart discovery or ask the owner to repeat known context.

## Repository
- Repo: https://github.com/marcelosofficial-ctrl/PocketCode-
- Working branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Live branch head and ahead/behind count: always fetch; do not trust historical snapshots.
- Open PR #2: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2 (previously OPEN/DRAFT; recheck).
- Open PR #3: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3 (previously OPEN/DRAFT; recheck).
- PR #4 is the draft process-refinement proposal: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/4. It must be reconciled with this branch's latest commits before merge.
- Do not assume active research-branch commits are included in PR #2/#3. Do not alter PRs without a concrete reason.

## Product direction and constraints
- Phone-first iOS/Android Agentic Orchestration Control Plane; broader PC-and-phone programme with RevDev, but separate repos, clients, roadmaps, adapters, runtimes, security boundaries, acceptance suites and release gates.
- Discovery/product-definition phase. Product hypothesis: provider-neutral task execution, evidence receipts, recovery and AI correction, not merely a mobile Python IDE.
- $0 default budget. No provider, production runner, cloud host or execution sandbox selected.
- No reliable PC/local access expected until approximately 2027-02-28. Treat PC/runtime/install state as UNKNOWN.
- Explicit paste-to-context only. No clipboard polling or intrusive overlays.
- Preserve canonical LOOP-01..14, CASE-01..16 and D-01..D-08 meanings and frozen fixtures. Do not silently remap IDs or alter acceptance semantics.
- Owner permits implementation and changing operational boundaries when evidence shows project benefit. Record authority changes, risks and verification. Do not ask permission for routine bounded engineering.

## Active task: Pyodios evidence and CASE-04 provenance

**Observed:** Editor displayed exactly `[Bridge/executePython] PythonError`.
**Owner-confirmed artifact:** existing `summary.json` exactly matches the frozen success oracle: grand_total string `10.75`, line_items integer `2`, notebook `7.00`, pen `3.75`.
**Classification:** ARTIFACT-LEVEL FUNCTIONAL SUCCESS (owner-inspected) / EDITOR BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE. No trusted process exit status, stderr, export/read-back, relaunch persistence or PocketCode acceptance is established.
**Do not rerun or overwrite the successful project.**
Next:
1. Owner inspects More → Settings → Error Log → View Error Log at the attempt timestamp and shares only a redacted relevant traceback.
2. If unhelpful, use the read-only Console probe checking `sys.last_exc` then `sys.last_value`.
3. After diagnostics are preserved, test malformed input only in a separate fresh project.
4. Preserve CASE-04 as INCOMPLETE / timed_out. Resolve child/wrapper/termination provenance before changing `classify_verdict()`.

## Read next
- [Latest 2026-11-06 handoff](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/NEW_CHAT_HANDOFF_20261106.md)
- [Pyodios bridge triage](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md)
- [Pyodios device protocol](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md)
- [Verdict/exit provenance matrix](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md)
- [Execution-loop acceptance, canonical](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md)
- [Owner decision register](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/OWNER_DECISION_REGISTER_20261029.md)
- [Current project status](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/../PROJECT_STATUS.md)
- [Continuity protocol](CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md)
- [Work packet template](WORK_PACKET_TEMPLATE_20261106.md)
- [Copy/paste continuation prompt](POCKETCODE_CHAT_CONTINUATION_PROMPT_20261106.md)
- [Cross-project RevDev update](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md)

## Multi-chat working rules
- Checkpoint after 2–3 substantial passes, and after every important source/test/CI/review/decision event. Rotate before context strain; never wait for a full-chat warning.
- Maintain the live entrypoint, append-only work log and task-specific packet. Do not produce giant last-minute handoffs.
- One lead writer per shared branch/work item. Parallelize independent read-only research/review; serialize shared writes.
- Re-fetch before writes, use atomic multi-file commits when practical, protect the current head and read back every changed file.
- Verify CI by exact workflow, run, event, branch, SHA, job and test count. Preserve useful completed runs. A cancelled run is CANCELLED, not FAIL.
- On stream/tool failure, inspect GitHub before retrying. Close every pass with what changed, what did not, evidence scope, unknowns and next action.
- Keep the entrypoint compact. Historical detail belongs in the work log or canonical evidence reports, not appended repeatedly here.

## Collaboration
- Claude: lead developer and architecture/implementation reviewer when assigned.
- Gemini: co-developer and independent security/spec auditor when assigned.
- ChatGPT: continuity/evidence/acceptance/cross-project coordinator; may lead bounded implementation.
- Owner forwards other AI reviews manually. Do not claim review completion without supplied evidence.

**Evidence labels:** VERIFIED (source opened or test run at exact SHA), INFERRED, UNKNOWN, PROPOSED, IMPLEMENTED, TESTED, NOT RUN, BLOCKED. Never blur these states.
