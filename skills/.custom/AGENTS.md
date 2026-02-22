# .custom Agent Instructions

This directory contains personal/custom skills used for repo-specific agent workflows.

- Keep skill definitions opinionated and minimal in `SKILL.md`.
- Put detailed instructions in `references/` files under each skill.
- Maintain one-to-one mirroring between `.custom/<skill>` and `.codex/skills/<skill>` via sync tooling.
- Treat `skills/.custom/*` as the source of truth and `.codex/skills/*` as a generated mirror.
- Run `uv run scripts/sync-custom-skills.py check` before committing to verify the mirror.
- Use `uv run scripts/sync-custom-skills.py sync` to refresh the mirror after `.custom` edits.
- Run `uv run scripts/test-custom-skills.py` before committing `.custom` updates.
