# PocketCode — Complete Continuation Handoff (2026-10-27)

**Read this first.** Continue from repository evidence, not from chat memory. This is a cautious handoff, not a claim that tests passed or that the project is production-ready.

## 0. Immediate instructions for the next chat

1. Read this handoff and [MASTER_WORKFLOW_EFFICIENCY_RULES_20261027.md](MASTER_WORKFLOW_EFFICIENCY_RULES_20261027.md).
2. Inspect the current PR, branch head, repository instructions, `PROJECT_STATUS.md`, master plan, product/architecture/security/roadmap/decision docs, and the latest checkpoint. Verify the branch head before editing because this handoff records the last observed state, not a permanent guarantee.
3. The owner pasted a detailed 18-section “POCKETCODE MASTER WORKFLOW” in the prior chat. Its principles have been consolidated into the linked GitHub workflow file. **If you cannot access/read that file or are unsure the consolidation captured the owner's intent, ask the owner to paste that workflow again before proceeding with substantial work.** Do not ask them to repeat it if the GitHub file is accessible and sufficient.
4. Continue the current high-value task: static lifecycle contract audit and testability. Do not jump to provider selection, live execution, UI expansion, or broad research without a reason.
5. No user action is needed unless a genuine decision/blocker requires it. Owner is primarily on phone and may lack PC access for months.

## 1. Product and long-term goal

PocketCode is a phone-first, AI-assisted coding project. The product hypothesis: users bring AI-generated or personally written code plus relevant small inputs from any preferred AI, choose a supported runtime, run it in an appropriate isolated environment, inspect truthful execution evidence, and paste a bounded/redacted report back into their preferred AI to iterate. Core loop: workspace/project → edit code and inputs → choose runtime → submit run → see status/stdout/stderr/timing/exit/files → distinguish program failure from infrastructure failure → share useful report → iterate/save/export.

The project direction is provider-neutral. Do not assume a provider, runtime, pricing model, backend, or public execution environment is selected. A request accepted by an API is not proof code ran; a running job is not complete; missing output must not be fabricated as success.

The product is still discovery-first. Separate validated user needs from hypotheses, requirements from proposals, architecture options from decisions, demos from reliable end-to-end behavior, and technical feasibility from sustainable service operations. Prioritize research that changes direction, narrows MVP, resolves costly uncertainty, or reduces safety risk. Do not expand platforms, languages, integrations, or infrastructure without evidence.

## 2. Owner situation, constraints, and working style

- Owner currently works mainly from an iPhone and has said they may lack PC/local file access for about four months.
- Keep spending at **$0**. No paid AI/service/provider, cloud workload, account setup, live execution, or infrastructure activation without explicit approval.
- Do not merge PRs, mark them ready, deploy, trigger workflows, release, change visibility, force-push, rewrite history, delete owner content, or do other consequential actions without explicit authorization.
- No GitHub Actions unless specifically approved; existing Pages workflow includes deployment, so do not dispatch it.
- PR #2 must remain untouched.
- Prefer regular chat, not Work mode.
- Minimize owner handoffs and manual PowerShell/file actions; do work through available connected tools when safe.
- Make substantial coherent passes, not many tiny exchanges. End with outcome, evidence, limitations, risks/blockers, and next action. If owner input is required, ask for the smallest specific item at the end.

## 3. Three-AI collaboration model

Defaults, contingent on tool access and current instructions:
- **Claude:** primary implementation lead when it has the necessary repository access/tools; consolidate information into one file rather than making the owner shuttle many files.
- **ChatGPT:** research, requirements clarification, architecture comparisons, continuity/handoff, integration planning, and evidence-based acceptance review.
- **Gemini:** independent architecture/specification review, adversarial analysis, test planning, and focused co-development when useful.

Use one primary implementer. Delegate a bounded question/deliverable to other AIs only when independent evidence or a different perspective is valuable. Avoid duplicate implementations/research, define ownership boundaries, consolidate findings, resolve disagreement from evidence and record the rationale. No assumption that another AI has done work unless its output/evidence is actually available.

