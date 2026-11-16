# Research pass — Pyodide concurrency, replay, CI identity and trust
Date: 2026-11-16
Scope: model/design evidence only. No stack, provider, database, runtime, adapter, workflow or acceptance-gate change.

## Ranked gaps

1. **Journal-to-receipt capture (critical):** freshness and coherent-cut guarantees must match the actual execution environment; the prior generic lock recommendation is not portable to PocketCode's reported Pyodide runtime.
2. **Outbox/inbox crash semantics (critical):** in-memory co-commit and duplicate suppression do not establish durable recovery or exactly-once external effects.
3. **Exact-source CI (critical):** historical pinned-tree success must remain distinct from verification of the push-triggering source SHA.
4. **Producer authentication (high):** source/event identity detects duplicate identity; it does not prove who emitted the event.
5. **Termination evidence (high):** browser-worker termination, supervisor intent, and native process teardown are different claims.

## Research findings (sources opened)

| Area | VERIFIED finding | Maintenance / licence | PocketCode disposition |
|---|---|---|---|
| Pyodide 314.0.5 concurrency | The exact-version official compatibility page says `threading`, `multiprocessing`, and sockets are included but not functional; Pyodide does not support threading or multiprocessing. The FAQ says starting threads raises RuntimeError. | Exact 314.0.5 docs opened; no dependency proposed. | Do **not** make `threading.Lock` a portable requirement for the Pyodide model. |
| Pyodide worker topology | Official Pyodide docs say a Web Worker runs in a separate global context and cannot directly share globals with the main window. Communication is message-based. | Current docs and 314.0.0 worker guide opened; no worker topology selected. | Treat UI↔worker messaging as serialized message exchange, not shared-memory locking. Runtime/worker topology in the user's app remains UNKNOWN. |
| Python locks | Python threading docs describe Lock as a synchronization primitive for concurrently executing threads. The builtins thread-safety page is explicitly scoped to free-threaded CPython; it warns multi-operation reads/iteration are not atomic. | Python 3.15 docs opened; scope carefully limited. | Native threaded adapters may use a shared lock, but only if all journal mutators and the full capture take that same lock. Do not infer this applies to Pyodide. |
| Transactional outbox | AWS guidance requires aggregate state and outbox row to commit in the same database transaction; it explicitly warns about duplicate delivery and ordering, and recommends idempotent consumers. | Official AWS pattern docs opened; no AWS infrastructure or code adopted. | Reuse only the pattern. A PocketCode model's in-memory commit point is not durable atomicity. |
| Delivery semantics | Kafka 4.4 docs distinguish at-most-once, at-least-once and exactly-once; exactly-once with an external destination requires coordination/cooperation with that destination, commonly atomically storing output and consumed position. | Official current 4.4 docs opened; Kafka is not a dependency. | Do not claim exactly-once side effects from an outbox, stable ID or broker alone. |
| Event identity | CloudEvents core says `source + id` uniquely identifies a distinct event; a redelivery may reuse the same ID. | Latest listed core release v1.0.2; repository LICENSE is Apache-2.0. | Preserve source+event identity. PocketCode's stricter rule—same identity with changed canonical digest is conflict/quarantine—is a sound application policy, not a claim made by CloudEvents itself. |
| CI source identity | GitHub says for `push`, `GITHUB_SHA` is the tip commit pushed to the ref. GitHub recommends pinning third-party Actions to full commit SHAs as the immutable action reference. | Official GitHub docs opened; actions/checkout releases page showed v7.0.1 current when searched. | Separate the SHA of the action implementation from the SHA of PocketCode source being tested. No workflow edit authorized. |
| Worker termination | HTML Living Standard's worker termination algorithm sets the closing flag, discards queued tasks, aborts the running script and empties the dedicated worker's message port. | Living Standard edition updated 2026-11-16; MDN compatibility page also opened. | This supports browser-worker termination semantics, not proof of an OS process, renderer process, native child or external sandbox teardown. |
| Producer trust | Sigstore keyless signing binds an ephemeral signing key to an OIDC identity in a short-lived certificate and records signing events in Rekor. | Official Sigstore docs opened; no dependency or hosted service selected. | Useful comparator for verified identity + artifact digest + audit trail. The current `AuthenticatedProducer` remains an assertion, not cryptographic authentication. |

