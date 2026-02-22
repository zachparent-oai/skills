# Streamlit app for evals (run + view)

## Purpose

Use a Streamlit app when you need a lightweight local UI for:

- running eval subsets quickly
- comparing run summaries
- filtering failures by category/tag
- inspecting row-level outputs and traces

This is most useful after the harness CLI exists and writes structured artifacts.

## Shared conventions (existing docs)

Read `$zach-stack` first, then load the relevant Python/workspace references inside that skill for:

- Streamlit + Plotly app conventions
- data/harness/UI boundary guidance
- CLI defaults (Typer) that the Streamlit app can call or mirror

## Template

Use `assets/streamlit_evals_app_template.py` as a starting point. It includes:

- CSV/JSON/JSONL dataset loading
- subset controls (`limit`, `sample-seed`, category filter)
- a harness function stub to replace with repo-specific logic
- summary metrics and Plotly charts
- row-level results table and detail viewer

## Recommended architecture

- Keep Streamlit as a thin UI layer.
- Put eval execution in reusable harness code or a stable CLI wrapper.
- Reuse the same dataset loaders and scorer logic used in CLI runs.
- Write run artifacts to disk with a run ID so the UI and CLI results are comparable.

## Implementation notes

- Use `st.cache_data` for dataset loading and derived summaries.
- Use `st.session_state` to keep the most recent results.
- Make subset controls explicit and default to small values.
- Add a clear "Run full dataset" action only after the harness is stable.
- Provide export buttons for failures (`CSV`, optionally `JSONL`).

## Typical enhancements after the template

- compare two run IDs side-by-side
- drill into agent traces/tool calls
- save "interesting failures" tags for follow-up
- rerun selected failed cases with a different prompt/model
- track latency and cost charts by category

## Anti-patterns

- embedding all harness logic directly in the Streamlit file
- making full-dataset runs the default button action
- hiding eval config details from the UI
- showing only aggregate pass rate without row-level inspection
