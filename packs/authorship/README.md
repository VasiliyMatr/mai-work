# mai-authorship

Attribution: who gets credit for a piece of work, human and AI.

Two rules with different lifetimes, kept in separate files on purpose — human
identity is per-user and persisted, AI credit is per-session and ephemeral.

## Contents

| Primitive | File | Effect |
|---|---|---|
| instruction | `authorship` | One human identity everywhere; never substitute a handle; never invent an email |
| instruction | `commit-attribution` | Ask once per session whether commits carry an AI `Co-Authored-By` trailer |
| hook | `authorship-context.sh` | `SessionStart`; injects `AUTHORSHIP: <name> <email>` or a setup nudge |
| prompt | `authorship-setup.prompt.md` | `/authorship-setup` — the one-time human-identity dialog |

## Human identity

Configured once per user in `${XDG_CONFIG_HOME:-~/.config}/mai/authorship`, one
`key=value` per line, no spaces around the `=`:

```
mode=git
```

```
mode=custom
name=Ada Lovelace
email=ada@example.com
```

`mode=git` resolves from `git config user.name` / `user.email` **at session
time**, so a repository-local override is honoured automatically. `mode=custom`
pins a fixed identity. Unknown keys and comment lines are ignored.

The file is machine-local and outside any repository, so a new machine runs the
dialog again. That is deliberate: it is a per-user setting, not a project one.

Reconfigure with `/authorship-setup`.

## AI co-authorship

No config file and no state on disk. The first commit request in a session asks
whether to add the trailer; the answer holds for that session and a new session
asks again.

The trailer never hardcodes a model name — the agent uses its own identity from
the current request's system prompt. That is also the only workable option: the
`model` field exists on `SessionStart` hooks alone, the documentation states it
is not guaranteed to be present, and there is no `$CLAUDE_MODEL` environment
variable, so a hook cannot supply the name reliably.

## Harness coverage

The hook reaches Claude Code and Codex. OpenCode has no hook support, so the
`authorship` instruction tells the agent to resolve the identity itself — read
the config file, then fall back to `git config`. The `commit-attribution` rule
needs no hook and works everywhere.

## Authoring notes

Same two APM constraints as `packs/personal`: instructions carry no `applyTo`
(otherwise the emitted rule becomes path-scoped and does not load at session
start), and hook paths in `hooks.json` resolve literally against the package
root, where `${CLAUDE_PLUGIN_ROOT}` anchors. All sources here live under `.apm/`,
so the payload does too and the reference reads
`${CLAUDE_PLUGIN_ROOT}/.apm/hooks/authorship-context.sh`. A reference that
disagrees with the script's actual location still installs — with a warning and
a dead hook.
