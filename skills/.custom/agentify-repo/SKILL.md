---
name: agentify-repo
description: "Incrementally add harness and tooling to an existing repo so it converges toward zach-stack safely over multiple passes."
---

# Agentify Repo

Use this skill when asked to make an existing repo more agent-friendly without one-shot rewrites.

## Core goal

Set up harness/tooling in small, reversible steps that make the repo more verifiable and easier for agents to work with.

## Recommended flow

1. Baseline assessment: detect current stack, docs state, tests, lints, and CI.
2. Harness setup phase: add/update only low-risk structure first (`docs/`, `Justfile`, command discoverability, test map).
3. Apply `zach-stack`-aligned improvements in small batches:
   - tooling defaults relevant to current stack
   - testing additions by priority
   - docs upkeep and file ownership mapping
4. Validate each phase.
5. Pause with explicit next milestone.

## Hard rules

- No broad migration in one run unless explicitly authorized.
- Prefer additive changes and stable commit points.
- If unknown/legacy constraints exist, defer and document them instead of forcing defaults.
- Ask before any environment or rules-file changes that require trust-sensitive decisions.

## References

- `references/incremental-harness.md`
- `references/convergence-phases.md`
- `references/rollback-and-safety.md`
- `../zach-stack` for target conventions.
