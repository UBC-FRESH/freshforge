# AGENTS.md

This file is the working contract for AI coding agents in this repository.

## Project Purpose

`freshforge` exists to build workflow-as-code infrastructure for open forest
resources and ecosystem services modelling.

The goal is not to recreate ArcGIS ModelBuilder or QGIS Graphical Modeler as a
GUI. The goal is to make the workflow graph, node contracts, provenance,
validation, and execution records the durable source of truth. User interfaces
may eventually edit or inspect those records, but the GUI should not become the
execution engine or the only representation of the model.

FreshForge should stay neutral across the FRESH software ecosystem. FEMIC,
FHOPS, ws3, Modelwright, Nemora, and other tools may eventually expose nodes or
adapters to FreshForge, but the FreshForge core should not directly import those
domain packages unless a future roadmap phase explicitly changes that boundary.

## Current Repo State

This repository has completed the Phase 2 core workflow-records milestone. It
contains:

- `README.md`: concise public overview and current status.
- `ROADMAP.md`: phase/task roadmap and issue tracker map.
- `CHANGE_LOG.md`: append-only project narrative.
- `planning/`: focused design notes and research records.
- `pyproject.toml`: package metadata and optional dependency groups.
- `src/freshforge/`: importable package code for CLI, records, loading,
  validation, and non-executing planning.
- `tests/`: package-backed tests for package metadata, CLI behavior, docs,
  records, loading, validation, and planning.
- `docs/`: Sphinx documentation skeleton.
- `examples/`: public-safe example workflow specs.
- `.github/workflows/`: CI, docs, and release-artifact checks.
- `tmp/`: ignored local working area for notes, experiments, and generated
  artifacts.

FreshForge implements provisional YAML/JSON workflow loading, structural
validation diagnostics, and non-executing run planning. Do not claim that
FreshForge implements node execution, provider discovery, provider protocols,
cache/checkpoint behavior, or FRESH ecosystem adapters until the relevant
roadmap phase records that evidence.

## Workflow Specs And Generated Outputs

Workflow recipes, local run records, generated reports, scratch execution logs,
and project-specific examples should be treated as local working material unless
the maintainer explicitly asks to track a sanitized artifact.

Rules:

- Keep `tmp/`, `local/`, `data/private/`, and `outputs/` ignored.
- Do not commit private project data, raw transcripts, local workflow outputs,
  credentials, machine-specific paths, or unpublished source documents.
- Tracked examples and tests must use synthetic or public-safe fixtures.
- Record provenance for every interpreted workflow source, external dataset,
  node implementation, command, environment, and validation result.
- Keep workflow-specific assumptions explicit rather than silently baking them
  into generic core logic.

## Working Principles

- Read `AGENTS.md`, `ROADMAP.md`, and `CHANGE_LOG.md` before making
  project-shaping changes.
- Keep CLI commands thin wrappers over Python APIs.
- Keep domain science in domain packages; keep FreshForge focused on workflow
  contracts, validation, planning, execution records, and orchestration
  semantics.
- Prefer structured records and parsers over ad hoc string handling.
- Emit explicit diagnostics for unsupported workflow features, missing node
  providers, invalid dependencies, uncertain provenance, and failed validation.
- Preserve uncertainty. A workflow result is only as strong as its declared
  inputs, node implementations, and verification evidence.
- Keep public repo content clean of private, irrelevant, or unpublished
  references. Prefer sanitized summaries over raw pasted notes.
- Keep changes scoped to the active roadmap phase and issue.

## Planning Workflow

This repo follows the UBC-FRESH phase/task/subtask workflow:

- `ROADMAP.md` is the current plan and issue tracker map.
- One roadmap phase maps to one GitHub parent issue and one feature branch.
- One roadmap task maps to one child issue linked from the parent issue body.
- Subtasks usually stay as checklist items inside the child issue body.
- Use at most three issue levels: phase, task, implementation subtask.
- Record issue numbers beside roadmap phases and tasks once created.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, planning notes, issue bodies, and PR
  descriptions synchronized.
- Open a PR from the phase branch to `main` only after phase tasks, tests, docs,
  and closeout notes are complete or explicitly deferred.

## Strict Development Workflow

Use this workflow for active development from the first phase boundary onward:

- One active roadmap phase should generally correspond to one GitHub parent
  issue and one feature branch.
- Create or activate the GitHub parent issue before starting a roadmap phase.
- Create the feature branch from current `main` for that parent issue.
- Create child issues for roadmap tasks under the parent issue.
- Document task subtasks as checklist steps inside the child issue body unless
  they are large enough to deserve third-level implementation issues.
- Work child issues one at a time where practical, usually in roadmap order.
- Before closing a child issue, update every issue-body checklist item to
  checked, or rewrite the issue body to make explicitly clear which items were
  superseded or are not applicable.
- Close each child issue only after its repo changes, documentation, issue-body
  checklist, and verification for that task are complete.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, and issue comments synchronized as task
  state changes.
- Open a PR from the phase branch back to `main` when the parent issue's child
  issues are complete or explicitly deferred.
- Close the parent issue only after the PR has merged back to `main`.
- Do not start a new active parent issue and branch until the current parent
  issue is closed, unless the maintainer explicitly approves a parallel lane.

## GitHub Issue And Comment Formatting

Formatting matters. GitHub issue bodies and comments must be readable as
rendered Markdown, not flattened prose.

Rules:

- Use short section labels on their own lines, such as `Roadmap task: P3.1`,
  `Parent phase issue: #18`, `Status: active`, and `Checklist:`.
- Use real GitHub task-list syntax, with one checklist item per line.
- Never write inline pseudo-checklists such as
  `Checklist: [ ] first. [ ] second.`
- Wrap branch names, file paths, commands, and commit hashes in backticks.
- For parent phase issues, list child issues as task-list bullets with issue
  numbers and task IDs.
- Before creating or editing several issues, prepare bodies as multi-line
  Markdown strings or temporary body files.

## GitHub Issue Body Quality Standard

Issue bodies are part of the project specification and onboarding material.
Write them so a new lab student, external collaborator, or coding agent can
understand the task, implement it, verify it, and close it without reading the
original chat transcript.

Parent phase issues must include phase identifier, status, branch name, roadmap
links, goal, scope, out-of-scope boundaries, architecture notes, child task
checklist, acceptance criteria, verification, and closeout requirements.

Child task issues must include task identifier, parent phase issue, status,
related planning links, goal, scope, out-of-scope boundaries, subtasks,
acceptance criteria, verification commands, artifacts, risks, and completion
metadata once closed.

Do not create placeholder issue bodies with only a title and a short checklist
unless the maintainer explicitly asks for a placeholder.

## Verification

Default local checks:

```bash
python -m ruff check .
python -m pytest
sphinx-build -b html docs _build/html -W
python -m build
twine check dist/*
```

Default CI must not require private project data, commercial GIS software, local
desktop applications, credentials, or network downloads beyond package
installation.
