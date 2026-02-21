# Incremental harness setup

## Purpose

Build the operating surface needed for agents before enforcing deeper stack shifts.

## Initial changes (safe first)

- Add/normalize `docs/` with a current file-map and runbook.
- Add/refresh `Justfile` command palette.
- Introduce a lightweight test index and smoke test list.
- Clarify command/tool ownership in docs.

## Principle

The harness layer should reduce uncertainty first: if agents can discover and run stable commands, deeper changes are cheaper and safer.
