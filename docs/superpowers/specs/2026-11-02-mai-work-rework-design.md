# mai-work rework design

Status: proposed for review. Scope: design only; implementation follows approval.

## Direction and layout

Use unitrace's evolved agentic behavior and management as the reference for
modernizing outdated mai-work. Port generic improvements, reconcile overlapping
rules, and keep project-specific policy in consuming repositories. Unitrace's
formats, C++ conventions, compiler/platform choices, and module paths stay out.

Use unitrace's separation of instructions, roles, and workflows, with one
canonical source per policy and thin harness adapters. Consolidate first-party
sources under root `.apm/`: `instructions/` for policies, `agents/` for role
contracts, `skills/` for workflows and their scenario guidance, and `hooks/` and
`prompts/` for integration. A short `.apm/README.md` owns the inventory and
maintenance commands. APM generates native harness files; those remain ignored.
This replaces the three local packs and their repeated packaging instructions.
Keep concerns independently configurable where useful; verify the replacement
for existing pack-disable behavior before migration.

Keep APM and Superpowers as the deployment and workflow foundations. A new
workflow engine or a broad Superpowers fork would add maintenance before the
desired review behavior has been proven. Keep reusable reviewer contracts
separate from the small Superpowers integration so future custom flows can use
them unchanged.

## First-party inventory

| Action | Features |
| --- | --- |
| Preserve | Response language and English/ASCII artifacts; human authorship identity; optional AI attribution; optional LingoFix; aligned Markdown tables; concise Conventional Commits. |
| Update | Request validation: include feature-support and abstraction costs, suggest simpler alternatives, and honor reaffirmed user intent. Keep routine choices autonomous. |
| Update | Contract preflight and prepared-change audits: retain evidence, provenance, and user-owned decisions; narrow triggers and coordinate with other reviewers to avoid duplicate audits. Existing authorization remains valid. |
| Backport | Unitrace's implementer/reviewer/fixer separation; read-only independent review; explicit local-fix versus substantial-redo routing; evidence-based handoffs; review of the final combined result. |
| Backport | Generic engineering discipline: simplest sufficient implementation, no speculative extension points, explicit conflicts between code/spec/tests, focused changes, preserved user work, and verified completion claims. |
| Backport | Newer test guidance: readable observable scenarios, minimal nonduplicative structural checks, deterministic synchronization, no rerun-until-pass, and no weakened assertions to satisfy a review. |
| Backport | Documentation guidance: explain intent, constraints, and guarantees; omit trivial commentary. Use project-specific documentation conventions rather than importing Doxygen or mandatory per-file documentation. |
| Backport/update | Central maintenance guide, pinned dependencies/tool versions, reproducible install/compile/audit commands, generated-file ownership, and explicit harness coverage. Revalidate unitrace's APM workarounds instead of copying stale hashes or paths. |
| Add | Simplicity/readability and terminology/wording reviewers, with scenario guidance and enforceable rework outcomes described below. |
| Replace | Retire the unused scratch/project/core terminology promotion scheme. Keep precise, audience-appropriate terminology and introduce small, purposeful Serena memories. |

Backport provenance: unitrace's current `.apm/instructions/unitrace.instructions.md`
and `.apm/README.md`, plus the canonical roles/workflow preserved immediately
before migration commit `e8a9239`. The historical files establish the role/layout
model; later unitrace refinements take precedence over their older details.
Inherited mai-work content is not itself a new backport.

## Review behavior inside Superpowers

Start with two reviewer families, each with one reusable role and short
scenario references. Split into more skills only when experience shows distinct
triggers or expertise are needed.

- **Simplicity and readability:** review requests, designs/plans, production
  code, and tests. Identify unnecessary layers, speculative configurability,
  duplicated paths, obscure control flow, and test machinery that hides the
  behavior. Each rejection must identify a concrete maintenance or comprehension
  cost and a simpler way to meet the same requirements. Necessary complexity
  and explicit user requirements are not defects.
- **Terminology and wording:** review designs, documentation, and comments in
  their surrounding context. Check consistent domain terms, clear explanations,
  useful guarantees/rationale, and appropriate detail. Compare additions with
  neighboring sections and the whole document: a small feature must not dominate
  a previously concise overview. Move necessary detail to its natural home;
  preserve essential contracts and examples. No arbitrary word quota.

Integrate at existing workflow boundaries:

1. **Request/brainstorming:** cheaply flag simplifications and support costs;
   use a dedicated review for substantial proposals. Advice challenges an
   approach without vetoing the user's objective.
2. **Design and planning:** run applicable reviewers before presenting the
   artifact for approval or execution. Include contract preflight when needed.
