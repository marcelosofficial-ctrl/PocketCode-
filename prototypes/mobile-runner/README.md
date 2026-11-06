# Mobile Runner Prototype Preview

This is a static, interactive **simulation-only** prototype. It does not execute Python, import files, create artifacts, select a runtime, or call a provider.

The example now represents the frozen CSV-to-JSON comparison task from [the fixed-task worksheet](../../AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md):
- canonical `main.py` source shown unchanged;
- success and malformed-header `items.csv` fixtures;
- fixture expectations for `summary.json`, stdout and stderr;
- explicit job, runtime, duration, cleanup, artifact-release and evidence-provenance states;
- copyable example report and debugging prompt with selectable-text fallback.

The two scenario buttons switch between **expected examples**. They are not Run controls. No sample output is offered as a downloadable artifact.

## Preview

Open `index.html` directly in a browser. The page has no external dependencies.

## Static checks

From the repository root:

```sh
python scripts/check_mobile_prototype.py
python -m unittest scripts.test_check_mobile_prototype -v
```

These checks inspect source structure only. They do not execute browser JavaScript, verify clipboard behavior, test screen readers, or execute the submitted Python fixture. Real iOS/Android interaction and accessibility remain NOT RUN.

## Review questions

1. Is it clear that the buttons switch examples rather than run code?
2. Can a reader distinguish fixture expectations from observations?
3. Are stdout, stderr, artifact, cleanup and release states understandable?
4. Can the report be selected and copied when clipboard access is unavailable?
