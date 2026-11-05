import test from 'node:test';
import assert from 'node:assert/strict';
import {
  DEFAULT_TASK_POLL_INTERVAL_MS,
  MIN_TASK_POLL_INTERVAL_MS,
  taskPollInterval,
} from './task_poll_interval.ts';

test('uses a one-second default when no server hint is supplied', () => {
  assert.equal(taskPollInterval(), 1_000);
  assert.equal(taskPollInterval(undefined, undefined), DEFAULT_TASK_POLL_INTERVAL_MS);
});

test('floors zero and smaller server hints to the minimum', () => {
  assert.equal(taskPollInterval(0), MIN_TASK_POLL_INTERVAL_MS);
  assert.equal(taskPollInterval(5), MIN_TASK_POLL_INTERVAL_MS);
  assert.equal(taskPollInterval(-100), MIN_TASK_POLL_INTERVAL_MS);
});

test('honors the largest supplied server hint', () => {
  assert.equal(taskPollInterval(50), 50);
  assert.equal(taskPollInterval(50, 250, undefined), 250);
});
