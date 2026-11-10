# Full-power gap research: durable relay, fencing, mobile storage and execution evidence

**Date:** 2026-11-10  
**Status:** source-opened research and implementation-ready acceptance guidance; NOT IMPLEMENTED / NOT RUN  
**Target:** `marcelosofficial-ctrl/PocketCode-` branch `pocketcode-ai-workflow-director-research-2026-10-28`  
**Scope:** highest-value non-Claude-owned gaps after fresh boot/state/next-task review. This does not authorize source/test edits, select a runtime/database/transport/provider, change canonical LOOP/CASE/D IDs, spend money, deploy, or alter PR #2/#3/#4. RevDev is out of scope.

## 1. Ranked work items

1. **P39 owner gate and event/receipt correctness.** OD-01..OD-13 remain open; model defects and adapter obligations cannot be implemented coherently until policy choices are explicit.
2. **Durable event relay and receipt atomicity.** The current Python models are sequential/in-memory evidence; they cannot prove atomicity across a database, relay, browser storage, worker or external effect.
3. **Revocation and fencing.** A lease/lock can coordinate cooperative actors but cannot prevent a stale actor from writing unless the protected mutation checks a current generation atomically.
4. **PWA local recovery.** IndexedDB and OPFS have separate commit boundaries; eviction, force-close, quota and device behavior require explicit reconciliation.
5. **Execution-boundary evidence.** Browser Worker termination, Python guest return, wrapper completion, output finalization and receipt commit are different observations.

## 2. Primary-source research and reuse

### 2.1 Transactional outbox and replay

**VERIFIED:** AWS's transactional-outbox guidance explains the dual-write failure and the standard repair: write aggregate state and the outbox row in the same database transaction, then publish committed outbox rows separately. Delivery can be duplicated; consumers must be idempotent. Event order must match state-update order, and rolled-back transactions must not emit events. Source: [AWS Prescriptive Guidance, Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), opened 2026-11-10.

**VERIFIED:** Temporal's workflow documentation treats replay as deterministic reconstruction from recorded history, and its activity failure material warns that side-effecting activities may execute more than once when a worker loses the response after the external effect. An activity timeout does not prove that the remote side effect stopped. Sources: [Temporal workflow replay](https://docs.temporal.io/workflows), [Activity failure and retry model](https://docs.temporal.io/encyclopedia/detecting-activity-failures), [Temporal MCP integration](https://docs.temporal.io/develop/python/integrations/mcp). These are server workflow patterns, not a PocketCode dependency recommendation.

**PocketCode deliverable, proposed contract:**

- One semantic state transition commits **aggregate state/version + canonical immutable event + outbox row + idempotency binding** in one local transaction at the selected durable adapter.
- A no-op must not advance version or create a state-change event.
- Publish only after commit. A crash after publish but before marking delivered is expected to cause duplicate delivery.
- Consumer dedupe is durable and bound to event identity, tenant/grant, expected source, attempt/effect and canonical digest. A valid digest is integrity, not producer authentication.
- Per-aggregate sequence is contiguous. A gap or poison predecessor enters visible HOLD/quarantine. Later events do not skip it. Repair is an audited operation that preserves original evidence.
- Distinguish publish accepted, consumer processed, external effect completed, outbox delivered marker committed and receipt committed. None is a synonym for another.
- An ambiguous external effect is reconciled with the same immutable EffectId/intent. A new AttemptId records a real retry; it does not silently create a new logical effect.

This directly strengthens the existing P39-EVENT-05/06, P39-OUTBOX-04/05, P39-ORDER-04 and P39-CRASH-04 worklist. It does not claim exactly-once delivery. It makes duplicate delivery safe through durable idempotency and ordering.

### 2.2 Fencing and revocation

**VERIFIED:** Redis's official distributed-lock guidance explicitly says long-running work should use fencing tokens and warns that TTL expiration is based on a non-monotonic wall clock, so clock shifts can compromise mutual exclusion. Source: [Redis distributed locks, consistency disclaimer](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/), opened 2026-11-10.

