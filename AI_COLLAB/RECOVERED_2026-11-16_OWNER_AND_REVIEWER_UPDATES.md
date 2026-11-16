# Recovery note — owner and reviewer updates
Date: 2026-11-16
Branch: `pocketcode-ai-workflow-director-research-2026-10-28`

## Recovery boundary

Prior DONE head: `eaed271c298f0a8f0cf8d6061f4068b9337852e6`.
Owner-authored commit after it: `8f952c6315b1b377bef19d8b69fb1ca462356b7b`.
This turn's checkpoint marker: `e503aa0a48a33b881e00dcd605e30fd81de6df5d`.

Branch comparison from prior DONE: 2 commits ahead, 0 behind. The owner-authored commit changed only:
- `AI_COLLAB/INBOX_chatgpt.md`: appended Claude message `2026-11-16-1`.
- `AI_COLLAB/WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md`: redacted private RevDev acceptance details from the public PocketCode repository and recorded progress in two website audit files.

No source, test, workflow, runtime, provider, PR or acceptance-ID changes were present in this recovery delta. The public-history redaction does not erase prior Git history; the owner commit explicitly records that no secrets were present.

## Claude request recovered

Claude's OPEN, non-blocking housekeeping request asks ChatGPT to:
1. Add four index rows: `AI_COLLAB/AI_PLATFORM_INSTRUCTIONS.md`, `AI_COLLAB/WEBSITE_AUDIT_HOME_AND_JA_20261115.md`, `AI_COLLAB/WEBSITE_AUDIT_ABOUT_CONTACT_RESUME_20261115.md`, and one grouped row for six files under `kit/templates/new-project/`; mark row 5 of `STRATEGY_PROGRAM_20261108.md` PARTIAL with the two website audit files as evidence.
2. Decide whether reviewer agents should avoid overwriting the lead's `CHECKPOINT.md`, with progress instead recorded in their own inbox.
3. Check whether this connection can read `marcelosofficial-ctrl/LingoMingle` and, only if accessible, install the starter kit there under the separate project's rules.

No item is silently treated as completed. They are independent of the PocketCode model/acceptance work and should be scheduled after the critical receipt/replay work, unless the owner reprioritizes them.

## Current recovery state

- Startup files read in required order: `AI_COLLAB/BOOT.md`, `AI_COLLAB/STATE.md`, `AI_COLLAB/NEXT_TASK.md`.
- BOOT/STATE/NEXT_TASK agree on priorities: exact-tree tests, journal-to-receipt provenance/freshness, grant replay/outbox semantics, producer trust, lifecycle/termination.
- BOOT's general rule says an AI overwrites CHECKPOINT first and last; Claude's request identifies a reviewer-only conflict. No policy change is made in this recovery note. The lead remains responsible for the active checkpoint in this turn.
- The last-five branch commits at recovery time were: `e503aa0`, `8f952c6`, `eaed271`, `bf32b87`, `2420a62`.

## Evidence limits

The compare endpoint verified the changed paths and compact patches. Full content of Claude's two referenced website audit files, INDEX, strategy tracker, platform instructions and six template files was not read in this turn. No claim is made that their requested index/tracker edits have been applied. No LingoMingle access or write was attempted.

## Next action

Resume the PocketCode critical model gap from `AI_COLLAB/NEXT_TASK.md`: inspect the exact current EventJournal and receipt API/test surface within the file-read budget, then implement a bounded source/test patch only if the GitHub tool path can preserve all unrelated content. Otherwise add no speculative code and report the exact editing limitation.
