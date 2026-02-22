---
name: init-repo
description: "Initialize a new repo with a fast, testable, documented, agent-friendly setup using zach-stack defaults."
---

# Init Repo

Use this skill when a user asks to start a new project or bootstrap an empty repository.

## Workflow

If dependent skills are needed for this workflow, use a local-first fallback order:

- If `zach-stack` / `configure-codex` are already available in the session, use them directly.
- If missing and network access is available, install via `$skill-installer` from the relevant repo/path (fork/local source preferred; GitHub path is a fallback).
- If network access is unavailable, continue with local repo conventions and note the missing skill dependency in your plan/notes.

1. Capture constraints and ask clarifying questions only if ambiguous.
2. Choose a stack profile: web, python, visualization, or mixed.
3. Create a phase-1 scaffold that is minimal but complete:
   - `docs/` with setup and file map starter.
   - `Justfile` with repeatable agent commands.
   - Testing skeleton (unit + at least one integration check).
   - Linting/pre-commit baseline for selected stack.
   - Optional `.codex/rules/default.rules` proposal via `configure-codex`.
4. Add technology-specific defaults from `zach-stack`:
   - web defaults (framework-light vs lightweight React)
   - Python defaults (`uv`)
   - workspace structure if mixed.
5. Define the first milestone commit boundary.

## Guardrails

- Keep `init-repo` incremental: prefer Phase 1 completion over full build-out.
- Default to minimal files and explain what is deferred.
- Never write sensitive agent/environment rules without explicit user confirmation.

## References

- Use `references/new-repo-runbook.md` for scaffold templates and command defaults.

## Reference usage map

- Use `references/new-repo-runbook.md` for Phase 1 scaffold checklists, canonical command names, and acceptance criteria.
- Use the `zach-stack` SKILL for stack selection decisions.
- Read only the relevant `zach-stack/references/*.md` files for the chosen stack (for example `web.md`, `python.md`, `testing.md`, `docs.md`, `workspaces.md`).
