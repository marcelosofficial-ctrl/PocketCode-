# PocketCode — Resource Containment and Teardown Evidence Review

**Research date:** 2026-11-01  
**Status:** Documentation research and proposed falsification design only. NOT RUN. No provider, runtime, account, store, or workload selected.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Scope:** Deepen PC-EXT-02 (resource boundary/host containment) and PC-EXT-04 (teardown/orphan reconciliation) without changing canonical LOOP/CASE meanings or selecting an execution provider.

## 1. Executive decision

Two claims must be kept separate:

1. **Resource containment:** a provider accepted or reports a configured limit; the actual execution boundary enforces it; the workload's resource failure is contained without destabilizing the orchestration worker or unrelated workloads.
2. **Teardown:** a control-plane request to stop/delete was accepted; the provider progressed through teardown; the exact execution resource reached a terminal destroyed state; no child process or provider resource remains active.

A successful API response, local database closure, timeout callback, process exit from the coordinator's perspective, or absence from a stale list/search result is not sufficient evidence for the second claim.

**Decision:** retain PC-EXT-02 and PC-EXT-04 as real provider/runtime integration gaps. Add a dedicated evidence contract and falsification matrix, but do not assign new canonical LOOP/CASE IDs. Treat all provider-specific observations below as desk research, not proof of runtime behavior. Do not select a provider on this evidence alone.

## 2. Resource-limit taxonomy: the mechanisms are not interchangeable

A future provider adapter must declare which enforcement mechanism applies to each requested limit. A generic `resource_limit_exceeded` boolean cannot explain what happened.

| Resource / behavior | Linux cgroup v2 or OS mechanism | What it actually establishes | What it does not establish |
|---|---|---|---|
| Memory hard ceiling | `memory.max` | Hard memory boundary for the cgroup; under pressure the kernel may invoke the OOM killer within that cgroup | That every allocation fails in the same way, or that the supervisor is safe if placed in the same cgroup |
| Swap ceiling | `memory.swap.max` | Hard cap on swap use by the cgroup | A substitute for `memory.max`; memory and swap are separate resource controls |
| Memory pressure | `memory.high` | Throttling/direct reclaim pressure | A kill threshold; crossing it does not itself invoke OOM killer |
| CPU bandwidth | `cpu.max` | Maximum CPU bandwidth per period for supported scheduler classes | A wall-clock deadline or a guarantee that a CPU-bound process is killed |
| Process/task count | `pids.max` | Prevents new fork/clone tasks once the hard task limit is reached | A memory limit or a guarantee that existing processes are terminated |
| Block I/O rate | `io.max` | Per-device read/write bytes-per-second and IOPS limits; requests are delayed when capped | A disk-capacity/quota limit |
| Disk capacity | Filesystem/project quota, bounded ephemeral volume, or provider-specific storage ceiling | Maximum persistent/ephemeral bytes available to the workload, if actually enforced at its storage boundary | `io.max`, `RLIMIT_FSIZE`, or a file-count limit |
| Per-file size | `RLIMIT_FSIZE` / provider equivalent | Maximum size of an individual file created by a process | Total workspace/disk usage across many files |
| File descriptors | `RLIMIT_NOFILE` | Per-process open-file descriptor ceiling | Process count or total disk usage |
| Wall-clock runtime | Provider hard TTL/deadline plus trusted supervisor termination | Maximum allowed elapsed execution time, if deadline enforcement and termination are confirmed | CPU time consumed or CPU bandwidth |
| Output collection | Worker/collector byte and time budgets | Amount of stdout/stderr retained or delivered | Whether the child process was terminated |
| Display | Client rendering cap | Amount rendered on the device | Runtime or collector truncation |

### 2.1 Important kernel details

- `memory.max` is the principal hard memory limit. The kernel documentation notes that usage may temporarily exceed the limit under some circumstances and some allocation types may return `-ENOMEM` without invoking OOM killer. Do not require every memory stress fixture to end with SIGKILL.
- `memory.events` is hierarchical by default and includes descendant events; `memory.events.local` reports only events local to the cgroup. The kernel's `memory_localevents` mount option changes `memory.events` to legacy local-only behavior, so record the actual mount option rather than assuming hierarchy. For a dedicated per-attempt root containing every descendant, the hierarchical file can capture subtree events; a local-only read at that parent can undercount child-cgroup activity. Conversely, a parent that contains multiple attempts can aggregate unrelated activity. Choose counters from the actual cgroup topology and prove the scope. (`pids.events` has a corresponding hierarchy/local distinction and `pids_localevents` mount option.)
- `memory.swap.max` is separate from `memory.max`. A memory-only test that ignores swap configuration may not establish the intended total memory pressure boundary.
- `cpu.max` expresses bandwidth as quota/period. It throttles eligible scheduler workloads; it does not terminate an infinite loop. Wall-time termination must be a separate, observed control.
- `pids.max` counts kernel tasks (TIDs), not just user-visible process leaders. `pids.events.local` and `pids.current` are relevant evidence.
- `io.max` limits throughput (BPS/IOPS), not total storage capacity. Disk exhaustion must be tested against the actual filesystem or volume quota.
- `cgroup.kill` sends SIGKILL to processes in the cgroup subtree and handles concurrent forks/migrations. It is a kill request/mechanism, not by itself a complete end-to-end proof that cleanup and provider resource release have finished.
- `cgroup.events: populated=0` means the cgroup subtree has no live processes. This is strong host-process evidence for that cgroup, but it does not prove that a cloud control-plane object, detached volume, snapshot, or billable resource has also been deleted.

### 2.2 Host-containment topology matters

A test that proves only that the workload hit a configured memory limit is incomplete. The supervisor/worker must not share the untrusted workload's kill domain.

For a cgroup-based implementation, document the cgroup tree and prove that:
- the supervisor and host control plane are outside the workload's killable subtree;
- every descendant process/thread created for the attempt remains inside the workload subtree;
- the workload cannot migrate itself or a sibling into another cgroup or change its parent-enforced limits;
- memory, CPU, PID and I/O controllers are actually available and enabled along the hierarchy;
- the worker heartbeat and a separate sibling canary remain responsive during bounded limit tests;
- the exact attempt's local counters and process population are collected before the cgroup is removed.

For a microVM or managed sandbox provider, use the provider's actual isolation and telemetry model instead of assuming host cgroup files are visible or authoritative. The provider must supply evidence that identifies the exact sandbox/attempt and supports the claimed boundary.

