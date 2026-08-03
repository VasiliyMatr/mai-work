# mai

My AI configuration: skills, instructions, MCP servers, and tooling for agentic
coding across Claude Code, Codex, and OpenCode.

Author: Vasilii Matrenin &lt;vasiliymatrenin@gmail.com&gt; — GitHub
[@VasiliyMatr](https://github.com/VasiliyMatr)

Everything is declared once in [`apm.yml`](apm.yml) and compiled to each harness
by [APM](https://microsoft.github.io/apm). `apm.yml` and `apm.lock.yaml` are the
source of truth; every harness directory is build output.

## Layout

| Path | Kind | Contents |
|---|---|---|
| `apm.yml` | source | Root manifest: targets, dependencies, local packs |
| `apm.lock.yaml` | source | Resolved versions and hashes. Generated, but committed |
| `packs/` | source | First-party packs, one per concern group |
| `LICENSE` | source | MIT |
| `apm_modules/` | build | Cloned dependencies |
| `.claude/` | build | Rules, skills, agents, commands, hooks, `settings.json` |
| `.codex/` | build | Agents, hooks, `config.toml` |
| `.opencode/` | build | Agents, commands |
| `.agents/` | build | Cross-tool skills (Codex reads these) |
| `.mcp.json`, `opencode.json` | build | MCP server config, per-harness format |
| `AGENTS.md` | build | Compiled instructions for Codex and OpenCode |
| `CLAUDE.md` | build | Dependency imports (Claude loads `.claude/rules/` natively) |

All build output is gitignored. The harness directories cannot be relocated —
each harness discovers its own directory by name while walking up from the
working directory.

## Packs

| Pack | Contents |
|---|---|
| [`packs/personal`](packs/personal) | Response language, terminology discipline, wording feedback, request validation |
| [`packs/authorship`](packs/authorship) | Attribution: one human identity for `author`, copyright, and credit fields, configured once per user via `/authorship-setup`; AI `Co-Authored-By` trailer on commits, decided once per session |

Packs are local path dependencies, edited in place with no tag cycle. Disable one
by commenting out its line in `apm.yml` and re-running `apm install`. Any pack can
graduate to its own repository unchanged.

## Dependencies

| Package | Purpose |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Agentic development methodology: brainstorming, plans, subagent-driven development, systematic debugging, TDD |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | Output-token compression; also compresses MCP tool descriptions |
| [oraios/serena](https://github.com/oraios/serena) | Semantic code intelligence over LSP (MCP), 40+ languages including C/C++ via clangd |

Serena needs the `serena` binary on `PATH`:

```bash
uv tool install -p 3.13 serena-agent && serena init
```

## Build

```bash
apm install    # resolve dependencies, deploy primitives to every harness
apm compile    # regenerate AGENTS.md / CLAUDE.md
```

A fresh clone needs both before any harness picks up the configuration.

## Toggles

```bash
touch ~/.claude/.lingofix-off   # disable the wording-correction footer
rm ~/.claude/.lingofix-off      # re-enable it
```

Per-user settings live outside the repository:

| File | Set by | Holds |
|---|---|---|
| `~/.config/mai/authorship` | `/authorship-setup` | `mode=git`, or `mode=custom` with a pinned name and email |
| `~/.claude/.lingofix-off` | `touch` / `rm` | Presence disables the wording footer |

## License

MIT — see [LICENSE](LICENSE).
