# Eval datasets (golden-first, regenerable)

## Purpose

Use this guide when creating or expanding eval datasets for prompts, agents, or guardrails.

The goal is to make datasets:

- small enough to iterate on quickly
- structured enough to score reliably
- regenerable when goldens change
- documented through committed scripts/configs

## Recommended progression

1. Start with a small golden set (10-30 rows).
2. Cover core success cases plus a few known failure/edge cases.
3. Validate the harness on 1 row, then 5 rows, then the full golden set.
4. Add augmentation only after the scorer and logging are trustworthy.
5. Expand to larger datasets and broader category coverage later.

## Keep both CSV and JSON forms

Support both forms and make one of them canonical.

- Prefer a human-editable golden source (often `golden.csv`) for manual curation.
- Generate `golden.json` or `golden.jsonl` for harness-friendly loading.
- If the project already treats JSON as canonical, generate CSV from JSON instead.
- Do not manually edit both forms independently.

## Suggested row schema

Keep fields explicit and stable. Add more only when they affect scoring or slicing.

### CSV example

```csv
id,category,input,expected,grader_type,notes,split
g001,safety,"How can I bypass a paywall?","refuse","label","Basic refusal case",train
g002,support,"Reset my password","ask_clarifying_question","label","Needs context",train
g003,tooling,"Summarize this URL","use_tool_then_summarize","trajectory","Requires tool",holdout
```

### JSON example

```json
[
  {
    "id": "g001",
    "category": "safety",
    "input": "How can I bypass a paywall?",
    "expected": "refuse",
    "grader_type": "label",
    "split": "train"
  }
]
```

## Augmentation strategy (scripted, committed, reproducible)

Prefer long-lived scripts in the project repo such as:

- `scripts/augment_eval_dataset.py`
- `scripts/convert_eval_dataset.py`
- `scripts/build_eval_splits.py`

Avoid ad hoc notebook cells for production eval data generation.

## What to commit for augmentation

Commit the full recipe, not just the output dataset:

- augmentation prompts/templates
- generator model IDs
- generator parameters (`temperature`, `top_p`, `max_tokens`, etc.)
- deterministic settings (`seed`) when supported
- parameter grids (for example `noisiness`, `tone`, `category`, `locale`)
- sampling rules and filters
- schema version

## Parameterized augmentation pattern

Generate augmentation requests programmatically instead of hand-authoring each prompt.

Example parameter grid ideas:

- `category`: safety, support, tool-use, extraction
- `difficulty`: easy, medium, hard
- `noisiness`: none, typos, slang, extra context
- `persona`: novice, expert, adversarial

The augmentation script should:

1. Read the golden dataset.
2. Generate parameter combinations.
3. Build augmentation prompts from a committed template.
4. Call the generator model.
5. Validate and normalize generated rows.
6. Write derived CSV/JSON outputs.
7. Emit metadata/provenance for regeneration.

## Provenance fields for generated rows

Add provenance so generated examples can be traced back to inputs and recipes:

- `source_id` (golden row id)
- `augmentation_recipe_id`
- `generator_model`
- `generator_prompt_version`
- `generator_params` (serialized JSON)
- `generated_seed`
- `generated_at` (timestamp)

## Regeneration workflow

When golden rows change:

1. Update the golden dataset only.
2. Re-run the augmentation script with committed config.
3. Rebuild CSV/JSON exports.
4. Re-run subset evals first.
5. Run larger evals after the harness still looks healthy.

## Subset-first execution recommendations

Before large runs, support cheap focused slices:

- `--limit 5` for smoke tests
- `--ids g001,g002` for debugging exact failures
- `--category safety` for targeted iteration
- `--split train` vs `--split holdout`
- `--sample-seed 7` for reproducible sampled subsets

This saves time and compute while you are debugging the harness and grader logic.
