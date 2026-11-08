# Execution boundary, durability and evidence provenance research

**Date:** 2026-11-09  
**Status:** Research and contract refinement only. No runtime, provider, database, host, transport or architecture selected. No implementation authorized. No canonical LOOP/CASE/D IDs changed.

## 1. Ranked highest-value gaps

1. **P39 independent-review and owner-decision gate:** without Gemini's source-pinned review and explicit OD-01..OD-13 decisions, implementation risks encoding unresolved security policy as code.
2. **Untrusted-code execution boundary:** the product must distinguish OS app isolation from per-execution isolation. A mobile app sandbox does not, by itself, make code run inside that app a separate hostile-code sandbox.
3. **Enforceable resource and termination evidence:** runtime fuel, memory limits, UI timeouts, cancellation requests and confirmed process termination are different things. Reports must not collapse them.
4. **Durable artifact/evidence provenance:** hashes bind bytes to a value but do not identify who produced them or prove that a run occurred. Reports need a trusted-observation boundary and immutable subject binding.
5. **Persistence crash/durability configuration:** "SQLite is ACID" is not a complete adapter acceptance statement. Durability depends on journal mode, synchronous setting, VFS/filesystem behavior and actual deployment topology.

## 2. Execution trust boundary: app sandbox is not guest sandbox

### Verified primary-source findings

- **Android app sandbox:** each app receives a distinct Linux UID and process isolation from other apps. Android's security checklist warns against dynamically loading code from outside the APK because it runs with the same permissions as the APK. An app that loads user code into its own process/runtime must not describe the Android application sandbox as a separate sandbox for that program. Sources opened 2026-11-09: https://developer.android.com/guide/components/fundamentals and https://developer.android.com/privacy-and-security/security-tips
- **WebAssembly core security model:** WebAssembly has no ambient access to the host environment. I/O, resources and OS calls require functions imported from the embedder. The embedder is responsible for controlling those capabilities. Source: https://www.w3.org/TR/wasm-core/
- **WebAssembly security overview:** modules execute in a sandbox, but their effective policy also depends on the embedding environment. Source opened 2026-11-09: https://webassembly.org/docs/security/
- **Pyodide integration:** Pyodide is designed to run in a browser or backend JavaScript environment, and its documentation describes the JavaScript API and Python/JavaScript proxy interface. The embedding code therefore forms part of the capability boundary. Sources: https://pyodide.org/en/stable/usage/ and https://pyodide.org/en/stable/usage/api/js-api.html
- **Wasmtime filesystem capabilities:** WASI filesystem access uses capability-based access to only the directories and files granted to the guest. Wasmtime also warns that untrusted terminal output can contain control sequences with dangerous side effects and filters terminal output. Source opened 2026-11-09: https://docs.wasmtime.dev/security.html

### Correct interpretation for PocketCode

The phrase "WASM sandbox" is too broad to support a public hostile-code guarantee. The enforceable boundary is the combination of:
1. WebAssembly engine memory/control-flow isolation;
2. exact imports and host functions made available to the guest;
3. filesystem/network capabilities granted to the guest;
4. resource and interruption controls actually configured;
5. embedding process OS permissions; and
6. any stronger external worker/VM/container boundary around that process.

For Pyodide embedded in an app or browser, do not expose host objects, application credentials, project-management functions, native bridges, unrestricted fetch/network, or broad filesystem APIs to untrusted code. A worker thread can protect UI responsiveness and simplify termination, but moving work to a worker does not itself prove OS-level hostile-code isolation. A web worker remains subject to the browser's origin and embedding security model.

**Product distinction:**
- **Trusted/local task mode:** standard-library/lightweight user code with explicit input files, no secrets, no sensitive app bridge, and no claim of hostile-code containment or hard OS quotas.
- **Untrusted/public code mode:** unavailable until a separately isolated, disposable execution boundary is reviewed and tested with server/OS-level CPU, memory, process, disk, wall-time, output, egress and cleanup enforcement.
- **Unknown boundary mode:** if the app cannot establish which capabilities are exposed or whether termination is enforceable, reject the run or label the missing control UNKNOWN. Do not silently downgrade into a "secure sandbox" claim.

This preserves the existing SECURITY.md and BOOT.md constraints. It does not select remote execution or any mobile runtime.

## 3. Wasmtime: useful guest controls, not a complete deployment boundary

### Verified primary-source findings

