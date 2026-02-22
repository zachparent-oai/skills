# Testing conventions (`zach-stack`)

## Scope

Use this file as the entrypoint for `zach-stack` testing guidance. It captures shared principles and points to focused testing references by project shape.

## Core testing principles

- Use a layered strategy: add focused unit tests plus at least one integration/acceptance layer.
- Prefer targeted tests over relying only on broad end-to-end/integration coverage.
- Keep tests deterministic where possible (inputs, outputs, fixtures, and assertions).
- Couple docs and tests: major behavior changes should update docs with intent and validation commands.
- For UI projects, include checks that cover real user workflows (manual exploration and automated regression where appropriate).

## Which testing reference to read next

- **CLI-heavy projects**: use `cli.md` for Typer/Click conventions and command testing patterns.
- **Web UI / JS/TS / Streamlit projects**: use `web-ui-e2e.md` for Playwright CLI exploration and regression E2E guidance.

## Related references

- `../web.md` for frontend stack defaults and broader web conventions.
- `../python.md` for Python/UV/workspace conventions (including Streamlit context).
- `../resources.md` for external source links.

## Notes

- Playwright tool-specific excerpts and source-backed best practices are intentionally kept in `web-ui-e2e.md` so this file stays compact and reusable.
