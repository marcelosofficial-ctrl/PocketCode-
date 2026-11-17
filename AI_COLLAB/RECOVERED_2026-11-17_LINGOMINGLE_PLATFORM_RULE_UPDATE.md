# Recovery note — 2026-11-17 platform-instructions update

## Recovery boundary
- Previous DONE checkpoint: `c2dec90d86eaddad02e3709a8a059301e2cab2a8`.
- This pass began at `430826b3911120ec79194641863beb63b338fae1`.
- Live branch head at recovery: `430826b3911120ec79194641863beb63b338fae1`.
- Compare against previous DONE: 2 commits ahead, 0 behind. The only intervening non-checkpoint change is owner-authored commit `bbf81105ad508cf1743ec95c4201ca6414530f31`.

## Verified owner change
Commit `bbf81105` changes only `AI_COLLAB/AI_PLATFORM_INSTRUCTIONS.md`. It corrects LingoMingle's canonical branch and file layout:
- Working branch: `lingomingle-foundation-2026-11-10`.
- Root `BOOT.md` on `main` is a pointer to the working branch.
- On the working branch, `AI_COLLAB/BOOT.md` and `AI_COLLAB/CHECKPOINT.md`; `STATE.md`, `NEXT_TASK.md` and inbox files at repository root.
- It records that the owner added LingoMingle to Claude's fine-grained GitHub access on 2026-11-16, resolving the earlier connector 404. This is an owner-recorded fact in the changed document, not an independently tested access check in this pass.
- It clarifies reviewer/lead checkpoint separation: Claude logs progress in `INBOX_claude.md` and does not overwrite the lead's checkpoint.
- It updates ChatGPT's project instructions to remove the incorrect instruction to install the starter kit on LingoMingle.

## Impact and disposition
- This is documentation/process correction only. No PocketCode runtime, source, tests, CI, provider, adapter, workflow, acceptance IDs, PRs or release gates changed.
- No LingoMingle repository was accessed or modified in this PocketCode pass.
- The current task remains the PocketCode journal-to-receipt provenance boundary. This pass could not inspect source implementation because the mandatory BOOT/STATE/NEXT_TASK startup reads consumed the three-file budget. Do not infer an API shape or patch source without a focused source/test review.
- **VERIFIED:** commit path and diff, branch comparison, latest five commits.
- **UNKNOWN:** current source API details and exact-tree test status.
- **NOT RUN:** tests; no test execution was attempted.

## Latest five branch commits at recovery
1. `430826b` — begin this bounded pass.
2. `bbf8110` — correct platform instructions and LingoMingle paths.
3. `c2dec90` — previous pass DONE.
4. `4b37348` — previous pass begin marker.
5. `30ae5d1` — grant replay research pass DONE.
