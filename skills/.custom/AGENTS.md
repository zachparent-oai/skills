# .custom Agent Instructions

This directory contains personal/custom skills used for repo-specific agent workflows.

- Keep skill definitions opinionated and minimal in `SKILL.md`.
- Put detailed instructions in `references/` files under each skill.
- Maintain one-to-one mirroring between `.custom/<skill>` and `.codex/skills/<skill>` via sync tooling.
- Run `bash scripts/test-custom-skills.sh` before committing `.custom` updates.