## 3. Teardown is a state machine, not a boolean

Proposed internal distinctions (not frozen public schema):

| State/evidence | Meaning | Permitted claim |
|---|---|---|
| `DELETE_REQUESTED` | Coordinator durably recorded intent to delete a known resource | Teardown requested |
| `DELETE_ACCEPTED` | Provider accepted the request or returned an asynchronous operation reference | Provider accepted request |
| `DESTROYING` | Authoritative provider read reports teardown in progress | Teardown in progress |
| `DESTROYED_CONFIRMED` | Authoritative provider read/event confirms the resource reached its documented terminal destroyed state | Provider resource destroyed |
| `PROCESS_TREE_EMPTY` | Trusted host/runtime evidence confirms the attempt's process subtree is empty | No live processes remain in that observed subtree |
| `RESOURCE_RELEASE_CONFIRMED` | Provider confirms the compute/storage resources governed by the relevant contract were released | Those identified resources released |
| `CLEANUP_UNKNOWN` | Request/response/observation was lost, stale, unavailable, or ambiguous | No cleanup success claim |
| `ORPHANED_TEARDOWN_REQUIRED` | Resource may still exist or consume resources and requires reconciliation | Cleanup action still required |
| `CLEANUP_FAILED_CONFIRMED` | Provider/runtime reports a terminal cleanup failure with attributable evidence | Cleanup failure confirmed |

Do not collapse these into one status. In particular:
- A local job/report can be closed while provider teardown remains unknown.
- A process can exit while the containing VM/sandbox, disk, volume, snapshot, or other billable resource remains.
- A provider may accept a delete request before destruction completes.
- A resource may disappear from a search/list index before the authoritative read model reaches a final state.
- Billing telemetry can lag actual resource termination. Cost reconciliation is a separate axis and must not be represented as proof of either process liveness or deletion.

### 3.1 Required reconciliation behavior

For one exact tenant/job/attempt/provider-resource identity:
1. Persist the delete intent and its stable operation/idempotency identity before calling the provider.
2. Treat lost acknowledgements and timeouts as ambiguous, not as success or failure.
3. Re-read the authoritative resource by stable ID or operation reference. Do not infer deletion from a list/search miss.
4. If the provider still reports active/deleting, continue bounded reconciliation with backoff and a durable next-check time.
5. If the provider reports a terminal destroyed/deleted state, append a new immutable cleanup observation with its source, provider version/time, and exact resource identity.
6. If lookup is unavailable or contradictory, preserve `CLEANUP_UNKNOWN` / `ORPHANED_TEARDOWN_REQUIRED`; do not close the cleanup gate.
7. Make repeated delete/reconcile operations idempotent. A late event from attempt N must not close attempt N+1.
8. Retain the original child execution outcome and exit code. Cleanup failure must not rewrite a known EXIT_ZERO or EXIT_NONZERO.
9. Keep a distinct operational alert/reconciliation queue for orphaned resources. A poison cleanup item must not block other jobs, and retry must not create a new sandbox.
10. Verify provider resource release separately from delayed invoice/cost reconciliation.

## 4. Official documentation findings: provider-neutral, no selection

The following are narrow claims from official documentation checked for this review. They are not independent security audits or runtime tests.

### 4.1 Linux cgroup v2

The kernel documentation defines the relevant controls and their limitations:
- `memory.max`, `memory.events.local`, `memory.swap.max`, `cpu.max`, `pids.max`, `io.max`, `cgroup.kill`, and `cgroup.events`.
- `cgroup.events: populated=0` can be used to start cleanup after the subtree has no live processes.
- `memory.events` is hierarchical unless local events are explicitly used.
- `io.max` is a throughput control, not a disk capacity quota.

Sources:
- https://docs.kernel.org/admin-guide/cgroup-v2.html
- https://docs.kernel.org/admin-guide/cgroup-v2.html#unpopulated-notification
- https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files
- https://docs.kernel.org/admin-guide/cgroup-v2.html#cpu-interface-files
- https://docs.kernel.org/admin-guide/cgroup-v2.html#io-interface-files
- https://docs.kernel.org/admin-guide/cgroup-v2.html#pid-interface-files
- https://man7.org/linux/man-pages/man2/getrlimit.2.html (RLIMIT_FSIZE and per-file semantics)

### 4.2 Firecracker as a self-operated boundary

Firecracker's production host guidance recommends using its Jailer (or equally/more restrictive constraints), seccomp, cgroups, namespaces, privilege dropping and carefully owned paths. The Jailer documentation explicitly says the operator remains responsible for cleanup after running the Jailer and warns about races in a `notify_on_release`-based cleanup approach. It also says the Jailer inputs are trusted and must be protected from unprivileged modification.

Implications:
- Firecracker is a building block, not a turnkey PocketCode execution service.
- Merely using a Firecracker microVM does not establish the surrounding host supervisor, resource policy, network policy, cleanup, storage, patching or reconciliation contract.
- Self-hosting transfers those responsibilities and operational risks to PocketCode. It is not currently justified under the $0 and no-PC constraints.

Sources:
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/jailer.md
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/seccomp.md

### 4.3 Modal Sandboxes

Current official documentation states:
- A default sandbox has no inbound network access and no access to Modal workspace resources, but outbound access to public IPs is allowed by default.
- `block_network=True` blocks all outbound traffic. CIDR allowlists are supported; domain allowlists are marked Beta and apply to TLS port 443. The docs warn about DNS and domain-fronting limitations.
- Runtime network-policy updates are documented as Alpha; the docs say the new policy takes effect immediately and established connections disallowed by the new policy are terminated. This is provider documentation, not independent proof of the data plane.
- Sandboxes can use gVisor or VM runtime isolation.
- CPU/memory resource requests are not hard ceilings by themselves. Separate limits cap bursting; resource billing is based on the greater of requested and actual usage.
- The JS SDK exposes `terminate({wait:true})`, which waits for the sandbox to finish and returns its exit code. This is stronger than a fire-and-forget terminate request, but it must not be generalized into proof that separately attached volumes or all billable resources have been released.

Implications:
- Any future test must set an explicit outbound policy at sandbox creation rather than rely on default egress denial.
- Distinguish request/reservation from hard cap.
- Do not treat a dynamic policy update as a safe pre-execution barrier unless the chosen runtime's applied state and data-plane behavior are independently proven.
- Current dynamic-update Alpha and domain allowlist Beta status are maturity risks.

