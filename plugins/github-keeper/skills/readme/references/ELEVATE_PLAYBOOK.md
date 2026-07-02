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
| Last commit | *volatile* — see below | `…/github/last-commit/{owner}/{repo}` | `/commits/{branch}` |
| Stars | *volatile* — see below | `…/github/stars/{owner}/{repo}` | `/stargazers` |
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

**Honest *and* not self-undermining (stable vs volatile).** All dynamic badges
auto-update (shields fetches live, ~5-min cache) — none need manual upkeep. But
"auto-updates" ≠ "should be shown":

- **Stable & meaningful** — `license`, `release`/version, `CI` status, registry
  version. They reflect the project's quality and don't fluctuate. Prefer these.
- **Volatile / vanity** — `stars`, `last-commit`. Optional, and they can backfire:
  a `stars` badge reading `1` says "nobody uses this," and **`last-commit`
  auto-advertises dormancy** — it will honestly update to "last commit 9 months
  ago" the moment the repo goes quiet. Use them only on an active, popular repo
  where they flatter; on a young or intermittently-maintained one, omit them.

The gate isn't just "is it true?" but "does it help, even six months from now?"

### The adaptive proposal set (project + maintainer, not a fixed list)

Badges are one instance of a wider idea: **propose the elements — badges, links,
and sections — that fit *this* project and *this* maintainer.** Propose from what's
**detectable**; ask at most **2–3** high-value questions for what isn't (a
community? sponsors? socials?). Never interrogate, never block on answers.

| Detected / asked | Propose |
|---|---|
| a community (Discord/Slack/forum) | a community badge **and** a Community section + invite |
| GitHub Sponsors / Open Collective | a sponsor badge + a short support line |
| a docs site | a docs badge + a Documentation link/section |
| published to a registry | version / downloads badges |
| active maintainer socials (X, Mastodon, blog) | a follow link in the footer |
| a company / org behind it | a "built by" line, if the maintainer wants it |
| screenshots / a CLI demo | a screenshot or an asciinema demo block |

Every proposal is bound by the **honesty gate** (only if it's real) and
**propose-and-confirm** (never added unasked). The output is a menu tailored to the
project and person — "you have a Discord, want a community badge + section?" — not a
one-size checklist.

## Step 3 — Build the hero (propose the archetype, confirm, then generate)

The hero must fit the project, not this marketplace. **Propose a direction and get a
yes before generating any visual** — never autonomously produce a banner.

**1. Classify the archetype** from the identity signals (Step 1):

| Archetype | Fits | Hero |
|---|---|---|
| Terminal-card | CLI, dev-tool, agent | dark card + prompt + chips (`assets/banner.svg` here is this example) |
| Typographic | library, framework, SDK | clean wordmark + type, palette from the brand |
| Screenshot-led | UI / app / dashboard | a real, current screenshot |
| Diagram-led | infra, protocol, data | an architecture / flow diagram |
| Illustrated | creative / consumer tool | an illustrated, branded hero |
| **Minimal / none** | serious tools (à la ruff/biome) | **no banner** — just a clean `<h1>` type hero |

**2. Propose + confirm.** State the chosen archetype, the palette (from the
logo/brand), and the voice — e.g. "typographic hero, indigo from your logo, no
terminal-card." Wait for approval. "No banner is the faithful choice here" is a
legitimate proposal.

**3. Generate within that language** (only after approval):
- **Minimal (always safe):** a centered `<h1>`, the badge row, a one-line tagline,
  a nav row (`[Install](#install) · [Quickstart](#quickstart) · [Docs](…)`).
- **A generated banner**, when the archetype calls for one: author a *static* SVG in
  the project's palette and idiom. For the **terminal-card** archetype,
  `assets/banner.svg` here is a worked example — a dark card with traffic-light dots,
  a prompt line with the real install command, a gradient wordmark, a chips row of
  the project's real commands/modules, and a caption. Other archetypes take their own
  form (type, screenshot, diagram, illustration). Commit to `assets/` with a
  descriptive `alt`; verify it renders (static SVG only — GitHub strips scripts).

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
