#!/usr/bin/env python3
"""PostToolUse hook: verify `path:line` claims written into markdown.

A `file:line` reference is a claim, and it is the kind of claim a reviewer
nods at and a command settles. This checks the ones that can be checked:
after markdown is written or edited, every `path:line` in it whose path
resolves on disk must point at a line that exists and is not blank.

Deliberately conservative — it reports only when the file is really there and
the line is really wrong, so a clean run is silent and a report is never a
guess. References to paths that do not resolve (illustrative examples, other
repos, planned files) are skipped rather than flagged.

Exit 2 shows stderr to Claude without blocking (PostToolUse already ran).
Any unexpected failure exits 0: this hook never costs anyone a turn.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MAX_BYTES = 2_000_000
MAX_REPORTS = 5

# foo/bar.ts:42 — path with an extension, then a line number.
REF = re.compile(r"(?<![\w:/.\-])((?:[\w.\-]+/)*[\w.\-]+\.[A-Za-z0-9]{1,8}):(\d{1,6})(?![\w.\-])")
# Scheme length is bounded on purpose: an unbounded `*` before `://` backtracks
# quadratically over a long unbroken run of scheme-legal characters, which a
# generated or minified line can supply. No real scheme is 16 characters.
URL = re.compile(r"[a-zA-Z][a-zA-Z0-9+.\-]{0,15}://\S+")


def repo_root(start: Path) -> Path | None:
    for d in [start, *start.parents]:
        if (d / ".git").exists():
            return d
    return None


def resolve(ref: str, md_dir: Path, cwd: Path) -> Path | None:
    """First existing candidate wins; None means 'not ours to judge'."""
    roots = [md_dir, cwd]
    root = repo_root(md_dir)
    if root is not None:
        roots.append(root)
    for base in roots:
        candidate = base / ref
        if candidate.is_file():
            return candidate
    return None


def read_target(ref: str, md: Path, md_dir: Path, cwd: Path) -> list[str] | None:
    """Lines of the referenced file, or None when it is not ours to judge."""
    target = resolve(ref, md_dir, cwd)
    if target is None:
        return None
    try:
        if target.stat().st_size > MAX_BYTES or target.resolve() == md.resolve():
            return None
        return target.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    path_str = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path_str.endswith((".md", ".mdx")):
        return 0

    md = Path(path_str)
    if not md.is_file() or md.stat().st_size > MAX_BYTES:
        return 0

    try:
        text = md.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd())
    md_dir = md.parent

    findings: list[str] = []
    seen: set[tuple[str, int]] = set()
    # Referenced files are read at most once each, and only if they are small
    # enough to be something a `file:line` could sanely point at.
    cache: dict[str, list[str] | None] = {}

    def lines_of(ref: str) -> list[str] | None:
        if ref not in cache:
            cache[ref] = read_target(ref, md, md_dir, cwd)
        return cache[ref]

    for raw_line in URL.sub(" ", text).splitlines():
        for ref, num in REF.findall(raw_line):
            line_no = int(num)
            if (ref, line_no) in seen:
                continue
            seen.add((ref, line_no))

            lines = lines_of(ref)
            if lines is None:
                continue

            if line_no < 1 or line_no > len(lines):
                findings.append(f"{ref}:{line_no} — file has {len(lines)} lines")
            elif not lines[line_no - 1].strip():
                findings.append(f"{ref}:{line_no} — that line is blank")

            if len(findings) >= MAX_REPORTS:
                break
        if len(findings) >= MAX_REPORTS:
            break

    if not findings:
        return 0

    print(
        f"Unverified file:line references in {md.name} — check each one against "
        "the file and fix or drop it:",
        file=sys.stderr,
    )
    for f in findings:
        print(f"  - {f}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # never break a turn over a doc check
        sys.exit(0)
