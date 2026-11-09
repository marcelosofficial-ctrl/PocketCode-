# PR #4 continuity refinement reconciliation

**Date:** 2026-11-09  
**Status:** Reviewed, not merged; owner decision required for PR disposition  
**PR:** [#4, Draft: Refine interruption-safe multi-chat continuity](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/4)  
**Working branch snapshot checked:** `2c39ce0270168c17c0a33db3032b9beca307a7e6`  
**PR head checked:** `bb7ed423af1872c2fe5895210cbd2669f6debe9f`

## 1. Live GitHub facts

**VERIFIED from GitHub API on 2026-11-09:**
- PR #4 remains OPEN and DRAFT.
- Base is `pocketcode-ai-workflow-director-research-2026-10-28`; head is `process/multichat-continuity-refinement-2026-11-06`.
- The PR files endpoint returns **7 changed files**, while the PR body says six.
- Comparing the current working branch to the PR head reports the process branch as **11 commits ahead and 312 behind**; the merge base is `33c246aba6339a7c36d039204e2cf66cf65dcbd8`.
- The process branch is an old snapshot, not a current head-equivalent proposal.
- No PR action, rebase, merge, close, review submission or branch mutation was performed.

The PR body also describes a previous verification of six files. That count is stale and does not match the current seven-file API response.

## 2. File-by-file disposition

The classifications below are recommendations for reconciliation, not GitHub merge decisions. “DROP” means exclude the stale/duplicate PR change from the eventual integration proposal; it does not authorize deleting historical content from the repository.

| PR path | Classification | Reason and exact treatment |
|---|---|---|
| `AI_COLLAB/CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md` | **MERGE-INTO-BOOT** | Sections 15–20 contain useful rules on source precedence, idea preservation, concurrent writers, task packets, rotation, CI retention and research hygiene. The active `AI_COLLAB/kit/docs/WORK_PROTOCOL.md` already supersedes this older protocol for startup and defines the compact boot flow. Do not copy six full sections into BOOT. Select only short missing invariants and merge them into the canonical BOOT/WORK_PROTOCOL after checking word limits and duplication. |
| `AI_COLLAB/CHAT_START_HERE.md` | **DROP** | This creates a second startup authority. It points to the old Pyodios assignment and historical handoff sequence, while active BOOT/STATE/NEXT_TASK now govern startup. It also carries language about implementation authority that should not replace current decision-register gates. Keep the old file only as a historical branch artifact; do not merge it as the active entrypoint. |
| `AI_COLLAB/CHAT_WORK_LOG.md` | **KEEP** | It is an append-only historical record of the process refinement and its red-team corrections. Retain its history if that branch is integrated, but do not use old HEAD, ahead-count or device facts as current state. |
| `AI_COLLAB/CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md` | **KEEP** | It explicitly distinguishes RevDev evidence from PocketCode and permits only process-method transfer. Preserve the boundary; do not copy RevDev code, runtime assumptions, acceptance results, test totals or release conclusions into PocketCode. |
| `AI_COLLAB/POCKETCODE_CHAT_CONTINUATION_PROMPT_20261106.md` | **DROP** | It is a second start prompt, routes users to the superseded CHAT_START_HERE page, and prioritizes the old Pyodios task over current NEXT_TASK. Its useful process constraints already belong in BOOT/WORK_PROTOCOL. |
| `AI_COLLAB/WORK_PACKET_TEMPLATE_20261106.md` | **KEEP** | The 69-line reusable task packet has useful fields for objective, scope, canonical invariants, exact source pins, acceptance cases, execution evidence, review and one next action. Keep it as an optional template for substantial tasks, not a mandatory file for every one-line change. |
| `PROJECT_STATUS.md` | **DROP** | The proposed additions duplicate the old process branch summary and stale Pyodios history. Current STATE/NEXT_TASK/CHECKPOINT and the append-only work log already separate live status from history. Do not merge a second duplicate narrative. |

## 3. Unique process improvements worth retaining

The process branch's useful contribution is not a new startup page. It is a compact set of explicit collaboration invariants:

1. **Authority precedence:** latest owner decision; canonical acceptance and fixtures; accepted decisions; exact source/test/CI; live task files; historical logs/chats last.
2. **Proposal is not acceptance:** retain unselected ideas as PROPOSED/DEFERRED/REJECTED rather than silently deleting them or promoting them to scope.
3. **Shared-branch collision handling:** one lead writer per shared work item; re-fetch after rejected SHA writes; use disjoint paths or an isolated branch; never force-push over another writer.
4. **Exact-SHA CI retention:** CI proves only its exact source/test SHA and scope; cancellation is not failure; a docs-only commit does not create new test evidence.
5. **Lean task packets:** link canonical rules instead of copying them; record exact blobs and observable completion evidence.
6. **Research discipline:** check platform fit, security boundary, licence, maintenance and transitive dependencies before reuse.

The active `AI_COLLAB/kit/docs/WORK_PROTOCOL.md` already covers bounded tasks, write-ahead commits, small file reads, evidence labels, one lead writer, reuse checks and exact-SHA CI. The recommended follow-up is a surgical addition of only the missing authority-precedence and concurrent-write wording there, plus a short pointer from BOOT if necessary. Do not create another full protocol.

## 4. Reconciliation decision

**Recommendation: do not merge PR #4 as-is.** Its branch is 312 commits behind the current working branch and has a stale competing entrypoint. Its useful content is small enough to extract selectively without importing its seven-file snapshot.

**Owner-controlled PR disposition:** keep PR #4 OPEN/DRAFT until the owner chooses whether to close it after selective incorporation. No close, merge, rebase, force-push or PR edit is performed by this reconciliation.

**No product effect:** this proposal concerns collaboration process only. It does not alter PocketCode source, tests, runtime/provider/database/transport, budget, acceptance IDs, security boundary or release gate.

## 5. Verification limits

- PR state, title, draft flag, head/base refs, PR head SHA, changed-file list and branch comparison were fetched from GitHub.
- The seven changed PR files were fetched and reviewed in targeted ranges; the old CHAT_START_HERE was fetched whole because it is 64 lines, and the task template whole because it is 69 lines.
- No local merge simulation or conflict-resolution test was run.
- No PR checks or product tests were run as part of this review.
- The recommendation is a review artifact, not an indication that PR #4 has been reconciled in GitHub.

**Next action:** owner decides whether to close PR #4 after the small set of process improvements has been merged into the canonical working-branch protocol. Until then it remains an untouched draft.
