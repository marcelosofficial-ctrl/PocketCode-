"""Pure provider-neutral lifecycle rules for deterministic offline tests.

This module does not launch processes, contact providers, or claim runtime
security. It models evidence/disposition decisions using synthetic inputs.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import unicodedata
from typing import Any, Iterable, Mapping


TERMINAL_EVENTS = {
    "exit_zero": "EXIT_ZERO",
    "exit_nonzero": "EXIT_NONZERO",
    "timeout": "TIMED_OUT",
    "cancel": "CANCELLED",
    "limit_exceeded": "LIMIT_EXCEEDED",
    "provider_error": "UNKNOWN",
}


class IdempotencyConflict(ValueError):
    """The same tenant-scoped key was reused for a different request."""


def derive_disposition(
    execution_outcome: str,
    cleanup_state: str,
    *,
    policy_confirmed: bool,
    termination_confirmed: bool,
    artifacts_valid: bool,
    tenant_job_authorized: bool,
    limit_violated: bool = False,
    output_truncated: bool = False,
    contradictory_evidence: bool = False,
) -> str:
    """Derive a conservative job disposition from trusted evidence fields."""
    if execution_outcome == "NOT_STARTED":
        return "REJECTED"
    if contradictory_evidence:
        return "INCOMPLETE"
    if execution_outcome == "UNKNOWN":
        return "PROVIDER_ERROR"
    if execution_outcome == "TIMED_OUT":
        return "TIMED_OUT" if termination_confirmed else "INCOMPLETE"
    if execution_outcome == "CANCELLED":
        return "CANCELLED" if termination_confirmed else "INCOMPLETE"
    if execution_outcome == "LIMIT_EXCEEDED" or limit_violated or output_truncated:
        return "LIMIT_EXCEEDED"
    if execution_outcome == "EXIT_NONZERO":
        return "FAILED"
    if execution_outcome != "EXIT_ZERO":
        return "INCOMPLETE"
    if cleanup_state != "CONFIRMED":
        return "INCOMPLETE"
    if not all((policy_confirmed, termination_confirmed, artifacts_valid, tenant_job_authorized)):
        return "INCOMPLETE"
    return "PASS"


def reduce_terminal_events(events: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Replay accepted events; the first terminal event by coordinator sequence wins.

    Duplicate event IDs with identical coordinator sequence, kind, and payload are
    idempotent. Conflicting reuse of an event ID marks evidence contradictory. Provider timestamps are
    intentionally ignored for ordering.
    """
    by_id: dict[str, tuple[int, str, Any]] = {}
    accepted: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    contradictory = False

    for raw in events:
        event = dict(raw)
        event_id = event.get("event_id")
        sequence = event.get("sequence")
        kind = event.get("kind")
        payload = event.get("payload")
        if not isinstance(event_id, str) or not event_id:
            contradictory = True
            continue
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            contradictory = True
            continue
        if not isinstance(kind, str) or not kind:
            contradictory = True
            continue
        signature = (sequence, kind, payload)
        if event_id in by_id:
            if by_id[event_id] != signature:
                contradictory = True
                conflicts.append(event)
            continue
        by_id[event_id] = signature
        accepted.append(event)

    # A coordinator sequence should be unique. If malformed input reuses one,
    # mark the evidence contradictory above and use event ID as a stable tie-break
    # so replay output is deterministic regardless of input iteration order.
    accepted.sort(key=lambda item: (item["sequence"], item["event_id"]))
    sequences = [item["sequence"] for item in accepted]
    if len(sequences) != len(set(sequences)):
        contradictory = True

    terminal_outcome = "UNKNOWN"
    winning_event_id = None
    for event in accepted:
        outcome = TERMINAL_EVENTS.get(event["kind"])
        if outcome is not None and winning_event_id is None:
            terminal_outcome = outcome
            winning_event_id = event["event_id"]

    return {
        "events": accepted,
        "conflicts": conflicts,
        "execution_outcome": terminal_outcome,
        "winning_event_id": winning_event_id,
        "contradictory_evidence": contradictory,
    }


def _canonical_input_name(name: str) -> str:
    if not isinstance(name, str) or not name:
        raise ValueError("input name must be a non-empty string")
    normalized = unicodedata.normalize("NFC", name)
    if normalized in {".", ".."} or "/" in normalized or "\\" in normalized or "\x00" in normalized:
        raise ValueError("input name must be a safe basename")
    return normalized


