"""Immutable result receipt and artifact-release conformance model.

This is an in-memory research model. It is not durable storage, a signing
system, malware scanner, provider authenticator, or production release service.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Optional


class ReceiptConflict(ValueError):
    pass


@dataclass(frozen=True)
class ArtifactInput:
    artifact_id: str
    logical_name: str
    media_type: str
    attempt_id: str
    content: bytes
    write_complete: bool
    reported_sha256: Optional[str] = None


@dataclass(frozen=True)
class ArtifactManifestEntry:
    artifact_id: str
    object_version: str
    logical_name: str
    media_type: str
    attempt_id: str
    byte_length: int
    sha256: str
    integrity_state: str
    quarantined: bool


@dataclass(frozen=True)
class ResultReceipt:
    receipt_id: str
    revision_key: str
    version: int
    effect_id: str
    attempt_id: str
    contract_version: str
    execution_outcome: str
    projection_reason: Optional[str]
    collection_state: str
    lifecycle_disposition: str
    cleanup_state: str
    evidence_refs: tuple[str, ...]
    evidence_sha256: tuple[str, ...]
    artifact_manifest: tuple[ArtifactManifestEntry, ...]
    uncertainties: tuple[str, ...]
    predecessor_receipt_id: Optional[str]
    revision_reason: Optional[str]
    created_at_ms: int
    receipt_sha256: str


@dataclass(frozen=True)
class ReleaseAuthorization:
    authorization_id: str
    policy_revision: str
    principal_id: str
    tenant_id: str
    receipt_id: str
    artifact_id: str
    object_version: str
    attempt_id: str
    current_attempt_id: str
    scope: str
    authorized: bool
    revoked: bool
    observed_at_ms: int
    expires_at_ms: int


@dataclass(frozen=True)
class ReleaseResult:
    disposition: str
    artifact_id: str
    object_version: Optional[str]
    content: Optional[bytes]
    authorization_id: Optional[str]


@dataclass(frozen=True)
class PublicationAttempt:
    receipt_id: str
    destination: str
    attempt_number: int
    disposition: str
    observed_at_ms: int


class ResultReceiptStore:
    """Append-only receipts, staged artifact bytes and report-publication attempts."""

    _SHA256 = re.compile(r"^[0-9a-f]{64}$")
    _SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")

    def __init__(self) -> None:
        self._artifacts: dict[str, tuple[ArtifactManifestEntry, bytes]] = {}
        self._receipts: list[ResultReceipt] = []
        self._receipt_by_revision: dict[str, ResultReceipt] = {}
        self._revision_fingerprints: dict[str, str] = {}
        self._publication_attempts: list[PublicationAttempt] = []

    @property
    def receipts(self) -> tuple[ResultReceipt, ...]:
        return tuple(self._receipts)

    @property
    def artifacts(self) -> tuple[ArtifactManifestEntry, ...]:
        return tuple(entry for entry, _ in self._artifacts.values())

    @property
    def publication_attempts(self) -> tuple[PublicationAttempt, ...]:
        return tuple(self._publication_attempts)

    def stage_artifact(self, item: ArtifactInput) -> ArtifactManifestEntry:
        if not isinstance(item, ArtifactInput):
            raise ReceiptConflict("artifact input must be typed")
        if not all(isinstance(v, str) and v.strip() for v in
                   (item.artifact_id, item.logical_name, item.media_type, item.attempt_id)):
            raise ReceiptConflict("artifact identity and media type are required")
        if not self._SAFE_NAME.fullmatch(item.logical_name) or item.logical_name in {".", ".."}:
            raise ReceiptConflict("artifact logical name must be a safe basename")
        if not isinstance(item.content, bytes):
            raise ReceiptConflict("artifact content must be immutable bytes")
        if type(item.write_complete) is not bool:
            raise ReceiptConflict("write_complete must be a literal boolean")
        digest = sha256(item.content).hexdigest()
        if item.reported_sha256 is not None and (
            not isinstance(item.reported_sha256, str)
            or not self._SHA256.fullmatch(item.reported_sha256)
        ):
            raise ReceiptConflict("reported SHA-256 must be 64 lowercase hex characters")
        integrity = "verified"
        quarantined = False
        if not item.write_complete:
            integrity, quarantined = "partial_write", True
        elif item.reported_sha256 is not None and item.reported_sha256 != digest:
            integrity, quarantined = "digest_mismatch", True
        entry = ArtifactManifestEntry(
            item.artifact_id, f"{item.artifact_id}:v1", item.logical_name,
            item.media_type, item.attempt_id, len(item.content), digest,
            integrity, quarantined,
        )
        prior = self._artifacts.get(item.artifact_id)
        if prior is not None:
            if prior == (entry, item.content):
                return prior[0]
            raise ReceiptConflict("artifact identity is immutable and cannot be overwritten")
        self._artifacts[item.artifact_id] = (entry, bytes(item.content))
        return entry

    def create_receipt(
        self, *, revision_key: str, effect_id: str, attempt_id: str,
        contract_version: str, execution_outcome: str, collection_state: str,
        lifecycle_disposition: str, cleanup_state: str,
        evidence_refs: tuple[str, ...], evidence_sha256: tuple[str, ...],
        artifact_ids: tuple[str, ...], uncertainties: tuple[str, ...] = (),
        created_at_ms: int, predecessor_receipt_id: Optional[str] = None,
        revision_reason: Optional[str] = None,
        projection_reason: Optional[str] = None,
    ) -> ResultReceipt:
        identity = (revision_key, effect_id, attempt_id, contract_version,
                    execution_outcome, collection_state, lifecycle_disposition,
                    cleanup_state, evidence_refs, evidence_sha256, artifact_ids,
                    uncertainties, created_at_ms, predecessor_receipt_id, revision_reason)
        if not all(isinstance(v, str) and v.strip() for v in
                   (revision_key, effect_id, attempt_id, contract_version,
                    execution_outcome, collection_state, lifecycle_disposition, cleanup_state)):
            raise ReceiptConflict("receipt identity and projection fields are required")
        if isinstance(created_at_ms, bool) or not isinstance(created_at_ms, int) or created_at_ms < 0:
            raise ReceiptConflict("receipt timestamp must be a non-negative integer")
        if not isinstance(evidence_refs, tuple) or not isinstance(evidence_sha256, tuple):
            raise ReceiptConflict("evidence references and digests must be immutable tuples")
        if len(evidence_refs) != len(evidence_sha256):
            raise ReceiptConflict("each evidence reference requires exactly one digest")
        if any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
            raise ReceiptConflict("evidence references must be non-empty strings")
        if any(not isinstance(digest, str) or not self._SHA256.fullmatch(digest)
               for digest in evidence_sha256):
            raise ReceiptConflict("evidence digests must be lowercase SHA-256 hex")
        if not isinstance(artifact_ids, tuple) or not isinstance(uncertainties, tuple):
            raise ReceiptConflict("artifact IDs and uncertainties must be immutable tuples")
        if any(not isinstance(value, str) or not value.strip() for value in artifact_ids):
            raise ReceiptConflict("artifact IDs must be non-empty strings")
        if len(set(artifact_ids)) != len(artifact_ids):
            raise ReceiptConflict("receipt artifact manifest cannot repeat artifact IDs")
        if len(set(evidence_refs)) != len(evidence_refs):
            raise ReceiptConflict("receipt evidence references cannot be repeated")
        if predecessor_receipt_id is not None and (
            not isinstance(predecessor_receipt_id, str) or not predecessor_receipt_id.strip()
        ):
            raise ReceiptConflict("predecessor receipt ID must be a non-empty string")
        if predecessor_receipt_id is not None and revision_reason is None:
            raise ReceiptConflict("a receipt revision must state why it supersedes its predecessor")
        if any(not isinstance(value, str) or not value.strip() for value in uncertainties):
            raise ReceiptConflict("uncertainties must be non-empty strings")
        if revision_reason is not None and (
            not isinstance(revision_reason, str) or not revision_reason.strip()
        ):
            raise ReceiptConflict("revision reason cannot be empty")
        if projection_reason is not None and (
            not isinstance(projection_reason, str) or not projection_reason.strip()
        ):
            raise ReceiptConflict("projection reason cannot be empty")
        if predecessor_receipt_id is not None and predecessor_receipt_id not in {
            receipt.receipt_id for receipt in self._receipts
        }:
            raise ReceiptConflict("predecessor receipt must already exist")

        manifest = []
        for artifact_id in artifact_ids:
            if artifact_id not in self._artifacts:
                raise ReceiptConflict("receipt references an unknown artifact")
            entry = self._artifacts[artifact_id][0]
            if entry.attempt_id != attempt_id:
                raise ReceiptConflict("artifact attempt does not match receipt attempt")
            manifest.append(entry)

        canonical = {
            "revision_key": revision_key, "effect_id": effect_id,
            "attempt_id": attempt_id, "contract_version": contract_version,
            "execution_outcome": execution_outcome, "collection_state": collection_state,
            "lifecycle_disposition": lifecycle_disposition, "cleanup_state": cleanup_state,
            "evidence_refs": list(evidence_refs), "evidence_sha256": list(evidence_sha256),
            "artifact_manifest": [entry.__dict__ for entry in manifest],
            "uncertainties": list(uncertainties), "created_at_ms": created_at_ms,
            "predecessor_receipt_id": predecessor_receipt_id,
            "revision_reason": revision_reason,
            "projection_reason": projection_reason,
        }
        fingerprint = sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        prior = self._receipt_by_revision.get(revision_key)
        if prior is not None:
            if self._revision_fingerprints[revision_key] == fingerprint:
                return prior
            raise ReceiptConflict("revision key already binds a different immutable receipt")

        history = [receipt for receipt in self._receipts
                   if receipt.effect_id == effect_id and receipt.attempt_id == attempt_id]
        latest = max(history, key=lambda receipt: receipt.version) if history else None
        if latest is None and predecessor_receipt_id is not None:
            raise ReceiptConflict("first receipt version cannot name a predecessor")
        if latest is not None and predecessor_receipt_id != latest.receipt_id:
            raise ReceiptConflict("new receipt version must extend the latest version without forking")
        if predecessor_receipt_id is not None:
            predecessor = next(receipt for receipt in self._receipts
                               if receipt.receipt_id == predecessor_receipt_id)
            if predecessor.effect_id != effect_id or predecessor.attempt_id != attempt_id:
                raise ReceiptConflict("predecessor must belong to the same effect and attempt")
        version = latest.version + 1 if latest is not None else 1
        receipt_id = f"receipt-{len(self._receipts) + 1}"
        receipt = ResultReceipt(
            receipt_id, revision_key, version, effect_id, attempt_id, contract_version,
            execution_outcome, projection_reason, collection_state, lifecycle_disposition,
            cleanup_state, evidence_refs, evidence_sha256, tuple(manifest), uncertainties,
            predecessor_receipt_id, revision_reason, created_at_ms, fingerprint,
        )
        self._receipts.append(receipt)
        self._receipt_by_revision[revision_key] = receipt
        self._revision_fingerprints[revision_key] = fingerprint
        return receipt

    def release_artifact(self, artifact_id: str, authorization: ReleaseAuthorization, *,
                         receipt_id: str, now_ms: int, operation: str = "download") -> ReleaseResult:
        """Revalidate receipt membership, object identity and current authorization per request.

        Authorization fields are still caller-supplied model inputs, not proof that
        a real policy authority authenticated the principal or checked revocation.
        """
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            return ReleaseResult("denied_invalid_artifact_id", str(artifact_id), None, None, None)
        stored = self._artifacts.get(artifact_id)
        if stored is None:
            return ReleaseResult("not_found", artifact_id, None, None, None)
        entry, content = stored
        if not isinstance(authorization, ReleaseAuthorization):
            return ReleaseResult("denied_missing_authorization", artifact_id, None, None, None)
        string_fields = (
            authorization.authorization_id, authorization.policy_revision,
            authorization.principal_id, authorization.tenant_id,
            authorization.receipt_id, authorization.artifact_id,
            authorization.object_version, authorization.attempt_id,
            authorization.current_attempt_id, authorization.scope,
        )
        if not all(isinstance(value, str) and value.strip() for value in string_fields):
            return ReleaseResult("denied_invalid_authorization", artifact_id, None, None,
                                 authorization.authorization_id if isinstance(authorization.authorization_id, str) else None)
        if (isinstance(now_ms, bool) or not isinstance(now_ms, int) or now_ms < 0
                or isinstance(authorization.observed_at_ms, bool)
                or not isinstance(authorization.observed_at_ms, int)
                or authorization.observed_at_ms < 0
                or isinstance(authorization.expires_at_ms, bool)
                or not isinstance(authorization.expires_at_ms, int)
                or authorization.expires_at_ms < 0):
            return ReleaseResult("denied_invalid_authorization", artifact_id, None, None,
                                 authorization.authorization_id)
        if (authorization.receipt_id != receipt_id
                or authorization.artifact_id != artifact_id
                or authorization.object_version != entry.object_version
                or authorization.attempt_id != entry.attempt_id
                or authorization.current_attempt_id != entry.attempt_id):
            return ReleaseResult("denied_stale_or_mismatched_attempt", artifact_id, None, None,
                                 authorization.authorization_id)
        receipt = next((item for item in self._receipts if item.receipt_id == receipt_id), None)
        if receipt is None or receipt.attempt_id != entry.attempt_id or not any(
            manifest.artifact_id == artifact_id and manifest.object_version == entry.object_version
            for manifest in receipt.artifact_manifest
        ):
            return ReleaseResult("denied_artifact_not_in_receipt", artifact_id, None, None,
                                 authorization.authorization_id)
        if operation not in {"download", "share"} or authorization.scope != f"artifact:{operation}":
            return ReleaseResult("denied_scope_mismatch", artifact_id, None, None,
                                 authorization.authorization_id)
        if type(authorization.authorized) is not bool or not authorization.authorized:
            return ReleaseResult("denied_by_current_authorization", artifact_id, None, None,
                                 authorization.authorization_id)
        if type(authorization.revoked) is not bool or authorization.revoked:
            return ReleaseResult("denied_revoked_authorization", artifact_id, None, None,
                                 authorization.authorization_id)
        if authorization.observed_at_ms > now_ms or now_ms >= authorization.expires_at_ms:
            return ReleaseResult("denied_expired_authorization", artifact_id, None, None,
                                 authorization.authorization_id)
        if entry.quarantined or entry.integrity_state != "verified":
            return ReleaseResult("denied_quarantined_artifact", artifact_id, None, None,
                                 authorization.authorization_id)
        if sha256(content).hexdigest() != entry.sha256 or len(content) != entry.byte_length:
            return ReleaseResult("denied_integrity_changed", artifact_id, None, None,
                                 authorization.authorization_id)
        return ReleaseResult("released", artifact_id, entry.object_version, bytes(content),
                             authorization.authorization_id)

    def publish_report(self, receipt_id: str, destination: str, *,
                       success: bool, observed_at_ms: int) -> PublicationAttempt:
        """Record a copy/share attempt for the same immutable receipt, never rerun work."""
        if not isinstance(receipt_id, str) or not receipt_id.strip():
            raise ReceiptConflict("receipt ID must be a non-empty string")
        if receipt_id not in {receipt.receipt_id for receipt in self._receipts}:
            raise ReceiptConflict("cannot publish an unknown receipt")
        if not isinstance(destination, str) or not destination.strip():
            raise ReceiptConflict("publication destination is required")
        if type(success) is not bool:
            raise ReceiptConflict("publication success must be a literal boolean")
        if isinstance(observed_at_ms, bool) or not isinstance(observed_at_ms, int) or observed_at_ms < 0:
            raise ReceiptConflict("publication observation time must be non-negative integer")
        attempt_number = 1 + sum(
            1 for item in self._publication_attempts
            if item.receipt_id == receipt_id and item.destination == destination
        )
        item = PublicationAttempt(
            receipt_id, destination, attempt_number,
            "published" if success else "failed", observed_at_ms,
        )
        self._publication_attempts.append(item)
        return item
