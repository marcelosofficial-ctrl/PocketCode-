"""Fail-closed decision helper for ambiguous provider dispatch acknowledgement.

This is a pure design/test aid, not a provider adapter or durable outbox.
The caller must authenticate provider responses, verify account/endpoint scope,
load the original persisted request, and enforce its real API contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DispatchContext:
    effect_id: str
    attempt_id: str
    request_fingerprint: str
    endpoint: str
    account_scope: str
    idempotency_token: Optional[str]
    provider_id: str
    api_version: str
    region_scope: str
    state: str  # reserved, sent_unacknowledged, acknowledged, running, terminal


@dataclass(frozen=True)
class ProviderLookup:
    outcome: str  # found, not_found, unknown
    authoritative: bool = False
    effect_id: Optional[str] = None
    attempt_id: Optional[str] = None
    request_fingerprint: Optional[str] = None
    endpoint: Optional[str] = None
    account_scope: Optional[str] = None
    idempotency_token: Optional[str] = None
    provider_id: Optional[str] = None
    api_version: Optional[str] = None
    region_scope: Optional[str] = None


@dataclass(frozen=True)
class IdempotencyContract:
    documented: bool = False
    endpoint: Optional[str] = None
    account_scope: Optional[str] = None
    idempotency_token: Optional[str] = None
    fingerprint: Optional[str] = None
    provider_id: Optional[str] = None
    api_version: Optional[str] = None
    region_scope: Optional[str] = None
    retention_active: bool = False
    same_request_replay_deduplicated: bool = False
    changed_parameters_rejected: bool = False


@dataclass(frozen=True)
class DispatchDecision:
    action: str
    reason: str
    reuse_effect_id: bool
    reuse_attempt_id: bool
    reuse_request_fingerprint: bool
    reuse_idempotency_token: bool


def _valid_context(context: DispatchContext) -> bool:
    required = (
        context.effect_id, context.attempt_id, context.request_fingerprint,
        context.endpoint, context.account_scope, context.provider_id,
        context.api_version, context.region_scope,
    )
    token_valid = (context.idempotency_token is None or
                   (isinstance(context.idempotency_token, str) and bool(context.idempotency_token.strip())))
    return all(isinstance(v, str) and bool(v.strip()) for v in required) and token_valid and context.state in {
        "reserved", "sent_unacknowledged", "acknowledged", "running", "terminal"
    }


def _decision(action: str, reason: str) -> DispatchDecision:
    # Every branch preserves the reserved semantic operation identity and exact
    # request. A human-authorized new execution is a different operation.
    return DispatchDecision(action, reason, True, True, True, True)


def _contract_matches(context: DispatchContext, contract: Optional[IdempotencyContract]) -> bool:
    if not isinstance(contract, IdempotencyContract):
        return False
    return all((
        contract.documented is True,
        contract.endpoint == context.endpoint,
        contract.account_scope == context.account_scope,
        context.idempotency_token is not None,
        contract.idempotency_token == context.idempotency_token,
        contract.fingerprint == context.request_fingerprint,
        contract.provider_id == context.provider_id,
        contract.api_version == context.api_version,
        contract.region_scope == context.region_scope,
        contract.retention_active is True,
        contract.same_request_replay_deduplicated is True,
        contract.changed_parameters_rejected is True,
    ))


def decide_ambiguous_dispatch(
    context: DispatchContext,
    lookup: Optional[ProviderLookup],
    contract: Optional[IdempotencyContract] = None,
) -> DispatchDecision:
    """Return one safe next action without generating IDs or changing state.

    Actions: dispatch_first, adopt_existing, retry_same_attempt,
    poll_existing, hold_unknown, conflict, do_not_replay.
    """
    if not isinstance(context, DispatchContext) or not _valid_context(context):
        return _decision("conflict", "dispatch_context_invalid")

    if context.state == "reserved":
        if lookup is not None:
            return _decision("conflict", "lookup_supplied_before_any_dispatch")
        return _decision("dispatch_first", "reserved_before_first_send")

    if context.state in {"acknowledged", "running"}:
        return _decision("poll_existing", "provider_acknowledgement_already_recorded")

    if context.state == "terminal":
        return _decision("do_not_replay", "attempt_already_terminal_new_attempt_requires_new_authorization")

    if lookup is not None:
        if not isinstance(lookup, ProviderLookup) or lookup.outcome not in {"found", "not_found", "unknown"}:
            return _decision("hold_unknown", "provider_lookup_invalid")

        if lookup.outcome in {"found", "not_found"}:
            if lookup.authoritative is not True:
                return _decision("hold_unknown", "provider_lookup_not_authoritative")
            expected = (
                lookup.effect_id == context.effect_id,
                lookup.attempt_id == context.attempt_id,
                lookup.request_fingerprint == context.request_fingerprint,
                lookup.endpoint == context.endpoint,
                lookup.account_scope == context.account_scope,
                lookup.idempotency_token == context.idempotency_token,
                lookup.provider_id == context.provider_id,
                lookup.api_version == context.api_version,
                lookup.region_scope == context.region_scope,
            )
            if not all(expected):
                return _decision("conflict", "provider_lookup_identity_or_request_mismatch")
            if lookup.outcome == "found":
                return _decision("adopt_existing", "authoritative_lookup_matches_exact_effect_attempt_and_request")
            return _decision("retry_same_attempt", "authoritative_non_acceptance_allows_same_attempt_retry")

    if _contract_matches(context, contract):
        return _decision("retry_same_attempt", "documented_exact_scope_idempotency_allows_same_request_replay")

    if lookup is None:
        return _decision("hold_unknown", "ambiguous_acknowledgement_without_lookup_or_exact_idempotency_contract")
    if lookup.outcome == "not_found":
        return _decision("hold_unknown", "non_authoritative_not_found_does_not_prove_non_acceptance")
    return _decision("hold_unknown", "lookup_unknown_and_no_exact_idempotency_contract")
