# Phase 13 Agent Workbench Pilot

Phase 13 used Agent Workbench as a supervisor-controlled proposal assistant
before activating implementation child issues under FreshForge issue #94.

## Pilot Shape

Three proposal-only worker tickets were run under ignored local artifacts:

- `tmp/agent_workbench/p13/p13-evidence-intake.ticket.md`
- `tmp/agent_workbench/p13/p13-cli-ergonomics-proposal.ticket.md`
- `tmp/agent_workbench/p13/p13-docs-and-acceptance-proposal.ticket.md`

Workers had no tool, command, file-edit, GitHub, or tracked-file mutation
authority. The supervisor retained all issue, code, documentation, and closeout
authority.

## Findings

The evidence-intake worker correctly identified that broad downstream evidence
for P13 remains thin. The CLI ergonomics worker proposed summary-only output,
but also included unsupported claims about user reports and inconsistent fields;
those claims were rejected by supervisor review.

The accepted bounded slice is to expose existing compact summary records
directly:

- `freshforge run --summary`
- `freshforge matrix run --summary`

This keeps Phase 13 generic and does not redesign summary schemas, add domain
semantics, or change execution behavior.

## Boundary

Raw worker transcripts and provider configuration remain ignored local
artifacts. Only this sanitized supervisor summary is tracked.
