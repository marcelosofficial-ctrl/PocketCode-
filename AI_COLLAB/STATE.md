# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-10 by ChatGPT. Active branch HEAD at last verified checkpoint: `c23c2b671a79b978be5a602c91d270543ccedd0c`. Exact-SHA CI query for that HEAD is pending in this pass; no source/tests/device tests were run.

## Status
- Phase: Discovery/product definition. P39/exit-provenance gate CLOSED. No runtime/provider/database/transport selected.
- VERIFIED: historical Actions run 42365455316 on source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS. This is historical source/test evidence only, not current HEAD evidence.
- COMMITTED: intent/proof separation, receipt binding, grant recovery, concurrency/crash models, PWA/origin/exit-provenance research, worker-channel red-team and full-power outbox/fencing/storage/evidence research.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional outbox relay; durable crash recovery; production fencing; transport stream ownership and revocation; trusted policy authority; client receipt.
- Claude and Gemini P39 reviews are reconciled. Gemini attribution corrections: S1 is in release_grant_conformance.py, not event_journal.py; S2 names a nonexistent receipt function, but consume_event() trusts supplied digest; S3 misattributes FakeOutbox fencing, while grant-event relay lacks it; S4 is adapter/MVP scope. Gemini tests NOT RUN; Claude C1-C7 were against a byte-verified copy, not repo CI.
- Event journal (21/21) and fake coordinator (14 harness tests) are in-memory/test-double evidence only; no durable/authenticated adapter proof.
- Pyodios on owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed only "[Bridge/executePython] PythonError"; Console probe NOT RUN; bridge cause UNKNOWN.
- PWA research defines IndexedDB atomic metadata, OPFS staging/readback, local fencing and recovery. No storage engine selected; target iOS/Safari build, persist() result, quota and lifecycle behavior UNKNOWN.
- Pages enabled and workflow verified; workflow deploys `prototypes/mobile-runner`. Actual URL/custom domain/deployed SHA/headers/sibling inventory UNKNOWN. No live exploit confirmed.
- Pyodide 314.0.5 FFI exposes worker globals; same-realm guest spoofing of default Worker messages is a conditional risk. Actual installed app topology UNKNOWN. PYO-CTRL-01..15 proposed, NOT RUN.
- `FULL_POWER_GAP_RESEARCH_20261110.md` records transactional outbox, replay/idempotency, fence-at-write, Web Locks caveat, IndexedDB/OPFS two-resource recovery and typed Worker lifecycle. No code copied/dependency added.
- `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md` now turns those findings into four gated slices: event parity/canonical envelope; relay ordering/fencing/time; policy/revocation/receipt binding; typed exit/output/receipt projection. It is a plan only, NOT AUTHORIZED / NOT RUN.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in public repo. D-004 validate before stack commitment. D-005 zero spend.
- D-006 (owner, 2026-11-08): no spending of any kind. No Apple Developer Program, TestFlight or App Store for now; distribution is installable web app on GitHub Pages.
- PR #2/#3/#4 remain owner-controlled and untouched. No durable store, provider, runtime or transport selected.
- CASE-04 stays INCOMPLETE / timed_out. No precedence-only patch to scripts/report_contract.py until trusted child/wrapper/termination provenance is resolved.
- 2026-11-07 owner: old process rules may be revised; AGENTS.md carries tiered decision rights. 2026-11-08 owner: PocketCode considered for renaming to PoCo; website design must not change; nothing renamed.

## Open items
- O-1 Owner: run read-only Pyodios Console probe in `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`.
- O-2 Await any additional Claude artifact supplied by owner. Do not create a competing Claude request while strategy assignment remains OPEN. OD-01..OD-13 remain OPEN.
- O-3 Run full Python suite in a real checkout/CI and record exact-SHA results.
- O-4 Obtain actual Pages URL/custom domain/deployed SHA/live headers/sibling-origin inventory; do not infer.
- O-5 Resolve typed child exit vs wrapper exit vs termination provenance and receipt ordering.
- O-6 P40 protocol prepared; execution still gated by owner decisions and explicit authorization.
- O-7 PoCo name remains undecided; LinkedIn work waits for laptop/export.
- O-8 Apple design/context/provider-cache and website strategy work remain Claude's lane.

## Evidence limits
- Historical 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- All current P40 scenarios, durable adapter, browser/device, origin exploit, transport and full-suite checks are NOT RUN.
- Keep PocketCode and RevDev evidence strictly separate.
