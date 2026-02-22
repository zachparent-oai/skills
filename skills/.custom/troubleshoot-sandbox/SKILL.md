---
name: troubleshoot-sandbox
description: "Diagnose Codex command failures caused by sandboxing, network restrictions, write access, approvals, rules, or missing tools, and choose the safest next step."
---

# Troubleshoot Sandbox

Use this skill when a command fails and the likely root cause may be sandbox permissions, write access limits, network restrictions, missing tools, or Codex rules/approval behavior.

## Use this skill when

- a command is blocked, denied, or requires approval/escalation
- a command cannot write to a path
- networked commands fail (for example `git fetch`, `curl`, package installers)
- a command fails and it is unclear whether the cause is sandboxing vs missing tools vs syntax
- the user asks whether to change Codex rules or request one-time escalation
- you need to explain the root cause and safest next action clearly

## Symptoms this skill covers

- `SandboxDenied` / permission-denied style errors
- `Operation not permitted` or "not writable" path failures
- DNS/connectivity errors (for example "Could not resolve host")
- `command not found` / missing binary
- commands that work only after escalation or after rule changes
- rule/prefix mismatches (command should be allowed but is still blocked)

## Triage workflow

1. Classify the likely failure family first:
   - network/connectivity
   - filesystem/write access
   - missing tool/binary
   - approval/rules/policy
   - command syntax/path/cwd
2. Capture evidence before retrying:
   - exact command
   - current working directory
   - stderr output (verbatim)
   - sandbox/approval error text if present
3. Separate sandboxing from non-sandbox issues:
   - missing binary or bad arguments are not fixed by escalation
   - path/cwd mistakes are not rules problems
   - DNS/network failures may be sandbox restrictions or local environment/network problems
4. Try one non-mutating diagnostic that narrows the cause.
5. If the command is important and clearly sandbox-blocked, request focused escalation with a narrow justification.
6. If the need is persistent and repo-specific (same command family repeatedly), consider `$configure-codex` for repo/user rules.
7. Explain root cause, confidence, and next action to the user in concrete terms.

## Hard rules

- Do not repeatedly retry the same blocked command without changing conditions or gathering new evidence.
- Do not broaden permissions without user confirmation.
- Prefer narrow command prefixes over broad shell access.
- Distinguish "network unavailable in this sandbox/session" from "the internet/service is down."
- Document whether the blocker is temporary (this run), repo configuration (rules), or missing tool/install.
- Use `$configure-codex` for repo/user rule adjustments instead of undocumented permission creep.

## Reference usage map

- Use [triage-flow](references/triage-flow.md) first for classification and the first three checks.
- Use [error-signatures](references/error-signatures.md) when you need to interpret stderr quickly.
- Use [filesystem-and-write-access](references/filesystem-and-write-access.md) for path/write failures and escalation decisions.
- Use [network-and-connectivity](references/network-and-connectivity.md) for DNS/network failures and offline fallbacks.
- Use [rules-approvals-and-prefixes](references/rules-approvals-and-prefixes.md) for approvals, `prefix_rule`, and `execpolicy` troubleshooting.
- Use [configure-codex-handoff](references/configure-codex-handoff.md) when repeated failures suggest repo/user rule updates.
