# Convergence phases

## Phase 0: Discovery

- Detect existing stack and constraints.
- Record what cannot be changed safely in one pass.
- Required outputs:
  - baseline summary (stack, package managers, test/lint commands, CI shape)
  - constraints list (legacy tooling, protected paths, ownership boundaries)
  - proposed Phase 1 scope with explicit non-goals
- Exit criteria:
  - at least one known validation command is runnable (or a documented reason it is not)
  - risky areas are identified before any toolchain changes

## Phase 1: Surface hardening

- Docs + Justfile + lightweight test discoverability.
- Add project-specific lint/test quick checks.
- Required outputs:
  - `docs/` onboarding/file-map refresh (or equivalent docs update)
  - `Justfile` or equivalent command palette entry point
  - lightweight validation checklist (smoke/lint/test commands)
- Exit criteria:
  - agents can discover the main commands quickly
  - at least one fast validation path is documented and verified
  - no architecture/toolchain migration was introduced accidentally

## Phase 2: Toolchain alignment

- Add `zach-stack` defaults where they do not disrupt current architecture.
- Required outputs:
  - small batch of stack-aligned changes (tooling/test/docs) with rationale
  - validation results for the changed command surface
  - rollback note for the batch
- Exit criteria:
  - changes are additive or low-risk refactors
  - lockfile/package manager changes are intentional and explained
  - user-facing workflow remains runnable after changes

## Phase 3+: Optional deepening

- Introduce additional stack pieces (workspaces, visualization layout, docs automation, etc.) as explicit follow-up passes.
- Required outputs:
  - follow-up milestone plan with dependency ordering
  - migration risk notes for each proposed deepening step
- Exit criteria:
  - each deepening step has a separate validation and rollback plan
  - user approval is captured for broad migrations

## Pause points (default)

- Pause after each phase with:
  - what changed
  - what was validated
  - next recommended milestone
  - open risks / deferred items

## Stop-and-ask triggers

- Legacy CI or release pipeline behavior is unclear.
- Lockfile churn affects unrelated packages/modules.
- Proposed change requires command permission/rules updates.
- Migration crosses architecture boundaries (workspace split, framework swap, packaging change).
- Validation commands fail in ways that suggest hidden environment constraints.
