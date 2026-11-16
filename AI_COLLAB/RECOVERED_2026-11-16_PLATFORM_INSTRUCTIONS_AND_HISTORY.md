# Recovery note — platform instructions and branch history

Date: 2026-11-16
Branch: pocketcode-ai-workflow-director-research-2026-10-28

## Verified branch recovery

The exact GitHub branch endpoint and commits collection were used instead of GitHub commit search. The search endpoint's top results were not the branch's latest commits; the branch-scoped commits endpoint returned the actual ordered history.

Latest five at the time of this note:
1. `458ef0f3f04018a2efb67a5ff7ace9a26af5f755` — fix(pocketcode): preserve checkpoint history while opening pass
2. `1d1222fc64e8fda50859ea6722470f8dfc3374cf` — chore(pocketcode): begin bounded continuation pass
3. `a98529d2b8e475ff52f36fb49f586bbcb53ab785` — docs(kit): add Claude block, LingoMingle access and Actions notes to platform instructions
4. `bc63ebc4481493c2d36415ca1c74704acd5378ab` — chore(pocketcode): complete bounded implementation pass
5. `69ea992c218f7ff7374de8de3bf7a2207f80937b` — docs(pocketcode): record bounded patch pass recovery

Compare from prior DONE `bc63ebc4481493c2d36415ca1c74704acd5378ab` to current head `458ef0f3f04018a2efb67a5ff7ace9a26af5f755`: 3 commits ahead, 0 behind. Aggregate paths: `AI_PLATFORM_INSTRUCTIONS.md` and `CHECKPOINT.md`. The external intervening commit `a98529d` changes only platform instructions; it adds Claude-specific guidance to avoid overwriting the lead's checkpoint and use `INBOX_claude.md`, and documents Actions evidence limitations. It does not change PocketCode source, tests, workflow, adapters or runtime.

## Checkpoint integrity

The original checkpoint content was fetched before the pass. During checkpoint initialization, an incomplete replacement was briefly committed; the next commit immediately restored the full previously fetched checkpoint history and set the status back to IN PROGRESS. The restored content includes the earlier pass records. This incident is disclosed rather than treated as a source change. The compare reports the final checkpoint path delta; no other project files were modified by this pass.

## Tooling finding

Use the branch-scoped REST collection:
`GET /repos/{owner}/{repo}/commits?sha={branch}&per_page=5`
for ordered latest-five history. The GitHub commit-search endpoint is not a reliable substitute for branch ancestry.

The available GitHub write surface still has no hunk-apply action. Contents updates require full replacement text; Git Data API blob/tree/commit operations also require a complete replacement blob. This does not provide a safe patch path for the current large journal/receipt files under the read/reconstruction limits. No source/test patch was attempted.

## Current verification

- Branch head: `458ef0f3f04018a2efb67a5ff7ace9a26af5f755`.
- Combined commit statuses: empty.
- Associated workflow runs returned by the connector: empty.
- Exact-tree tests, device/browser acceptance and adapter conformance: NOT RUN.
- P39 implementation/adapter conformance remains CLOSED; CASE-04 remains INCOMPLETE / `timed_out`.
- No source, test, workflow, PR, provider, runtime, adapter, deployment or infrastructure changes.

## Next bounded unit

Find a patch-capable GitHub/local editing route that applies a reviewed diff against the exact blob without reconstructing a large file. Then implement live-journal receipt capture with an explicit linearization contract and focused stale-snapshot/scope regressions. Run tests against and report the exact resulting SHA; do not change workflow authorization or promote historical CI to current-tree proof.
