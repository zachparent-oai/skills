# Python conventions (`zach-stack`)

## Scope
Use for Python-heavy or mixed repos with Python services/modules.

## Tooling defaults

- Use `uv` for dependency/developer workflow.
- Prefer workspace separation when there are multiple independent Python modules.
- Use a dedicated `workspace` structure when teams need clean boundaries for CLI, service, library, and jobs.

## CLI conventions

- Prefer **Typer** for new CLI development.
- Accept **Click** when existing codepaths or existing teams standardize on Click.
- Keep CLI entrypoints near interfaces and minimize coupling to service internals.
- Make scripts standalone where practical:
  - put CLI dependency declarations in the nearest packaging boundary
  - avoid importing large module stacks at module import time
  - keep defaults explicit to reduce runtime surprises

## App architecture recommendations

- If data is consumed by both core services and visualization:
  - create a separate data workspace/project for shared contracts and loaders
  - create separate consumer workspaces (for example API layer, Streamlit app)
- For data visualization: use Streamlit + Plotly.
- If the project is small and one-purpose, keep one workspace and add explicit module boundaries.

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
