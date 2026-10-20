# PocketCode First-Run Workflow

**Status:** Proposed MVP workflow for validation  
**Purpose:** Turn the product idea into testable tasks before selecting infrastructure.

## Primary scenario: run and diagnose a small Python script from a phone

### User story

As a person using an iPhone or Android phone without access to a PC, I want to paste a small Python program, run it in a clearly described environment, inspect what happened, and share the real result with an AI assistant so I can improve the program.

### Starting task

The first demonstration task should be useful but narrow: accept a small Python script that processes a provided text or CSV file and creates a result file. It exercises source input, file input, execution, output, errors, and file download without requiring a complex build system.

### Main path

1. Open the PocketCode mobile workspace in a phone browser.
2. Start a new temporary workspace.
3. Paste a Python script or add a small text/CSV input file.
4. See the selected runtime and its limitations before execution.
5. Press Run.
6. See a clear state: submitting, queued, running, succeeded, failed, timed out, cancelled, or infrastructure error.
7. Inspect stdout, stderr, exit status, and duration.
8. Download supported generated files.
9. Copy a structured execution report containing the runtime version, status, exit status when available, bounded output, and file list.
10. Paste that report into the user's AI assistant, apply a suggested correction, and rerun.

### Required error scenarios

- Syntax error.
- Runtime exception.
- Infinite loop or a program that exceeds the wall-clock limit.
- Excessive output.
- Invalid or missing input file.
- User cancellation.
- Lost connection while a run is in progress.
- Execution service unavailable.
- Generated file missing or too large to return.

The interface must distinguish program failure from infrastructure failure. It must never show success merely because the API accepted a run request.

## Secondary scenarios to validate

### A. Repair AI-generated code

The user pastes code that fails, runs it, copies the actual error report to an AI, reviews the changed code, and reruns it.

### B. Transform a file

The user supplies a small CSV or text file, runs a script, and downloads the generated output. This tests whether PocketCode offers value beyond a console-only code runner.

### C. Work with multiple files

The user adds a small project containing a main script and one helper module. This is intentionally not a full repository or package-manager workflow in the first test.

## Explicit first-version boundaries

- Python only for the first execution proof.
- No promise that arbitrary third-party packages are available.
- No arbitrary outbound network access by default.
- No persistent background processes.
- No root/administrator access.
- No secret credentials passed into user programs.
- Resource, upload, output, and duration limits must be enforced server-side.
- Do not use a canned output as if code actually ran. A design prototype must label simulated states and sample output clearly.

## Proposed acceptance tests

A first vertical slice is credible only when these tests are demonstrated against the chosen execution backend:

1. A valid script returns the expected output and a successful terminal status.
2. A syntax error returns an understandable failure and useful stderr.
3. A runtime exception returns a non-success status and diagnostic output.
4. A time-limited program is stopped by a server-enforced deadline.
5. Cancellation is reflected accurately and the worker is stopped or safely allowed to terminate.
6. Output is truncated or rejected safely when a limit is exceeded.
7. A generated file can be downloaded and its content verified.
8. An uploaded input file is available only inside that run's workspace.
9. A run cannot read another user's files or application secrets.
10. Worker resources and temporary files are cleaned up according to the defined policy.
11. Connection loss does not cause the UI to invent a result.
12. The copied report is useful for debugging and does not contain secrets.

## Questions to answer through user testing

- Does the user want a code editor, a runner, or a simple “test this AI code” tool?
- Is file transformation more valuable than console output alone?
- What is the smallest useful file/project size?
- Is copy/paste to an AI assistant acceptable for the first version?
- What wait time is acceptable before a result feels broken?
- Would users return to the product for a second task in the same week?
- Would they pay for reliable execution, and at what usage pattern?

## Decision gate

Do not build broad project management, Git, direct AI-provider integrations, or additional runtimes until the primary scenario has been observed with target users and the execution proof passes the safety and reliability tests.
