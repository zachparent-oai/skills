#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///

"""Run local skill eval suites from root `evals/` (eval-skills inspired layout)."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import typer

REPO = Path(__file__).resolve().parents[1]
CUSTOM_SKILLS_DIR = REPO / "skills" / ".custom"
DEFAULT_EVAL_DIR = REPO / "evals"

app = typer.Typer(help="Run root `evals/` suites against `.custom` skills.")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    _, raw_fm, _ = parts
    result: dict[str, str] = {}
    for line in raw_fm.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def _read_text_cached(
    cache: dict[Path, str],
    skill_dir: Path,
    rel_path: str,
) -> tuple[Path, str | None]:
    target = skill_dir / rel_path
    if target in cache:
        return target, cache[target]
    if not target.exists() or not target.is_file():
        return target, None
    content = target.read_text()
    cache[target] = content
    return target, content


def run_check(
    *,
    suite_name: str,
    case_id: str,
    skill_name: str,
    skill_dir: Path,
    check: dict[str, Any],
    text_cache: dict[Path, str],
) -> tuple[int, list[str]]:
    kind = str(check.get("kind", "")).strip()
    passed = 0
    failures: list[str] = []
    label = f"{suite_name}/{case_id}"

    if kind == "file_exists":
        rel_path = str(check.get("path", "")).strip()
        target = skill_dir / rel_path
        if rel_path and target.exists():
            return 1, []
        failures.append(f"{label}: {skill_name} missing file {rel_path or '<unset>'}")
        return 0, failures

    if kind == "contains_text":
        rel_path = str(check.get("path", "SKILL.md")).strip()
        needle = str(check.get("text", ""))
        target, content = _read_text_cached(text_cache, skill_dir, rel_path)
        if content is None:
            failures.append(f"{label}: {skill_name} missing file {target.relative_to(REPO)}")
            return 0, failures
        if needle and needle in content:
            return 1, []
        failures.append(f"{label}: {skill_name} missing text {needle!r} in {rel_path}")
        return 0, failures

    if kind == "contains_all":
        rel_path = str(check.get("path", "SKILL.md")).strip()
        texts_raw = check.get("texts", [])
        texts = [str(item) for item in texts_raw] if isinstance(texts_raw, list) else []
        target, content = _read_text_cached(text_cache, skill_dir, rel_path)
        if content is None:
            failures.append(f"{label}: {skill_name} missing file {target.relative_to(REPO)}")
            return 0, failures
        if not texts:
            failures.append(f"{label}: {skill_name} contains_all check has no texts")
            return 0, failures
        missing = [needle for needle in texts if needle not in content]
        if not missing:
            return 1, []
        failures.append(
            f"{label}: {skill_name} missing {len(missing)} expected text(s) in {rel_path}: "
            + ", ".join(repr(item) for item in missing)
        )
        return 0, failures

    if kind == "frontmatter_field_equals":
        rel_path = str(check.get("path", "SKILL.md")).strip()
        field = str(check.get("field", "")).strip()
        expected = str(check.get("value", ""))
        target, content = _read_text_cached(text_cache, skill_dir, rel_path)
        if content is None:
            failures.append(f"{label}: {skill_name} missing file {target.relative_to(REPO)}")
            return 0, failures
        frontmatter = parse_frontmatter(content)
        actual = frontmatter.get(field)
        if field and actual == expected:
            return 1, []
        failures.append(
            f"{label}: {skill_name} frontmatter {field!r} expected {expected!r}, got {actual!r}"
        )
        return 0, failures

    failures.append(f"{label}: {skill_name} unknown check type {kind!r}")
    return passed, failures


def load_prompt_set(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        required = {"prompt_id", "prompt"}
        missing_headers = sorted(required - fieldnames)
        if missing_headers:
            raise SystemExit(
                f"FAIL: {path.relative_to(REPO)} missing CSV headers: {', '.join(missing_headers)}"
            )

        prompts: dict[str, dict[str, str]] = {}
        for index, row in enumerate(reader, start=2):
            prompt_id = (row.get("prompt_id") or "").strip()
            prompt = (row.get("prompt") or "").strip()
            if not prompt_id:
                raise SystemExit(f"FAIL: {path.relative_to(REPO)} row {index} missing prompt_id")
            if not prompt:
                raise SystemExit(f"FAIL: {path.relative_to(REPO)} row {index} missing prompt")
            if prompt_id in prompts:
                raise SystemExit(
                    f"FAIL: {path.relative_to(REPO)} duplicate prompt_id {prompt_id!r}"
                )
            prompts[prompt_id] = {k: (v or "") for k, v in row.items()}
        return prompts


def load_test_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for index, raw_line in enumerate(path.read_text().splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"FAIL: {path.relative_to(REPO)} line {index}: invalid JSON ({exc})"
            ) from exc
        if not isinstance(data, dict):
            raise SystemExit(f"FAIL: {path.relative_to(REPO)} line {index}: expected JSON object")
        cases.append(data)
    if not cases:
        raise SystemExit(f"FAIL: {path.relative_to(REPO)} has no test cases")
    return cases


def run_suite(suite_dir: Path) -> dict[str, Any]:
    suite_name = suite_dir.name
    prompt_set_path = suite_dir / "prompt_set.csv"
    test_path = suite_dir / "test.jsonl"
    failures: list[str] = []
    case_results: list[dict[str, Any]] = []
    total_checks = 0
    passed_checks = 0

    if not prompt_set_path.exists():
        return {
            "suite": suite_name,
            "status": "FAIL",
            "prompts": 0,
            "cases": 0,
            "passed_checks": 0,
            "total_checks": 0,
            "failures": [f"{suite_name}: missing {prompt_set_path.relative_to(REPO)}"],
            "case_results": [],
        }
    if not test_path.exists():
        return {
            "suite": suite_name,
            "status": "FAIL",
            "prompts": 0,
            "cases": 0,
            "passed_checks": 0,
            "total_checks": 0,
            "failures": [f"{suite_name}: missing {test_path.relative_to(REPO)}"],
            "case_results": [],
        }

    prompts = load_prompt_set(prompt_set_path)
    cases = load_test_cases(test_path)
    text_cache: dict[Path, str] = {}

    for case in cases:
        case_id = str(case.get("case_id", "")).strip()
        prompt_id = str(case.get("prompt_id", "")).strip()
        skill_name = str(case.get("skill", suite_name)).strip()
        checks_raw = case.get("checks", [])
        checks = (
            [item for item in checks_raw if isinstance(item, dict)]
            if isinstance(checks_raw, list)
            else []
        )

        case_failures: list[str] = []
        case_passed = 0

        if not case_id:
            case_failures.append(f"{suite_name}: case missing case_id")
        if not prompt_id:
            case_failures.append(
                f"{suite_name}/{case_id or '<missing-case-id>'}: missing prompt_id"
            )
        elif prompt_id not in prompts:
            case_failures.append(f"{suite_name}/{case_id}: unknown prompt_id {prompt_id!r}")

        skill_dir = CUSTOM_SKILLS_DIR / skill_name
        if not skill_name:
            case_failures.append(
                f"{suite_name}/{case_id or '<missing-case-id>'}: missing skill name"
            )
        elif not skill_dir.is_dir():
            case_failures.append(
                f"{suite_name}/{case_id}: missing skill directory {skill_dir.relative_to(REPO)}"
            )

        if not checks:
            case_failures.append(
                f"{suite_name}/{case_id or '<missing-case-id>'}: case has no checks"
            )

        if not case_failures and skill_name:
            for check in checks:
                passed, check_failures = run_check(
                    suite_name=suite_name,
                    case_id=case_id,
                    skill_name=skill_name,
                    skill_dir=skill_dir,
                    check=check,
                    text_cache=text_cache,
                )
                total_checks += 1
                passed_checks += passed
                case_passed += passed
                case_failures.extend(check_failures)
        else:
            total_checks += len(checks)

        case_status = "PASS" if not case_failures else "FAIL"
        failures.extend(case_failures)
        case_results.append(
            {
                "case_id": case_id,
                "prompt_id": prompt_id,
                "skill": skill_name,
                "status": case_status,
                "passed_checks": case_passed,
                "total_checks": len(checks),
                "failures": case_failures,
            }
        )

    return {
        "suite": suite_name,
        "status": "PASS" if not failures else "FAIL",
        "prompts": len(prompts),
        "cases": len(cases),
        "passed_checks": passed_checks,
        "total_checks": total_checks,
        "failures": failures,
        "case_results": case_results,
    }


def run_evals(eval_dir: Path) -> int:
    if not eval_dir.exists():
        print(f"FAIL: no evals directory found: {eval_dir}")
        return 1
    if not eval_dir.is_dir():
        print(f"FAIL: eval path is not a directory: {eval_dir}")
        return 1

    suite_dirs = []
    for path in sorted(eval_dir.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        # Only treat directories with the expected static-eval files as suites.
        if not (path / "prompt_set.csv").exists() or not (path / "test.jsonl").exists():
            continue
        suite_dirs.append(path)
    if not suite_dirs:
        print(f"FAIL: no eval suites found in {eval_dir}")
        return 1

    results = [run_suite(suite_dir) for suite_dir in suite_dirs]
    print(json.dumps(results, indent=2))

    failed = [result for result in results if result["status"] == "FAIL"]
    if failed:
        for suite in failed:
            suite_name = str(suite.get("suite"))
            suite_failures = suite.get("failures", [])
            if isinstance(suite_failures, list):
                for message in suite_failures:
                    print(f"FAIL {suite_name} :: {message}")
            else:
                print(f"FAIL {suite_name} :: {suite_failures}")
        return 1

    total_suites = len(results)
    total_cases = sum(int(item.get("cases", 0)) for item in results)
    total_checks = sum(int(item.get("total_checks", 0)) for item in results)
    print(
        "PASS: all skill evals passed "
        f"({total_suites} suites, {total_cases} cases, {total_checks} checks)"
    )
    return 0


@app.callback(invoke_without_command=True)
def main(
    eval_dir: Path = typer.Option(
        DEFAULT_EVAL_DIR,
        "--eval-dir",
        help="Path to root eval suites directory.",
    ),
) -> None:
    """Run root eval suites against `.custom` skills."""
    raise typer.Exit(code=run_evals(eval_dir))


if __name__ == "__main__":
    app()
