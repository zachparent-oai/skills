# External references for `zach-stack`

Use this file as an annotated index when you need upstream docs to justify or refresh a `zach-stack` recommendation.

## Skills and agent workflow

- [Agent Skills homepage](https://agentskills.io/home)
  - Why: overview of the skills ecosystem and terminology.
- [Agent Skills specification](https://agentskills.io/specification)
  - Why: standards-based reference when structuring or validating skill layout decisions.
- [What are Skills?](https://agentskills.io/what-are-skills)
  - Why: concise explainer for skill-trigger/use framing.
- [Harness engineering at OpenAI](https://openai.com/index/harness-engineering/)
  - Why: background context for incremental harness/tooling improvements.
- [Testing Agent Skills with Evals](https://developers.openai.com/blog/eval-skills/)
  - Why: supports the eval-first quality mindset for reusable skills.

## Web and tooling docs

- [Playwright CLI (`microsoft/playwright-cli`)](https://github.com/microsoft/playwright-cli)
  - Why: source for terminal-driven browser exploration guidance before codifying regressions.
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
  - Why: source for resilient locator/assertion guidance in `web.md` and testing references.
- [Playwright Writing Tests](https://playwright.dev/docs/writing-tests)
  - Why: source for actionability/auto-waiting and test authoring guidance.
- [Playwright Python test runners (pytest plugin)](https://playwright.dev/python/docs/test-runners)
  - Why: source for Playwright Python + `pytest` guidance for Streamlit/Python web UIs.
- [Playwright Codex skill docs (installable via `$skill-installer`)](https://skills.sh/openai/skills/playwright)
  - Why: source for the `$playwright` skill framing and CLI-first exploration workflow.
- [Tailwind CLI Installation](https://tailwindcss.com/docs/installation/tailwind-cli)
  - Why: source for lightweight Tailwind setup guidance.
- [Tailwind Play CDN](https://tailwindcss.com/docs/installation/play-cdn)
  - Why: source for the "development only" caveat.
- [pnpm Workspaces](https://pnpm.io/workspaces)
  - Why: source for workspace structure and `workspace:` protocol behavior.
- [Eleventy Getting Started](https://www.11ty.dev/docs/)
  - Why: source for current Node baseline and quick-start expectations.

## Python and data app docs

- [uv Project Structure and Files](https://docs.astral.sh/uv/concepts/projects/layout/)
  - Why: source for `pyproject.toml`, `.venv`, and `uv.lock` guidance.
- [uv Using Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
  - Why: source for uv workspace root/member behavior.
- [Typer First Steps](https://typer.tiangolo.com/tutorial/first-steps/)
  - Why: source for CLI ergonomics and minimal setup framing.
- [Typer Commands / SubCommands](https://typer.tiangolo.com/tutorial/commands/)
  - Why: source for subcommand/group patterns.
- [Streamlit Caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
  - Why: source for `st.cache_data` vs `st.cache_resource` guidance.
- [Streamlit Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state)
  - Why: source for state initialization and session-scoped interaction handling.
- [Plotly Express in Python](https://plotly.com/python/plotly-express/)
  - Why: source for "high-level starting API" recommendation.

## Last reviewed

- 2026-02-22: web/tooling and Python/data-app source-backed notes refreshed for `zach-stack`.
