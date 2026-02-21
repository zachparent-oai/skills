#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

"""Run all custom-skill lint/validation checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    print(">=> lint: validate custom skill structure and markdown style")
    run([sys.executable, "scripts/validate-custom-skills.py"], root)

    print(">=> compile: sync .custom skills into .codex/skills")
    run([sys.executable, "scripts/sync-custom-skills.py"], root)

    print(">=> verify: ensure .codex/skills mirrors .custom")
    run([sys.executable, "scripts/verify-custom-skill-mirror.py"], root)

    print("PASS: custom skill lint/tests complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
