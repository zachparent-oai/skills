# CLI testing conventions (`zach-stack`)

## CLI strategy defaults

- **CLI frameworks**: prefer `Typer` for new CLI implementations.
- **CLI alternatives**: `Click` is acceptable for existing or click-first codebases and when explicit subcommand ergonomics are required.
- **Dependency hygiene**: keep CLI modules lightweight; make scripts as self-contained and dependency-bounded as possible by:
  - placing entrypoints in dedicated files/modules
  - scoping dependencies to the package/script boundary
  - avoiding monolithic "utility" scripts with broad transitive imports

## Test expectations by framework

- Add focused unit tests for parsing, argument validation, and command routing.
- Add integration-style tests for command side effects (filesystem, subprocess calls, exit codes).
- For **Typer** CLIs:
  - test commands with `click.testing.CliRunner` syntax (Typer uses Click internally)
  - verify exit codes and output
  - verify help text and global options
- For **Click** CLIs:
  - test via `click.testing.CliRunner`
  - validate success and failure paths
  - include edge-case tests around argument parsing and exit codes
- For both, assert deterministic outputs where possible.

## CLI command style for single-command scripts

- For scripts intended to have a single action, prefer exposing the behavior on the default command and avoid a dedicated `run` subcommand label.
- This keeps invocation simple for agents: `uv run scripts/<tool>.py`.

## Examples

- `uv run scripts/validate-custom-skills.py` (default entrypoint)
- `uv run scripts/run-skill-evals.py`
- `uv run scripts/test-custom-skills.py`
- `uv run scripts/sync-custom-skills.py sync --dry-run`

## Source-backed notes

### Typer command organization

- Source: [Typer Commands / SubCommands](https://typer.tiangolo.com/tutorial/commands/)
- Excerpt (short): "SubCommands - Command Groups"
- Why it matters for zach-stack: testing scope grows with command surface complexity.
- Practical implication: keep single-purpose scripts as one command when possible; add subcommands only when behavior naturally groups.
