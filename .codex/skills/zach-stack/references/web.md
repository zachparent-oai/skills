# Web conventions (`zach-stack`)

## Scope
Use when a project includes frontend code and needs a consistent, lightweight stack.

## Conventions

- Use lightweight, framework-free implementations for simple pages.
- For dynamic client behavior, prefer lightweight React over heavy abstraction layers.
- Use Tailwind for styling defaults.
- For content-heavy or markdown-driven complex static sites, use Eleventy.
- Use `pnpm` as package manager by default for web tooling.
- Keep browser-facing code testable with at least:
  - unit-level checks for pure functions/components (or equivalent)
  - integration tests for user flows
  - end-to-end checks for critical UI paths

## Playwright and checks

- For interactive UI exploration and triage, use Playwright CLI first.
- For stable e2e coverage, standardize on Playwright-based automation in CI for key flows.
- For Python-facing web UIs, include the Python Playwright stack where helpful.
- Keep selectors and test semantics resilient to refactors.

## Decision points

- If no interactive state and no component orchestration are needed: no React.
- If there are interactive widgets, state-driven forms, or realtime updates: use React.