- **Wasmtime resource limits:** StoreLimitsBuilder can cap guest linear-memory growth, table elements, instances, tables and memories. Several count defaults are high (10,000), and linear memory/table growth is unlimited unless configured. Source: https://docs.wasmtime.dev/api/wasmtime/struct.StoreLimitsBuilder.html
- **CPU interruption:** Wasmtime supports deterministic fuel accounting and epoch-based interruption. Fuel is deterministic but more expensive; epochs are lower overhead and nondeterministic. Epoch deadlines must be configured before execution. Bulk memory operations can run between epoch checks, so strict time limits also require a bounded guest heap. Sources: https://docs.wasmtime.dev/api/wasmtime/struct.Config.html and https://docs.wasmtime.dev/examples/interrupting-wasm.html
- **ResourceLimiter limitation:** Wasmtime explicitly says its resource limiter does not account for 100% of memory used by the Store; host-side data structures and embedder allocations are outside that guest memory limit. CPU limits require fuel/epochs separately. Source: https://docs.wasmtime.dev/api/wasmtime/trait.ResourceLimiter.html
- **Current release:** Wasmtime 50.0.1 was released 2026-10-29. Its release notes include a WASI sockets authorization fix: UDP connect previously accepted an address allowed for receive but not send. It also includes memory/type safety and HTTP content-length fixes. Source: https://github.com/bytecodealliance/wasmtime/releases
- **Licence:** Wasmtime repository and Python binding metadata identify Apache-2.0 / Apache-2.0 WITH LLVM-exception. Verify the exact bundled component and dependency notices before redistribution. Sources: https://github.com/bytecodealliance/wasmtime and https://github.com/bytecodealliance/wasmtime-py/blob/main/pyproject.toml

### Adaptation

Wasmtime demonstrates that a runtime can provide explicit guest memory limits, fuel/epoch interruption and capability-scoped filesystem access. It does not supply a complete process memory quota, host-call quota, network policy, filesystem lifecycle, or production VM boundary automatically.

A candidate Wasmtime adapter must configure, record and test:
- fuel or epoch interruption, with a tested deadline and an outer wall-clock watchdog;
- guest memory/table/instance limits, plus external process/container/VM memory limits for host allocations;
- explicit filesystem preopens only, with no ambient host path;
- no network imports by default; if network is enabled, host-side destination/port/IP policy and DNS rebinding defenses;
- bounded stdin/stdout/stderr and safe rendering of terminal control sequences;
- no credentials or control-plane secrets in guest memory/environment;
- explicit worker termination acknowledgement and disposable workspace cleanup;
- exact Wasmtime version, enabled proposals, WASI version, host imports, limits and platform build in the evidence record.

The official release notes show why version pinning matters: a recent security fix changed enforcement of UDP send permission. Do not pin to a release solely because it is latest; track security advisories and retest upgrades. No Wasmtime dependency or runtime selection is recommended here.

## 4. Pyodide version and suitability review

### Verified facts

- Pyodide 314.0.7 is the latest stable release visible in the official release page on 2026-11-09; its changelog dates it 2026-09-14. Version 314.0.5 is dated 2026-08-15. Sources: https://github.com/pyodide/pyodide/releases and https://pyodide.org/en/stable/project/changelog.html
- The owner's previously reported Pyodios device baseline is Pyodide 314.0.5, Python 3.14.2, app 1.1.0 Build 7. This is owner-reported device evidence, not independently inspected in this pass.
- Pyodide's upstream licence is Mozilla Public License 2.0, not MIT/BSD. Source: https://github.com/pyodide/pyodide/blob/main/LICENSE
- Pyodide documents browser and backend JavaScript environments and the Pyodide JS API. Browser use is not synonymous with a dedicated hostile-code worker. Sources: https://pyodide.org/en/stable/usage/ and https://pyodide.org/en/stable/usage/api/js-api.html

### Decision impact

The device baseline is two patch releases behind upstream Pyodide 314.0.7. That is a version observation, not evidence of a defect or proof that Pyodios can safely upgrade independently. Do not ask the owner to replace a bundled runtime manually. At the next owner-controlled device check, record the vendor app/build and bundled Pyodide version, then compare the vendor's supported update path.

For PocketCode, Pyodide remains a candidate for trusted/light local tasks only unless its embedding, exposed JS capabilities, interruption behavior, resource ceilings and persistence are independently verified. The existing BOOT rule that stock Pyodide/WASM is not a hostile-code sandbox remains correct.