def canonical_request_fingerprint(
    *,
    contract_version: str,
    tenant_id: str,
    runtime: str,
    entrypoint: str,
    source: bytes,
    inputs: Iterable[tuple[str, str, bytes]],
    effective_policy: Mapping[str, Any],
) -> str:
    """Return a versioned SHA-256 fingerprint of canonical request semantics.

    Input bytes are exact decoded bytes. Input order is canonicalized by name
    because the initial contract treats named inputs as an unordered mapping.
    """
    if not all(isinstance(value, str) and value for value in
               (contract_version, tenant_id, runtime, entrypoint)):
        raise ValueError("contract, tenant, runtime, and entrypoint are required")
    if not isinstance(source, bytes):
        raise TypeError("source must be decoded bytes")

    canonical_inputs = []
    seen = set()
    for name, media_type, data in inputs:
        canonical_name = _canonical_input_name(name)
        collision_key = canonical_name.casefold()
        if collision_key in seen:
            raise ValueError("duplicate normalized input name")
        seen.add(collision_key)
        if not isinstance(media_type, str) or not isinstance(data, bytes):
            raise TypeError("input media type must be text and content must be bytes")
        canonical_inputs.append({
            "name": canonical_name,
            "media_type": media_type.strip().lower(),
            "content_b64": base64.b64encode(data).decode("ascii"),
        })
    canonical_inputs.sort(key=lambda item: item["name"])

    document = {
        "fingerprint_version": 1,
        "contract_version": contract_version,
        "tenant_id": tenant_id,
        "runtime": runtime.strip().lower(),
        "entrypoint": entrypoint,
        "source_b64": base64.b64encode(source).decode("ascii"),
        "inputs": canonical_inputs,
        "effective_policy": dict(effective_policy),
    }
    encoded = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reserve_idempotency(
    records: dict[tuple[str, str], tuple[str, str]],
    *,
    tenant_id: str,
    key: str,
    fingerprint: str,
    proposed_job_id: str,
) -> tuple[str, str]:
    """Pure single-process reservation model; not a concurrency implementation."""
    if not tenant_id or not key or not fingerprint or not proposed_job_id:
        raise ValueError("tenant, key, fingerprint, and job ID are required")
    record_key = (tenant_id, key)
    existing = records.get(record_key)
    if existing is None:
        records[record_key] = (fingerprint, proposed_job_id)
        return ("CREATED", proposed_job_id)
    old_fingerprint, old_job_id = existing
    if old_fingerprint != fingerprint:
        raise IdempotencyConflict("key already belongs to a different request")
    return ("REPLAY", old_job_id)


def artifact_release_allowed(
    *,
    cleanup_state: str,
    digest_valid: bool,
    job_association_valid: bool,
    tenant_authorized: bool,
) -> bool:
    """Artifacts are releasable only when every cleanup/integrity/auth gate passes."""
    return (
        cleanup_state == "CONFIRMED"
        and digest_valid
        and job_association_valid
        and tenant_authorized
    )


class OutputBudget:
    """Bound retained output by per-stream and aggregate byte caps."""
    def __init__(self, per_stream_cap: int = 32 * 1024, aggregate_cap: int = 64 * 1024):
        if per_stream_cap <= 0 or aggregate_cap <= 0:
            raise ValueError("caps must be positive")
        self.per_stream_cap = per_stream_cap
        self.aggregate_cap = aggregate_cap
        self.observed = {"stdout": 0, "stderr": 0}
        self.retained = {"stdout": bytearray(), "stderr": bytearray()}
        self.redactors = {"stdout": StreamingRedactor(), "stderr": StreamingRedactor()}
        self.exceeded = False

    def add(self, stream: str, chunk: bytes) -> None:
        if stream not in self.retained or not isinstance(chunk, bytes):
            raise ValueError("stream must be stdout/stderr and chunk must be bytes")
        previous_stream = self.observed[stream]
        previous_total = sum(self.observed.values())
        self.observed[stream] += len(chunk)
        if self.exceeded:
            return

        stream_room = max(0, self.per_stream_cap - previous_stream)
        aggregate_room = max(0, self.aggregate_cap - previous_total)
        allowed = min(len(chunk), stream_room, aggregate_room)
        safe_chunk = self.redactors[stream].feed(chunk[:allowed])
        self.retained[stream].extend(safe_chunk[:max(
            0, min(self.per_stream_cap - len(self.retained[stream]),
                   self.aggregate_cap - sum(len(value) for value in self.retained.values()))
        )])
        if len(chunk) > allowed:
            self.exceeded = True
            for redactor in self.redactors.values():
                redactor.reset()

    def finish(self) -> None:
        """Flush safe redacted tails unless a cap breach discarded pending data."""
        if self.exceeded:
            return
        for stream, redactor in self.redactors.items():
            safe_tail = redactor.finish()
            room = max(0, min(
                self.per_stream_cap - len(self.retained[stream]),
                self.aggregate_cap - sum(len(value) for value in self.retained.values()),
            ))
            self.retained[stream].extend(safe_tail[:room])

    def retained_bytes(self, stream: str) -> bytes:
        return bytes(self.retained[stream])


