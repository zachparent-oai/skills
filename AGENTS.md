# Repository Agents Instructions

- Purpose: this repository is a personal fork of the OpenAI Skills catalog plus a `.custom` namespace for your own workflows.
- Scope: keep the public skill catalogs untouched unless explicitly requested.
- Keep new skills focused on role and workflow, and place detailed guidance under `references/`.
- Prefer concise SKILL files with one-level references.
- Use incremental changes for this skills suite and commit in logical milestones.
- Do not add scripts unless they are essential and deterministic.
- No README/CHANGELOG style collateral is required inside a skill.

## Linting and tests

Run `uv run scripts/test-custom-skills.py` before committing `.custom` changes.

Install pre-commit hooks once with:
`PRE_COMMIT_HOME=.pre-commit-cache pre-commit install --install-hooks`.

Run pre-commit checks:
`pre-commit run --all-files` (or `just pre-commit-check`).

Hooks install command in this repo uses a local pre-commit home:
`PRE_COMMIT_HOME=.pre-commit-cache pre-commit install --install-hooks`.
