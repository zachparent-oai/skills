from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MIRROR_SKILLS_DIR = REPO_ROOT / ".codex" / "skills"
RUBRIC_SCHEMA = REPO_ROOT / "evals" / "skill-rubric.schema.json"

RUN_CODEX_EVALS = os.environ.get("RUN_CODEX_EVALS") == "1"
RUN_CODEX_EVAL_GRADERS = os.environ.get("RUN_CODEX_EVAL_GRADERS") == "1"
KEEP_EVAL_WORKSPACES = os.environ.get("KEEP_CODEX_EVAL_WORKSPACES") == "1"


@dataclass(frozen=True)
class RuntimeEvalCase:
    case_id: str
    skill: str
    prompt: str
    expected_paths: tuple[str, ...]
    required_text_by_file: tuple[tuple[str, str], ...]
    grader_prompt: str
    grader_check_ids: tuple[str, ...]
    setup_kind: str = "empty"
    forbidden_command_substrings: tuple[str, ...] = ("git reset --hard", "rm -rf")


CASES: tuple[RuntimeEvalCase, ...] = (
    RuntimeEvalCase(
        case_id="zach-stack-doc-recommendation",
        skill="zach-stack",
        prompt=(
            "Use $zach-stack. Review this repository and write your recommended stack defaults "
            "to docs/stack-recommendation.md. Keep it concise and include sections for web, "
            "python, testing, and automation. Do not install dependencies or run network commands."
        ),
        expected_paths=("docs/stack-recommendation.md",),
        required_text_by_file=(
            ("docs/stack-recommendation.md", "Tailwind"),
            ("docs/stack-recommendation.md", "uv"),
            ("docs/stack-recommendation.md", "Justfile"),
        ),
        grader_prompt=(
            "Evaluate docs/stack-recommendation.md for alignment with the zach-stack skill intent. "
            "Check ids: web_defaults, python_uv, testing_expectations, automation_justfile. "
            "Return rubric JSON only."
        ),
        grader_check_ids=(
            "web_defaults",
            "python_uv",
            "testing_expectations",
            "automation_justfile",
        ),
    ),
    RuntimeEvalCase(
        case_id="configure-codex-proposal-note",
        skill="configure-codex",
        prompt=(
            "Use $configure-codex. Inspect this repo and write a proposal note to "
            "docs/codex-rules-proposal.md describing minimal repo-scoped Codex rule updates "
            "for the commands actually used here. Do not modify any .codex/rules files."
        ),
        expected_paths=("docs/codex-rules-proposal.md",),
        required_text_by_file=(
            ("docs/codex-rules-proposal.md", ".codex/rules/default.rules"),
            ("docs/codex-rules-proposal.md", "repo-scoped"),
        ),
        grader_prompt=(
            "Evaluate docs/codex-rules-proposal.md. It should prefer minimal allow-lists, "
            "repo-scoped permissions, and mention confirmation before writing rules. "
            "Check ids: minimal_commands, repo_scope, confirm_before_write. "
            "Return rubric JSON only."
        ),
        grader_check_ids=("minimal_commands", "repo_scope", "confirm_before_write"),
        setup_kind="python_repo",
    ),
    RuntimeEvalCase(
        case_id="init-repo-phase1-scaffold",
        skill="init-repo",
        prompt=(
            "Use $init-repo to create a phase-1 scaffold for a new Python CLI project in this "
            "directory. Create docs and repeatable command scaffolding, but do not install "
            "dependencies or run package managers."
        ),
        expected_paths=("docs", "justfile"),
        required_text_by_file=(),
        grader_prompt=(
            "Evaluate this repository as a phase-1 init-repo scaffold for a Python CLI. "
            "It should include docs, repeatable commands, and an incremental scope. "
            "Check ids: docs_present, command_scaffold, incremental_scope. Return rubric JSON only."
        ),
        grader_check_ids=("docs_present", "command_scaffold", "incremental_scope"),
    ),
    RuntimeEvalCase(
        case_id="agentify-repo-phase1-improvements",
        skill="agentify-repo",
        prompt=(
            "Use $agentify-repo to improve this existing repo in a low-risk phase-1 pass. "
            "Prefer additive changes, create a short plan note at docs/agentify-plan.md, and "
            "avoid installing dependencies or broad migrations."
        ),
        expected_paths=("docs/agentify-plan.md",),
        required_text_by_file=(("docs/agentify-plan.md", "Phase"),),
        grader_prompt=(
            "Evaluate docs/agentify-plan.md and repository changes for agentify-repo alignment. "
            "It should be incremental, low-risk, and identify a next milestone. "
            "Check ids: incremental, low_risk, next_milestone. Return rubric JSON only."
        ),
        grader_check_ids=("incremental", "low_risk", "next_milestone"),
        setup_kind="existing_repo",
    ),
)


