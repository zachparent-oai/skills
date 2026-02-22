#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///

"""Run all custom-skill lint/validation checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer(help="Run the custom-skill lint/eval pipeline.")


def run_command(command: list[str]) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_python_script(script_path: str, *args: str) -> None:
    run_command([sys.executable, str(ROOT / script_path), *args])


def run_pipeline() -> int:
    print(">=> lint: markdown references " "(skills/.custom only; web URLs auto-skip if offline)")
    run_command(
        [
            # Reuse the current Python env to avoid nested `uv run` startup overhead.
            sys.executable,
            str(ROOT / "scripts/lint-markdown-references.py"),
            "--scope",
            "custom",
            "--web-mode",
            "auto",
            "--timeout-seconds",
            "2",
        ]
    )

    print(">=> lint: validate custom skill structure and markdown style")
    run_python_script("scripts/validate-custom-skills.py")

    print(">=> sync+check: sync .custom skills and verify mirror")
    run_python_script("scripts/sync-custom-skills.py", "sync")
    run_python_script("scripts/sync-custom-skills.py", "check")

    print("PASS: custom skill lint/tests complete")
    return 0


@app.callback(invoke_without_command=True)
def main() -> None:
    """Run validation + sync/check pipeline."""
    raise typer.Exit(code=run_pipeline())


if __name__ == "__main__":
    app()
