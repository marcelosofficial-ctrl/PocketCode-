from pathlib import Path


def path_is_within_root(root: Path, resolved: Path) -> bool:
    """Check whether a resolved path is the root or has it as an ancestor.

    Adapted from rasbt/mini-coding-agent. The nearest existing ancestor is
    checked with samefile(), so nonexistent targets below an in-root directory
    can still be validated without treating an outside symlink as in-root.
    """
    root = Path(root).resolve()
    resolved = Path(resolved).resolve()
    probe = resolved
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    for candidate in (probe, *probe.parents):
        try:
            if candidate.samefile(root):
                return True
        except OSError:
            continue
    return False


def resolve_workspace_path(root: Path, raw_path: str | Path) -> Path:
    """Resolve a user path and reject it when the resolved target escapes root.

    The workspace root must already exist. This is a path validation helper,
    not a file-open primitive or OS security sandbox.
    """
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"workspace root is not an existing directory: {root}")

    path = Path(raw_path)
    path = path if path.is_absolute() else root / path
    resolved = path.resolve()
    if not path_is_within_root(root, resolved):
        raise ValueError(f"path escapes workspace: {raw_path}")
    return resolved
