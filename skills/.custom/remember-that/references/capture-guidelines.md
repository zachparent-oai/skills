# Capture guidelines (`remember-that`)

## Decision rubric: where should the rule live?

- **Existing docs file**: Use when the rule belongs to a current topic (testing, deployment, repo workflow, etc.).
- **Skill `references/*.md`**: Use when the rule applies to a specific skill or a narrow workflow.
- **`docs/<topic>.md`**: Use when the rule is repo-level, reusable, and no existing doc is a good fit.
- **Root [`AGENTS` file](../../../../AGENTS.md)**: Use only for repo-wide agent behavior, constraints, and compact operating rules.

## What makes a good rule worth saving?

- It has a clear trigger/context.
- It specifies an action or default behavior.
- It includes constraints or exceptions when they matter.
- It is likely to be reused across future tasks.

## Anti-patterns (do not save these)

- One-off debugging observations that will not recur.
- Temporary status notes or task-specific progress logs.
- Long narratives explaining the history of a decision in the root [`AGENTS` file](../../../../AGENTS.md).
- Vague reminders without a clear trigger or action.

## Writing pattern

Use short, operational wording:

- **Context/trigger**: when this applies
- **Default action**: what to do
- **Constraint/exception**: what changes the default

## Mini templates

### Repo workflow rule

- When updating a custom skill, edit `skills/.custom/<skill>` first, then run sync to refresh `.codex/skills/<skill>`.

### Tool usage convention

- For browser UI triage, start with `playwright-cli` exploration, then codify stable regressions in Playwright tests.

### Skill-specific testing convention

- Keep the skill `SKILL.md` short and put detailed examples in `references/` files linked from `SKILL.md`.

## Success tips

- Prefer editing the narrowest relevant file over adding broad AGENTS rules.
- Merge related rules into existing docs sections instead of creating scattered tiny notes.
- If adding to the root [`AGENTS` file](../../../../AGENTS.md), keep the rule high-signal and implementation-agnostic.
