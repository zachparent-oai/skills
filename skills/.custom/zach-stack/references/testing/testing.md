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

- **CLI-heavy projects**: use `./cli.md` for Typer/Click conventions and command testing patterns.
- **Web UI / JS/TS / Streamlit projects**: use `./web-ui-e2e.md` for Playwright CLI exploration and regression E2E guidance.

## Focused testing references

- `./cli.md` for command-line testing patterns (`Typer`/`Click`, `CliRunner`, script command shape).
- `./web-ui-e2e.md` for browser E2E exploration and regression guidance using `playwright-cli`, Playwright JS/TS, and Playwright Python + `pytest`.

## Related references

- `../web.md` for frontend stack defaults and broader web conventions.
- `../python.md` for Python/UV/workspace conventions (including Streamlit context).
- `../resources.md` for external source links.

## Key external docs (Playwright)

- [Playwright CLI README (`microsoft/playwright-cli`)](https://github.com/microsoft/playwright-cli): terminal-driven browser exploration and automation.
- Playwright docs:
  - [Docs home](https://playwright.dev/docs/intro)
  - [Writing tests](https://playwright.dev/docs/writing-tests)
  - [Best practices](https://playwright.dev/docs/best-practices)
  - [Locators](https://playwright.dev/docs/locators)
  - [Actionability / auto-waiting checks](https://playwright.dev/docs/actionability)
- Playwright Python docs:
  - [Docs home](https://playwright.dev/python/docs/intro)
  - [Pytest plugin / test runners](https://playwright.dev/python/docs/test-runners)
  - [Locators](https://playwright.dev/python/docs/locators)
