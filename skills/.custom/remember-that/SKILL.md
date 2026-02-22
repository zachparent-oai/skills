---
name: remember-that
description: "Capture reusable rules or concepts learned from the user or during repo work, and persist them in the right docs file or root AGENTS file (kept light)."
---

# Remember That

Use this skill when a generalizable rule, convention, or concept is learned and should be written down for future work.

## When to use

- A user states a reusable rule or preference ("always do X", "remember that Y").
- You discover a repeatable repo workflow rule while working.
- You notice a general lesson that will likely help future tasks in this repo.

## Goal

Capture durable guidance in the narrowest useful place so future agents and collaborators can apply it consistently.

## Target selection (brief)

- Prefer updating an existing docs file that already covers the topic.
- Prefer skill-specific `references/*.md` when the rule applies to one skill or workflow.
- Create a focused `docs/<topic>.md` file when the rule is repo-level and no suitable doc exists.
- Use the root [`AGENTS` file](../../../AGENTS.md) only for repo-wide agent behavior, constraints, or high-signal workflow rules.
- Keep the root [`AGENTS` file](../../../AGENTS.md) concise; avoid long rationale/history.

## Workflow

1. Extract the rule in actionable language (context + action + constraints).
2. Choose the right destination file.
3. Check for an existing matching rule to avoid duplication.
4. Draft concise wording with concrete triggers and expected behavior.
5. Update/create the doc when requested.
6. Reference the updated file path in the response.

## References

- `references/capture-guidelines.md` for a decision rubric, anti-patterns, and templates.
