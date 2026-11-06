import unittest

try:
    from dispatch_reconciliation import (
        DispatchContext, IdempotencyContract, ProviderLookup, decide_ambiguous_dispatch,
    )
except ModuleNotFoundError:
    from scripts.dispatch_reconciliation import (
        DispatchContext, IdempotencyContract, ProviderLookup, decide_ambiguous_dispatch,
    )


CTX = DispatchContext("effect-1", "attempt-1", "sha256:abc", "https://api.example/run",
                      "account-A", "token-1", "provider-X", "v2", "region-west",
                      "sent_unacknowledged")


def exact_contract(**changes):
    values = dict(documented=True, endpoint=CTX.endpoint, account_scope=CTX.account_scope,
                  idempotency_token=CTX.idempotency_token, fingerprint=CTX.request_fingerprint,
                  provider_id=CTX.provider_id, api_version=CTX.api_version, region_scope=CTX.region_scope,
                  retention_active=True, same_request_replay_deduplicated=True,
                  changed_parameters_rejected=True)
    values.update(changes)
    return IdempotencyContract(**values)


def found(**changes):
    values = dict(outcome="found", authoritative=True, effect_id=CTX.effect_id,
                  attempt_id=CTX.attempt_id, request_fingerprint=CTX.request_fingerprint,
                  endpoint=CTX.endpoint, account_scope=CTX.account_scope,
                  idempotency_token=CTX.idempotency_token, provider_id=CTX.provider_id,
                  api_version=CTX.api_version, region_scope=CTX.region_scope)
    values.update(changes)
    return ProviderLookup(**values)


def authoritative_not_found(**changes):
    values = dict(outcome="not_found", authoritative=True, absence_final=True, effect_id=CTX.effect_id,
                  attempt_id=CTX.attempt_id, request_fingerprint=CTX.request_fingerprint,
                  endpoint=CTX.endpoint, account_scope=CTX.account_scope,
                  idempotency_token=CTX.idempotency_token, provider_id=CTX.provider_id,
                  api_version=CTX.api_version, region_scope=CTX.region_scope)
    values.update(changes)
    return ProviderLookup(**values)


