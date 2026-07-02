"""Generic run-matrix expansion for FreshForge workflows."""

from __future__ import annotations

import itertools
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from freshforge.execution import run_workflow, validate_run_namespace
from freshforge.loading import load_workflow_document
from freshforge.planning import create_run_plan
from freshforge.providers import ProviderRegistry
from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    RunPlan,
    RunStatus,
    WorkflowRunResult,
    WorkflowRunSummary,
    WorkflowSpec,
)
from freshforge.validation import has_error_diagnostics, validate_workflow_document

_SLUG_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
_PLACEHOLDER_RE = re.compile(r"\$\{matrix\.([A-Za-z0-9_.-]+)\}")


@dataclass(frozen=True)
class MatrixAxisValue:
    """One value for a matrix axis."""

    id: str
    variables: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"id": self.id}
        if self.variables:
            data["variables"] = self.variables
        return data


@dataclass(frozen=True)
class MatrixAxis:
    """One Cartesian-product axis in a matrix document."""

    id: str
    values: tuple[MatrixAxisValue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "values": [value.to_dict() for value in self.values]}


@dataclass(frozen=True)
class MatrixCase:
    """One expanded or explicitly declared matrix case."""

    id: str
    variables: dict[str, Any] = field(default_factory=dict)
    namespace: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"id": self.id}
        if self.namespace is not None:
            data["namespace"] = self.namespace
        if self.variables:
            data["variables"] = self.variables
        return data


@dataclass(frozen=True)
class WorkflowMatrixSpec:
    """A matrix specification that expands one workflow template into cases."""

    id: str
    workflow_template: str
    cases: tuple[MatrixCase, ...] = ()
    axes: tuple[MatrixAxis, ...] = ()
    name: str | None = None
    description: str | None = None
    source_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        matrix: dict[str, Any] = {"id": self.id, "workflow_template": self.workflow_template}
        if self.name is not None:
            matrix["name"] = self.name
        if self.description is not None:
            matrix["description"] = self.description
        data: dict[str, Any] = {"matrix": matrix}
        if self.cases:
            data["cases"] = [case.to_dict() for case in self.cases]
        if self.axes:
            data["axes"] = [axis.to_dict() for axis in self.axes]
        if self.source_path is not None:
            data["source_path"] = self.source_path
        return data