## 4. Repository and PR state last verified

- Repository: `marcelosofficial-ctrl/PocketCode-` (**trailing hyphen is part of repo name**).
- Working branch: `pocketcode-pass0-audit-2026-10-26`.
- PR #3: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3 — draft, open, unmerged.
- Last observed PR #3 head: `e9718b7faf631c169326597fbc8a1678f65236a8` (verify current head before any further edits).
- PR #2: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2 — draft, open, unmerged. Last observed head `eb8b7ea83cb0e8fe1880351276c485b761431791`; updated_at last observed `2026-10-26T18:23:36Z`. Do not edit it.
- PR #3 title: “Draft: Add evidence-led PocketCode research baseline”.
- PR #3 was last observed updated `2026-10-27T20:35:49Z`.
- PR #3’s exact checked-in `scripts/test_lifecycle_contract.py` had **24 test methods** on the last fetch; this is a source count only, not test execution.
- No verified Actions run, provider workload, spend, deployment, or merge was performed in the described work. Verify current state if it materially matters.

## 5. Current code scope and limits

`scripts/lifecycle_contract.py` is a **pure provider-neutral contract/helper model**, not an execution backend. It does not execute user code, create real isolated sandboxes, enforce OS/network/resource isolation, perform transactional persistence, or prove evidence authenticity. The test file uses synthetic fixtures.

Relevant files in PR #3:
- `scripts/lifecycle_contract.py`: derived lifecycle disposition, ordered event replay, canonical request fingerprint, idempotency replay/conflict model, artifact release gate, output budget, configured-pattern streaming redaction, append-only in-memory report history, deletion tombstones, deterministic idempotency batch simulation.
- `scripts/test_lifecycle_contract.py`: synthetic unit-style test methods; last observed count 24.
- `AI_COLLAB/CONTRACT_CODE_TEST_TRACEABILITY_20261027.md`: decisions → helper seams → tests → gaps.
- `AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md`: acceptance cases.
- `AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md`: provider-neutral lifecycle contract proposal.
- `AI_COLLAB/PASS1_OWNER_DECISIONS_RESEARCH_20261027.md`
- `AI_COLLAB/PASS1_OWNER_DECISION_PACKET_20261027.md`
- `AI_COLLAB/PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md`
- `AI_COLLAB/DECISION_REGISTER.md`
- `AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md`
- `AI_COLLAB/RESEARCH_CHECKPOINT_ADDENDUM_20261027.md`
- `PROJECT_STATUS.md`
- `DECISIONS.md`