Sources:
- https://modal.com/docs/guide/sandbox-networking
- https://modal.com/docs/guide/sandbox-resources
- https://modal.com/docs/sdk/js/latest/Sandbox
- https://modal.com/docs/sdk/py/latest/Sandbox (Python terminate(wait=True) and poll semantics)

### 4.4 Daytona Sandboxes

Current official documentation distinguishes stable v0 and v2 (v2 documentation labels itself alpha):
- The v2 lifecycle includes `destroying` and `destroyed`; deletion returns when teardown starts, and the resource reaches `destroyed` only after teardown finishes. A direct control-plane `get` reads current state; wait APIs can wait for target states.
- v2 Linux sandbox configuration exposes CPU/memory maxima, lifecycle timeouts, and network policy fields. Its documentation says timeout/idle actions can delete the sandbox.
- Stable v0 documentation says delete is fire-and-forget by default, returning when the API accepts deletion. It offers an explicit `wait` option to wait for the destroyed state.
- Daytona's v2 persistence documentation says deleting a sandbox discards its filesystem, memory and processes; external volumes/snapshots have independent lifecycles.
- Daytona v2 architecture documentation describes an API that writes state, publishes a job to a regional queue, and relies on runner events to update state. That architecture makes the asynchronous transition and authoritative state read important to test.

Implications:
- A Daytona adapter must not map successful delete-call return to cleanup-confirmed.
- It must wait/read until the documented terminal state, preserve UNKNOWN on timeout or lookup failure, and separately track attached volume/snapshot resources.
- Do not treat v2 alpha docs as a production guarantee. Verify the exact stable/selected API version and account capabilities before any implementation.

Sources:
- https://www.daytona.io/docs/en/v2/sandboxes/
- https://www.daytona.io/docs/en/v2/linux-sandboxes/
- https://www.daytona.io/docs/en/v2/architecture/
- https://www.daytona.io/docs/en/v2/persistence/
- https://www.daytona.io/docs/en/linux-sandboxes/

### 4.5 Cloudflare Sandboxes: API generation must be pinned

The official docs now describe two materially different API generations. Do not combine their lifecycle semantics:

**Current `@cloudflare/sandbox` 1.0 / Durable Object + Container model**
- A Durable Object provides the stable sandbox identity and retains its own storage (for example, session metadata or a snapshot ID) until application code deletes that storage. The container instance has a separate lifetime.
- Stopping/destroying the container ends its processes and instance-local disk. It does not, by itself, delete Durable Object storage, stored snapshot objects, or mounted R2 bucket objects.
- An inactivity timeout sends SIGTERM and stops the instance shortly after whether or not processes exit. Explicit `destroy()` stops the instance immediately without time for process cleanup.
- A Durable Object restart can leave the container instance running while the DO restarts; the inactivity timeout must be re-established. A pending `monitor()` observation is not a durable external cleanup record.
- The official lifetime page says mounted buckets outlive every instance, and snapshots can be used to restore writable root filesystem state into a new instance. Those are distinct resources and must be separately inventoried and deleted/expired according to their own contracts.
- Cloudflare states that Sandboxes are available on Workers Paid. Its Containers pricing page describes active-instance CPU/memory/disk billing and included monthly allowances on the paid plan. A zero-cost assumption is therefore invalid; DO storage, snapshots, buckets, and other products need separate cost/retention checks.

**Legacy Sandbox SDK 0.x**
- The 0.x lifecycle API documents `destroy()` as deleting the sandbox container's files, processes and sessions.
- Cloudflare explicitly labels those docs as SDK 0.x for existing applications and directs new work to the current Sandboxes model. The 0.x destruction statement must not be generalized to 1.0 Durable Object storage or separately mounted/persistent resources.

Implications:
- Pin the exact SDK/API generation and compatibility date in every provider capability record and test.
- A 1.0 container destroy can prove instance stop only; it cannot prove Durable Object storage, snapshots, mounted buckets or other separately managed resources were deleted.
- A 0.x `destroy()` result must be interpreted only within its documented sandbox-container scope.
- Do not rely on graceful application cleanup on explicit destroy or timeout.
- An inactivity timeout is not a substitute for durable external intent, reconciliation and resource inventory.
- Cloudflare is a paid-plan candidate, not a $0 implementation option under the current project gate.

Sources:
- https://developers.cloudflare.com/sandbox/concepts/lifetime/ (current Durable Object + Container lifetime, last updated 2026-10-22)
- https://developers.cloudflare.com/sandbox/sdk/api/lifecycle/ (legacy SDK 0.x API; explicitly versioned)
- https://developers.cloudflare.com/sandbox/ (availability and version routing)
- https://developers.cloudflare.com/containers/platform/pricing/ (active container resource billing)
- https://developers.cloudflare.com/sandbox/files/save-and-restore-a-workspace/ (snapshot and mounted storage behavior)

### 4.6 E2B

E2B's security page describes each sandbox as running in its own Firecracker microVM with its own kernel, and says sandboxes are destroyed on timeout or shutdown. This is useful vendor architecture information, but it is still a provider statement. The page alone does not supply PocketCode-specific evidence for exact resource limits, supervisor containment, process-tree emptiness, delete acknowledgement semantics, attached resource cleanup, or durable orphan reconciliation.

Source:
- https://e2b.dev/security

## 5. Revised falsification matrix for PC-EXT-02 and PC-EXT-04

These are subcases under the existing research plan, not new canonical acceptance IDs.