## Corrected design contract

### A. Journal capture: environment-specific, synchronous model boundary

**Decision:** the prior contract's blanket requirement for a Python shared `threading.Lock` is withdrawn for the Pyodide execution profile. The exact 314.0.5 docs explicitly say threading is unsupported. A Web Worker has its own global context; the browser message boundary is not a shared Python heap.

1. The model's portable baseline is a **single-owner, synchronous journal operation**. `append_accepted`, `append_conflict`, and `capture_receipt_snapshot` must be synchronous, must not `await`, yield to JavaScript, invoke user callbacks, or call external code while reading/updating journal state.
2. `capture_receipt_snapshot` reads all global high-waters and exact effect/attempt conflict references from the same journal-owned state during one uninterrupted synchronous operation. Its linearization point is the instant the method begins the immutable local copy; an append ordered before that point is included, and one ordered after it belongs to a later snapshot.
3. If a future adapter truly shares one journal across native threads, it must supply one synchronization primitive and use it for **every** journal mutation and the complete multi-field capture. A lock around only the snapshot reader is insufficient. This is an adapter-specific profile, not the Pyodide baseline.
4. If a worker boundary is used, one worker owns the journal; messages carry immutable event inputs and returned receipt evidence. Do not claim cross-worker object sharing. The actual PocketCode app's topology is still UNKNOWN.
5. Receipt creation must use the authoritative journal dependency wired once by the composition root, not accept a detached snapshot on each call. Prefer a journal-owned `create_receipt_for(effect_id, attempt_id, receipt_store)` operation or a store constructed with the authoritative journal. This removes the stale detached-snapshot path in the intended composition, but **does not create a Python security boundary**: callers able to construct arbitrary model objects can still fabricate a journal. Cryptographic producer verification remains outside the model.

### B. Receipt invariants and tests

- Snapshot fields are derived only from journal state: global observation high-water, global accepted-event high-water, exact-scope conflict sequence references, effect ID and attempt ID.
- Validate `0 <= accepted_high_water <= observation_high_water`; reject bool-as-int; require conflict references positive, unique, strictly ordered and no greater than observation high-water.
- Receipt fingerprint binds the full snapshot and identity tuple. A successor receipt may include later evidence; predecessor evidence and fingerprint remain unchanged.
- Required regressions: live journal capture; conflict appended before capture is included; conflict appended after capture is excluded from predecessor and included in successor; exact effect/attempt filtering; malformed high-water/reference rejection; caller-supplied detached snapshot/scalar rejection; synchronous no-yield capture contract; native-thread shared-lock test only in a native-thread test profile.
- A deterministic interleaving test should place an append immediately before and immediately after the capture call. Do not write a Pyodide test that tries to start a Python thread; that is unsupported by the exact-version runtime docs.

### C. Outbox/inbox replay contract

| Failure point | Required durable behavior | Allowed claim |
|---|---|---|
| Before aggregate/outbox transaction commits | Neither aggregate transition nor outbox event is visible | Atomic only if one real durable transaction is implemented |
| After commit, before send | Outbox row remains discoverable and retryable | At-least-once publication |
| Send accepted, acknowledgement lost | Retry same immutable event ID and canonical bytes | Duplicate delivery is possible |
| Consumer receives duplicate | Atomically check inbox identity and apply business mutation in one destination transaction | Idempotent effect only if inbox + mutation share atomic commit |
| Consumer crashes between effect and dedupe record | If not atomic, replay can duplicate effect | Exactly-once NOT established |
| Version N+1 arrives before N | Do not advance projection over a missing predecessor; buffer or reject without mutation | Ordered application only after gap resolution |

The durable adapter contract must define: aggregate/outbox transaction boundary; stable outbox identity; per-aggregate sequence; retry policy; consumer inbox uniqueness key `(source, event_id)`; digest comparison on identity collision; atomic inbox+business mutation; restore/replay cursor; retention and compaction rules. Until those exist, current grant/outbox code remains an in-memory semantic model only. No database or transport is selected.

### D. Exact-SHA CI contract (proposal only; workflow edits remain unauthorized)

