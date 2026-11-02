# mai-work rework design

Proposed for review; implementation follows approval.

## Organization

Use unitrace's newer generic behavior and management to modernize mai-work;
leave language-specific engineering and product policy in consumers. Consolidate
packs under `.apm/{instructions,skills,agents}`, with shared references and thin
harness adapters. Keep generated files ignored and useful feature toggles.

Instructions provide only essential preferences and routing. Skills contain
on-demand procedures; agents perform scoped work with explicit inputs, outputs,
and permissions. One canonical contract per feature; no repeated policy in
instructions, prompts, and adapters. Retain APM and Superpowers, keeping role
contracts reusable by future custom workflows.

## First-party features

| Feature                       | Type        | Change and responsibility |
| -------                       | ----        | ------------------------- |
| Language preferences          | instruction | Match the user's language; any language is welcome, with no language-specific examples. Keep English/ASCII artifact rules. |
| Workflow routing              | instruction | Load only applicable skills and agent variants; preserve user authorization and overrides. |
| Authorship                    | skill       | Resolve the configured human identity without inventing attribution. |
| Commit preparation            | skill       | Follow project instructions and established commit style. Ask for AI attribution once per user and persist the choice across sessions. Every commit handoff explicitly mentions whether `Co-Authored-By` was included and shows it when included. |
| LingoFix                      | skill       | Optional, brief language feedback under its existing toggle. |
| Aligned tables                | skill       | Align source columns; separator dash runs match heading width, minimum three, with alignment padding outside the run. Retain the long-final-column guard. |
| Toolchain selection           | skill       | Use project-required tools/versions; otherwise ask the user. Remember supplied choices and versions; recheck when project requirements change. |
| Context memory                | skill       | Read/update relevant Serena memories: decisions, toolchain choices, constraints, corrected terms, and source links. Replace stale entries; retire tiered glossary promotion. |
| Configuration maintenance     | skill       | Install/compile/audit, generated ownership, harness coverage, feature toggles, and upgrades using the selected toolchain. |
| Request assessment            | agent       | Challenge ambiguity, unsupported assumptions, unnecessary scope, and feature-support costs; suggest simpler options without vetoing reaffirmed intent. |
| Implementation                | agent       | Design/code variants own substantial work and redesign; preserve user work, expose spec conflicts, and report evidence. |
| Correction                    | agent       | Make focused fixes, verify findings, and return substantial redesign to implementation. |
| Contract review               | agent       | Preflight and prepared-result variants establish provenance, check guarantees, and expose missing user-owned decisions. |
| Simplicity/readability review | agent       | Brainstorm/design/code variants assess abstraction costs, clarity, and test readability; reject with a simpler requirement-preserving alternative. |
| Terminology/wording review    | agent       | Brainstorm/design/code variants check terms, essential information, comments, and document-wide proportionality. Small features must not dominate concise docs. |

Generic unitrace guidance becomes scenario references used by these roles:
focused changes, observable behavioral tests, minimal structural checks,
deterministic synchronization, meaningful documentation, and verified claims.
No weakened tests or rerun-until-pass. Backport from current `.apm/` and historical
pre-`e8a9239` role contracts, applying newer unitrace refinements first.

## Unified roles in Superpowers

All agents share a brief/handoff format: request, applicable constraints, exact
artifact/scope, evidence, findings, and next action. Scenario variants specialize
one role contract rather than duplicating agents. Superpowers remains the
coordinator; compose its existing implementer/review stages with these roles,
without creating a second orchestration loop or duplicate reviewer seats.

```text
brainstorming
  -> request assessment + applicable brainstorm reviewers
  -> alternatives and costs -> user direction

brainstorming / writing-plans
  -> contract[preflight, when needed] -> implementation[design]
  -> simplicity[design] + wording[design] -> user approval -> execution

subagent-driven-development / executing-plans
  -> toolchain + relevant memories -> contract[preflight, when needed]
  -> implementation[code] -> existing task review + applicable code reviewers
  -> correction or redesign -> re-review
  -> whole-result review -> verification-before-completion
  -> finishing-a-development-branch -> commit preparation when committing
```

Review lenses include tests and prose only when relevant. Reviewers are read-only;
the coordinator sequences one writer. Without subagents, use separate passes
and disclose the lack of independence.

```text
accepted         -> next stage
changes-required -> correction -> re-review
redo-required    -> implementation[design/code] -> re-review
blocked          -> missing evidence/user decision -> resume
```

Findings require location, evidence, impact, and correction; suggestions are
nonblocking. Bound repair loops, then redesign or surface the unresolved decision.
Never silently pass blockers; record user exceptions. Integrate through routing
and briefs; use minimal versioned source overrides only where required, including
Superpowers' parked-blocker completion policy. Never edit generated upstream files.

## Third parties and validation

Candidates checked 2026-11-02, not tested or imposed toolchain versions:

- [APM 0.35.0](https://github.com/microsoft/apm/releases/tag/v0.35.0): evaluate
  frozen-install/verification/packaging fixes and retire proven-obsolete workarounds.
- [Superpowers 7.0.1](https://github.com/obra/superpowers/releases/tag/v7.0.1):
  reuse brainstorming, task/final reviews, repair limits, progress records, and
  skill testing; override [parked blockers](https://github.com/obra/superpowers/blob/v7.0.1/skills/subagent-driven-development/SKILL.md).
- [Serena 2.1.0](https://github.com/oraios/serena/blob/v2.1.0/CHANGELOG.md):
  retain navigation; use [Markdown memories](https://oraios.github.io/serena/02-usage/045_memories.html)
  without duplicate specs or private-state commits. Evaluate REPL separately;
  account for the GPL-3.0-or-later change.
- [Caveman 4.0.1](https://github.com/JuliusBrussee/caveman/releases/tag/v4.0.1):
  evaluate portable skills/handoffs, retest harness targeting, and adapt commit
  behavior to project conventions. Avoid competing orchestration/memory systems.
- [RTK](https://github.com/rtk-ai/rtk): document shared usage and raw-output fallback.
- [Promptfoo](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/):
  optional runner after small reviewer scenarios demonstrate evaluation needs.

Consolidate/backport, validate selected upgrades, integrate roles, then memories.
Check clean install, repeatability, compile/audit, hooks, and routing across
Claude Code, Codex, and OpenCode. Exercise rejection/rework, justified-complexity
acceptance, terminology drift, oversized docs, user exceptions, project commit
styles, remembered toolchains, and table formatting. Measure missed defects,
false positives, and review cost. Verify language-neutral guidance and attribution
consent persistence, explicit trailer reporting, and user preference changes.
