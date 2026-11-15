STATUS: DONE

## Decision and recovery
- Owner delegated resolution of the read-budget conflict. For this pass, prioritized the three coupled implementation/test files. Reused BOOT/STATE/NEXT_TASK content read in the immediately preceding turn; they were not reread because the strict cap is 3 files. CHECKPOINT.md was updated via Git tree/blob; INBOX_chatgpt.md was not read.
- IN PROGRESS marker: f3ef4c1ff7a89b17b24d98384a94aa6b7d017c16.
- Latest five at startup: f3ef4c1ff7a89b17b24d98384a94aa6b7d017c16 (IN PROGRESS), bc08615 (DONE), 7e3f680 (IN PROGRESS), a03b87d (DONE), 711811f (IN PROGRESS). All checkpoint-only.
- Read bounded sections of scripts/event_journal.py, scripts/result_receipts.py and scripts/test_result_receipts.py. No file was opened whole beyond 1,500 words.

## VERIFIED source findings
- EventJournal.receipt_snapshot(effect_id, attempt_id) builds global observation/accepted high-waters and scoped conflict sequences from mutable in-memory lists; no lock/transaction is present. It is not a durable or concurrency-safe provenance boundary.
- ResultReceiptStore.create_receipt currently accepts detached journal_snapshot plus legacy scalar keyword arguments (rejecting scalar claims only when a snapshot is present); it validates snapshot seal/scope, then fingerprints the detached fields. A caller can import the module sentinel and can reuse a stale snapshot after a late conflict.
- Tests currently pass detached snapshots through journal_snapshot; cover scope mismatch, ordinary unsealed constructor rejection, immutable snapshot capture and late successor receipts. They do not test stale-snapshot use at receipt creation or live-journal binding.
- Best bounded API migration: accept journal: Optional[EventJournal]; reject non-EventJournal values; derive journal.receipt_snapshot(effect_id, attempt_id) inside create_receipt; do not expose snapshot or caller-supplied watermark/ref inputs as provenance. Update tests to pass live journals, assert a late conflict is included in the receipt, preserve global watermarks and exact effect/attempt scope. Document EventJournal as single-threaded/not thread-safe unless lock semantics are deliberately added. Keep detached snapshot construction private/non-public only if compatibility requires it; never claim authenticity.
- Two implementation/test files would need coordinated edits; event_journal.py needs only a documented concurrency statement unless synchronization is separately chosen.

## Why no source commit
- The available GitHub write surface replaces a file with its complete content; no patch/apply operation is exposed. The coupled source and test files are large (38 KB and 45 KB). Reconstructing/replacing them would violate the instruction not to rewrite a large file or open over 1,500 words whole. No safe bounded patch mechanism was available.
- No source/test/workflow/PR/provider/adapter/runtime/device/infrastructure/canonical acceptance changes were made. Tests NOT RUN; local network limitation and pinned historical CI evidence remain as previously recorded.

## Next pass
- Use an authorized patch-capable GitHub editing route or PC/local patch workflow to make the two-file API/test migration without rewriting whole files. Then run the focused test file and full scripts suite against the exact commit, recording actual output. Do not change P39 adapter gate, workflow, report format, CASE-04, or infrastructure choices.
- P39 adapter/conformance gate CLOSED; CASE-04 INCOMPLETE / timed_out; $0/provider-neutral constraints unchanged.
