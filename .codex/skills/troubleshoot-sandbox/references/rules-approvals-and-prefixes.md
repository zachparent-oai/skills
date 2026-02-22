# Rules, approvals, and prefixes (`troubleshoot-sandbox`)

Use this file when a command is blocked, unexpectedly denied, or repeatedly needs escalation.

## What to distinguish first

- One-time sandbox block that is appropriate for focused escalation
- Repeated workflow command that should be covered by repo/user rules
- Missing binary / bad syntax (not a rules problem)
- Rule mismatch (command looks allowed, but the actual invocation does not match the pattern)

## Approvals vs rules vs sandbox (practical mental model)

- Sandbox controls what the command can do in the current session.
- Approval/escalation allows a specific command to run with broader access when appropriate.
- Rules/prefixes define persistent allow/deny behavior for command families.

## `prefix_rule` guidance (narrow by default)

- Prefer the smallest prefix that solves the real workflow need.
- Prefer repo-scoped rules before user-level rules.
- Do not use broad shell wrappers (`bash -c`, `sh -c`) unless truly necessary and explicitly approved.
- Validate the command family with representative examples and near-miss commands.

## Signs of a likely rule mismatch

- Similar command succeeds, but one variant fails unexpectedly.
- The command includes extra flags/subcommands not covered by the prefix.
- The command is invoked through a wrapper that changes the actual executable/prefix.

## Validation pattern

- Check the rule file and scope (repo vs user).
- Run `codex execpolicy check` with the exact command shape you expect to allow.
- Test a nearby command that should remain blocked to ensure the rule is not too broad.

## Source-backed notes

- Source: [Codex Rules](https://developers.openai.com/codex/rules)
- Excerpt (short): "prefix_rule"
- Why it matters for troubleshooting: command matching is explicit and pattern-based.
- Practical implication: compare the failing command against the actual prefix pattern instead of assuming intent matches behavior.

- Source: [Codex Rules](https://developers.openai.com/codex/rules)
- Excerpt (short): "execpolicy check"
- Why it matters for troubleshooting: rule debugging is much faster when you test the exact command shape.
- Practical implication: use `codex execpolicy check` before broadening a rule.

- Source: [Codex Security](https://developers.openai.com/codex/security)
- Excerpt (short): paraphrase: approvals and sandboxing are part of the normal safety model.
- Why it matters for troubleshooting: repeated "approval needed" prompts are not necessarily bugs.
- Practical implication: decide whether the command needs one-time escalation or a persistent rule update.

## Skill references

- `$configure-codex` for guarded workflow and scope decisions.
- Within `$configure-codex`, read the rules defaults reference for rule syntax and `execpolicy` validation.
- Within `$configure-codex`, read the allowed-commands matrix for minimal command family selection.