**VERIFIED:** PostgreSQL's row-lock guidance says locks are held through transaction completion; its concurrency guidance requires handling deadlocks/serialization failures by retrying the full transaction decision, not blindly retrying only the last statement. Sources: [PostgreSQL 17 explicit locking](https://www.postgresql.org/docs/17/explicit-locking.html), [PostgreSQL serialization failure handling](https://www.postgresql.org/docs/16/mvcc-serialization-failure-handling.html).

**PocketCode deliverable, proposed contract:**

1. A durable, restore-safe authority issues monotonically increasing fence generations scoped to the protected resource/aggregate. A random lock token is not a fence.
2. Every protected mutation performs a compare-current-fence and mutation in the same transaction. A pre-check followed by a separate write is racy.
3. Lease expiry is a liveness/takeover mechanism only. The fence is the stale-writer safety mechanism. Worker-provided timestamps are observations, never lease authority.
4. On conflict, reload current grant, policy epoch, receipt revision, aggregate version and fence, then recompute the complete authorization/transition. Do not replay a stale decision.
5. Revocation semantics must be explicit at each boundary: before commit, after grant commit but before claim, during transfer, and on resume. If streaming is excluded by OD-01, explicitly defer transport cancellation claims rather than silently assuming a database fence retracts emitted bytes.
6. Preserve emitted/accepted/client-observed/client-acknowledged byte counts separately. Server progress cannot prove client receipt.

This is aligned with OD-02..07 and P39-POLICY-02..06 / P39-CLOCK-01 / P39-ID-01. No Redis/PostgreSQL dependency is selected.

### 2.3 Browser coordination and local storage

**VERIFIED:** the W3C Web Locks document opened is a **Working Draft dated 9 November 2026**, not a Recommendation. It coordinates cooperative windows/workers sharing a storage bucket. Its `steal` option releases held locks and rejects the previous holder's released promise, but the spec explicitly warns the previous code may continue running without exclusive-access guarantees. Source: [W3C Web Locks API, 9 Nov 2026 WD](https://www.w3.org/TR/2026/WD-web-locks-20261109/).

