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

    def repair_missing_lease_claim_event(self, effect_id: str) -> str:
        record = self.store.get(effect_id)
        if (record.state not in {"leased", "dispatching", "reconciling", "acknowledged", "retry_authorized"}
                or record.lease_claimed_at is None or record.lease_owner is None):
            raise OutboxConflict("no persisted lease claim is available to repair")
        return self._append(
            kind="lease_claimed", effect_id=effect_id,
            attempt_id=record.reservation.attempt_id,
            event_id=f"claim:{effect_id}:{record.reservation.attempt_id}:{record.fence}",
            at_ms=record.lease_claimed_at, fence=record.fence,
            owner=record.lease_owner, expires_at=record.lease_expires_at,
        ).disposition

    def repair_missing_dispatch_intent_event(self, effect_id: str) -> str:
        record = self.store.get(effect_id)
        if (record.state not in {"dispatching", "reconciling", "acknowledged", "retry_authorized", "terminal"}
                or record.dispatch_intent_at is None):
            raise OutboxConflict("no persisted dispatch intent is available to repair")
        return self._append(
            kind="dispatch_intent", effect_id=effect_id,
            attempt_id=record.reservation.attempt_id,
            event_id=f"dispatch:{effect_id}:{record.reservation.attempt_id}:{record.fence}",
            at_ms=record.dispatch_intent_at, fence=record.fence,
        ).disposition

    def repair_missing_ack_event(self, effect_id: str) -> str:
        record = self.store.get(effect_id)
        if (record.state not in {"acknowledged", "terminal"}
                or not record.provider_reference or record.acknowledged_at is None):
            raise OutboxConflict("no accepted acknowledgement is available to repair")
        attempt_id = record.reservation.attempt_id
        if record.acknowledgement_source == "reconciliation":
            kind = "provider_acceptance_reconciled"
            event_id = f"reconciled-found:{effect_id}:{attempt_id}:{record.fence}"
        else:
            kind = "dispatch_acknowledged"
            event_id = f"ack:{effect_id}:{attempt_id}:{record.fence}"
        return self._append(
            kind=kind, effect_id=effect_id, attempt_id=attempt_id,
            event_id=event_id, at_ms=record.acknowledged_at, fence=record.fence,
            provider_reference=record.provider_reference,
        ).disposition

    def reconcile(self, effect_id: str, *, outcome: str, exact_identity_match: bool,
                  authoritative: bool, now: int, absence_final: bool = False,
                  provider_reference: Optional[str] = None) -> str:
        """Apply a caller-verified exact-scope lookup and journal its observation.

        This model does not authenticate the lookup result. A real adapter must
        verify provider authority, scope and final-absence guarantees first.
        """
        record = self.store.get(effect_id)
        attempt_id = record.reservation.attempt_id
        disposition = self.store.resolve_reconciliation(
            effect_id, outcome=outcome, exact_identity_match=exact_identity_match,
            authoritative=authoritative, absence_final=absence_final,
            provider_reference=provider_reference, now=now,
        )
        if disposition == "adopt_existing":
            self._append(
                kind="provider_acceptance_reconciled", effect_id=effect_id,
                attempt_id=attempt_id,
                event_id=f"reconciled-found:{effect_id}:{attempt_id}:{record.fence}",
                at_ms=now, fence=record.fence,
                provider_reference=provider_reference,
            )
        elif disposition == "safe_to_retry_same_attempt":
            self._append(
                kind="final_absence_reconciled", effect_id=effect_id,
                attempt_id=attempt_id,
                event_id=f"reconciled-absent:{effect_id}:{attempt_id}:{record.fence}",
                at_ms=now, fence=record.fence,
            )
        return disposition

    def repair_missing_reconciliation_event(self, effect_id: str) -> str:
        record = self.store.get(effect_id)
        if record.state != "retry_authorized" or record.reconciliation_observed_at is None:
            raise OutboxConflict("no final-absence retry authorization is available to repair")
        return self._append(
            kind="final_absence_reconciled", effect_id=effect_id,
            attempt_id=record.reservation.attempt_id,
            event_id=f"reconciled-absent:{effect_id}:{record.reservation.attempt_id}:{record.fence}",
            at_ms=record.reconciliation_observed_at, fence=record.fence,
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
        seen_dispatch_intent = False
        seen_acknowledgement = False
        for sequence, payload in matching:
            kind = payload.get("kind")
            if kind == "lease_claimed":
                state = "leased"
            elif kind == "dispatch_intent":
                state = "dispatching"
                seen_dispatch_intent = True
            elif kind in {"dispatch_acknowledged", "provider_acceptance_reconciled"}:
                state = "acknowledged"
                seen_acknowledgement = True
                provider_reference = payload.get("provider_reference")
            elif kind == "final_absence_reconciled":
                state = "retry_authorized"

        # The outbox is the recovery authority for state transitions whose
        # corresponding journal append may have been interrupted. Surface the
        # gap explicitly instead of silently projecting an earlier state.
        has_claim = any(payload.get("kind") == "lease_claimed" for _, payload in matching)
        if record.state in {"leased", "dispatching", "reconciling", "acknowledged", "retry_authorized", "terminal"} and not has_claim:
            state = "lease_claim_unjournaled"
        elif record.state == "reconciling":
            state = "reconciliation_required"
        elif record.state in {"dispatching", "acknowledged", "retry_authorized", "terminal"} and not seen_dispatch_intent and record.dispatch_intent_at is not None:
            state = "dispatch_intent_unjournaled"
        elif record.state == "dispatching" and not seen_dispatch_intent:
            state = "dispatch_intent_unjournaled"
        elif record.state == "acknowledged" and not seen_acknowledgement:
            state = "acknowledgement_unjournaled"
        elif record.state == "retry_authorized" and not any(
                payload.get("kind") == "final_absence_reconciled"
                for _, payload in matching):
            state = "retry_authorization_unjournaled"
        elif record.state == "retry_authorized":
            state = "retry_authorized"
        elif record.state == "terminal":
            state = "terminal"
        return RebuiltEffect(
            effect_id, attempt_id, state,
            matching[-1][0] if matching else 0, len(matching), provider_reference,
        )
