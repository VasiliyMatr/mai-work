# mai-personal

Personal working preferences, deployed to every harness through APM.

Consumed as a local path dependency from the repo root `apm.yml`. The pack is
self-contained: to reuse it elsewhere, copy this directory or publish it as its
own APM package — nothing here depends on the parent repo.

## Contents

| Primitive   | File                      | Effect                                                                    |
| ---         | ---                       | ---                                                                       |
| instruction | `languages`               | Reply language follows the user; artifacts always English                 |
| instruction | `terminology`             | Precise terms, ambiguity resolved out loud, three-tier term store         |
| instruction | `lingofix`                | Optional footer reporting wording errors in the user's messages           |
| instruction | `request-validation`      | Pre-flight checks for contradictions, reinvention, wrong layer            |
| hook        | `lingofix-reminder.sh`    | `UserPromptSubmit`; restates LingoFix on/off each turn                    |
| skill       | `aligned-markdown-tables` | Keeps pipe-table columns aligned in raw Markdown; ships `align-tables.py` |

Instructions deploy natively to `.claude/rules/` and reach Codex and OpenCode
through `apm compile` (`AGENTS.md`). The hook reaches Claude Code and Codex;
OpenCode has no hook support, so it falls back to the instruction default.

## Authoring notes

Two APM behaviours these files depend on:

- **No `applyTo` in instruction frontmatter.** APM maps `applyTo` to the `paths`
  field of the emitted `.claude/rules/*.md`, and Claude Code treats a rule with
  `paths` as *path-scoped* — it loads only when a matching file is read, not at
  session start. Omitting `applyTo` emits a bare rule that loads
  unconditionally, and compiles into `## Global Instructions` in `AGENTS.md`.
  These preferences must apply from the first turn, so none of them set it.
- **`${CLAUDE_PLUGIN_ROOT}` anchors at the package root, not at `.apm/`.**
  APM resolves hook paths literally, relative to that root — there is no
  `.apm/` stripping and no fallback search. Since every source file in these
  packs lives under `.apm/`, the hook payload does too, and the reference spells
  out `${CLAUDE_PLUGIN_ROOT}/.apm/hooks/<script>`. (Superpowers and caveman put
  their payloads at the package root instead; both layouts work, the reference
  just has to match.)

  A mismatch between the script's location and the reference is the failure to
  watch for: APM warns `Hook script not found`, then merges the entry anyway
  with the variable unsubstituted and exits 0. Claude Code defines
  `CLAUDE_PLUGIN_ROOT` only for plugin hooks, so in a `settings.json` hook the
  leftover variable expands to nothing and the hook silently no-ops.

`.claude-plugin/plugin.json` marks the pack as a plugin bundle so the hook
payload is copied to `.claude/hooks/personal/` and `.codex/hooks/personal/`.

## Toggles

```bash
touch ~/.claude/.lingofix-off   # disable the wording footer
rm ~/.claude/.lingofix-off      # re-enable it
```

Disable the whole pack by commenting out its line in the root `apm.yml`, then
re-running `apm install`.
