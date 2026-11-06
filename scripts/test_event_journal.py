import unittest
try:
    from event_journal import AuthenticatedProducer, EventJournal, JournalConflict
except ModuleNotFoundError:
    from scripts.event_journal import AuthenticatedProducer, EventJournal, JournalConflict

P = AuthenticatedProducer("issuer-A", "worker-7", "key-2", "sha256:credential",
                          "pocketcode-journal", ("worker-events", "provider-events"))


class EventJournalTests(unittest.TestCase):
    def setUp(self):
        self.journal = EventJournal(expected_audience="pocketcode-journal")

    def append(self, **changes):
        args = dict(producer=P, source="worker-events", event_id="evt-1",
                    payload=b'{"state":"started"}', occurred_at_ms=100,
                    observed_at_ms=110)
        args.update(changes)
        return self.journal.append(**args)

    def test_accepts_verified_authorized_producer(self):
        result = self.append()
        self.assertEqual(result.disposition, "accepted")
        self.assertEqual(result.sequence, 1)

    def test_duplicate_same_source_event_and_same_payload_is_idempotent(self):
        first = self.append()
        second = self.append(observed_at_ms=120)
        self.assertEqual(second.disposition, "duplicate")
        self.assertEqual(second.sequence, first.sequence)
        self.assertEqual(len(self.journal.events), 1)

    def test_same_event_id_from_different_source_is_distinct(self):
        self.append()
        result = self.append(source="provider-events")
        self.assertEqual(result.disposition, "accepted")
        self.assertEqual(result.sequence, 2)

    def test_key_rotation_for_same_producer_does_not_break_exact_duplicate(self):
        self.append()
        rotated = AuthenticatedProducer("issuer-A", "worker-7", "key-rotated", "sha256:new",
                                        "pocketcode-journal", ("worker-events",))
        result = self.append(producer=rotated)
        self.assertEqual(result.disposition, "duplicate")
        self.assertEqual(result.sequence, 1)

    def test_same_source_event_id_cannot_be_replayed_across_attempt_scope(self):
        first = self.append(effect_id="effect-A", attempt_id="attempt-A")
        replay = self.append(effect_id="effect-B", attempt_id="attempt-B")
        self.assertEqual(first.disposition, "accepted")
        self.assertEqual(replay.disposition, "quarantined")
        self.assertEqual(self.journal.events[0].effect_id, "effect-A")
        self.assertEqual(self.journal.events[0].attempt_id, "attempt-A")

    def test_unfenced_reservation_event_remains_unfenced_after_lease_advance(self):
        reservation_producer = AuthenticatedProducer(
            "issuer-A", "coordinator", "key-2", "sha256:credential",
            "pocketcode-journal", ("pocketcode.coordinator",),
        )
        payload = b'{"attempt_id":"attempt-1","effect_id":"effect-1","kind":"effect_reserved"}'
        first = self.journal.append(
            producer=reservation_producer, source="pocketcode.coordinator",
            event_id="reservation-1", payload=payload, occurred_at_ms=100,
            observed_at_ms=110, effect_id="effect-1", attempt_id="attempt-1",
            require_fence=False,
        )
        self.journal.advance_fence("effect-1", "attempt-1", 1)
        replay = self.journal.append(
            producer=reservation_producer, source="pocketcode.coordinator",
            event_id="reservation-1", payload=payload, occurred_at_ms=100,
            observed_at_ms=120, effect_id="effect-1", attempt_id="attempt-1",
            require_fence=False,
        )
        self.assertEqual(first.disposition, "accepted")
        self.assertEqual(replay.disposition, "duplicate")
        self.assertIsNone(first.event.fence)

    def test_unfenced_worker_event_is_rejected_even_with_flag(self):
        with self.assertRaises(JournalConflict):
            self.append(effect_id="effect-1", attempt_id="attempt-1",
                        require_fence=False)

    def test_unfenced_wrong_kind_or_scope_is_rejected(self):
        reservation_producer = AuthenticatedProducer(
            "issuer-A", "coordinator", "key-2", "sha256:credential",
            "pocketcode-journal", ("pocketcode.coordinator",),
        )
        with self.assertRaises(JournalConflict):
            self.journal.append(
                producer=reservation_producer, source="pocketcode.coordinator",
                event_id="not-reservation",
                payload=b'{"attempt_id":"attempt-1","effect_id":"effect-1","kind":"dispatch_intent"}',
                occurred_at_ms=100, observed_at_ms=110,
                effect_id="effect-1", attempt_id="attempt-1", require_fence=False,
            )

    def test_same_event_replay_under_new_fence_is_quarantined(self):
        self.journal.advance_fence("effect-1", "attempt-1", 1)
        first = self.append(effect_id="effect-1", attempt_id="attempt-1", fence=1)
        self.journal.advance_fence("effect-1", "attempt-1", 2)
        replay = self.append(effect_id="effect-1", attempt_id="attempt-1", fence=2)
        self.assertEqual(first.disposition, "accepted")
        self.assertEqual(replay.disposition, "quarantined")
        self.assertEqual(self.journal.events[0].fence, 1)
        self.assertEqual(len(self.journal.events), 1)
        self.assertEqual(len(self.journal.conflicts), 1)

    def test_same_payload_with_changed_occurrence_time_is_quarantined(self):
        self.append()
        result = self.append(occurred_at_ms=101)
        self.assertEqual(result.disposition, "quarantined")
        self.assertEqual(len(self.journal.events), 1)
        self.assertEqual(len(self.journal.conflicts), 1)

    def test_same_source_event_id_from_different_authenticated_producer_is_quarantined(self):
        self.append()
        other = AuthenticatedProducer("issuer-A", "worker-8", "key-3", "sha256:other",
                                      "pocketcode-journal", ("worker-events",))
        result = self.append(producer=other)
        self.assertEqual(result.disposition, "quarantined")
        self.assertEqual(len(self.journal.events), 1)
        self.assertEqual(len(self.journal.conflicts), 1)

    def test_same_source_event_id_with_changed_payload_is_quarantined(self):
        self.append()
        result = self.append(payload=b'{"state":"failed"}')
        self.assertEqual(result.disposition, "quarantined")
        self.assertEqual(len(self.journal.events), 1)
        self.assertEqual(len(self.journal.conflicts), 1)
        self.assertEqual(result.conflict.accepted_payload_sha256,
                         self.journal.events[0].payload_sha256)

    def test_quarantine_is_append_only_and_does_not_replace_accepted_event(self):
        original = self.append().event
        self.append(payload=b"changed")
        duplicate = self.append()
        self.assertEqual(duplicate.disposition, "duplicate")
        self.assertEqual(self.journal.events[0], original)
        self.assertEqual(self.journal.last_sequence, 2)

    def test_wrong_audience_rejected(self):
        bad = AuthenticatedProducer("i", "s", "k", "fp", "other", ("worker-events",))
        with self.assertRaises(JournalConflict):
            self.append(producer=bad)

    def test_unauthorized_source_rejected(self):
        with self.assertRaises(JournalConflict):
            self.append(source="untrusted-source")

    def test_incomplete_identity_rejected(self):
        bad = AuthenticatedProducer("i", "", "k", "fp", "pocketcode-journal", ("worker-events",))
        with self.assertRaises(JournalConflict):
            self.append(producer=bad)

    def test_unverified_object_rejected(self):
        with self.assertRaises(JournalConflict):
            self.append(producer={"issuer": "issuer-A"})

    def test_event_id_and_payload_are_validated(self):
        for event_id, payload in (("", b"x"), ("evt", b""), ("evt", "not-bytes")):
            with self.subTest(event_id=event_id, payload=payload):
                with self.assertRaises(ValueError):
                    self.append(event_id=event_id, payload=payload)

    def test_timestamps_reject_bool_negative_and_non_integer(self):
        for occurred, observed in ((True, 1), (-1, 1), (1, False), (1, "2")):
            with self.subTest(occurred=occurred, observed=observed):
                with self.assertRaises(ValueError):
                    self.append(occurred_at_ms=occurred, observed_at_ms=observed)

    def test_effect_and_attempt_must_be_paired(self):
        with self.assertRaises(ValueError):
            self.append(effect_id="effect-1")

    def test_initial_attempt_event_can_be_bound_before_first_fence(self):
        result = self.append(event_id="reserved", effect_id="effect-1", attempt_id="attempt-1")
        self.assertEqual(result.disposition, "accepted")
        self.assertIsNone(result.event.fence)

    def test_effect_event_rejects_fence_before_first_lease(self):
        with self.assertRaises(JournalConflict):
            self.append(event_id="premature", effect_id="effect-1", attempt_id="attempt-1", fence=1)

    def test_current_fence_accepts_and_stale_fence_rejects(self):
        self.journal.advance_fence("effect-1", "attempt-1", 2)
        accepted = self.append(effect_id="effect-1", attempt_id="attempt-1", fence=2)
        self.assertEqual(accepted.disposition, "accepted")
        self.journal.advance_fence("effect-1", "attempt-1", 3)
        with self.assertRaises(JournalConflict):
            self.append(event_id="evt-2", effect_id="effect-1",
                        attempt_id="attempt-1", fence=2)

    def test_fence_must_strictly_increase(self):
        self.journal.advance_fence("effect-1", "attempt-1", 1)
        for value in (1, 0, True, "2"):
            with self.subTest(value=value):
                with self.assertRaises((ValueError, JournalConflict)):
                    self.journal.advance_fence("effect-1", "attempt-1", value)

    def test_sequences_are_coordinator_assigned_and_monotonic(self):
        a = self.append()
        b = self.append(source="provider-events", event_id="evt-2")
        self.assertEqual((a.sequence, b.sequence), (1, 2))
        self.assertEqual([e.sequence for e in self.journal.events], [1, 2])

    def test_event_payload_is_immutable_bytes_copy(self):
        with self.assertRaises(ValueError):
            self.append(payload=bytearray(b"payload"))

    def test_invalid_expected_audience_rejected(self):
        with self.assertRaises(ValueError):
            EventJournal(expected_audience=" ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
