# Repository Agents Instructions

- Purpose: this repository is a personal fork of the OpenAI Skills catalog plus a `.custom` namespace for your own workflows.
- Scope: keep the public skill catalogs untouched unless explicitly requested.
- Keep new skills focused on role and workflow, and place detailed guidance under `references/`.
- Prefer concise SKILL files with one-level references.
- Use incremental changes for this skills suite and commit in logical milestones.
- Do not add scripts unless they are essential and deterministic.
- No README/CHANGELOG style collateral is required inside a skill.

## Linting and tests

Run `bash scripts/test-custom-skills.sh` before committing changes to `.custom` skills.
