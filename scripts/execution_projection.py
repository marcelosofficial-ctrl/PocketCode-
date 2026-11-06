"""Pure, fail-closed verdict projection for typed execution observations.

This is a design-stage helper, not an authenticated coordinator or runner.
Callers must authenticate producers, authorize the attempt, deduplicate events,
validate policy, and persist observations before calling this function.
The helper deliberately does not infer a child exit from wrapper or embedded
interpreter results.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

KNOWN_LIFECYCLE_STATUSES = frozenset({
    "accepted", "queued", "running", "succeeded", "program_failed",
    "timed_out", "cancelled", "rejected", "infrastructure_failed",
})
CHILD_EXIT_PRODUCERS = frozenset({"direct_child_wait", "provider_child_wait"})
WRAPPER_PRODUCERS = frozenset({"shell_wrapper", "supervisor"})
FAILURE_PRODUCERS = frozenset({"trusted_runtime", "provider_runtime"})
NON_SUCCESS_TERMINAL_STATES = frozenset({
    "timed_out", "cancelled", "rejected", "infrastructure_failed",
})


@dataclass(frozen=True)
class LifecycleObservation:
    attempt_id: str
    status: str
    producer: str
    sequence: int


@dataclass(frozen=True)
class ExitObservation:
    attempt_id: str
    producer: str
    kind: str
    sequence: int
    exit_code: Optional[int] = None
    signal_number: Optional[int] = None


@dataclass(frozen=True)
class ProgramFailureObservation:
    attempt_id: str
    producer: str
    confirmed: bool
    sequence: int


@dataclass(frozen=True)
class VerdictProjection:
    verdict: str
    reason: str
    execution_status: str
    child_exit_code: Optional[int] = None


def _valid_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_sequence(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _valid_code(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _incomplete(reason: str, status: str = "unknown") -> VerdictProjection:
    return VerdictProjection("INCOMPLETE", reason, status, None)


def project_verdict(
    expected_attempt_id: str,
    lifecycle: Optional[LifecycleObservation],
    exit_observation: Optional[ExitObservation] = None,
    program_failure: Optional[ProgramFailureObservation] = None,
) -> VerdictProjection:
    """Project only explicitly typed, attempt-bound observations.

    PASS requires coordinator lifecycle=succeeded and a direct child's natural
    exit 0. FAIL requires coordinator lifecycle=program_failed, a direct child's
    natural nonzero exit, or an explicit trusted runtime failure, without a
    contradictory success/timeout state.
    Wrapper exits, signal numbers, embedded SystemExit requests, and missing or
    contradictory evidence never become child exit codes.
    """
    if not isinstance(expected_attempt_id, str) or not expected_attempt_id.strip():
        return _incomplete("expected_attempt_id_missing")

    status = "unknown"
    if lifecycle is not None:
        if not isinstance(lifecycle, LifecycleObservation):
            return _incomplete("lifecycle_observation_invalid")
        if not _valid_text(lifecycle.attempt_id) or lifecycle.attempt_id != expected_attempt_id:
            return _incomplete("lifecycle_attempt_mismatch")
        if lifecycle.producer != "coordinator":
            return _incomplete("lifecycle_producer_not_authoritative")
        if not _valid_sequence(lifecycle.sequence):
            return _incomplete("lifecycle_sequence_invalid")
        if not _valid_text(lifecycle.status) or lifecycle.status not in KNOWN_LIFECYCLE_STATUSES:
            return _incomplete("lifecycle_status_unknown")
        status = lifecycle.status

    child_code = None
    exit_kind = None
    if exit_observation is not None:
        if not isinstance(exit_observation, ExitObservation):
            return _incomplete("exit_observation_invalid", status)
        if not _valid_text(exit_observation.attempt_id) or exit_observation.attempt_id != expected_attempt_id:
            return _incomplete("exit_attempt_mismatch", status)
        if not _valid_text(exit_observation.producer) or not _valid_text(exit_observation.kind):
            return _incomplete("exit_provenance_fields_invalid", status)
        if not _valid_sequence(exit_observation.sequence):
            return _incomplete("exit_sequence_invalid", status)
        exit_kind = exit_observation.kind
        if exit_kind == "natural_exit":
            if exit_observation.producer not in CHILD_EXIT_PRODUCERS:
                return _incomplete("natural_exit_source_not_child_wait", status)
            if not _valid_code(exit_observation.exit_code) or exit_observation.signal_number is not None:
                return _incomplete("natural_exit_fields_invalid", status)
            child_code = exit_observation.exit_code
        elif exit_kind == "signal_terminated":
            if exit_observation.producer not in CHILD_EXIT_PRODUCERS:
                return _incomplete("signal_source_not_child_wait", status)
            if (exit_observation.exit_code is not None
                    or not _valid_sequence(exit_observation.signal_number)):
                return _incomplete("signal_fields_invalid", status)
        elif exit_kind == "wrapper_exit":
            if exit_observation.producer not in WRAPPER_PRODUCERS:
                return _incomplete("wrapper_exit_source_invalid", status)
            if not _valid_code(exit_observation.exit_code) or exit_observation.signal_number is not None:
                return _incomplete("wrapper_exit_fields_invalid", status)
        elif exit_kind in {"system_exit_requested", "embedded_exception"}:
            if exit_observation.producer != "embedded_interpreter":
                return _incomplete("embedded_observation_source_invalid", status)
            if exit_kind == "system_exit_requested":
                if not _valid_code(exit_observation.exit_code) or exit_observation.signal_number is not None:
                    return _incomplete("embedded_system_exit_fields_invalid", status)
            elif exit_observation.exit_code is not None or exit_observation.signal_number is not None:
                return _incomplete("embedded_exception_fields_invalid", status)
        else:
            return _incomplete("exit_observation_kind_unknown", status)

    failure_confirmed = False
    if program_failure is not None:
        if not isinstance(program_failure, ProgramFailureObservation):
            return _incomplete("program_failure_observation_invalid", status)
        if not _valid_text(program_failure.attempt_id) or program_failure.attempt_id != expected_attempt_id:
            return _incomplete("program_failure_attempt_mismatch", status)
        if not _valid_text(program_failure.producer) or program_failure.producer not in FAILURE_PRODUCERS:
            return _incomplete("program_failure_source_not_authoritative", status)
        if not _valid_sequence(program_failure.sequence):
            return _incomplete("program_failure_sequence_invalid", status)
        if not isinstance(program_failure.confirmed, bool):
            return _incomplete("program_failure_confirmation_not_boolean", status)
        failure_confirmed = program_failure.confirmed

    # Lifecycle dispositions dominate numeric codes. A timeout wrapper's 137,
    # for example, is not evidence of a naturally failing child program.
    if status in NON_SUCCESS_TERMINAL_STATES:
        return _incomplete("lifecycle_is_not_program_completion", status)

    # Natural child exit is the only exit observation that supplies child_code.
    # A confirmed failure and zero exit, or succeeded state and nonzero exit,
    # are contradictions and require reconciliation rather than precedence.
    if status == "succeeded":
        if failure_confirmed:
            return _incomplete("success_conflicts_with_confirmed_program_failure", status)
        if child_code is None:
            return _incomplete("success_without_natural_child_exit", status)
        if child_code != 0:
            return _incomplete("success_conflicts_with_nonzero_child_exit", status)
        return VerdictProjection("PASS", "trusted_success_and_child_exit_zero", status, 0)

    if status == "program_failed":
        if child_code == 0:
            return _incomplete("program_failed_conflicts_with_child_exit_zero", status)
        if exit_kind == "system_exit_requested" and exit_observation.exit_code == 0:
            return _incomplete("program_failed_conflicts_with_embedded_system_exit_zero", status)
        # Coordinator-authored program_failed is a failure classification. It
        # is not inferred from a wrapper code.
        return VerdictProjection("FAIL", "coordinator_confirmed_program_failure", status, child_code)

    if child_code is not None and child_code != 0:
        if status in {"accepted", "queued", "running"}:
            return _incomplete("nonterminal_lifecycle_conflicts_with_child_exit", status)
        return VerdictProjection("FAIL", "direct_child_natural_nonzero_exit", status, child_code)

    if failure_confirmed:
        if status in {"accepted", "queued", "running"}:
            return _incomplete("failure_confirmation_conflicts_with_nonterminal_lifecycle", status)
        return VerdictProjection("FAIL", "trusted_runtime_confirmed_program_failure", status, None)

    if exit_kind in {"wrapper_exit", "system_exit_requested", "embedded_exception", "signal_terminated"}:
        return _incomplete("exit_observation_is_not_natural_child_exit", status)

    return _incomplete("insufficient_terminal_evidence", status)
