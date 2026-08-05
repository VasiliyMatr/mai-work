# Caveman Target Isolation Design

## Context

Before this change, `mai-work` deployed `JuliusBrussee/caveman#v1.9.1`
through APM `0.27.0` to Claude Code, Codex, and OpenCode. Caveman's Cavecrew
agents declare Claude-style `tools` allowlists. APM preserves those allowlists
for Claude, emits them unchanged for OpenCode--which rejects them at load
time--and drops them when transforming agents to Codex TOML.

Codex custom-agent settings inherit from the parent session when omitted.
The generated Cavecrew TOML therefore inherits the parent's sandbox and MCP
surface instead of enforcing the documented role boundaries. This broadens
investigator and reviewer beyond read-only access, gives builder shell access
despite its documentation, and may expose Serena to every Cavecrew agent.

APM `0.27.0` supports target restrictions on dependencies, including virtual
dependencies rooted at package subdirectories. It does not support excluding
one primitive type from a package, consuming native Codex agent TOML from an
APM package, or preserving Caveman's tool restrictions in its Codex agent
transformer. It also materializes full and virtual dependencies from one
repository into the same package directory, so they cannot be clean-installed
together for different targets.

## Goal

Deploy Caveman fail-closed across the configured clients:

- preserve the complete pinned Caveman package on Claude Code;
- deploy no Caveman primitives to Codex or OpenCode;
- remove APM warnings caused by weakened or invalid Cavecrew agent output;
- keep Serena's root MCP configuration unchanged while preventing Caveman
  subagents from inheriting it outside Claude;
- make the target policy reproducible from clean source with APM `0.27.0`.

## User Decisions

The user selected full Caveman for Claude Code only. Claude keeps its current
Cavecrew agents, hooks, commands, and skills. Codex and OpenCode intentionally
receive no Caveman primitives.

The initial decision was to keep portable Caveman skills on Codex and
OpenCode. Clean-install testing showed that APM maps the full package and
virtual skill paths to the same `apm_modules/JuliusBrussee/caveman`
destination, causing a materialization collision. The user selected the
fail-closed fallback: remove Caveman entirely from Codex and OpenCode rather
than add a post-install patch or maintain a fork.

## Dependency Composition

Replace the scalar Caveman dependency in root `apm.yml` with one object
dependency pinned to `v1.9.1` and restricted to `claude` through APM's
supported `git`, `ref`, and `targets` fields. Do not fork or vendor Caveman,
edit `apm_modules/`, patch generated files after installation, or use local
primitive-name collisions as overrides.

Regenerate `apm.lock.yaml` through APM. APM must reconcile existing package
ownership and remove stale Caveman outputs from Codex and OpenCode during
installation.

## Generated Target Contract

| Target | Caveman skills | Cavecrew agents | Hooks and commands | Serena interaction |
| --- | --- | --- | --- | --- |
| Claude Code | Full upstream set | Full upstream set | Full upstream set | Existing Claude tool allowlists remain authoritative |
| Codex | None | None | None | No Caveman custom agent exists to inherit parent MCP access |
| OpenCode | None | None | None | No Caveman custom agent exists; no invalid upstream tool list is deployed |

Claude's upstream Cavecrew permissions are preserved, not reinterpreted or
claimed as portable. This change does not attempt to strengthen Claude's
upstream package or alter Serena's project-wide configuration.

## Documentation

Update root `README.md` with:

- the target matrix and fail-closed rationale;
- the absence of all Caveman primitives on Codex and OpenCode;
- the APM materialization collision that prevents clean full-package plus
  virtual-skill composition from the same repository;
- the remaining APM/Caveman limitation: no portable custom-agent permission
  contract and no APM `0.27.0` primitive-level target exclusion.

Generated `.claude/`, `.codex/`, `.opencode/`, `.agents/`, and `apm_modules/`
content remains build output, not maintained source.

## Verification

Use a disposable clean checkout populated from tracked and intended source
files, then use pinned APM `0.27.0` to:

1. run a normal `apm install` so dependencies are materialized;
2. run `apm install --frozen` against the resulting lock state;
3. run `apm compile`;
4. run `apm audit --ci`;
5. inspect clean generated output rather than relying on the developer's
   existing generated tree.

Manual clean-output inspection must prove:

- installation emits no Cavecrew `tools`-dropped or OpenCode-invalid-agent
  warning;
- Claude receives all three Cavecrew agents with upstream `tools` allowlists;
- Codex and OpenCode receive no `cavecrew-*` agent files;
- Codex and OpenCode receive no Caveman skills;
- Codex and OpenCode receive no Caveman hooks or commands;
- no generated Codex Cavecrew TOML can inherit Serena or parent sandbox access;
- generated ownership reconciles without unmanaged collisions.

Also run `git diff --check` and review the scoped source and lockfile diff.
Do not touch unrelated `.serena/` state.

## Alternatives Rejected

- **Upgrade Caveman only:** current upstream agents still use Claude-style
  `tools` lists, so a version bump does not restore Codex least privilege.
- **Remove `tools`:** silences metadata without enforcing the documented roles.
- **Patch generated Codex TOML:** generated output is not source and the patch
  would not survive clean installation or update.
- **Deploy native Codex replacements through APM:** APM `0.27.0` cannot consume
  native Codex agent TOML, and Codex runtime overrides can still affect child
  session settings.
- **Keep upstream OpenCode agents:** OpenCode rejects the list-shaped `tools`
  metadata; instructions alone would not enforce least privilege.
- **Compose portable skills through virtual paths:** APM materializes the full
  package and virtual paths from the same repository into one destination, so
  a clean install fails with a non-empty destination collision.
- **Fork Caveman:** can preserve more hooks, but creates unnecessary ownership
  and upstream-sync cost.
- **Remove Caveman everywhere:** maximizes uniformity but regresses explicitly
  retained Claude behavior.

## Remaining Upstream Limitations

APM needs target-specific agent primitives or a lossless Codex-native agent
source path to express role-level permissions. Caveman needs portable metadata
or maintained target-native definitions if Cavecrew should run safely outside
Claude. Until either changes, absence is the fail-closed Codex and OpenCode
policy.

## Commit Scope

Design documentation remains a separate commit. Implementation includes root
manifest and README changes plus regenerated lock state. Verification is run
from disposable generated output and is not committed as a repository script.
Generated ignored directories and unrelated user state are not committed.