| Subcase | Setup / attack | Required observation | Failure condition |
|---|---|---|---|
| RES-01 limit configuration binding | Requested limits differ from defaults; inspect the exact sandbox/attempt's effective configuration | Provider/host authoritative effective limits, identity-bound | Only request payload or adapter echo is available |
| RES-02 memory boundary | Bounded allocator crosses memory ceiling in a dedicated test sandbox, including a nested child cgroup when the actual topology uses one | Effective limit-owner configuration; before/after hierarchical and local counter snapshots selected for the exact tree; exact process-to-cgroup membership; independently observed child outcome | Supervisor or unrelated workload is killed/degraded, counter scope is unknown, or one OOM counter is treated as causal proof |
| RES-03 swap accounting | Exercise memory pressure with declared swap policy | Effective swap cap and relevant counters/state | Swap remains unbounded contrary to declared policy |
| RES-04 CPU bandwidth vs deadline | CPU-bound workload exceeds bandwidth request, then separate wall-clock deadline | Throttling/accounting separated from deadline event and termination | CPU throttling is misreported as timeout, or infinite loop survives hard deadline |
| RES-05 process/task ceiling | Bounded fork/thread pressure | Effective task limit, local event evidence, no host-wide task exhaustion | Host worker or sibling task capacity is exhausted |
| RES-06 disk capacity vs I/O rate | Write many files and one oversized file; separately saturate I/O | Filesystem/volume capacity evidence distinct from I/O throughput and per-file cap | `io.max` or `RLIMIT_FSIZE` is claimed as total disk quota |
| RES-07 output cap | Emit bounded large stdout/stderr with process status independently observed | Runtime termination vs collector loss vs display truncation | One boolean hides the enforcement layer or fabricates child termination |
| RES-08 supervisor/sibling containment | Workload hits bounded memory/OOM, PID, CPU, disk and output-pressure cases while the orchestration worker, its own bounded buffers, host-side VMM/log collector, and a second independent run are observed | Supervisor/worker and host-side log collector are outside the workload's kill domain and required namespaces/filesystem/credentials; every host-side stdout/stderr/serial/log buffer and sink has a hard bound; worker heartbeat and bounded memory remain healthy; second run continues; exact workload failure is attributed | Worker or log collector shares the workload kill domain; guest-influenced VMM logs can exhaust host memory/disk; output is only truncated after unbounded buffering; sibling is degraded; or collateral host impact occurs |
| RES-09 descendant termination | Workload forks descendants, daemonizes, attempts cgroup/process migration where the runtime exposes such interfaces, ignores graceful termination, and races with timeout cleanup | Trusted supervisor requests escalation; workload cannot write/migrate through delegated cgroup controls; all attempt descendants are observed gone; `cgroup.events: populated=0` or provider-equivalent process-tree evidence is captured before teardown; observer survives outside the workload kill domain | Parent exits but a descendant remains, workload can move a process outside the observed subtree, observer is killed, or cleanup is inferred from parent PID alone |
| RES-10 host-side VMM/log pressure | Guest workload floods serial output when enabled, VMM stdout/stderr, or guest-influenced log files while the host runs a second VMM and orchestration worker | Serial is disabled where not needed or has an explicit token-bucket rate limit; if rate-limited, `uart.rate_limiter_dropped_bytes` is collected as loss evidence; VMM log files/pipes and host sinks are independently bounded; host disk and memory remain bounded; worker and sibling VMM remain healthy | Serial is assumed rate-limited when the optional limiter is absent (default is unrate-limited), log sink can grow without bound, loss is hidden, or collector blocks/degrades host/another run |
| TDN-01 delete accepted but pending | Provider accepts deletion asynchronously | State remains DELETE_ACCEPTED/DESTROYING until terminal observation | API 2xx/202 response is mapped directly to CLEANUP_CONFIRMED |
| TDN-02 lost delete acknowledgement | Provider may have accepted delete but coordinator times out or loses the response | Reconcile the same stable resource and operation identity; no duplicate resource is created; UNKNOWN is retained until an authoritative terminal observation | Retry creates a new sandbox, or closes cleanup without evidence |
| TDN-03 provider lookup unavailable or ambiguous 404 | Delete request accepted/ambiguous; subsequent reads fail, return 404, or use a potentially wrong account/region/project scope | Verify exact tenant/account/region/resource scope and documented read consistency; keep CLEANUP_UNKNOWN / ORPHANED_TEARDOWN_REQUIRED and a durable retry schedule until authoritative absence/destruction is established | A list miss, unscoped 404, eventual-consistency gap, or missing state is treated as deletion; provider auto-expiry is treated as proof |
| TDN-04 terminal deletion | Exact-resource provider read reaches documented destroyed/deleted terminal state after a stop/delete operation | Immutable event binds tenant/job/attempt/provider-resource/account/region/version and terminal state; stopped/paused is not treated as destroyed | Search miss, local DB close, stopped/paused state, or stale event substitutes for authoritative destruction |
| TDN-05 attached resource independence | Sandbox has attached volumes, snapshots, persistent disks, object stores/buckets, Durable Object or equivalent control-plane storage, preview URLs, tunnels, or other separately managed resources | Each resource and control-plane identity is inventoried by stable tenant/job/attempt/provider-generation identity and has its own lifecycle/release evidence; stopped compute does not imply metadata, snapshots, buckets, or storage were deleted or billing stopped | Sandbox destruction is assumed to delete independent resources, durable control-plane state, snapshots, or every chargeable resource |
| TDN-06 late cleanup event | Attempt N is deleted after attempt N+1 starts | Event remains bound to N and cannot mutate N+1 | Stale cleanup event closes the wrong attempt |
| TDN-07 reconciliation crash | Coordinator crashes after provider accepted delete but before persisting the response or cleanup observation | Restart resumes lookup/reconciliation from durable intent for the same resource/operation identity; repeated reconciliation is idempotent; poison records do not block later jobs | New resource or untracked orphan is created, evidence is lost, or one poison item stalls the queue |
| TDN-08 cleanup vs billing lag | Provider terminal state observed while usage/invoice data is delayed, pending, or later adjusted | Resource termination and provider-reported cost reconciliation remain separate axes; cost remains PENDING/UNKNOWN until authoritative usage/charge data is reconciled | Pending invoice appears as final zero cost, or billing telemetry is used as a proxy for process liveness/deletion |

### 5.1 Safety of the future test harness

Do not use an unbounded allocation, uncontrolled fork bomb, disk fill, or network exfiltration test. Once separately authorized and a provider is selected:
- run only in a disposable, low-quota test environment with a hard external watchdog;
- use bounded, calibrated workloads and a separate supervisor/worker heartbeat;
- cap concurrency and storage before launch;
- predefine stop conditions and ensure a kill/reconcile path exists;
- capture exact configuration, identity, before/after telemetry and provider state;
- stop immediately on host instability, unexpected egress, cross-tenant visibility, missing termination evidence, or unexpected billing.

No such test is authorized or performed by this document.

## 6. Integration with existing authoritative documents

- `AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md`: PC-EXT-02 and PC-EXT-04 remain the summary entry points. This review supplies the detailed resource/teardown subcases.
- `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`: keep execution observation, evidence quality, verdict, disposition, cleanup and artifact release separate.
- `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md`: RH-05/06/07/12 preserve cleanup updates, contradictions, crash recovery and cross-store publication.
- `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md`: provider operation identity, trusted evidence acceptance, idempotent lookup/reconciliation and independent proof layers.
- `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md`: provider/runtime work remains blocked until owner decisions, provider selection, store semantics and actual integration evidence exist.
- `SECURITY.md`: server-side CPU, memory, process, disk, output, concurrency and per-user limits plus cleanup, network and monitoring are launch gates.

