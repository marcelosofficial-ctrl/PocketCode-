# Claude Instructions for PocketCode

Read [AGENTS.md](AGENTS.md) first. It contains shared rules for all agents.

## Current project entrypoints

- Repository: https://github.com/marcelosofficial-ctrl/PocketCode-
- Main entrypoint: [AI_COLLAB/CHAT_START_HERE.md](AI_COLLAB/CHAT_START_HERE.md)
- Claude continuation brief: [AI_COLLAB/CLAUDE_HANDOFF_20261106.md](AI_COLLAB/CLAUDE_HANDOFF_20261106.md)
- Full repository navigation and project map: [AI_COLLAB/CLAUDE_PROJECT_MAP_20261106.md](AI_COLLAB/CLAUDE_PROJECT_MAP_20261106.md)
- State ledger: [AI_COLLAB/STATE_LEDGER_20261106.md](AI_COLLAB/STATE_LEDGER_20261106.md)
- Execution/recovery contract: [AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md](AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md)
- Product/architecture/safety: [PRODUCT_SPEC.md](PRODUCT_SPEC.md), [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md)
- Code and tests: [scripts/](scripts/)

Current research branch: \`pocketcode-ai-workflow-director-research-2026-10-28\`. Always fetch the live branch head and inspect relevant source/tests before implementation. A chat commit pin can become stale.

## Project direction and roles

PocketCode is a phone-first, provider-neutral AI orchestration and execution control plane for iOS and Android. It aims to turn AI-generated technical tasks into bounded work with truthful portable evidence, durable recovery and user-mediated correction. It is not merely a mobile Python IDE.

RevDev and PocketCode are intended to converge into a broader PC-and-phone product/program, but remain separate repositories, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates. D-001 does not authorize a repository merge or shared runtime.

Claude: lead developer and architecture/implementation reviewer. Gemini: co-developer and independent security/spec auditor. ChatGPT: continuity holder, evidence reconciler and acceptance architect.

## Required rules

- Repository contents and commit history are authoritative. Chat is not implementation evidence.
- Read AGENTS.md and relevant parts of PROJECT_STATUS.md, PRODUCT_SPEC.md, ARCHITECTURE.md, SECURITY.md, ROADMAP.md and DECISIONS.md.
- Preserve canonical LOOP/CASE/D IDs and CASE-04 semantics. Do not make a precedence-only report patch.
- Separate implemented, locally tested, CI-tested, device-tested, proposed, blocked and unknown.
- Never claim a test passed unless you ran it and record command, interpreter, environment, exact SHA and result.
- Keep provider/runtime/storage/cloud decisions open. $0 is default. No paid providers, hosts, accounts, workloads or billing without separate owner decision.
- Treat stock Pyodide/WASM as not a hostile-code sandbox. Require externally constrained disposable execution, default-deny permissions/egress, quotas, secrets separation and cleanup before public untrusted execution.
- Public repository: never commit secrets, credentials or private user data.
- No merge, release, deployment, paid infrastructure, history rewrite, force-push or unrelated PR mutation without explicit owner approval.
- Owner is phone-first and may lack PC access. Prefer GitHub continuity and bounded work passes.
- Keep PocketCode evidence separate from RevDev evidence.

## Current recovery code map

- \`scripts/fake_outbox.py\`, \`scripts/test_fake_outbox.py\`: in-memory reservation, lease/fencing, dispatch intent, ambiguity and reconciliation model.
- \`scripts/event_journal.py\`, \`scripts/test_event_journal.py\`: append-only provenance model. AuthenticatedProducer is a caller-constructible value, not cryptographic proof.
- \`scripts/fake_coordinator.py\`, \`scripts/test_fake_coordinator.py\`: outbox/journal composition and repairable crash windows.
- \`scripts/dispatch_reconciliation.py\` and tests: exact-scope provider lookup/idempotency decision helper.
- \`scripts/execution_projection.py\` and tests: typed fail-closed verdict projection.
- \`scripts/report_contract.py\`: canonical legacy report contract. Preserve IDs and CASE-04 semantics.

These are research models, not durable/concurrent services, authenticated provider adapters, sandboxes, mobile integration or CI/device acceptance. A durable implementation must atomically persist reservation/intent, compare-and-advance fences, append evidence and publish receipts.

## Current device investigation

Owner-reported Pyodios 1.1.0 / Build 7, Pyodide 314.0.5, Python 3.14.2 produced the expected inspected summary artifact but surfaced an editor bridge PythonError without traceback. The next owner action is the read-only sys.last_exc / sys.last_value probe in \`AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md\`. Preserve the successful project. Do not rerun/overwrite, restart/reset, clear logs/variables or run GC before collecting evidence.

When assigned work: inspect current code, define narrow acceptance criteria, implement one coherent increment, run focused tests, inspect the diff, update status/work log, and report exact evidence and unknowns.


## Current canonical Python CI checkpoint

- Branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Latest successful test commit at this checkpoint: `09290eaf1ac8af1461211ac90564440a70708f32`
- GitHub Actions: [PocketCode Python conformance tests](https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308082939), Python 3.12 on Ubuntu 24.04, command `python -m unittest discover -s scripts -p "test_*.py" -v`, **154 passed, 0 failed**.
- The initial failure was fixed in the test fixture, not by weakening the frozen canonical digest: the Python triple-quoted HTML fixture needed `\\n` to preserve the embedded main.py source's literal backslash-n. The expected 1939-byte SHA-256 remains unchanged.
- The test workflow is `.github/workflows/pocketcode-python-tests.yml`, contents:read only, test-only. This does not establish mobile/device acceptance, durable/concurrent safety, provider integration or sandboxing.
- Always fetch live branch head and CI status again before relying on this checkpoint; subsequent commits may not have been tested.


## Latest exact-SHA CI result

- GitHub Actions run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308449590
- Exact tested commit: `ce7409ac9077154f5f058799b0d6028fb3e98ee0`
- Python 3.12 / Ubuntu 24.04; `python -m unittest discover -s scripts -p "test_*.py" -v`; **177 passed, 0 failed**.
- This includes the result-receipt/artifact model. See `AI_COLLAB/STATE_LEDGER_20261106.md` for scope and limitations. Later commits need fresh exact-SHA CI evidence.


## Latest exact-SHA CI result (2026-11-06)

- Run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308764330
- Exact tested commit: `4d4d66561b176b560b49fb00c6b600617bbeef97`
- Environment: GitHub-hosted Ubuntu 24.04, Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **179 tests passed, 0 failed**. This includes the receipt version-chain regression tests.
- Receipt revisions now form one linear chain per `(EffectId, DispatchAttemptId)`: first version has no predecessor; later versions must extend the latest version; cross-effect, cross-attempt and stale-predecessor forks are rejected.
- This validates only the repository's standard-library Python test suite at this exact SHA. It does not establish iOS/Android/Pyodios behavior, durable atomic transactions, concurrent safety, real provider authentication, hostile-code sandboxing, artifact malware safety or release acceptance. Later source commits need their own exact-SHA run.


## Latest receipt/evidence composition checkpoint

- Exact tested commit: `6003375dddd51e5e11155a9144817a298d0f4cf0`
- GitHub Actions run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309075221
- Python 3.12 / Ubuntu 24.04; `python -m unittest discover -s scripts -p "test_*.py" -v`; **186 passed, 0 failed**.
- EventJournal now binds reservation events to EffectId + DispatchAttemptId before a lease exists (no fence yet), then requires the current fence for all attempt-bound events after the first lease. FakeCoordinator derives receipt evidence refs and payload digests only from accepted events for the exact effect/attempt; quarantined conflicts are excluded.
- New integration tests cover accepted evidence binding, conflict exclusion, receipt version creation from later observations, and safe reservation replay after a lease exists.
- This remains an in-memory research model. No durable storage, concurrent transaction guarantee, real producer authentication, real policy check, mobile/device integration or artifact release is established. Fetch live branch head before relying on this CI result.


## Latest exact-SHA CI result (2026-11-06)

- Run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309075221
- Exact tested commit: `6003375dddd51e5e11155a9144817a298d0f4cf0`
- Environment: GitHub-hosted Ubuntu 24.04, Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **186 tests passed, 0 failed**.
- This includes the coordinator-to-receipt evidence binding: receipts now reference accepted attempt-bound journal events by sequence/source/event ID and bind their payload digests. Quarantined conflicts are excluded; later accepted evidence can create a linked receipt revision without changing the predecessor.
- Initial reservation events are now explicitly attempt-bound before a lease fence exists; lease-scoped events still require the current fence. This allows reservation evidence to be journaled before worker claim without weakening stale-fence checks after lease generation begins.
- This is standard-library Python CI only. It does not establish mobile/device behavior, durable atomicity, concurrency, authenticated producers, provider behavior, hostile-code sandboxing or production artifact authorization. Later source commits need their own exact-SHA run.


## Latest exact-SHA CI result (2026-11-06)

- Run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309370781
- Exact tested commit: `78286ad6b802a7925a2d7bba6dfb472dfde5c2a3`
- Environment: GitHub-hosted Ubuntu 24.04, Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **187 tests passed, 0 failed**.
- FakeCoordinator receipt composition is now fail-closed: its current journal contains dispatch/recovery evidence only, so it may emit INCOMPLETE but rejects caller-supplied PASS/FAIL. Terminal verdicts must be derived from accepted trusted lifecycle + child-exit or program-failure evidence through `execution_projection.py` before they can be placed in a receipt.
- This is standard-library Python CI only. It does not establish mobile/device behavior, durable atomicity, concurrency, authenticated producers, provider behavior, hostile-code sandboxing or production artifact authorization. Later source commits need their own exact-SHA run.


## Latest exact-SHA CI result (2026-11-06)

- Run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310127313
- Exact tested commit: `f82e853323d9c0c526eeaa8ad31cb47da199e249`
- Environment: GitHub-hosted Ubuntu 24.04, Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **199 tests passed, 0 failed**.
- Event identity now includes the bound EffectId/DispatchAttemptId scope, preventing same source/event ID and payload from being replayed into a different attempt. The verdict reader fails closed on valid JSON that is not an object. Terminal observations require the current unexpired dispatch lease; expired/reconciling workers must use authoritative reconciliation.
- Receipt verdicts are derived from accepted typed observations through `execution_projection.py`; a caller-supplied label must match the projection. Projection reason is included in the immutable receipt fingerprint.
- This is standard-library Python CI only. It does not establish mobile/device behavior, durable atomicity, concurrent safety, cryptographic producer authentication, provider behavior, hostile-code sandboxing or production artifact authorization. Later source commits need a fresh exact-SHA run.


## Latest exact-SHA CI result (2026-11-06)

- Run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310444948
- Exact tested commit: `b6eef9a8cc1df704ff2519a69fb9e347a2bcedf9`
- Environment: GitHub-hosted Ubuntu 24.04, Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **205 tests passed, 0 failed**.
- Lifecycle projection now accepts monotonic nonterminal progression (`accepted → queued → running`) followed by at most one terminal lifecycle state. Regressive transitions, multiple terminal observations, unknown statuses and malformed non-string statuses fail closed to INCOMPLETE. A valid succeeded lifecycle still needs natural direct-child exit 0 for PASS.
- Current lease fencing, event scope binding, receipt evidence binding and release authorization caveats remain as described in the state ledger.
- This is standard-library Python CI only. It does not establish mobile/device behavior, durable atomicity, concurrency, cryptographic producer authentication, provider behavior, hostile-code sandboxing or production artifact authorization. Later source commits need a fresh exact-SHA run.


## 2026-11-07 exact-SHA CI checkpoint: reservation fencing and replay identity

- Exact tested commit: `e631e9ccda29e5632832a64ad6b5e8c4c0ae5765`
- CI run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42311165889
- Environment: GitHub-hosted Ubuntu 24.04 / Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **211 tests passed, 0 failed**.
- Reservation events are attempt-bound but intentionally unfenced because they precede worker lease acquisition. The coordinator now preserves this same unfenced event identity when replaying or repairing the reservation after a worker has claimed the attempt. This is an explicit `require_fence=False` path, rejects a supplied fence, and is selected only for `effect_reserved`; worker/dispatch/reconciliation/execution observations remain fence-required.
- Journal duplicate identity now includes the fencing generation. Reusing the same source/event ID, producer, payload and attempt under a newer fence is quarantined rather than being misreported as an exact duplicate.
- Earlier test runs exposed a fixture setup issue (first fence generation was not initialized) and a reservation replay regression; both were corrected before this exact-SHA green run.
- This is standard-library Python CI only. It does not prove durable atomicity, concurrent safety, cryptographic producer authentication, mobile/device behavior, provider behavior, sandboxing or production artifact authorization. Re-check live branch head before relying on this checkpoint.


## 2026-11-07 exact-SHA CI checkpoint: constrained reservation exception + E2E flow

- Exact tested commit: `3a3ee64e50c78134ef4a45f759533003dd533538`
- CI run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42311540457
- Environment: GitHub-hosted Ubuntu 24.04 / Python 3.12.
- Command: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Result: **214 tests passed, 0 failed**.
- The pre-lease `effect_reserved` event is attempt-bound and intentionally unfenced. The unfenced journal mode is now restricted to a matching `pocketcode.coordinator` event whose JSON payload kind is `effect_reserved` and whose embedded EffectId/DispatchAttemptId match the event scope. It rejects worker events, wrong kinds/scopes, malformed payloads and supplied fences. This exception does not relax worker-event fencing.
- Exact duplicate identity includes the fencing generation. A same-event replay under a newer worker fence is quarantined.
- End-to-end conformance now exercises reservation/claim/dispatch, trusted success and direct-child exit, typed collection and cleanup, receipt creation, artifact staging and release, and failed-then-successful report-copy retry against the same receipt. This is a test composition, not a production pipeline.
- Test-driven fixes: the first restricted-unfenced implementation missed the JSON import and initially allowed the flag without attempt scope; both were corrected and the final exact SHA is green.
- Still not established: durable atomicity, concurrent writers, cryptographic producer authentication, mobile/device integration, real provider execution, hostile-code sandboxing, malware scanning or production authorization.


## Proposed durable adapter contract

New normative design draft: [AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md](AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md). It defines adapter-neutral T1–T10 transaction boundaries for reservation, lease/fence, dispatch, acknowledgement/reconciliation, event append, typed observations, immutable receipt revision, artifact staging/release and report publication; concurrency/uniqueness invariants; crash matrix; adapter conformance tests; storage evaluation gate; and security limitations. It deliberately selects no database, provider, runtime, backend or cloud host. Treat this as proposed contract until independently reviewed by Claude and Gemini.