Keep the historical P40 lane clearly labelled as historical. Add a separate current-source lane only after owner authorization:
- For a push run, expected source SHA is the event's `GITHUB_SHA`; do not substitute the current moving branch name.
- Checkout that exact source SHA, then print and assert `git rev-parse HEAD == GITHUB_SHA` before installing dependencies or running tests.
- Record workflow run ID, event, ref, expected SHA, actual SHA, Python version, OS, job, test command and exact pass/fail totals in the run output.
- Pin `actions/checkout` itself to a verified full-length action commit SHA. This action SHA is distinct from the PocketCode source SHA under test.
- If a later push changes the branch, an earlier run still proves only its own triggering SHA. A historical fixed SHA job must never be presented as current-head verification.
- Do not edit `.github/workflows/pocketcode-python-tests.yml` in this pass.

### E. Producer and termination evidence

Producer ingress must verify issuer, subject, audience, signature/key validity and canonical payload digest before writing an authenticated producer identity into the journal. Bind the verified identity to the event's source, event ID, effect/attempt scope and digest. A plain `AuthenticatedProducer` constructor argument is not verification. Sigstore is a research comparator only; it is not selected.

For browser workers, record distinct facts: `termination_requested`, browser `Worker.terminate()` invoked, message channel detached/fenced, and stale messages rejected by run token. Do not label these native process termination. If a later adapter starts an OS child or sandbox, it needs an authoritative process-exit/reap or host termination receipt tied to ExecutionId and attempt; absence of such proof remains UNKNOWN.

## Red-team corrections to previous work

1. **Portability error:** previous contract recommended a shared Python lock without checking the actual Pyodide target. Exact Pyodide 314.0.5 docs say threading is unsupported. Replaced universal lock requirement with synchronous single-owner baseline and native-thread-only lock obligation.
2. **False API-strength implication:** passing a live journal object is fresher than passing a detached snapshot, but a caller-supplied journal parameter can itself be fabricated. Replaced per-call trust in a journal argument with composition-root ownership; explicitly states this remains a model convention, not a security boundary.
3. **Outbox atomicity overreach:** one in-memory commit point was described too close to transactional atomicity. Clarified durable aggregate/outbox atomicity requires one real transaction; inbox dedupe and business mutation must also share one destination transaction.
4. **CI identity conflation:** action implementation pinning and source checkout SHA are separate identities. Explicitly requires both: pin the action code by full SHA, test the source tree at event `GITHUB_SHA`, and assert actual checkout.
5. **Termination overstatement risk:** `terminate()` is meaningful browser-worker abort semantics, but not native process/renderer/OS teardown proof. Split browser-worker facts from any future host-process proof.

## Explicit non-decisions

No runtime, database, provider, host, transport, authentication vendor, storage engine, framework, deployment or billing choice. No code copied. No third-party dependency added. No workflow, adapter, device, PR, CASE, LOOP, D-ID or OD-ID changed. P39 implementation/adapter conformance remains CLOSED; CASE-04 remains INCOMPLETE / `timed_out`; report format 1 remains unchanged. Exact-tree tests remain NOT RUN.

## Sources opened

- Pyodide 314.0.5 compatibility: https://pyodide.org/en/314.0.5/usage/wasm-constraints.html
- Pyodide 314.0.5 FAQ: https://pyodide.org/en/314.0.5/usage/faq.html
- Pyodide Web Worker guide: https://pyodide.org/en/314.0.0/usage/webworker.html
- Python threading: https://docs.python.org/3/library/threading.html
- Python thread-safety scope: https://docs.python.org/3/builtins/threadsafety.html
- AWS transactional outbox: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Apache Kafka 4.4 delivery semantics: https://kafka.apache.org/44/design/design/
- CloudEvents core/release: https://github.com/cloudevents/spec/releases ; https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- CloudEvents LICENSE (Apache-2.0): https://github.com/cloudevents/spec/blob/main/LICENSE
- GitHub push event SHA: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- GitHub secure use of actions: https://docs.github.com/en/actions/reference/security/secure-use
- actions/checkout releases: https://github.com/actions/checkout/releases
- HTML Living Standard workers: https://html.spec.whatwg.org/dev/workers.html
- Sigstore signing overview: https://docs.sigstore.dev/cosign/signing/overview/

All research claims above are VERIFIED only where the linked source was opened. Product runtime topology, native-thread adapter behavior, durable persistence and cryptographic ingress remain UNKNOWN / NOT IMPLEMENTED.