No existing checklist is superseded. RES/TDN are test-design labels local to this review and must not be confused with canonical LOOP/CASE or other projects' acceptance IDs.

## 7. Current disposition and hard stops

- Resource containment: **SPECIFIED GAP / NOT RUN**.
- Teardown/orphan reconciliation: **SPECIFIED GAP / NOT RUN**.
- Provider selection: **NONE**.
- Runtime/store/account: **NONE**.
- Budget: **$0; no paid usage or provider calls**.
- Implementation: **NOT AUTHORIZED**.
- Canonical LOOP/CASE acceptance: **UNCHANGED**.
- Main, PR #2 and PR #3: **NOT TOUCHED**.
- Local PC/runtime/queue state: **UNKNOWN**.

The next engineering review should challenge the RES/TDN cases and the source-specific lifecycle semantics. It must not promote desk research or mocked state transitions into runtime proof.


## 8. Additional attribution correction: OOM counters are not self-authenticating

A final kernel-source pass found an important nuance for RES-02. The kernel defines `memory.events.local:oom_kill` as the number of processes belonging to the cgroup killed by **any kind of OOM killer**. Therefore, an increase in `oom_kill` alone does not prove that this cgroup's own `memory.max` boundary caused the kill.

Likewise, a workload may hit `memory.max` and receive `-ENOMEM` without an OOM kill. A defensible cgroup-based test should capture, for the exact target cgroup:
- effective `memory.max`, `memory.high`, and `memory.swap.max` before launch;
- before/after values of local `memory.events.local` counters, especially `max`, `oom`, and `oom_kill`;
- exact cgroup path/identity and hierarchy, plus workload PID-to-cgroup association;
- trusted kernel/provider termination evidence and the child process exit/signal observation;
- supervisor and sibling-canary health.

Interpret the combined evidence rather than a single counter. Do not require `oom_kill` to increase for every limit-hit fixture, and do not label an arbitrary OOM kill as a cgroup-limit violation without corroboration. This is a proof-attribution refinement, not a new product requirement.


## 9. Claude's independent challenge and evidence-boundary reconciliation (2026-11-01)

**Review limitation:** Claude reported that it could not read this review, the lifecycle regression plan, or the readiness backlog during its review attempt. Its response is therefore recorded as a useful adversarial challenge, not as a verdict on the contents of those three documents. The points below were reconciled against the pinned canonical acceptance and the exact research-branch documents in this pass. No implementation or runtime test was performed.

### 9.1 Canonical acceptance gaps remain explicit

- The canonical LOOP/CASE contract has no standalone acceptance ID for "cleanup confirmed." Cleanup appears as a gate/consequence in the first-useful-proof text and as a cancellation-observation concern in CASE-05; CASE-06 covers a worker/provider failure before a trustworthy program result. Neither is a complete provider resource teardown/reconciliation acceptance case.
- The canonical lifecycle status list is accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected, and infrastructure_failed. There is no resource-limit lifecycle status. Do not introduce resource_limit_exceeded as though it were canonical.
- CASE-07 is the configured stdout/stderr output-limit scenario. CASE-14 is output-file path/size validation. Neither is a general acceptance test for total workspace disk quota, filesystem exhaustion, I/O throughput, or per-file operating-system limits.
- Do not silently assign OOM, ENOSPC, SIGXFSZ/per-file-size rejection, PID exhaustion, or I/O throttling to a lifecycle status. Preserve the exact cause, enforcement layer, child terminal evidence, and infrastructure attribution. The canonical user verdict remains PASS/FAIL/INCOMPLETE; whether a particular enforced limit is a confirmed program/runtime failure or an infrastructure failure depends on the actual ownership/contract and remains an owner/architecture decision where D-01/D-02 do not settle it.
- RES/TDN labels remain supplementary falsification identifiers. They do not amend canonical LOOP/CASE or create a cleanup status.

### 9.2 Correct cgroup event attribution for nested workloads

The kernel documentation confirms:
- memory.events is hierarchical by default and counts descendant events. The system-wide memory_localevents mount option changes that behavior to local-only.
- memory.events.local reports only events local to the specific cgroup. A local read at a job parent can therefore miss events recorded in child cgroups.
- oom records that the cgroup's memory usage reached the limit and an allocation was about to fail. The event is not raised in every allocation-failure mode.
- oom_kill counts processes belonging to the cgroup that were killed by any OOM killer. It does not, by itself, prove that this cgroup's own memory.max caused the kill.
- pids.events is hierarchical by default; pids.events.local is local. The pids_localevents mount option changes the default aggregate behavior.

**Test rule:** record the kernel version, cgroup v2 mount options, exact hierarchy, the cgroup that owns each hard limit, exact workload PID/TID membership, and before/after hierarchical and local event snapshots. For a dedicated per-attempt root that contains all descendants, hierarchical counters can expose descendant events. Local counters remain useful for identifying which cgroup recorded local activity. Do not use an ancestor that mixes unrelated attempts as a per-attempt source. Persist all needed counter snapshots before removing the cgroup.

Treat the following as separate observations:
1. limit pressure/approach (max, oom, pids.events);
2. OOM victim evidence (oom_kill);
3. supervisor-requested timeout/cancellation signal and its timestamp;
4. trusted child exit/signal observation;
5. process-tree-empty confirmation.

A timeout/OOM race must retain both event streams. Exit status 137 or SIGKILL alone does not identify the cause. If the trusted observer cannot establish which control caused termination, report cause as UNKNOWN/ambiguous rather than selecting a convenient explanation. The supervisor and evidence collector must live outside the workload's kill domain; if they can be OOM-killed with the workload, missing telemetry is not a clean pass. Capture counters before cgroup removal because the evidence interface disappears with the cgroup.

### 9.3 Resource enforcement is a vector, not one generic kill

Keep these cases distinct and do not infer a kill from a throttle:
- memory hard limit and swap limit;
- memory.high pressure/throttling;
- CPU bandwidth throttling versus CPU-time and wall-clock deadline;
- PID/task creation rejection;
- disk capacity/ENOSPC versus per-file-size enforcement;
- I/O BPS/IOPS throttling;
- runtime output enforcement versus collector/transport/display truncation.