class DispatchReconciliationTests(unittest.TestCase):
    def test_reserved_without_prior_send_dispatches_first(self):
        ctx = DispatchContext(**{**CTX.__dict__, "state": "reserved"})
        self.assertEqual(decide_ambiguous_dispatch(ctx, None).action, "dispatch_first")

    def test_acknowledged_attempt_is_polled_not_redispatched(self):
        ctx = DispatchContext(**{**CTX.__dict__, "state": "acknowledged"})
        self.assertEqual(decide_ambiguous_dispatch(ctx, None).action, "poll_existing")

    def test_running_attempt_is_polled_not_redispatched(self):
        ctx = DispatchContext(**{**CTX.__dict__, "state": "running"})
        self.assertEqual(decide_ambiguous_dispatch(ctx, None).action, "poll_existing")

    def test_terminal_attempt_is_never_replayed(self):
        ctx = DispatchContext(**{**CTX.__dict__, "state": "terminal"})
        self.assertEqual(decide_ambiguous_dispatch(ctx, None).action, "do_not_replay")

    def test_exact_found_provider_result_is_adopted(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found()).action, "adopt_existing")

    def test_found_different_attempt_is_conflict(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found(attempt_id="attempt-old")).action, "conflict")

    def test_found_different_effect_is_conflict(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found(effect_id="effect-old")).action, "conflict")

    def test_found_changed_request_fingerprint_is_conflict(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found(request_fingerprint="sha256:changed")).action, "conflict")

    def test_found_different_endpoint_is_conflict(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found(endpoint="https://other.example/run")).action, "conflict")

    def test_non_authoritative_found_result_cannot_be_adopted(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found(authoritative=False)).action, "hold_unknown")

    def test_authoritative_not_found_for_different_attempt_is_conflict(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, authoritative_not_found(attempt_id="attempt-old")).action, "conflict")

    def test_found_different_account_scope_is_conflict(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, found(account_scope="account-B")).action, "conflict")

    def test_found_different_provider_version_or_region_is_conflict(self):
        for change in ({"provider_id": "provider-Y"}, {"api_version": "v3"}, {"region_scope": "region-east"}):
            with self.subTest(change=change):
                self.assertEqual(decide_ambiguous_dispatch(CTX, found(**change)).action, "conflict")

    def test_provider_api_or_region_contract_mismatch_holds_unknown(self):
        for change in ({"provider_id": "provider-Y"}, {"api_version": "v3"}, {"region_scope": "region-east"}):
            with self.subTest(change=change):
                self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), exact_contract(**change)).action, "hold_unknown")

    def test_authoritative_not_found_allows_same_attempt_retry(self):
        lookup = authoritative_not_found()
        got = decide_ambiguous_dispatch(CTX, lookup)
        self.assertEqual(got.action, "retry_same_attempt")
        self.assertTrue(got.reuse_attempt_id)
        self.assertTrue(got.reuse_idempotency_token)

    def test_non_authoritative_not_found_holds_unknown(self):
        lookup = ProviderLookup(outcome="not_found", authoritative=False)
        self.assertEqual(decide_ambiguous_dispatch(CTX, lookup).action, "hold_unknown")

    def test_unknown_lookup_without_contract_holds_unknown(self):
        self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown")).action, "hold_unknown")

    def test_exact_idempotency_contract_allows_exact_same_request_retry(self):
        got = decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), exact_contract())
        self.assertEqual(got.action, "retry_same_attempt")
        self.assertTrue(got.reuse_effect_id and got.reuse_attempt_id and got.reuse_request_fingerprint)

    def test_expired_idempotency_retention_does_not_allow_retry(self):
        contract = exact_contract(retention_active=False)
        self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), contract).action, "hold_unknown")

    def test_wrong_endpoint_contract_does_not_allow_retry(self):
        contract = exact_contract(endpoint="https://other.example/run")
        self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), contract).action, "hold_unknown")

    def test_wrong_account_contract_does_not_allow_retry(self):
        contract = exact_contract(account_scope="account-B")
        self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), contract).action, "hold_unknown")

    def test_changed_fingerprint_contract_does_not_allow_retry(self):
        contract = exact_contract(fingerprint="sha256:changed")
        self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), contract).action, "hold_unknown")

    def test_changed_parameters_must_be_rejected_by_contract(self):
        contract = exact_contract(changed_parameters_rejected=False)
        self.assertEqual(decide_ambiguous_dispatch(CTX, ProviderLookup("unknown"), contract).action, "hold_unknown")

    def test_lookup_on_never_sent_reservation_conflicts(self):
        ctx = DispatchContext(**{**CTX.__dict__, "state": "reserved"})
        self.assertEqual(decide_ambiguous_dispatch(ctx, found()).action, "conflict")

    def test_invalid_context_holds_as_conflict(self):
        ctx = DispatchContext("", CTX.attempt_id, CTX.request_fingerprint, CTX.endpoint,
                              CTX.account_scope, CTX.idempotency_token, CTX.provider_id,
                              CTX.api_version, CTX.region_scope, "sent_unacknowledged")
        self.assertEqual(decide_ambiguous_dispatch(ctx, None).action, "conflict")

    def test_authoritative_lookup_can_reconcile_without_provider_idempotency_token(self):
        ctx = DispatchContext(CTX.effect_id, CTX.attempt_id, CTX.request_fingerprint, CTX.endpoint,
                              CTX.account_scope, None, CTX.provider_id, CTX.api_version,
                              CTX.region_scope, "sent_unacknowledged")
        exact = found(idempotency_token=None)
        got = decide_ambiguous_dispatch(ctx, exact)
        self.assertEqual(got.action, "adopt_existing")
        self.assertFalse(got.reuse_idempotency_token)

    def test_missing_provider_token_cannot_use_token_based_replay_contract(self):
        ctx = DispatchContext(CTX.effect_id, CTX.attempt_id, CTX.request_fingerprint, CTX.endpoint,
                              CTX.account_scope, None, CTX.provider_id, CTX.api_version,
                              CTX.region_scope, "sent_unacknowledged")
        self.assertEqual(decide_ambiguous_dispatch(ctx, ProviderLookup("unknown"), exact_contract()).action, "hold_unknown")

    def test_invalid_lookup_does_not_authorize_retry(self):
        class BadLookup:
            outcome = "found"
        self.assertEqual(decide_ambiguous_dispatch(CTX, BadLookup()).action, "hold_unknown")


    def test_invalid_context_type_fails_closed(self):
        got = decide_ambiguous_dispatch(None, None)
        self.assertEqual(got.action, "conflict")
        self.assertFalse(got.reuse_idempotency_token)

    def test_missing_token_does_not_claim_token_reuse(self):
        ctx = DispatchContext(CTX.effect_id, CTX.attempt_id, CTX.request_fingerprint, CTX.endpoint,
                              CTX.account_scope, None, CTX.provider_id, CTX.api_version,
                              CTX.region_scope, "sent_unacknowledged")
        got = decide_ambiguous_dispatch(ctx, ProviderLookup("unknown"))
        self.assertEqual(got.action, "hold_unknown")
        self.assertFalse(got.reuse_idempotency_token)

    def test_eventually_consistent_not_found_does_not_authorize_retry(self):
        lookup = authoritative_not_found(absence_final=False)
        self.assertEqual(decide_ambiguous_dispatch(CTX, lookup).action, "hold_unknown")

    def test_tokenless_lookup_does_not_claim_token_reuse(self):
        ctx = DispatchContext(CTX.effect_id, CTX.attempt_id, CTX.request_fingerprint, CTX.endpoint,
                              CTX.account_scope, None, CTX.provider_id, CTX.api_version,
                              CTX.region_scope, "sent_unacknowledged")
        lookup = found(idempotency_token=None)
        got = decide_ambiguous_dispatch(ctx, lookup)
        self.assertEqual(got.action, "adopt_existing")
        self.assertFalse(got.reuse_idempotency_token)

    def test_invalid_context_type_fails_closed(self):
        got = decide_ambiguous_dispatch(None, None)
        self.assertEqual(got.action, "conflict")


if __name__ == "__main__":
    unittest.main(verbosity=2)
