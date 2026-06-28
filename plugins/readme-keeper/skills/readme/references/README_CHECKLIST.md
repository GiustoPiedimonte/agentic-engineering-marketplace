# Public README — audit checklist & reference

A README is a contract: every claim in it (version, install command, link, badge)
is implicitly promised true. README *rot* is when reality moves and the README
doesn't. This checklist is phrased so each item is **verifiable** — pass/fail, not
vibes. Synthesized from the Art of README, the Standard Readme spec, GitHub's docs,
and the README conventions of high-star repos (transformers, langchain, ruff, gum).

## The honesty gate (the one rule above the rest)

**Never show a signal you cannot back.** No CI badge without a workflow. No
downloads badge without a registry. No Discord badge without a server. No static
`version-X.Y.Z` badge that a release will silently outdate. No "used by" without
real users. A broken or dishonest badge is worse than no badge — it signals
active neglect. When in doubt, drop it.

## Section order — the cognitive funnel

Order from broadest audience to narrowest. A newcomer should learn *what it is* in
10 seconds; an integrator should reach the API/usage without scrolling past noise.

1. **Hero** — banner/logo, a tight badge row (3–6, all honest), a one-line
   plain-English tagline, and a nav link row (`Install · Quickstart · Docs`).
2. **Why this exists** — the problem, then the claim, then immediate proof
   (benchmark, diagram, stat, or quote). Not marketing copy.
3. **Table of contents** — once the README exceeds ~100 lines or 5+ `##` sections.
   Clickable anchors.
4. **Install** — exact, copy-pasteable commands in a fenced block.
5. **Quickstart / Usage** — the smallest working example first, then richer ones.
6. **Features / What you get** — tables or bullets.
7. **Configuration · Requirements · Customize.**
8. **Project status / Maintaining / Roadmap** — signals active vs abandoned.
9. **Contributing** — where issues go, whether PRs are welcome, dev setup.
10. **License** — last. SPDX identifier + owner.

## Verifiable checks

### A. Content accuracy (README vs reality)
- [ ] Version stated/badged in the README matches the manifest (`package.json`,
      `pyproject.toml`, `plugin.json`, `Cargo.toml`, …). Prefer a **dynamic**
      badge that reads the registry/releases over a hardcoded number.
- [ ] Every install command runs clean on the default branch (try it).
- [ ] Every usage example reflects the current public API (no renamed flags,
      removed functions, dead import paths).
- [ ] Screenshots/GIFs depict the current output/UI.
- [ ] The stated project status matches actual activity.

### B. Link & anchor integrity
- [ ] Every **relative** link resolves to a file on the default branch.
- [ ] Every **external** URL returns 200 (or an acceptable redirect).
- [ ] Every **anchor** (`#section`) matches a heading that exists. (GitHub slugs:
      lowercase, spaces→`-`, punctuation/emoji stripped. Emoji headers produce
      fragile anchors — prefer clean headers.)
- [ ] Externally-hosted images are reachable.

### C. Badge integrity
- [ ] No badge renders `unknown` / `invalid` (fetch the badge URL; check the JSON
      `message`).
- [ ] Every badge is **clickable** and its target resolves — the idiom is
      `[![alt](image-url)](target-url)`, not a bare `![alt](image-url)`.
- [ ] Badge link targets are conventional: license→LICENSE file; version/release→
      releases or registry page; stars→stargazers; CI→the specific workflow.
- [ ] All badges share **one** `?style=` (don't mix `flat` / `flat-square` / `for-the-badge`).
- [ ] Every badge has non-empty, meaningful alt text.

### D. Metadata consistency
- [ ] README one-liner ≈ the GitHub "About" description (`gh repo view --json description`).
- [ ] README H1/title aligns with the repo/package name.
- [ ] License agrees across README, `LICENSE` file, and manifest `license` field.

### E. Style & structure
- [ ] Exactly one H1.
- [ ] No skipped heading levels (H2→H4).
- [ ] Every fenced code block has a language tag.
- [ ] No bare URLs outside `<…>` or links.
- [ ] No empty links `[text]()` / `[](url)`.

### F. Accessibility
- [ ] Every image has non-empty alt text that describes content (not the filename).
- [ ] No generic link text ("click here", "here", "learn more").
- [ ] README stays under GitHub's 500 KiB render limit.

### G. Freshness
- [ ] Changelog/release section matches the latest tag.
- [ ] Documented runtime/dependency versions match the manifest constraints.

## Top README-rot failure modes (and how to catch them)

| # | Failure mode | Detection |
|---|---|---|
| 1 | Version drift (static badge / install pin vs manifest) | diff the version string vs manifest; prefer dynamic badges |
| 2 | Dead relative links after a move/rename | link-check relative paths against the tree |
| 3 | Broken workflow-status badge (workflow renamed/deleted) | the `workflow=`/path no longer exists in `.github/workflows/` |
| 4 | Stale screenshots/GIFs | human review tied to the feature they show; meaningful filenames |
| 5 | Install command no longer works | run it in a clean env |
| 6 | External link rot | scheduled external link check |
| 7 | Badge shows `unknown`/`invalid` | fetch badge URL, grep the message |
| 8 | Translation drift (`README.zh.md` lags) | structural diff of headings between translations |

## Portable verification snippets

No tool installs required — these run with `git`, `curl`, `grep`, `bash`. Optional
heavier tools when available: `lychee` (link-check, supports `--include-fragments`),
`markdownlint` (style/structure: MD001/025/040/042/045), `cspell` (spelling).

```bash
# Relative links resolve (run from repo root)
grep -oE '\]\(([^)#][^)]*)\)' README.md | sed -E 's/.*\(([^)]+)\)/\1/' \
  | grep -vE '^https?:|^#|^mailto:' \
  | while read -r p; do [ -e "${p%%#*}" ] && echo "OK  $p" || echo "MISS $p"; done

# Anchor links match a heading
refs=$(grep -oE '\]\(#[a-z0-9-]+\)' README.md | grep -oE '#[a-z0-9-]+' | sort -u)
heads=$(grep -E '^#{1,6} ' README.md | sed -E 's/^#+ //' \
  | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9 -]//g; s/ /-/g; s/^/#/' | sort -u)
for r in $refs; do printf '%s\n' "$heads" | grep -qx "$r" \
  && echo "OK  $r" || echo "BROKEN $r"; done

# Dynamic badge not unknown/invalid
curl -s "<badge-image-url>" | grep -qiE 'unknown|invalid|not found' \
  && echo "PROBLEM" || echo "OK"

# Version consistency (example: a JSON manifest vs README)
v=$(grep -oE '"version"[^,]*' manifest.json | head -1)
echo "manifest: $v"; grep -n "$(echo "$v" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')" README.md || echo "not pinned in README (fine if using a dynamic badge)"
```

## Anti-patterns
- Walls of prose above the fold; bury the install command.
- Emoji in every heading (reads consumer-grade; also breaks anchors). Tasteful or none.
- Star-history charts / "used by" at low adoption — backfires.
- Adding a TOC to a 40-line README.
- Padding with badges for vanity instead of signal.