3. **Implementation:** add the applicable review lenses to Superpowers' task
   review. Test guidance is activated by test changes; wording review by prose
   changes. Use separate reviewers where independence or scope warrants it,
   rather than spawning every reviewer for every edit.
4. **Final review:** check the complete branch/result for accumulated complexity,
   inconsistent terminology, and disproportionate documentation. Cover inline
   execution as well as subagent-driven development.

Every actionable finding names its location, evidence, impact, and correction.
Verdicts are `accepted`, `changes-required` (focused correction), `redo-required`
(return to designer/implementer), or `blocked` (missing evidence/decision).
Suggestions are explicitly nonblocking. Revisions receive focused verification;
final acceptance covers the complete current artifact. Reviewers do not edit or
spawn further reviewers; the coordinator owns sequencing and one writer at a time.

Bound repair loops. Repeated failure routes to redesign or exposes a concrete
unresolved decision; it never silently converts a blocking finding into a pass.
User-authorized exceptions are recorded with their tradeoff. Where independent
agents are unavailable, perform explicit review passes and disclose that limit.

Ship a first-party routing skill/instruction and reviewer briefs bound to the
pinned Superpowers stages. Avoid editing generated upstream files. If routing
cannot reliably enforce a boundary, use a minimal versioned source override for
that stage and verify it on upgrades. In particular, override upstream's ability
to park blocking findings as completed work; keep contract decisions with the user.

## Third-party choices and underused features

Upstream snapshot checked on 2026-11-02; versions below are upgrade candidates,
not installed or compatibility-tested by this design.

- **[APM 0.35.0](https://github.com/microsoft/apm/releases/tag/v0.35.0):**
  upgrade from the lockfile's 0.27.0 after deployment checks. Relevant changes
  include cold frozen installs, local-content verification, hook-resource
  packaging, and consumer source replacements. Recheck unitrace's frozen-install,
  hash, and generated `CLAUDE.md` workarounds; retire only those proven unnecessary.
- **[Superpowers 7.0.1](https://github.com/obra/superpowers/releases/tag/v7.0.1):**
  evaluate upgrading from 6.2.0. Reuse context-first brainstorming, task/final
  reviews, bounded fix loops, and persistent progress records. Its
  [execution policy](https://github.com/obra/superpowers/blob/v7.0.1/skills/subagent-driven-development/SKILL.md)
  permits rulings and parked findings; the acceptance rules above must take
  precedence. Use upstream skill-testing practices for our additions.
- **[Serena 2.1.0](https://github.com/oraios/serena/blob/v2.1.0/CHANGELOG.md):**
  retain semantic navigation and pin the currently external installation.
  Evaluate the newer REPL separately. Version 2 changes licensing to
  GPL-3.0-or-later; record that change when selecting the dependency.
  Use its existing [Markdown memories](https://oraios.github.io/serena/02-usage/045_memories.html):
  list/read relevant project memories at task start; update durable decisions,
  surprising constraints, and user-corrected project vocabulary when learned.
  Keep source links and replace stale entries. Track deliberately shared memories,
  ignore caches/private state, and read the files directly if MCP is unavailable.
  No automatic global glossary promotion, transcript archive, or duplicate specs.
- **[Caveman 4.0.1](https://github.com/JuliusBrussee/caveman/releases/tag/v4.0.1):**
  the current 1.9.1 pin is substantially behind. Evaluate portable skills and
  compact handoffs separately from the newer proxy/cloud/memory stack. Preserve
  useful compression without degrading user-facing prose. Retest harness support
  before lifting the existing Claude-only restriction; avoid competing memory
  and orchestration systems.
- **[RTK](https://github.com/rtk-ai/rtk):** document the already-used CLI output
  reduction and raw-output escape hatch as shared tooling; do not rely on an
  undistributed machine-local instruction file.
- **[Promptfoo](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/):**
  useful new-to-this-repo candidate for comparing reviewer behavior across
  harnesses. Start with small checked-in scenarios; adopt its runner only when
  repeatable evaluation warrants the dependency. No additional orchestration or
  memory framework is needed for this rework.

## Rollout and acceptance

First consolidate sources and generic unitrace improvements; then validate
dependency upgrades, integrate reviewers, and introduce the memory policy.
Preserve Claude Code, Codex, and OpenCode support with documented capability
differences. Test a clean consumer install, frozen repeatability, compilation,
audit, hooks, and actual reviewer discovery; ensure maintainer-only instructions
do not leak into consumers.

Behavioral scenarios must demonstrate rejection and successful re-review of an
overengineered design, obscure code/tests, terminology drift, and an oversized
feature section. Include passing cases for justified complexity and concise
documentation, plus repeated-failure and explicit-user-exception cases. Judge
false positives, missed defects, review cost, and routing behavior, not merely
whether a reviewer ran. Deliver the implementation in reviewable stages after
this design is approved.
