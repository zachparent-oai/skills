# `.codex/rules/default.rules` guidance

## Principles

- Keep permissions scoped to the project workflow.
- Prefer minimal, explicit commands.
- Ask before writing any potentially sensitive settings.

## Typical command families

- `uv`: Python install/test/runtime commands
- `just`: repeated repo task orchestration
- `pnpm`: node tooling for web apps
- `gh`: GitHub workflows and issue/pr management
- `glab`: GitLab/GLab workflow parity where used

## Process

- Propose a diff, confirm with user, then apply.
- Re-check the rule set after each commit boundary.
## Example `prefix_rule` syntax

```python
prefix_rule(
    pattern = ["uv", "sync"],
    decision = "allow",
    justification = "Allow project dependency sync outside sandbox",
    match = [
        "uv sync",
        "uv sync --locked",
    ],
    not_match = ["uv run sync"],
)
```

Use `match` and `not_match` as inline rule tests so malformed patterns fail fast when the rule file is loaded.

## Validate the rules file

Run a rule check after updating `default.rules`:

```bash
codex execpolicy check --pretty --rules .codex/rules/default.rules -- uv sync
```

Use the same command for any command you changed in the allow list.

## Review checklist (after edits)

- Syntax/load check: run `codex execpolicy check` for each newly allowed command family.
- Positive check: verify at least one intended command now matches/loads successfully.
- Negative check: verify a nearby command that should remain blocked is still denied (or does not match the new rule).
- Scope check: confirm whether the change was applied to repo-scoped `.codex/rules/default.rules` or user-level `$CODEX_HOME/rules/default.rules`, and note why.
- Rollback note: record the exact rule entries added/changed so they can be removed quickly if behavior is too broad.