@dataclass(frozen=True)
class ExpandedWorkflowCase:
    """One matrix case expanded into an ordinary FreshForge workflow spec."""

    case: MatrixCase
    namespace: str
    variables: dict[str, Any]
    workflow: WorkflowSpec | None
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return self.workflow is not None and not has_error_diagnostics(self.diagnostics)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case": self.case.to_dict(),
            "namespace": self.namespace,
            "variables": self.variables,
            "workflow": self.workflow.to_dict() if self.workflow is not None else None,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class WorkflowMatrixPlanCase:
    """Run-plan result for one expanded matrix case."""

    case_id: str
    namespace: str
    workflow_id: str | None
    plan: RunPlan | None
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return self.plan is not None and not self.plan.has_errors and not has_error_diagnostics(
            self.diagnostics
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "namespace": self.namespace,
            "workflow_id": self.workflow_id,
            "plan": self.plan.to_dict() if self.plan is not None else None,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class WorkflowMatrixPlan:
    """Non-executing plan for all cases in a matrix."""

    matrix_id: str
    cases: tuple[WorkflowMatrixPlanCase, ...]
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return not has_error_diagnostics(self.diagnostics) and all(case.ok for case in self.cases)

    def to_dict(self) -> dict[str, Any]:
        return {
            "matrix_id": self.matrix_id,
            "cases": [case.to_dict() for case in self.cases],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class WorkflowMatrixRunCase:
    """Execution result for one matrix case."""

    case_id: str
    namespace: str
    run: WorkflowRunResult | None
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return self.run is not None and self.run.ok and not has_error_diagnostics(self.diagnostics)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "namespace": self.namespace,
            "run": self.run.to_dict() if self.run is not None else None,
            "summary": self.run.summary().to_dict() if self.run is not None else None,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class WorkflowMatrixSummary:
    """Compact summary for a matrix run."""

    matrix_id: str
    status: RunStatus
    case_count: int = 0
    succeeded_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    diagnostic_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    cases: tuple[WorkflowRunSummary, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status is RunStatus.SUCCESS and self.error_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "matrix_id": self.matrix_id,
            "status": self.status.value,
            "case_count": self.case_count,
            "succeeded_count": self.succeeded_count,
            "failed_count": self.failed_count,
            "skipped_count": self.skipped_count,
            "diagnostic_count": self.diagnostic_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "cases": [case.to_dict() for case in self.cases],
        }


@dataclass(frozen=True)
class WorkflowMatrixRunResult:
    """Execution result for all cases in a matrix."""

    matrix_id: str
    status: RunStatus
    cases: tuple[WorkflowMatrixRunCase, ...]
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status is RunStatus.SUCCESS and not has_error_diagnostics(self.diagnostics)

    def summary(self) -> WorkflowMatrixSummary:
        case_summaries = tuple(case.run.summary() for case in self.cases if case.run is not None)
        diagnostics = list(self.diagnostics)
        for case in self.cases:
            diagnostics.extend(case.diagnostics)
            if case.run is not None:
                diagnostics.extend(case.run.diagnostics)
        return WorkflowMatrixSummary(
            matrix_id=self.matrix_id,
            status=self.status,
            case_count=len(self.cases),
            succeeded_count=sum(1 for case in self.cases if case.ok),
            failed_count=sum(1 for case in self.cases if not case.ok),
            skipped_count=0,
            diagnostic_count=len(diagnostics),
            error_count=sum(
                1 for diagnostic in diagnostics if diagnostic.severity is DiagnosticSeverity.ERROR
            ),
            warning_count=sum(
                1
                for diagnostic in diagnostics
                if diagnostic.severity is DiagnosticSeverity.WARNING
            ),
            cases=case_summaries,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "matrix_id": self.matrix_id,
            "status": self.status.value,
            "cases": [case.to_dict() for case in self.cases],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


def load_workflow_matrix(path: str | Path) -> tuple[WorkflowMatrixSpec | None, list[Diagnostic]]:
    """Load and validate a matrix document from YAML or JSON."""
    source_path = Path(path)
    try:
        document = load_workflow_document(source_path)
    except OSError as exc:
        return None, [_diagnostic("source.read_failed", str(exc), str(source_path))]
    except (ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return None, [_diagnostic("source.load_failed", str(exc), str(source_path))]
    return validate_workflow_matrix_document(document, source_path=str(source_path))


def validate_workflow_matrix_document(
    document: Any,
    *,
    source_path: str | None = None,
) -> tuple[WorkflowMatrixSpec | None, list[Diagnostic]]:
    """Validate a raw matrix document."""
    diagnostics: list[Diagnostic] = []
    if not isinstance(document, Mapping):
        return None, [
            _diagnostic("matrix.source.not_mapping", "Matrix source must be a mapping.", "$")
        ]

    matrix_data = document.get("matrix")
    if not isinstance(matrix_data, Mapping):
        diagnostics.append(
            _diagnostic("matrix.not_mapping", "Top-level 'matrix' must be a mapping.", "matrix")
        )
        matrix_data = {}

    matrix_id = _optional_string(matrix_data.get("id")) if matrix_data else None
    if not matrix_id:
        diagnostics.append(_diagnostic("matrix.id.required", "Matrix id is required.", "matrix.id"))
        matrix_id = ""
    elif not _is_slug(matrix_id):
        diagnostics.append(
            _diagnostic("matrix.id.invalid", "Matrix id must be slug-like.", "matrix.id")
        )

    workflow_template = (
        _optional_string(matrix_data.get("workflow_template")) if matrix_data else None
    )
    if not workflow_template:
        diagnostics.append(
            _diagnostic(
                "matrix.workflow_template.required",
                "Matrix workflow_template is required.",
                "matrix.workflow_template",
            )
        )
        workflow_template = ""

    cases = _parse_cases(document.get("cases"), diagnostics)
    axes = _parse_axes(document.get("axes"), diagnostics)
    if cases and axes:
        diagnostics.append(
            _diagnostic(
                "matrix.shape.ambiguous",
                "Matrix must define either cases or axes, not both.",
                "cases",
            )
        )
    if not cases and not axes:
        diagnostics.append(
            _diagnostic(
                "matrix.shape.empty",
                "Matrix must define at least one explicit case or one axis.",
                "cases",
            )
        )

    return (
        WorkflowMatrixSpec(
            id=matrix_id,
            name=_optional_string(matrix_data.get("name")) if matrix_data else None,
            description=_optional_string(matrix_data.get("description")) if matrix_data else None,
            workflow_template=workflow_template,
            cases=tuple(cases),
            axes=tuple(axes),
            source_path=source_path,
        ),
        diagnostics,
    )


def expand_workflow_matrix(
    matrix: WorkflowMatrixSpec,
    *,
    diagnostics: Sequence[Diagnostic] | None = None,
) -> tuple[ExpandedWorkflowCase, ...]:
    """Expand all matrix cases into workflow specs."""
    initial_diagnostics = tuple(diagnostics or ())
    if has_error_diagnostics(initial_diagnostics):
        return ()

    template_path = _matrix_template_path(matrix)
    try:
        template_document = load_workflow_document(template_path)
    except OSError as exc:
        return (
            _unexpanded_case(
                matrix=matrix,
                case=MatrixCase(id="template"),
                diagnostics=(
                    _diagnostic("matrix.template.read_failed", str(exc), str(template_path)),
                ),
            ),
        )
    except (ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return (
            _unexpanded_case(
                matrix=matrix,
                case=MatrixCase(id="template"),
                diagnostics=(
                    _diagnostic("matrix.template.load_failed", str(exc), str(template_path)),
                ),
            ),
        )

    return tuple(
        _expand_case(matrix=matrix, case=case, template_document=template_document)
        for case in _matrix_cases(matrix)
    )


def plan_workflow_matrix(
    matrix: WorkflowMatrixSpec,
    *,
    diagnostics: Sequence[Diagnostic] | None = None,
    registry: ProviderRegistry | None = None,
) -> WorkflowMatrixPlan:
    """Create non-executing run plans for every matrix case."""
    initial_diagnostics = tuple(diagnostics or ())
    expanded = expand_workflow_matrix(matrix, diagnostics=initial_diagnostics)
    cases: list[WorkflowMatrixPlanCase] = []
    for case in expanded:
        if case.workflow is None:
            cases.append(
                WorkflowMatrixPlanCase(
                    case_id=case.case.id,
                    namespace=case.namespace,
                    workflow_id=None,
                    plan=None,
                    diagnostics=case.diagnostics,
                )
            )
            continue
        plan = create_run_plan(case.workflow, diagnostics=case.diagnostics, registry=registry)
        cases.append(
            WorkflowMatrixPlanCase(
                case_id=case.case.id,
                namespace=case.namespace,
                workflow_id=case.workflow.id,
                plan=plan,
                diagnostics=case.diagnostics,
            )
        )
    return WorkflowMatrixPlan(
        matrix_id=matrix.id,
        cases=tuple(cases),
        diagnostics=initial_diagnostics,
    )


def run_workflow_matrix(
    matrix: WorkflowMatrixSpec,
    *,
    diagnostics: Sequence[Diagnostic] | None = None,
    registry: ProviderRegistry | None = None,
    workdir: str | Path | None = None,
    fail_fast: bool = False,
) -> WorkflowMatrixRunResult:
    """Execute every matrix case serially."""
    initial_diagnostics = tuple(diagnostics or ())
    expanded = expand_workflow_matrix(matrix, diagnostics=initial_diagnostics)
    run_cases: list[WorkflowMatrixRunCase] = []
    for case in expanded:
        if case.workflow is None:
            run_cases.append(
                WorkflowMatrixRunCase(
                    case_id=case.case.id,
                    namespace=case.namespace,
                    run=None,
                    diagnostics=case.diagnostics,
                )
            )
        else:
            run = run_workflow(
                case.workflow,
                diagnostics=case.diagnostics,
                registry=registry,
                workdir=workdir,
                run_namespace=case.namespace,
            )
            run_cases.append(
                WorkflowMatrixRunCase(
                    case_id=case.case.id,
                    namespace=case.namespace,
                    run=run,
                    diagnostics=case.diagnostics,
                )
            )
        if fail_fast and not run_cases[-1].ok:
            break

    status = (
        RunStatus.SUCCESS
        if run_cases and all(case.ok for case in run_cases)
        else RunStatus.FAILED
    )
    if has_error_diagnostics(initial_diagnostics):
        status = RunStatus.FAILED
    return WorkflowMatrixRunResult(
        matrix_id=matrix.id,
        status=status,
        cases=tuple(run_cases),
        diagnostics=initial_diagnostics,
    )


def _expand_case(
    *,
    matrix: WorkflowMatrixSpec,
    case: MatrixCase,
    template_document: Any,
) -> ExpandedWorkflowCase:
    namespace = case.namespace or f"{matrix.id}/{case.id}"
    diagnostics: list[Diagnostic] = []
    namespace_diagnostic = validate_run_namespace(namespace)
    if namespace_diagnostic is not None:
        diagnostics.append(namespace_diagnostic)
    variables = {
        "case_id": case.id,
        "namespace": namespace,
        **case.variables,
    }
    if "__matrix_duplicate_variables__" in variables:
        diagnostics.append(
            _diagnostic(
                "matrix.axis.variables.duplicate",
                "Axis values produced duplicate matrix variable keys.",
                f"cases.{case.id}.variables",
            )
        )
        variables.pop("__matrix_duplicate_variables__")
    if "__matrix_duplicate_case_id__" in variables:
        diagnostics.append(
            _diagnostic(
                "matrix.axis.case_id.duplicate",
                f"Axis values produced duplicate case id '{case.id}'.",
                f"cases.{case.id}.id",
            )
        )
        variables.pop("__matrix_duplicate_case_id__")
    substituted = _substitute_template(template_document, variables, diagnostics, location="$")
    workflow, workflow_diagnostics = validate_workflow_document(
        substituted,
        source_path=f"{_matrix_template_path(matrix)}#{case.id}",
    )
    diagnostics.extend(workflow_diagnostics)
    return ExpandedWorkflowCase(
        case=case,
        namespace=namespace,
        variables=variables,
        workflow=workflow,
        diagnostics=tuple(diagnostics),
    )


def _substitute_template(
    value: Any,
    variables: Mapping[str, Any],
    diagnostics: list[Diagnostic],
    *,
    location: str,
) -> Any:
    if isinstance(value, str):
        return _substitute_string(value, variables, diagnostics, location=location)
    if isinstance(value, list):
        return [
            _substitute_template(item, variables, diagnostics, location=f"{location}[{index}]")
            for index, item in enumerate(value)
        ]
    if isinstance(value, Mapping):
        return {
            key: _substitute_template(item, variables, diagnostics, location=f"{location}.{key}")
            for key, item in value.items()
        }
    return value


def _substitute_string(
    value: str,
    variables: Mapping[str, Any],
    diagnostics: list[Diagnostic],
    *,
    location: str,
) -> str:
    def replacement(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in variables:
            diagnostics.append(
                _diagnostic(
                    "matrix.placeholder.missing",
                    f"Matrix placeholder '{key}' has no value.",
                    location,
                )
            )
            return match.group(0)
        return str(variables[key])

    return _PLACEHOLDER_RE.sub(replacement, value)


def _matrix_cases(matrix: WorkflowMatrixSpec) -> tuple[MatrixCase, ...]:
    if matrix.cases:
        return matrix.cases

    cases: list[MatrixCase] = []
    generated_ids: set[str] = set()
    for combination in itertools.product(*(axis.values for axis in matrix.axes)):
        case_id = "_".join(
            f"{axis.id}-{value.id}"
            for axis, value in zip(matrix.axes, combination, strict=True)
        )
        variables: dict[str, Any] = {}
        duplicate_keys: set[str] = set()
        for value in combination:
            for key, item in value.variables.items():
                if key in variables:
                    duplicate_keys.add(key)
                variables[key] = item
        if duplicate_keys:
            variables["__matrix_duplicate_variables__"] = ",".join(sorted(duplicate_keys))
        if case_id in generated_ids:
            variables["__matrix_duplicate_case_id__"] = case_id
        generated_ids.add(case_id)
        cases.append(MatrixCase(id=case_id, variables=variables))
    return tuple(cases)


def _unexpanded_case(
    *,
    matrix: WorkflowMatrixSpec,
    case: MatrixCase,
    diagnostics: Sequence[Diagnostic],
) -> ExpandedWorkflowCase:
    namespace = case.namespace or f"{matrix.id}/{case.id}"
    return ExpandedWorkflowCase(
        case=case,
        namespace=namespace,
        variables={"case_id": case.id, "namespace": namespace, **case.variables},
        workflow=None,
        diagnostics=tuple(diagnostics),
    )


def _matrix_template_path(matrix: WorkflowMatrixSpec) -> Path:
    path = Path(matrix.workflow_template)
    if path.is_absolute() or matrix.source_path is None:
        return path
    return Path(matrix.source_path).parent / path


def _parse_cases(value: Any, diagnostics: list[Diagnostic]) -> list[MatrixCase]:
    if value is None:
        return []
    if not isinstance(value, list):
        diagnostics.append(
            _diagnostic("matrix.cases.not_list", "Matrix cases must be a list.", "cases")
        )
        return []
    cases: list[MatrixCase] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        location = f"cases[{index}]"
        if not isinstance(item, Mapping):
            diagnostics.append(
                _diagnostic("matrix.case.not_mapping", "Matrix case must be a mapping.", location)
            )
            continue
        case_id = _optional_string(item.get("id"))
        if not case_id:
            diagnostics.append(
                _diagnostic(
                    "matrix.case.id.required",
                    "Matrix case id is required.",
                    f"{location}.id",
                )
            )
            case_id = ""
        elif not _is_slug(case_id):
            diagnostics.append(
                _diagnostic(
                    "matrix.case.id.invalid",
                    "Matrix case id must be slug-like.",
                    f"{location}.id",
                )
            )
        elif case_id in seen_ids:
            diagnostics.append(
                _diagnostic(
                    "matrix.case.id.duplicate",
                    f"Matrix case id '{case_id}' is duplicated.",
                    f"{location}.id",
                )
            )
        seen_ids.add(case_id)
        variables = _variables(
            item.get("variables", {}),
            diagnostics,
            location=f"{location}.variables",
        )
        namespace = _optional_string(item.get("namespace"))
        cases.append(MatrixCase(id=case_id, variables=variables, namespace=namespace))
    return cases


def _parse_axes(value: Any, diagnostics: list[Diagnostic]) -> list[MatrixAxis]:
    if value is None:
        return []
    if not isinstance(value, list):
        diagnostics.append(
            _diagnostic("matrix.axes.not_list", "Matrix axes must be a list.", "axes")
        )
        return []
    axes: list[MatrixAxis] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        location = f"axes[{index}]"
        if not isinstance(item, Mapping):
            diagnostics.append(
                _diagnostic("matrix.axis.not_mapping", "Matrix axis must be a mapping.", location)
            )
            continue
        axis_id = _optional_string(item.get("id"))
        if not axis_id:
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.id.required",
                    "Matrix axis id is required.",
                    f"{location}.id",
                )
            )
            axis_id = ""
        elif not _is_slug(axis_id):
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.id.invalid",
                    "Matrix axis id must be slug-like.",
                    f"{location}.id",
                )
            )
        elif axis_id in seen_ids:
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.id.duplicate",
                    f"Matrix axis id '{axis_id}' is duplicated.",
                    f"{location}.id",
                )
            )
        seen_ids.add(axis_id)
        values = _parse_axis_values(item.get("values"), diagnostics, location=f"{location}.values")
        axes.append(MatrixAxis(id=axis_id, values=tuple(values)))
    return axes


