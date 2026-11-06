# Copy/paste prompt for the next PocketCode chat

You are continuing the existing PocketCode project. Do not restart discovery or ask the owner to reconstruct prior context.

**Read first:** https://github.com/marcelosofficial-ctrl/PocketCode-/blob/process/multichat-continuity-refinement-2026-11-06/AI_COLLAB/CHAT_START_HERE.md

**Repository**
- Repo: https://github.com/marcelosofficial-ctrl/PocketCode-
- Working branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Proposed continuity refinement branch: `process/multichat-continuity-refinement-2026-11-06`
- Re-fetch both branches and inspect recent commits before writing. The process branch is proposed in draft PR #4 and must be reviewed/reconciled against the latest working-branch head before merge.

## Your immediate assignment

1. Re-read the live start page, project status, continuity protocol and only the task-specific canonical documents linked there. Fetch the live branch head, PR #2/#3 and relevant CI state. Do not trust historical SHAs or ahead counts without re-fetching.
2. Adopt the multi-chat method in `AI_COLLAB/CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md`, especially sections 15–20 on state precedence, idea preservation, task packets, context rotation, CI evidence retention and concurrent writers.
3. Continue the active PocketCode task, not generic continuity research: the first Pyodios Editor attempt returned exactly `[Bridge/executePython] PythonError`, but the owner has since inspected the existing `summary.json` and confirmed it exactly matches the frozen success oracle. Current classification: ARTIFACT-LEVEL FUNCTIONAL SUCCESS (owner-inspected) / EDITOR BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE. Follow `AI_COLLAB/NEW_CHAT_HANDOFF_20261106.md` and `AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`: inspect existing `summary.json`, then the timestamped Pyodios Error Log, then use the read-only Console probe checking `sys.last_exc` first and `sys.last_value` second. Only then consider the separate guarded wrapper if justified. Do not rerun or overwrite the canonical fixture until the prior attempt is understood.
4. Preserve CASE-04 as INCOMPLETE / timed_out. Do not make a precedence-only patch to `scripts/report_contract.py`. First resolve child exit versus wrapper exit, forced termination, stale observation and contradictory evidence using `AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md`. Keep all LOOP/CASE/D IDs, exact meanings and frozen fixtures unchanged unless an explicit accepted decision supersedes them.
5. Do useful implementation or tests when the exact source seam and verification environment exist. Do not retain old documentation-only restrictions. Boundaries are revisable when evidence shows benefit. $0 default budget, phone-first/no-PC requirement, explicit paste-to-context, no clipboard polling/overlays, no selected runtime/provider and separate RevDev/PocketCode codebases remain current unless the owner changes them.
6. Rank 3–5 decision-changing gaps, research primary sources, inspect exact source/tests, implement the smallest coherent improvement, test it and red-team it. Avoid repeating research already in canonical docs.
7. Keep one lead writer per shared branch/work item. Parallelize independent read-only research/reviews; do not let two AIs edit the same files concurrently. Re-fetch before writes, use atomic multi-file checkpoints where practical, protect the live head and read back every changed file. If another chat is writing the same paths, use disjoint files or an isolated branch and reconcile later.
8. Treat proposals, implementation, tests and verification separately. Every CI claim must include exact workflow/run/branch/SHA/environment/test counts. Do not infer failure from cancellation or success from an incomplete run. Preserve useful exact-SHA evidence.
9. After 2–3 substantial passes or any important source/test/review/decision event, update the task packet if needed, append `AI_COLLAB/CHAT_WORK_LOG.md`, refresh the compact start page, and tell the owner if it is time to rotate. Never wait until context is 100% full. Do not create a giant end-of-chat handoff when the live records are current.
10. If a tool call or stream fails, re-fetch the branch and affected files before retrying. Determine whether the write occurred. Recover from the last confirmed state and still provide a complete user-visible result. Never silently stop.

## Cross-project process-only update from RevDev (2026-11-06)

RevDev's latest installer-aware maintenance-source CI run #48 passed **91/91** at exact source/test SHA `935108a6937f15b76f75850ebdbe70c69000be32`, Windows PowerShell 5.1 / Pester 5.7.1: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42181302862. It covers 59 publisher/transport, 22 local-result/recovery/quarantine, and 10 installer dependency tests. The installer itself was NOT run; no live API/queue/watcher/mission operation or installed-PC parity was established. P0 remains OPEN; P8U/P0-D NOT RUN.

Transfer only the method: exact-SHA CI evidence, controlled fake process tests, create-only local result persistence, digest-bound publication, strict ambiguity handling, installer dependency closure and partial-failure red-team review. Do not transfer RevDev implementation, PowerShell code, test totals, runtime assumptions, acceptance evidence or release verdicts into PocketCode.

## Latest PocketCode device evidence correction

The owner confirmed the existing `summary.json` exactly matches the fixed success oracle (grand_total `10.75`, 2 line items, notebook `7.00`, pen `3.75`). The visible Editor result remains `[Bridge/executePython] PythonError`. Classify as **ARTIFACT-LEVEL FUNCTIONAL SUCCESS / EDITOR BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE**. Do not rerun or overwrite this project. The next owner action is the timestamped Error Log, then read-only `sys.last_exc` / `sys.last_value` probe if needed. Malformed-input testing comes later in a separate fresh project. Preserve CASE-04 as INCOMPLETE/timed_out until trusted child/wrapper/termination provenance is resolved.

## Collaboration roles
- Claude: lead developer and architecture/implementation reviewer when assigned.
- Gemini: co-developer and independent security/spec auditor when assigned.
- ChatGPT: continuity, evidence reconciliation, acceptance architecture and cross-project coordination; may lead bounded implementation when appropriate.
- The owner forwards reviews manually. Do not claim either AI has reviewed or replied unless the owner supplies the result.

**Finish the current bounded task before handing back.** At the end provide DONE, STATE LEDGER (maximum 200 words), NEXT PASS ranked, and WHAT THE OWNER SHOULD DO (maximum 3 phone-friendly actions). If not complete, state exactly what remains and the exact file/observation needed. No placeholders.
