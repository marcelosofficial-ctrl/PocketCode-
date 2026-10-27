"""Pure provider-neutral lifecycle rules for deterministic offline tests.

This module does not launch processes, contact providers, or claim runtime
security. It models evidence/disposition decisions using synthetic inputs.
"""
from __future__ import annotations

import base64
import hashlib
import json
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

    Duplicate event IDs with identical kind/payload are idempotent. Conflicting
    reuse of an event ID marks evidence contradictory. Provider timestamps are
    intentionally ignored for ordering.
    """
    by_id: dict[str, tuple[str, Any]] = {}
    accepted: list[dict[str, Any]] = []
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
        signature = (kind, payload)
        if event_id in by_id:
            if by_id[event_id] != signature:
                contradictory = True
            continue
        by_id[event_id] = signature
        accepted.append(event)

    accepted.sort(key=lambda item: item["sequence"])
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
        self.exceeded = False

    def add(self, stream: str, chunk: bytes) -> None:
        if stream not in self.retained or not isinstance(chunk, bytes):
            raise ValueError("stream must be stdout/stderr and chunk must be bytes")
        self.observed[stream] += len(chunk)
        if self.exceeded:
            return

        stream_room = max(0, self.per_stream_cap - len(self.retained[stream]))
        aggregate_used = sum(len(value) for value in self.retained.values())
        aggregate_room = max(0, self.aggregate_cap - aggregate_used)
        keep = min(len(chunk), stream_room, aggregate_room)
        self.retained[stream].extend(chunk[:keep])
        if len(chunk) > keep or len(self.retained[stream]) > self.per_stream_cap:
            self.exceeded = True

    def retained_bytes(self, stream: str) -> bytes:
        return bytes(self.retained[stream])
