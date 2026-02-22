# Network and connectivity (`troubleshoot-sandbox`)

## Distinguish the failure type

- DNS/host resolution failures (`Could not resolve host`) often indicate no network access in the current shell sandbox or local DNS/network issues.
- Connection timeouts/refused connections may indicate network policy, service outage, VPN/proxy issues, or a bad endpoint.
- Package download failures can be network-related or registry/auth-related; inspect stderr carefully.

## Triage steps

1. Capture the exact network error text.
2. Determine whether the command is shell-network dependent or if a built-in web/browser tool can substitute.
3. Confirm whether network is expected in the current sandbox/session configuration.
4. If the command is essential and network is blocked by policy, request escalation with a narrow justification.

## When a web tool can substitute

- Reading docs, checking a webpage, or confirming a version/reference can often be done via a built-in web tool instead of shell commands like `curl`.
- Do not substitute a web tool when the task requires local command execution semantics (installers, package managers, auth-bound CLIs).

## Local/offline fallback patterns

- Use local docs and repo references first.
- Ask the user to paste relevant error output or docs snippets when external access is unavailable.
- Defer non-essential fetches and continue with offline-safe parts of the task.

## Source-backed notes

- Source: [Codex Security](https://developers.openai.com/codex/security)
- Excerpt (short): "network access can be disabled"
- Why it matters for troubleshooting: network failures may be a configured environment constraint, not a transient outage.
- Practical implication: avoid retry loops; verify whether network is disabled before troubleshooting the remote service.

- Source: [Codex Config Reference](https://developers.openai.com/codex/config-reference)
- Excerpt (short): paraphrase: `network_access` is a configurable setting.
- Why it matters for troubleshooting: session/profile configuration can explain environment-specific network behavior.
- Practical implication: include the expected network setting when explaining why a shell fetch failed.
