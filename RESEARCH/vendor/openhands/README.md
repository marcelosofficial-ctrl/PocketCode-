# OpenHands atomic text writer reference copy

**Status:** Isolated third-party reference copy. Not imported by PocketCode, not selected as a persistence backend, and not approved for production use.

## Provenance

- Project: [OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk)
- Pinned upstream commit: `2b4d980b6a54ef6685e4337e7643c40ec24be1bb`
- Source path: `openhands-sdk/openhands/sdk/utils/files.py`
- Upstream source blob: `cdf2b7e6807d135d6386270e1988467009543701`
- Upstream repository license: MIT
- Upstream LICENSE blob: `b0bd86a6335a564bd3766666bebbf014fd6a8013`
- This folder carries the full upstream MIT license.

`atomic_write_text` writes to a randomized temporary file in the destination directory, sets mode `0600` where supported, flushes and fsyncs the file, then replaces the destination with `os.replace`. If the operation fails before replacement, it attempts to remove the temporary file and re-raises the error. `is_temp_file` recognizes the `.tmp` suffix.

## Local adaptation checks

The accompanying five-test `unittest` suite is project-authored, not copied from OpenHands. It checks UTF-8 writes/replacement, same-directory temporary files, cleanup after successful replacement, preservation of the previous target after a simulated replace failure, POSIX mode, and the temp suffix classifier.

The five tests were executed successfully on 2026-11-05 using CPython 3.13.5 on Linux: `python -m unittest discover -s /tmp/pocketcode_vendor_test/openhands -v` (5 passed, 0 failed, 0 skipped). The test source Git blob is `4876a3652517bb57d4a7ba59697f693be0cc1448`; the copied helper blob is identical to the upstream blob `cdf2b7e6807d135d6386270e1988467009543701`. This is a reference-fixture result only, not a PocketCode product test, Windows/mobile test, crash/power-loss durability test, or concurrent-writer test.

## Critical limitations

- This helper does not fsync the parent directory after `os.replace`. It therefore does not prove that the rename survives sudden power loss on every filesystem.
- It does not provide a lock, compare-and-swap, multi-writer conflict detection, transaction, append-only history, write-ahead log, or recovery journal.
- It does not canonicalize JSON or verify hashes, schemas, tenant/job/attempt identity, or producer provenance.
- It does not prevent symlink/reparse-point or path-race attacks in caller-supplied paths. Only pass trusted, root-validated internal paths.
- The `0600` mode has POSIX meaning; Windows ACL behavior must be designed and tested separately.
- It writes text, not arbitrary binary files.
- The same-directory temp file is essential to keep the rename on the same filesystem, but atomic rename behavior and durability still depend on the target OS/filesystem.

## Adoption decision

**Keep as a candidate utility, not a selected component.** If PocketCode later selects a native Python persistence component, this is a useful starting point for atomic replacement of individual small state files. It is not sufficient for the event log, report history, idempotency reservation, concurrent run state, or cross-store publication contract. Compare it with the selected platform's native persistence primitive before adopting it.
