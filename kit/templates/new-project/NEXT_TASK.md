# NEXT_TASK: <PROJECT> (one task only; the lead writer replaces it when it is done)

Task ID: T-001
Owner of this task: ChatGPT (lead)
Budget: one turn (see BOOT.md turn budget)

## Task
Bootstrap the project record from the repo, without inventing anything.
1. Read at most 3 files: README (if any), the top-level file tree, and the main manifest (package, project or build file).
2. Fill every UNKNOWN in BOOT.md and STATE.md that those files prove, tagged VERIFIED with the path.
3. Write the questions only the owner can answer (maximum 5) into STATE.md.
4. Set CHECKPOINT.md to DONE with the commit SHAs, then replace this file with T-002.

## Done when
- BOOT.md Identity section has no <...> left.
- STATE.md lists what exists, what is UNKNOWN, and the owner questions.
- No claim about behaviour or tests without a source path or CI output.

## Do not
- Invent features, stack choices, budgets or acceptance criteria.
- Import anything from RevDev or PocketCode.
- Change files outside AI_COLLAB/ in this task.
