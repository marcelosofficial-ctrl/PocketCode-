# Remote agent control planes and workflow protocols — 2026-11-05

**Status:** Focused desk and source-code research; no hands-on product tests.
**Purpose:** Extend the existing competitor work with newer mobile-first agent control planes and durable workflow protocols. This is not a new product direction or a runtime/provider selection.

## 1. Executive conclusion

PocketCode should **not pivot from its run/inspect/report/iterate hypothesis into a generic remote coding-agent control room**. Happier, Cretli and similar products already provide phone access to agents that continue running on a user's PC or server. They are important alternatives, but that model does not solve the four-month no-PC period unless a reachable host or separate hosted runner exists.

PocketCode's stronger product proof remains:
1. execute a bounded task in a deliberately selected environment;
2. observe truthful output, lifecycle, artifacts and cleanup;
3. create a compact, portable evidence receipt;
4. hand the evidence to the user's chosen AI;
5. review a proposed correction and rerun as a new attempt;
6. preserve task/result continuity without accidentally rerunning completed work.

The AI Workflow Director remains a supporting feature, not the core differentiator. Its future value is to reduce repeated context transfer and improve safe continuation across providers.

## 2. New competitor findings

| Project | What it offers | Why it matters | PocketCode decision |
|---|---|---|---|
| Happier | Desktop, web and mobile control surface for Claude Code, Codex, OpenCode, Pi and many more; connected machines, one session inbox, cross-agent delegation, approvals, voice and encrypted sync | Strongest direct comparison for mobile control of existing agents. It makes multi-agent continuity and approval UX expected capabilities, but still relies on an agent host. | Treat as a benchmark for optional remote-host/session adapters, not a substitute for PocketCode's actual execution proof. |
| Cretli | Self-hosted PWA with phone chat, terminal, files, Git, tasks, browser and pluggable AI harnesses; one live session shared across devices | Demonstrates the breadth of a mobile developer cockpit and workspace tools. It requires a reachable host and exposes a powerful shell. | Do not copy its full-shell model or present remote PC access as PC-less execution. Borrow workspace navigation and session concepts only. |
| agent-device | CLI, MCP server and typed Node API for controlling real devices/simulators and capturing accessibility snapshots and visual evidence | Useful for automated mobile UI testing, device regression and evidence capture. It does not run user code or prove sandbox/process termination. | Keep as an optional future QA adapter if actual iOS/Android UI test gaps are identified. Do not add to MVP dependencies. |
| OpenWOP | Provider-neutral workflow protocol for durable runs, event logs, interrupts, idempotency, replay/fork and conformance | Useful contract patterns for the secondary AI Workflow Director and future cross-provider workflows. | Borrow selected ideas; do not adopt the whole protocol or claim conformance. |

## 3. Happier source audit

Repository: happier-dev/happier, branch dev at inspection.
- README blob: 40da631916aa654cb786b81c68a548706c5795e9
- MIT license blob: da0b4ae30a42be8db9776eb887acb671b19699a0
- session transition cutover source blob: 5ab5524bb633144b8594917ec418a47cff62f5d5
- session forking documentation blob: b56cb175530521da7e69fad2ead7023e20452917
- attach-to-session documentation blob: 500d99fd25efc4d9a8b7af4f95b5451fb1db89fe

### Features worth benchmarking

- One inbox across agents and machines.
- Attach to the same running session from app or terminal rather than creating a duplicate.
- Provider-native attach/resume only when the provider declares and negotiates the needed capability.
- Explicit Native fork / Replay fork / New session strategy. If the user explicitly selects Native and it fails, do not silently substitute Replay.
- Replay seed applied once to a child session, parent transcript visible read-only, no inherited actionable approval controls.
- Permission approval cards are distinct from structured questions that resume the run.
- Stale historical questions are read-only.
- Windows interactive-host modes avoid assuming tmux is available.
- End-to-end encrypted relay is a useful model if PocketCode later adds remote-host control.

### Implementation lesson

