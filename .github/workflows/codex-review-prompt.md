# Codex Pull Request Review

Review the current pull request and produce a PR comment with actionable findings.

Focus on:
- Bugs and behavioral regressions
- Security or data safety issues
- Performance issues with meaningful impact
- Missing or incorrect tests for changed behavior
- Risky edge cases introduced by the diff

Instructions:
- Review the actual changed code and surrounding context.
- Prioritize findings over summaries.
- Be specific and reference files/lines when possible.
- Keep the comment concise and high signal.
- If there are no clear issues, say so explicitly and mention any residual risks or test gaps.
- Do not modify files.

Output format (Markdown):
- Start with `## Codex Review`
- List findings in severity order
- End with a short `### Summary`
