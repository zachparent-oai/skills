#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///

"""Sync and verify `.custom` skills into the `.codex/skills` overlay."""

from __future__ import annotations

import shutil
from pathlib import Path

import typer

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CUSTOM_ROOT = REPO_ROOT / "skills" / ".custom"
DEFAULT_MIRROR_ROOT = REPO_ROOT / ".codex" / "skills"

app = typer.Typer(help="Sync and verify .custom skills in the .codex/skills overlay.")


def _resolve(path_like: str | Path) -> Path:
    value = Path(path_like)
    return value if value.is_absolute() else (REPO_ROOT / value).resolve()


def sync_skills(custom_root: Path, mirror_root: Path, dry_run: bool = False) -> list[str]:
    if not custom_root.is_dir():
        raise SystemExit(f"FAIL: custom skills root not found: {custom_root}")

    if dry_run:
        return [
            skill_dir.name
            for skill_dir in sorted(custom_root.iterdir())
            if (
                skill_dir.is_dir()
                and not skill_dir.name.startswith(".")
                and (skill_dir / "SKILL.md").is_file()
            )
        ]

    mirror_root.mkdir(parents=True, exist_ok=True)

    # Clear any prior .custom marker in mirror root.
    legacy_marker = mirror_root / ".custom"
    if legacy_marker.is_symlink() or legacy_marker.exists():
        if legacy_marker.is_dir() and not legacy_marker.is_symlink():
            shutil.rmtree(legacy_marker)
        else:
            legacy_marker.unlink()

    for skill_dir in sorted(custom_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").is_file():
            continue

        skill_name = skill_dir.name
        target = mirror_root / skill_name

        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.copytree(skill_dir, target)

    return [
        skill_dir.name
        for skill_dir in sorted(custom_root.iterdir())
        if (
            skill_dir.is_dir()
            and not skill_dir.name.startswith(".")
            and (skill_dir / "SKILL.md").is_file()
        )
    ]


def list_skill_dirs(root: Path) -> dict[str, set[tuple[str, ...]]]:
    skills: dict[str, set[tuple[str, ...]]] = {}
    if not root.exists():
        return skills

    for path in sorted(root.iterdir()):
        if not path.is_dir():
            continue
        if not (path / "SKILL.md").is_file():
            continue
        files = {tuple(p.relative_to(path).parts) for p in path.rglob("*") if p.is_file()}
        skills[path.name] = files
    return skills


def check_skills(custom_root: Path, mirror_root: Path) -> int:
    custom_skills = list_skill_dirs(custom_root)
    mirror_skills = list_skill_dirs(mirror_root)

    custom_names = set(custom_skills)
    mirror_names = set(mirror_skills)

    missing = custom_names - mirror_names
    if missing:
        raise SystemExit(
            f"FAIL: missing mirrored skills in .codex/skills: {', '.join(sorted(missing))}"
        )

    for name in sorted(custom_names):
        if custom_skills[name] != mirror_skills.get(name, set()):
            raise SystemExit(f"FAIL: mirroring mismatch for skill '{name}'")

    print("PASS: all .custom skills are mirrored in .codex/skills (extras allowed)")
    return 0


def _run_sync(custom_root: str, mirror_root: str, dry_run: bool) -> None:
    custom_root_path = _resolve(custom_root)
    mirror_root_path = _resolve(mirror_root)
    skills = sync_skills(custom_root_path, mirror_root_path, dry_run=dry_run)
    if dry_run:
        print(f"dry-run: scanning {custom_root_path} -> {mirror_root_path}")
        for skill in skills:
            print(f"would sync: {skill}")
        return

    for skill in skills:
        print(f"synced: {Path('.codex/skills') / skill}")


def _run_check(custom_root: str, mirror_root: str) -> None:
    custom_root_path = _resolve(custom_root)
    mirror_root_path = _resolve(mirror_root)
    check_skills(custom_root_path, mirror_root_path)


@app.command("sync")
def sync(
    custom_root: str = typer.Option(
        str(DEFAULT_CUSTOM_ROOT),
        "--custom-root",
        help="Source directory for custom skills.",
    ),
    mirror_root: str = typer.Option(
        str(DEFAULT_MIRROR_ROOT),
        "--mirror-root",
        help="Target directory for mirrored skills.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show planned sync updates without writing files.",
    ),
) -> None:
    """Copy `.custom` skills into `.codex/skills` without deleting extra repo skills."""
    _run_sync(custom_root=custom_root, mirror_root=mirror_root, dry_run=dry_run)


@app.command("check")
def check(
    custom_root: str = typer.Option(
        str(DEFAULT_CUSTOM_ROOT),
        "--custom-root",
        help="Source directory for custom skills.",
    ),
    mirror_root: str = typer.Option(
        str(DEFAULT_MIRROR_ROOT),
        "--mirror-root",
        help="Target directory for mirrored skills.",
    ),
) -> None:
    """Verify every `.custom` skill exists and matches in `.codex/skills`."""
    _run_check(custom_root=custom_root, mirror_root=mirror_root)


@app.callback(invoke_without_command=True)
def _default(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        sync(
            custom_root=str(DEFAULT_CUSTOM_ROOT),
            mirror_root=str(DEFAULT_MIRROR_ROOT),
            dry_run=False,
        )


if __name__ == "__main__":
    app()