The inspected cutover source deliberately commits one current-view write and then uses a separate canonical transcript-message writer. The two operations are not one transaction. It returns an explicit partial outcome if the first committed and the second failed. This is the correct lesson: expose partial state honestly rather than bypass a canonical writer to fake atomicity.

Do not copy the source's owner-only/reserved-ID access argument as a general security pattern. Every PocketCode action still needs its own authorization and host/runtime boundary.

### Product limitation

Happier controls agents running on the user's own machine. It is not a no-host execution environment. A phone can reconnect to an existing session, but the remote agent host still needs to exist and remain available.

## 4. Cretli source and security audit

Repository: cretli/cretli, commit c5e1db2ca77a6d15a2d93ee0796edb8acfebfab6.
- README blob: 04b9587cdce6a4eb65cbc52f78a44ba8c83deb7c
- MIT license blob: 11f9ca2d5115d60e6f0ac761a0795b316dab1010
- architecture blob: 4e8a569db9470890d346a27dec6322d8d2a7475c
- security policy blob: e7b1e47220ed509e96c106e7f930c7eef1b3607b
- delegation tree source blob: 3450f15dfa1d1e75332d2233dbc9d9f8a48c8d5e
- runtime worker source blob: dfe0fc66736a40d53a8d5c6fc5a4b82995213a62
- SQLite delegation store source blob: 25e0d1f2fe6fa78817b21f90ec77fec7f89975d8
- mailbox source blob: efe9ef8c5f168fc62ffd60ddd21a3d391094ef24

Useful patterns:
- explicit parent/child delegation tree, bounded depth and grant attenuation;
- separate progress messages and final reports, linked to attempt identity;
- a mailbox/outbox that avoids starting the parent again for an already acknowledged attempt;
- non-overlapping runtime ticks, dispatch-in-flight accounting, degraded health and bounded backoff;
- SQLite tables for delegations, attempts, outbox, mailbox and idempotency tombstones, with unique idempotency indexes and transactional writes;
- typed corrupt/I/O errors that must not be mistaken for an empty store.

Caveats:
- the JSON atomic-rename path is last-writer-wins across processes and does not merge concurrent writers;
- the in-memory promise-chain lock only serializes one process;
- SQLite is explicitly a single-host/WAL/busy-timeout design and depends on its owner-lock assumption;
- Cretli's security policy says a network-reachable terminal user can execute arbitrary shell commands as the host user;
- Plan mode is not a sandbox for every backend; Codex Plan is prompt-only with broad sandbox access;
- its browser policy explicitly documents residual SSRF/network limitations.

Decision: learn from its session/workspace and delegation UI, but do not adopt its shell exposure, browser boundary or persistence implementation as PocketCode's execution/security design.

## 5. agent-device source audit

Repository: callstack/agent-device, main at inspection.
- README blob: 17c0c4a8f7485290007aca52bd97664257fd81f8
- package.json blob: a39877d3eacfc1bfecd91a484bb76db865f4b8fb
- MIT license blob: e339c7e96e4f372b7f80d7ed7a19570dfc4f336d

The package exposes the same command surface through CLI, MCP and typed Node API. It uses accessibility snapshots and short-lived refs for interaction, then captures screenshots/video as evidence. This is useful for testing a mobile app's actual UI and avoiding screenshot-only agent navigation.

It requires Node 22.12+ and platform-specific helpers. It is not a user-code runner, sandbox, evidence receipt store or process supervisor. It should be evaluated only as a separate test adapter if it solves an identified device QA gap.

## 6. OpenWOP protocol audit

Repository: openwop/openwop, main at inspection.
- README blob: 7cb5e798d11f53ef4ff64cf91d7e8b712b059212
- Apache-2.0 license blob: 09000c90f40b3482291793ee9c850b3af34475da
- idempotency spec blob: 3cb7765c0ff81b68c2ca426974865477c2cb0260
- event spec blob: 0e7c936830c3907ed316bca630e16ce3adf55006
- replay spec blob: 2e51564fc0082a5b52bff6ae6d14e9a1c8e863c2
- conformance spec blob: 68fb2d17c8f1f643c10127ddbc320fd405e1f1b6
- known limits blob: 57703f469b35c69a5b642720e6af507361d1df3e
- durable execution qualification RFC blob: 38b58466f389088110e21a813a72219ad0a2a987

