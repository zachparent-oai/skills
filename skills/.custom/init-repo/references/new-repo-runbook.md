# New repo runbook

## Phase 1 scaffold (minimum)

- Create `docs/` and add a compact onboarding file.
- Add `Justfile` with build/test/lint commands.
- Add dependency/tool defaults for selected stack (`pnpm` for web, `uv` for Python).
- Add testing skeleton for targeted unit and integration coverage.
- Add workspace/docs conventions in notes for future phases.

## Recommended first tasks

- Choose stack from `zach-stack` profiles.
- Add contributor-level checklist for tests and docs updates.
- Add a clean rollback point before changing environment/config files.

## Suggested outputs by stack

- Web: Tailwind baseline + lightweight project setup + test/check commands.
- Python: `pyproject.toml`/`uv` convention + basic test command.
- Mixed: two-phase plan with clear module boundaries and shared-data workspace notes.
