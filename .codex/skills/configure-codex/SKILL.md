---
name: configure-codex
description: "Conservatively configure `.codex/rules/default.rules` and Codex environment setup for repo and user ergonomics."
---

# Configure Codex

Use this skill when asked to update Codex rules, command permissions, or environment setup for repository work.

## Scope
- `.codex/rules/default.rules` updates.
- Command allow-list selection.
- Codex environment/worktree ergonomics.
- Guidance for repo-scoped vs user-scoped settings.

## Guarded workflow

1. Inventory current constraints and user intent.
2. Propose only relevant allowed command families (e.g., uv, just, pnpm, gh, glab).
3. Ask for confirmation before writing rule updates.
4. Apply minimally and explain impact.
5. Validate the new command surface and leave a follow-up note.

## Conservative defaults

- Keep allow-lists minimal.
- Prefer repo-only permissions over broad global overrides.
- Add no commands that are not used by the project.

## References

- `references/rules-default.md`
- `references/allowed-commands-matrix.md`
- `references/codex-environment.md`
