"""Deterministic release-grant transaction and worker-fencing reference model.

This module models commit ordering and atomic state transitions. It is NOT a
database adapter, a threaded race test, durable storage, or a security boundary.
Its purpose is to make the P37/P38 adapter contract executable and CI-checkable.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Optional


class ContractConflict(ValueError):
    """A request conflicts with the currently committed contract state."""


class StaleFence(RuntimeError):
    """A worker no longer owns the current fenced lease."""


@dataclass(frozen=True)
class ReceiptHead:
    effect_id: str
    attempt_id: str
    receipt_id: str
    revision: int
    artifact_id: str
    object_version: str
    artifact_length: int


@dataclass(frozen=True)
class Grant:
    grant_id: str
    tenant_id: str
    principal_id: str
    request_key: str
    intent_fingerprint: str
    head: ReceiptHead
    operation: str
    authorization_id: str
    policy_revision: str
    state: str = "reserved"
    aggregate_version: int = 1
    progress_bytes: int = 0


@dataclass(frozen=True)
class GrantEvent:
    source: str
    event_id: str
    grant_id: str
    aggregate_version: int
    state: str
    payload_sha256: str


@dataclass(frozen=True)
class OutboxItem:
    event: GrantEvent
    delivered: bool = False


@dataclass(frozen=True)
class WorkerLease:
    grant_id: str
    owner: str
    fence: int
    expires_at: int


class ReleaseGrantContractModel:
    """Small executable reference for CAS, idempotency, atomic intent and fences."""

    def __init__(self) -> None:
        self.heads: dict[tuple[str, str], ReceiptHead] = {}
        self.grants: dict[tuple[str, str, str], Grant] = {}
        self.events: dict[tuple[str, str], GrantEvent] = {}
        self.outbox: dict[tuple[str, str], OutboxItem] = {}
        self.fences: dict[str, int] = {}
        self.leases: dict[str, WorkerLease] = {}
        self.consumer_seen: dict[tuple[str, str], str] = {}
        self.consumer_versions: dict[str, int] = {}
        self._next_grant = 1

    def seed_head(self, head: ReceiptHead) -> None:
        key = (head.effect_id, head.attempt_id)
        if key in self.heads:
            raise ContractConflict("receipt head already exists")
        identity_values = (
            head.effect_id, head.attempt_id, head.receipt_id,
            head.artifact_id, head.object_version,
        )
        if (not all(isinstance(value, str) and value.strip() for value in identity_values)
                or isinstance(head.revision, bool) or not isinstance(head.revision, int) or head.revision < 1
                or isinstance(head.artifact_length, bool) or not isinstance(head.artifact_length, int)
                or head.artifact_length < 0):
            raise ValueError("invalid initial receipt head")
        self.heads[key] = head

    def advance_receipt_head(
        self, *, effect_id: str, attempt_id: str, expected_receipt_id: str,
        expected_revision: int, successor_receipt_id: str,
        artifact_id: str, object_version: str, artifact_length: int,
    ) -> ReceiptHead:
        """CAS the stable head. Competing successors from one predecessor cannot both win."""
        if not all(isinstance(value, str) and value.strip() for value in (
            effect_id, attempt_id, expected_receipt_id, successor_receipt_id,
            artifact_id, object_version,
        )):
            raise ValueError("receipt-head identity values must be non-empty strings")
        if (isinstance(expected_revision, bool) or not isinstance(expected_revision, int)
                or expected_revision < 1):
            raise ValueError("expected_revision must be a positive integer")
        key = (effect_id, attempt_id)
        current = self.heads.get(key)
        if current is None:
            raise ContractConflict("receipt head does not exist")
        if (current.receipt_id, current.revision) != (expected_receipt_id, expected_revision):
            raise ContractConflict("receipt head compare-and-swap failed")
        if not successor_receipt_id or successor_receipt_id == current.receipt_id:
            raise ValueError("successor receipt identity must be new and non-empty")
        if isinstance(artifact_length, bool) or not isinstance(artifact_length, int) or artifact_length < 0:
            raise ValueError("artifact_length must be a non-negative integer")
        successor = ReceiptHead(
            effect_id, attempt_id, successor_receipt_id, current.revision + 1,
            artifact_id, object_version, artifact_length,
        )
        self.heads[key] = successor
        return successor

    @staticmethod
    def _fingerprint(
        *, effect_id: str, attempt_id: str, receipt_id: str, revision: int,
        artifact_id: str, object_version: str, operation: str,
    ) -> str:
        # Authorization ID, policy revision, and token expiry are deliberately
        # excluded: they are proof provenance, not stable release intent.
        payload = {
            "effect_id": effect_id,
            "attempt_id": attempt_id,
            "receipt_id": receipt_id,
            "receipt_revision": revision,
            "artifact_id": artifact_id,
            "object_version": object_version,
            "operation": operation,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return sha256(encoded).hexdigest()

    def reserve(
        self, *, tenant_id: str, principal_id: str, request_key: str,
        effect_id: str, attempt_id: str, receipt_id: str, receipt_revision: int,
        artifact_id: str, object_version: str, operation: str,
        auth_tenant_id: str, auth_principal_id: str, auth_allowed: bool,
        auth_operation: str, auth_effect_id: str, auth_attempt_id: str,
        auth_receipt_id: str, auth_receipt_revision: int,
        auth_artifact_id: str, auth_object_version: str,
        authorization_id: str, policy_revision: str,
        fail_at: Optional[str] = None,
    ) -> Grant:
        """Authenticate first; exact replay recovers grant; new intent requires current head.

        fail_at accepts after_grant, after_event, or before_commit. Each injected
        failure leaves grant, event, outbox and sequence unchanged.
        """
        strings = (
            tenant_id, principal_id, request_key, effect_id, attempt_id,
            receipt_id, artifact_id, object_version, operation,
            auth_tenant_id, auth_principal_id, auth_operation,
            auth_effect_id, auth_attempt_id, auth_receipt_id,
            auth_artifact_id, auth_object_version,
            authorization_id, policy_revision,
        )
        if not all(isinstance(value, str) and value.strip() for value in strings):
            raise ValueError("all identity, scope and provenance values must be non-empty strings")
        if auth_allowed is not True or auth_tenant_id != tenant_id or auth_principal_id != principal_id:
            raise ContractConflict("authenticated authorization is not valid for this principal and tenant")
        if operation not in ("download", "share"):
            raise ValueError("operation must be download or share")
        if auth_operation != operation:
            raise ContractConflict("authorization operation scope mismatch")
        if (auth_effect_id, auth_attempt_id, auth_receipt_id, auth_artifact_id, auth_object_version) != (
            effect_id, attempt_id, receipt_id, artifact_id, object_version
        ):
            raise ContractConflict("authorization decision is not bound to this exact release intent")
        if (isinstance(auth_receipt_revision, bool) or not isinstance(auth_receipt_revision, int)
                or auth_receipt_revision != receipt_revision):
            raise ContractConflict("authorization decision receipt revision mismatch")
        if isinstance(receipt_revision, bool) or not isinstance(receipt_revision, int) or receipt_revision < 1:
            raise ValueError("receipt_revision must be a positive integer")

        identity = (tenant_id, principal_id, request_key)
        fingerprint = self._fingerprint(
            effect_id=effect_id, attempt_id=attempt_id, receipt_id=receipt_id,
            revision=receipt_revision, artifact_id=artifact_id,
            object_version=object_version, operation=operation,
        )
        existing = self.grants.get(identity)
        if existing is not None:
            if existing.intent_fingerprint != fingerprint:
                raise ContractConflict("idempotency key already binds different release intent")
            # The first grant and its authorization provenance remain immutable.
            return existing

        head = self.heads.get((effect_id, attempt_id))
        if head is None:
            raise ContractConflict("receipt head not found")
        if (head.receipt_id, head.revision, head.artifact_id, head.object_version) != (
            receipt_id, receipt_revision, artifact_id, object_version
        ):
            raise ContractConflict("stale receipt or artifact object version")

        grant_id = f"release-grant-{self._next_grant}"
        grant = Grant(
            grant_id, tenant_id, principal_id, request_key, fingerprint,
            head, operation, authorization_id, policy_revision,
        )
        event_id = f"{grant_id}:v1"
        payload = json.dumps(
            {"grant_id": grant_id, "version": 1, "state": "reserved"},
            sort_keys=True, separators=(",", ":"),
        ).encode()
        event = GrantEvent(
            source="urn:pocketcode:release-grants", event_id=event_id,
            grant_id=grant_id, aggregate_version=1, state="reserved",
            payload_sha256=sha256(payload).hexdigest(),
        )
        outbox_item = OutboxItem(event)

        # Staged values are not visible until the single commit point below.
        if fail_at == "after_grant":
            raise RuntimeError("injected crash after staged grant insert")
        if fail_at == "after_event":
            raise RuntimeError("injected crash after staged event insert")
        if fail_at == "before_commit":
            raise RuntimeError("injected crash immediately before commit")

        self.grants[identity] = grant
        self.events[(event.source, event.event_id)] = event
        self.outbox[(event.source, event.event_id)] = outbox_item
        self.fences[grant_id] = 0
        self._next_grant += 1
        return grant

    def claim_worker(
        self, *, grant_id: str, owner: str, now: int, lease_seconds: int,
    ) -> WorkerLease:
        if not isinstance(owner, str) or not owner.strip() or isinstance(now, bool) or not isinstance(now, int) or now < 0:
            raise ValueError("valid owner and non-negative integer time required")
        if isinstance(lease_seconds, bool) or not isinstance(lease_seconds, int) or lease_seconds <= 0:
            raise ValueError("lease_seconds must be a positive integer")
        grant = next((g for g in self.grants.values() if g.grant_id == grant_id), None)
        if grant is None:
            raise ContractConflict("grant not found")
        if grant.state not in ("reserved", "transferring"):
            raise ContractConflict("grant is not eligible for a transfer worker")
        current = self.leases.get(grant_id)
        if current is not None and current.expires_at > now:
            raise ContractConflict("worker lease is still active")
        fence = self.fences[grant_id] + 1
        lease = WorkerLease(grant_id, owner, fence, now + lease_seconds)
        self.fences[grant_id] = fence
        self.leases[grant_id] = lease
        return lease

    def record_progress(self, lease: WorkerLease, *, now: int, progress_bytes: int) -> Grant:
        if isinstance(now, bool) or not isinstance(now, int) or now < 0:
            raise ValueError("now must be a non-negative integer")
        current = self.leases.get(lease.grant_id)
        if (current is None or current.fence != lease.fence
                or current.owner != lease.owner or current.expires_at <= now):
            raise StaleFence("worker lease expired or fencing token is stale")
        grant_identity = next(
            (key for key, value in self.grants.items() if value.grant_id == lease.grant_id), None
        )
        if grant_identity is None:
            raise ContractConflict("grant not found")
        grant = self.grants[grant_identity]
        if (isinstance(progress_bytes, bool) or not isinstance(progress_bytes, int)
                or progress_bytes < grant.progress_bytes
                or progress_bytes > grant.head.artifact_length):
            raise ContractConflict("progress must be monotonic and within immutable artifact length")
        updated = Grant(
            grant.grant_id, grant.tenant_id, grant.principal_id, grant.request_key,
            grant.intent_fingerprint, grant.head, grant.operation,
            grant.authorization_id, grant.policy_revision,
            "transferring", grant.aggregate_version + 1, progress_bytes,
        )
        self.grants[grant_identity] = updated
        return updated

    def consume_event(self, event: GrantEvent) -> str:
        """Idempotent, ordered consumer reference; gaps are rejected, not silently skipped."""
        identity = (event.source, event.event_id)
        digest = event.payload_sha256
        previous = self.consumer_seen.get(identity)
        if previous is not None:
            if previous != digest:
                raise ContractConflict("same source/event identity has different payload")
            return "duplicate"
        last = self.consumer_versions.get(event.grant_id, 0)
        if event.aggregate_version > last + 1:
            # A future event is not corrupt merely because its predecessor is
            # delayed. Defer it without recording it as consumed.
            return "deferred_gap"
        if event.aggregate_version <= last:
            raise ContractConflict("unknown or stale aggregate event version")
        self.consumer_seen[identity] = digest
        self.consumer_versions[event.grant_id] = event.aggregate_version
        return "accepted"

    def mark_outbox_delivered(self, source: str, event_id: str) -> None:
        identity = (source, event_id)
        item = self.outbox.get(identity)
        if item is None:
            raise ContractConflict("outbox event not found")
        self.outbox[identity] = OutboxItem(item.event, True)