## 5. Persistence: SQLite candidate evidence, without selecting it

### Verified primary-source findings

- SQLite states that transactions are serializable by serializing writes; only one writer can write at a time, while separate connections/processes see committed transactions. Sources opened 2026-11-09: https://sqlite.org/isolation.html and https://www.sqlite.org/transactional.html
- SQLite WAL improves reader/writer concurrency, but all processes using the WAL database must be on the same host; WAL does not work over a network filesystem. Source: https://www.sqlite.org/wal.html
- In WAL mode, synchronous=NORMAL preserves consistency but a committed transaction can be lost after power failure or OS crash. synchronous=FULL adds a WAL sync at each commit and is the documented durable choice for WAL. In rollback-journal mode, EXTRA may be needed for full durability around power loss. Source opened 2026-11-09: https://www.sqlite.org/pragma.html
- SQLite's crash-testing documentation describes a VFS that simulates partial writes, garbage data and out-of-order writes, then checks that recovery yields either the complete transaction or none. It also documents assumptions about OS flush, locking and filesystem behavior. Source: https://www.sqlite.org/atomiccommit.html
- SQLite core is dedicated to the public domain. Source: https://www.sqlite.org/copyright.html

### Adapter acceptance consequence

Do not write "SQLite is durable" as a generic statement. If SQLite is ever evaluated, adapter evidence must include:
- exact SQLite library version and compile options;
- journal_mode, synchronous, fullfsync, VFS and busy/timeout configuration;
- filesystem/container path and whether any network/shared filesystem is involved;
- independent connections and processes, including process-death recovery;
- WAL checkpoint, backup/restore and migration behavior;
- crash/power-loss simulation appropriate to the actual platform;
- verification that grant + event + outbox + receipt-head mutations are in one transaction;
- a measured test proving that a committed transaction survives the target device's stated failure model.

WAL + synchronous=FULL is a documented candidate configuration for local durability, not a PocketCode decision or universal guarantee. Filesystem, VFS, platform and backup behavior still require tests. SQLite's single-writer serialization may fit a local store, but does not by itself solve distributed/cloud multi-host concurrency.

## 6. Evidence provenance: adapt in-toto structure, not trust assumptions

### Verified primary-source findings

- **in-toto Attestation Framework v1.2** separates predicate, statement, envelope and bundle. The statement binds a claim to one or more artifact subjects; the envelope handles authentication and serialization. The framework repository describes itself as under development. Sources: https://github.com/in-toto/attestation and https://github.com/in-toto/attestation/blob/main/spec/README.md
- The in-toto attestation repository's LICENSE is Apache-2.0. Source: https://github.com/in-toto/attestation/blob/main/LICENSE
- **SLSA provenance** is a predicate describing how a build platform produced artifact subjects. External parameters are untrusted inputs and must be included and verified downstream. It is a build-provenance standard, not proof that a PocketCode user program ran correctly. Source: https://slsa.dev/spec/v1.1/provenance
- **Sigstore bundles** package signature content with verification material, including certificates, timestamps and optional transparency-log entries. A bundle signature is verified against an expected identity and artifact digest. A signature authenticates a claim by a signer; it does not make a false claim true. Sources: https://docs.sigstore.dev/about/bundle/ and https://docs.sigstore.dev/about/security/
- Sigstore bundle documentation identifies format version 0.3.2 and last updated 2025-01-14. in-toto Attestation v1.2 is the latest tagged release shown in the official repository on 2026-11-09. No exact current Cosign release was verified in this pass.

### PocketCode evidence-envelope proposal

Keep the existing identity chain unchanged:

CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt

Add a versioned, adapter-neutral **EvidenceEnvelope** projection around the immutable receipt. It is a design proposal, not a frozen public schema.

| Field | Meaning | Trust rule |
|---|---|---|
| envelope_version | Version of the envelope contract | Required literal version |
| command_id | User command identity | Coordinator-issued |
| dispatch_attempt_id | One actual dispatch attempt | Coordinator-issued; transport retry retains it |
| execution_id | Identity from execution boundary | UNKNOWN if boundary did not issue it |
| observation_range | First/last accepted ObservationSequence | Coordinator-assigned; no caller ordering authority |
| runtime_identity | Runtime name/version/build and config digest | Adapter-observed, not client supplied |
| input_manifest_digest | Digest of exact immutable input manifest | Coordinator recomputes over canonical bytes |
| output_manifest_digest | Digest of exact output manifest and artifact bytes | Producer digest is a claim until independently read back |
| lifecycle_observations | Raw start/exit/timeout/cancel/termination/cleanup facts | Append-only; provenance and attempt binding required |
| verdict_projection | PASS/FAIL/INCOMPLETE/UNKNOWN plus reason codes | Resolved by trusted coordinator from accepted evidence |
| artifact_disposition | staged/quarantined/released/deleted/unknown | Separate from execution verdict |
| producer_identity | Authenticated execution authority/adapter identity | Bound to credential/key and scope |
| signature_or_attestation_ref | Optional verifiable signature/attestation bundle | Optional; absence must not be presented as signed provenance |

