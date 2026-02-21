#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///

"""Simple rule-based evaluator for `.custom` skills (eval-skills inspired)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

REPO = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_DIR = REPO / "skills" / ".custom" / "evals"

app = typer.Typer(help="Run eval checks for `.custom` skills.")


def run_eval(skill_name: str, spec: dict[str, object]) -> dict[str, object]:
    skill_dir = REPO / "skills" / ".custom" / skill_name
    checks_raw = spec.get("checks", [])
    checks: list[dict[str, Any]]
    if isinstance(checks_raw, list):
        checks = [
            check
            for check in checks_raw
            if isinstance(check, dict)
        ]
    else:
        checks = []
    passed = 0
    failed = []

    for check in checks:
        kind = check.get("kind")
        if kind == "file_exists":
            target = skill_dir / str(check.get("path", ""))
            ok = target.exists()
            if not ok:
                failed.append(f"{skill_name}: missing required file {target.relative_to(REPO)}")
            else:
                passed += 1

        elif kind == "frontmatter_name":
            skill_md = (skill_dir / "SKILL.md").read_text()
            ok = f"name: {skill_name}" in skill_md
            if not ok:
                failed.append(
                    f"{skill_name}: SKILL.md frontmatter name does not match {skill_name}"
                )
            else:
                passed += 1

        elif kind == "contains_link":
            skill_md = (skill_dir / "SKILL.md").read_text()
            needle = str(check.get("text", ""))
            ok = needle in skill_md
            if not ok:
                failed.append(f"{skill_name}: missing required text '{needle}' in SKILL.md")
            else:
                passed += 1

        elif kind == "contains_reference":
            ref = check.get("reference")
            if not ref:
                failed.append(f"{skill_name}: contains_reference check missing reference")
                continue
            path = skill_dir / "references" / str(ref)
            ok = path.exists()
            if not ok:
                failed.append(f"{skill_name}: missing reference {path}")
            else:
                passed += 1

        else:
            failed.append(f"{skill_name}: unknown check type {kind}")

    return {
        "skill": skill_name,
        "passed": passed,
        "total": len(checks),
        "status": "PASS" if not failed else "FAIL",
        "failures": failed,
    }


def run_evals(eval_dir: Path) -> int:
    if not eval_dir.exists():
        print(f"No evals directory found: {eval_dir}")
        return 1

    results: list[dict[str, object]] = []
    for spec_file in sorted(eval_dir.glob("*.json")):
        data = json.loads(spec_file.read_text())
        skill_name = str(data.get("skill"))
        results.append(run_eval(skill_name, data))

    print(json.dumps(results, indent=2))

    failed = [r for r in results if r["status"] == "FAIL"]
    if failed:
        for item in failed:
            failures = item["failures"]
            if isinstance(failures, list):
                fail_messages = ", ".join(str(f) for f in failures)
            else:
                fail_messages = str(failures)
            print("FAIL", item["skill"], "::", fail_messages)
            return 1

    print("PASS: all skill evals passed")
    return 0


@app.callback(invoke_without_command=True)
def main(
    eval_dir: Path = typer.Option(
        DEFAULT_EVAL_DIR,
        "--eval-dir",
        help="Path to JSON eval specs.",
    ),
) -> None:
    """Run all `.custom` skill eval specs."""
    raise typer.Exit(code=run_evals(eval_dir))


if __name__ == "__main__":
    app()