For disk exhaustion, preserve whether the exhausted resource was a per-job quota controlled by PocketCode/provider or shared infrastructure. A per-file limit is not a workspace quota; an I/O rate limit is not a capacity limit. The same OS symptom can require different product attribution depending on which boundary owned the resource.

### 9.4 Teardown counterexamples added without changing canonical IDs

The original TDN cases are strengthened above. Two additional supplementary cases are now explicit:

| Subcase | Setup / attack | Required observation | Failure condition |
|---|---|---|---|
| TDN-09 lost create acknowledgement | Persist create intent, then provider creates a resource but the acknowledgement containing its ID is lost | Durable pre-call intent/idempotency identity; bounded, correctly scoped reconciliation/list pagination discovers or rules out the resource; exactly the same logical create is reconciled without blind duplicate creation | No durable intent, incomplete pagination/scope, a second resource is created, or orphan is silently forgotten |
| TDN-10 warm/reused sandbox contamination | A provider reuses a warm sandbox or task environment after a job appears complete; a daemonized child/agent remains | Prove job-level process-tree emptiness and sandbox reuse isolation; a later attempt cannot inherit an earlier attempt's process, files, credentials, tunnels, or state | Parent exit or per-job report closure is treated as full cleanup, or stale child/state leaks into another attempt |

Additionally, TDN-06 must cover the case where a retry/attempt shares or is incorrectly attached to a still-live resource from a previous attempt. Cleanup for attempt N must not terminate or close attempt N+1, and attempt N+1 must not inherit attempt N's live process or provider resource. TDN-10's stale-observation negative case must re-check state after late child/retry activity; one earlier empty-tree observation is not perpetual proof.

### 9.5 Isolation and proof-layer additions

RES-08 is the worker-containment test, not merely a workload-limit test. Its evidence should show the orchestration worker is outside the workload cgroup/PID namespace and does not share the untrusted workspace or credentials; its own stream buffers are bounded before rendering; a second concurrent attempt remains healthy while a bounded adversarial attempt is terminated. A collector that truncates after buffering unbounded output does not prove worker protection.

Use this evidence ladder:
1. **Pure-helper tests:** test fail-closed interpretation of typed evidence and state transitions. They do not prove that an observer is authentic.
2. **Fake-adapter protocol tests:** test call order, retry counts, acknowledgement loss, asynchronous delete, lookup scope, pagination, and reconciliation decisions. They do not prove provider behavior.
3. **Persistence tests:** prove durable write-ahead create/delete intent, atomic reservation, restart recovery, immutable observations, and stable identity. A lost-create-ack orphan case is blocked until this layer exists.
4. **Local Linux cgroup tests:** only in an explicitly approved, isolated environment; prove actual kernel enforcement and observer/sibling survival for that exact kernel/cgroup topology. No such local test was run here.
5. **Provider/runtime tests:** prove the selected provider's real enforcement, deletion, attached-resource release, and telemetry behavior. LOOP-14's explicit approval/verified zero-cost gate applies; fake tests and desk research cannot prove that billing stopped.

Firecracker remains a VMM/microVM building block, not a managed sandbox service. When self-operated, the owner of the deployment remains responsible for the host cgroups, jailer/chroot, tap/network devices, root filesystem copies, supervisor, durable cleanup and orphan reconciliation. Provider and kernel documentation are design inputs, not observed PocketCode behavior.

### 9.6 Review disposition

- Claude's canonical-gap observations are ACCEPTED as scope clarifications.
- The cgroup local-versus-hierarchical concern is ACCEPTED, with the kernel mount-option caveat added.
- The timeout/OOM race, observer survival and pre-removal snapshot requirements are ACCEPTED as supplementary evidence requirements.
- The teardown counterexamples are ACCEPTED as additional TDN coverage.
- No new canonical LOOP/CASE ID, lifecycle status, schema, provider choice, or architecture decision is made here.
- All RES/TDN cases remain SPECIFIED ONLY / NOT RUN. No host, provider, runtime, account, billing, queue, source, tests, Actions, PR, merge or deployment was touched.


## 10. Provider-version and host-telemetry correction (2026-11-01)

A fresh official-documentation pass identified two additional precision requirements:

1. **Cloudflare API generation separation.** Current `@cloudflare/sandbox` 1.0 documentation describes a Durable Object whose storage/identity outlives the container instance. Instance-local processes and writable disk end when the instance stops, but stored snapshot metadata and mounted R2 bucket objects have independent lifetimes. The legacy Sandbox SDK 0.x `destroy()` documentation describes deletion of that SDK's sandbox files/processes/sessions. These are not interchangeable claims. Pin SDK generation and test instance stop, DO storage deletion, snapshot lifecycle and mounted bucket deletion independently. The current service is Workers Paid; container active-resource billing is documented separately from instance stop. Sources are listed in Section 4.5.

2. **Firecracker host-side output is part of the attack surface.** Firecracker's production setup document warns that guest-controlled serial output and guest-influenced log generation can create unbounded host memory/storage usage unless the operator bounds, rate-limits or safely discards those streams. The API schema specifies an optional serial token-bucket rate limiter; when absent (the default), serial output is not rate-limited, and when exceeded guest writes are dropped and counted in `uart.rate_limiter_dropped_bytes`. RES-10 now requires the limiter/drop metric or serial disablement plus independently bounded log sinks. This is additional to bounding the PocketCode worker's own stdout/stderr collector; both the VMM/host logging path and the app-level collector must be bounded.

3. **Observed cgroup emptiness requires control of membership.** `cgroup.events: populated=0` means no live processes remain in the observed cgroup subtree at that observation time. It does not prove a workload process was never moved outside that subtree. RES-09 now requires that untrusted code cannot write/migrate via delegated cgroup controls and that the supervisor's process-membership boundary is enforced. A process-tree-empty observation is time- and scope-bound, not a permanent statement about all resources.

4. **Modal create and detach are not cleanup synonyms.** Current Python SDK docs state that sandbox container creation is asynchronous, `detach()` disconnects the client and cleans connection resources, while `terminate(wait=True)` waits for sandbox execution termination and returns the exit code. The SDK also exposes identity-based reattachment/listing (`from_id`, `from_name`, `list`) and terminated lookup by name. Future adapter evidence must distinguish create intent from actual container readiness, connection detach from execution termination, and execution termination from separately attached volume release. See https://modal.com/docs/sdk/py/latest/Sandbox.

