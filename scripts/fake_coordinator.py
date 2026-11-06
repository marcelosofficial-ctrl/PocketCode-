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
    from execution_projection import (
        ExitObservation, LifecycleObservation, ProgramFailureObservation,
        VerdictProjection, project_verdict,
    )
except ModuleNotFoundError:
    from scripts.fake_outbox import FakeOutboxStore, Lease, OutboxConflict
    from scripts.event_journal import AuthenticatedProducer, EventJournal, AppendResult
    from scripts.execution_projection import (
        ExitObservation, LifecycleObservation, ProgramFailureObservation,
        VerdictProjection, project_verdict,
    )


@dataclass(frozen=True)
class AttemptReportState:
    collection_state: str
    cleanup_state: str
    reasons: tuple[str, ...]


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
        bound = {"effect_id": effect_id, "attempt_id": attempt_id}
        if fence is not None:
            bound["fence"] = fence
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
            fence=(self.store.get(effect_id).fence or None),
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
            fence=(self.store.get(effect_id).fence or None),
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

    def _require_live_observation_lease(self, effect_id: str, attempt_id: str,
                                        fence: int, now: int) -> None:
        try:
            record = self.store.get(effect_id, attempt_id)
        except KeyError as exc:
            raise OutboxConflict("observation has no matching reserved attempt") from exc
        if (isinstance(fence, bool) or not isinstance(fence, int) or fence <= 0
                or record.fence != fence
                or record.state not in {"dispatching", "acknowledged"}
                or record.lease_claimed_at is None
                or record.lease_expires_at is None
                or isinstance(now, bool) or not isinstance(now, int)
                or now < record.lease_claimed_at or now >= record.lease_expires_at):
            raise OutboxConflict(
                "worker observation requires the current unexpired dispatch lease; "
                "expired or reconciling attempts must use authoritative reconciliation"
            )

    def record_lifecycle_observation(self, effect_id: str, attempt_id: str, *,
                                    event_id: str, status: str, fence: int,
                                    now: int) -> AppendResult:
        self._require_live_observation_lease(effect_id, attempt_id, fence, now)
        return self._append(
            kind="lifecycle_observation", effect_id=effect_id, attempt_id=attempt_id,
            event_id=event_id, at_ms=now, fence=fence,
            status=status, producer="coordinator",
        )

    def record_exit_observation(self, effect_id: str, attempt_id: str, *,
                                event_id: str, producer: str, kind: str,
                                fence: int, now: int, exit_code=None,
                                signal_number=None) -> AppendResult:
        self._require_live_observation_lease(effect_id, attempt_id, fence, now)
        return self._append(
            kind="exit_observation", effect_id=effect_id, attempt_id=attempt_id,
            event_id=event_id, at_ms=now, fence=fence,
            producer=producer, exit_kind=kind, exit_code=exit_code,
            signal_number=signal_number,
        )

    def record_program_failure_observation(self, effect_id: str, attempt_id: str, *,
                                          event_id: str, producer: str,
                                          confirmed: bool, fence: int,
                                          now: int) -> AppendResult:
        self._require_live_observation_lease(effect_id, attempt_id, fence, now)
        return self._append(
            kind="program_failure_observation", effect_id=effect_id, attempt_id=attempt_id,
            event_id=event_id, at_ms=now, fence=fence,
            producer=producer, confirmed=confirmed,
        )

    def record_collection_observation(self, effect_id: str, attempt_id: str, *,
                                      event_id: str, state: str, fence: int,
                                      now: int) -> AppendResult:
        self._require_live_observation_lease(effect_id, attempt_id, fence, now)
        if state not in {"complete", "degraded", "unknown"}:
            raise OutboxConflict("unknown collection state")
        return self._append(
            kind="collection_observation", effect_id=effect_id, attempt_id=attempt_id,
            event_id=event_id, at_ms=now, fence=fence,
            producer="trusted_collector", state=state,
        )

    def record_cleanup_observation(self, effect_id: str, attempt_id: str, *,
                                   event_id: str, state: str, fence: int,
                                   now: int) -> AppendResult:
        self._require_live_observation_lease(effect_id, attempt_id, fence, now)
        if state not in {"complete", "failed", "not_applicable", "unknown"}:
            raise OutboxConflict("unknown cleanup state")
        return self._append(
            kind="cleanup_observation", effect_id=effect_id, attempt_id=attempt_id,
            event_id=event_id, at_ms=now, fence=fence,
            producer="trusted_cleanup", state=state,
        )

    def project_attempt_report_state(self, effect_id: str, attempt_id: str) -> AttemptReportState:
        record = self.store.get(effect_id, attempt_id)
        matching = [event for event in self.journal.events
                    if event.effect_id == effect_id and event.attempt_id == attempt_id]
        matching.sort(key=lambda event: event.sequence)
        collection = []
        cleanup = []
        reasons = []
        for event in matching:
            try:
                payload = json.loads(event.payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return AttemptReportState("unknown", "unknown", ("accepted_event_payload_invalid",))
            if not isinstance(payload, dict):
                return AttemptReportState("unknown", "unknown", ("accepted_event_payload_not_object",))
            kind = payload.get("kind")
            if kind not in {"collection_observation", "cleanup_observation"}:
                continue
            if event.fence != record.fence:
                reasons.append("stale_fence_report_observation")
                continue
            expected_producer = "trusted_collector" if kind == "collection_observation" else "trusted_cleanup"
            if payload.get("producer") != expected_producer:
                reasons.append("report_observation_producer_mismatch")
                continue
            target = collection if kind == "collection_observation" else cleanup
            target.append(payload.get("state"))
        if len(collection) > 1:
            reasons.append("multiple_collection_observations_require_reconciliation")
        if len(cleanup) > 1:
            reasons.append("multiple_cleanup_observations_require_reconciliation")
        collection_state = collection[0] if len(collection) == 1 and collection[0] in {"complete", "degraded", "unknown"} else "unknown"
        cleanup_state = cleanup[0] if len(cleanup) == 1 and cleanup[0] in {"complete", "failed", "not_applicable", "unknown"} else "unknown"
        return AttemptReportState(collection_state, cleanup_state, tuple(reasons))

    def project_attempt_verdict(self, effect_id: str, attempt_id: str) -> VerdictProjection:
        record = self.store.get(effect_id, attempt_id)
        matching = [event for event in self.journal.events
                    if event.effect_id == effect_id and event.attempt_id == attempt_id]
        matching.sort(key=lambda event: event.sequence)
        lifecycle_items = []
        exit_items = []
        failure_items = []
        for event in matching:
            try:
                payload = json.loads(event.payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return VerdictProjection("INCOMPLETE", "accepted_event_payload_invalid", "unknown")
            if not isinstance(payload, dict):
                return VerdictProjection("INCOMPLETE", "accepted_event_payload_not_object", "unknown")
            kind = payload.get("kind")
            if kind in {"lifecycle_observation", "exit_observation", "program_failure_observation"}:
                if event.fence != record.fence:
                    return VerdictProjection(
                        "INCOMPLETE", "stale_fence_terminal_observation_requires_reconciliation", "unknown"
                    )
            if kind == "lifecycle_observation":
                lifecycle_items.append(LifecycleObservation(
                    attempt_id, payload.get("status"), payload.get("producer"), event.sequence,
                ))
            elif kind == "exit_observation":
                exit_items.append(ExitObservation(
                    attempt_id, payload.get("producer"), payload.get("exit_kind"),
                    event.sequence, payload.get("exit_code"), payload.get("signal_number"),
                ))
            elif kind == "program_failure_observation":
                failure_items.append(ProgramFailureObservation(
                    attempt_id, payload.get("producer"), payload.get("confirmed"), event.sequence,
                ))
        lifecycle = None
        if lifecycle_items:
            nonterminal_rank = {"accepted": 0, "queued": 1, "running": 2}
            terminal = {"succeeded", "program_failed", "timed_out", "cancelled",
                        "rejected", "infrastructure_failed"}
            previous_rank = -1
            terminal_seen = False
            for observation in lifecycle_items:
                status = observation.status
                if not isinstance(status, str):
                    return VerdictProjection("INCOMPLETE", "lifecycle_status_invalid", "unknown")
                if status not in nonterminal_rank and status not in terminal:
                    return VerdictProjection("INCOMPLETE", "lifecycle_status_unknown", status)
                if status in nonterminal_rank:
                    if terminal_seen or nonterminal_rank[status] < previous_rank:
                        return VerdictProjection(
                            "INCOMPLETE", "lifecycle_transition_conflict", status,
                        )
                    previous_rank = nonterminal_rank[status]
                elif status in terminal:
                    if terminal_seen:
                        return VerdictProjection(
                            "INCOMPLETE", "multiple_terminal_lifecycle_observations", status,
                        )
                    terminal_seen = True
            lifecycle = lifecycle_items[-1]
        if len(exit_items) > 1 or len(failure_items) > 1:
            return VerdictProjection("INCOMPLETE", "multiple_execution_observations_require_reconciliation", "unknown")
        return project_verdict(
            attempt_id,
            lifecycle,
            exit_items[0] if exit_items else None,
            failure_items[0] if failure_items else None,
        )

    def create_result_receipt(self, receipt_store, *, effect_id: str, attempt_id: str,
                              revision_key: str, contract_version: str,
                              execution_outcome: Optional[str] = None, collection_state: Optional[str] = None,
                              lifecycle_disposition: str, cleanup_state: Optional[str] = None,
                              artifact_ids: tuple[str, ...], created_at_ms: int,
                              uncertainties: tuple[str, ...] = (),
                              predecessor_receipt_id: Optional[str] = None,
                              revision_reason: Optional[str] = None):
        """Create a receipt whose verdict is derived from accepted attempt evidence."""
        projection = self.project_attempt_verdict(effect_id, attempt_id)
        if execution_outcome is not None and execution_outcome != projection.verdict:
            raise OutboxConflict("caller-supplied verdict conflicts with accepted evidence projection")
        if lifecycle_disposition != projection.execution_status:
            raise OutboxConflict("caller-supplied lifecycle disposition conflicts with accepted evidence projection")
        report_state = self.project_attempt_report_state(effect_id, attempt_id)
        if collection_state is not None and collection_state != report_state.collection_state:
            raise OutboxConflict("caller-supplied collection state conflicts with accepted evidence")
        if cleanup_state is not None and cleanup_state != report_state.cleanup_state:
            raise OutboxConflict("caller-supplied cleanup state conflicts with accepted evidence")
        collection_state = report_state.collection_state
        cleanup_state = report_state.cleanup_state
        execution_outcome = projection.verdict
        lifecycle_disposition = projection.execution_status
        events = [event for event in self.journal.events
                  if event.effect_id == effect_id and event.attempt_id == attempt_id]
        events.sort(key=lambda event: event.sequence)
        if not events:
            raise OutboxConflict("cannot create a receipt without accepted attempt-bound evidence")
        evidence_refs = tuple(
            f"seq:{event.sequence}:{event.source}:{event.producer_event_id}"
            for event in events
        )
        evidence_digests = tuple(event.payload_sha256 for event in events)
        return receipt_store.create_receipt(
            revision_key=revision_key, effect_id=effect_id, attempt_id=attempt_id,
            contract_version=contract_version, execution_outcome=execution_outcome,
            collection_state=collection_state, lifecycle_disposition=lifecycle_disposition,
            cleanup_state=cleanup_state, evidence_refs=evidence_refs,
            evidence_sha256=evidence_digests, artifact_ids=artifact_ids,
            projection_reason=projection.reason,
            uncertainties=uncertainties, created_at_ms=created_at_ms,
            predecessor_receipt_id=predecessor_receipt_id,
            revision_reason=revision_reason,
        )

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
                matching.append((event.sequence, payload, event.fence))
        matching.sort(key=lambda item: item[0])
        state = "reserved"
        provider_reference = None
        for sequence, payload, event_fence in matching:
            kind = payload.get("kind")
            if kind == "lease_claimed":
                state = "leased"
            elif kind == "dispatch_intent":
                state = "dispatching"
            elif kind in {"dispatch_acknowledged", "provider_acceptance_reconciled"}:
                state = "acknowledged"
                provider_reference = payload.get("provider_reference")
            elif kind == "final_absence_reconciled":
                state = "retry_authorized"

        # The outbox is the recovery authority for state transitions whose
        # corresponding journal append may have been interrupted. Surface the
        # gap explicitly instead of silently projecting an earlier state.
        has_claim = any(payload.get("kind") == "lease_claimed" and event_fence == record.fence
                        for _, payload, event_fence in matching)
        if record.state in {"leased", "dispatching", "reconciling", "acknowledged", "retry_authorized", "terminal"} and not has_claim:
            state = "lease_claim_unjournaled"
        elif record.state == "reconciling":
            state = "reconciliation_required"
        elif record.state in {"dispatching", "acknowledged", "retry_authorized", "terminal"} and not any(payload.get("kind") == "dispatch_intent" and event_fence == record.fence
                        for _, payload, event_fence in matching) and record.dispatch_intent_at is not None:
            state = "dispatch_intent_unjournaled"
        elif record.state == "dispatching" and not any(
                payload.get("kind") == "dispatch_intent" and event_fence == record.fence
                for _, payload, event_fence in matching):
            state = "dispatch_intent_unjournaled"
        elif record.state == "acknowledged" and not any(
                payload.get("kind") in {"dispatch_acknowledged", "provider_acceptance_reconciled"}
                and event_fence == record.fence for _, payload, event_fence in matching):
            state = "acknowledgement_unjournaled"
        elif record.state == "retry_authorized" and not any(
                payload.get("kind") == "final_absence_reconciled" and event_fence == record.fence
                for _, payload, event_fence in matching):
            state = "retry_authorization_unjournaled"
        elif record.state == "retry_authorized":
            state = "retry_authorized"
        elif record.state == "terminal":
            state = "terminal"
        return RebuiltEffect(
            effect_id, attempt_id, state,
            matching[-1][0] if matching else 0, len(matching), provider_reference,
        )
