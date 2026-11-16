# .devcontainer — the L2 codespace environment

`devcontainer.json` boots the environment that `CLOUD_DEPLOY.md`
(section 2) specifies, so the setup steps there become automatic:

- Python 3.12 (mcr.microsoft.com/devcontainers/python:3.12).
- `postCreateCommand` installs the pipeline stack
  (numpy, pandas, pyarrow, scipy, lifelines) plus the library
  tooling (pypdf, fonttools) and pytest, then runs the repo's test
  suite: a codespace that boots with a red test suite is a broken
  environment, caught before any data work.
- The Tardis key is injected from the Codespaces secret
  `TARDIS_API_KEY` (repo Settings > Codespaces > Secrets). It is
  never echoed, logged, or committed; `CLOUD_DEPLOY.md` section 3
  governs its use.

Machine sizing and disk guidance remain in `CLOUD_DEPLOY.md`
section 1 (4-core/16GB minimum; disk grows with the raw CSVs).
