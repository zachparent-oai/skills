#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

"""Verify skills in `skills/.custom` and `.codex/skills` are mirrored."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CUSTOM_ROOT = REPO_ROOT / "skills" / ".custom"
MIRROR_ROOT = REPO_ROOT / ".codex" / "skills"


def list_skill_dirs(root: Path) -> dict[str, set[tuple[str, ...]]]:
    skills: dict[str, set[tuple[str, ...]]] = {}
    if not root.exists():
        return skills

    for path in sorted(root.iterdir()):
        if not path.is_dir():
            continue
        if (path / "SKILL.md").is_file():
            files = {tuple(p.relative_to(path).parts) for p in path.rglob("*") if p.is_file()}
            skills[path.name] = files
    return skills


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    custom_skills = list_skill_dirs(CUSTOM_ROOT)
    mirror_skills = list_skill_dirs(MIRROR_ROOT)

    custom_names = set(custom_skills)
    mirror_names = set(mirror_skills)

    if custom_names != mirror_names:
        missing = custom_names - mirror_names
        extra = mirror_names - custom_names
        if missing:
            fail(f"missing mirrored skills in .codex/skills: {', '.join(sorted(missing))}")
        if extra:
            fail(f"unexpected extra skills in .codex/skills: {', '.join(sorted(extra))}")

    for name in sorted(custom_names):
        if custom_skills[name] != mirror_skills.get(name, set()):
            fail(f"mirroring mismatch for skill '{name}'")

    print("PASS: .custom and .codex/skills are mirrored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
