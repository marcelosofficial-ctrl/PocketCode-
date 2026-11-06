# Claude project map: PocketCode

**Canonical repository:** https://github.com/marcelosofficial-ctrl/PocketCode-  
**Working research branch:** [pocketcode-ai-workflow-director-research-2026-10-28](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/pocketcode-ai-workflow-director-research-2026-10-28)  
**Branch commits:** https://github.com/marcelosofficial-ctrl/PocketCode-/commits/pocketcode-ai-workflow-director-research-2026-10-28  
**Actions / test runs:** https://github.com/marcelosofficial-ctrl/PocketCode-/actions  
**Pull requests:** https://github.com/marcelosofficial-ctrl/PocketCode-/pulls

This is a navigation map and project brief, not a substitute for fetching the live branch head and reading current source. GitHub branch links are intentionally used instead of a pinned SHA because work continues.

## Start here, in order

1. [AGENTS.md](../AGENTS.md): shared agent rules and safety boundaries.
2. [CLAUDE.md](../CLAUDE.md): Claude-specific entrypoint and working rules.
3. [CHAT_START_HERE.md](CHAT_START_HERE.md): project goals, current priorities, constraints and continuity protocol.
4. [STATE_LEDGER_20261106.md](STATE_LEDGER_20261106.md): latest evidence, decisions, unknowns and current state.
5. [CLAUDE_HANDOFF_20261106.md](CLAUDE_HANDOFF_20261106.md): role-specific continuation brief.
6. [CHAT_WORK_LOG.md](CHAT_WORK_LOG.md): chronological implementation and CI evidence.
7. [EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md](EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md): lifecycle, dispatch, provenance, verdict and recovery semantics.
8. Root product docs: [PROJECT_STATUS.md](../PROJECT_STATUS.md), [PRODUCT_SPEC.md](../PRODUCT_SPEC.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [SECURITY.md](../SECURITY.md), [ROADMAP.md](../ROADMAP.md), [DECISIONS.md](../DECISIONS.md).

## Product mission

PocketCode is a phone-first, provider-neutral AI orchestration and execution control plane for iOS and Android. It is intended to convert AI-authored technical tasks into bounded work, truthful execution evidence, recoverable attempts, portable result receipts and user-controlled artifact publication. It is not merely a mobile Python IDE.

The user is phone-first and may lack reliable PC access for months. Prefer repository-backed continuity, multi-file coherent passes, exact-SHA CI evidence and concise requests only when owner action is genuinely required.

## Repository and code map

- `scripts/report_contract.py`: canonical legacy report contract. Preserve LOOP/CASE/D IDs and CASE-04 timed_out => INCOMPLETE/timed_out semantics.
- `scripts/dispatch_reconciliation.py` and `scripts/test_dispatch_reconciliation.py`: exact-scope provider lookup and idempotency decision model.
- `scripts/fake_outbox.py` and `scripts/test_fake_outbox.py`: in-memory reservation, leases, fencing, dispatch intent, ambiguity, reconciliation and retry authorization.
- `scripts/event_journal.py` and `scripts/test_event_journal.py`: append-only provenance, exact immutable bytes, source-scoped event identity, replay and conflict quarantine. Producer identity object is not cryptographic authentication.
- `scripts/fake_coordinator.py` and `scripts/test_fake_coordinator.py`: outbox/journal composition and recovery projection.
- `scripts/execution_projection.py` and tests: typed, fail-closed execution verdict projection.
- `scripts/result_receipts.py` and `scripts/test_result_receipts.py`: immutable receipt versions, attempt-bound artifact manifests, digest/size checks, quarantine, release authorization checks and same-receipt report publication retry.
- `prototypes/mobile-runner/`: static mobile runner prototype; checker and fixtures under `scripts/check_mobile_prototype.py` and `scripts/test_check_mobile_prototype.py`.
- `.github/workflows/pocketcode-python-tests.yml`: test-only Python 3.12 CI workflow, contents:read; no deploy step.
- `AI_COLLAB/`: project handoffs, state ledgers, conformance contracts, research and work logs.
- `RESEARCH/`: competitor, open-source architecture, code reuse, remote execution and mobile recovery research.

## Current technical direction and hard non-decisions

- $0 default. No paid provider, host, account, workload or billing commitment.
- Provider, model, runtime, app framework, database, durable store, backend and cloud host remain unselected.
- Local WASM/Pyodide/JSC are candidates for lightweight work, not hostile-code sandboxes.
- SSH/Tailscale and optional cloud execution are adapters under consideration, not commitments.
- Explicit paste/import only. No clipboard polling or intrusive overlays.
- Untrusted code needs disposable externally constrained isolation, default-deny permissions/egress, quotas, secret separation and cleanup.
- RevDev and PocketCode converge at product/program direction only. Keep repositories, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates separate. No repo merge or shared runtime.

## Roles

- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect and cross-project coordinator.

## Acceptance suites and evidence discipline

Keep PocketCode suites separate from RevDev suites. Canonical PocketCode sets include AWC-001–018, P8U-01–12 and P0-D 1–10, alongside the preserved LOOP/CASE/D report contract. Do not remap IDs or silently alter acceptance semantics. Distinguish implemented, locally tested, CI-tested, device-tested, proposed, blocked and unknown. A green Python CI run is not mobile/device, durability, concurrency, provider or sandbox acceptance.

## Collaboration / authority boundaries

Claude may inspect, propose and implement within the authorized research branch. Owner authorized GitHub continuity updates. Do not merge, deploy, publish a release, install, restart, use secrets/elevation, mutate unrelated PRs or spend money without explicit authorization. PR #2 and PR #3 remain untouched. No provider execution, durable infrastructure or release authority is implied by these research models.

## Current focus

Finish the fake end-to-end recovery-to-receipt-to-artifact publication conformance chain. Then red-team crash windows, stale attempt fencing, duplicate/reordered evidence, partial artifact writes, receipt version linearity, revoked authorization and publication retry. Only after the semantics and failure tests are stable should the team compare durable-store options. Do not select a database or backend prematurely.

## Claude's next actions

1. Fetch the live branch head and inspect current diff/status.
2. Read this map and the start-here/ledger/contract docs above.
3. Inspect all related scripts/tests, not just the newest file.
4. Independently review the receipt model for version-chain and authorization weaknesses.
5. Run the exact Python suite and report exact commit/environment/results.
6. Keep the next increment small enough to prove; update the ledger and work log with limitations.


## Latest verified test checkpoint

- Exact SHA: `4d4d66561b176b560b49fb00c6b600617bbeef97`
- CI run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308764330
- Python 3.12 / Ubuntu 24.04; 179 passed, 0 failed.
- Latest receipt version-chain implementation is included. Always re-check branch head before relying on this checkpoint.
