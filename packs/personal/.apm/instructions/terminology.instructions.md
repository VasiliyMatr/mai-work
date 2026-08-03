---
description: Use precise domain terminology, resolve ambiguous terms explicitly, and record agreed terms in the tiered term store.
---

# Terminology

## Usage

- Use the concrete domain term, not a generic paraphrase: "TU-local linkage" not
  "file-private thing"; "lock contention" not "slowness"; "ODR violation" not
  "duplicate symbol problem".
- When a term is ambiguous in context, state the reading you are using in one
  clause and continue. Stop to ask only when the readings lead to materially
  different work.
- Give a one-line definition on first use of a term the user has not used
  before. Expand only on request.
- When the user asks what a term means, answer with the definition first, then
  why it matters here.

## Term store - three tiers, one owner each

| Tier | Location | Holds | Lifetime |
|---|---|---|---|
| scratch | Claude auto memory, `~/.claude/projects/<project>/memory/` | terms seen this session, not yet confirmed | until confirmed or stale |
| project | Serena memories, `.serena/memories/` (`write_memory` / `read_memory`) | terms agreed for this repo; readable by every harness that loads Serena | life of the repo, tracked in git |
| core | `packs/personal/.apm/instructions/glossary.instructions.md` | stable terms that hold across every project | permanent, loaded every session |

Promotion is one-way: scratch -> project -> core. A term lives in exactly one
tier; when you promote it, delete it from the tier below.

The core tier file does not exist yet - create it on the first term that earns
that tier, with the same frontmatter shape as this file.

## What to record

Record a term when the user corrects your wording, defines a term explicitly, or
reuses a non-obvious term across three or more turns.

Do not record what a reader can look up in the codebase, the language standard,
or a library's own documentation. The store is for *this* project's and *this*
user's conventions.

Keep the core tier under 30 entries - it costs context on every session start.
Past that, demote entries to the project tier.