class StreamingRedactor:
    """Best-effort bounded token-pattern redaction across chunk boundaries.

    Replacements preserve byte length so the safe output cutoff maps to the
    original input cutoff. This covers configured patterns only, not all secrets.
    """
    CARRY_BYTES = 768
    PATTERNS = (
        re.compile(rb"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{8,256}\b"),
        re.compile(rb"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]{1,256}"),
        re.compile(rb"\b(?:sk-[A-Za-z0-9_-]{16,128}|gh[pousr]_[A-Za-z0-9]{20,128}|AKIA[0-9A-Z]{16})\b"),
    )

    def __init__(self) -> None:
        self.pending = bytearray()

    @classmethod
    def _redact(cls, data: bytes) -> bytes:
        result = data
        for pattern in cls.PATTERNS:
            result = pattern.sub(lambda match: b"*" * len(match.group(0)), result)
        return result

    def feed(self, chunk: bytes) -> bytes:
        combined = bytes(self.pending) + chunk
        if len(combined) <= self.CARRY_BYTES:
            self.pending = bytearray(combined)
            return b""
        cutoff = len(combined) - self.CARRY_BYTES
        # Never split a configured match at the raw carry boundary: doing so
        # would leave an unredacted suffix in pending after the prefix is emitted.
        while True:
            earlier = [
                match.start()
                for pattern in self.PATTERNS
                for match in pattern.finditer(combined)
                if match.start() < cutoff < match.end()
            ]
            if not earlier:
                break
            cutoff = min(earlier)
        redacted = self._redact(combined)
        safe_prefix = redacted[:cutoff]
        self.pending = bytearray(combined[cutoff:])
        return safe_prefix

    def finish(self) -> bytes:
        result = self._redact(bytes(self.pending))
        self.pending.clear()
        return result

    def reset(self) -> None:
        self.pending.clear()


class ReportHistory:
    """Pure append-only report-version model; persistence/atomicity are external.

    A new disposition after cleanup reconciliation creates a new version. Existing
    entries are never edited or replaced by this helper.
    """
    def __init__(self) -> None:
        self._versions: dict[str, list[dict[str, Any]]] = {}

    def append(self, job_id: str, *, disposition: str, cleanup_state: str,
               evidence_ref: str) -> dict[str, Any]:
        if not all(isinstance(value, str) and value for value in
                   (job_id, disposition, cleanup_state, evidence_ref)):
            raise ValueError("job, disposition, cleanup state, and evidence reference are required")
        if disposition == "PASS" and cleanup_state != "CONFIRMED":
            raise ValueError("PASS requires confirmed cleanup")
        versions = self._versions.setdefault(job_id, [])
        report = {"job_id": job_id, "version": len(versions) + 1,
                  "disposition": disposition, "cleanup_state": cleanup_state,
                  "evidence_ref": evidence_ref}
        versions.append(dict(report))
        return dict(report)

    def versions(self, job_id: str) -> tuple[dict[str, Any], ...]:
        return tuple(dict(item) for item in self._versions.get(job_id, []))


class DeletionTombstones:
    """Pure 30-day post-deletion key-retention model, not a storage implementation."""
    RETENTION_SECONDS = 30 * 24 * 60 * 60

    def __init__(self) -> None:
        self._records: dict[tuple[str, str], tuple[str, int]] = {}

    def add(self, *, tenant_id: str, key: str, fingerprint: str, deleted_at: int) -> None:
        if not tenant_id or not key or not fingerprint:
            raise ValueError("tenant, key, and fingerprint are required")
        if not isinstance(deleted_at, int) or isinstance(deleted_at, bool) or deleted_at < 0:
            raise ValueError("deleted_at must be a non-negative integer epoch")
        self._records[(tenant_id, key)] = (fingerprint, deleted_at + self.RETENTION_SECONDS)

    def lookup(self, *, tenant_id: str, key: str, now: int) -> tuple[str, str] | None:
        """Return a tombstone while retained; expire at the exact deadline."""
        record_key = (tenant_id, key)
        record = self._records.get(record_key)
        if record is None:
            return None
        fingerprint, expires_at = record
        if now >= expires_at:
            del self._records[record_key]
            return None
        return ("TOMBSTONE", fingerprint)


def reserve_idempotency_batch(
    records: dict[tuple[str, str], tuple[str, str]],
    submissions: Iterable[Mapping[str, str]],
) -> list[dict[str, str]]:
    """Deterministic serializable model for racing submissions; NOT atomic storage.

    The first submission in coordinator order reserves the key. Later submissions
    replay or conflict. Production must enforce this with a unique constraint or
    transaction; this function only tests intended outcomes.
    """
    results = []
    for item in submissions:
        tenant_id = item.get("tenant_id", "")
        key = item.get("key", "")
        fingerprint = item.get("fingerprint", "")
        proposed_job_id = item.get("proposed_job_id", "")
        if not all((tenant_id, key, fingerprint, proposed_job_id)):
            raise ValueError("each submission needs tenant, key, fingerprint, and proposed job ID")
        try:
            status, job_id = reserve_idempotency(
                records, tenant_id=tenant_id, key=key,
                fingerprint=fingerprint, proposed_job_id=proposed_job_id,
            )
        except IdempotencyConflict:
            results.append({"status": "CONFLICT", "job_id": "", "proposed_job_id": proposed_job_id})
        else:
            results.append({"status": status, "job_id": job_id, "proposed_job_id": proposed_job_id})
    return results
