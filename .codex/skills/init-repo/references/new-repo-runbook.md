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
- Visualization: `pyproject.toml`/`uv` + Streamlit/Plotly baseline + app/run/check commands.

## Minimal Phase 1 file checklist by stack

Use this as a checklist, not a mandate to over-scaffold.

### Web

- `docs/` onboarding + file map
- `package.json` (or existing web manifest) with check/test scripts
- `Justfile`
- frontend source entrypoint(s)
- test setup and at least one user-flow check path
- lint/format config baseline (project-native)

### Python

- `pyproject.toml`
- `uv.lock` (after dependency sync, if dependencies are added)
- `docs/` onboarding + file map
- `Justfile`
- package/module or `scripts/` entrypoint
- `tests/` with unit + one integration/smoke path

### Visualization

- `pyproject.toml`
- `docs/` onboarding + run/check commands
- `Justfile`
- app entrypoint (for example Streamlit app module)
- data boundary module or loader path
- `tests/` for data/loading or transformation logic

### Mixed

- `docs/` onboarding + module map + boundary notes
- `Justfile`
- Python manifest (`pyproject.toml`) and/or web manifest (`package.json`) as applicable
- clear top-level folders/workspaces per module
- test path in each active module
- phase plan note for deferred cross-module integration

## Canonical `Justfile` target names (examples)

Pick only what applies to the repo. Prefer these names for discoverability:

- `setup`
- `dev`
- `test`
- `test-unit`
- `test-integration`
- `lint`
- `format`
- `check`
- `smoke`
- `docs-check`

## Phase 1 acceptance checklist

- Stack profile is selected and documented (including why alternatives were deferred).
- `docs/` contains a quickstart/runbook and a file/module map (or equivalent).
- A command palette exists (`Justfile` preferred) and points to real commands.
- At least one fast validation command and one deeper check are documented.
- Minimal test skeleton exists (unit + integration/smoke path where applicable).
- Deferred items and the next milestone boundary are documented explicitly.
