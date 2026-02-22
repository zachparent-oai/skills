# `configure-codex` handoff (`troubleshoot-sandbox`)

Use this file when sandbox troubleshooting indicates the user needs a persistent rules/config change rather than a one-off retry.

## When to invoke `$configure-codex`

- The same command family is repeatedly required for repo work and repeatedly blocked.
- The user wants a smoother recurring workflow (for example `uv sync`, `pnpm run build`, `just test`).
- The command needs repo-scoped or user-level rule decisions.
- The issue is not a missing tool/syntax problem and not solved by changing cwd/path.

## When *not* to invoke `$configure-codex`

- The command failed because the binary/tool is missing.
- The command failed due to wrong arguments or wrong cwd.
- The task only needs one one-off escalated run and the user does not want persistent rule changes.

## Handoff payload (what context to provide)

- repo type / stack (web, Python, mixed)
- exact command(s) needed (with representative variants)
- observed errors (including sandbox/approval text)
- current scope preference (repo-scoped vs user-level unknown / preferred)
- whether the command is recurring or one-off
- any constraints (security-sensitive repos, CI parity needs, minimal permissions preference)

## Recommended handoff phrasing

- "This looks like a recurring repo workflow command, not a syntax issue. Use `$configure-codex` to propose a minimal repo-scoped rule for `<command family>`."
- "This failure appears to be a rule/approval mismatch. Use `$configure-codex` to validate the current rule surface and propose a narrower `prefix_rule`."
- "If `.codex/rules` is not writable here, use `$configure-codex` to decide whether a user-level `$CODEX_HOME/rules/default.rules` update is appropriate."

## Approval prompt patterns (examples)

- "Do you want to allow `uv sync` outside the sandbox for this repo's dependency setup?"
- "Do you want repo-scoped rules only for `pnpm run` in this project, or should this be added to your user-level Codex rules?"
- "Do you want to allow `just test` for this repo's validation workflow, or keep test runs manual for now?"

## Source-backed notes

- Source: [Codex Rules](https://developers.openai.com/codex/rules)
- Excerpt (short): paraphrase: rules can be written and validated with explicit command matching behavior.
- Why it matters for handoff: `configure-codex` should receive exact commands and intended scope, not vague "make it work" requests.
- Practical implication: pass representative command examples and minimal scope requirements.

- Source: [Codex Config Reference](https://developers.openai.com/codex/config-reference)
- Excerpt (short): paraphrase: config profiles/settings can change runtime behavior across environments.
- Why it matters for handoff: persistent fixes may belong in repo config, user config, or rules depending on the failure.
- Practical implication: include environment/scope context when requesting `configure-codex`.

## Skill references

- `$configure-codex` for the guarded workflow and scope decisions.
- Within `$configure-codex`, read the rules defaults reference for rule syntax and validation.
- Within `$configure-codex`, read the allowed-commands matrix for minimal command family selection.
- Within `$configure-codex`, read the codex environment reference for repo-vs-user setup guidance.
