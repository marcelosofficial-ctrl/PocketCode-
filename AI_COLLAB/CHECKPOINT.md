# CHECKPOINT — 2026-11-10

**Unit:** Full-power gap research pass. Starting HEAD: `c6c159189cc6f899744a0b3ba3659c485281461d`. Pre-checkpoint work HEAD: `f2cd5f0bc0181fd378eddbdf575f0599802e5769`.

## Fresh resume and branch evidence
Read BOOT, STATE, NEXT_TASK, CHECKPOINT and INBOX_chatgpt in the required order. Listed the latest five branch commits. Branch had advanced since prior chat: Claude committed `APPLE_DESIGN_ENGINEERING_SPEC_20261108.md` at `c6c1591`; Claude strategy assignment remains OPEN. The design spec is indexed and treated as Claude-owned. No duplicate Apple design or context/provider-cache research was done.

## Deliverables
- Created and indexed `AI_COLLAB/FULL_POWER_GAP_RESEARCH_20261110.md` (2,485 words, 140 lines): transactional outbox/replay, fence-at-write/revocation, Web Locks, IndexedDB/OPFS recovery, Worker termination/result provenance, competitor reuse assessment and concrete acceptance mapping to existing IDs.
- Corrected INDEX omissions: added Claude's Apple design spec and this research document; compressed INDEX to 1,126 words, under its 1,200-word target.
- Updated STATE (870 words) and NEXT_TASK (398 words) with new evidence and next steps.
- Red-team corrections recorded: Web Locks `steal` does not stop old callback code; IndexedDB completion/persist is not universal power-loss backup; OPFS and IndexedDB do not share one atomic transaction; prototype CI trigger/checker limitations are verified.

## Evidence and limits
- **VERIFIED:** AWS outbox guidance; Temporal replay/retry semantics; Redis fencing/clock caveat; PostgreSQL row locks; W3C Web Locks WD dated 2026-11-09; MDN IndexedDB, persist and OPFS; WHATWG Worker termination; OpenAI Agents SDK lifecycle; Cline checkpoints/licence, Aider repo-map options, Sentry repo licence.
- **VERIFIED:** `.github/workflows/pocketcode-python-tests.yml` triggers on `scripts/**` and workflow changes, or manual dispatch. `scripts/check_mobile_prototype.py` is a static source checker and does not execute JavaScript or Python.
- **UNKNOWN:** actual Pages URL/deployment headers, installed Pyodios worker topology, target-device storage guarantees and production adapter behavior.
- **NOT RUN:** all fault injection, device tests, browser exploit tests and current full Python suite. Exact-SHA CI for latest checkpoint must be read from GitHub after this commit.
- P39/P40 CLOSED; OD-01..OD-13 OPEN; CASE-04 remains INCOMPLETE / timed_out. No source/tests, canonical IDs, PRs, runtime/provider/database/transport selection, spend, deployment or RevDev work.

## Next
1. Obtain owner OD-01..OD-13 decisions or explicit deferrals.
2. Complete Pages/ORIGIN evidence only with actual URL/settings; do not guess.
3. Keep O-5/relay/fencing/storage acceptance design separate from implementation until gate closure.
