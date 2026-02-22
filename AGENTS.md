# Repository Agents Instructions

- Purpose: this repository is a personal fork of the OpenAI Skills catalog plus a `.custom` namespace for your own workflows.
- Scope: keep the public skill catalogs untouched unless explicitly requested.
- Keep new skills focused on role and workflow, and place detailed guidance under `references/`.
- Prefer concise SKILL files with one-level references.
- Use incremental changes for this skills suite and commit in logical milestones.
- Do not add scripts unless they are essential and deterministic.
- No README/CHANGELOG style collateral is required inside a skill.

## Skills repo editing workflow

- For updates to existing skills, keep `SKILL.md` compact and put detailed procedures/examples under the skill's `references/` files.
- Before editing, read the target `SKILL.md` and only the referenced files needed for the requested change (avoid broad reference-chasing).
- For custom skills, `skills/.custom/<skill>` is the source of truth; `.codex/skills/<skill>` is a sync-generated mirror.
- Do not manually edit `.codex/skills/<custom-skill>`; run `uv run scripts/sync-custom-skills.py sync` after updating `skills/.custom/<skill>`.
- If `uv run scripts/sync-custom-skills.py check` fails after mirror-side edits, port the changes into `skills/.custom/<skill>` and sync again.
- Do not run lint/content checks against `.codex/skills`; custom-skill linting should focus on `skills/.custom` (mirror sync/check is separate).
- When adding guidance about another skill (for example `$playwright`), first check whether it is installed under `$CODEX_HOME/skills`; if not, document the `$skill-installer` path and any required restart step.
- When documenting external tools in `references/`, include source links and short excerpts instead of long copied passages.

## Linting and tests

Run `uv run scripts/test-custom-skills.py` before committing `.custom` changes.

Install pre-commit hooks once with:
`PRE_COMMIT_HOME=.pre-commit-cache pre-commit install --install-hooks`.

Run pre-commit checks:
`pre-commit run --all-files` (or `just pre-commit-check`).

Hooks install command in this repo uses a local pre-commit home:
`PRE_COMMIT_HOME=.pre-commit-cache pre-commit install --install-hooks`.
