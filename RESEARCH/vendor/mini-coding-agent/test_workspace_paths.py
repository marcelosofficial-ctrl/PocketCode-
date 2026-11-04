import tempfile
import unittest
from pathlib import Path

from workspace_paths import path_is_within_root, resolve_workspace_path


class WorkspacePathTests(unittest.TestCase):
    def test_accepts_root_and_nested_existing_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "src" / "main.py"
            nested.parent.mkdir()
            nested.write_text("pass\n", encoding="utf-8")
            self.assertEqual(resolve_workspace_path(root, "."), root.resolve())
            self.assertEqual(resolve_workspace_path(root, "src/main.py"), nested.resolve())

    def test_accepts_nonexistent_target_below_existing_in_root_parent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = resolve_workspace_path(root, "out/new/result.json")
            self.assertEqual(target, (root / "out/new/result.json").resolve())
            self.assertFalse(target.exists())

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "workspace"
            root.mkdir()
            with self.assertRaisesRegex(ValueError, "escapes workspace"):
                resolve_workspace_path(root, "../outside.txt")

    def test_rejects_absolute_path_outside_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "workspace"
            outside = Path(directory) / "outside.txt"
            root.mkdir()
            outside.write_text("private", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "escapes workspace"):
                resolve_workspace_path(root, outside)

    def test_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "secret.txt").write_text("private", encoding="utf-8")
            link = root / "external"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable")
            with self.assertRaisesRegex(ValueError, "escapes workspace"):
                resolve_workspace_path(root, "external/secret.txt")

    def test_resolves_symlink_that_stays_inside_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("pass", encoding="utf-8")
            (root / "current").symlink_to(root / "src", target_is_directory=True)
            result = resolve_workspace_path(root, "current/main.py")
            self.assertEqual(result, (root / "src" / "main.py").resolve())

    def test_direct_ancestor_check_rejects_unrelated_root(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            other = base / "elsewhere"
            root.mkdir()
            other.mkdir()
            self.assertFalse(path_is_within_root(root, other))

    def test_requires_existing_workspace_root(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            with self.assertRaisesRegex(ValueError, "not an existing directory"):
                resolve_workspace_path(missing, "file.txt")


if __name__ == "__main__":
    unittest.main()
