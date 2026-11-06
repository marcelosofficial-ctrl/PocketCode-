"""Deterministic in-memory outbox model for PocketCode recovery tests.

This is a fake-store conformance model, NOT durable storage, a dispatcher,
a provider adapter, or a production security boundary. All methods are
synchronous so tests can explore transaction and crash-point semantics.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional


class OutboxConflict(ValueError):
    pass


class StaleLease(RuntimeError):
    pass


@dataclass(frozen=True)
class Reservation:
    effect_id: str
    attempt_id: str
    request_fingerprint: str
    request_bytes: bytes
    sequence: int
    created_at_ms: Optional[int] = None


@dataclass(frozen=True)
class Lease:
    effect_id: str
    attempt_id: str
    owner: str
    fence: int
    expires_at: int


@dataclass(frozen=True)
class OutboxRecord:
    reservation: Reservation
    state: str = "pending"  # pending, leased, dispatching, reconciling, acknowledged
    lease_owner: Optional[str] = None
    lease_expires_at: Optional[int] = None
    fence: int = 0
    provider_reference: Optional[str] = None
    acknowledged_at: Optional[int] = None
    acknowledgement_source: Optional[str] = None
    reconciliation_observed_at: Optional[int] = None
    reconciliation_outcome: Optional[str] = None
    lease_claimed_at: Optional[int] = None
    dispatch_intent_at: Optional[int] = None


@dataclass(frozen=True)
class DeliveryResult:
    disposition: str  # accepted, duplicate, conflict
    effect_id: str
    request_fingerprint: str
    provider_reference: str


class FakeOutboxStore:
    """In-memory model with explicit transaction boundaries and fencing."""

    def __init__(self) -> None:
        self._records: dict[tuple[str, str], OutboxRecord] = {}
        self._active_attempt: dict[str, str] = {}
        self._sequence = 0
        self._consumer_receipts: dict[str, DeliveryResult] = {}

    @property
    def records(self) -> tuple[OutboxRecord, ...]:
        return tuple(self._records.values())

    def get(self, effect_id: str, attempt_id: Optional[str] = None) -> OutboxRecord:
        selected = attempt_id or self._active_attempt[effect_id]
        return self._records[(effect_id, selected)]

    def reserve(
        self, effect_id: str, attempt_id: str, request_fingerprint: str,
        request_bytes: bytes, *, fail_before_commit: bool = False,
        new_attempt_authorized: bool = False, created_at_ms: Optional[int] = None,
    ) -> Reservation:
        """Atomically add reservation + dispatch intent, or add neither."""
        if not all(isinstance(v, str) and v.strip() for v in
                   (effect_id, attempt_id, request_fingerprint)):
            raise ValueError("reservation identity fields must be non-empty strings")
        if not isinstance(request_bytes, bytes) or not request_bytes:
            raise ValueError("request_bytes must be non-empty immutable bytes")
        if created_at_ms is not None and (isinstance(created_at_ms, bool) or not isinstance(created_at_ms, int) or created_at_ms < 0):
            raise ValueError("created_at_ms must be a non-negative integer when supplied")
        key = (effect_id, attempt_id)
        existing = self._records.get(key)
        if existing is not None:
            old = existing.reservation
            if (old.request_fingerprint, old.request_bytes) == (request_fingerprint, request_bytes):
                return old
            raise OutboxConflict("attempt identity already reserved for a different request")
        previous_attempt = self._active_attempt.get(effect_id)
        if previous_attempt is not None:
            previous = self._records[(effect_id, previous_attempt)]
            if previous.state != "terminal" or new_attempt_authorized is not True:
                raise OutboxConflict("new attempt requires prior terminal state and explicit authorization")

        # Prepare all values before the commit point. No store mutation occurs
        # until after the injected crash point.
        reservation = Reservation(
            effect_id, attempt_id, request_fingerprint, bytes(request_bytes),
            self._sequence + 1, created_at_ms,
        )
        record = OutboxRecord(reservation=reservation)
        if fail_before_commit:
            raise RuntimeError("simulated crash before atomic commit")
        self._records[key] = record
        self._active_attempt[effect_id] = attempt_id
        self._sequence = reservation.sequence
        return reservation

    def claim(self, effect_id: str, owner: str, *, now: int, lease_seconds: int) -> Lease:
        if (not isinstance(owner, str) or not owner.strip()
                or isinstance(now, bool) or not isinstance(now, int) or now < 0
                or isinstance(lease_seconds, bool) or not isinstance(lease_seconds, int)
                or lease_seconds <= 0):
            raise ValueError("valid owner, non-negative integer time and positive integer lease required")
        record = self.get(effect_id)
        if record.state in {"dispatching", "reconciling", "acknowledged", "terminal"}:
            raise OutboxConflict("record is not eligible for dispatch claim")
        if record.state == "leased" and record.lease_expires_at is not None and now < record.lease_expires_at:
            raise OutboxConflict("active lease cannot be stolen")
        fence = record.fence + 1
        expires = now + lease_seconds
        self._records[(effect_id, record.reservation.attempt_id)] = replace(
            record, state="leased", lease_owner=owner,
            lease_expires_at=expires, fence=fence, lease_claimed_at=now,
        )
        return Lease(effect_id, record.reservation.attempt_id, owner, fence, expires)

    def _require_current_lease(self, lease: Lease, *, now: int) -> OutboxRecord:
        if (not isinstance(lease, Lease) or isinstance(now, bool)
                or not isinstance(now, int) or now < 0):
            raise StaleLease("lease token or observation time is invalid")
        record = self._records.get((lease.effect_id, lease.attempt_id))
        if (record is None or record.reservation.attempt_id != lease.attempt_id
                or record.lease_owner != lease.owner or record.fence != lease.fence
                or record.lease_expires_at is None or now >= record.lease_expires_at
                or record.state != "leased"):
            raise StaleLease("lease expired, fenced, or no longer dispatchable")
        return record

    def mark_dispatching(self, lease: Lease, *, now: int) -> None:
        """Persist send-intent before external I/O; expiry thereafter is ambiguous."""
        record = self._require_current_lease(lease, now=now)
        self._records[(lease.effect_id, lease.attempt_id)] = replace(record, state="dispatching", dispatch_intent_at=now)

    def recover_expired(self, effect_id: str, *, now: int) -> str:
        """Recover a crashed worker without confusing pre-send and post-intent."""
        if isinstance(now, bool) or not isinstance(now, int) or now < 0:
            raise ValueError("now must be a non-negative integer")
        record = self.get(effect_id)
        key = (effect_id, record.reservation.attempt_id)
        if record.state == "leased" and record.lease_expires_at is not None and now >= record.lease_expires_at:
            self._records[key] = replace(
                record, state="pending", lease_owner=None, lease_expires_at=None,
            )
            return "safe_to_reclaim_before_send"
        if record.state == "dispatching" and record.lease_expires_at is not None and now >= record.lease_expires_at:
            self._records[key] = replace(
                record, state="reconciling", lease_owner=None, lease_expires_at=None,
            )
            return "reconcile_before_any_retry"
        return "no_recovery_transition"

    def acknowledge(self, lease: Lease, provider_reference: str, *, now: int) -> None:
        record = self._records.get((lease.effect_id, lease.attempt_id))
        if (record is None or record.state != "dispatching"
                or record.reservation.attempt_id != lease.attempt_id
                or record.fence != lease.fence or record.lease_owner != lease.owner
                or record.lease_expires_at is None or isinstance(now, bool)
                or not isinstance(now, int) or now >= record.lease_expires_at):
            raise StaleLease("acknowledgement is stale or no longer authoritative")
        if not isinstance(provider_reference, str) or not provider_reference.strip():
            raise ValueError("provider reference must be non-empty")
        self._records[(lease.effect_id, lease.attempt_id)] = replace(
            record, state="acknowledged", provider_reference=provider_reference,
            acknowledged_at=now, acknowledgement_source="dispatch",
        )

    def resolve_reconciliation(
        self, effect_id: str, *, outcome: str, exact_identity_match: bool,
        authoritative: bool, absence_final: bool = False,
        provider_reference: Optional[str] = None, now: Optional[int] = None,
    ) -> str:
        """Apply a supplied reconciliation result; caller trust is NOT verified here."""
        record = self.get(effect_id)
        key = (effect_id, record.reservation.attempt_id)
        if record.state != "reconciling":
            raise OutboxConflict("record is not awaiting reconciliation")
        if exact_identity_match is not True or authoritative is not True:
            return "hold_unknown"
        if outcome == "found" and isinstance(provider_reference, str) and provider_reference.strip():
            if now is not None and (isinstance(now, bool) or not isinstance(now, int) or now < 0):
                raise ValueError("reconciliation observation time must be a non-negative integer")
            self._records[key] = replace(
                record, state="acknowledged", provider_reference=provider_reference,
                acknowledged_at=now, acknowledgement_source="reconciliation",
                reconciliation_observed_at=now, reconciliation_outcome="found",
            )
            return "adopt_existing"
        if outcome == "not_found" and absence_final is True:
            # This model returns to pending only after explicitly final exact-scope non-acceptance.
            if now is not None and (isinstance(now, bool) or not isinstance(now, int) or now < 0):
                raise ValueError("reconciliation observation time is required for final absence")
            self._records[key] = replace(
                record, state="retry_authorized", lease_owner=None, lease_expires_at=None,
                reconciliation_observed_at=now, reconciliation_outcome="final_absence",
            )
            return "safe_to_retry_same_attempt"
        return "hold_unknown"

    def mark_terminal(self, effect_id: str, *, attempt_id: Optional[str] = None) -> None:
        """Close an attempt; a later attempt still requires explicit authorization."""
        record = self.get(effect_id, attempt_id)
        if record.state not in {"acknowledged", "pending", "retry_authorized"}:
            raise OutboxConflict("only acknowledged or reconciled-pending attempts can close")
        key = (effect_id, record.reservation.attempt_id)
        self._records[key] = replace(
            record, state="terminal", lease_owner=None, lease_expires_at=None,
        )

    def consume(self, effect_id: str, request_fingerprint: str,
                provider_reference: str) -> DeliveryResult:
        """Fake idempotent receiver keyed by EffectId and exact request digest."""
        if not all(isinstance(v, str) and v.strip() for v in
                   (effect_id, request_fingerprint, provider_reference)):
            raise ValueError("consumer identity fields must be non-empty strings")
        prior = self._consumer_receipts.get(effect_id)
        if prior is not None:
            if prior.request_fingerprint != request_fingerprint:
                return DeliveryResult("conflict", effect_id, request_fingerprint, prior.provider_reference)
            return DeliveryResult("duplicate", effect_id, request_fingerprint, prior.provider_reference)
        receipt = DeliveryResult("accepted", effect_id, request_fingerprint, provider_reference)
        self._consumer_receipts[effect_id] = receipt
        return receipt
