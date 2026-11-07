# NEXT TASK: PocketCode (seed; verify against live state)

## Goal
Get a real test result for the recovery prototypes: run the full existing Python test suite, including the new outbox and coordinator tests, against the actual repository modules, and record PASS / FAIL / NOT RUN with output.

## Files to read
- [Recovery contract](AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md) (section on lifecycle and recovery only)
- scripts/fake_coordinator.py and scripts/test_fake_coordinator.py (headers and test names only)

## Constraints for this task
- Mode: normal. Output: about 350 lines per turn. Do not choose a database or provider.
- If code cannot be executed in this chat, write NOT RUN and instead prepare the exact command list and expected-output checklist for a runtime that can (GitHub Actions or a PC).
- Out of scope: durable storage choice, provider integration, merging PRs.

## Steps
1. Locate the test entry command (check .github/workflows and scripts/).
2. Run, or prepare, the suite command.
3. Record results; list failures with file and test name.

## Done when
- A results note exists in AI_COLLAB with the command, output or NOT RUN, and any failures listed.
- STATE.md and CHECKPOINT.md updated.

## If blocked
Write the blocker into CHECKPOINT and stop.
