# mai

My AI configuration: skills, instructions, MCP servers, and tooling for agentic
coding across Claude Code, Codex, and OpenCode.

Author: Vasilii Matrenin <vasiliymatrenin@gmail.com> — GitHub
[@VasiliyMatr](https://github.com/VasiliyMatr)

Everything is declared once in [apm.yml](apm.yml) and compiled to each harness
by [APM](https://microsoft.github.io/apm).

## Integration

Add [mai-work](https://github.com/VasiliyMatr/mai-work) as an APM dependency
from any project:

```yaml
dependencies:
  apm:
    - VasiliyMatr/mai-work
```

Pin it like any APM dependency — by tag, branch, or commit:

```yaml
dependencies:
  apm:
    - VasiliyMatr/mai-work#main
```

Then `apm install` deploys the manifests and `apm compile` regenerates
`AGENTS.md` / `CLAUDE.md` for the project's harnesses.

## Layout

| Path            | Contents                                               |
| ---             | ---                                                    |
| `apm.yml`       | Root manifest: targets, dependencies, local packs, MCP |
| `apm.lock.yaml` | Resolved versions and hashes, committed                |
| `packs/`        | First-party packs, one per concern group               |

Harness directories (`.claude/`, `.codex/`, `.opencode/`, `.agents/`) and
`AGENTS.md` / `CLAUDE.md` are build output, gitignored, and cannot be relocated.

## Packs

| Pack                                 | Contents |
| ---                                  | --- |
| [packs/personal](packs/personal)     | Response language, terminology discipline, wording feedback, request validation, aligned Markdown tables |
| [packs/authorship](packs/authorship) | Attribution: one human identity for author/copyright/credit fields; per-session AI `Co-Authored-By` choice |
| [packs/contracts](packs/contracts)   | Contract-sensitive pre-flight and prepared-change audits with provenance and user-owned decisions |

Packs are local path dependencies, edited in place with no tag cycle. Disable
one by commenting out its line in `apm.yml` and re-running `apm install`. Any
pack can graduate to its own repository unchanged.

## Dependencies

| Package                                                           | Purpose |
| ---                                                               | --- |
| [obra/superpowers](https://github.com/obra/superpowers)           | Agentic development methodology: brainstorming, plans, subagent-driven development, systematic debugging, TDD |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | Output-token compression, Claude Code only (other harnesses reject its agent allowlists) |
| [oraios/serena](https://github.com/oraios/serena)                 | Semantic code intelligence over LSP (MCP) |

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

## License

MIT — see [LICENSE](LICENSE).
