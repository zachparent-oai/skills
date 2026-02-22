---
name: evals
description: "Create and maintain eval datasets and eval harnesses for prompts, agents, guardrails, and related systems, including golden-set-first workflows, augmentation pipelines, subset-first execution, and Streamlit eval UIs."
---

# Evals

Use this skill when work involves building or improving evals for prompts, agents, guardrails, classifiers, or tool-using systems.

It covers dataset creation/augmentation (CSV and JSON), harness design and maintenance, cost-aware execution strategy, prompt-improvement loops, and a Streamlit app pattern for running and viewing evals.

## Core workflow

1. Start with a small golden dataset (often 10-50 cases).
2. Get the harness working on 1-5 rows and then tiny batches.
3. Add scoring, logging, and failure review before scaling.
4. Add augmentation via committed scripts/configs (not ad hoc prompts).
5. Run larger datasets later, after subset runs are stable and interpretable.

## Defaults and guardrails

- Keep one human-editable golden source and generate alternate formats with scripts.
- Support both CSV and JSON (or JSONL) dataset forms; do not hand-maintain derived files.
- Prefer long-lived repo scripts for augmentation, conversion, and eval runs.
- Commit augmentation prompts, model IDs, config, seeds, and parameter grids.
- Add provenance fields to generated rows so datasets can be regenerated.
- Add subset controls (`--ids`, `--limit`, `--sample-seed`, `--category`) before full runs.
- Save run artifacts with a run ID: config, inputs, outputs, scores, and traces.
- Separate prompt-tuning loops from final holdout evaluation to reduce overfitting.

## When to read which reference

- `references/datasets.md`: dataset schemas, CSV/JSON strategy, augmentation and regeneration.
- `references/harnesses.md`: harness structure, subset-first execution, metrics, and hill-climb loops.
- `references/streamlit-evals-app.md`: recommendations and a Streamlit template for running/viewing evals.
- `$zach-stack`: shared Python/CLI defaults (Typer), Streamlit + Plotly guidance, and workspace boundary conventions.

## Asset template

- `assets/streamlit_evals_app_template.py`: starter Streamlit app for local eval runs and result review.
