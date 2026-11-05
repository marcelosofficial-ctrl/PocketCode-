// Copyright 2025 The Model Context Protocol Authors.
// Reproduced from @modelcontextprotocol/ext-tasks, packages/ext-tasks/src/client/execution.ts.
// Upstream commit: cc9aaac1047a9440b07486e38f37060bbebeef4c
// Upstream source blob: 60f097b5accc6e4582f57ac7d8c8215a2357202e
// This is an isolated research reference and is not imported by PocketCode product code.

// The floor only clamps server-suggested cadences, because a server hint of
// 0ms would otherwise turn every poll loop into a busy-wait.
export const MIN_TASK_POLL_INTERVAL_MS = 10;
// Polling falls back to one request per second when the server offers no
// pollInterval hint, because a 10ms fallback is 100 requests/second/task and
// overwhelms both sides under ordinary concurrent workloads.
export const DEFAULT_TASK_POLL_INTERVAL_MS = 1_000;

/** Resolves the polling cadence from server hints, floored and defaulted. */
export function taskPollInterval(
  ...suggestedIntervals: readonly (number | undefined)[]
): number {
  const hints = suggestedIntervals.filter(
    (interval): interval is number => interval !== undefined,
  );
  if (hints.length === 0) return DEFAULT_TASK_POLL_INTERVAL_MS;
  return Math.max(MIN_TASK_POLL_INTERVAL_MS, ...hints);
}
