#!/usr/bin/env python3
"""Deterministic, network-free validation for this marketplace.

Checks, in CI and locally:
  - every *.json parses;
  - each plugin's plugin.json name/version agrees with its marketplace entry;
  - each SKILL.md has frontmatter with name + description;
  - each README: exactly one H1, every fenced code block has a language tag,
    no empty links, and every relative link / <img src> resolves on disk.

Exit 1 on any failure. No external network calls (external-link liveness is
checked by the /readme skill, not gated in CI).
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def check_json_parses() -> None:
    for p in ROOT.rglob("*.json"):
        if ".git" in p.parts:
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            err(f"{p.relative_to(ROOT)}: invalid JSON — {e}")


def check_manifests() -> None:
    mkt_path = ROOT / ".claude-plugin" / "marketplace.json"
    mkt = json.loads(mkt_path.read_text(encoding="utf-8"))
    entries = {p["name"]: p for p in mkt.get("plugins", [])}
    for name, entry in entries.items():
        src = (ROOT / entry["source"]).resolve()
        pj = src / ".claude-plugin" / "plugin.json"
        if not pj.exists():
            err(f"marketplace lists '{name}' but {pj.relative_to(ROOT)} is missing")
            continue
        plugin = json.loads(pj.read_text(encoding="utf-8"))
        if plugin.get("name") != name:
            err(f"{pj.relative_to(ROOT)}: name '{plugin.get('name')}' != marketplace entry '{name}'")
        if plugin.get("version") != entry.get("version"):
            err(f"{name}: plugin.json version '{plugin.get('version')}' != marketplace entry '{entry.get('version')}'")


def check_skills() -> None:
    for skill in ROOT.rglob("skills/*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        rel = skill.relative_to(ROOT)
        if not text.startswith("---"):
            err(f"{rel}: missing YAML frontmatter")
            continue
        block = text.split("---", 2)[1] if text.count("---") >= 2 else ""
        if not re.search(r"^name:\s*\S", block, re.M):
            err(f"{rel}: frontmatter missing 'name'")
        if not re.search(r"^description:\s*\S", block, re.M):
            err(f"{rel}: frontmatter missing 'description'")


def check_readme(md: Path) -> None:
    rel = md.relative_to(ROOT)
    lines = md.read_text(encoding="utf-8").splitlines()

    # exactly one H1 (markdown '# ' or an <h1> tag)
    h1 = sum(1 for ln in lines if ln.startswith("# ") or "<h1" in ln)
    if h1 != 1:
        err(f"{rel}: expected exactly one H1, found {h1}")

    # fenced code blocks must declare a language
    in_fence = False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            if not in_fence:
                lang = ln.lstrip()[3:].strip()
                if lang == "":
                    err(f"{rel}:{i}: code fence without a language tag")
                in_fence = True
            else:
                in_fence = False

    text = "\n".join(lines)
    # empty links
    for m in re.finditer(r"\]\(\s*\)", text):
        err(f"{rel}: empty link target '](...)' near offset {m.start()}")

    # relative markdown links and <img src> must resolve
    targets = re.findall(r"\]\(([^)]+)\)", text) + re.findall(r'src="([^"]+)"', text)
    for t in targets:
        t = t.strip().split()[0]  # drop optional "title"
        if t.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = t.split("#", 1)[0]
        if not path:
            continue
        if not (md.parent / path).exists():
            err(f"{rel}: relative link does not resolve → {t}")


def main() -> int:
    check_json_parses()
    check_manifests()
    check_skills()
    readmes = [ROOT / "README.md"] + sorted(ROOT.glob("plugins/*/README.md"))
    for md in readmes:
        check_readme(md)

    if errors:
        print(f"✗ {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("✓ all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
