# MCP Tasks poll-interval helper (research reference only)

This folder contains a small source-level reuse candidate from the MCP Tasks extension. It is not part of PocketCode product code, an approved runtime choice, or a dependency decision.

## Source and license

- Upstream repository: https://github.com/modelcontextprotocol/ext-tasks
- Upstream commit: `cc9aaac1047a9440b07486e38f37060bbebeef4c`
- Upstream file: `packages/ext-tasks/src/client/execution.ts`
- Upstream blob: `60f097b5accc6e4582f57ac7d8c8215a2357202e`
- Package: `@modelcontextprotocol/ext-tasks` 0.2.3
- License: Apache-2.0; full upstream license is copied to `LICENSE`.
- Copy scope: only the two poll interval constants and `taskPollInterval` helper, with source attribution. No MCP protocol implementation or external package code is copied.

## Behavior

The helper uses 1,000 ms when the server supplies no polling hint and clamps supplied hints to at least 10 ms. This prevents a missing hint from becoming a 10 ms busy loop (100 requests per second per task), while respecting a larger server-requested cadence. It is an interval selector only. It does not perform network requests, retries, task recovery, deadline enforcement, cancellation, or server-side execution.

## Important integration constraints

1. Treat the server hint as untrusted protocol input. Validate that it is a finite, non-negative number before calling the helper. The upstream TypeScript signature is a compile-time type, not runtime validation.
2. Apply a platform timer ceiling separately. The upstream implementation has a separate safe-timer helper; this extracted helper does not cap large values.
3. Polling is only a fallback when a durable event stream or push update is unavailable. Do not poll when a push stream already provides authoritative progress.
4. This helper is not a security boundary or sandbox.
5. Do not treat this isolated reference test as product or device acceptance.

## Reproducible local test

Requires Node.js with built-in TypeScript type stripping (Node 22.6+):

```sh
node --experimental-strip-types --test task_poll_interval.test.mjs
```

The test intentionally covers the extracted function's existing behavior only. It does not add different semantics to upstream code.
