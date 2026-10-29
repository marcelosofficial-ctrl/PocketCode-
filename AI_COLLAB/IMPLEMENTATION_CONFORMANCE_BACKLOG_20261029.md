# PocketCode — implementation conformance backlog (research-only)
**Date:** 2026-10-29  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Status:** Proposed work order only. No implementation authorized by this document; all checks below are NOT RUN unless explicitly stated otherwise.  
**Authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and `PRODUCT/EXECUTION_CONTRACT.md` remain canonical and unchanged.

## Why this backlog exists
The Gemini reconciliation and read-only source inspection identified specific places where the research semantics are stronger than the helper contracts currently visible in PR #2/#3. This document converts those findings into small, ordered, reviewable tasks. It is not a request to merge either PR and does not authorize edits to them.

## Priority 0 — Freeze the trust boundary before implementation
**Gate:** Do not choose a provider or launch an untrusted workload until the chosen boundary can demonstrate all of these properties.

- **P0.1 Policy barrier:** attempt binds to an immutable policy revision, or dispatch is atomic/conditional against the expected revision. A policy read followed by a separate start call is insufficient evidence.
- **P0.2 Ambiguous start:** durable idempotency reservation is not proof of exactly-once execution. If start may have been accepted but acknowledgement is lost, perform authoritative lookup of the same attempt; if unresolved, retain UNKNOWN and do not automatically redispatch.
- **P0.3 Enforced controls:** identify authoritative evidence for isolation, egress denial, process/resource limits, termination, cleanup, and absence of service credentials. A fake adapter can test projection logic, not prove these controls.
- **P0.4 Budget/authority:** LOOP-14 remains a pre-workload gate. No account, billing, provider workload, Actions, deployment, or spend without explicit approval.

**Exit evidence:** a selected-boundary capability matrix with proof source, failure mode, and BLOCKED/UNKNOWN treatment for every required control. Provider choice remains OPEN.

## Priority 1 — Make report projection fail closed on incomplete evidence
**Source gap:** PR #2 `scripts/report_contract.py` `classify_verdict` accepts lifecycle status and integer exit code but has no collection-quality, policy, cleanup, or artifact-gate inputs. Its formatter-only contract means trusted caller gates are essential. PR #3 `derive_disposition` has no collection-state input.

Required behavior and focused tests:
1. Trusted exit code 0 + all required evidence complete + every mandatory gate confirmed -> PASS may be eligible (not automatically safe without the full contract).
2. Trusted exit code 0 + required stream UNAVAILABLE -> INCOMPLETE, preserving raw exit fact and collection reason.
3. Trusted exit code 0 + required stream PARTIAL_FAILURE -> INCOMPLETE, preserving raw exit fact and collection reason.
4. Trusted exit code 0 + required stream TRUNCATED_BY_POLICY -> no PASS unless that specific acceptance case explicitly allows partial output.
5. Empty COMPLETE stream remains distinguishable from unavailable/partial stream.
6. Collector failure does not rewrite cleanup state; collection and cleanup are independent dimensions.
7. Untrusted stdout/stderr containing PASS/success never overrides trusted nonzero exit or missing evidence.
8. Contradictory authoritative terminal evidence remains INCOMPLETE/UNKNOWN according to the canonical contract; no optimistic tie-break.

**Traceability:** LOOP-03, LOOP-04, LOOP-05, LOOP-07; CASE-01, CASE-03, CASE-06, CASE-09, CASE-10. Proposed supplement: SUP-REPORT-01..03 and SUP-RUN-04 where applicable. Do not rename or remap canonical IDs.

## Priority 2 — Separate runtime enforcement from presentation truncation
**Source gap:** PR #3 `derive_disposition(output_truncated=True)` maps truncation directly to LIMIT_EXCEEDED, but the single boolean does not distinguish runtime-enforced output limits from report/UI display truncation.

Required changes/tests, if separately authorized:
- Replace the ambiguous single fact with typed provenance or equivalent explicit fields: runtime-enforced truncation versus UI/report display truncation.
- Runtime truncation only yields LIMIT_EXCEEDED when trusted evidence shows the configured limit was enforced.
- UI/report truncation alone must not claim the runtime exceeded its limit.
- Preserve bounded original observation metadata; do not buffer unbounded output to calculate it.
- Test exact cap boundary, over-cap output, unavailable count, and display-only truncation independently.

