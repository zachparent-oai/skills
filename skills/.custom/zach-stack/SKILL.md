---
name: zach-stack
description: "Define opinionated conventions for testable, well-documented, agent-friendly repos. Use for stack selection and application defaults."
---

# Zach-Stack

Use this skill when asked to define or apply a preferred stack for a new/existing project.

## Purpose

`zach-stack` is the compact decision source for:
- project scaffolding defaults
- tooling conventions
- test strategy expectations
- docs/lifecycle defaults
- Codex-friendly repository structure

## When to use

- before or during `init-repo`
- during `agentify-repo` as the target conventions
- when a team member asks for your preferred stack defaults

## Core rules (high signal)

- **Minimal web by default**: prefer plain HTML/CSS/JS when requirements are simple.
- **Dynamic web**: choose a lightweight React setup when needed for stateful interactions.
- **JS/TS app tooling**: prefer Vite for new browser apps (especially React) unless framework-specific tooling is required.
- **Complex static sites**: prefer Eleventy.
- **CSS**: default to Tailwind.
- **Python work**: use `uv` for package management and virtual environments.
- **Workspaces**: prefer workspace-based organization for multi-module projects.
- **CLI stack**: prefer **Typer** for new CLIs; use **Click** when existing codebases already use it.
- **Testing**: add targeted unit tests and at least one integration/acceptance layer.
- **Frontend checks**: include automated checks that cover real user workflows.
- **Playwright path**: use Playwright CLI for exploration and flow debugging; use Playwright-driven E2E where applicable.
- **Visualization**: prefer Streamlit + Plotly for analytics UI.
- **Project shape for shared data**: use a dedicated workspace/module for data, plus workspace boundaries for Streamlit/compute when needed.
- **Standalone scripts**: keep CLIs standalone with minimal dependencies and explicit script-level dependency boundaries; keep CLIs minimally scoped.
- **Docs as source of truth**: every project must have `docs/` and keep it current with code changes.
- **Automation**: include `Justfile` in most repos for repeatable agent tasks.
- **Pre-commit**: always define pre-commit via project-native tooling (`pnpm` or `uv`).

## Process

1. Ask for project intent: web app, python service, data app, or mixed.
2. Select a minimal stack from these preferences.
3. Confirm constraints that override defaults (security, infra, legacy platform).
4. Apply only what is relevant for the project phase.

For implementation details and version-sensitive guidance, load the source-backed notes in the relevant `references/*.md` files instead of relying on memory.

## Reference usage map

- Use `references/web.md` when choosing plain HTML/JS vs React, Tailwind setup shape, or Playwright usage patterns.
- Use `references/python.md` for `uv`, Typer/Click tradeoffs, Streamlit/Plotly defaults, and Python workspace structure.
- Use `references/testing/testing.md` first for testing principles and routing to CLI vs browser E2E guidance.
- Use `references/testing/cli.md` for CLI testing conventions and command-style examples.
- Use `references/testing/web-ui-e2e.md` for Playwright CLI exploration and browser E2E guidance.
- Use `references/docs.md` for living-docs expectations and completion criteria.
- Use `references/workspaces.md` when deciding whether to split modules/workspaces now or later.
- Use `references/resources.md` when you need upstream sources or a quick pointer to official docs.

## References

- `references/web.md` for web defaults, CSS, and Playwright use.
- `references/python.md` for UV, workspace, and Python conventions.
- `references/testing/testing.md` for test principles and routing by project type.
- `references/testing/cli.md` for CLI testing conventions.
- `references/testing/web-ui-e2e.md` for Playwright/browser E2E workflows (JS/TS and Streamlit/Python).
- `references/docs.md` for living docs patterns.
- `references/workspaces.md` for shared workspaces in mixed stacks.
- `references/resources.md` for external source references.
