"""Provider metadata and explicit registry support."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from importlib import metadata as importlib_metadata
from typing import Protocol

from freshforge.records import (
    Diagnostic,
    DiagnosticSeverity,
    ExecutionContext,
    ProviderExecutionResult,
    WorkflowNode,
)

PROVIDER_ENTRY_POINT_GROUP = "freshforge.providers"


@dataclass(frozen=True)
class ProviderReference:
    """Parsed workflow provider reference."""

    reference: str
    provider_id: str
    node_type: str

    def to_dict(self) -> dict[str, str]:
        return {
            "reference": self.reference,
            "provider_id": self.provider_id,
            "node_type": self.node_type,
        }


@dataclass(frozen=True)
class NodeTypeMetadata:
    """Provider-owned metadata for one node type."""

    id: str
    name: str | None = None
    description: str | None = None
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    parameters: tuple[str, ...] = ()
    artifacts: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "parameters": list(self.parameters),
            "artifacts": list(self.artifacts),
        }
        if self.name is not None:
            data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        return data


@dataclass(frozen=True)
class ProviderMetadata:
    """Provider-owned metadata for registry listing and planning."""

    id: str
    version: str
    name: str | None = None
    description: str | None = None
    node_types: tuple[NodeTypeMetadata, ...] = ()

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "version": self.version,
            "node_types": [node_type.to_dict() for node_type in self.node_types],
        }
        if self.name is not None:
            data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        return data


@dataclass(frozen=True)
class ProviderResolution:
    """Provider registry interpretation of a node provider reference."""

    reference: str
    provider_id: str | None
    node_type: str | None
    provider_available: bool
    node_type_available: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "reference": self.reference,
            "provider_id": self.provider_id,
            "node_type": self.node_type,
            "provider_available": self.provider_available,
            "node_type_available": self.node_type_available,
        }


class Provider(Protocol):
    """Non-executing provider interface."""

    def metadata(self) -> ProviderMetadata:
        """Return provider metadata."""

    def validate_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        location: str,
    ) -> Sequence[Diagnostic]:
        """Validate one node without executing it."""


class ExecutableProvider(Provider, Protocol):
    """Provider interface extension for executable workflow nodes."""

    def execute_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        context: ExecutionContext,
    ) -> ProviderExecutionResult:
        """Execute one workflow node and return provider-owned metadata."""


@dataclass
class ProviderRegistry:
    """Explicit in-process provider registry."""

    _providers: dict[str, Provider] = field(default_factory=dict)

    def register(self, provider: Provider) -> None:
        """Register a provider by metadata id."""
        provider_id = provider.metadata().id
        if provider_id in self._providers:
            raise ValueError(f"Provider '{provider_id}' is already registered.")
        self._providers[provider_id] = provider

    def try_register(self, provider: Provider, *, location: str | None = None) -> Diagnostic | None:
        """Register a provider and return a diagnostic instead of raising."""
        try:
            self.register(provider)
        except Exception as exc:  # noqa: BLE001
            provider_id = _safe_provider_id(provider)
            return Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="provider.registration.failed",
                message=f"Could not register provider '{provider_id}': {exc}",
                location=location,
            )
        return None

    def get(self, provider_id: str) -> Provider | None:
        """Return a provider by id when registered."""
        return self._providers.get(provider_id)

    def list(self) -> tuple[ProviderMetadata, ...]:
        """Return registered provider metadata in deterministic order."""
        return tuple(
            self._providers[provider_id].metadata() for provider_id in sorted(self._providers)
        )

    def resolve(self, reference: str) -> ProviderResolution:
        """Resolve a workflow provider reference against the registry."""
        parsed = parse_provider_reference(reference)
        if parsed is None:
            return ProviderResolution(
                reference=reference,
                provider_id=None,
                node_type=None,
                provider_available=False,
                node_type_available=False,
            )
        provider = self.get(parsed.provider_id)
        if provider is None:
            return ProviderResolution(
                reference=reference,
                provider_id=parsed.provider_id,
                node_type=parsed.node_type,
                provider_available=False,
                node_type_available=False,
            )
        node_type_available = _find_node_type(provider.metadata(), parsed.node_type) is not None
        return ProviderResolution(
            reference=reference,
            provider_id=parsed.provider_id,
            node_type=parsed.node_type,
            provider_available=True,
            node_type_available=node_type_available,
        )


def parse_provider_reference(reference: str) -> ProviderReference | None:
    """Parse a provider reference using the final dotted part as node type."""
    parts = reference.rsplit(".", maxsplit=1)
    if len(parts) != 2:
        return None
    provider_id, node_type = (part.strip() for part in parts)
    if not provider_id or not node_type:
        return None
    return ProviderReference(reference=reference, provider_id=provider_id, node_type=node_type)


def default_provider_registry(
    *,
    include_entry_points: bool = True,
) -> tuple[ProviderRegistry, tuple[Diagnostic, ...]]:
    """Return FreshForge's built-in public-safe provider registry."""
    registry = ProviderRegistry()
    registry.register(ExampleProvider())
    diagnostics: list[Diagnostic] = []
    if include_entry_points:
        diagnostics.extend(discover_entry_point_providers(registry))
    return registry, tuple(diagnostics)


