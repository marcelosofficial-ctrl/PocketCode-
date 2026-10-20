# Controlled Python Execution Proof — Runbook

**Status:** Prepared, not executed. Requires explicit owner approval before creating a provider account, adding credentials, or running a live provider workload.  
**Target:** One disposable Modal Sandbox as the leading candidate for evaluation; provider-neutral test expectations.  
**Purpose:** Verify the smallest useful execution path without building the whole app.

## Safety gates before the first run

Do not start unless every item is checked:

- [ ] Owner explicitly approves the selected provider and the proposed live test.
- [ ] Current account plan, included credits, billing controls, and budget/usage alerts have been reviewed. No assumption that credits guarantee a zero bill.
- [ ] Provider SDK/API version and exact sandbox product are recorded.
- [ ] One fresh disposable sandbox per test run; no reuse across unrelated tests.
- [ ] Network egress is explicitly blocked in provider configuration, not merely by environment variables. For Modal, set `block_network=True` and verify it in the resulting sandbox configuration.
- [ ] No credentials, API tokens, private data, SSH keys, cloud metadata credentials, or production secrets are present in the sandbox or test input.
- [ ] Server-side absolute wall-time, CPU, memory, process, input-size, output-size, file-count, and total-output limits are configured and documented.
- [ ] There is a tested way to terminate a timed-out or cancelled process and destroy the sandbox.
- [ ] Only harmless synthetic data is used. Do not install packages or enable general Internet access.
- [ ] Record actual spend/usage if the provider exposes it; stop immediately if billing behavior differs from expectations.

If any gate is unknown, stop and document the unknown rather than trying the workload.

## Test order

Run each test in a new disposable sandbox unless the test specifically verifies input/output files within one run. Save raw evidence privately during testing; only publish sanitized summaries and never commit credentials, raw environment dumps, or private data.

### PC-RUN-001 — Successful execution

Source:
```python
print("POCKETCODE_PROOF_OK")
print(6 * 7)
```

Expected: exit code `0`; stdout contains exactly `POCKETCODE_PROOF_OK\n42\n`; stderr empty; terminal status `succeeded`. Capture provider-reported runtime and duration, if available.

### PC-RUN-002 — Syntax error

Source:
```python
def broken(:
    pass
```

Expected: non-zero exit code and a Python syntax error; terminal status `program_failed`, not `infrastructure_failed`. Do not assert exact traceback paths or line formatting across Python builds.

### PC-RUN-003 — Runtime exception

Source:
```python
print("before error")
raise ValueError("POCKETCODE_EXPECTED_EXCEPTION")
```

Expected: stdout includes `before error`; stderr or provider error output identifies `ValueError`; non-zero exit; status `program_failed`.

### PC-RUN-004 — Server-enforced timeout

Source (run only after timeout enforcement and termination have been confirmed):
```python
while True:
    pass
```

Configure a short server-side deadline, initially 2 seconds if the provider supports it. Expected: the trusted coordinator/provider stops the process, records `timed_out` only with evidence that the deadline fired, and confirms the sandbox/process is terminated. A client-side browser timeout alone is not a pass.

### PC-RUN-005 — Cancellation

Start a bounded long-running test only after the termination control is available. Request cancellation through the server/provider API. Expected: cancellation is confirmed and the final state is `cancelled`, or the API reports uncertainty honestly. Never claim cancellation based only on hiding the UI or closing the browser.

### PC-RUN-006 — Bounded output

Source:
```python
for i in range(10000):
    print("POCKETCODE_OUTPUT_LINE", i)
```

Configure a small server-side output cap. Expected: captured output does not exceed the cap; response explicitly says output was truncated; the run cannot exhaust memory by returning an unbounded log. Record whether the provider buffers all output before PocketCode can cap it.

### PC-RUN-007/008 — Input and output files

Upload a synthetic file named `input.txt` containing exactly `pocketcode-file-input-v1\n`.

Source:
```python
from pathlib import Path

data = Path("input.txt").read_text(encoding="utf-8")
Path("result.txt").write_text("copied:" + data, encoding="utf-8")
print("input_bytes", len(data.encode("utf-8")))
```

Expected: the program reads the supplied file; `result.txt` is downloadable only through the authenticated run result; downloaded bytes match the expected bytes exactly. Confirm that a different run cannot fetch the file by guessing an ID or path.

### PC-RUN-010 — Egress default-deny

Do not probe cloud metadata endpoints, internal networks, or arbitrary public hosts until the isolation/network configuration is reviewed and the owner explicitly approves the test scope. First verify the provider's configured block-network setting and run only a controlled harmless connectivity check to an explicitly approved test endpoint, if one is necessary.

Expected: the sandbox's effective policy matches the configured deny-by-default requirement. A configuration flag alone is not evidence that bypasses, proxy paths, DNS, or private targets are blocked; record this test as incomplete until the approved network test verifies the boundary.

## Evidence record template

Create one record per test with these fields:

- Test ID and date/time (UTC):
- Provider, exact product, plan, SDK/API version:
- Sandbox configuration (CPU, memory, disk, network policy, timeout):
- Input fixture identifier/hash (no secrets):
- Expected result:
- Observed terminal state / exit code:
- stdout/stderr summary and truncation indicator:
- File names, sizes, and hash of expected/downloaded bytes where applicable:
- Start/cold-start and run duration, source of timing:
- Cancellation/termination/cleanup confirmation:
- Usage/cost evidence from provider:
- Outcome: PASS / FAIL / BLOCKED / INCONCLUSIVE:
- Evidence location (private if it contains raw logs):
- Follow-up or unresolved question:

A test is **PASS** only if observed evidence matches the expectation. Use **BLOCKED** for an unapproved action or missing prerequisite and **INCONCLUSIVE** when the provider cannot supply trustworthy evidence.

## First proof exit criteria

The first proof is useful only if PC-RUN-001, 002, 003, 004, 006, 007, and 008 produce the expected evidence; cancellation and network enforcement must be recorded honestly as pass, fail, or blocked. Do not proceed to public multi-user use until isolation, authorization, network boundaries, quotas, cleanup, and abuse controls are tested. This runbook does not itself prove any test has passed.
