#!/usr/bin/env python3
"""Validation and lightweight lint checks for .custom skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CUSTOM_ROOT = REPO_ROOT / ".custom"

REQUIRED_SKILLS = {
    "zach-stack": {
        "references": {
            "web.md",
            "python.md",
            "testing.md",
            "docs.md",
            "workspaces.md",
            "resources.md",
        }
    },
    "init-repo": {
        "references": {
            "new-repo-runbook.md",
        }
    },
    "agentify-repo": {
        "references": {
            "incremental-harness.md",
            "convergence-phases.md",
            "rollback-and-safety.md",
        }
    },
    "configure-codex": {
        "references": {
            "rules-default.md",
            "allowed-commands-matrix.md",
            "codex-environment.md",
        }
    },
}

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str, *, file: Path | None = None) -> None:
    if file:
        print(f"FAIL: {file}: {message}")
    else:
        print(f"FAIL: {message}")
    raise SystemExit(1)


def check_markdown_lint(path: Path) -> None:
    content = path.read_text()
    if not content.endswith("\n"):
        fail("does not end with newline", file=path)
    if "\t" in content:
        fail("contains tabs", file=path)

    if path.name == "SKILL.md":
        if not content.startswith("---\n"):
            fail("missing YAML frontmatter start", file=path)
        parts = content.split("---", 2)
        if len(parts) < 3:
            fail("missing YAML frontmatter end marker", file=path)
        if not re.search(r"^# ", content, re.M):
            fail("missing top-level markdown heading", file=path)


def parse_frontmatter(lines: list[str]) -> dict[str, str]:
    fm: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip().strip('"')
    return fm


def validate_frontmatter(skill_dir: Path) -> str:
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        fail("missing SKILL.md", file=skill_dir)

    content = skill_path.read_text()
    check_markdown_lint(skill_path)

    if not content.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter", file=skill_path)
    try:
        _, raw_fm, _ = content.split("---", 2)
    except ValueError as exc:
        fail("invalid frontmatter block", file=skill_path)
        raise SystemExit from exc

    fm = parse_frontmatter(raw_fm.splitlines())
    if "name" not in fm or "description" not in fm:
        fail("missing required frontmatter keys: name, description", file=skill_path)

    name = fm["name"].strip()
    if not SKILL_NAME_RE.match(name):
        fail(f"invalid skill name '{name}' in frontmatter; expected lower-case hyphen name", file=skill_path)

    if name != skill_dir.name:
        fail(f"frontmatter name '{name}' must match directory '{skill_dir.name}'", file=skill_path)

    description = fm["description"].strip()
    if len(description) > 1024:
        fail("description exceeds 1024 chars", file=skill_path)
    if "<" in description or ">" in description:
        fail("description contains angle brackets", file=skill_path)

    for token in re.findall(r"\(references/([^)\s]+\.md)\)", content):
        ref_path = skill_dir / "references" / token
        if not ref_path.exists():
            fail(f"references/{token} link does not exist", file=skill_path)

    for token in re.findall(r"\.\.\/\.\.\/(zach-stack|init-repo|agentify-repo|configure-codex)", content):
        pass

    return name


def validate_agents_config(skill_dir: Path, name: str) -> None:
    agent_cfg = skill_dir / "agents" / "openai.yaml"
    if not agent_cfg.exists():
        return
    content = agent_cfg.read_text()
    if not content.startswith("interface:"):
        fail("agents/openai.yaml missing interface block", file=agent_cfg)
    if "display_name:" not in content:
        fail("agents/openai.yaml missing display_name", file=agent_cfg)
    if "default_prompt:" not in content:
        fail("agents/openai.yaml missing default_prompt", file=agent_cfg)
    if f"${name}" not in content:
        fail(f"agents/openai.yaml default_prompt should mention ${name}", file=agent_cfg)


def validate_references(skill_dir: Path, required: set[str]) -> None:
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        if required:
            fail("missing references directory", file=skill_dir)
        return

    actual = {
        p.name
        for p in refs_dir.glob("*.md")
        if p.is_file()
    }
    missing = required - actual
    if missing:
        missing_str = ", ".join(sorted(missing))
        fail(f"missing required references: {missing_str}", file=skill_dir / "references")

    for p in refs_dir.glob("*.md"):
        check_markdown_lint(p)


def check_root_custom_docs() -> None:
    readme = REPO_ROOT / "README-custom.md"
    if not readme.exists():
        fail("missing README-custom.md")
    check_markdown_lint(readme)


def main() -> int:
    if not CUSTOM_ROOT.exists():
        fail(".custom directory does not exist at repository root")

    check_root_custom_docs()

    if not (CUSTOM_ROOT / "AGENTS.md").exists():
        fail("missing .custom/AGENTS.md")

    custom_skills = [
        p
        for p in sorted(CUSTOM_ROOT.iterdir())
        if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").exists()
    ]

    for skill_dir in custom_skills:
        name = validate_frontmatter(skill_dir)

        required = REQUIRED_SKILLS.get(name, {}).get("references", set())
        validate_references(skill_dir, set(required))
        validate_agents_config(skill_dir, name)

    print("PASS: custom skills lint and structure checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
