# `.codex/rules/default.rules` guidance

## Principles

- Keep permissions scoped to the project workflow.
- Prefer minimal, explicit commands.
- Ask before writing any potentially sensitive settings.

## Typical command families

- `uv`: Python install/test/runtime commands
- `just`: repeated repo task orchestration
- `pnpm`: node tooling for web apps
- `gh`: GitHub workflows and issue/pr management
- `glab`: GitLab/GLab workflow parity where used

## Process

- Propose a diff, confirm with user, then apply.
- Re-check the rule set after each commit boundary.