**VERIFIED:** IndexedDB transactions are active only in the creation/request event tasks and become inactive between event-loop tasks; they auto-commit when no new requests are placed and no requests remain. Transactions can abort on I/O failure, quota exceeded or user-agent crash. MDN also documents that a transaction completion event may occur before physical disk flush in some browser durability modes. Sources: [MDN IDBTransaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction), [IndexedDB 3.0 specification](https://www.w3.org/TR/IndexedDB-3/).

**VERIFIED:** `navigator.storage.persist()` is a request that may be granted or denied by browser policy; a true result means the bucket is persistent, not a backup against manual clearing, device loss or corruption. Source: [MDN StorageManager.persist](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist), page updated 12 October 2026.

**VERIFIED:** OPFS synchronous access handles are available in workers; `flush()` ensures the file contents include modifications made through `write()`. OPFS and IndexedDB are separate APIs, so there is no shared cross-API ACID transaction. Source: [MDN Origin Private File System](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system/).

**PocketCode deliverable, proposed recovery contract:**

- Use IndexedDB transaction completion as the commit boundary for metadata. Never treat an individual request's `success` as transaction commit.
- Keep transactions short. Do not hold them across network, Python/WASM execution, hashing, user interaction or timers.
- Treat Web Locks as a cooperative optimization, not a correctness authority. Avoid `steal` as routine recovery. If recovery preempts a lock, increment a durable fence in IndexedDB and require all writers to compare it in their own metadata transaction. Old code may continue running, but it must be unable to publish.
- Stage large artifacts under immutable, attempt-scoped OPFS names. Write, flush, close, read back and verify length/digest. Then commit a manifest reference and receipt revision in IndexedDB. This is a two-resource protocol, not a cross-API transaction.
- Recovery scans for: metadata with no file, partial file with staging metadata, complete orphan file with no manifest, manifest with missing/mismatched file, and committed receipt whose artifact reference cannot be verified. Quarantine ambiguous artifacts; never publish them by guessing.
- Request persistent storage and record the actual result, but display local work as device-local and exportable, not backed up or guaranteed durable. Test force-close, quota, eviction, app reinstall, iOS Home Screen origin and user-clearing separately.

This refines the existing PWA crash matrix and ORIGIN/PWA acceptance families without selecting a storage engine or asserting iPhone behavior.

### 2.4 Worker termination and result evidence

**VERIFIED:** the WHATWG HTML Living Standard (last updated 9 November 2026) defines Worker termination by setting the closing flag, discarding queued tasks, aborting the currently running script and emptying the dedicated worker's implicit message queue. It does not define a native child-process exit code or a cleanup receipt. Source: [HTML Living Standard, Web Workers](https://html.spec.whatwg.org/multipage/workers.html).

**VERIFIED:** MDN states `Worker.terminate()` immediately terminates the worker without giving it an opportunity to finish its operations. Source: [MDN Worker.terminate](https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate).

**VERIFIED:** OpenAI Agents SDK documentation separates run hooks, agent hooks, model/tool lifecycle and tracing spans. Its runner lifecycle guidance says cancellation is a request, and cancelled tasks should be awaited when finalizers, exceptions or owned resources affect correctness. Sources: [Agents SDK lifecycle hooks](https://github.com/openai/openai-agents-python/blob/main/docs/agents.md), [runner lifecycle reference](https://github.com/openai/openai-agents-python/blob/main/.agents/references/runner-lifecycle.md). Reuse the lifecycle-observation discipline, not its SDK as a dependency.

**PocketCode deliverable, proposed observation model (no schema freeze):**

| Observation | Authority | Does not prove |
|---|---|---|
| Guest return/exception/stdout/stderr | Guest/runtime data | Trusted wrapper completion, child exit, artifact integrity |
| Bootstrap await resolve/reject | Trusted wrapper | Native child exit, output closure, durable receipt |
| Worker error/messageerror/port close | Host browser | Why execution stopped, cleanup complete |
| Cancellation requested | User/coordinator | Cancellation took effect |
| `Worker.terminate()` invoked | Host browser | Graceful shutdown, termination acknowledgement, cleanup |
| Output callbacks closed and buffers finalized | Trusted output collector | Receipt committed |
| OPFS artifact readback verified | Host artifact collector | IndexedDB manifest/receipt committed |
| IndexedDB transaction complete | Browser storage API | Cross-API atomicity or permanent backup |
| Receipt read back after restart | Local durable state | Client received bytes or origin was uncompromised |

Keep the existing identity chain `CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt`. The coordinator validates provenance and produces the verdict projection. The renderer displays it; it must not infer missing facts. Preserve CASE-04 as INCOMPLETE / timed_out until trusted boundary evidence resolves it.

## 3. Red-team corrections to previous research and pass claims

1. **Web Locks were too easy to over-trust.** The current W3C WD says `steal` can release the old lock while the previous callback continues executing. Correction: the IndexedDB fence check at each protected write is mandatory; lock state alone cannot prevent stale publication.
2. **“Strict” IndexedDB durability was too close to a hardware guarantee.** A durability hint is a browser request/contract, not proof of device-level power-loss persistence across every iOS/WebKit build. MDN documents relaxed durability and an experimental, non-standard `readwriteflush` path in Firefox. Correction: label actual requested/reported durability, keep crash/restart readback tests, and never claim physical-media durability from `complete` alone.
3. **OPFS flush plus IndexedDB completion was described too much like a unified commit.** They are distinct storage APIs. Correction: retain immutable OPFS staging and an explicit two-phase recovery matrix; manifest/receipt commit happens only after readback, and orphan/missing-file states are quarantined.
4. **The Apple design commit was not indexed in the previous HEAD's index.** Claude's latest commit adds `APPLE_DESIGN_ENGINEERING_SPEC_20261108.md`, but INDEX.md had no row. Correction: this pass adds the missing index row. The design spec remains Claude-owned; no duplicate design work is attempted.
5. **The prototype CI scope was only an inference in the Apple spec.** Direct inspection confirms `.github/workflows/pocketcode-python-tests.yml` runs on pushes only when `scripts/**` or the workflow file changes, plus manual dispatch. It does not run for prototype-only HTML/CSS/JS changes. The checker is a static source-text checker and explicitly does not execute JavaScript or submitted Python. Correction: mark prototype edits as untested unless a future authorized workflow change adds prototype paths and real browser tests.

## 4. Competitor and reuse assessment

| Reference | Verified current evidence | Reusable idea | What not to import |
|---|---|---|---|
| Temporal | Official workflow replay and activity retry docs opened 2026-11-10 | Deterministic history replay; treat side effects as at-least-once; reconcile ambiguous completion | Full server/workers service and infrastructure |
| OpenAI Agents SDK | GitHub docs opened; repo reports MIT licence; PyPI project metadata in repository | Explicit run/agent/tool lifecycle hooks and parent/child spans | Provider-specific runtime, default tracing/data handling or SDK dependency |
| Cline | GitHub repository opened 2026-11-10; Apache-2.0 stated; checkpoint docs show a shadow Git repo with per-tool snapshots | Reversible per-operation snapshots and separate task conversation state | IDE/desktop runtime and full agent implementation |
| Aider | Official options docs show repo-map token budget, refresh policy and prompt-cache switches | Compact, refreshable repo map and stable context prefixes | Assuming its cache behavior transfers across providers |
| Sentry JS | Repository LICENSE opened; MIT applies to repository code, with a separate third-party CLI licence exception | Inspect envelope/outbox design only if a future browser-specific adapter is evaluated | Treating repository-wide MIT as covering every transitive/package dependency |

No source code was copied and no dependency is added. The references are pattern evidence, not a technology selection. Licence notices and package-specific dependency licences must be checked before any future code reuse. Maintenance is evidenced by live official docs/repositories opened during this pass; no release number is asserted where a release page was not verified.

## 5. Executable acceptance work, mapped to existing IDs

The following is the concrete test matrix to attach to existing P39/PWA/ORIGIN/EP/PYO work. It deliberately adds no canonical LOOP/CASE/D IDs.

| Existing family | Setup / fault injection | Required assertions |
|---|---|---|
| P39-EVENT-05 / P39-EVENT-06 | Crash before transaction commit; mutate event metadata; forge first event for unknown grant | State/event/outbox all commit or none; digest recomputed from canonical bytes; grant/source/scope validated |
| P39-OUTBOX-04/05 / P39-CRASH-04 | Relay A publishes then pauses; B takes over; A attempts delivered marker; redeliver duplicate; poison version N | Stale fence rejected atomically; duplicate effect deduped; N+1 blocked until N is audited/resolved |
| P39-CLOCK-01 / P39-ID-01 | Future/backdated worker time; restart/restore with deleted grants and prior fence | Authority clock wins; durable fence high-water and tombstones prevent reuse |
| P39-POLICY-02..06 | Revoke before commit, after commit/before claim, during transfer and on resume | Apply owner-selected policy epoch; recovered grant does not authorize new bytes; ambiguous authority fails closed |
| PWA storage recovery / ORIGIN-01..10 | Kill tab/app at every OPFS/IndexedDB boundary; quota error; clear origin; run controlled same-origin sibling probe | Reconcile missing/orphan/mismatched artifacts; no unverified manifest; report storage protection and origin exposure honestly |
| EP-21..25 / PYO-CTRL-01..15 | Worker error, default-channel forged message, terminate with no acknowledgement, output callback race, crash after terminal message before receipt commit | No native child exit inferred; no terminal PASS from guest channel; termination/cleanup unknown without authority evidence; receipt must be durable/read-back verified |

**Run protocol:** pin source SHA and environment; preserve deterministic fixture and expected event order; inject faults at each boundary; capture raw observations; run recovery twice to prove idempotence; verify no duplicate terminal event, artifact release or external side effect. Run sequential model tests first, then real concurrent-process and crash/restore adapter tests, then target-device tests. These layers cannot substitute for one another.

## 6. Scope and verification

- **VERIFIED:** source facts and platform rules linked above were opened during this pass. The branch's Pages prototype is still simulation-only; its static checker does not execute JS/Python.
- **INFERRED:** the contracts above are the safest adaptation to PocketCode's current identity/evidence requirements.
- **UNKNOWN:** actual deployed Pages URL/custom domain/headers, installed Pyodios worker topology, iPhone WebKit durability/OPFS behavior, sibling-origin inventory and production adapter behavior.
- **NOT RUN:** all new fault-injection scenarios, iPhone/Android tests, browser exploit tests, full Python suite on current branch and real durable-adapter tests.
- P39/P40 remains CLOSED; OD-01..OD-13 remain OPEN. No implementation, stack, dependency, deployment, spend, PR or canonical-ID change was made.
