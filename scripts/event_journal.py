"""Append-only event provenance model for PocketCode.

Pure deterministic model. Producer authentication is supplied by a trusted
adapter as an AuthenticatedProducer value; this module does not verify keys,
signatures, certificates, sessions, or external credentials.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


class JournalConflict(ValueError):
    pass


@dataclass(frozen=True)
class AuthenticatedProducer:
    issuer: str
    subject: str
    key_id: str
    credential_fingerprint: str
    audience: str
    authorized_sources: tuple[str, ...]


@dataclass(frozen=True)
class JournalEvent:
    sequence: int
    source: str
    producer_event_id: str
    producer_issuer: str
    producer_subject: str
    producer_key_id: str
    payload: bytes
    payload_sha256: str
    occurred_at_ms: int
    observed_at_ms: int
    effect_id: Optional[str]
    attempt_id: Optional[str]
    fence: Optional[int]


@dataclass(frozen=True)
class QuarantinedConflict:
    sequence: int
    source: str
    producer_event_id: str
    accepted_payload_sha256: str
    conflicting_payload_sha256: str
    reason: str = "producer_event_id_payload_conflict"


@dataclass(frozen=True)
class AppendResult:
    disposition: str
    sequence: int
    event: Optional[JournalEvent] = None
    conflict: Optional[QuarantinedConflict] = None


class EventJournal:
    """In-memory append-only journal with source-scoped identity and fencing."""

    def __init__(self, *, expected_audience: str) -> None:
        if not isinstance(expected_audience, str) or not expected_audience.strip():
            raise ValueError("expected_audience must be non-empty")
        self.expected_audience = expected_audience
        self._events: list[JournalEvent] = []
        self._conflicts: list[QuarantinedConflict] = []
        self._identity: dict[tuple[str, str], JournalEvent] = {}
        self._fences: dict[tuple[str, str], int] = {}
        self._sequence = 0

    @property
    def events(self) -> tuple[JournalEvent, ...]:
        return tuple(self._events)

    @property
    def conflicts(self) -> tuple[QuarantinedConflict, ...]:
        return tuple(self._conflicts)

    @property
    def last_sequence(self) -> int:
        return self._sequence

    def advance_fence(self, effect_id: str, attempt_id: str, fence: int) -> None:
        if not _nonempty(effect_id, attempt_id) or not _positive_int(fence):
            raise ValueError("valid effect, attempt and positive fence required")
        key = (effect_id, attempt_id)
        current = self._fences.get(key, 0)
        if fence <= current:
            raise JournalConflict("fence must strictly increase")
        self._fences[key] = fence

    def append(
        self, *, producer: AuthenticatedProducer, source: str, event_id: str,
        payload: bytes, occurred_at_ms: int, observed_at_ms: int,
        effect_id: Optional[str] = None, attempt_id: Optional[str] = None,
        fence: Optional[int] = None, require_fence: bool = True,
    ) -> AppendResult:
        _validate_producer(producer, self.expected_audience, source)
        if not _nonempty(event_id) or not isinstance(payload, bytes) or not payload:
            raise ValueError("event_id and immutable non-empty payload bytes required")
        if not _nonnegative_int(occurred_at_ms) or not _nonnegative_int(observed_at_ms):
            raise ValueError("timestamps must be non-negative integer milliseconds")
        if type(require_fence) is not bool:
            raise ValueError("require_fence must be a literal boolean")
        if (effect_id is None) != (attempt_id is None):
            raise ValueError("effect_id and attempt_id must be supplied together")
        if not require_fence and effect_id is None:
            raise JournalConflict("unfenced events must be bound to an effect and attempt")
        if effect_id is not None:
            if not _nonempty(effect_id, attempt_id):
                raise ValueError("effect/attempt identity must be non-empty")
            current_fence = self._fences.get((effect_id, attempt_id))
            if require_fence:
                if current_fence is None:
                    if fence is not None:
                        raise JournalConflict("fence supplied before a lease generation exists")
                elif not _positive_int(fence) or fence != current_fence:
                    raise JournalConflict("event rejected by current fencing token")
            else:
                if fence is not None:
                    raise JournalConflict("unfenced event cannot carry a fencing token")
                try:
                    reservation_payload = json.loads(payload.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise JournalConflict("unfenced events must be valid reservation payloads") from exc
                if (source != "pocketcode.coordinator"
                        or not isinstance(reservation_payload, dict)
                        or reservation_payload.get("kind") != "effect_reserved"
                        or reservation_payload.get("effect_id") != effect_id
                        or reservation_payload.get("attempt_id") != attempt_id):
                    raise JournalConflict(
                        "only a matching coordinator effect_reserved event may be unfenced"
                    )
        elif fence is not None:
            raise ValueError("fence cannot be supplied without effect and attempt identity")
        digest = sha256(payload).hexdigest()
        key = (source, event_id)
        prior = self._identity.get(key)
        if prior is not None:
            same_producer = (
                prior.producer_issuer == producer.issuer
                and prior.producer_subject == producer.subject
                and prior.effect_id == effect_id
                and prior.attempt_id == attempt_id
                and prior.fence == fence
            )
            if (same_producer and prior.payload_sha256 == digest
                    and prior.payload == payload
                    and prior.occurred_at_ms == occurred_at_ms):
                return AppendResult("duplicate", prior.sequence, event=prior)
            self._sequence += 1
            conflict = QuarantinedConflict(
                self._sequence, source, event_id, prior.payload_sha256, digest,
            )
            self._conflicts.append(conflict)
            return AppendResult("quarantined", conflict.sequence, conflict=conflict)

        self._sequence += 1
        event = JournalEvent(
            sequence=self._sequence, source=source, producer_event_id=event_id,
            producer_issuer=producer.issuer, producer_subject=producer.subject,
            producer_key_id=producer.key_id, payload=bytes(payload),
            payload_sha256=digest, occurred_at_ms=occurred_at_ms,
            observed_at_ms=observed_at_ms, effect_id=effect_id,
            attempt_id=attempt_id, fence=fence,
        )
        self._events.append(event)
        self._identity[key] = event
        return AppendResult("accepted", event.sequence, event=event)


def _nonempty(*values: object) -> bool:
    return all(isinstance(v, str) and bool(v.strip()) for v in values)


def _nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _validate_producer(producer: object, expected_audience: str, source: str) -> None:
    if not isinstance(producer, AuthenticatedProducer):
        raise JournalConflict("producer must be adapter-verified identity")
    if not _nonempty(producer.issuer, producer.subject, producer.key_id,
                     producer.credential_fingerprint, producer.audience):
        raise JournalConflict("producer identity is incomplete")
    if producer.audience != expected_audience:
        raise JournalConflict("producer audience mismatch")
    if not isinstance(producer.authorized_sources, tuple) or source not in producer.authorized_sources:
        raise JournalConflict("producer is not authorized for this source")
