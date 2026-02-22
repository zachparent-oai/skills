# Rollback and safety

## Why it matters

Incremental changes are useful only if each step is reversible.

## Safety pattern

- Make one conceptual category of change at a time.
- Validate commands and tests after each change set.
- Record a simple checkpoint note:
  - What changed
  - Why it changed
  - How to revert

## Example rollback triggers

- Unexpected behavioral diff
- Test coverage mismatch introduced by command changes
- Documentation or automation drift
