# Decisions

Append-only. One decision per block, dated, never edited. A revised decision is a
new ADR that supersedes the old one. This is the authoritative record of *why* we
decided things — not a plan, not a backlog.

## ADR-001 — The fidelity gate (derive from the project, not from us)
**Date:** 2026-06-29
**Status:** accepted
**Decision:** `/readme` (github-keeper) gains a **fidelity gate**: before generating
any visual, voice, or proposable element, it derives the direction from the target
**project's own communication** (logo, palette, tone, domain, audience) and
**proposes-and-confirms** with the human before producing anything. Our
`assets/banner.svg` terminal-card is demoted from "the template" to one archetype
among several, and "no banner / minimal" is a valid recommendation. The fidelity
gate is ranked **below** the honesty gate.
**Context:** Field feedback: the skill imposed our house style ("le immagini vengono
generate troppo secondo quello standard invece che prendere la comunicazione del
progetto"). The elevate playbook literally told the agent to reuse our banner as the
template, so libraries, UI apps, and research repos all trended toward our terminal
aesthetic. Detecting a project's identity is error-prone.
**Rationale:** Imposing one house look is both low-quality (wrong for most repos) and
a subtle dishonesty (an identity that isn't the project's). Making the gate
propose-and-confirm de-risks the unreliable detection — a wrong guess costs a
sentence, not a rebuild — and matches the "more collaborative" ask. Ranking it below
honesty resolves conflicts: a project's vibe never justifies a signal the repo can't
back.
**Consequences:**
- `elevate` is no longer a one-shot rebuild to a fixed look; it proposes a direction
  first. Slightly more interactive, materially more faithful.
- The badge/section guidance becomes an adaptive proposal set (project + maintainer),
  not a fixed checklist — with an "ask at most 2–3 questions" bound to avoid an
  intake interrogation.
- Extends the existing "preserve an existing style / gate big rewrites" rule from
  prose to visuals and brand.
- Out of scope for this slice: beyond-README docs, a formal iterative mode,
  translations, a banner-generator script.

## ADR-002 — Agentic engineering is graph engineering (name the lens, add /graph)
**Date:** 2026-07-23
**Status:** accepted
**Decision:** Adopt **graph engineering** as the explicit organizing lens of the
agentic-engineering plugin, and add a `/graph` skill plus a general `verifier` agent
to make it operational. The existing cycle is reframed, not replaced: `/pitch` shapes
and now names the graph a piece of work touches + its gated edges; `/graph` fans work
out across a fleet of subagents on dynamic workflows; `/ship` serializes the one
writer; `/eval` and `/measure` verify on real data. Ship `GRAPH_MODEL.md` (grammar +
five graphs + topology-first principles) and `WORKFLOW_LIBRARY.md` (six starter
scripts). The plugin **keeps its name** (`agentic-engineering`) so every consumer's
`.claude/settings.json` reference keeps working; a rename would be a separate ADR.
**Context:** The plugin already embodied graph structure implicitly — the cycle is a
graph, the subagents are nodes, adversarial review is a verifier, dark-launch +
flip-criteria is an audit projection — but nothing named it, and there was no
first-class way to fan breadth work (audits, reviews, research) across a fleet. Claude
Code shipped dynamic workflows (JS orchestration, zero-token coordination), which is
the missing execution-graph runtime. Convergent external work (LangGraph graph
engineering, graph-augmented LLM agents, Agentforce guided determinism) points the
same way.
**Rationale:** Making the graph explicit is high-leverage and low-cost: it adds a
capability (`/graph` + `verifier`) and a shared vocabulary without breaking the cycle
or any consumer. Keeping the name avoids a breaking change across every repo that
enables the plugin. Fan-out lives in code the model wrote, so coordination is free and
each subagent keeps its own context — breadth one session can't hold becomes reachable.
**Consequences:**
- New surface: `/graph` skill, `GRAPH_MODEL.md`, `WORKFLOW_LIBRARY.md`, `verifier`
  agent; `/pitch` template gains `Graph` + `Gated edges` fields.
- Governance is stated on edges: the human gate is a conditional edge, and every
  acting node should project a row into the audit graph. Self-routing is allowed for
  read/analysis graphs, never for consequential actions.
- Versions: agentic-engineering → 0.3.0; marketplace → 0.4.0.
- Out of scope: renaming the plugin; a graph-DB-backed memory (kept additive/light,
  reassessed only when a real multi-hop case pays for it); distributing runnable
  workflows as plugin assets (shipped as copy-ready templates for now).
