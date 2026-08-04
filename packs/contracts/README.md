# mai-contracts

Contract-sensitive work gates for pre-flight decisions and prepared changes,
deployed to every harness through APM.

Consumed as a local path dependency from the root `apm.yml`. The pack is
self-contained: copy this directory or publish it as its own APM package
without depending on parent-repository files.

## Contents

| Primitive | File | Effect |
|---|---|---|
| instruction | `contracts` | Routes contract-sensitive work through required pre-flight and prepared-change audits |
| agent | `contracts-preflight` | Establishes contract provenance, unknowns, assumptions, and required user decisions before work begins |
| agent | `contracts-review` | Checks prepared code, configuration, tests, documentation, and commit claims against relevant contracts |

## Audit flow

1. Primary agent decides whether proposed work can create, change, or materially
   depend on a contract.
2. `contracts-preflight` audits relevant sources before preparation begins.
3. Primary agent resolves blocking findings and asks for user-owned decisions.
4. Work proceeds through its normal design and implementation workflow.
5. `contracts-review` audits contract-sensitive prepared changes and claims.
6. Primary agent resolves required changes and surfaces residual assumptions.

The auditors are read-only. They research and report; only the primary agent
invokes them or asks the user to choose project-owned behavior.

## Scope

Contracts include APIs, CLIs, ABIs, schemas, formats, paths, errors, lifecycle,
ownership, state, concurrency, security, compatibility, versioning, and
language, runtime, framework, tool, or platform semantics. Obviously local
defects that neither change nor materially depend on a contract receive
proportionate diagnosis and verification without both audits.

## Harness coverage

APM deploys both agents natively to Claude Code, Codex, and OpenCode. The
instruction loads as a Claude rule and reaches Codex and OpenCode through the
compiled root `AGENTS.md`.

## Authoring notes

- Keep instruction frontmatter free of `applyTo`; this gate must load globally
  and decide applicability from task semantics.
- Keep auditors read-only and non-recursive: neither auditor invokes another
  contract auditor.
- Keep user-owned decisions with the primary agent and user; successful code,
  examples, and ordinary tests do not authorize a new contract.
- Disable the whole pack by commenting out `./packs/contracts` in root
  `apm.yml`, then re-run `apm install`.