Canonicalization rules:
1. Hash exact bytes, not a parsed/re-serialized object unless a specified canonical JSON format is used.
2. Bind every artifact to ArtifactId, immutable object version, byte length, digest algorithm and digest.
3. Bind every observation to CommandId, DispatchAttemptId and ExecutionId where available; stale or cross-attempt events are quarantined.
4. Preserve the raw producer claim alongside the coordinator's accepted observation. Never overwrite one with the other.
5. A client-provided digest is a claim. A coordinator read-back digest verifies stored bytes. Neither proves a remote client received them.
6. A signature proves that a signer signed the bound claim, subject to key/identity validation. It does not prove the execution was isolated, policy-compliant or successful unless the signer is a trusted execution authority and its attested process is itself audited.
7. Keep execution verdict and artifact release disposition as separate axes.
8. If provenance is missing, mismatched or unverifiable, retain UNKNOWN/INCOMPLETE and prevent release where policy requires proof.

### Reuse decision

Use in-toto's subject/statement/envelope separation as a conceptual template. Do not add in-toto, Sigstore, Cosign or SLSA as required MVP dependencies. A public transparency log or signing service would add operational, identity and potentially cost dependencies. First define the trusted producer and the claim being authenticated. No code copied.

## 7. Proposed acceptance tests (not canonical LOOP/CASE/D IDs)

These are proposed adapter/security tests only. They do not authorize implementation and must not be merged into canonical suites without owner/reviewer approval.

| Proposed test | Setup | Required result |
|---|---|---|
| P39-BOUNDARY-01 | Guest attempts to read host app environment, credentials and arbitrary paths | No ambient access; only explicitly preopened capabilities work |
| P39-BOUNDARY-02 | Guest invokes every host import/bridge entry point | Only documented allowlisted operations are reachable; all calls are scoped to current attempt |
| P39-BOUNDARY-03 | Guest attempts DNS, loopback, private IP, cloud metadata and arbitrary egress | Denied by default; allowlisted network path enforces destination and port policy |
| P39-BOUNDARY-04 | Guest emits ANSI/OSC/control sequences and bidi/confusable output | Rendered inertly; no terminal action or misleading control-plane UI |
| P39-RESOURCE-01 | Infinite loop, recursive stack growth, linear-memory growth and table growth | Each applicable limit is independently enforced; exhaustion produces non-success with raw cause |
| P39-RESOURCE-02 | Guest performs large memory.copy under epoch interruption | Maximum uninterruptible operation remains bounded by configured guest heap; wall-clock watchdog independently tested |
| P39-RESOURCE-03 | Guest floods stdout/stderr and creates many files | Output, file count, per-file size, total disk and report limits enforced without unbounded host memory |
| P39-TERM-01 | UI requests cancellation but worker continues | State remains cancellation-requested/termination-unknown until same-attempt worker/transport termination evidence arrives |
| P39-TERM-02 | Worker is killed after writing staged artifact but before manifest commit | Artifact remains quarantined/unaddressable; recovery does not publish partial bytes |
| P39-DB-01 | Two processes concurrently create first receipt-head anchor | Unique key yields one root; loser reloads winner; no fork |
| P39-DB-02 | Inject crash at every transaction write and immediately before/after commit | Grant, event, outbox and head are all present or all absent; ambiguous response recovers by same idempotency key |
| P39-DB-03 | Commit WAL transaction with NORMAL then simulate power-loss recovery | Demonstrate durability matches selected setting; test FULL separately |
| P39-EVIDENCE-01 | Mutate artifact bytes after manifest creation | Read-back digest mismatch quarantines artifact and prevents release |
| P39-EVIDENCE-02 | Replay event from another attempt or reuse event ID with changed payload | Cross-attempt event rejected; same identity/different bytes is a conflict |
| P39-EVIDENCE-03 | Submit caller-provided PASS verdict and digest without trusted producer evidence | Caller claim remains untrusted; coordinator does not promote it to PASS |
| P39-EVIDENCE-04 | Verify signed envelope with wrong signer identity or wrong subject digest | Verification fails; no release |
| P39-EVIDENCE-05 | Correct signature over a false or incomplete claim | Signature is reported valid, claim remains insufficient for PASS; trust policy requires independently supported execution evidence |