def discover_entry_point_providers(
    registry: ProviderRegistry,
    *,
    group: str = PROVIDER_ENTRY_POINT_GROUP,
) -> tuple[Diagnostic, ...]:
    """Discover and register provider factories from Python entry points."""
    diagnostics: list[Diagnostic] = []
    for entry_point in _provider_entry_points(group):
        location = f"entry_points.{group}.{entry_point.name}"
        try:
            factory = entry_point.load()
        except Exception as exc:  # noqa: BLE001
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="provider.discovery.load_failed",
                    message=f"Could not load provider entry point '{entry_point.name}': {exc}",
                    location=location,
                )
            )
            continue

        try:
            provider = factory()
        except Exception as exc:  # noqa: BLE001
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="provider.discovery.factory_failed",
                    message=f"Provider entry point '{entry_point.name}' failed: {exc}",
                    location=location,
                )
            )
            continue

        invalid_diagnostic = _validate_provider_object(provider, location=location)
        if invalid_diagnostic is not None:
            diagnostics.append(invalid_diagnostic)
            continue

        duplicate_diagnostic = registry.try_register(provider, location=location)
        if duplicate_diagnostic is not None:
            duplicate_diagnostic = Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="provider.discovery.duplicate",
                message=duplicate_diagnostic.message,
                location=location,
            )
            diagnostics.append(duplicate_diagnostic)

    return tuple(diagnostics)


