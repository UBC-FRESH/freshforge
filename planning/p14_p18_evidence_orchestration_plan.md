# P14-P18 Evidence-Orchestration Plan

Date: 2026-07-04

Purpose: activate the next FreshForge roadmap tranche after `v0.1.0a5` and Phase 13. The tranche
moves FreshForge from a generic alpha workflow runner toward an auditable workflow evidence substrate
before adding heavier execution features.

## Evidence Sources

P14 uses sanitized planning-level evidence only. Raw worker transcripts, private downstream project
artifacts, endpoint details, credentials, and machine-specific paths remain ignored.

| Source | Evidence available for P14 | Planning implication |
| --- | --- | --- |
| Modelwright matrix generated-model evidence aggregation | Downstream packages need compact evidence that can survive matrix runs and generated-model validation workflows. | FreshForge should persist run and matrix evidence instead of making downstream tools scrape CLI JSON. |
| FABLE Pyculator benchmark matrix evidence cookbook | Repeated benchmark/scenario runs need comparable case summaries and portable evidence packaging. | Matrix evidence should be exportable in table-friendly shapes after it is persisted. |
| FEMIC FreshForge compatibility and matrix/preflight workflow work | FEMIC needs workflow/preflight evidence that can be audited without adding forest-domain semantics to FreshForge core. | FreshForge should own generic evidence records; FEMIC should own domain interpretation. |
| Agent Workbench P13 pilot and real-project deployment notes | Proposal workers can identify affordances, but unsupported claims need supervisor filtering and durable evidence. | Agent Workbench should consume FreshForge evidence; FreshForge should not absorb supervision economics. |

## Ownership Classification

| Friction or need | Owner | Rationale |
| --- | --- | --- |
| Durable run and matrix evidence records | FreshForge core | This is generic workflow infrastructure and avoids repeated downstream parsing of CLI output. |
| Provider-reported validation/evidence conventions | FreshForge core plus provider packages | FreshForge can define optional generic fields; providers own meaning and production. |
| Matrix case summaries for notebooks, CI, and supervisor packets | FreshForge core | Case status, diagnostics, artifacts, and provider IDs are generic enough to export. |
| Modelwright generated-model validation meaning | Provider/domain package | FreshForge should not interpret generated-model correctness. |
| FABLE scenario or benchmark semantics | Provider/domain package | Scenario meaning belongs in FABLE Pyculator or companion providers. |
| FEMIC preflight or forestry semantics | Provider/domain package | Domain checks remain outside FreshForge core. |
| Worker model trust, delegation economics, and claim review | Agent Workbench/supervision | FreshForge evidence can be an input, but delegation policy belongs in Agent Workbench. |
| Caching, checkpoints, retries, remotes, parallel execution, and scheduling | Deferred execution-system concern | These need auditable run evidence before FreshForge can safely add execution complexity. |

## Compatibility Map

Current FreshForge surfaces are sufficient for basic local automation:

- `freshforge validate`, `inspect`, and `plan` provide structural and provider-aware diagnostics.
- `freshforge run --json` preserves full single-run results.
- `freshforge run --summary` exposes compact single-run summaries.
- `freshforge matrix run --json` preserves full matrix-run results.
- `freshforge matrix run --summary` exposes compact matrix summaries.

The gap is durability and downstream comparison ergonomics:

- CLI JSON can be redirected, but FreshForge does not own a declared evidence-manifest contract.
- Matrix summaries are compact, but downstream tools still need to preserve source metadata,
  provider metadata, diagnostics, declared artifacts, and per-case status together.
- Provider outputs can include arbitrary provider data, but FreshForge has no optional generic
  evidence convention for validation status, evidence labels, or artifact roles.
- Matrix consumers need table-friendly exports after evidence exists; adding export helpers before
  manifests would force another ad hoc source contract.

## Tranche Decision

P15 should implement durable run and matrix evidence manifests. This is the next FreshForge-owned
contract because it is generic, directly addresses observed downstream parsing and audit friction,
and creates the audit substrate needed before any heavier execution features are considered.

P16 should add optional provider result and validation evidence conventions after manifests exist.
P17 should add matrix evidence exports from persisted manifests. P18 should package P15-P17 as
`v0.1.0a6`.

## Deferred Work

The P14-P18 tranche does not implement domain semantics, real ecosystem adapters, caching,
checkpointing, resumability, remotes, retries, parallel execution, production scheduling, plotting,
notebook execution, or statistical comparison. Those features should be revisited only after
evidence manifests and provider evidence conventions are implemented, documented, and tested.
