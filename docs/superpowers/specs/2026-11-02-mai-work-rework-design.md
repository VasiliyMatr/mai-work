# mai-work rework design

Proposed for review; implementation follows approval.

## Direction and layout

Modernize mai-work using unitrace's newer generic behavior and management.
Keep language, platform, format, and module-specific policies in consumers.

Consolidate first-party packs under `.apm/`: `instructions/` for policies,
`agents/` for roles, `skills/` for workflows, plus hooks/prompts. Maintain one
canonical source, thin generated harness adapters, and a short maintenance
README. Preserve useful concern-level toggles when replacing packs.

Keep APM and Superpowers. Separate reusable reviewer contracts from workflow
integration so future custom flows can reuse them. Backport from unitrace's
current `.apm/` and pre-`e8a9239` roles/workflow; newer refinements take precedence.

## First-party inventory

| Action | Features |
| --- | --- |
| Preserve | Language preferences, English/ASCII artifacts, authorship, optional AI attribution/LingoFix, aligned tables, Conventional Commits. |
| Update | Request validation: simpler alternatives and support costs; respect reaffirmed intent and existing authorization. Contract audits: preserve provenance and user-owned decisions, avoid duplicate reviews. |
| Backport | Implementer/reviewer/fixer separation; evidence-based handoffs; local-fix versus redesign routing; final combined-result review. |
| Backport | Simple implementations, explicit spec/code/test conflicts, focused changes, preserved user work, verified completion claims. |
| Backport | Readable behavioral tests, minimal structural checks, deterministic synchronization; no rerun-until-pass or weakened assertions. Documentation explains intent and guarantees without trivial commentary. |
| Backport/update | Pinned tooling, reproducible install/compile/audit, generated-file ownership, harness coverage; revalidate historical APM workarounds. |
| Add/replace | Two reviewer families; replace tiered terminology promotion with purposeful Serena memories. |

## Review integration

- **Simplicity/readability:** requests, designs/plans, code, and tests. Reject
  unnecessary abstractions, duplicated paths, and obscurity with concrete costs
  and a simpler alternative preserving requirements. Necessary complexity passes.
- **Terminology/wording:** designs, docs, and comments. Check consistent terms,
  essential information, and proportional detail against surrounding material.
  Small features must not dominate concise overviews; preserve useful contracts.

Start with one role per family and scenario references. Suggest simplifications
at brainstorming; review designs before approval, relevant changes during task
review, and the complete result before acceptance. Cover inline and subagent
execution; activate only applicable reviewers.

Findings specify location, evidence, impact, and correction. Verdicts:
`accepted`, `changes-required` (fixer), `redo-required` (designer/implementer),
`blocked` (missing evidence/decision). Suggestions remain nonblocking.
Reviewers are read-only; the coordinator sequences one writer and re-review.
Bound retries, then redesign or expose the unresolved decision. Never silently
accept blocking findings; record user exceptions. Disclose non-independent review.

Use first-party routing and briefs at pinned Superpowers boundaries; use minimal
versioned source overrides only where necessary. Do not edit generated files.
Override upstream completion through parked blockers; retain user contract authority.

## Third parties

Checked 2026-11-02; upgrade candidates, not compatibility-tested:

- **[APM 0.35.0](https://github.com/microsoft/apm/releases/tag/v0.35.0)**
  from 0.27.0: frozen-install, local-verification, packaging, and source-replacement
  improvements. Recheck hash/bootstrap/`CLAUDE.md` workarounds.
- **[Superpowers 7.0.1](https://github.com/obra/superpowers/releases/tag/v7.0.1)**
  from 6.2.0: reuse context-first brainstorming, task/final reviews, bounded
  repair, progress records, and skill testing. Its
  [parked-findings policy](https://github.com/obra/superpowers/blob/v7.0.1/skills/subagent-driven-development/SKILL.md)
  needs the acceptance override above.
- **[Serena 2.1.0](https://github.com/oraios/serena/blob/v2.1.0/CHANGELOG.md):**
  pin the external installation; retain semantic navigation. Evaluate REPL
  separately; note the GPL-3.0-or-later change. Use
  [project memories](https://oraios.github.io/serena/02-usage/045_memories.html)
  for decisions, surprising constraints, and corrected vocabulary: read relevant
  entries at task start, update with source links, replace stale content. Track
  shared knowledge, ignore private/cache state; Markdown remains usable without
  MCP. No glossary promotion or duplicated specifications.
- **[Caveman 4.0.1](https://github.com/JuliusBrussee/caveman/releases/tag/v4.0.1)**
  from 1.9.1: evaluate portable skills/compact handoffs separately from
  proxy/cloud/memory features. Retest Claude-only targeting; preserve readable prose.
- **[RTK](https://github.com/rtk-ai/rtk):** document shared usage and raw-output
  fallback instead of relying on machine-local instructions.
- **[Promptfoo](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/):**
  candidate for cross-harness reviewer evaluations; start with small scenarios
  before adding its runner. No additional orchestration/memory framework.

## Rollout and acceptance

Consolidate/backport, validate upgrades, integrate reviewers, then enable memories.
Verify clean install, frozen repeatability, compile/audit, hooks, and reviewer
routing across Claude Code, Codex, and OpenCode, without leaking maintainer rules.

Exercise rejection/rework for excessive complexity, obscure tests, terminology
drift, and oversized docs; acceptance for justified complexity; repeated failure
and user exceptions. Measure missed defects, false positives, and review cost.
