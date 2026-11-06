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


### Release authorization caveat

`ResultReceiptStore.release_artifact()` validates a caller-supplied authorization snapshot. It does not fetch/authenticate an authority or prove freshness/revocation. The caller must obtain a fresh trusted decision per request. See the execution/recovery contract's artifact authorization caveat.


## Latest verified test checkpoint

- Exact SHA: `6003375dddd51e5e11155a9144817a298d0f4cf0`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309075221
- Python 3.12 / Ubuntu 24.04; 186 passed, 0 failed.
- FakeCoordinator now binds accepted attempt-scoped journal evidence to immutable receipt revisions. Quarantined conflicts are excluded. Initial reservation event is attempt-bound before the first lease fence; later lease events remain fenced.
- Always re-check the live branch head before relying on this checkpoint.


### Terminal verdict gate

The current FakeCoordinator receipt builder only permits INCOMPLETE because its journal has not yet integrated trusted terminal lifecycle and child-exit observations. PASS/FAIL must be derived via `execution_projection.py`, not supplied as a caller assertion. See the execution/recovery contract.


## Latest verified test checkpoint

- Exact SHA: `78286ad6b802a7925a2d7bba6dfb472dfde5c2a3`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309370781
- Python 3.12 / Ubuntu 24.04; 187 passed, 0 failed.
- FakeCoordinator receipt builder only permits INCOMPLETE until trusted terminal execution evidence is integrated. PASS/FAIL must come from `execution_projection.py`, not caller-supplied labels.
- Always re-check the live branch head before relying on this checkpoint.


### Typed terminal evidence integration (in progress)

FakeCoordinator now appends typed lifecycle, child-exit and program-failure observations and reconstructs a verdict through `execution_projection.py`. Receipt composition derives the verdict from accepted attempt-bound journal evidence and records the projection reason. Multiple same-kind observations fail closed. This remains in-memory and does not authenticate the payload's producer class. CI pending for the current source increment.


## Latest verified test checkpoint

- Exact SHA: `f82e853323d9c0c526eeaa8ad31cb47da199e249`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310127313
- Python 3.12 / Ubuntu 24.04; 199 passed, 0 failed.
- Terminal observations require a current unexpired dispatch lease. Event identity is attempt-scoped. Receipt verdicts derive from accepted typed observations. Expired workers reconcile instead of appending terminal facts.
- Always fetch the live branch head before relying on this checkpoint.


## Typed terminal evidence and current release gate checkpoint

- Exact tested commit: `fd41883364e98e9c2ee306e89a8140f5566083a9`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310308543, Ubuntu 24.04 / Python 3.12, **201 passed, 0 failed**.
- FakeCoordinator now derives PASS/FAIL/INCOMPLETE via `execution_projection.py` from accepted attempt-bound lifecycle, direct-child exit and trusted program-failure observations. Caller-supplied verdict and lifecycle disposition must match the projection. Multiple same-kind observations and stale-fence terminal evidence fail closed to INCOMPLETE.
- Terminal observations require a current unexpired dispatch lease; expired/reconciling attempts must use authoritative reconciliation. This remains a caller-constructible in-memory model, not cryptographic producer authentication.
- Artifact release now binds to a receipt manifest, exact object version, attempt, principal/tenant, operation scope, authorization snapshot, expiry and revocation flag, and rechecks on every request. The authorization snapshot is still caller supplied, not an external policy decision.
- Current receipt publication and artifact storage are in-memory; no durable transactions, actual mobile release, malware scanning or provider integration are established. Fetch live head and exact-SHA CI before relying on this checkpoint.


### Next verification gate

Stress the composed receipt projection with contradictory collector/teardown evidence, stale/revoked release authorization, cross-effect artifact IDs, artifact digest tampering and process interruption. Then specify atomic durable receipt/artifact publication without choosing a storage engine prematurely.


## Latest verified test checkpoint

- Exact SHA: `b6eef9a8cc1df704ff2519a69fb9e347a2bcedf9`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310444948
- Python 3.12 / Ubuntu 24.04; 205 passed, 0 failed.
- Lifecycle progression supports monotonic accepted/queued/running updates followed by at most one terminal state; unknown, malformed, regressive or forked states fail closed. PASS requires succeeded + natural child exit zero.
- Always re-check the live branch head before relying on this checkpoint.


## 2026-11-07 verified source checkpoint

- Exact tested SHA: `e631e9ccda29e5632832a64ad6b5e8c4c0ae5765`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42311165889
- Result: 211 passed, 0 failed, Ubuntu 24.04 / Python 3.12.
- Source changes: `scripts/event_journal.py`, `scripts/test_event_journal.py`, `scripts/fake_coordinator.py`; regression coverage also in `scripts/test_fake_coordinator.py`.
- Reservation event remains unfenced because it precedes lease acquisition; replay and repair after claim preserve its original identity. Worker event deduplication includes fence generation and quarantines a replay under a newer fence.
- Live branch head may have advanced beyond the tested SHA due documentation-only follow-up commits; always fetch the branch before starting.
