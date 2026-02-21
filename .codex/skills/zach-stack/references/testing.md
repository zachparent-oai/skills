# Testing conventions (`zach-stack`)

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
  - test commands via `CliRunner` or equivalent runner-style invocation with synthetic args
  - verify exit codes and output
  - verify help text and global options
- For **Click** CLIs:
  - test via `click.testing.CliRunner`
  - validate success and failure paths
  - include edge-case tests around argument parsing and exit codes
- For both, assert deterministic outputs where possible.

## Frontend checks

- For UI work, include interaction-level validation against real page behavior (manual Playwright flow check and automated checks where feasible).

## Docs/test coupling

- Every major behavior change should include an updated doc entry describing intent and validation command.
- Avoid relying on broad integration tests only; use focused tests for failure isolation.
