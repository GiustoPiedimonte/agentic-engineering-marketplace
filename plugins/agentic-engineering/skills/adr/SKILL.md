---
name: adr
description: >
  This skill should be used to record an architecture decision. Trigger when the
  user says "record this decision", "write an ADR", "we decided to...", "log why
  we chose X", or when a consequential, hard-to-reverse technical choice is made.
  Appends a dated, immutable decision block to the decision log.
metadata:
  version: "0.2.0"
---

# /adr — record an architecture decision

Decisions are the answer to "why did we do X?". They live in a single
append-only log so the reasoning survives long after the code changes.

`$ARGUMENTS` is the decision to record (or "review" to summarize recent ones).

## Process

1. **Locate the log:** `docs/DECISIONS.md` (create it if missing, with a one-line
   header stating the contract — see below).
2. **Find the next number:** read existing `## ADR-NNN` headers and increment.
   If multiple sessions may run concurrently, confirm the number isn't taken
   right before writing (number collisions are a known failure mode).
3. **Append one block** using `references/ADR_FORMAT.md`. Never edit or delete an
   existing ADR — a changed decision is a NEW ADR that supersedes the old one
   (add `**Supersedes:** ADR-XXX` and note it on the old block only as a pointer).
4. **Keep it tight:** one decision per block, dated, with rationale and
   consequences. This is a retrospective record of *why*, not a plan or a todo.
5. **Link it:** if the decision came from a pitch, cross-link the pitch and ADR.

The log's header contract (write it once at the top of the file):

> Append-only. One decision per block, dated, never edited. A revised decision is
> a new ADR that supersedes the old one. This is the authoritative record of *why*
> we decided things — not a plan, not a backlog.