### Concepts useful to the AI Workflow Director

- request idempotency and side-effect/effect idempotency are separate;
- stable business effect identity survives retries; attempt counter is not part of identity;
- an effect is claimed atomically so concurrent duplicate execution cannot both win;
- event log is append-only; UI snapshots are projections;
- human approval, clarification, refinement and cancellation are typed interrupts;
- replay suppresses external effects and reuses recorded outcomes;
- conformance assigns stable requirement IDs and distinguishes blocked, skipped, inapplicable and executed-pass;
- capability discovery must advertise only behavior actually witnessed.

### Important limitations

OpenWOP's own known-limits document says no independent tier-3 host has certified a profile. The only durability rung witnessed was single-instance restart on the steward's reference host; peer resume, multi-instance and multi-region qualification were not witnessed. Some security/idempotency behavior also lacks major-2 behavioral legs.

Decision: use it as a design reference, not as a runtime dependency or evidence that PocketCode has durable orchestration.

## 7. Feature recommendations, in priority order

### P0: Preserve the current core product hypothesis

No pivot away from run/inspect/report/iterate. The differentiator is evidence quality and safe correction, not chat UI alone.

### P1: Evidence-first run history

- list attempts under one task identity;
- preserve exact input/source digest, runtime/environment identity and adapter version;
- show stdout, stderr, lifecycle, exit/outcome, artifacts and cleanup as separate facts;
- clearly mark unavailable/unknown rather than infer facts from client timeout or UI state;
- retain a portable receipt and its source provenance.

### P1: AI correction packet

- compact packet includes original task, exact failure evidence, environment constraints and relevant files;
- separate original run from each patch/retry attempt;
- patch preview and user approval before applying;
- verification run is a new attempt with linked lineage, not a rewrite of the original receipt.

### P2: Provider-neutral AI session continuity

- stable provider/session identity and explicit capability negotiation;
- reconnect to the same session using a durable event cursor;
- approval requests and user questions are different UI actions;
- native fork, replay fork and new session are explicit choices;
- provider fallback must be visible and never silently change a user-selected strategy.

### P2: Optional remote host adapter

Only if the fixed-task comparison shows remote execution genuinely helps. Treat the host as an execution authority; phone disconnect is not process termination. Use authenticated pairing, least privilege, encrypted transport, bounded commands and explicit host-side receipts. Never expose a full shell by default.

### P3: Device QA adapter

Evaluate agent-device only after a real UI regression/evidence gap exists. Keep it outside the user-code execution sandbox and outside the authoritative run journal.

## 8. Code reuse decision

No new upstream code was copied into PocketCode in this pass.

Reasons:
- Happier is a large TypeScript/Expo/Prisma product, not a small reusable runner component.
- Cretli's delegation-tree helper is small and MIT, but encodes Cretli-specific chat row fields and process environment. Porting its invariant is safer than copying it verbatim.
- Cretli's SQLite/outbox implementation is Node-specific and relies on a single-host owner-lock assumption.
- agent-device is an optional external Node test tool, not a PocketCode runtime component.
- OpenWOP's SDK/schema surface is much larger than PocketCode's current contract and its independent-host evidence is incomplete.

This is a deliberate no-copy decision, not a failure to inspect code. Reuse should reduce integration risk, not add a new framework or silently change product boundaries.

## 9. Current gates and non-actions

- PocketCode remains discovery/product-definition stage.
- No production runner, provider, cloud runtime, sandbox or paid service selected.
- $0 default budget remains.
- Fixed-task product comparison and AI Director evaluation remain NOT RUN.
- LOOP/CASE and AWD acceptance definitions remain unchanged.
- No app installed, user code executed, device test run, provider workload or cost incurred.
- No source/runtime/PR/Actions/deployment change. PR #2 and #3 remain protected and untouched.
