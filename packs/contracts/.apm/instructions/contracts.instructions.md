---
description: Route contract-sensitive work through focused audits before work begins and after changes are prepared.
---

# Contract audit gate

A contract is behavior, structure, or a constraint that another party may rely
on. Examples include APIs and CLIs, ABIs, schemas and formats, paths and
discovery, errors and recovery, lifecycle and ownership, state and concurrency,
security, versioning, and language, runtime, framework, tool, or platform
semantics.

Use this gate when getting a contract wrong could change the solution,
compatibility, persistent data, interoperability, or a behavioral claim.

## Required audits

- Before preparing code, configuration, tests, documentation, or a behavioral
  claim, delegate to the `contracts-preflight` agent when the work may create
  or change a contract, or materially depends on one.
- After a change or commit message is prepared, delegate to the
  `contracts-review` agent when it may affect or must preserve a contract, or
  makes claims about one.
- Run both audits when both conditions apply. A pre-flight result does not prove
  that prepared changes preserved the contracts.

Only the primary agent invokes the auditors and supplies the request, plan or
change set, relevant versions, and known user decisions. Auditors research and
report; they neither invoke a contract auditor nor decide a missing user-owned
contract. The primary agent asks the user for that decision and surfaces
unresolved external assumptions in the main conversation and final handoff; a
subagent report alone is not disclosure.

Resolve blocking findings before proceeding. For contracts, this overrides the
default ambiguity handling in `request-validation`.

Use proportionate diagnosis and verification for an obviously local defect
that neither changes nor materially depends on a contract. Do not classify a
problem as local only because its symptom or apparent fix is small.
