---
name: readme
description: >
  This skill should be used to audit, improve, or maintain the README of a public
  repository to a high standard. Trigger with "improve the README", "audit the
  readme", "is our README good", "make the readme public-ready", "check the badges
  / links", or before publishing/releasing a repo. Honesty-first: never adds a
  signal the repo can't back. Produces a verifiable findings report, then fixes.
metadata:
  version: "0.1.0"
---

# /readme — audit & maintain a public README

A README is a contract: every claim in it — version, install command, link, badge
— is implicitly promised true. This skill keeps that contract honest and the
document high-quality. `$ARGUMENTS` is the target (a path, default `README.md`) and
optionally `audit` (report only) or `fix` (apply changes). Default: audit, then
offer to fix.

The governing rule is the **honesty gate**: never show a signal you cannot back.
No CI badge without a workflow, no version badge a release will outdate, no
"used by" without real users. A broken or dishonest badge is worse than none.

## Process

1. **Establish ground truth — read, don't assume.** Before judging anything,
   gather the facts the README must agree with:
   - repo name, default branch, and the GitHub "About" description (`gh repo view`);
   - the manifest(s) and their `version` / `license` (e.g. `package.json`,
     `pyproject.toml`, `plugin.json`, `marketplace.json`);
   - whether real infrastructure exists: `.github/workflows/`, a published
     registry package, git tags/releases, a community link. This decides which
     badges are *honest*.

2. **Audit against the checklist.** Run the verifiable checks in
   `references/README_CHECKLIST.md` — content accuracy, link & anchor integrity,
   badge integrity, metadata consistency, style/structure, accessibility,
   freshness. Use the portable `git`/`curl`/`grep` snippets there (no installs
   required); reach for `lychee` / `markdownlint` / `cspell` only if present.
   Delegate wide reads or live-URL checks to a read-only research subagent when
   one is available, to keep the main context clean.

3. **Report findings as pass/fail with specifics** — `file:line`, the broken
   link/anchor, the drifted version, the dishonest badge. Rank by impact
   (broken/dishonest > missing structure > style > nits). No "looks fine" —
   either a check passed or it failed.

4. **Fix to the cognitive funnel.** When applying changes, structure the README
   broadest-audience-first (hero → why → install → quickstart → features →
   config → maintaining → contributing → license; see the checklist). Make every
   badge clickable (`[![alt](img)](target)`) and honest. Prefer **dynamic** badges
   (read the registry/releases live) over hardcoded numbers that drift. Use clean
   headings for reliable anchors; add a TOC once the README passes ~100 lines or
   5+ sections. Convert load-bearing notes to GitHub callouts
   (`> [!NOTE]` / `[!TIP]` / `[!IMPORTANT]`). Keep alt text meaningful.

5. **Verify the fixes, don't assert them.** Re-run the link/anchor/badge checks
   after editing and show the output. A README change isn't done until the new
   links resolve and no badge reads `unknown`.

## What to add only if real
Release/version badge → only with a tag or registry release. CI badge → only with
a workflow. Community badge → only with a live invite. Screenshots → only current
ones. Everything else honest-by-default: license, stars, last-commit are live and
safe; a banner and an ASCII/diagram are always fair game.

## Output
A ranked findings report (passed / failed checks with specifics), the concrete
edits proposed or applied, and the re-verification output. If publishing, confirm
the README one-liner matches the GitHub "About" description and that the license
agrees across README, `LICENSE`, and manifest.
