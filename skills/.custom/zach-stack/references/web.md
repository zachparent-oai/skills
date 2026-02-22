# Web conventions (`zach-stack`)

## Scope
Use when a project includes frontend code and needs a consistent, lightweight stack.

## Conventions

- Use lightweight, framework-free implementations for simple pages.
- For dynamic client behavior, prefer lightweight React over heavy abstraction layers.
- For quick prototypes/static pages, prefer Tailwind CLI or a minimal stylesheet pipeline.
- For production apps, use `pnpm` as the package manager and wire Tailwind into the project build (not Play CDN).
- For content-heavy or markdown-driven complex static sites, prefer Eleventy.
- Workspace/monorepo-specific `pnpm` details live in [workspaces.md](workspaces.md).
- Keep browser-facing code testable with at least:
  - unit-level checks for pure functions/components (or equivalent)
  - integration tests for user flows
  - end-to-end checks for critical UI paths

## Playwright and checks

- For interactive UI exploration and triage, use Playwright CLI first (`codegen`, inspector, `--debug`) to understand the page and generate resilient locators.
- For stable e2e coverage, standardize on Playwright-based automation in CI for key flows.
- For Python-facing web UIs, include the Python Playwright stack where helpful.
- Keep selectors and test semantics resilient to refactors by preferring user-facing locators and web-first assertions.

## Decision points

- If no interactive state and no component orchestration are needed: no React.
- If there are interactive widgets, state-driven forms, or realtime updates: use React.
- If you only need to demo styles quickly in a single HTML file: Tailwind Play CDN is acceptable for development only.
- If the site is heading toward production deployment: switch to a real Tailwind build path before shipping.

## Source-backed notes

### Playwright test style

- Source: [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- Excerpt (short): "Test user-visible behavior."
- Why it matters for zach-stack: reinforces the preference for flow-level tests that behave like users, not DOM-structure assertions.
- Practical implication: prioritize `getByRole`/text/test-id locators and assertions on visible outcomes for CI-critical flows.

- Source: [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- Excerpt (short): "Use locators."
- Why it matters for zach-stack: Playwright locators include auto-waiting and retry behavior, which improves test reliability.
- Practical implication: avoid brittle CSS/XPath selectors in default examples unless there is no stable user-facing locator.

- Source: [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- Excerpt (short): "Use web first assertions."
- Why it matters for zach-stack: web-first assertions reduce flaky timing failures in UI tests.
- Practical implication: prefer `await expect(locator).toBeVisible()` style assertions over manual immediate checks.

### Tailwind setup choices

- Source: [Tailwind CLI Installation](https://tailwindcss.com/docs/installation/tailwind-cli)
- Excerpt (short): "The simplest and fastest way ... is with the Tailwind CLI tool."
- Why it matters for zach-stack: supports the lightweight default for simple pages and prototypes.
- Practical implication: start with Tailwind CLI for minimal web scaffolds before introducing heavier framework build integration.

- Source: [Tailwind Play CDN](https://tailwindcss.com/docs/installation/play-cdn)
- Excerpt (short): "designed for development purposes only, and is not intended for production."
- Why it matters for zach-stack: clarifies when Play CDN is acceptable and prevents accidental production defaults.
- Practical implication: use Play CDN only for throwaway demos/prototypes; migrate to a build pipeline for production.

### Eleventy baseline

- Source: [Eleventy Getting Started](https://www.11ty.dev/docs/)
- Excerpt (short): "If ... lower than 18, you will need to download and install Node.js..."
- Why it matters for zach-stack: Eleventy remains a good static-site default, but Node runtime constraints should be checked early.
- Practical implication: confirm Node version (>=18 per current docs) before recommending Eleventy scaffolding.
