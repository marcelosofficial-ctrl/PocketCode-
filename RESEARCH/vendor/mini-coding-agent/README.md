# Mini-Coding-Agent workspace path validation reference

**Status:** Isolated third-party-derived research utility. Not imported into PocketCode or RevDev. Not a complete filesystem sandbox.

## Provenance

- Upstream project: [rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent)
- Pinned commit: `717cae4ff10d01773bd12951f62a575825053414`
- Upstream source: `mini_coding_agent.py`, blob `1bf2403e5033227e24954faad7f7ba4442f7e4c2`
- Source functions: `MiniAgent.path_is_within_root` and `MiniAgent.path`
- Upstream license: Apache-2.0, LICENSE blob `1e79798da4aac546989b7ca4f26bf1acfea64864`
- This folder contains the relevant license terms and retains the upstream attribution.

The adaptation makes the functions standalone and adds an explicit requirement that the workspace root already exist. It is not a verbatim copy of the complete source module.

## Behavior

- Resolves relative paths below a configured workspace root.
- Resolves symlinks before checking containment.
- Checks the nearest existing ancestor with `samefile()`, allowing a not-yet-created output path beneath an in-root directory.
- Rejects parent traversal, absolute outside paths and symlink escapes.

The accompanying eight tests are project-authored, not upstream tests.

## Limitations

- This is a path validation helper, not an OS sandbox, file permission boundary or hostile-code containment layer.
- A separate filesystem actor may replace a path or symlink between validation and later open/write. It does not use directory file descriptors or race-resistant openat-style handles.
- It does not address hard-link aliasing, Windows reparse point semantics, ACLs, case-folding edge cases, device files, mount points, archive extraction or platform-specific path namespaces.
- Every file read/write must still enforce limits, use a controlled root, avoid following attacker-controlled paths after validation and produce evidence of the exact bytes used.
- The correct production design may instead use an OS-native sandbox, document-provider URI, storage API or immutable file handle.

Use it as a starting point for a native Python workspace adapter only after selecting the execution boundary and adding platform-specific security tests.
