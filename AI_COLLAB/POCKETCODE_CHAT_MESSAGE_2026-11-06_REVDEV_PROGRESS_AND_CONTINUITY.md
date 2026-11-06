# Message for the active PocketCode chat — 2026-11-06

Please read the live PocketCode entrypoint first:
https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CHAT_START_HERE.md

This is a cross-project update and collaboration instruction. It does not authorize copying RevDev implementation into PocketCode.

## What has changed in RevDev

- Local result persistence is create-only/atomic. Discovery validates project, mission, protocol, schema, run ID/directory and result state. Multiple candidates are AMBIGUOUS; malformed, unreadable or partial discovery is DISCOVERY_INCOMPLETE. It does not choose the newest result.
- Runner emits a SHA-256 for the immutable local result; watcher passes it through; publisher re-reads/verifies it and binds CLI Project/Mission to the result identity before any GitHub API request.
- Publisher uses typed process + HTTP response classification. Missing immutable mission paths require a complete, parse-clean HTTP 404 with the expected JSON message. Authentication, cancellation, malformed responses and unknown status do not mean absence.
- Exact prepared-envelope bytes are verified on remote readback. Existing identity fields alone are not treated as operation attribution or idempotent success.
- A hermetic fake native executable exercises the actual child-process boundary, including stdout/stderr, exit codes, HTTP 200/404/429, missing executable and Windows PowerShell 5.1 global LASTEXITCODE lifecycle.
- Recovery quarantine uses unique destinations and create-only metadata.
- The clean installer now stages, parses, hashes, backs up, installs and rolls back four newly imported sibling modules. It resolves production main once and fetches every file from that immutable commit SHA.
- A further audit found the installation marker R5_INSTALLED.txt also needed rollback. It is now backed up/restored, or removed if newly created and no previous marker existed.

## Exact evidence, not broad claims

RevDev Actions run #48 passed **91/91** at exact source/test SHA 935108a6937f15b76f75850ebdbe70c69000be32, Windows PowerShell 5.1 / Pester 5.7.1:
https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42181302862

That run includes 59 publisher/transport tests, 22 local-result/recovery/quarantine tests and 10 installer dependency/source-pin tests. It does not cover the later installation-marker rollback change.

Latest RevDev source commit: a6defbb0e8b0902e8ecc20777d0a10dc25ae344b.
Latest docs checkpoint: 287b36a4cf7db1727ce3cf18e22b0dc2ea16170d.
Latest suite: **93 authored tests**. Run #49 42182731390 targets the latest source commit and was IN_PROGRESS at the last observation:
https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42182731390

No installer was executed. No PC files, live queue, watcher, mission or live API were touched. Installed product parity remains UNKNOWN. RevDev P0 remains OPEN; P8U/P0-D remain NOT RUN.

## Collaboration improvements to adopt in PocketCode

The owner wants both projects to progress over months and hundreds of chats without giant last-minute handoffs or silent stalls. Keep GitHub as durable project memory and treat each chat as a replaceable worker.

1. Every chat starts by reading the live AI_COLLAB/CHAT_START_HERE.md, fetching the current branch head and checking relevant PR/CI state. Do not reconstruct context from old chat memory.
2. Maintain three layers: compact start page, append-only CHAT_WORK_LOG.md, and detailed canonical design/evidence docs.
3. Checkpoint after every 2–3 meaningful passes, and immediately after any important source, test, CI, reviewer or decision event. Do not wait for a full-context warning or a user request for a huge handoff.
4. Every work pass must end with a user-visible response and a durable checkpoint. State what changed, what did not, exact verification scope, unresolved UNKNOWN/BLOCKED/NOT RUN items and the next action. A tool error or interrupted stream is not permission to silently stop.
5. On tool failure, re-fetch the live branch and target blobs before retrying. Verify whether a write landed. Never blindly repeat an ambiguous write.
6. Batch related docs/source changes into one atomic multi-file Git tree commit where practical. Use expected-head protection; serialize writes to the same branch/path. Parallelize independent read-only research/reviews.
7. Pin CI to exact SHA. Query repository Actions runs by workflow path, branch, event and SHA; inspect job result and logs for test counts. Never let an older green run validate a newer source revision.
8. Use bounded passes and bounded CI polling. If CI is pending, checkpoint the run ID/SHA and continue useful independent work rather than polling indefinitely.
9. Keep entrypoints compact. Do not dump full goals ledgers or every old handoff into every chat. Read task-specific evidence only.
10. Rotate chats while there is still enough context to close the pass. The outgoing chat should only need to update the log and entrypoint, not compose a giant handoff from memory.

The owner has explicitly broadened routine engineering authority: implement, test, research, build and use CI when the target is available and it benefits the project. Do not ask permission repeatedly for ordinary reversible work. Boundaries can be revised when evidence supports it, with changed authority and risk controls recorded. The $0 default budget and PC-unavailable constraint remain. Do not install, deploy or touch a live runtime merely because hosted CI passes.

## PocketCode remains independent

Do not adopt RevDev PowerShell code, test counts, runtime choices, acceptance IDs or release conclusions. PocketCode's immediate priority remains its own CASE-04 timeout/report-contract evidence-provenance work. Preserve LOOP/CASE/D semantics, phone-first design, explicit paste-to-context, no clipboard polling/overlays, $0 budget and no runtime/provider selection.

The current Pyodios attempt is recorded as artifact-level functional success, bridge error unresolved, full run inconclusive. Preserve the successful project and do not rerun or overwrite it. Follow the live PocketCode start page for the next diagnostic step.

## Latest CI correction

Run #49 is now complete and green at exact source/test SHA a6defbb0e8b0902e8ecc20777d0a10dc25ae344b: 93/93. This supersedes the pending status above. Source/test validation only; no installer execution or PC/live runtime action.