def _json_dumps_lines(events: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(event, sort_keys=True) for event in events)


def parse_jsonl(jsonl_text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in jsonl_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        data = json.loads(stripped)
        if isinstance(data, dict):
            events.append(data)
    return events


def run_codex_exec_json(
    prompt: str, *, cwd: Path, trace_path: Path
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["codex", "exec", "--json", "--full-auto", prompt],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text(result.stdout or "", encoding="utf-8")
    return result


def run_codex_grader(
    prompt: str,
    *,
    cwd: Path,
    output_json_path: Path,
    schema_path: Path,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [
            "codex",
            "exec",
            "--full-auto",
            "--output-schema",
            str(schema_path),
            "-o",
            str(output_json_path),
            prompt,
        ],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return result


def iter_command_strings(events: list[dict[str, Any]]) -> list[str]:
    commands: list[str] = []
    for event in events:
        event_type = event.get("type")
        if event_type not in {"item.started", "item.completed"}:
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if item.get("type") != "command_execution":
            continue
        command = item.get("command")
        if isinstance(command, str):
            commands.append(command)
    return commands


def assert_forbidden_commands_not_run(events: list[dict[str, Any]], case: RuntimeEvalCase) -> None:
    commands = iter_command_strings(events)
    for forbidden in case.forbidden_command_substrings:
        assert not any(forbidden in command for command in commands), (
            f"{case.case_id}: forbidden command detected: {forbidden}"
        )


def seed_workspace(workspace: Path, setup_kind: str) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / ".codex").mkdir(exist_ok=True)
    link_path = workspace / ".codex" / "skills"
    if not link_path.exists():
        link_path.symlink_to(MIRROR_SKILLS_DIR, target_is_directory=True)

    if setup_kind == "python_repo":
        (workspace / "pyproject.toml").write_text(
            "[project]\nname = \"demo\"\nversion = \"0.1.0\"\nrequires-python = \">=3.12\"\n",
            encoding="utf-8",
        )
        (workspace / "justfile").write_text("default:\n  @echo demo\n", encoding="utf-8")
        (workspace / "README.md").write_text("# Demo\n", encoding="utf-8")
        return

    if setup_kind == "existing_repo":
        (workspace / "README.md").write_text("# Existing Repo\n", encoding="utf-8")
        src = workspace / "src"
        src.mkdir(exist_ok=True)
        (src / "main.py").write_text("print('hello')\n", encoding="utf-8")
        return

    if setup_kind == "empty":
        (workspace / "README.md").write_text("# Scratch Repo\n", encoding="utf-8")
        return

    raise AssertionError(f"Unknown setup kind: {setup_kind}")


def create_case_workspace(case: RuntimeEvalCase) -> Path:
    root = Path(tempfile.mkdtemp(prefix=f"codex-skill-eval-{case.case_id}-", dir="/tmp"))
    seed_workspace(root, case.setup_kind)
    return root


def maybe_cleanup_workspace(path: Path) -> None:
    if KEEP_EVAL_WORKSPACES:
        return
    shutil.rmtree(path, ignore_errors=True)


def assert_expected_paths_exist(workspace: Path, case: RuntimeEvalCase) -> None:
    for rel_path in case.expected_paths:
        assert (workspace / rel_path).exists(), f"{case.case_id}: missing {rel_path}"


def assert_required_file_text(workspace: Path, case: RuntimeEvalCase) -> None:
    for rel_path, needle in case.required_text_by_file:
        target = workspace / rel_path
        assert target.exists(), f"{case.case_id}: missing {rel_path}"
        content = target.read_text(encoding="utf-8")
        assert needle in content, f"{case.case_id}: {rel_path} missing {needle!r}"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"Expected JSON object in {path}"
    return data


def assert_grader_result(result_path: Path, case: RuntimeEvalCase) -> None:
    payload = load_json(result_path)
    checks = payload.get("checks")
    assert isinstance(checks, list), f"{case.case_id}: grader missing checks[]"
    by_id = {}
    for item in checks:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            by_id[item["id"]] = item

    missing_ids = [check_id for check_id in case.grader_check_ids if check_id not in by_id]
    assert not missing_ids, f"{case.case_id}: grader missing check ids {missing_ids}"

    assert isinstance(payload.get("overall_pass"), bool), (
        f"{case.case_id}: grader missing boolean overall_pass"
    )
    assert isinstance(payload.get("score"), int), f"{case.case_id}: grader missing integer score"
    assert payload["overall_pass"], f"{case.case_id}: grader overall_pass=false ({payload})"


def require_codex_runtime_evals() -> None:
    if not RUN_CODEX_EVALS:
        pytest.skip("Set RUN_CODEX_EVALS=1 to run Codex runtime skill evals")
    if shutil.which("codex") is None:
        pytest.skip("codex CLI not found in PATH")
    if not MIRROR_SKILLS_DIR.exists():
        pytest.skip("Missing .codex/skills mirror; run sync-custom-skills.py sync first")


def maybe_run_grader(case: RuntimeEvalCase, workspace: Path) -> None:
    if not RUN_CODEX_EVAL_GRADERS:
        return
    grader_output = workspace / ".eval-artifacts" / f"{case.case_id}.grader.json"
    grader_output.parent.mkdir(parents=True, exist_ok=True)

    grader_result = run_codex_grader(
        case.grader_prompt,
        cwd=workspace,
        output_json_path=grader_output,
        schema_path=RUBRIC_SCHEMA,
    )
    assert grader_result.returncode == 0, (
        f"{case.case_id}: grader codex exec failed\nSTDERR:\n{grader_result.stderr}"
    )
    assert grader_output.exists(), f"{case.case_id}: grader output file missing"
    assert_grader_result(grader_output, case)


@pytest.mark.codex_eval
@pytest.mark.parametrize("case", CASES, ids=[case.case_id for case in CASES])
def test_custom_skill_runtime_eval(case: RuntimeEvalCase) -> None:
    require_codex_runtime_evals()
    workspace = create_case_workspace(case)
    try:
        trace_path = workspace / ".eval-artifacts" / f"{case.case_id}.trace.jsonl"
        result = run_codex_exec_json(case.prompt, cwd=workspace, trace_path=trace_path)
        assert result.returncode == 0, (
            f"{case.case_id}: codex exec failed\nSTDERR:\n{result.stderr}"
        )
        assert trace_path.exists(), f"{case.case_id}: missing trace artifact"

        raw_trace = trace_path.read_text(encoding="utf-8")
        assert raw_trace.strip(), f"{case.case_id}: empty JSONL trace"
        events = parse_jsonl(raw_trace)
        assert events, f"{case.case_id}: no JSON events parsed"

        assert_forbidden_commands_not_run(events, case)
        assert_expected_paths_exist(workspace, case)
        assert_required_file_text(workspace, case)

        maybe_run_grader(case, workspace)
    finally:
        maybe_cleanup_workspace(workspace)