def _parse_axis_values(
    value: Any,
    diagnostics: list[Diagnostic],
    *,
    location: str,
) -> list[MatrixAxisValue]:
    if not isinstance(value, list) or not value:
        diagnostics.append(
            _diagnostic(
                "matrix.axis.values.invalid",
                "Matrix axis values must be a non-empty list.",
                location,
            )
        )
        return []
    values: list[MatrixAxisValue] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        item_location = f"{location}[{index}]"
        if not isinstance(item, Mapping):
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.value.not_mapping",
                    "Matrix axis value must be a mapping.",
                    item_location,
                )
            )
            continue
        value_id = _optional_string(item.get("id"))
        if not value_id:
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.value.id.required",
                    "Matrix axis value id is required.",
                    f"{item_location}.id",
                )
            )
            value_id = ""
        elif not _is_slug(value_id):
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.value.id.invalid",
                    "Matrix axis value id must be slug-like.",
                    f"{item_location}.id",
                )
            )
        elif value_id in seen_ids:
            diagnostics.append(
                _diagnostic(
                    "matrix.axis.value.id.duplicate",
                    f"Matrix axis value id '{value_id}' is duplicated.",
                    f"{item_location}.id",
                )
            )
        seen_ids.add(value_id)
        variables = _variables(
            item.get("variables", {}),
            diagnostics,
            location=f"{item_location}.variables",
        )
        values.append(MatrixAxisValue(id=value_id, variables=variables))
    return values


def _variables(value: Any, diagnostics: list[Diagnostic], *, location: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        diagnostics.append(
            _diagnostic(
                "matrix.variables.not_mapping",
                "Matrix variables must be a mapping.",
                location,
            )
        )
        return {}
    variables: dict[str, Any] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not _is_slug(key):
            diagnostics.append(
                _diagnostic(
                    "matrix.variable.key.invalid",
                    "Matrix variable keys must be slug-like strings.",
                    location,
                )
            )
            continue
        variables[key] = item
    return variables


def _optional_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _is_slug(value: str) -> bool:
    return bool(_SLUG_RE.fullmatch(value))


def _diagnostic(code: str, message: str, location: str | None = None) -> Diagnostic:
    return Diagnostic(
        severity=DiagnosticSeverity.ERROR,
        code=code,
        message=message,
        location=location,
    )