**Traceability:** LOOP-07, LOOP-12; CASE-07; SUP-RUN-04. Keep the canonical meaning of CASE-07 intact.

## Priority 3 — Revalidate artifact safety at the actual release boundary
**Source gap:** PR #3 `artifact_release_allowed` checks selected booleans (cleanup, digest, job association, tenant authorization) but does not itself establish the full release-time checklist.

Required release-time checks:
- Current requester authorization is re-evaluated for each download/export.
- Safe normalized path/name; reject traversal, ambiguous normalization, and disallowed names.
- Allowed media type and per-file/aggregate size and count limits.
- Integrity of final stored bytes, not only a pre-storage digest.
- Exact job + attempt + tenant association.
- Required cleanup and evidence gates resolved.
- On mismatch or unknown mandatory evidence: deny/quarantine, emit a bounded reason, and do not leak bytes.
- Secret scanning/redaction remains an explicit policy decision; do not claim it exists unless implemented and tested.

**Regression:** FAKE-17 — historical PASS, but release-time authorization or artifact validation fails -> deny/quarantine at release; preserve historical report and record current release denial separately.

**Traceability:** LOOP-10, LOOP-11, LOOP-12; CASE-08, CASE-14, CASE-15; SUP-FILE-01..02 and SUP-SEC-01. A unit test of booleans does not prove storage or authorization enforcement.

## Priority 4 — Recover safely after disconnect and out-of-order events
Only required if the selected architecture supports remote asynchronous execution.

- Lost acknowledgement after possible accepted start -> lookup same job/attempt using authoritative state; never create a new attempt solely because the response was lost.
- If authoritative lookup is unavailable or ambiguous -> UNKNOWN/INCOMPLETE; no automatic redispatch.
- Identical event ID + identical payload -> idempotent replay; same ID + conflicting payload -> contradiction, not overwrite.
- Late evidence creates a new report version; it does not rewrite an issued report or imply a new execution attempt.
- Two attempts completing out of start order must retain correct attempt/report/artifact association.
- A durable idempotency key/reservation is not by itself an exactly-once guarantee.

**Traceability:** CASE-11, CASE-13, CASE-16; SUP-REC-01. Current TPM-07/08/14 coverage is partial, not proof of recovery semantics.

## Priority 5 — Mobile loop and privacy acceptance
Keep these as real UI/platform acceptance tests, not inferred from pure Python helpers:
- LOOP-01: select/edit script and input file on phone, run, inspect output, export a file.
- LOOP-02/13: simulated states and cross-app capabilities are labelled honestly; no unsupported background automation claims.
- LOOP-06: named structured checks retain status, source, and meaning.
- LOOP-08: copy action plus selectable-text fallback when clipboard access fails.
- LOOP-09: preserve prior report, edit, explicitly rerun, and identify the new attempt.
- LOOP-11: inspect the actual copied report against seeded secrets/unrelated files and size limits.
- CASE-12: copy a failed/incomplete report with useful diagnostics and no secret leakage.

These need a chosen UI and platform test setup. Until then they are BLOCKED, not passed by helper tests.

## Suggested execution order
1. Owner approves a bounded implementation task and identifies whether PR #2 or PR #3 is in scope.
2. Write focused tests first for Priority 1 and Priority 2; keep raw execution facts separate from derived disposition.
3. Implement only the authorized helper change; run the exact checked-in tests plus full relevant suite and record interpreter/version, command, exit code, counts, and commit.
4. Address Priority 3 only with a defined storage/release boundary; pure helper tests are necessary but insufficient.
5. Select/assess a provider only after Priority 0 evidence is available; run hosted security and resource tests only with explicit approval.
6. Do not close mobile, recovery, isolation, egress, or $0 acceptance gaps using mock-only evidence.

## Evidence state at creation
- PR #2 report helper: static source inspected; no current test execution in this pass.
- PR #3 lifecycle helper: static source inspected; no current test execution in this pass; 24 test methods observed in source, not run.
- TPM-01..16 and SUP-* cases: specifications only; NOT RUN.
- Provider, hosted runtime, mobile UI, isolation, egress, termination, durable recovery, and real artifact storage: not selected or not verified.
- Canonical acceptance IDs and files: unchanged.
- PR #2 and PR #3: untouched by this task.
