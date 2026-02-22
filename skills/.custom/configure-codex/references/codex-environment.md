# Codex environment and worktree setup

## Objective

Make agent work predictable and repeatable in local and customer environments.

## Setup areas

- command presets for project startup
- worktree naming and path strategy
- reusable command sequences via `Justfile`
- lightweight onboarding docs for Codex behavior

## Recommendations

- Keep environment setup documented in `docs/`.
- Separate repo updates from user-profile updates.
- Validate environment commands after each phase.
- Use conservative defaults and escalate only as needed.
