#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

"""Simple rule-based evaluator for `.custom` skills (eval-skills inspired)."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EVAL_DIR = REPO / "skills" / ".custom" / "evals"


def run_eval(skill_name: str, spec: dict[str, object]) -> dict[str, object]:
    skill_dir = REPO / "skills" / ".custom" / skill_name
    checks = spec.get("checks", [])
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


def main() -> int:
    if not EVAL_DIR.exists():
        print("No evals directory found: skills/.custom/evals")
        return 1

    results = []
    for spec_file in sorted(EVAL_DIR.glob("*.json")):
        data = json.loads(spec_file.read_text())
        skill_name = str(data.get("skill"))
        results.append(run_eval(skill_name, data))

    print(json.dumps(results, indent=2))

    failed = [r for r in results if r["status"] == "FAIL"]
    if failed:
        for item in failed:
            print("FAIL", item["skill"], "::", ", ".join(item["failures"]))
        return 1

    print("PASS: all skill evals passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
