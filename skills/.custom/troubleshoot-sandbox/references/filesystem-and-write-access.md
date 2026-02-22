# Filesystem and write access (`troubleshoot-sandbox`)

## Mental model

Treat write failures as one of three buckets:

- path/cwd mistake (wrong target, missing directory, typo)
- OS/filesystem permissions issue
- sandbox write restriction (path is outside writable roots or otherwise protected)

## Quick checks

1. Confirm the command is writing where you think it is writing.
2. Confirm cwd and resolve relative paths.
3. Check whether the target is inside the workspace or another known writable area.

## Repo-tracked files vs cache/build-artifact writes

- Repo-tracked edits usually belong inside the workspace.
- Cache/build artifacts may be redirected to workspace-local directories when defaults point to protected paths.
- If a tool defaults to a user cache directory that is blocked, use a repo-local cache env var if supported.

## When escalation is appropriate

- The command is important to the task.
- The failure is clearly due to sandbox/path restrictions, not bad syntax.
- A workspace-local alternative is not available or would materially distort the workflow.

## Safe alternatives before escalation

- Change cwd to the intended workspace.
- Write to a workspace or temp directory and then inspect results.
- Redirect caches to repo-local paths (for example tool cache env vars).
- Ask the user whether they want to allow the specific command/path access.

## Source-backed notes

- Source: [Codex Security](https://developers.openai.com/codex/security)
- Excerpt (short): "sandbox protections and approval controls"
- Why it matters for troubleshooting: write failures may be an intentional safety boundary.
- Practical implication: explain the safety boundary and propose a narrow workaround or escalation.

- Source: [Codex Config Reference](https://developers.openai.com/codex/config-reference)
- Excerpt (short): paraphrase: sandbox settings are configurable and can differ by profile.
- Why it matters for troubleshooting: path/write behavior may vary across repos or user profiles.
- Practical implication: include current sandbox config context when suggesting persistent fixes.
