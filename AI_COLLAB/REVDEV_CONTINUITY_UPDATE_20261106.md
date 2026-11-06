# Cross-project continuity update for PocketCode — 2026-11-06

This document is a forwardable briefing from the RevDev chat. It contains process improvements and method-only engineering lessons. It does not authorize PocketCode to adopt RevDev code, architecture, runtime, acceptance evidence or release decisions.

## What changed in our working method

The owner wants the multi-month, hundreds-of-chats workflow to be smoother and less dependent on giant handoffs at the point a chat is already full. Adopt this as a PocketCode operating objective:

**GitHub is durable project memory; each ChatGPT conversation is a replaceable worker.**

- Keep `AI_COLLAB/CHAT_START_HERE.md` as the live entrypoint, not a long transcript.
- Keep `AI_COLLAB/CHAT_WORK_LOG.md` append-only for completed work, decisions, tests and evidence.
- Keep canonical design, contracts, test suites and detailed handoffs in their own docs. The start page points to the current task-specific documents.
- Checkpoint after 2–3 meaningful work passes, and immediately after implementation, test, review or decision events. Do not wait until context is almost full.
- Rotate to a fresh chat while the current one still has enough context to summarize. A fresh chat reads the start page and relevant canonical docs, verifies live GitHub state, and continues.
- The owner should not have to ask an exhausted chat to create a handoff. Every substantial user request ends with a visible summary and exact next step.
- After every source/test/review/decision change, update the entrypoint and work log. For important work, create a dated detailed handoff with exact branch/head, file/blob pins, test SHA/count, open issues and next steps.
- Parallelize independent reads and research. Do not parallelize writes to the same file or shared branch without coordination. Use one lead writer per repo/branch/work item. Re-fetch before writes, serialize shared-path writes and read back every changed file.
- When a tool fails, re-fetch the branch/file state, determine whether the operation landed, then recover. Never silently stop or repeat an uncertain write.
- Use exact-SHA CI evidence. Inspect workflow path, event, branch, head SHA, job conclusion and test logs. Empty/partial status from a connector is not proof that no workflow ran.
- Keep checkpoints compact. Do not make every new chat read hundreds of messages or every historical handoff. Read the start page, then only the current canonical task docs.
- Rotate after 2–3 meaningful passes or sooner when context load or task complexity suggests it. Do not use a fixed message count as the limit.

## Three-AI collaboration remains

- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect and cross-project coordinator.
- Owner forwards exact review packets and results between chats.
- Assign one lead writer to each repository/branch/work item; other AIs review read-only or own disjoint tasks.
- Review requests must include exact commit SHA, file paths/blob hashes, expected outcome and specific questions. Ask for line-level findings, counterexamples, severity and regression tests.
- Resolve differences using source evidence and executable tests, not consensus by repetition.

## RevDev engineering/CI lesson, method only

RevDev's R5 publisher/transport/installer source suite passed **93/93** in Windows PowerShell 5.1 / Pester 5.7.1 at exact source/test SHA `a6defbb0e8b0902e8ecc20777d0a10dc25ae344b`, Actions run #49:
https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42182731390

Useful methods PocketCode may independently consider:
- test native process exit status and parsed HTTP status together;
- fake the child process to test stdout, stderr, nonzero exit, typed 404/429 and conflicting acknowledgements without live network calls;
- fail closed on missing executable or unknown exit status;
- exact-byte digest/readback, not just matching business identity;
- include installer dependency closure and mutable provenance markers in rollback tests;
- pin all fetched source files to one immutable source commit;
- record exactly what CI does not prove.

This is **RevDev-only evidence**. It does not validate PocketCode code, architecture, runtime, device behavior or CASE/LOOP/D acceptance. Do not transfer code or acceptance.

## PocketCode direction and constraints remain unchanged

- PocketCode is a separate phone-first iOS/Android product, not a RevDev merge.
- Keep separate repos, roadmaps, clients, adapters, runtime, security boundaries, acceptance suites and release gates.
- $0 default budget, no PC requirement, no runtime/provider selected.
- Explicit paste-to-context only; no clipboard polling or intrusive overlays.
- SSH/Tailscale and cloud remain adapter/research directions; local WASM/Pyodide/JSC only for suitable light/trusted tasks.
- Preserve canonical LOOP/CASE/D IDs and meanings. PR #2 and #3 remain untouched.
- Execution, observation, immutable receipt, artifacts, cleanup and AI correction lineage remain distinct.

## PocketCode's own current work is not displaced

Immediate priority remains CASE-04 timeout/report-contract evidence provenance. Do not change `report_contract.py` based only on exit-code precedence. Distinguish trusted child exit, wrapper exit, forced termination, timeout lifecycle and collector/teardown degradation. Preserve CASE-04 INCOMPLETE/timed_out and all canonical IDs.

Pyodios device evidence remains:
**ARTIFACT-LEVEL FUNCTIONAL SUCCESS (owner-inspected) / EDITOR BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE.**
The existing exact-match `summary.json` must be preserved. The Error Log showed only `Editor: PythonError`, without traceback. Next action is only the read-only `sys.last_exc` / `sys.last_value` Console probe in the existing session. Do not rerun, overwrite, restart the session, clear variables/logs or run GC. See `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md` and `NEW_CHAT_HANDOFF_20261106.md`.

## Copy/paste message to the PocketCode chat

```text
Please read AI_COLLAB/CHAT_START_HERE.md and AI_COLLAB/REVDEV_CONTINUITY_UPDATE_20261106.md on branch pocketcode-ai-workflow-director-research-2026-10-28. Adopt the multi-chat continuity method as a first-class project objective: GitHub is durable memory and each chat is a replaceable worker. Keep the start page current, append the work log, checkpoint every 2-3 meaningful passes or after source/test/review/decision events, and rotate before context exhaustion. Do not wait for me to ask for a giant handoff when the chat is already full. Always finish substantial turns with a visible result and exact next step. If a tool fails, re-fetch and recover instead of silently stopping.

Use one lead writer per repo/branch/work item. Parallelize independent research/reads, serialize shared-path writes, re-fetch before writes and read back afterward. Give Claude and Gemini exact commit/file pins and focused review questions. Keep their roles: Claude lead developer/architecture reviewer, Gemini independent security/spec auditor, ChatGPT continuity/evidence/acceptance coordinator. I manually forward results between AIs.

RevDev's run #49 passed 93/93 Windows PowerShell 5.1/Pester 5.7.1 at exact SHA a6defbb0e8b0902e8ecc20777d0a10dc25ae344b. You may reuse the testing and continuity methods described in the update, but this is RevDev-only evidence. Do not adopt RevDev code, runtime, architecture, acceptance or security decisions into PocketCode.

Continue PocketCode's own priorities unchanged: CASE-04 timeout/report-contract provenance first; preserve canonical LOOP/CASE/D IDs and meanings. Pyodios remains artifact-level success with bridge error unresolved and full run inconclusive. Preserve the exact-match summary.json and do only the read-only sys.last_exc/sys.last_value probe next. Do not rerun or overwrite the successful project. Keep phone-first, $0, no-PC requirement, explicit paste-to-context, no clipboard polling/overlays, no runtime/provider selected, and PR #2/#3 untouched.

Please verify live branch/PR/CI state first, then continue the highest-value bounded work. Update the start page, work log and handoff as you go. Make executive decisions when they improve the project, and if changing a boundary, record the benefit, risk and verification plan.
```
