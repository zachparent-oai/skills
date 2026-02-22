# Python conventions (`zach-stack`)

## Scope
Use for Python-heavy or mixed repos with Python services/modules.

## Tooling defaults

- Use `uv` for dependency/developer workflow.
- Prefer workspace separation when there are multiple independent Python modules with distinct responsibilities.
- Use a dedicated `workspace` structure when teams need clean boundaries for CLI, service, library, and jobs.
- For single-purpose repos, start with one `pyproject.toml` and split later only when boundaries are real.

## CLI conventions

- Prefer **Typer** for new CLI development.
- Accept **Click** when existing codepaths or existing teams standardize on Click.
- Keep CLI entrypoints near interfaces and minimize coupling to service internals.
- Use Typer subcommands when the tool has multiple stable actions; keep single-purpose tools as a default command entrypoint.
- Make scripts standalone where practical:
  - put CLI dependency declarations in the nearest packaging boundary
  - avoid importing large module stacks at module import time
  - keep defaults explicit to reduce runtime surprises

## App architecture recommendations

- If data is consumed by both core services and visualization:
  - create a separate data workspace/project for shared contracts and loaders
  - create separate consumer workspaces (for example API layer, Streamlit app)
- For data visualization: use Streamlit + Plotly.
- If the project is small and one-purpose, keep one workspace/project and add explicit module boundaries.
- Keep Streamlit app and backend together initially if the app is thin and owned by one team; split when shared contracts or release cadence diverge.

## Streamlit eval and analytics app guidance

- Keep Streamlit as a thin UI over stable data loaders and eval/harness modules.
- Default UI actions to small subset runs first (`limit`, category filter, sample seed).
- Reuse the same run artifact formats as CLI eval runs (config, results, summary, failures).
- Prefer Plotly charts for pass-rate and latency/cost breakdowns by category.
- Persist run IDs and expose row-level failure inspection, not only aggregate metrics.
- Reserve large/full-dataset runs for an explicit action after the harness is stable.

## Maintenance and tests

- Keep unit tests near implementation modules.
- Add integration tests for external boundaries (HTTP handlers, file contracts, job inputs).

## Source-backed notes

### uv project and workspace structure

- Source: [uv Project Structure and Files](https://docs.astral.sh/uv/concepts/projects/layout/)
- Excerpt (short): "uv requires this file to identify the root directory of a project."
- Why it matters for zach-stack: reinforces `pyproject.toml` as the Python project boundary and the natural place to start.
- Practical implication: start with one project root and only introduce a workspace when multiple `pyproject.toml` members are justified.

- Source: [uv Project Structure and Files](https://docs.astral.sh/uv/concepts/projects/layout/)
- Excerpt (short): "uv creates a `uv.lock` file next to the `pyproject.toml`."
- Why it matters for zach-stack: supports the convention of checking in a lockfile for reproducible developer and CI environments.
- Practical implication: treat `uv.lock` as part of the normal project scaffold and update it intentionally.

- Source: [uv Using Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- Excerpt (short): "Every workspace needs a root, which is also a workspace member."
- Why it matters for zach-stack: clarifies the shape of uv workspaces and avoids hand-wavy "workspace" guidance.
- Practical implication: when splitting into workspaces, define a clear root project and document which commands run at root vs member level.

- Source: [uv Using Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- Excerpt (short): "By default, `uv run` and `uv sync` operates on the workspace root."
- Why it matters for zach-stack: command behavior changes once a repo becomes a workspace.
- Practical implication: document root vs member commands in `docs/` and `Justfile` to prevent confusion for agents.

### Typer conventions

- Source: [Typer First Steps](https://typer.tiangolo.com/tutorial/first-steps/)
- Excerpt (short): `ls` is the program (or "command", "CLI app").`
- Why it matters for zach-stack: Typer stays close to CLI ergonomics, which supports lightweight agent-facing tools.
- Practical implication: prefer Typer for new CLIs when you want fast, readable command definitions and help text.

- Source: [Typer Commands / SubCommands](https://typer.tiangolo.com/tutorial/commands/)
- Excerpt (short): "SubCommands - Command Groups"
- Why it matters for zach-stack: supports using subcommands only when the domain genuinely has multiple actions.
- Practical implication: keep single-action tools simple; use grouped subcommands when the command surface is stable and shared.

### Streamlit + Plotly defaults

- Source: [Streamlit Caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
- Excerpt (short): "`@st.cache_data`"
- Why it matters for zach-stack: data loading/transforms are common bottlenecks in analytics apps and should be cached deliberately.
- Practical implication: cache data queries/transforms by default (and consider `ttl` for changing upstream data).

- Source: [Streamlit Caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
- Excerpt (short): "`st.cache_resource` does not create a copy..."
- Why it matters for zach-stack: resource caching has different mutation/thread-safety behavior than data caching.
- Practical implication: use `st.cache_resource` for shared connections/models and keep thread-safety in mind.

- Source: [Streamlit Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- Excerpt (short): "The Session State API follows a field-based API..."
- Why it matters for zach-stack: interactive apps need explicit state, not hidden module globals.
- Practical implication: use `st.session_state` for user/session interaction state and initialize keys deterministically.

- Source: [Plotly Express in Python](https://plotly.com/python/plotly-express/)
- Excerpt (short): paraphrase: Plotly Express is the high-level, recommended starting API for common figures.
- Why it matters for zach-stack: matches the goal of fast iteration and readable analytics UI code.
- Practical implication: start visualization examples with `plotly.express as px`; move to graph objects only for advanced customization.