No provider selection, API call, account, workload, local host test, implementation or cost decision is authorized by this documentation update. All RES/TDN cases remain NOT RUN.


### RES-10 implementation evidence precision

The Firecracker API schema defines the serial rate limiter as optional. When configured, over-rate guest writes are silently dropped and counted in `uart.rate_limiter_dropped_bytes`; when absent, serial output is not rate-limited. Therefore a test must verify the effective configuration and read the metric, not infer rate limiting from the existence of Firecracker. The production host guide separately requires bounded handling of VMM stdout and guest-influenced log files. Sources: https://github.com/firecracker-microvm/firecracker/blob/main/src/firecracker/swagger/firecracker.yaml ; https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md.


## 11. Pinned Linux strict-service source audit — 2026-11-03

**Evidence class:** PINNED SOURCE INSPECTION and upstream test-source review only. No compile, test execution, host setup, device test, workflow run, provider call, or workload occurred. This section does not select or adopt Happy Agent, change PocketCode's contract, or amend canonical acceptance.

### 11.1 Scope and source pins

Reviewed the Linux service implementation in `slopus/happy-agent` at immutable commit `fb9f68ff10333068b87436bd1d531d6d353f5c93`, including:

- `platform/service_filesystem.rs` blob `ec7a980b3e757c255b5678efc21d1f97df5c82d2`
- `platform/service_cgroup.rs` blob `c7a831261f5fcacd0f38263f01ef7dc00439f6b9`
- `service_policy.rs` blob `6fce0adcb5c9fe2605bd638e1e9e665bf24bdc86`
- `platform/linux.rs` blob `65e0df6e5c603d9a288fa52a4ba5611191df251a`
- `exec.rs` blob `f4f98f482f791b9f807ec7504a24689e38a62fe4`
- `policy.rs` blob `262cb36881b719b9198d0c616142af706e053ff6`
- `proxy/hosts.rs` blob `145f8762a9781cae3ac9178cb09ef0e7c47ab4f8`
- `proxy/egress.rs` blob `7e797ad21086834dcd253bcebdadc357d03c992f`
- `platform/service_bridge.rs` blob `25964e69011c487e5387125e640d9ddc708702b6`
- Native service tests in `native/supervisor/tests/services.rs` at the same commit.

### 11.2 Controls that are genuinely present in source

1. **Private filesystem construction.** The service starts from an empty, private, daemon-owned root. It mounts a bounded tmpfs root, a fixed read-only runtime, private home/temp areas, and only explicitly selected workspace inputs. It does not expose the normal host home, general host `/etc`, `/var`, or daemon state through this service root.
2. **Pinned read-only input mounts.** Input sources are opened with `openat2` using no-symlink/no-magic-link resolution, then mounted through the held file descriptor. This reduces path-swap and symlink redirection races. Input directories are recursively mounted read-only and marked `NODEV`/ `NOSUID`.
3. **Clean execution environment.** The service uses an explicit environment allowlist: `PATH`, `HOME`, `TMPDIR`, `TERM`, `NO_COLOR`, `PAGER`, and `LANG`, plus explicit supervisor overrides. It does not merge the supervisor's ambient credentials into the service child.
4. **Kernel memory and process controls.** A unique cgroup v2 is created per execution. The service sets `memory.max`, `memory.swap.max=0`, `memory.oom.group=1`, and `pids.max`; the workload is moved into it before `execve`. Cleanup requires `cgroup.events` to report `populated 0` before the group is removed.
5. **Namespace and syscall restrictions.** The workload enters user, mount, PID, IPC, UTS and isolated network namespaces. Capabilities are dropped and privilege transitions locked. The service seccomp filter blocks selected namespace/mount operations, `io_uring`, Unix-domain sockets/socketpairs, and other escape-relevant operations. This is a targeted deny filter, not a demonstrated default-deny syscall allowlist.
6. **Network-off is structurally fail-closed.** Service policy validation requires an empty outbound list, `egress=false`, and no outgoing proxy when network access is disabled. When egress is enabled, service policy requires an outbound list and proxy. The workload has no direct route to the host network.
7. **DNS check/connect consistency.** For proxy egress, the requested hostname and exact port are checked, name resolution is performed once, and the filtered addresses from that same resolution are the addresses passed to TCP connect. This avoids a second-resolution DNS rebinding gap.
8. **Lifecycle evidence.** The controller identity is checked during startup; native process identities include PID plus process start time; startup readiness is committed before the workload is admitted; and the parent waits for namespace-init exit, stops the egress process, and checks cgroup emptiness. The bridge has a private directory, authenticated token, bounded connection count, and connection timeouts.

The upstream native test source includes cases for private environment/filesystem, read-only selected inputs, detached descendants, memory and PID limits, host Unix-socket denial, symlinked input rejection, authenticated bridge operation, abrupt supervisor death, and the distinction between application exit 125 and native startup failure. Many of these tests are marked ignored unless delegated cgroups are available; their inclusion in source or a release script is not evidence that CI or a real kernel run passed.

### 11.3 Gaps against PocketCode's one-shot execution contract

