# Convergence phases

## Phase 0: Discovery

- Detect existing stack and constraints.
- Record what cannot be changed safely in one pass.

## Phase 1: Surface hardening

- Docs + Justfile + lightweight test discoverability.
- Add project-specific lint/test quick checks.

## Phase 2: Toolchain alignment

- Add `zach-stack` defaults where they do not disrupt current architecture.

## Phase 3+: Optional deepening

- Introduce additional stack pieces (workspaces, visualization layout, docs automation, etc.) as explicit follow-up passes.
