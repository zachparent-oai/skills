# Allowed command matrix (`configure-codex`)

## Always avoid by default

- Blanket escalation of broad shell commands.
- Universal global allow-lists without project need.

## Recommended matrix by project type

- **Web-first**: `pnpm`, `just`, `gh`, optional `uv`.
- **Python-first**: `uv`, `just`, `gh`, optional `glab`.
- **Mixed**: web + python commands only where actively used.

## Confirmation requirements

- Ask before enabling commands not currently used by the repo.
- Keep user-visible logs of every newly enabled command.
