# P40 bounded model-run authorization request

**Prepared:** 2026-11-11  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Target commit:** `319cffef121e327331aeaff59522ae279b112ecc`  
**Status:** PREPARED / NOT AUTHORIZED / NOT RUN  
**Decision basis:** OD-01..OD-13 adopted in `P39_OWNER_DELEGATED_DECISIONS_20261111.md`. This request does not itself open the technical gate.

## 1. Exact scope requested

Authorize one read-only test run against the exact target commit above:
- run existing model test files for P40 lanes 1, 2, 3, 5 and 6;
- run the full `scripts` unittest discovery suite once;
- print Python and SQLite versions in the run log;
- make no source, test, workflow, dependency, schema or configuration changes;
- do not run browser/device, provider, transport, database-adapter, Pages or deployment tests;
- do not spend money, add secrets, call providers, or modify PRs.

Lane 4 (grant-event relay fencing) is explicitly BLOCKED / NOT TESTABLE in the current model. Do not substitute FakeOutbox effect-dispatch tests as relay evidence.

## 2. Source and test pins

All ten current branch blob SHAs were re-fetched after docs-only decision commits and match the prior P40 audit:

| Lane | Source blob SHA | Test blob SHA | Command |
|---|---|---|---|
| 1. Release-grant aggregate | `f9107fe46d60bbb5cd7115daf2513cd751221986` | `e3bbe94838807a1f9214042af262a2497c057fd7` | `python -m unittest discover -s scripts -p "test_release_grant_conformance.py" -v` |
| 2. Grant-event consumer | same as lane 1 | same as lane 1 | Covered by lane 1 command; report consumer methods separately |
| 3. Effect-dispatch FakeOutbox | `813957e5061d40cba2ebb5e2936edcbac645820b` | `67951a77f87e9523c9080970068fd158680f23a9` | `python -m unittest discover -s scripts -p "test_fake_outbox.py" -v` |
| 4. Grant-event relay | `f9107fe46d60bbb5cd7115daf2513cd751221986` | No relay-specific test coverage | BLOCKED / NOT TESTABLE; no command |
| 5. EventJournal | `371a175739b9cb65cd4d59bb4cd5b3c1c4953564` | `333cf5ec856d4244c3f84da9e82bb2fa126607b5` | `python -m unittest discover -s scripts -p "test_event_journal.py" -v` |
| 6a. Result receipts | `0d1588f8590b57e0bf7447c7d5c519186ff0f39d` | `d1f3546d15a6f5473b9a8eda43ea7a1fee0bca7c` | `python -m unittest discover -s scripts -p "test_result_receipts.py" -v` |
| 6b. Execution projection | `f32237c8c5ee5d62b0416b3dd867515ce567c21b` | `cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1` | `python -m unittest discover -s scripts -p "test_execution_projection.py" -v` |

After the five lane commands, run:
`python --version`
`python -c "import sqlite3; print(sqlite3.sqlite_version)"`
`python -m unittest discover -s scripts -p "test_*.py" -v`

Run environment: the existing CI workflow specifies `ubuntu-latest` and Python `3.12`. Record the actual resolved OS/Python/SQLite versions, command exit codes and complete test totals. Do not claim a pass from a green summary without the exact run/SHA/job evidence.

## 3. Known expected limits and reporting

- Lane 1 has known static gaps: equal progress increments aggregate_version without a matching event/outbox; aggregate-version/event parity is not established. Existing tests do not directly cover both invariants. Record STATIC GAP / NOT TESTED unless a pre-existing assertion actually exercises it. Do not edit tests in this run.
- Lane 2 existing duplicate/gap tests do not prove first-delivery authentication, canonical digest recomputation or tenant/grant/source binding. Those remain BLOCKED on a canonical envelope and trusted ingress contract.
- Lane 3 proves only FakeOutbox effect-dispatch semantics, not grant-event relay fencing.
- Lane 4 remains BLOCKED / NOT TESTABLE.
- Lane 5 proves only in-memory journal behavior; not cryptographic authentication, durable fences or atomic persistence.
- Lane 6 proves only in-memory receipt and pure projection behavior; not browser storage, worker lifecycle, termination acknowledgement or client receipt.
- A model test PASS does not pass canonical LOOP/CASE acceptance or prove production adapter behavior. CASE-04 stays INCOMPLETE / timed_out.
- Record all results as PASS / FAIL / NOT RUN / BLOCKED with exact method and source/test pins. No missing lane can be silently omitted.

## 4. Stop conditions

Stop without running if target branch HEAD differs from `319cffef121e327331aeaff59522ae279b112ecc`, any of the ten blob pins differs, the workflow would trigger a deployment or billable workload, or the test command requires code/config changes. Do not rebase, force-push, merge, modify PR #2/#3/#4, or use RevDev evidence.

## 5. Authorization state

**NOT AUTHORIZED.** The owner delegated OD policy decisions but has not yet explicitly authorized this bounded P40 execution. Replying with approval of this exact request (or a narrower lane subset) will open only this read-only test run. It will not authorize implementation, adapter selection, provider calls, device tests, deployment or spending.
