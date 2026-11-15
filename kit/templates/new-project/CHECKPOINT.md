# CHECKPOINT: <PROJECT>

STATUS: DONE
Unit: template installed, nothing started.
Files: none.
Commits: none.
Next: run NEXT_TASK.md T-001.

Format rules (every AI follows them):
- First action of a turn: overwrite this file with `STATUS: IN PROGRESS`, the unit, the files you will touch and the time.
- Last action of a turn: overwrite it with `STATUS: DONE`, the unit, the commit SHAs and the next step.
- If you find IN PROGRESS, or commits newer than this file, write a `RECOVERED:` line saying what landed and what did not, then continue with one unit.
- Keep this file under 150 words. History lives in git, not here.
