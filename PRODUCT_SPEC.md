# PocketCode Product Specification

**Status:** Draft for validation  
**Product name:** Provisional  
**Last reviewed:** 2026-10-20

## 1. Problem

People increasingly receive code from AI assistants, but code generation is not the same as successful execution. A user on a phone may have no practical way to install dependencies, run the program, inspect files and errors, or return precise evidence to an AI for correction.

## 2. Target user hypothesis

Primary early user: someone who uses AI to create or modify scripts and small programs, but often has only a phone available or wants to work away from a desktop.

Potential users include beginners, students, hobbyists, and developers who need a portable execution and debugging workflow. These groups may have different needs; interviews and prototype tests must narrow the initial audience.

## 3. Core job to be done

“When I receive code from an AI or write a small program on my phone, help me run it safely, understand what actually happened, and iterate without needing a PC.”

## 4. Proposed core loop

1. Create a workspace or open a small project.
2. Paste code or add files.
3. Choose a supported runtime and environment.
4. Run the code in an isolated execution environment.
5. Inspect stdout, stderr, exit status, timing, and output files.
6. Share a compact, redacted execution report with the AI assistant of the user's choice.
7. Apply a proposed change, review what changed, and rerun.
8. Save or export the project and its useful evidence.

The AI handoff may initially be copy/paste rather than direct integrations. This keeps the product provider-neutral and avoids prematurely depending on multiple AI APIs.

## 5. MVP scope candidate

- Responsive mobile UI usable in iOS Safari and Android browsers.
- One remote runtime, provisionally Python.
- Code entry and a small project file list.
- Run, cancel, and server-enforced timeout.
- Streaming or promptly refreshed stdout/stderr, where supported.
- Exit code and clear distinction between success, program failure, timeout, cancellation, and infrastructure failure.
- Output-file listing and download for safe supported file types.
- Recent execution history with timestamps and execution status.
- Copyable execution report with relevant source/runtime metadata and redaction.
- Basic authentication and per-user resource limits before private workspaces are offered.
- Automated tests for the execution contract and major failure modes.

## 6. Explicit non-goals for the first MVP

- A complete desktop IDE replacement.
- Every programming language or arbitrary operating-system access.
- Running arbitrary code directly on the phone with no sandbox limitations.
- An AI model of our own.
- Required integration with one specific AI provider.
- Unrestricted outbound network access from executed code.
- Persistent servers or daemons started by user code.
- Guaranteed support for large builds, GPU workloads, or long-running jobs.
- Native iOS and Android apps before the web prototype validates demand.

## 7. Product principles

- Evidence over claims: show what actually ran and the result.
- Provider-neutral: support useful workflows with any AI assistant, even without API integration.
- Mobile-first: primary flows must work with touch, small screens, and unreliable connections.
- Secure by default: user code is untrusted, resource-constrained, and isolated.
- Honest capability boundaries: communicate unsupported APIs, packages, networking, and platform behavior.
- Portable ownership: users should be able to export their code and data.
- Incremental complexity: add runtimes only when there is a real user case and a safe execution strategy.

## 8. MVP acceptance criteria

A first vertical slice is not complete until tests demonstrate that:
- a supported program executes in an isolated worker;
- successful output and generated files can be retrieved;
- syntax/runtime errors return useful stderr and a non-success status;
- excessive or infinite work is stopped by enforced limits;
- cancellation and timeout are distinguishable;
- one user's workspace and results cannot be read by another user;
- worker cleanup occurs after completion or failure;
- logs and reports do not expose configured secrets;
- the UI handles lost connections and infrastructure errors without falsely claiming success.

## 9. Open decisions

- Is the main initial audience beginner AI coders, mobile-first developers, or both?
- Is the core value execution, project editing, AI iteration, or a combination?
- What are the first three real tasks users want to complete?
- Which Python subset and package strategy are needed for the first useful workflow?
- What are acceptable run latency and cost per execution?
- Should the first prototype be anonymous, invite-only, or authenticated?
- What evidence would justify native apps instead of a PWA?
- What pricing, if any, do target users consider worthwhile?

Unanswered questions are not approved design decisions.

## 10. RevDev compatibility and shared-core direction

The long-term product vision is to offer the same trustworthy script-execution and diagnostics workflow on PC and phone. RevDev is the reference for the existing PC experience; PocketCode explores the mobile-first experience. The shared foundation to evaluate first is the run lifecycle, result semantics, and copyable report format—not a premature repository merge or frontend rewrite.

A result should use an evidence-based verdict: **PASS** only for a confirmed completed run with exit code 0; **FAIL** for a confirmed program/runtime failure; and **INCOMPLETE** for timeout, cancellation, rejection, or missing trustworthy execution evidence. The exact execution status must remain visible. Reports should include actual bounded stdout/stderr, runtime/version, exit code and duration only when known, output files, and explicit truncation or uncertainty notes. The prominent result block may use RevDev-inspired pink styling, but copied content must remain readable plain text in any AI assistant.

The phone flow should prioritize one Run action and one obvious Copy result action. See [RevDev + PocketCode shared-core proposal](PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md). RevDev implementation details and report compatibility still need to be inspected; shared code, a unified app, and repository migration remain undecided.
