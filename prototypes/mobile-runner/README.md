# Mobile Runner Prototype Preview

**[Open the live phone preview](https://marcelosofficial-ctrl.github.io/PocketCode-/)** — sample output only; submitted code is not executed.

This is a static, interactive UI prototype for product feedback. It does not execute submitted code and must not be treated as evidence that the runtime works.

## Enable the phone-friendly preview

The repository's workflow is ready to publish only this folder to GitHub Pages:
- Workflow: [Publish mobile prototype preview](../../.github/workflows/preview-prototype.yml)
- Source: `prototypes/mobile-runner/index.html`

GitHub Pages must be enabled once in repository settings. For this public repository, GitHub Free supports Pages. Configure the publishing source as GitHub Actions.

1. Open the repository on GitHub.
2. Open **Settings → Pages**.
3. Under **Build and deployment → Source**, select **GitHub Actions** and save if prompted.
4. Open the **Actions** tab.
5. Open **Publish mobile prototype preview** and choose **Re-run all jobs** for the existing failed run, or use **Run workflow** on the default branch.
6. Wait for a successful deployment. Open the published page URL shown in the workflow's deployment environment.

The preview is public because this repository is public. It contains only a sample interface and fabricated example output; do not add private data, credentials, or real user code to this demo.

## What to review on a phone

- Can you understand what PocketCode does from the first screen?
- Is the code / input file switcher clear?
- Is the Run action easy to find and tap?
- Is it obvious that the output is a simulation?
- Is the error report understandable?
- Would you use **Copy report** or **Copy AI prompt** after a real run?

## Prototype boundaries

- No backend, runtime provider, login, persistence, analytics, or external JavaScript libraries.
- The success/error output and download are samples only.
- Clipboard behavior depends on browser permissions and secure-context support.
- No browser interaction or accessibility audit has been completed yet.
