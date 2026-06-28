# Elevate playbook — turn a README into a high-quality, repo-specific one

Auditing finds what's broken. **Elevating** rebuilds a thin or generic README into
a polished one — banner, honest badges, cognitive-funnel structure, callouts — with
every signal *derived from the actual repo*, not boilerplate. The honesty gate still
rules: only emit a badge/claim the repo can back.

The reference implementation is this very marketplace's own README and
`assets/banner.svg` — match that bar, adapted to the target repo's identity.

## Step 1 — Detect what the repo actually is

Read, don't assume. Gather the signals that decide the hero, the badges, and the
install command:

| Signal | How to detect | Drives |
|---|---|---|
| Stack / package manager | `package.json` (npm), `pyproject.toml`/`setup.py` (PyPI), `Cargo.toml` (crates), `go.mod`, `composer.json`, `Gemfile`, `pubspec.yaml` | install command, version/downloads badges |
| Published? | does the registry resolve the package name? (`npm view`, `pip index`, crates.io) | whether a version/downloads badge is *honest* |
| CI | `.github/workflows/*.yml` | build-status badge → that workflow |
| Releases | `git tag` / `gh release list` | release badge → releases |
| License | `LICENSE` + manifest `license` field | license badge |
| Identity | `gh repo view --json name,description,homepageUrl,repositoryTopics,stargazerCount` | wordmark, tagline, About sync, docs link |
| What it does | the existing README, entry points, CLI defs, `examples/`, top of `src` | the one-liner, "why", feature table |
| Real usage | a minimal example from `examples/`, tests, or docstrings | a *true* quickstart (don't invent API) |
| Visual identity | existing logo/brand colors, or the language's palette | banner palette, accent colors |

If the project is a CLI/agent/plugin (not a library), there is no registry — the
install path is the tool's own (`brew`, `claude plugin`, `npx`, a script). Detect
that and don't force a PyPI/npm badge.

## Step 2 — Choose badges from reality (honesty gate)

Emit **only** badges with a real backing artifact and a live click target. One
consistent `?style=`. Idiom is always `[![alt](image)](target)`.

| Badge | Emit when | shields image | Click target |
|---|---|---|---|
| License | a LICENSE exists | `img.shields.io/github/license/{owner}/{repo}` | `/blob/{branch}/LICENSE` |
| Last commit | always (GitHub) | `…/github/last-commit/{owner}/{repo}` | `/commits/{branch}` |
| Stars | always (GitHub) | `…/github/stars/{owner}/{repo}` | `/stargazers` |
| Release | a tag/release exists | `…/github/v/release/{owner}/{repo}` | `/releases` |
| CI build | a workflow exists | `…/github/actions/workflow/status/{owner}/{repo}/{file}.yml` | `/actions/workflows/{file}.yml` |
| npm version | published to npm | `…/npm/v/{pkg}` | `npmjs.com/package/{pkg}` |
| npm downloads | published to npm | `…/npm/dm/{pkg}` | same |
| PyPI version | published to PyPI | `…/pypi/v/{pkg}` | `pypi.org/project/{pkg}` |
| Python versions | published to PyPI | `…/pypi/pyversions/{pkg}` | same |
| crates.io | published to crates | `…/crates/v/{crate}` | `crates.io/crates/{crate}` |
| Docs | a docs site exists | static or `…/readthedocs/{slug}` | the docs URL |
| Discord | a live invite exists | `…/discord/{server_id}` | the invite |
| Custom info chip | a true static fact | `…/badge/{label}-{message}-{color}` | the relevant dir/page |

**Custom chips** are the repo-specific touch: a static `badge/<label>-<message>`
that states a true fact and links to the proof — e.g. `skills-5` → the `skills/`
dir, `models-300k` → the models page, `coverage-via-codecov` only if codecov is
wired. Derive the label/number from the repo; link it to where it's verifiable.
Never a vanity number with no link.

Keep the row tight: 3–6 badges. Drop anything that would render `unknown`.

## Step 3 — Build the hero

Two tiers; pick by ambition and asset support.

**Minimal (always safe):** a centered block — `<h1 align="center">name</h1>`, the
badge row, a one-line plain-English tagline, a nav row
(`[Install](#install) · [Quickstart](#quickstart) · [Docs](…)`).

**Full (signature look):** add an SVG banner at the top. Generate a terminal-card
SVG parameterized to the repo (see `assets/banner.svg` here as the template):
- a rounded dark card with three traffic-light dots and a faint title-bar label;
- a prompt line showing the real install command (`$ <install>`);
- the wordmark in a gradient (palette from the repo's brand or language);
- a **chips row** = the repo's primary commands / subpackages / pipeline stages
  (this is the most repo-specific element — derive it from the actual CLI verbs,
  workspaces, or workflow), each chip a labeled rounded rect;
- a caption line of the project's organizing idea.
Commit it to `assets/` and reference with descriptive `alt`. Verify it renders
(it must be static SVG — GitHub strips scripts).

## Step 4 — Fill the funnel with repo-derived content

Order: hero → why → (TOC if ≥100 lines/5+ sections) → install → quickstart →
features → config/requirements → maintaining → contributing → license.

- **Why this exists:** state the problem this repo solves, then prove it (a real
  benchmark, a diagram, a before/after) — pulled from the repo, not invented.
- **Install:** the *real* command for the detected manager.
- **Quickstart:** the smallest example that actually runs — lifted from
  `examples/`/tests, with a language-tagged fence.
- **Features / What you get:** a table built from the repo's real capabilities
  (commands, modules, integrations). For a multi-part repo, one row each.
- **Callouts:** convert load-bearing notes to `> [!NOTE]/[!TIP]/[!IMPORTANT]`.
- **Contributing / License:** point to real `CONTRIBUTING.md`/issues and the SPDX.

## Step 5 — Verify, don't assert

Re-run the audit checks (links, anchors, badge liveness, one H1, fenced-language,
version consistency, About-vs-tagline). Render-check the banner. A badge that
reads `unknown` or a dead link means the elevate isn't done.

## Guardrails
- **Preserve an existing style.** If the README already has a deliberate voice and
  structure, improve within it — don't replace it with this template.
- **Gate big rewrites on human confirmation.** A light pass (badges, TOC, callouts,
  fixed links, tightened prose) can proceed. A substantial transformation (new
  voice, restructured sections, dropped content, a banner where none existed) must
  be presented as a plan and approved by the human first. The human owns the voice.
- Never fabricate adoption ("used by X"), benchmarks, or API that isn't there.
- Never emit a registry/CI/community badge without the backing artifact.
- Keep it maintainable — prefer dynamic badges (read live) over hardcoded numbers.
