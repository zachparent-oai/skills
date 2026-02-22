# Triage flow (`troubleshoot-sandbox`)

## First 3 checks (always)

1. Capture the exact command, cwd, and stderr (do not paraphrase yet).
2. Classify the symptom family: network, write access, missing tool, rules/approval, syntax/path.
3. Run one non-mutating diagnostic that tests the hypothesis before retrying the original command.

## Primary decision flow

1. Does the error mention sandbox/permission/approval?
   - Yes: check `rules-approvals-and-prefixes.md` and `filesystem-and-write-access.md`.
   - No: continue.
2. Does the error mention host resolution, connection, timeout, SSL, or download failures?
   - Yes: check `network-and-connectivity.md`.
   - No: continue.
3. Does the error mention `command not found`, `No such file`, or unknown flags?
   - Yes: check `error-signatures.md` for missing binary vs syntax/cwd mismatch.
   - No: continue.
4. Is the command trying to write outside the workspace or protected paths?
   - Yes: check `filesystem-and-write-access.md`.
   - No: continue.
5. Is the same command family repeatedly needed and repeatedly blocked?
   - Yes: use `configure-codex-handoff.md` and consider `$configure-codex`.

## Symptom-to-reference routing table

- `SandboxDenied`, escalation prompt, rules blocked: `rules-approvals-and-prefixes.md`
- `Operation not permitted`, not writable path: `filesystem-and-write-access.md`
- `Could not resolve host`, network download failure: `network-and-connectivity.md`
- `command not found`, missing executable: `error-signatures.md`
- Repeated repo workflow blockage: `configure-codex-handoff.md`

## Source-backed notes

- Source: [Codex Security](https://developers.openai.com/codex/security)
- Excerpt (short): "Code runs in a sandbox."
- Why it matters for troubleshooting: sandbox constraints are a first-class root cause category.
- Practical implication: classify sandbox/policy issues before assuming tool or code defects.

- Source: [Codex Security](https://developers.openai.com/codex/security)
- Excerpt (short): "balance productivity with safety"
- Why it matters for troubleshooting: approvals and sandboxing are expected controls, not random failures.
- Practical implication: prefer focused escalation requests or rule updates instead of repeated retries.

- Source: [Codex Rules](https://developers.openai.com/codex/rules)
- Excerpt (short): "match commands before they run"
- Why it matters for troubleshooting: blocked commands may be rule mismatches, not OS-level permission issues.
- Practical implication: verify rule matching behavior when a command "should" have been allowed.
