"""Composition model joining fake outbox and event journal recovery semantics.

This is a deterministic in-memory conformance model, not durable storage,
a production coordinator, a provider adapter, or a security boundary.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

try:
    from fake_outbox import FakeOutboxStore, Lease, OutboxConflict
    from event_journal import AuthenticatedProducer, EventJournal, AppendResult
except ModuleNotFoundError:
    from scripts.fake_outbox import FakeOutboxStore, Lease, OutboxConflict
    from scripts.event_journal import AuthenticatedProducer, EventJournal, AppendResult


@dataclass(frozen=True)
class RebuiltEffect:
    effect_id: str
    attempt_id: str
    state: str
    last_sequence: int
    event_count: int
    provider_reference: Optional[str] = None


class FakeCoordinator:
    """Coordinates explicit model boundaries and deterministic crash injection."""

    def __init__(self, *, store: FakeOutboxStore, journal: EventJournal,
                 producer: AuthenticatedProducer) -> None:
        self.store = store
        self.journal = journal
        self.producer = producer

    @staticmethod
    def _payload(kind: str, effect_id: str, attempt_id: str, **extra: object) -> bytes:
        value = {"kind": kind, "effect_id": effect_id, "attempt_id": attempt_id}
        value.update(extra)
        return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def _append(self, *, kind: str, effect_id: str, attempt_id: str,
                event_id: str, at_ms: int, fence: Optional[int] = None,
                **extra: object) -> AppendResult:
        bound = {}
        if fence is not None:
            bound = {"effect_id": effect_id, "attempt_id": attempt_id, "fence": fence}
        return self.journal.append(
            producer=self.producer, source="pocketcode.coordinator",
            event_id=event_id,
            payload=self._payload(kind, effect_id, attempt_id, **extra),
            occurred_at_ms=at_ms, observed_at_ms=at_ms, **bound,
        )

    def reserve(self, effect_id: str, attempt_id: str, fingerprint: str,
                request: bytes, *, at_ms: int,
                crash_after_store_commit: bool = False) -> str:
        self.store.reserve(effect_id, attempt_id, fingerprint, request,
                           created_at_ms=at_ms)
        if crash_after_store_commit:
            raise RuntimeError("simulated crash after outbox reservation commit")
        return self._append(
            kind="effect_reserved", effect_id=effect_id, attempt_id=attempt_id,
            event_id=f"reserved:{effect_id}:{attempt_id}", at_ms=at_ms,
            request_fingerprint=fingerprint,
        ).disposition

    def repair_missing_reservation_event(self, effect_id: str) -> str:
        reservation = self.store.get(effect_id).reservation
        if reservation.created_at_ms is None:
            raise OutboxConflict("reservation has no persisted creation timestamp")
        return self._append(
            kind="effect_reserved", effect_id=effect_id,
            attempt_id=reservation.attempt_id,
            event_id=f"reserved:{effect_id}:{reservation.attempt_id}",
            at_ms=reservation.created_at_ms,
            request_fingerprint=reservation.request_fingerprint,
        ).disposition

    def claim(self, effect_id: str, owner: str, *, now: int,
              lease_seconds: int) -> Lease:
        lease = self.store.claim(effect_id, owner, now=now, lease_seconds=lease_seconds)
        self.journal.advance_fence(lease.effect_id, lease.attempt_id, lease.fence)
        self._append(
            kind="lease_claimed", effect_id=lease.effect_id,
            attempt_id=lease.attempt_id,
            event_id=f"claim:{lease.effect_id}:{lease.attempt_id}:{lease.fence}",
            at_ms=now, fence=lease.fence, owner=owner, expires_at=lease.expires_at,
        )
        return lease

    def mark_dispatching(self, lease: Lease, *, now: int,
                         crash_after_store_transition: bool = False) -> str:
        self.store.mark_dispatching(lease, now=now)
        if crash_after_store_transition:
            raise RuntimeError("simulated crash after persisted dispatch intent")
        return self._append(
            kind="dispatch_intent", effect_id=lease.effect_id,
            attempt_id=lease.attempt_id,
            event_id=f"dispatch:{lease.effect_id}:{lease.attempt_id}:{lease.fence}",
            at_ms=now, fence=lease.fence,
        ).disposition

    def acknowledge(self, lease: Lease, provider_reference: str, *, now: int,
                    crash_after_store_transition: bool = False) -> str:
        # Validate and persist acknowledgement in the outbox before journaling.
        # If interrupted, repair from this accepted record using its stored time.
        self.store.acknowledge(lease, provider_reference, now=now)
        if crash_after_store_transition:
            raise RuntimeError("simulated crash after outbox acknowledgement")
        return self._append(
            kind="dispatch_acknowledged", effect_id=lease.effect_id,
            attempt_id=lease.attempt_id,
            event_id=f"ack:{lease.effect_id}:{lease.attempt_id}:{lease.fence}",
            at_ms=now, fence=lease.fence, provider_reference=provider_reference,
        ).disposition

    def repair_missing_ack_event(self, effect_id: str) -> str:
        record = self.store.get(effect_id)
        if (record.state not in {"acknowledged", "terminal"}
                or not record.provider_reference or record.acknowledged_at is None):
            raise OutboxConflict("no accepted acknowledgement is available to repair")
        attempt_id = record.reservation.attempt_id
        return self._append(
            kind="dispatch_acknowledged", effect_id=effect_id,
            attempt_id=attempt_id, event_id=f"ack:{effect_id}:{attempt_id}:{record.fence}",
            at_ms=record.acknowledged_at, fence=record.fence,
            provider_reference=record.provider_reference,
        ).disposition

    def recover_expired(self, effect_id: str, *, now: int) -> str:
        return self.store.recover_expired(effect_id, now=now)

    def rebuild_effect(self, effect_id: str) -> RebuiltEffect:
        """Rebuild a read model from accepted events; quarantine is excluded."""
        record = self.store.get(effect_id)
        attempt_id = record.reservation.attempt_id
        matching = []
        for event in self.journal.events:
            if event.effect_id == effect_id and event.attempt_id == attempt_id:
                try:
                    payload = json.loads(event.payload.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                matching.append((event.sequence, payload))
        matching.sort(key=lambda pair: pair[0])
        state = "reserved"
        provider_reference = None
        for sequence, payload in matching:
            kind = payload.get("kind")
            if kind == "lease_claimed":
                state = "leased"
            elif kind == "dispatch_intent":
                state = "dispatching"
            elif kind == "dispatch_acknowledged":
                state = "acknowledged"
                provider_reference = payload.get("provider_reference")
        return RebuiltEffect(
            effect_id, attempt_id, state,
            matching[-1][0] if matching else 0, len(matching), provider_reference,
        )
