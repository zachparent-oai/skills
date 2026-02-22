#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["typer>=0.12"]
# ///

"""Lint markdown references for local file existence and external URL validity."""

from __future__ import annotations

import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import typer

REPO_ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIR_NAMES = {
    ".git",
    ".pre-commit-cache",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "node_modules",
    "__pycache__",
}
DEFAULT_MD_DIRS = (
    Path("skills/.custom"),
)
PATHLIKE_CODE_PREFIXES = (
    "skills/",
    ".codex/skills/",
    "scripts/",
    "evals/",
    "references/",
    "agents/",
    "./",
    "../",
)
PATHLIKE_CODE_EXACT = {"AGENTS.md", "README.md", "contributing.md"}

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
BARE_URL_RE = re.compile(r"https?://[^\s<>)`]+")


@dataclass(frozen=True)
class RefIssue:
    path: Path
    line: int
    message: str


@dataclass(frozen=True)
class LocalRef:
    source_path: Path
    line: int
    raw: str


@dataclass(frozen=True)
class ExternalRef:
    source_path: Path
    line: int
    url: str


@dataclass
class UrlCheckResult:
    status: Literal["ok", "skipped", "error"]
    detail: str


app = typer.Typer(help="Lint markdown links and code-path references.")


def _iter_markdown_files(root: Path, scope: Literal["custom", "all"]) -> list[Path]:
    files: list[Path] = []
    if scope == "all":
        scan_roots = [root]
    else:
        scan_roots = [root / rel for rel in DEFAULT_MD_DIRS]

    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*.md"):
            if not path.is_file():
                continue
            if any(part in IGNORED_DIR_NAMES for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def _line_number(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def _strip_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    # Remove optional markdown title if present: (path "title")
    if " " in target and not target.startswith("http"):
        # local links with spaces are rare in this repo; keep only first token
        target = target.split(" ", 1)[0]
    elif " " in target and target.startswith("http"):
        target = target.split(" ", 1)[0]
    return target


def _normalize_external_url(url: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError:
        return url
    clean = parsed._replace(fragment="")
    return urllib.parse.urlunsplit(clean)


def _resolve_local_ref(source_path: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return None
    if "://" in target or target.startswith("mailto:"):
        return None
    if "$" in target or "<" in target or ">" in target:
        return None

    # Strip query/fragment for filesystem resolution.
    target = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None

    path_obj = Path(target)
    if path_obj.is_absolute():
        try:
            resolved = path_obj.resolve()
        except OSError:
            return None
        if resolved == REPO_ROOT or REPO_ROOT in resolved.parents:
            return resolved
        return None

    candidates = [(source_path.parent / path_obj).resolve()]
    candidates.append((REPO_ROOT / path_obj).resolve())
    for candidate in candidates:
        if candidate == REPO_ROOT or REPO_ROOT in candidate.parents:
            return candidate
    return candidates[0]


def _is_pathlike_code_token(token: str) -> bool:
    if not token or "\n" in token or "://" in token:
        return False
    if " " in token:
        return False
    if token.endswith("/"):
        return False
    if "$" in token or "*" in token:
        return False
    if token in PATHLIKE_CODE_EXACT:
        return True
    if token.startswith(PATHLIKE_CODE_PREFIXES):
        return True
    return False


def _extract_refs(path: Path) -> tuple[list[LocalRef], list[ExternalRef]]:
    text = path.read_text()
    local_refs: list[LocalRef] = []
    external_refs: list[ExternalRef] = []
    seen_local: set[tuple[int, str]] = set()
    seen_external: set[tuple[int, str]] = set()

    for match in MD_LINK_RE.finditer(text):
        raw_target = _strip_link_target(match.group(1))
        line = _line_number(text, match.start())
        if raw_target.startswith("http://") or raw_target.startswith("https://"):
            norm = _normalize_external_url(raw_target)
            key = (line, norm)
            if key not in seen_external:
                seen_external.add(key)
                external_refs.append(ExternalRef(source_path=path, line=line, url=norm))
            continue
        resolved = _resolve_local_ref(path, raw_target)
        if resolved is not None:
            key = (line, raw_target)
            if key not in seen_local:
                seen_local.add(key)
                local_refs.append(LocalRef(source_path=path, line=line, raw=str(raw_target)))

    for match in INLINE_CODE_RE.finditer(text):
        token = match.group(1).strip()
        if not _is_pathlike_code_token(token):
            continue
        resolved = _resolve_local_ref(path, token)
        if resolved is None:
            continue
        line = _line_number(text, match.start())
        key = (line, token)
        if key not in seen_local:
            seen_local.add(key)
            local_refs.append(LocalRef(source_path=path, line=line, raw=token))

    for match in BARE_URL_RE.finditer(text):
        url = _normalize_external_url(match.group(0).rstrip(".,])"))
        line = _line_number(text, match.start())
        key = (line, url)
        if key not in seen_external:
            seen_external.add(key)
            external_refs.append(ExternalRef(source_path=path, line=line, url=url))

    return local_refs, external_refs


def _check_local_ref(ref: LocalRef) -> RefIssue | None:
    resolved = _resolve_local_ref(ref.source_path, ref.raw)
    if resolved is None:
        return None
    if not resolved.exists():
        rel_source = ref.source_path.relative_to(REPO_ROOT)
        return RefIssue(
            path=rel_source,
            line=ref.line,
            message=f"missing local reference: {ref.raw}",
        )
    return None


def _request_url(url: str, timeout_seconds: float, method: str) -> UrlCheckResult:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "skills-md-link-lint/1.0"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            code = getattr(resp, "status", 200)
            return UrlCheckResult(status="ok", detail=f"HTTP {code}")
    except urllib.error.HTTPError as exc:
        if exc.code == 405 and method == "HEAD":
            return _request_url(url, timeout_seconds, "GET")
        if exc.code in {401, 403}:
            return UrlCheckResult(status="ok", detail=f"HTTP {exc.code}")
        if exc.code in {404, 410}:
            return UrlCheckResult(status="error", detail=f"HTTP {exc.code}")
        return UrlCheckResult(status="error", detail=f"HTTP {exc.code}")
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            return UrlCheckResult(status="skipped", detail=f"network/DNS unavailable: {reason}")
        return UrlCheckResult(status="skipped", detail=f"network error: {reason}")
    except TimeoutError:
        return UrlCheckResult(status="skipped", detail="timeout")
    except OSError as exc:
        return UrlCheckResult(status="skipped", detail=f"os error: {exc}")


def _check_external_refs(
    refs: list[ExternalRef],
    *,
    web_mode: Literal["auto", "strict", "off"],
    timeout_seconds: float,
) -> tuple[list[RefIssue], int, int]:
    if web_mode == "off":
        return [], 0, 0

    issues: list[RefIssue] = []
    checked = 0
    skipped = 0
    seen_urls: set[str] = set()
    url_results: dict[str, UrlCheckResult] = {}
    offline_assumed = False
    consecutive_skips = 0

    for ref in refs:
        if ref.url not in seen_urls:
            seen_urls.add(ref.url)
            checked += 1
            if web_mode == "auto" and offline_assumed:
                result = UrlCheckResult(
                    status="skipped",
                    detail="assumed offline after repeated network errors",
                )
            else:
                result = _request_url(ref.url, timeout_seconds, "HEAD")
            if result.status == "skipped":
                skipped += 1
                consecutive_skips += 1
                if web_mode == "auto" and consecutive_skips >= 3:
                    offline_assumed = True
            else:
                consecutive_skips = 0
            url_results[ref.url] = result

    for ref in refs:
        result = url_results[ref.url]
        if result.status == "ok":
            continue
        if result.status == "skipped" and web_mode == "auto":
            continue
        rel_source = ref.source_path.relative_to(REPO_ROOT)
        issues.append(
            RefIssue(
                path=rel_source,
                line=ref.line,
                message=f"external URL check failed ({result.detail}): {ref.url}",
            )
        )
    return issues, checked, skipped


def lint_markdown_references(
    *,
    root: Path = REPO_ROOT,
    scope: Literal["custom", "all"] = "custom",
    web_mode: Literal["auto", "strict", "off"] = "strict",
    timeout_seconds: float = 5.0,
) -> int:
    files = _iter_markdown_files(root, scope)
    local_refs: list[LocalRef] = []
    external_refs: list[ExternalRef] = []
    for path in files:
        local, external = _extract_refs(path)
        local_refs.extend(local)
        external_refs.extend(external)

    local_issues: list[RefIssue] = []
    for ref in local_refs:
        issue = _check_local_ref(ref)
        if issue is not None:
            local_issues.append(issue)

    external_issues, urls_checked, urls_skipped = _check_external_refs(
        external_refs,
        web_mode=web_mode,
        timeout_seconds=timeout_seconds,
    )

    issues = local_issues + external_issues
    for issue in sorted(issues, key=lambda x: (str(x.path), x.line, x.message)):
        print(f"FAIL: {issue.path}:{issue.line}: {issue.message}")

    unique_external = {ref.url for ref in external_refs}
    print(
        "INFO: markdown reference lint scanned "
        f"{len(files)} markdown files ({scope} scope), "
        f"{len(local_refs)} local refs, {len(unique_external)} unique URLs"
    )
    if web_mode == "off":
        print("INFO: external URL checks disabled (--web-mode off)")
    elif web_mode == "auto" and urls_skipped:
        print(
            "WARN: skipped "
            f"{urls_skipped}/{urls_checked} URL checks due network restrictions/errors (auto mode)"
        )
        if urls_checked and urls_skipped == urls_checked:
            print(
                "WARN: assuming offline environment for web checks; "
                "rerun with --web-mode strict when network is available"
            )

    if issues:
        return 1

    print("PASS: markdown references are valid")
    return 0


@app.callback(invoke_without_command=True)
def main(
    root: Path = typer.Option(REPO_ROOT, "--root", help="Repo root to scan for markdown files."),
    scope: Literal["custom", "all"] = typer.Option(
        "custom",
        "--scope",
        help="Markdown scan scope: custom (skills/.custom only) or all repo markdown.",
    ),
    web_mode: Literal["auto", "strict", "off"] = typer.Option(
        "strict",
        "--web-mode",
        help="External URL checking mode: strict (default), auto (skip network errors), or off.",
    ),
    timeout_seconds: float = typer.Option(
        5.0,
        "--timeout-seconds",
        min=1.0,
        help="Timeout per external URL request.",
    ),
) -> None:
    """Lint markdown references across the repo."""
    raise typer.Exit(
        code=lint_markdown_references(
            root=root,
            scope=scope,
            web_mode=web_mode,
            timeout_seconds=timeout_seconds,
        )
    )


if __name__ == "__main__":
    app()
