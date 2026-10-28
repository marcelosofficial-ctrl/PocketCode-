# PocketCode — Open-Source Reuse Audit

**Review date:** 2026-10-29  
**Status:** Public-source and repository-document review; no competitor code copied, no build/tests run, no PocketCode runtime selected.  
**Scope:** Find prior work that can reduce PocketCode's custom engineering across phone-first coding, execution lifecycle, truthful evidence, recovery, provider neutrality, and cross-AI continuation.

## Executive decision

**Reuse patterns and conformance ideas now; do not vendor an agent framework or execution runtime yet.** The strongest sources show that many proposed PocketCode features already exist elsewhere. The product hypothesis cannot rely on generic tool logs, mobile AI coding, error handoff, session recovery, or a structured run record as unique by themselves.

The current PocketCode proposal already has valuable foundations: a provider-neutral execution contract, separate user verdict vs exact lifecycle status, unknown evidence kept explicit, bounded stdout/stderr, file metadata, explicit timeout/cancellation semantics, and no PASS without trusted terminal evidence. Keep the existing contract as the one candidate schema; do not fork it into a new “receipt schema.” The best additions from prior art are mostly stronger conformance fixtures and recovery semantics, not more fields or a bigger framework.

## Findings and recommended adoption

### 1. RunSeal — execution protocol, policy and conformance (highest value for contract review)

