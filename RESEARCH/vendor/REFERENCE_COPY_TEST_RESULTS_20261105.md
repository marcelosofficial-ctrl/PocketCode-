# Reference-code copy verification record — 2026-11-05

**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Purpose:** Record local tests of the two isolated third-party-derived reference utilities. This is not a PocketCode product test or acceptance result.

## Environment

- OS: Linux container
- Interpreter: CPython 3.13.5
- Test framework: standard-library `unittest`
- Workspace: temporary isolated directory `/tmp/pocketcode_vendor_test/`
- No network calls, provider, account, billing, production service or app runtime used.

## OpenHands atomic text writer

Upstream:
- Repository: `OpenHands/software-agent-sdk`
- Commit: `2b4d980b6a54ef6685e4337e7643c40ec24be1bb`
- Source blob: `cdf2b7e6807d135d6386270e1988467009543701`
- Copied PocketCode helper blob: `cdf2b7e6807d135d6386270e1988467009543701` (exact Git blob match)
- PocketCode test blob: `4876a3652517bb57d4a7ba59697f693be0cc1448`
- Upstream MIT LICENSE blob: `b0bd86a6335a564bd3766666bebbf014fd6a8013`

Command:
```bash
python -m unittest discover -s /tmp/pocketcode_vendor_test/openhands -v
```

Result:
- 5 tests run
- 5 passed
- 0 failed
- 0 skipped
- Duration: 0.010 s

Covered: UTF-8 write and replacement, same-directory temporary file, temporary cleanup, previous-target preservation on replace failure, POSIX mode 0600, and temp suffix recognition.

## Mini-Coding-Agent workspace path guard

Upstream:
- Repository: `rasbt/mini-coding-agent`
- Commit: `717cae4ff10d01773bd12951f62a575825053414`
- Upstream source file blob: `1bf2403e5033227e24954faad7f7ba4442f7e4c2`
- Adapted PocketCode helper blob: `d91b205e6c9a23732fb95a214ddcac0731b0c27f` (includes the required Apache-2.0 modification notice)
- PocketCode test blob: `a244c6c0db6e884d9e0c6ae51c393c87a7a36435`
- Upstream Apache-2.0 LICENSE blob: `1e79798da4aac546989b7ca4f26bf1acfea64864` (PocketCode license blob exactly matches upstream)

Command:
```bash
python -m unittest discover -s /tmp/pocketcode_vendor_test/workspace_paths -v
```

Result:
- 8 tests run
- 8 passed
- 0 failed
- 0 skipped
- Duration: 0.010 s

Covered: workspace root and nested files, non-existent target under an in-root parent, parent traversal, absolute outside path, symlink escape, internal symlink, unrelated root and missing workspace root.

## MCP Tasks poll-interval helper

Upstream:
- Repository: `modelcontextprotocol/ext-tasks`
- Commit: `cc9aaac1047a9440b07486e38f37060bbebeef4c`
- Source file: `packages/ext-tasks/src/client/execution.ts`
- Source blob: `60f097b5accc6e4582f57ac7d8c8215a2357202e`
- License: Apache-2.0; the full license is retained adjacent to the copied helper.

Copied reference: `RESEARCH/vendor/mcp-tasks/task_poll_interval.ts`. The companion test imports the TypeScript source directly through Node's experimental type stripping.

Command:
```bash
node --experimental-strip-types --test task_poll_interval.test.mjs
```

Environment:
- Node.js 22.16.0
- Built-in `node:test` and `node:assert/strict`
- No npm install, network request, MCP server, provider, service or account

Result:
- 3 tests run
- 3 passed
- 0 failed
- 0 skipped

Covered: one-second fallback when no hint exists; 10 ms floor for zero/short/negative hints; largest supplied hint selected.

Limitations: helper only. No runtime validation of untrusted values, timer maximum, polling loop, task protocol, reconnect, cancellation, durability, concurrency or PocketCode integration is tested. Node reports type stripping as experimental. No product code imports this file.

## Scope and limitations

These tests verify only the isolated helper functions under Linux/CPython 3.13.5. They do not verify:
- PocketCode imports or product integration;
- iOS, Android, Windows or browser behavior;
- ACL, reparse point, hard link, mount or archive semantics;
- time-of-check/time-of-use protection for later file opens;
- parent-directory fsync or power-loss durability;
- concurrency, locking, compare-and-swap, append-only event storage, run/attempt identity, evidence provenance or artifact release;
- hostile-code containment, egress isolation or process-tree teardown.

Both folders remain reference-only under `RESEARCH/vendor/`; product code does not import them. Test PASS must not be cited as product acceptance or as proof of a secure execution boundary.
