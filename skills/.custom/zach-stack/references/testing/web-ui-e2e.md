# Web UI E2E testing (`zach-stack`)

## Frontend checks

- For UI work, include interaction-level validation against real page behavior (manual Playwright flow check and automated checks where feasible).

## Web UI E2E strategy (JS/TS and Streamlit)

Use this for any project with a browser UI (JS/TS apps, Streamlit apps, mixed Python/web tools).

### Default workflow (opinionated)

1. Start the app locally in a realistic mode (real routing, real forms, representative data if possible).
2. Use `playwright-cli` first to explore the app manually from the terminal and thoroughly exercise journeys before writing tests.
3. Record what breaks, what is flaky, and which selectors/roles are stable.
4. Promote critical journeys into regression tests.
5. Keep a small, reliable E2E suite in CI; keep wider exploration as an on-demand debugging workflow.

### Codex skill usage (`$playwright`)

- Prefer the `$playwright` skill (if installed) for CLI-first browser exploration and fast test drafting.
- If `$playwright` is not installed, use `$skill-installer` to install the `playwright` skill, then restart Codex so it becomes available.
- Use the skill to explore real user flows, identify robust selectors/roles, and draft candidate regression tests before codifying stable tests in the project.

### Exploration-first checklist (before codifying tests)

Use `playwright-cli` to intentionally try multiple journeys, not just the happy path:

- primary task success path (the user outcome that matters most)
- validation failures and inline error states
- reload/back/forward behavior
- empty/loading/error data states
- auth/session-expiry/logged-out behavior (if applicable)
- multi-step flows and resumability
- keyboard navigation and submit behavior
- responsive viewport spot checks for key screens
- file upload/download flows (if applicable)
- repeated actions/reruns (important for Streamlit rerender behavior)

### What to codify as regression tests

Promote flows that are both user-critical and likely to regress:

- sign-in/sign-out and session guards
- highest-value form submissions
- navigation paths across major pages/screens
- stateful interactions (filters, sort, pagination, wizards)
- data-visualization controls and drill-downs (common in Streamlit)
- any bug you just fixed (reproduce -> test -> verify)

Do not try to codify every exploratory check. Keep the automated suite focused, deterministic, and fast enough to run regularly.

### JS/TS projects: standard Playwright tests

- Use `@playwright/test` for regression coverage.
- Prefer role-, label-, and test-id-based locators over brittle CSS selectors.
- Assert user-visible outcomes (URL changes, visible text, enabled/disabled states, table/chart updates), not implementation details.
- Capture traces/screenshots/video on failures in CI for debuggability.
- Add one smoke path early, then expand only after real bugs or product risk justify more coverage.

### Streamlit / Python web UI projects: Playwright + pytest

- Use Playwright Python with `pytest` (Playwright's pytest plugin is the default path for Python-side E2E).
- Run the app in a test fixture (or dedicated test command) and point browser tests at the local URL.
- Favor stable selectors (roles, labels, text contracts, `data-testid` where needed) because Streamlit reruns can re-render DOM nodes.
- Assert post-rerun visible state, not transient intermediate DOM structure.
- Keep long data-loading paths deterministic with seeded fixtures or mocked upstream data where practical.

### Test quality rules

- One test = one user intent.
- Avoid hidden inter-test dependencies; each test should be runnable alone.
- Prefer explicit setup helpers/fixtures over giant end-to-end mega-tests.
- Stabilize selectors before adding retries/timeouts.
- When a test flakes, fix the cause (selector/wait/data isolation) before expanding coverage.

### Docs coupling for E2E work

- When adding or changing E2E tests, update project docs with:
  - how to start the app under test
  - the exploration command/workflow (Playwright CLI / `$playwright` skill)
  - the regression test command (`pnpm playwright test`, `pytest`, etc.)
  - what critical journeys are intentionally covered vs left exploratory

## Source excerpts (for this guidance)

Relevant excerpts from primary docs and the installable skill docs.

- `microsoft/playwright-cli` README: "If you are using coding agents, that is the best fit!" Source: https://github.com/microsoft/playwright-cli
- Playwright skill docs (`$playwright`): "Drive a real browser from the terminal using `playwright-cli`." Source: https://skills.sh/openai/skills/playwright
- Playwright best practices: "Each test should be completely isolated from another test..." Source: https://playwright.dev/docs/best-practices
- Playwright writing tests: "Playwright automatically waits for actionability checks to pass..." Source: https://playwright.dev/docs/writing-tests
- Playwright Python pytest plugin docs: "Playwright provides a Pytest plugin to write end-to-end tests." Source: https://playwright.dev/python/docs/test-runners
