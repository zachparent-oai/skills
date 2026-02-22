# Eval harnesses (build small, then scale)

## Purpose

Use this guide when writing or maintaining an eval harness for prompts, agents, or guardrails.

The harness should make runs repeatable, debuggable, and cheap to iterate on.

## Harness design goals

- deterministic enough to compare runs
- easy to run on tiny subsets
- explicit about configs and versions
- clear outputs for failure review
- scalable to larger datasets later

## Build order (practical)

1. One-row smoke path
2. Tiny batch path (5-10 rows)
3. Scorer/grader validation
4. Structured run artifact writing
5. Category/split subset controls
6. Parallelization and larger batch runs

Do not start with full-dataset runs.

## Recommended project layout (adapt to repo)

```text
evals/
  datasets/
    golden.csv
    golden.jsonl
    augmented/
  prompts/
    system_prompt_v1.txt
    augmentation_prompt_v1.txt
  configs/
    eval.default.yaml
    augment.default.yaml
  scripts/
    run_evals.py
    augment_eval_dataset.py
    convert_eval_dataset.py
  runs/
    2026-02-22T101500Z_local-smoke/
      config.json
      results.jsonl
      summary.json
      failures.csv
```

## Harness responsibilities

The eval harness should usually do all of the following:

- load dataset rows (CSV/JSON/JSONL)
- apply subset filters (`ids`, `category`, `split`, `limit`, sampled subset)
- run the system under test (prompt, agent, or guardrail)
- score results with a grader (exact match, label, rubric, model grader, trajectory checks)
- persist structured artifacts
- emit a summary for quick comparison

## Minimum run artifact set

Write artifacts on every run, even small ones:

- `config.json` (model, prompt version, grader config, subset filters)
- `results.jsonl` (row-level outputs and scores)
- `summary.json` (pass rate and aggregate metrics)
- `failures.csv` (easy to review and share)

For agent evals, also persist traces/tool calls if available.

## Subset-first execution policy

Treat subset runs as the default during development:

- smoke: `--limit 1`
- debug: `--ids ...`
- tiny slice: `--limit 10 --category ...`
- sampled slice: `--limit 50 --sample-seed 13`

Only run the large dataset after:

- the harness runs without crashes
- the scorer outputs look sane
- artifacts are being written correctly
- failure review is actually usable

## Scoring and grading notes

- Start with the simplest grader that matches the task.
- Prefer deterministic checks first (exact/label/regex/schema) before model graders.
- If you use model graders, version and log their prompts/configs too.
- Keep grader outputs structured (`pass`, `score`, `reason`, `tags`).

## Maintenance guidelines

- Keep prompts and model configs versioned in files, not buried in code literals.
- Add regression cases whenever you fix a failure mode.
- Separate train/tuning vs holdout/final-eval rows.
- Avoid silently changing schemas; use a schema version field.
- Keep the harness CLI stable so CI/nightly jobs and Streamlit UI can call it.

## Prompt improvement loops (hill climbing)

Use automated loops carefully. The goal is to improve prompts without overfitting.

### Recommended loop

1. Split data into `train` (tuning) and `holdout` (confirmation).
2. Generate prompt candidates (manual edits or model-proposed variants).
3. Run candidates on a limited training subset first.
4. Keep the top candidates by score and failure profile.
5. Confirm winners on holdout before promoting.
6. Save the promoted prompt as a versioned file and record the run IDs.

### Hill-climb safeguards

- Never optimize only on the final holdout.
- Track per-category metrics, not only global pass rate.
- Review failure examples before accepting a change.
- Keep cost controls (subset, caps, concurrency) in the loop.
- Stop when gains are noise or regress key categories.

## Agents and guardrails specifics

For agent or guardrail evals, add fields and artifacts for:

- tool call validity
- refusal correctness
- policy tag matches
- trajectory-level success/failure
- latency and token cost

A label-only pass rate can hide agent regressions. Persist enough detail to debug behavior.