class ExampleProvider:
    """Public-safe example provider for tests and documentation."""

    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            id="freshforge.example",
            version="0.1.0a1",
            name="FreshForge example provider",
            description="Non-executing example node types for public FreshForge workflows.",
            node_types=(
                NodeTypeMetadata(
                    id="load_inventory",
                    name="Load inventory",
                    description="Declare a synthetic inventory input node.",
                    outputs=("inventory",),
                ),
                NodeTypeMetadata(
                    id="classify_fuel",
                    name="Classify fuel",
                    description="Declare a placeholder fuel classification node.",
                    inputs=("inventory",),
                    outputs=("fuel_class",),
                    parameters=("classification",),
                ),
                NodeTypeMetadata(
                    id="choose_treatment",
                    name="Choose treatment",
                    description="Declare a placeholder treatment selection node.",
                    inputs=("fuel_class",),
                    outputs=("prescription",),
                    artifacts=("report",),
                ),
            ),
        )

    def validate_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        location: str,
    ) -> Sequence[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        diagnostics.extend(
            _missing_key_diagnostics(
                required=node_type.inputs,
                actual=node.inputs,
                field_name="inputs",
                location=location,
            )
        )
        diagnostics.extend(
            _missing_key_diagnostics(
                required=node_type.outputs,
                actual=node.outputs,
                field_name="outputs",
                location=location,
            )
        )
        return diagnostics


class FixtureProvider:
    """Public-safe fixture provider that simulates an ecosystem adapter."""

    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            id="freshforge.fixture",
            version="0.1.0a1",
            name="FreshForge fixture ecosystem adapter",
            description=(
                "Non-executing fixture provider for adapter discovery examples."
            ),
            node_types=(
                NodeTypeMetadata(
                    id="inventory_summary",
                    name="Inventory summary declaration",
                    description="Declare a public-safe inventory summary step.",
                    inputs=("inventory",),
                    outputs=("summary",),
                    parameters=("units",),
                ),
                NodeTypeMetadata(
                    id="yield_table_check",
                    name="Yield table check declaration",
                    description="Declare a public-safe yield table consistency check.",
                    inputs=("summary",),
                    outputs=("check",),
                    parameters=("species_group",),
                ),
                NodeTypeMetadata(
                    id="scenario_report",
                    name="Scenario report declaration",
                    description="Declare a public-safe scenario report artifact.",
                    inputs=("summary", "check"),
                    outputs=("report",),
                    artifacts=("report",),
                ),
            ),
        )

    def validate_node(
        self,
        node: WorkflowNode,
        node_type: NodeTypeMetadata,
        *,
        location: str,
    ) -> Sequence[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        diagnostics.extend(
            _missing_key_diagnostics(
                required=node_type.inputs,
                actual=node.inputs,
                field_name="inputs",
                location=location,
            )
        )
        diagnostics.extend(
            _missing_key_diagnostics(
                required=node_type.outputs,
                actual=node.outputs,
                field_name="outputs",
                location=location,
            )
        )
        diagnostics.extend(
            _missing_key_diagnostics(
                required=node_type.parameters,
                actual=node.parameters,
                field_name="parameters",
                location=location,
            )
        )
        diagnostics.extend(
            _missing_key_diagnostics(
                required=node_type.artifacts,
                actual=node.artifacts if isinstance(node.artifacts, dict) else {},
                field_name="artifacts",
                location=location,
            )
        )
        return diagnostics


def fixture_provider_factory() -> Provider:
    """Return the FreshForge fixture provider for entry-point discovery."""
    return FixtureProvider()


def _find_node_type(
    metadata: ProviderMetadata,
    node_type_id: str,
) -> NodeTypeMetadata | None:
    for node_type in metadata.node_types:
        if node_type.id == node_type_id:
            return node_type
    return None


def _provider_entry_points(group: str) -> tuple[importlib_metadata.EntryPoint, ...]:
    entry_points = importlib_metadata.entry_points()
    if hasattr(entry_points, "select"):
        selected = entry_points.select(group=group)
    else:
        selected = entry_points.get(group, ())
    return tuple(sorted(selected, key=lambda entry_point: entry_point.name))


def _validate_provider_object(
    provider: object,
    *,
    location: str,
) -> Diagnostic | None:
    if not hasattr(provider, "metadata") or not callable(provider.metadata):
        return Diagnostic(
            severity=DiagnosticSeverity.ERROR,
            code="provider.discovery.invalid",
            message="Provider entry point did not return an object with metadata().",
            location=location,
        )
    if not hasattr(provider, "validate_node") or not callable(provider.validate_node):
        return Diagnostic(
            severity=DiagnosticSeverity.ERROR,
            code="provider.discovery.invalid",
            message="Provider entry point did not return an object with validate_node().",
            location=location,
        )
    try:
        metadata = provider.metadata()
    except Exception as exc:  # noqa: BLE001
        return Diagnostic(
            severity=DiagnosticSeverity.ERROR,
            code="provider.discovery.metadata_failed",
            message=f"Provider metadata failed: {exc}",
            location=location,
        )
    if not isinstance(metadata, ProviderMetadata) or not metadata.id:
        return Diagnostic(
            severity=DiagnosticSeverity.ERROR,
            code="provider.discovery.metadata_invalid",
            message="Provider metadata must be a ProviderMetadata record with a nonempty id.",
            location=location,
        )
    return None


def _safe_provider_id(provider: object) -> str:
    try:
        return provider.metadata().id
    except Exception:  # noqa: BLE001
        return "<unknown>"


def _missing_key_diagnostics(
    *,
    required: Sequence[str],
    actual: dict[str, object],
    field_name: str,
    location: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for key in required:
        if key not in actual:
            diagnostics.append(
                Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code=f"node.{field_name}.missing",
                    message=f"Node is missing required provider-declared {field_name} key '{key}'.",
                    location=f"{location}.{field_name}.{key}",
                )
            )
    return diagnostics