For every adapter test record exact source/build SHA, engine/runtime version, OS/device, configuration, process count, test schedule, crash point, raw logs and evidence digests. Sequential fakes cannot close process, storage, OS or transport claims.

## 8. Red-team corrections to prior work

1. **Previous STATE HEAD was wrong:** it stated e643d59 despite the live branch already being 42a9f48. This pass refreshes and records the exact live HEAD after committing.
2. **The previous checkpoint described the pre-checkpoint commit as the current state:** 821522a was the parent immediately before the checkpoint commit, not the current branch HEAD. New checkpoint records the actual final commit and five commits.
3. **"SQLite ACID" is not enough for durability:** SQLite's official docs explicitly distinguish WAL NORMAL from FULL and rollback-journal EXTRA. The earlier generic adapter specification lacked this candidate-specific configuration caveat. This addendum adds it without selecting SQLite.
4. **WASM memory limit was easy to overstate:** Wasmtime's ResourceLimiter does not cap all host/Store allocations. A guest memory cap is not a whole-process memory cap. The proposed test plan now requires external process limits as well.
5. **Runtime interruption was easy to overstate:** epoch interruption is periodic, not deterministic, and bulk memory operations check only at operation boundaries. Bound the guest heap and keep an outer watchdog; do not claim an exact wall-time kill from fuel/epochs alone.
6. **Evidence signature could be mistaken for truth:** in-toto/Sigstore authenticate a subject-bound claim. They do not prove the execution boundary behaved honestly. Require a trusted producer and independently verified artifact bytes.
7. **Pyodide version baseline was stale relative to upstream:** the owner-reported device runtime 314.0.5 predates upstream stable 314.0.7 (2026-09-14). This is a compatibility/update observation only, not a device defect or permission to replace the vendor-bundled runtime.

## 9. Source, maintenance and licence register

| Project/source | Verified maintenance/version | Licence checked | PocketCode use |
|---|---|---|---|
| Pyodide | 314.0.7 latest stable visible 2026-11-09; released 2026-09-14 | MPL-2.0 | Runtime reference; trusted/light only pending embedding audit |
| Wasmtime | 50.0.1 released 2026-10-29; 51.0.0-rc.1 is prerelease | Apache-2.0 / Apache-2.0 WITH LLVM-exception metadata | Guest resource/capability reference; no dependency selected |
| SQLite | Official docs opened 2026-11-09; current docs describe WAL and sync semantics | Public domain for core library | Local persistence candidate only; not selected |
| in-toto Attestation | v1.2 latest tagged release visible 2026-11-09 | Apache-2.0 | Subject-bound evidence format reference |
| Sigstore/Cosign | Bundle format 0.3.2 docs last updated 2025-01-14; exact current Cosign release not verified | Cosign Apache-2.0 | Optional signature verification reference; not MVP dependency |
| Android platform | Current official security checklist and app fundamentals opened 2026-11-09 | Platform documentation; no code copied | App sandbox and dynamic-code warning |
| WebAssembly | Current W3C core specification search result and official security page opened 2026-11-09 | Standards/documentation; no code copied | Capability import boundary |
| Apple iOS app security | Official source search result located; full page returned HTTP 429 on open | Not assessed | No detailed iOS sandbox claim relies on this page in this addendum |

## 10. Gate and status

- P39/P40 implementation gate remains **CLOSED**. Gemini review and explicit OD-01..OD-13 owner decisions remain pending.
- This document makes no owner decision and does not authorize source/tests.
- No runtime, provider, database, hosting, transport or app architecture is selected.
- No canonical LOOP/CASE/D identifiers changed.
- No code copied, no dependency added, no test executed.
- **VERIFIED:** source documents opened as listed above. **INFERRED:** PocketCode recommendations and acceptance proposals. **UNKNOWN / NOT RUN:** actual mobile embedder capabilities, hostile-code containment, real adapter concurrency, process-level quotas, device interruption, crash/power-loss recovery and production provenance.