**Sources:** [RunSeal implementation](https://github.com/runseal-labs/runseal), [RFC-0006 stable execution protocol](https://github.com/runseal-labs/rfcs/blob/main/rfcs/0006-stable-execution-protocol.md), [RFC-0021 real-time protocol v2](https://github.com/runseal-labs/rfcs/blob/main/rfcs/0021-realtime-execution-protocol-v2.md), [RFC-0016 adversarial conformance](https://github.com/runseal-labs/rfcs/blob/main/rfcs/0016-adversarial-conformance-harness-and-case-format.md). Repository license: Apache-2.0. Maintainer status: technical preview; Windows reference backend, other platform backends experimental. This is not an independent security audit.

**Useful patterns to map onto PocketCode:**
- One lifecycle owner is responsible for start, streaming output, cancellation/timeout, cleanup and terminal publication; avoid contradictory “CLI says cancelled / worker still running” states.
- Separate the execution's own result from wrapper/coordinator errors. RunSeal's CLI wrapper status and child process exit status are distinct.
- Explicit capability discovery and fail-closed behavior when a requested capability is unsupported; a skipped test is not a pass.
- Ordered structured events / JSONL audit, stable execution IDs, versioned protocol, immutable policy identity for the duration of a run, and adversarial black-box conformance tests.
- Treat timeout/cancellation as proven only when the execution boundary confirms it; do not infer process death from a client timer.

**PocketCode application:** use these as cross-checks for the existing proposed lifecycle contract and the PR #3 reconciliation. Add missing expectations to the fixed-task/conformance matrix only when they clarify a real gap. Do not copy RunSeal's OS-specific sandbox code: it is Rust/desktop OS infrastructure and is not an iOS/Android/browser sandbox drop-in. Do not import RunSeal's state machine wholesale; PocketCode's accepted lifecycle vocabulary and PR #3 status still require reconciliation.

### 2. AndroidHarness — phone-native task receipts, recovery and diagnostics (highest value for phone UX patterns)

**Sources:** [AndroidHarness](https://github.com/Sanuu7/AndroidHarness), [README and implementation overview](https://github.com/Sanuu7/AndroidHarness/blob/main/README.md). Root license: MIT. Android/Kotlin-specific; maintainer-described features, not independently verified by this review.

**Useful patterns:**
- Persist completed tool results before advancing to the next model action; after interruption, resume from a durable checkpoint instead of replaying completed writes.
- If an operation's completion is uncertain, show a recovery/inspect step instead of blindly repeating it.
- Build diagnostics from a fixed whitelist of safe fields and state missing logs/collection failures explicitly.
- Name the actual execution backend in the receipt; use a digest to reject stale edits.
- Use a doctor-style capability self-test to report what works on the current device, instead of a blanket “supported” label.

**PocketCode application:** map these patterns to the future AI Workflow Director continuation capsule, report privacy requirements, and mobile preflight. Keep the first Director evaluation local/manual and supporting. A general phone-agent implementation is not the target, and AndroidHarness is not an iOS implementation. Do not copy Kotlin UI/runtime code into the current platform-neutral product.

### 3. PhoneCode — crash-safe sessions and strict runtime claims

**Sources:** [PhoneCode](https://github.com/dttdrv/phonecode), [mobile backend boundary](https://github.com/dttdrv/phonecode/blob/main/MOBILE_BACKEND.md), [third-party inventory](https://github.com/dttdrv/phonecode/blob/main/THIRD_PARTY.md). Original project code: Apache-2.0. Its inventory identifies additional third-party components with separate licenses, including PRoot (GPL-2.0 family) and talloc (LGPL-3.0 family). Android-specific, and its production runtime design is in active migration per its documentation.

**Useful patterns:**
- Crash-safe sessions, atomic state writes, explicit tool checkpoints, bounded retries and explicit recovery when the OS interrupts a task.
- Keep provider credentials and app state outside the untrusted execution guest; expose only explicit files/channels.
- Make unsupported runtime boundaries explicit. A path translator such as PRoot is not automatically a security sandbox.
- Use a release gate that blocks distribution until runtime isolation, licensing/provenance and device lifecycle evidence pass.

**PocketCode application:** add these as future implementation/release checks, not as claims about our current static prototype. Do not vendor PhoneCode's whole runtime or any bundled dependency before component-level license/provenance review. Its Android-specific VM work does not resolve iOS execution or browser sandbox decisions.

### 4. OpenHand — provider-neutral modularity and failure taxonomy

**Sources:** [OpenHand repository](https://github.com/ricardo-foundry/openhand), [error-handling strategy](https://github.com/ricardo-foundry/openhand/blob/main/docs/ERROR_HANDLING.md). License: MIT. TypeScript monorepo, relatively small by agent-framework standards, but it is a general agent runtime rather than a tiny execution receipt library. Its own docs warn that its allowlist sandbox runs under the host UID and is not OS-level isolation unless placed in a stronger boundary.

**Useful patterns:**
- A narrow provider interface so provider changes do not leak throughout product logic.
- Separate user/input errors, provider errors, sandbox/execution errors and internal errors; retry only known transient classes with bounded attempts and delay.
- Do not show raw provider responses, stack traces or headers to users; retain safe structured diagnostics with correlation IDs.
- Test protocol adapters and streaming failure paths with fake providers and deterministic fixtures.

**PocketCode application:** retain the existing provider-neutral boundary. Use the error taxonomy as a review checklist when the contract/error categories are reconciled. Do not adopt its runtime wholesale or mistake command allowlists for an OS sandbox. Exact TypeScript modules are a future candidate only if PocketCode chooses a compatible TypeScript runtime and the module saves more work than its dependencies add.

### 5. Pairlet — remote-host continuity and capability matrix

**Sources:** [Pairlet](https://github.com/heypandax/pairlet), [contributor architecture and test guidance](https://github.com/heypandax/pairlet/blob/main/CONTRIBUTING.md), [observability documentation](https://github.com/heypandax/pairlet/tree/main/docs/observability). Root project license: MIT (verify all transitive components before code reuse). Pairlet's primary execution model requires a separate computer/daemon; it is not a no-PC execution substitute.

**Useful patterns for a later host-available scenario:**
- Reconnect with missed event backfill; explicit approval prompts; safe deny on approval timeout.
- A capability matrix per backend rather than pretending every agent supports the same operations.
- Distinguish client-side observation from end-to-end correlation and from server-confirmed completion.
- Keep diagnostics opt-in, structured and privacy-filtered; record partial/incomplete log reads explicitly.

**PocketCode application:** use the backend capability matrix if a remote-PC option remains in the study. Do not make Pairlet or a remote daemon the default while execution location remains undecided and PC access is unavailable.

### 6. OpenHands — event history and sandbox/runtime separation

**Sources:** [OpenHands](https://github.com/OpenHands/OpenHands), [OpenHands sandbox server](https://github.com/OpenHands/sandbox-server). Core repositories are MIT-licensed, with an enterprise-directory carve-out in the main repository. Large and fast-moving; check the exact subrepository and directory license before reuse.

**Useful patterns:** separate UI/client, agent SDK, server/control plane and execution workspace; keep a reviewable event history; use isolated workspaces; expose stable client abstractions rather than coupling UI directly to one runtime.

**PocketCode application:** architecture inspiration only. The full framework is too broad for our narrow, $0 first workflow. If we ever use a component, choose the smallest standalone, MIT-covered module and verify the exact pinned revision, dependency graph, mobile/browser compatibility and license notices first.

## Cross-project adoption matrix

| PocketCode concern | Best prior-art pattern | Where to apply it | Decision |
|---|---|---|---|
| Truthful run lifecycle | One owner, child exit separate from wrapper failure, explicit timeout/cancel confirmation | Existing execution contract + PR #3 crosswalk | Adopt as review criteria; reconcile states before edits |
| Audit/report provenance | Ordered events, source labels, bounded logs, explicit unknown/missing evidence | Existing report contract + fixed-task worksheet | Adopt test criteria; do not create a second schema |
| Recovery after interruption | Persist completed step before next action; never replay uncertain writes blindly | Director capsule proposal and future session design | Adopt as future design requirement |
| Device/backend support | Capability discovery, safe fixed whitelist, per-backend capability matrix | Mobile preflight and competitor matrix | Adopt in the test protocol |
| Provider portability | Thin provider interface and deterministic adapter tests | Existing provider-neutral architecture | Keep; reuse implementation only after stack choice |
| Security boundary | Fail closed; explicit runtime isolation; separate secrets and untrusted code | SECURITY.md, acceptance gates, PC-return checklist | Adopt as mandatory gate; no security claims from docs alone |
| Error handling | Stable error categories, bounded retry only for transient errors, sanitized user messages | Execution contract/error mapping review | Adopt as review checklist |
| Remote PC | Reconnect/backfill, explicit approval, backend-specific support matrix | Optional remote-PC comparator only | Defer; not the no-PC core |
| Whole agent framework | Large integrated runtime / mobile app | None for current discovery stage | Do not import wholesale |

## Reuse rules before any code is copied

1. Record exact upstream repository, immutable commit/tag, file paths, root and file-level licenses, required notices, modifications, and dependency closure.
2. Prefer small libraries or a thin adapter over a wholesale framework. If a feature can be adopted as a documented invariant/test first, do that before introducing code.
3. Do not infer license compatibility from a repository badge alone. Check subdirectories, vendored binaries, transitive packages and generated assets; preserve attribution and notices.
4. Compare current upstream source with PocketCode's exact branch contract before porting. Never import an upstream state machine as if it were already compatible with PR #2/#3.
5. Add a deterministic regression test for each adopted behavior. A README claim or upstream green badge is not evidence that PocketCode satisfies it.
6. Do not introduce paid services, hosted dependencies, account setup, network calls, native build requirements, CI/Actions, or provider workload under this research pass.
7. No competitor source code has been copied in this audit. “Adopt” here means recording specific, traceable design/test patterns into PocketCode's existing work queue; implementation remains a separately approved step.

## Recommended next actions (ordered)

1. **Now:** use this audit to refine the existing cross-branch discrepancy list and fixed-task test protocol; do not edit PR #2/#3.
2. **Before contract freeze:** add test cases for timeout-with-process-still-running, wrapper failure vs child exit, unsupported capability, interrupted write/uncertain completion, partial diagnostic evidence, and reconnect/backfill if the remote path is retained.
3. **When execution location is chosen:** select only one candidate adapter/runtime, inspect its exact source/license/dependency graph, and run the canonical success/failure task in a fresh isolated workspace.
4. **At PC return:** verify the exact PR #2/#3 blobs and execute only the approved offline tests before considering any runtime integration.
5. **Decision gate:** if native evidence from a local app is already adequate and a portable report does not improve the next correction, narrow the product to the smallest useful evidence/continuity utility or stop the separate execution-product direction.

## Evidence boundary

This is a desk review of public repositories and their own documentation as retrieved on 2026-10-29. Feature statements are maintainer claims, not independent tests. No competitor was built or executed, no code was transplanted, and no PocketCode implementation/security/market claim is validated by this document.
