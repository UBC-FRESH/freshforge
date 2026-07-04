# Phase 15 Agent Workbench Pilot

Date: 2026-07-04

Purpose: use Agent Workbench as a proposal assistant before implementing P15
durable run and matrix evidence manifests.

## Pilot Setup

P15.1 ran three proposal-only worker tickets with
`qwen3-coder-next:latest` through Agent Workbench:

- `p15-manifest-fields`
- `p15-compatibility-tests`
- `p15-downstream-consumption`

Worker authority was no-tool and proposal-only. Raw tickets, manifests,
transcripts, summaries, and rendered evidence remain under ignored
`tmp/agent_workbench/p15/` paths. Only this sanitized supervisor summary is
tracked.

The generated evidence summaries validated with Agent Workbench, and a
supervisor decision packet was synthesized from them.

## Worker Outcome Summary

| Ticket | Classification | Supervisor decision |
| --- | --- | --- |
| `p15-manifest-fields` | `extra-prose` | accepted candidate |
| `p15-compatibility-tests` | `structured-output` | accepted candidate |
| `p15-downstream-consumption` | `structured-output` | accepted candidate |

The first output was classified as `extra-prose` because it used subheadings
inside the required sections. The content was still useful after supervisor
review. The downstream-consumption output contained useful framing but also
over-scoped fields and encoding artifacts, so it required heavier filtering.

Claim review totals:

- accepted claims: 10
- rejected claims: 6
- needs-evidence claims: 6

## Accepted Contract Direction

P15 should implement optional evidence manifest writing for:

- `freshforge run WORKFLOW --evidence PATH`
- `freshforge matrix run MATRIX --evidence PATH`

The first manifest contract should be deterministic, generic, and built from
current FreshForge records plus CLI-known metadata.

For single workflow runs, the manifest should include:

- manifest format version;
- FreshForge package version;
- source type and source path;
- work directory;
- run namespace when present;
- workflow id;
- run status;
- compact run summary;
- full run result or enough structured detail to recover node status,
  diagnostics, provider ids, node types, outputs, data, and declared artifacts;
  and
- top-level diagnostics.

For matrix runs, the manifest should include:

- manifest format version;
- FreshForge package version;
- source type and source path;
- work directory;
- matrix id;
- matrix status;
- compact matrix summary;
- per-case case id, namespace, status, summary, diagnostics, and run result
  where available;
- deterministic case ordering; and
- top-level diagnostics.

The manifest should avoid fields that are not supported by current records or
that imply future execution-system behavior.

## Rejected Or Deferred Worker Claims

The supervisor rejected these P15 requirements:

- required worker ids;
- required step stacks;
- required artifact digests;
- required idempotency keys;
- required parent run ids;
- live polling fields;
- `RUNNING` or `CANCELLED` statuses;
- a mandatory standalone JSON schema file; and
- provider-specific or domain-specific evidence fields.

These may be revisited later, but they exceed the first durable-manifest
contract.

The supervisor marked these claims as needing implementation review:

- whether matrix case inputs should be serialized as full input objects or a
  smaller case-parameter record;
- whether execution start timestamps are deterministic enough for default test
  expectations;
- whether duration fields exist and are stable enough to include;
- how invalid evidence paths should fail in Typer CLI commands; and
- whether read-only directory tests are portable enough for the Windows and CI
  test matrix.

## Test Plan Implications

P15 should test:

- evidence output is optional;
- `--json`, `--summary`, and human output remain compatible;
- evidence JSON is deterministic enough for regression tests;
- matrix case ordering is deterministic;
- workdir and namespace path handling are preserved;
- evidence paths are resolved predictably; and
- public examples can write evidence manifests in direct smoke tests.

P15 should not assume that human output must mention the evidence path unless
the implementation deliberately chooses and tests that behavior.

## Delegation Accounting

The delegation was useful but not free.

Observed benefits:

- The worker pack quickly surfaced the important split between current-record
  fields and future provider or execution-system fields.
- The compatibility ticket produced a useful regression-test checklist.
- The downstream-consumption ticket helped frame consumer needs, even though
  many proposed fields were rejected.

Observed costs:

- Supervisor effort was needed to replace generic scaffold tickets with
  context-rich tickets.
- Supervisor review was needed to reject over-scoped fields and unsupported
  assumptions.
- One output violated the strict response-shape contract by using subheadings.
- One output included encoding artifacts and over-specific schema claims.

Net judgment:

P15.1 was positive-value as a proposal-assist delegation. It did not remove the
need for supervisor code inspection or implementation design, but it narrowed
the manifest contract and sharpened the test plan enough to justify the setup
and review cost.

## Implementation Decision

Proceed with P15 implementation using supervisor-owned tracked-file mutation.
Workers should remain proposal-only for this phase.

The initial implementation should prefer simple Python helpers and dataclasses
over a separate schema system. P16 can add provider evidence conventions after
the base manifest contract exists. P17 can add export helpers after manifests
are persisted.
