# Error signatures (`troubleshoot-sandbox`)

Use this file to map common error text to likely root causes and the next diagnostic step.

## Common signatures and likely causes

- `SandboxDenied` / explicit sandbox policy denial
  - Usually means: the command is blocked by sandbox policy or requires escalation.
  - Test next: inspect command purpose and decide whether narrow escalation is appropriate.
- `Operation not permitted` / permission denied on a path
  - Usually means: write/read permission issue, protected path, or sandbox write restriction.
  - Test next: verify target path and whether it is inside a writable root.
- `Could not resolve host`
  - Usually means: DNS/network restriction in the sandbox or local environment/network issue.
  - Test next: confirm whether shell network is available in this environment and whether a web tool can substitute.
- `command not found` / executable not found
  - Usually means: missing binary/tool install, wrong PATH, or typo.
  - Test next: run a non-mutating version/help check for the expected binary (if available) or inspect project docs.
- `No such file or directory`
  - Usually means: wrong cwd, bad path, or missing generated file.
  - Test next: verify cwd and inspect the referenced path before retrying.
- `unknown option` / `unknown command`
  - Usually means: wrong CLI syntax, wrong tool version, or command intended for a different tool.
  - Test next: check `--help` output and repo docs/Justfile.

## Confidence cues (what increases confidence in root cause)

- Explicit sandbox/approval wording -> high confidence policy/sandbox issue.
- Host resolution/download failures across multiple tools -> high confidence network restriction.
- Tool-specific syntax errors with valid filesystem access -> likely command usage/version mismatch.
- Path errors that change when cwd changes -> likely path/cwd issue, not rules.

## Source-backed notes

- Source: [Codex Security](https://developers.openai.com/codex/security)
- Excerpt (short): paraphrase: sandbox modes and network access can be configured differently per environment.
- Why it matters for troubleshooting: the same command may fail in one environment and succeed in another without any code changes.
- Practical implication: report the environment/sandbox mode when explaining failures to the user.

- Source: [Codex CLI](https://developers.openai.com/codex/cli)
- Excerpt (short): paraphrase: CLI exposes sandbox and approval controls.
- Why it matters for troubleshooting: blocked-command symptoms can reflect current CLI/session settings.
- Practical implication: check sandbox/approval settings before attributing failures to the repo.