| Gap | Source-level finding | PocketCode consequence |
|---|---|---|
| No wall-clock deadline | Service policy has no deadline field and the Linux supervisor waits for namespace init without an internal absolute execution deadline. | **CASE-04 is not satisfied.** A non-yielding or blocked workload can persist until an external controller intervenes. A client timeout is not a substitute. |
| No CPU quota or CPU-time budget | The service cgroup requires memory and pids controllers only. It does not configure `cpu.max` or a CPU-time budget. | Memory/PID containment must not be described as full resource containment. CPU bandwidth, CPU time and wall time remain separate controls. |
| No complete storage/file budget | The root, home, temp and scratch mounts use tmpfs size limits, but there is no explicit total workspace byte/file-count contract, per-file output cap, or independent disk quota in this service policy. | The existing PocketCode input/output caps and artifact rules still need independent enforcement. A tmpfs size option is not proof of all file-count, file-size and output-collector requirements. |
| Special input files are not comprehensively excluded | The source opens selected paths and contains an explicit comment that named pipes in selected inputs are accepted in the first version. | FIFO/device/socket/special-file inputs need a defined policy. A FIFO can block a task, reinforcing the need for an enforced deadline and regular-file-only input validation. |
| Inputs are live mounts, not immutable snapshots | The mount pins the selected source inode/path against redirection, but does not copy/hash an immutable content snapshot. | Host-side edits to a selected input tree may be visible during execution. PocketCode should stage bounded regular-file snapshots and bind their hashes to the run, or explicitly accept live-input semantics. |
| Scratch overlap is under-specified | Input destination mounts are checked for overlap. Scratch paths are normalized, but there is no equivalent complete duplicate/ancestor/descendant overlap validation across scratch entries and input destinations. | Reject ambiguous overlapping mounts or define and test deterministic overlay semantics before reuse. |
| Egress-on address filter has gaps | The service checks exact hostname/port and blocks many private/special ranges, but its hand-maintained IP filter is not a complete positive global-unicast policy. It omits IANA special ranges including IPv4 `192.88.99.2/32` and IPv6 documentation `3fff::/20`. | Keep egress disabled for the first proof. Any later egress broker needs an up-to-date positive destination policy and tests for all IANA special-purpose ranges, not only RFC1918/private addresses. |
| Hostname approval is not full application-host binding | The proxy authorizes the TCP destination hostname/port, then relays a byte tunnel. It does not establish that TLS SNI or HTTP Host inside that tunnel matches the approved hostname. | Do not claim strict domain-level egress enforcement from a TCP connect allowlist alone. Shared CDN/IP routing and domain-fronting behavior require L7 enforcement or a narrower broker. |
| Egress child has a parent-death race | The Linux egress child calls `PR_SET_PDEATHSIG` but does not check the return value or re-check its expected parent PID before serving. Linux documents a fork-to-`prctl` race where the parent can exit before the setting takes effect. | Fix with checked setup plus parent-identity recheck and an adversarial parent-death regression test before treating proxy teardown as reliable. |
| End-to-end output caps are not established by this service layer | The inspected service supervisor does not itself define PocketCode's stdout/stderr collector budget or report truncation contract. | The caller/compute layer must prove streaming byte caps before unbounded buffering, overflow disposition, collector survival and truthful truncation. Display clipping alone does not qualify. |
| Platform boundary is Linux-specific | This strict service requires Linux namespace/cgroup facilities and delegated cgroup v2 controllers. The service path is explicitly unavailable in the macOS adapter and is not a phone-local iOS/Android runtime. | This is a server/host-side reference pattern only. It does not solve PocketCode's on-phone runtime or Windows execution boundary. |

The IP-range findings are independently checked against the IANA special-purpose registries: `192.88.99.2/32` is not globally reachable in the [IPv4 registry](https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml), and `3fff::/20` is documentation space and not globally reachable in the [IPv6 registry](https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml). The Linux parent-death behavior is documented in [PR_SET_PDEATHSIG](https://man7.org/linux/man-pages/man2/PR_SET_PDEATHSIG.2const.html).

### 11.4 Mapping to existing PocketCode acceptance

- **LOOP-12 / CASE-15:** the Linux service is a useful source-level example for private filesystem, environment allowlisting, process/resource containment and default-deny networking. It is not PocketCode evidence and is not verified against our cases. Egress-off configuration is the correct first-proof posture.
- **CASE-04:** blocked by the missing trusted wall-clock deadline and confirmed termination path.
- **CASE-07 / LOOP-07:** output collector byte/time budgets and report truncation semantics are not established by this service source.
- **CASE-08 / CASE-14:** normalized paths and selected input mounts are useful patterns, but special-file rejection, immutable input staging, bounded output files and release-time authorization remain separate requirements.
- **CASE-13:** a unique execution ID does not prove durable coordinator idempotency, lost-ack recovery or exactly-once reservation.
- **CASE-16:** per-execution cgroups support isolation by identity, but concurrent report/output isolation and cross-run correctness are not proven by these source tests.
- **RES/TDN:** use this source as a test-design reference for resource enforcement and cleanup reconciliation. Keep RES/TDN supplementary; no canonical ID or lifecycle status is added or remapped.

### 11.5 Adaptation sequence for PocketCode

1. **Keep the first proof narrow:** fixed Python entrypoint, pinned runtime, no general shell, no arbitrary package install, no user-selected privilege, no provider credentials, and egress fully disabled. Continue comparing local/browser and other paths on the same frozen task; do not select Pyodide or a hosted runtime from this source audit.
2. **Make it a real bounded job:** trusted monotonic wall deadline recorded before dispatch; CPU bandwidth cap and, where required, CPU-time budget; hard memory/swap and process limits; bounded workspace/storage/file count/per-file/output sizes; independent worker/collector limits. Each limit needs effective-configuration evidence.
3. **Make inputs deterministic:** accept individually selected regular files only; reject symlinks, FIFOs, devices, sockets and unsupported file types; enforce per-file/aggregate byte and count caps; stage immutable snapshots and bind content digests to the attempt. Reject overlapping input/scratch mount destinations.
4. **Make timeout/cleanup authoritative:** the watchdog must live outside the workload kill domain; use a race-safe whole-cgroup termination mechanism where supported; capture exit/signal, limit counters, deadline cause and process-tree state before resource removal; report cleanup separately and keep UNKNOWN when causation or termination cannot be proved.
5. **Keep egress off:** if a later requirement justifies network access, introduce a separate broker with exact hostname+port policy, positive IANA global-unicast validation, DNS/connect budgets, L7 destination binding, no ambient proxy variables, and explicit tests for rebinding, special ranges, tunnels and domain fronting.
6. **Prove each layer in order:** pure contract tests; fake-adapter ordering/retry tests; durable reservation and crash-recovery tests; real isolated Linux kernel tests; then provider-specific tests only after owner-approved zero-cost/consent gates. Physical iOS/Android workflow tests remain separate and cannot be inferred from Linux results.

### 11.6 Decision

**Retain Happy Agent Linux strict-service as the strongest inspected Linux containment reference, not as a PocketCode dependency, provider, or approved architecture.** Reuse its patterns for clean environments, private filesystems, scoped cgroups, pinned input mounts, egress brokering and reconciliation. Do not copy the service unchanged: the missing absolute deadline and CPU limit alone prevent it from satisfying PocketCode's bounded-run requirement. Fix the identified lifecycle, input and egress gaps before any future reuse assessment.

The separate Happy Agent Windows adapter remains unsuitable as-is for untrusted execution, for the previously recorded root-wide read-access and inherited-environment concerns. It is not an equivalent fallback.

**Current state:** source reviewed; upstream test sources inspected; actual upstream tests NOT RUN; PocketCode adaptation NOT IMPLEMENTED; canonical LOOP/CASE unchanged; provider/runtime NONE; budget $0; local PC state UNKNOWN.
