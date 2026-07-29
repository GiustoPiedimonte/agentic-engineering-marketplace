#!/usr/bin/env python3
"""Tests for the agentic-engineering `verify-refs` hook.

The hook exists because a claim a command can settle should not be spending a
reviewer's attention. That argument only holds if the checker is itself checked
by a command — so this runs in the same gate as everything else.

Run directly, or via `scripts/ci_validate.py`, which invokes it.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "plugins" / "agentic-engineering" / "hooks" / "verify-refs.py"

failures: list[str] = []


def run(md_path: Path | str, cwd: Path | str, *, raw_stdin: str | None = None):
    payload = raw_stdin
    if payload is None:
        payload = json.dumps({"cwd": str(cwd), "tool_input": {"file_path": str(md_path)}})
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return proc.returncode, proc.stderr


def expect(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        failures.append(f"{name}{': ' + detail if detail else ''}")


def main() -> int:
    if not HOOK.is_file():
        print(f"✗ hook not found at {HOOK.relative_to(ROOT)}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "src").mkdir()
        # line 1 = "alpha", line 2 = blank, line 3 = "gamma"
        (d / "src" / "target.py").write_text("alpha\n\ngamma\n", encoding="utf-8")

        # --- the two real findings -------------------------------------------
        md = d / "findings.md"
        md.write_text(
            "blank: src/target.py:2\nrange: src/target.py:99\n", encoding="utf-8"
        )
        code, err = run(md, d)
        expect("blank line reported", "src/target.py:2" in err and "blank" in err, err)
        expect("out of range reported", "src/target.py:99" in err and "3 lines" in err, err)
        expect("findings exit 2", code == 2, f"exit {code}")

        # --- everything that must stay silent --------------------------------
        md = d / "quiet.md"
        md.write_text(
            "good: src/target.py:1 and src/target.py:3\n"
            "missing path: src/imaginary.py:12\n"
            "url: https://example.com:8080/src/target.py:99\n"
            "time: 12:30 — version: 1.2:3 — image: python:3.11\n"
            "self: quiet.md:999\n",
            encoding="utf-8",
        )
        code, err = run(md, d)
        expect("clean file silent", code == 0 and err.strip() == "", f"exit {code}: {err}")

        # --- inputs that must never cost a turn -------------------------------
        for name, kwargs in [
            ("non-markdown file", {"md_path": d / "src" / "target.py", "cwd": d}),
            ("missing markdown file", {"md_path": d / "nope.md", "cwd": d}),
        ]:
            code, err = run(**kwargs)
            expect(f"{name} exits 0", code == 0 and err.strip() == "", f"exit {code}: {err}")

        for name, payload in [
            ("malformed json", "not json at all"),
            ("empty object", "{}"),
            ("empty stdin", ""),
            ("json scalar", "42"),
            ("null tool_input", '{"tool_input": null}'),
            ("non-string file_path", '{"tool_input": {"file_path": 42}}'),
        ]:
            code, err = run("", "", raw_stdin=payload)
            expect(f"{name} exits 0", code == 0 and err.strip() == "", f"exit {code}: {err}")

        # --- the report is capped ---------------------------------------------
        md = d / "many.md"
        md.write_text(
            "".join(f"ref {i}: src/target.py:{100 + i}\n" for i in range(20)),
            encoding="utf-8",
        )
        code, err = run(md, d)
        reported = err.count("  - ")
        expect("report capped at 5", reported == 5, f"reported {reported}")

        # --- a huge referenced file is skipped, not read (D2) -----------------
        big = d / "src" / "big.log"
        with big.open("w", encoding="utf-8") as fh:
            fh.write("x\n" * 1_200_000)  # > MAX_BYTES
        expect("fixture is over the cap", big.stat().st_size > 2_000_000)
        md = d / "big.md"
        md.write_text("huge: src/big.log:99999999\n", encoding="utf-8")
        code, err = run(md, d)
        expect("oversized target skipped", code == 0 and err.strip() == "", f"exit {code}: {err}")

        # --- no quadratic blowup on a long scheme-legal run (D1) --------------
        md = d / "pathological.md"
        md.write_text("a" * 200_000 + "\ntrailing: src/target.py:2\n", encoding="utf-8")
        started = time.monotonic()
        code, err = run(md, d)
        elapsed = time.monotonic() - started
        expect("pathological line stays fast", elapsed < 5.0, f"took {elapsed:.1f}s")
        expect("pathological line still finds the real ref", code == 2 and "blank" in err, err)

    if failures:
        print("✗ verify-refs hook:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("✓ verify-refs hook: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
