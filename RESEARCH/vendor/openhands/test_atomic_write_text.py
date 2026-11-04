import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from atomic_write_text import atomic_write_text, is_temp_file


class AtomicWriteTextTests(unittest.TestCase):
    def test_writes_utf8_and_replaces_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "state.json"
            atomic_write_text(target, '{"label":"café"}')
            self.assertEqual(target.read_text(encoding="utf-8"), '{"label":"café"}')
            atomic_write_text(target, '{"version":2}')
            self.assertEqual(target.read_text(encoding="utf-8"), '{"version":2}')
            self.assertEqual([p.name for p in Path(directory).iterdir()], ["state.json"])

    def test_temp_file_is_created_beside_target_and_removed_after_replace(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested" / "state.json"
            target.parent.mkdir()
            observed = []
            real_replace = os.replace

            def recording_replace(source, destination):
                observed.append(Path(source))
                real_replace(source, destination)

            with patch("atomic_write_text.os.replace", recording_replace):
                atomic_write_text(target, "ok")

            self.assertEqual(len(observed), 1)
            self.assertEqual(observed[0].parent, target.parent)
            self.assertTrue(observed[0].name.startswith(".state.json."))
            self.assertTrue(is_temp_file(observed[0]))
            self.assertEqual([p.name for p in target.parent.iterdir()], ["state.json"])

    def test_replace_failure_preserves_previous_file_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "state.json"
            atomic_write_text(target, "old")

            with patch("atomic_write_text.os.replace", side_effect=OSError("replace failed")):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    atomic_write_text(target, "new")

            self.assertEqual(target.read_text(encoding="utf-8"), "old")
            self.assertEqual([p.name for p in Path(directory).iterdir()], ["state.json"])

    def test_posix_file_mode_is_owner_only(self):
        if os.name != "posix":
            self.skipTest("POSIX permission bits are not portable to this OS")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "private.json"
            atomic_write_text(target, "synthetic fixture")
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)

    def test_temp_file_classifier_is_suffix_based(self):
        self.assertTrue(is_temp_file(Path(".state.json.abcd.tmp")))
        self.assertFalse(is_temp_file(Path("state.json")))
        self.assertFalse(is_temp_file(Path(".state.json.marker")))


if __name__ == "__main__":
    unittest.main()
