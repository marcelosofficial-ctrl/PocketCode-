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
- `memory.events` is hierarchical by default. Use `memory.events.local` when attributing an event to the exact target cgroup. Capture before/after counters and the cgroup identity; a pre-existing or ancestor counter is not per-attempt proof.
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

### 4.5 Cloudflare Sandboxes

The current Cloudflare sandbox docs describe inactivity-driven instance lifetime, explicit `destroy()`, and the fact that an inactivity timeout sends SIGTERM before the instance stops. The docs caution that `destroy()` stops the instance immediately without time for process cleanup, so state must be saved beforehand. A Durable Object restart also does not automatically preserve the inactivity timeout; it must be re-established.

Implications:
- A graceful application-level cleanup hook cannot be assumed to run on explicit destroy.
- State persistence and teardown evidence need to be designed separately.
- An inactivity timeout is not a substitute for a durable external watchdog/reconciler.
- The sandbox docs state the feature is available on a Workers Paid plan; this is not a zero-cost assumption.

Sources:
- https://developers.cloudflare.com/sandbox/concepts/lifetime/
- https://developers.cloudflare.com/sandbox/sdk/api/lifecycle/
- https://developers.cloudflare.com/sandbox/

### 4.6 E2B

E2B's security page describes each sandbox as running in its own Firecracker microVM with its own kernel, and says sandboxes are destroyed on timeout or shutdown. This is useful vendor architecture information, but it is still a provider statement. The page alone does not supply PocketCode-specific evidence for exact resource limits, supervisor containment, process-tree emptiness, delete acknowledgement semantics, attached resource cleanup, or durable orphan reconciliation.

Source:
- https://e2b.dev/security

## 5. Revised falsification matrix for PC-EXT-02 and PC-EXT-04

These are subcases under the existing research plan, not new canonical acceptance IDs.

| Subcase | Setup / attack | Required observation | Failure condition |
|---|---|---|---|
| RES-01 limit configuration binding | Requested limits differ from defaults; inspect the exact sandbox/attempt's effective configuration | Provider/host authoritative effective limits, identity-bound | Only request payload or adapter echo is available |
| RES-02 memory boundary | Bounded allocator crosses memory ceiling in a dedicated test sandbox | Limit evidence; target-local before/after counters where available; exact child outcome | Supervisor or unrelated workload is killed/degraded, or evidence is global/unattributed |
| RES-03 swap accounting | Exercise memory pressure with declared swap policy | Effective swap cap and relevant counters/state | Swap remains unbounded contrary to declared policy |
| RES-04 CPU bandwidth vs deadline | CPU-bound workload exceeds bandwidth request, then separate wall-clock deadline | Throttling/accounting separated from deadline event and termination | CPU throttling is misreported as timeout, or infinite loop survives hard deadline |
| RES-05 process/task ceiling | Bounded fork/thread pressure | Effective task limit, local event evidence, no host-wide task exhaustion | Host worker or sibling task capacity is exhausted |
| RES-06 disk capacity vs I/O rate | Write many files and one oversized file; separately saturate I/O | Filesystem/volume capacity evidence distinct from I/O throughput and per-file cap | `io.max` or `RLIMIT_FSIZE` is claimed as total disk quota |
| RES-07 output cap | Emit bounded large stdout/stderr with process status independently observed | Runtime termination vs collector loss vs display truncation | One boolean hides the enforcement layer or fabricates child termination |
| RES-08 supervisor/sibling containment | Workload hits memory/PID/CPU limits while worker heartbeat and independent sibling canary run | Worker remains responsive; sibling remains isolated; exact workload failure is attributed | Shared kill domain or collateral host impact |
| RES-09 descendant termination | Workload forks descendants and ignores graceful signal | All attempt descendants terminated; exact process subtree empty | Parent exits but descendant remains, or cleanup is inferred from parent PID alone |
| TDN-01 delete accepted but pending | Provider accepts deletion asynchronously | State remains DELETE_ACCEPTED/DESTROYING until terminal observation | API 2xx/202 response is mapped directly to CLEANUP_CONFIRMED |
| TDN-02 lost delete acknowledgement | Provider may have accepted delete but coordinator times out | Lookup same stable resource ID; no duplicate resource created | Retry creates a new sandbox or closes cleanup without evidence |
| TDN-03 provider lookup unavailable | Delete request accepted/ambiguous; subsequent reads fail | CLEANUP_UNKNOWN / ORPHANED_TEARDOWN_REQUIRED and durable retry schedule | Missing state is treated as deletion |
| TDN-04 terminal deletion | Provider read reaches documented destroyed/deleted terminal state | Immutable event binds tenant/job/attempt/resource/version and terminal state | Search miss, local DB close, or stale event substitutes for authoritative state |
| TDN-05 attached resource independence | Sandbox has attached volume/snapshot/artifact storage | Each separately billable/persistent resource has its own release/delete state | Sandbox destruction is assumed to delete independent resources |
| TDN-06 late cleanup event | Attempt N is deleted after attempt N+1 starts | Event remains bound to N and cannot mutate N+1 | Stale cleanup event closes the wrong attempt |
| TDN-07 reconciliation crash | Coordinator crashes after provider accepted delete but before persisting response | Restart resumes lookup/reconciliation for same resource identity | New resource or untracked orphan is created |
| TDN-08 cleanup vs billing lag | Provider terminal state observed; billing data remains pending | Resource termination and cost reconciliation represented separately | Pending invoice appears as zero cost or active billing is mistaken for live process evidence |

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
