# Allowed command matrix (`configure-codex`)

## Always avoid by default

- Blanket escalation of broad shell commands.
- Universal global allow-lists without project need.

## Recommended matrix by project type

- **Web-first**: `pnpm`, `just`, `gh`, optional `uv`.
- **Python-first**: `uv`, `just`, `gh`, optional `glab`.
- **Mixed**: web + python commands only where actively used.

## Example allow-list choices (starting points)

- **Web-first (pnpm repo)**:
  - allow: `pnpm install`, `pnpm test`, `pnpm run <project-scripts>`, `just <project-targets>`, `gh pr/status` workflows
  - defer: `uv *`, `glab *`, Docker commands, broad shell wrappers unless already part of the repo workflow
- **Python-first (uv repo)**:
  - allow: `uv sync`, `uv run <project-commands>`, `uv tool run <approved-tools>`, `just <project-targets>`, `gh` or `glab` (one host only if possible)
  - defer: `pnpm *`, `npm *`, `poetry *` unless the repo actively uses them
- **Mixed repo**:
  - allow only the command families visible in manifests/scripts (`pyproject.toml`, `package.json`, `justfile`, CI config)
  - prefer narrower prefixes (for example `uv run`, `pnpm run`) before broader ones

## Commands to defer unless explicitly justified

- Broad shell execution patterns (`bash -c`, `sh -c`, blanket shell escalation).
- Package managers not used by the repo.
- Destructive VCS commands (`git reset --hard`, force pushes).
- Infra/runtime commands (Docker, cloud CLIs, kubectl) when unrelated to the current repo task.
- Download/execution tools (`curl`, `wget`) unless required by the documented workflow.

## Confirmation requirements

- Ask before enabling commands not currently used by the repo.
- Keep user-visible logs of every newly enabled command.
- Use explicit approval prompts for trust-sensitive additions. Examples:
  - "Do you want to allow `uv sync` outside the sandbox for this repo's dependency setup?"
  - "Do you want to allow `pnpm run build` for this project, or keep builds manual for now?"
  - "Do you want repo-scoped rules only, or should this be added to your user-level Codex rules?"
