# Cline Workspace Checkpoint and Restore Audit — 2026-11-05

**Upstream repository:** https://github.com/cline/cline  
**Reviewed revision:** \`d3ecc4890e8f9bcb77182b96c77fa90575e8e145\`  
**License:** Apache-2.0  
**Status:** Source and test inspection. No Cline source copied. No PocketCode product code, runtime or workspace implementation changed.

## Executive decision

A recoverable workspace checkpoint is a real product feature worth adding to PocketCode's roadmap. It directly supports the stated goal of approving or reviewing corrections, rerunning them safely, and recovering from a bad multi-step change without losing the AI conversation or evidence.

Cline is the strongest inspected source for the workspace checkpoint and restoration problem. Reuse its **design invariants and test cases**, not its implementation wholesale:

1. Create a checkpoint before a bounded set of potentially mutating operations.
2. Preserve the user conversation and the task/evidence record separately from workspace state.
3. Capture tracked and untracked non-ignored files, and state honestly what was not captured.
4. Never move a branch pointer backward if HEAD changed after the checkpoint. Use an expected-old compare-and-swap guard.
5. Make restoration transactional: preserve the current workspace first, then either commit the restore or roll it back.
6. Treat failed, partial, stale, too-large or unsupported snapshots as visibly incomplete, not as a complete recovery point.
7. Keep the real user Git history and index under user control. Choose explicitly between a separate shadow object store and carefully namespaced refs in the workspace repository.

**Priority recommendation:** P1 product feature, with a P0 safety precondition for any future unattended multi-file editing or automatic repair: the system must have a tested reversible checkpoint or must require explicit confirmation before the destructive operation. A checkpoint feature itself is not yet implemented or tested in PocketCode.

## 1. What Cline documents

Cline's public checkpoint documentation says checkpoints allow code rollback while retaining the conversation. It describes a shadow Git repository separate from the project Git history, with checkpoints after tool use, full file snapshots including untracked files, and separate restore choices for files, task messages, or both. It also notes storage/performance costs in large repositories. Source: [Cline checkpoint documentation](https://github.com/cline/cline/blob/main/docs/core-workflows/checkpoints.mdx).

The user-facing feature is relevant to PocketCode because it separates two distinct recovery questions:
- "The work is useful, but the conversation needs to go back to an earlier instruction."
- "The conversation is useful, but the workspace changes need to be undone."

These should not be one destructive undo operation.

## 2. Source-level implementation findings

### 2.1 Checkpoint creation

Reviewed file:
- \`sdk/packages/core/src/hooks/checkpoint-hooks.ts\`
- Blob: \`5dd05ebe646fa02ef1b280b35c4898844f1639e8\`

The inspected SDK hook records checkpoint metadata consisting of a Git ref, creation time, run count and checkpoint kind (\`stash\` or \`commit\`). It uses session metadata to avoid overwriting the original pre-run checkpoint during a resumed/replayed run. The hook's run count is span-aware so compacted conversation messages do not simply reset numbering.

For a workspace that is already a Git repository, the hook:
- uses \`git stash create\` to snapshot tracked worktree changes without resetting the user's workspace;
- explicitly enumerates untracked but non-ignored files with \`git ls-files --others --exclude-standard\`;
- builds a third-parent commit for the untracked snapshot through a private \`GIT_INDEX_FILE\`, leaving the actual Git index untouched;
- persists the snapshot object under \`refs/cline/checkpoints/{sessionId}/{runCount}\`, keeping it out of the normal visible stash list;
- pins \`core.ignorestat=false\` and \`core.splitIndex=false\` for its scratch index because those repository settings can otherwise break later change detection;
- emits snapshot telemetry containing outcome and duration, not paths or file contents;
- falls back to a HEAD commit checkpoint if a dirty snapshot fails, and records that as a degraded \`head_fallback\` rather than silently calling it a complete worktree snapshot.

Its private scratch index is keyed from a hash of workspace path plus session ID, held under the user's private Cline data directory, and aged out after 14 days without refresh. The source includes special handling for vanished files, stale/corrupt index files, large path lists and nested untracked repositories.

**Important documentation/source distinction:** the public docs describe a separate shadow Git repository. The inspected SDK hook instead invokes Git with \`-C <workspace>\` and writes namespaced refs and a scratch index. In this reviewed path, the checkpoint object is stored in the workspace repository's object database under a private ref, while the user's ordinary branch HEAD and real index are not intentionally changed by checkpoint creation. Do not assume every Cline client/integration uses the same implementation. This is a reason to choose PocketCode's storage boundary deliberately rather than copying the marketing-level phrase "shadow repo".

### 2.2 Diff generation

Reviewed file:
- \`sdk/packages/core/src/session/checkpoint-diff.ts\`
- Blob: \`9c2d77ab6b61272fb010cb54985a40483435126b\`

The diff code:
- compares tracked content, newly untracked files and files that were untracked at snapshot time but later deleted;
- resolves every workspace-relative path and rejects paths escaping the workspace;
- uses \`git cat-file --batch\` / \`--batch-check\` to read many blobs without spawning one Git process per file;
- has a 50 MiB Git output ceiling.

One caution needs to be addressed in PocketCode: the inspected code comments say blobs above the 50 MiB ceiling are skipped and compare as empty. A skipped large file must not be presented as "unchanged" or as a complete diff. PocketCode should surface a per-file unavailable/oversize marker or use streaming/hash comparison that retains honest completeness.

### 2.3 Restore planning and destructive-operation guard

Reviewed file:
- \`sdk/packages/core/src/session/checkpoint-restore.ts\`
- Blob: \`574acd5c1025316a1fb6134f3f1089e4b2d99923\`

The restore implementation has several strong safeguards:

- It validates that the workspace is a Git repository and that the checkpoint ref exists before resetting or cleaning anything.
- It resolves the checkpoint's base commit and compares it with current HEAD.
- If later commits exist, or the branch was rebased/switched, it refuses to move the branch pointer. The error tells the user that the workspace can remain untouched while the conversation alone is restored, or that the user can deliberately move the branch back.
- It moves HEAD using Git's \`update-ref <ref> <new> <old>\` compare-and-swap form. This closes the race between checking HEAD and resetting the worktree.
- It only runs \`git clean -fd\` when the checkpoint has the third parent containing untracked files. It then applies the stash snapshot to restore their checkpoint-time content and remove files created after the checkpoint.
- It deliberately does not remove Git-ignored files such as build output, \`node_modules\` or \`.env\`. Older two-parent stashes and HEAD-only fallback checkpoints cannot reconstruct untracked files, so those files are left untouched instead of risking unrecoverable loss.

The implementation does not claim it can rewind a workspace after arbitrary external Git changes. It refuses when it cannot safely establish that the branch still has the checkpoint's expected base.

### 2.4 Restore transaction

Before destructive restoration, \`beginWorktreeRestoreTransaction\` creates a temporary stash including untracked files, moves it under a private transaction ref and removes it from the ordinary visible stash list. The caller can then:
- \`commit()\`: discard the private recovery ref after the replacement session succeeds;
- \`rollback()\`: reset to the original HEAD, clear newly created non-ignored files and apply the saved snapshot back.

If capture of the temporary restore state fails, it attempts to put the workspace back and raises an aggregate error if both capture and rollback fail. This pattern is especially valuable for PocketCode's proposed correction loop: a correction must not destroy the state that existed immediately before the correction merely because the correction itself or session setup failed.

### 2.5 Tests inspected

Pinned tests:
- \`sdk/packages/core/src/session/checkpoint-diff.test.ts\`, blob \`aa298953533b57aba564d4efbf3df4505f50885a\`.
- \`sdk/packages/core/src/session/checkpoint-restore.test.ts\`, blob \`f5da1142b405f4950bc85c70504ccef6ea3dc9bd\`.
- \`sdk/packages/core/src/hooks/checkpoint-hooks.test.ts\`, blob \`?\` (not pinned in this review).

The inspected hook tests cover one checkpoint per root user run, inclusion of untracked files as a third parent, no overwrite on reopened-session resume, compacted/seeded prompt numbering, clean-worktree HEAD fallback, deduplication, subagent exclusion, snapshot telemetry without paths, stale scratch-index cleanup, disappeared untracked files, nested repositories/gitlinks, stale index-lock recovery and repository settings that would otherwise break change detection. The inspected diff tests cover:
- tracked changes, deleted files and newly untracked files;
- reading checkpoint-time untracked content from a third parent;
- excluding unchanged pre-existing untracked files from the diff;
- deleted untracked files;
- nested file paths containing spaces;
- selecting the nearest checkpoint at or before a requested run.

The inspected restore tests cover:
- invalid checkpoint ref rejection before reset/clean;
- refusal when one or multiple later commits exist;
- refusal after branch divergence/amend;
- preservation of HEAD and current workspace after refused restore;
- restoration of tracked and untracked content;
- removal of files created after checkpoint when the checkpoint actually captured untracked state.

The upstream test source was inspected only. These tests were not executed by PocketCode and are not PocketCode acceptance evidence.

## 3. PocketCode feature design

Implement a workspace recovery abstraction around the existing task/attempt identity. Do not bind it directly to Git as the only workspace type.

### 3.1 Separate identities and state

A checkpoint should record at least:
- checkpoint ID;
- task ID, attempt ID and the operation/pass it protects;
- workspace ID and canonical root identity;
- parent checkpoint ID;
- created-at timestamp plus an ordered per-workspace sequence;
- capture strategy and implementation version;
- tracked/untracked/ignored/oversize coverage summary;
- per-entry path, kind, size, digest and capture result;
- storage reference or snapshot manifest;
- completeness status and any capture failures.

Checkpoint identity must remain distinct from mission/task identity, execution attempt identity and publication operation identity.

### 3.2 Separate restoration choices

Keep three explicit actions:
1. **Restore workspace only:** preserve the current conversation, task history and evidence, and restore files to the selected checkpoint.
2. **Restore task context only:** restore the selected conversation/checkpoint context without modifying workspace files.
3. **Restore both:** require an explicit confirmation that both the workspace and task context will be rewound.

For any workspace restore, show the diff and list of files that will change before applying it. If an external user or process has changed a file since the selected checkpoint, detect the conflict and ask rather than silently overwriting that newer change.

### 3.3 Use reversible workspace transactions

Proposed state sequence:
\`CAPTURE_CURRENT\` → \`VALIDATE_TARGET\` → \`PREVIEW_DIFF\` → \`APPLY_TO_STAGING\` → \`VERIFY_RESULT\` → \`COMMIT_RESTORE\`

Any error before \`COMMIT_RESTORE\` should take the rollback path back to the exact pre-restore workspace. If capture of the current workspace is incomplete or fails, block destructive restoration. Do not delete recovery material until the restored state and the new task/session state are durably committed.

### 3.4 Workspace backends

Define a provider-neutral interface first, then choose a backend after platform research:

| Backend option | Strength | Risk/decision |
|---|---|---|
| Shadow object store / separate Git dir | Strong separation from user's branch, refs and index | More storage, lifecycle, path and symlink complexity; Cline docs describe this model |
| Namespaced refs in existing Git repo | Git object reuse, cheap snapshots and diffs | Shares object DB/config and depends on a valid Git repo; must never modify user HEAD/index |
| File-manifest/object store | Works without Git and can cover arbitrary workspaces | Must implement atomic capture, content hashing, symlink and permissions semantics |
| Hybrid | Git for repositories, manifest store for non-Git/unsupported paths | Two capture implementations need one truthful completeness contract |

No backend is selected here. The source/documentation mismatch above is a reason to keep the storage boundary explicit and independently testable.

## 4. Threats and failure cases PocketCode must handle

1. **External concurrent writer:** another editor, terminal, Git operation or sync client changes files after checkpoint. Refuse or merge on conflict; never silently overwrite.
2. **HEAD moved:** branch advanced, switched, reset or rebased after checkpoint. CAS expected-old pointer and block unsafe restoration.
3. **Incomplete snapshot:** ignored files, oversized binaries, permission-denied paths, symlinks or an interrupted scan. Mark incomplete and do not claim full recovery.
4. **Untracked-file loss:** a file existed before checkpoint but was not included in the snapshot. Never clean it unless the snapshot proves it can be restored.
5. **Capture/rollback failure:** preserve recovery refs/objects and show a blocked/unknown state; don't claim rollback succeeded.
6. **Storage exhaustion:** cap snapshot size and retention, but never silently drop a checkpoint needed by an active operation.
7. **Secret leakage:** checkpoint manifests and diffs may include secrets. Keep private storage permissions, exclude configured sensitive paths only with visible coverage reporting, and never upload contents automatically.
8. **Symlink/path traversal:** canonicalize paths, reject escape from the workspace, and avoid following untrusted symlinks outside allowed roots.
9. **Partial restore:** a restore may fail after some files are written. The pre-restore transaction must allow exact recovery.
10. **Stale checkpoint:** the underlying object/ref was pruned or unavailable. Validate before any destructive step.

## 5. Suggested acceptance tests (proposal only)

Place these under the existing PocketCode test architecture only after implementation authorization. These are test ideas, not new canonical CASE/LOOP IDs and not changes to expected strings.

- Capture a dirty tracked file and verify its content returns exactly.
- Capture an existing untracked file, modify and delete it later, then restore the checkpoint-time content.
- Create a file after the checkpoint and verify it is removed only when the snapshot completeness proves the earlier workspace state.
- Verify ignored files are explicitly preserved or captured according to the selected backend policy.
- Make the snapshot exceed a size limit and verify the checkpoint becomes partial/unavailable instead of a false complete snapshot.
- Change HEAD between preview and restore and verify compare-and-swap refusal before destructive mutation.
- Modify one file externally after checkpoint and verify conflict detection.
- Inject failure after each restore phase and verify the exact pre-restore workspace is recovered.
- Fail to capture current workspace and verify restore is blocked.
- Use a path with spaces, Unicode, nested directories, symlinks and case-sensitive/case-insensitive collisions.
- Ensure the real Git index and current branch are unchanged by checkpoint creation.
- Restart the app/host and recover checkpoint metadata and references.
- Delete a session and verify private checkpoint refs and scratch files are safely retired without deleting user data.

## 6. Roadmap decision and boundaries

**Recommended priority: P1.** A simple diff/restore checkpoint would materially improve user confidence in multi-pass changes and correction loops. Before any future automatic multi-file repair is allowed, a reversible checkpoint or explicit user approval should be a P0 safety gate.

Do not add "every tool call makes a full copy" as a fixed behavior. Capture cost scales with repository size and untracked file count. Use a policy such as checkpoints before/after bounded mutation groups, before destructive operations, and at verified pass boundaries, with incremental snapshots where available.

No checkpoint should replace:
- immutable execution receipt and evidence;
- task/attempt/step identity;
- a visible file diff and operation history;
- user approval for privileged actions;
- real Git commits and branch history;
- backups outside the workspace for data that cannot be safely recreated.

## 7. Verification and non-actions

- Pinned public Cline source and tests were inspected at commit \`d3ecc4890e8f9bcb77182b96c77fa90575e8e145\`.
- No Cline source code was copied into PocketCode.
- No PocketCode source, tests, runtime, workspace or Git operations were executed or changed.
- No mobile, browser or PC runner was selected or tested.
- No PocketCode canonical LOOP/CASE IDs or expected values changed.
- No RevDev P8U/AEC/AWC/P0-D IDs, owner decisions or source code changed by this report.
## 8. Follow-on design pass: backend-neutral checkpoint storage contract

**Status:** Proposed contract for architecture review. Not a frozen schema, implementation, runtime choice, or new canonical acceptance suite. This section reconciles the Cline Git-checkpoint approach with the content-addressed/journal patterns inspected in safe-fs-ops.

### 8.1 Executive decision

Use a **content-addressed immutable snapshot manifest plus a durable checkpoint journal** as the conceptual contract. Permit multiple backend adapters:
- Git object/ref backend when a workspace is a Git repository and its object/ref behavior is proven on the target platform.
- File/object blob backend for non-Git workspaces or where Git metadata must not be touched.
- A browser-local backend only after the actual PocketCode host/runtime is selected and its persistence semantics are tested.

Do not force every workspace into Git. Do not make the user's branch, index, stash, or visible commit history the product's checkpoint database. Do not store checkpoint state only in the chat transcript or an in-memory map.

### 8.2 Core records and immutable identities

Conceptual records (names illustrative):
- `workspace_id`: stable logical workspace identity; not a filesystem path.
- `checkpoint_id`: immutable identity for one capture.
- `checkpoint_sequence`: monotonic sequence within a workspace, allocated by the durable journal.
- `parent_checkpoint_id`: optional prior checkpoint for ancestry; not proof that the snapshots are complete.
- `capture_id`: one capture attempt. A failed retry gets a new capture ID and preserves the failed attempt.
- `restore_id`: one requested restore operation.
- `restore_attempt_id`: one execution attempt to apply a restore.
- `entry_id`: stable within the immutable manifest; identifies a captured path entry.
- `blob_digest`: SHA-256 over exact captured bytes for regular-file content. Symlink target metadata is separately typed and hashed/encoded; never follow a symlink as if it were a regular file.
- `manifest_digest`: SHA-256 over a canonical, versioned serialization of the manifest, including its coverage/completeness declarations.

Task/run/attempt/step IDs remain distinct. A checkpoint may be associated with a task and attempt, but must not replace those identities. A checkpoint is not an execution receipt, PASS verdict, or artifact-release authorization.

### 8.3 Capture coverage is part of the data, not a UI footnote

A snapshot must record an explicit coverage policy and outcome:
- root identity and capture boundary;
- included regular files, symlinks and supported metadata;
- ignored/excluded paths and exclusion rule/version;
- nested repositories or mount boundaries;
- unsupported file types, sockets, devices, FIFOs and reparse points;
- files skipped for size, permissions, mutation during read, path races or I/O failure;
- empty directories and directory metadata, if supported;
- case-sensitivity/collision behavior;
- file count, total bytes and configured limits;
- whether the workspace changed during capture.

Completeness is a computed result, never a default. Suggested states:
- `COMPLETE`: all paths required by the declared capture policy were captured and verified.
- `PARTIAL`: at least one required path or required metadata was not captured.
- `FAILED`: no usable manifest was committed.
- `UNKNOWN`: recovery cannot establish whether capture finished or whether its stored data is intact.

A checkpoint with PARTIAL/UNKNOWN coverage may be useful for inspection or selective recovery, but must never authorize whole-workspace restore or deletion of paths absent from the manifest. A missing manifest entry is not proof that a file did not exist.

### 8.4 Capture and publication ordering

Proposed sequence:
1. Allocate and durably record `capture_id` and intent, bound to workspace identity and capture policy version.
2. Enumerate paths under a defined root policy. Reject path escape, traversal, unsupported link/reparse behavior and ambiguous aliases.
3. For each regular file, capture to a temporary object, hash the bytes actually captured, verify size/digest, then install the immutable blob without replacing an existing digest object.
4. Record each completed blob reference in the capture journal as it becomes durable. A crash must not leave unaccounted partial objects.
5. Recheck file identity/metadata (and where feasible content digest) after read. If the file changed during capture, mark that entry unstable and the snapshot PARTIAL unless a retry captures a consistent version.
6. Canonicalize and hash the manifest. Verify every referenced blob exists and matches its digest.
7. Commit the manifest and transition the checkpoint to COMPLETE only after all required object and metadata checks succeed.
8. Acknowledge checkpoint completion to the caller only after the backend's documented durable-commit boundary succeeds.

A database transaction cannot atomically include arbitrary filesystem/object-store writes. The journal must therefore track staged blobs, manifest publication and cleanup debt explicitly. Content-addressed objects are immutable; the manifest/reference transaction is the logical commit point. Garbage collection may remove only proven-unreferenced objects after a safe retention window and a fresh reference scan.

### 8.5 Restore is a new transaction, not a reverse copy loop

Before changing any workspace path:
1. Authenticate the caller and validate workspace ownership.
2. Validate checkpoint identity, manifest digest, schema version, completeness and every referenced blob.
3. Enumerate the current workspace and compute the proposed change set.
4. Compare current path identity/content against the expected restore base or the state captured during preview. Detect changed, new, missing and type-changed entries.
5. Reject or request explicit resolution for conflicts. Never silently overwrite a file changed after checkpoint creation or preview.
6. Capture a **pre-restore recovery checkpoint** of the current state. If that capture is incomplete, block destructive restore.
7. Persist restore intent and a per-entry action plan before mutation.
8. Apply writes through temporary sibling files/atomic replacement where the platform supports it; record each completed action and verify the resulting digest.
9. Apply deletions only when the selected checkpoint is COMPLETE for the relevant deletion scope and the current entry still matches the exact expected identity/version. Deletion is never inferred from a missing manifest entry in a PARTIAL snapshot.
10. Verify the resulting workspace against the target manifest and commit the restore journal.
11. If any phase fails, restore from the pre-restore checkpoint only when conflict checks still prove that rollback will not overwrite newer external changes. Otherwise stop and require manual intervention.

This is not an all-or-nothing filesystem transaction. It is a recoverable sequence with explicit partial states and conservative stop conditions.

### 8.6 State model and crash reconciliation

Keep checkpoint lifecycle separate from restore lifecycle.

Checkpoint: `CAPTURE_INTENT`, `CAPTURING`, `MANIFEST_STAGED`, `VERIFYING`, `COMPLETE`, `PARTIAL`, `FAILED`, `UNKNOWN`, `EXPIRED`.

Restore: `RESTORE_INTENT`, `PREFLIGHTED`, `PREIMAGE_COMPLETE`, `APPLYING`, `VERIFYING`, `RESTORED`, `ROLLED_BACK`, `CONFLICTED`, `MANUAL_INTERVENTION`, `UNKNOWN`.

These are proposed internal states, not public receipt verdicts or changes to LOOP/CASE acceptance.

On startup, reconcile incomplete operations from durable journal and exact object verification. Never replay a restore action merely because a lease expired. Each action has a stable action ID, restore attempt ID, expected precondition, intended postcondition and observed result. Use a monotonic fencing token if multiple processes/workers can own the same workspace. A process-local mutex is insufficient evidence of cross-process exclusivity.

### 8.7 Backend-specific constraints

**Git backend**
- Cline's use of namespaced refs, a private scratch index, stash-created snapshots and `update-ref <ref> <new> <old>` is a useful reference.
- Preserve the user's actual index and branch. Record whether the snapshot includes tracked, untracked, ignored and nested-repository content.
- Never use `git clean` or move HEAD unless the checkpoint coverage and exact preconditions prove the operation safe.
- Git object existence is not proof of complete workspace coverage; HEAD-only fallback is degraded.
- Validate ref CAS and crash behavior on the actual Git version/platform before relying on it.

**Blob/object backend**
- Immutable digest-named blobs, canonical manifests and no-replace installation are appropriate.
- The manifest commit/reference update is the logical snapshot publication boundary.
- Filesystem atomic rename, fsync and directory durability vary by OS/filesystem. Adapter must declare actual guarantees, not claim universal atomicity.

**Browser OPFS backend**
- Use only if the chosen product host supports it and the app's worker/storage lifecycle is verified.
- Keep database metadata and file blobs logically separate; never treat a database commit as proof that every blob has been synced.
- Query effective SQLite journal/synchronous settings and document the VFS flush/sync behavior.
- Handle quota, eviction, origin-data clearing, single-writer ownership and export/restore.
- OPFS is not the only copy of user data; export must reconstruct a project independently.

### 8.8 Proposed falsification tests (not new canonical IDs)

| Scenario | Required safe outcome |
|---|---|
| Crash after blob write but before journal reference | Orphan object is discoverable and collectible only after safe reference scan; checkpoint remains incomplete |
| Crash after some blob references but before manifest commit | Resume/reconcile same capture or mark PARTIAL; never report COMPLETE |
| File changes while being read | Entry marked unstable/recaptured; no false consistent snapshot |
| Permission denied or oversized file | Explicit partial coverage; absent entry cannot authorize deletion |
| Symlink/reparse point points outside root | Capture link metadata or reject according to policy; never follow outside root |
| Case-colliding names on target filesystem | Reject ambiguous restore or apply platform-specific conflict policy; never silently overwrite |
| Blob digest mismatch or missing object | Checkpoint invalid for restore; no workspace mutation |
| Manifest schema version unsupported | Preserve bytes and journal; no best-guess migration or destructive restore |
| Workspace changes after preview | Precondition/CAS conflict; stop before overwriting newer content |
| Crash after restore action but before action acknowledgement | Read back exact target digest and reconcile; do not repeat blindly |
| Crash halfway through restore | Use pre-restore checkpoint if still safe; otherwise MANUAL_INTERVENTION |
| Pre-restore checkpoint partial | Destructive restore blocked |
| Stale worker resumes after takeover | Fencing rejects writes/actions from old owner |
| Garbage collection races with checkpoint publication | No referenced blob is deleted; collector must use a safe mark/sweep snapshot or generation boundary |
| Export interrupted or quota exhausted | Export marked partial; original workspace and checkpoint remain intact |

These are proposed test cases only. They do not add canonical acceptance IDs or establish test results.

### 8.9 Roadmap and adoption decision

- **P1 feature:** visible workspace checkpoints, diffs and selective restore for the correction loop.
- **P0 precondition:** before unattended multi-file repair or destructive automatic correction, require a verified COMPLETE preimage checkpoint or an explicit user confirmation that accepts the loss risk.
- **MVP:** one workspace writer, bounded snapshot size, explicit coverage report, immutable blobs, manifest digest, pre-restore capture, conflict detection, manual resolution. Avoid multi-writer merge, background GC, and arbitrary filesystem type support in the first slice.
- **Do not implement yet:** until runtime/host selection, storage ownership, target filesystem matrix, schema migration policy and user-visible export requirements are approved.

This proposal complements the provider-neutral recipe/run/attempt model. It must not duplicate execution receipts, remote dispatch reservations, artifact release records or GitHub publisher state. Canonical LOOP-01..14, CASE-01..16 and D-01..D-08 remain unchanged.