Other repository sources remain authoritative: inspect the actual repository for `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `SECURITY.md`, `ROADMAP.md`, `PRODUCT/EXECUTION_CONTRACT.md`, `MVP_DECISION_BRIEF.md`, `PASS0_REPOSITORY_AUDIT.md`, provider/competitor/cost research. The master plan itself says it is partial and incomplete; Gemini's pasted specification is not verified as a canonical repo update.

## 6. Adopted/provisional lifecycle policy decisions

These are current working decisions/provisional contract behavior; check DECISIONS.md and decision register before changing them.

1. **Artifact quarantine/release:** Do not release bytes, live provider URLs, or raw output if cleanup is uncertain. Release requires confirmed cleanup, valid digest/integrity, correct job association, and tenant authorization. Later-confirmed cleanup creates a new report version; never overwrite history.
2. **Events/races:** Coordinator ingress sequence controls replay order, not provider timestamps. One terminal decision per attempt; preserve later/conflicting evidence. Ambiguous or contradictory evidence cannot PASS. Replay by monotonic coordinator sequence; conflicting terminal evidence → INCOMPLETE.
3. **Idempotency:** tenant-scoped key. Same key + same canonical fingerprint replays existing job/report; same key + different fingerprint conflicts before allocation; explicit rerun uses a new key. Records retained while job/report addressable; provisional MVP uses a 30-day one-way tenant-scoped tombstone after deletion. Clients should not intentionally reuse keys after expiry.
4. **Output caps (provisional tests):** stdout 32 KiB, stderr 32 KiB, aggregate retained output 64 KiB. On cap breach terminate, stop retaining output, bounded drain/discard up to 1 second. Return LIMIT_EXCEEDED, never PASS. If termination/cleanup is uncertain, preserve uncertainty.
5. **Canonical fingerprint:** server-side, versioned fingerprint over contract/schema version, tenant, normalized runtime, entrypoint, exact decoded source/input bytes, canonical safe input names, media types, effective server policy/version. Exclude transport timestamps and client fingerprint. Named inputs sorted as an unordered mapping.
6. **Separate facts:** immutable execution observations, cleanup state, and versioned derived job disposition. PASS requires zero exit, policy confirmed before start, termination evidence, no timeout/cancel/limit/truncation, validated artifacts, correct tenant/job association, and confirmed cleanup.
7. **Provisional numeric test values:** source 64 KiB, inputs 256 KiB, stdout/stderr 32 KiB each, aggregate output 64 KiB, drain/discard 1 second, wall time 10 seconds, maximum 10 artifacts, 256 KiB per artifact, 1 MiB total artifacts. These are provisional contract/test values, not proven production enforcement.

## 7. Recent code audit findings / changes

Recent static review identified and addressed:
- Portable input-name validation rejects traversal/path separators, drive-relative/colon syntax, Windows reserved characters/device names, trailing dot/space, normalized-name collisions, and blank media types. This is not a complete request validator; upstream allowlists and policy enforcement are still required.
- ReportHistory restricts disposition and cleanup-state vocabularies; PASS append requires confirmed cleanup and explicit required gates.
- Output-limit breach has precedence over timeout/cancel/provider-error when evidence is not contradictory; contradiction still wins and yields INCOMPLETE.
- Duplicate event identity includes coordinator sequence/kind/payload; changed sequence is contradictory. Replay sorts by coordinator sequence with deterministic tie-break for malformed duplicate sequence; duplicate sequence is contradictory. Distinct terminal events create contradiction.
- Report history is append-only in-memory, versions per job, old snapshots are not mutated; no durable persistence/transactional allocation.
- Deletion tombstones are an in-memory tenant-scoped 30-day model.
- Idempotency batch reservation is a serial-order simulation, not actual atomic concurrent behavior.
- OutputBudget models observed bytes/caps/stopping retention, not real subprocess drain/termination.
- `derive_disposition` now requires literal boolean `True` for PASS gates, rather than Python truthiness. This prevents malformed values like `"false"` or integer `1` being treated as valid. Timeout/cancel termination confirmation also requires literal `True`.
- `artifact_release_allowed` now requires literal boolean `True` for digest validity, job association, and tenant authorization. Synthetic negative coverage added.
- Current acceptance matrix additions include STREAM-SEM-03 (aggregate cap+1 while streams individually under cap), LC-13 (contradictory evidence + NOT_STARTED => INCOMPLETE), LC-14 (exit-zero with cleanup PENDING/FAILED/UNKNOWN never PASS), FP-01 (non-portable names/blank media type rejected), OUT-02 (output cap combined with timeout/cancel/provider error → LIMIT_EXCEEDED unless contradiction), LC-15 (malformed truthy PASS flags fail closed), ART-SEM-02 (malformed artifact release flags fail closed).

**Important review caveat:** helper arguments/boolean fixtures are still caller-supplied assertions. Strict type checks do not prove evidence is authoritative, fresh, signed, transactionally stored, or bound to the actual job/tenant. This must be handled by future architecture/integration work, not claimed as solved by unit tests.

## 8. Test/verification truth

- Exact current checked-in helper/test pair and full repository suite were **NOT RUN** in the previous work.
- Earlier temporary reconstructed-copy test run 8/8 does not validate the current checked-in files.
- Attempt to fetch raw GitHub source from the container failed due DNS (`curl: (6) Could not resolve host: raw.githubusercontent.com`). Python 3.13.5 exists in that container, but exact files could not be retrieved there.
- GitHub connector can fetch exact file contents, but no safe confirmed route was found to execute those exact contents in a local interpreter. Do not use GitHub Actions because workflow may deploy Pages and no authorization was given.
- The latest code/test/doc writes were verified by fetching files again from the branch; that verifies contents are present, not that they parse or pass.
- Never call a written test “passed” unless actually executed. Continue looking for safe local/offline execution of exact checked-in source if feasible without running Actions or creating paid workloads.

## 9. Research and provider notes

Research references already considered:
- AWS Builders Library safe retries/idempotency: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- Stripe idempotency: https://docs.stripe.com/api/idempotent_requests
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OWASP File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- Python subprocess pipe deadlock warning: https://docs.python.org/3/library/subprocess.html
- Modal sandbox networking: https://frontend-deadbeef.modal.com/docs/guide/sandbox-networking (outbound allowed by default; block_network=True blocks outbound; docs do not prove full runtime isolation)
- E2B security: https://e2b.dev/security (asks users to contact before testing; terms require prior written consent)
- Cloudflare Containers requires Workers Paid ($5/month); Modal starter credits are not a hard $0 cap. E2B security testing requires prior written consent. No provider selected.
Do not restart provider research unless there is a decision-relevant question or new evidence.

## 10. Next recommended pass

Priority: **static audit the exact current checked-in lifecycle helper, tests, matrix, traceability, and decision wording as one coherent pass; fix concrete semantic gaps; update all affected docs; then attempt safe offline test execution if feasible.**

Acceptance criteria:
1. Verify current PR #3 head and branch before editing; confirm PR #2 remains untouched.
2. Review current source and tests for semantic mismatches: disposition precedence, malformed/missing evidence, strict booleans, artifact release gates, input normalization, terminal event conflicts, output-limit precedence, report history, idempotency/tombstone caveats.
3. Ensure each material behavior has a synthetic negative test and acceptance-matrix/crosswalk entry.
4. Update the existing traceability/status/checkpoint/PR description only as needed; no duplicate planning document.
5. Run exact checked-in tests only if a safe, authorized execution path exists; otherwise document the specific blocker and do not claim success.
6. Inspect exact final changed files/head; keep PR draft and unmerged, no Actions/provider spend/deploy, and do not touch PR #2.

## 11. Latest working-tree/repository details observed before this handoff was written

- Branch `pocketcode-pass0-audit-2026-10-26`.
- PR #3 head last observed `e9718b7faf631c169326597fbc8a1678f65236a8`.
- Current fetched helper blob SHA last observed: `ba8d4d0b217c90513bed020e298029ef4e16f164`.
- Current fetched test blob SHA last observed: `39db87d9f44f5e8474f33cff60136e529364199a`, 24 test methods.
- Current fetched master plan blob SHA: `246a6206d0349ceb897f3595f237da2426bc76e`.
- The status/checkpoint/traceability/matrix docs were fetched for review in the last pass; verify current blob SHAs and contents after this handoff commit because this handoff itself changes branch head.
- Last verified PR #2 state: draft/open/unmerged, head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- Exact source hashes/SHAs are blob identifiers, not commits. Do not confuse them with the PR head commit.


## Follow-up checkpoint — lifecycle static audit (2026-10-27)

- Separate branch: `pocketcode-lifecycle-fingerprint-audit-2026-10-27`. PR #3 remains open/draft/unmerged; this audit branch has not been merged or promoted to a PR.
- At the earlier lifecycle-audit checkpoint, source inspection found 30 test methods in `scripts/test_lifecycle_contract.py`; no exact test execution had occurred, so this was not a pass count.
- Additional static changes: reject blank canonical fingerprint identity values; reject blank/non-string idempotency reservation fields; preserve malformed event inputs under `invalid_events` and mark evidence contradictory; validate tombstone identity fields and epoch inputs.
- Acceptance matrix and traceability crosswalk updated with FP-02..FP-04, IDEM-03..IDEM-04, and LIFE-16.
- Exact helper/test suite and full repository suite remain **NOT RUN**. No GitHub Actions, provider workload, merge, deployment, account setup, or spend was initiated.
- Next: verify the final branch files and test syntax/behavior using an approved offline Python runtime. Continue static review only until executable verification is available.

- Additional event-schema audit: terminal-event reduction now rejects whitespace-only event IDs/kinds and missing or non-mapping payloads into `invalid_events`, marking evidence contradictory. Acceptance case LIFE-17 and regression test added. Source/test suite remains NOT RUN.

- Tombstone retry audit: repeated insertion for the same tenant/key/fingerprint now preserves the later expiry and cannot shorten retention; a different fingerprint conflicts. Added IDEM-05 regression and matrix/crosswalk entries. Exact suite remains NOT RUN.


Latest source-count refresh for the earlier lifecycle-audit branch: 30 test methods in `scripts/test_lifecycle_contract.py`, confirmed by fetching that branch file. Exact tests remained NOT RUN.


## Follow-up checkpoint — report-history PASS gate audit (2026-10-27)

- New isolated branch: `pocketcode-report-pass-gate-hardening-2026-10-27`, based on `pocketcode-lifecycle-fingerprint-audit-2026-10-27`. This branch is not PR #3's source branch.
- Static review found `ReportHistory.append` accepted PASS when only five gates were present. It now requires nine explicit consistency gates: exit zero, policy confirmed, termination confirmed, artifacts valid, tenant/job authorized, no limit violation, no output truncation, evidence consistent, and evidence associated.
- The helper now rejects whitespace-only job IDs and evidence references. Added two regression test methods: `test_report_history_rejects_whitespace_only_identity_fields` and `test_report_history_pass_requires_complete_limit_and_evidence_gates`.
- Updated the acceptance matrix with REPORT-03 and REPORT-04 and extended the code/test traceability table.
- Current `scripts/test_lifecycle_contract.py` count: 32 test methods by source inspection only. **The exact checked-in test module and full repository suite remain NOT RUN.** No GitHub Actions, provider, spend, deployment, merge, or PR update.
- Important limitation: the additional booleans are a pure-model consistency guard, not authenticated evidence. Production must derive gates from authoritative job-bound observations, not trust caller-provided booleans.
- Next: static diff review and consistency check across helper, test fixtures, matrix, and traceability. Do not claim test success without executing the exact checked-in files in an offline checkout.


- Additional follow-up: added `test_report_history_pass_rejects_truthy_non_boolean_gates`, covering `1`, `"true"`, and `None` for each of the nine PASS gates; added acceptance case REPORT-05. Static source count is now 33 test methods; exact tests remain NOT RUN.


## Follow-up checkpoint — limit-breach termination/cleanup coherence (2026-10-27)

- Cross-contract audit found that `derive_disposition` returned `LIMIT_EXCEEDED` for a cap breach even when process termination was unconfirmed or cleanup remained pending/unknown. That could make a terminal-looking disposition conceal unresolved lifecycle state.
- The helper now preserves the cap breach as an execution observation but returns disposition `LIMIT_EXCEEDED` only when termination and cleanup are both confirmed. Otherwise it returns `INCOMPLETE`; contradictory evidence still takes precedence and returns `INCOMPLETE`.
- Extended the existing synthetic regression test for both unconfirmed termination and pending cleanup, plus the confirmed limit-exceeded path. Updated OUT-02 and the code/test traceability caveat to match.
- This is a static source/document review and test-source change only. Exact checked-in tests and the full suite remain **NOT RUN**. Do not treat these cases as executed or production enforcement.
- Branch remains isolated and unmerged. No Actions, provider workload, spend, deployment, or PR #2/#3 changes.
