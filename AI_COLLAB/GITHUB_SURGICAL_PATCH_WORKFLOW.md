# GitHub-only surgical source patch procedure

Purpose: make narrow edits to large source/test files without copying entire files into chat, while avoiding blind overwrites.

## Safe workflow
1. Fetch the live branch head and target file's complete UTF-8 content programmatically. Do not print large content.
2. Apply a deterministic string patch in memory. Each patch must use exact, unique anchors; assert each anchor count is exactly one before changing it.
3. Assert the resulting file has the expected change (and unchanged prefix/suffix or unchanged occurrence counts as appropriate). Reject ambiguous anchors.
4. Create a new Git blob with the complete modified content, create a tree based on the current head's tree containing that blob, create a commit with current head as parent, and move the branch ref using an expected-head compare-and-swap.
5. If the lease fails, stop and inspect the new head. Never retry against an unseen head.
6. After commit, fetch the exact path and commit/tree again to verify the patch landed. Tests are a separate step and must report actual output.

## Guardrails
- Keep patches small (one or two files, preferably under 200 changed lines).
- Do not replace a large file by manually reconstructing it from line excerpts.
- Use full-content fetch only inside the orchestrator; source text remains unprinted. Do not rely on hidden state across calls.
- Treat successful GitHub API writes as commit evidence only; they do not establish runtime correctness.
- If source patching needs semantic context, read targeted line ranges first and preserve unrelated content byte-for-byte.
- Checkpoint commits must use the latest blob SHA and remain the final write of the turn.

This method avoids oversized chat output and stale-head overwrites, but it is still a full-blob replacement internally. It does not make partial GitHub blob edits possible.
