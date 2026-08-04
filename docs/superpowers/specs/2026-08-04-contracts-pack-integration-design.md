# Contracts Pack Integration Design

## Context

`packs/contracts` contains one global contract-audit instruction and two
read-only audit agents. It does not yet contain package metadata, so APM cannot
resolve or deploy it as a local dependency. The root project already uses
first-party local packs for personal preferences and authorship.

## Goal

Integrate `packs/contracts` as a self-contained first-party APM package and
deploy its instruction and agents consistently to Claude Code, Codex, and
OpenCode.

Success means:

- the pack has valid metadata and documentation;
- the root manifest declares it as a local dependency;
- APM records its source, deployed files, hashes, and ownership in the
  lockfile;
- all three harnesses receive both agents;
- the contract audit gate appears once in compiled global instructions;
- APM `0.27.0` frozen installation verifies lockfile presence, the presence of
  lockfile entries for manifest-declared non-local direct dependencies, and MCP
  configuration state, but skips local dependency manifest and source
  validation;
- reproducing the local-pack deployment uses the same Git checkout, including
  `packs/contracts`, plus `apm.lock.yaml`;
- an APM audit verifies current deployed-output integrity.

## Non-goals

- Change contract-audit policy or agent behavior.
- Add hooks, commands, skills, or runtime dependencies.
- Publish the pack to a registry or separate repository.
- Upgrade APM or existing remote dependencies.
- Modify `.serena/` or other unrelated user-owned files.

## Package Boundary

Add `packs/contracts/apm.yml` with:

- name `mai-contracts`;
- version `0.1.0`;
- a description covering contract-sensitive pre-flight and prepared-change
  audits;
- author `Vasilii Matrenin <vasiliymatrenin@gmail.com>`;
- license `MIT`.

The existing `.apm/instructions/contracts.instructions.md` remains the global,
conditionally triggered gate. The existing `.apm/agents/` files remain
read-only auditors invoked by the primary agent. No primitive content changes
are required for integration.

Add `packs/contracts/README.md` documenting pack purpose, primitive inventory,
trigger behavior, audit flow, harness coverage, and authoring constraints.

## Root Integration and Data Flow

Add `./packs/contracts` to the first-party dependency group in root `apm.yml`,
after `./packs/authorship`.

Deployment flow:

1. Root APM resolves `./packs/contracts` as a local package.
2. APM scans and records package contents in `apm.lock.yaml`.
3. APM deploys both agents into each configured harness's native agent
   location.
4. APM deploys the instruction to Claude's native rules and compiles it into
   global `AGENTS.md` guidance for Codex and OpenCode.
5. APM compilation refreshes harness entrypoints without hand-copying generated
   files.

Root `README.md` gains a contracts row in the pack catalog. It describes the
conditional gate and its pre-flight and prepared-change auditors.

## Tooling and Failure Handling

Use APM `0.27.0`, matching the version recorded in the existing lockfile. Run
it from a temporary installation so integration does not modify the user's
global toolchain.

Do not use `--force`. Inspect every install diagnostic: APM may skip one file
with an unmanaged collision without aborting. Stop the workflow manually on
any collision or on manifest validation, security scan, ownership, or
deployment errors. Do not weaken the pack or bypass checks to make installation
pass.

The install must preserve locked versions of existing remote dependencies.
Any unrelated lockfile or generated-output churn is a failure to investigate,
not part of this change.

## Verification

Run:

1. `apm install` to resolve the new local dependency and deploy primitives.
2. `apm compile` to refresh compiled harness instructions.
3. Targeted inspection of `apm.lock.yaml` for the `mai-contracts` local source,
   deployed paths, hashes, and ownership.
4. Targeted inspection of Claude, Codex, and OpenCode outputs for both agents
   and one global gate.
5. `apm install --frozen` to verify lockfile presence, the presence of lockfile
   entries for manifest-declared non-local direct dependencies, and MCP
   configuration state. APM `0.27.0` skips local dependencies during this check,
   so it does not validate manifest or source drift for `./packs/contracts`.
   Reproducing the local-pack deployment requires the same Git checkout,
   including `packs/contracts`, plus `apm.lock.yaml`.
6. `apm audit --ci` to check current deployed-output integrity.
7. `git diff --check` and a scoped diff review to catch malformed or unrelated
   changes.

Verification must include untracked pack source files while excluding
unrelated `.serena/` content from staging and commits.

## Commit Scope

Implementation commit includes pack source, root manifest and documentation,
lockfile, and tracked generated outputs changed by APM. Design documentation
remains a separate preceding commit.
