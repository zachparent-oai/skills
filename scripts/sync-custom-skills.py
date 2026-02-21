#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

"""Compile `.custom` skills into `.codex/skills` for local Codex discovery."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> tuple[Path, Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--custom-root",
        default="skills/.custom",
        help="Source directory for custom skills",
    )
    parser.add_argument(
        "--mirror-root",
        default=".codex/skills",
        help="Target directory for mirrored skills",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    custom_root = (root / args.custom_root).resolve()
    mirror_root = (root / args.mirror_root).resolve()
    return custom_root, mirror_root


def sync_skills(custom_root: Path, mirror_root: Path) -> list[str]:
    if not custom_root.is_dir():
        raise SystemExit(f"FAIL: custom skills root not found: {custom_root}")

    mirror_root.mkdir(parents=True, exist_ok=True)

    # Clear any prior .custom link/copy in mirror root.
    legacy_marker = mirror_root / ".custom"
    if legacy_marker.is_symlink() or legacy_marker.exists():
        if legacy_marker.is_dir() and not legacy_marker.is_symlink():
            shutil.rmtree(legacy_marker)
        else:
            legacy_marker.unlink()

    expected: set[str] = set()

    for skill_dir in sorted(custom_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").is_file():
            continue

        skill_name = skill_dir.name
        expected.add(skill_name)
        target = mirror_root / skill_name

        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.copytree(skill_dir, target)

    for entry in sorted(mirror_root.iterdir()):
        if not entry.is_dir():
            continue
        if not entry.name.startswith(".") and entry.name not in expected:
            shutil.rmtree(entry)

    return sorted(expected)


def main() -> int:
    custom_root, mirror_root = parse_args()
    synced = sync_skills(custom_root, mirror_root)
    for name in synced:
        print(f"synced: .codex/skills/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
