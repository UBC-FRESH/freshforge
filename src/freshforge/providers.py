"""Provider metadata and explicit registry support."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol

from freshforge.records import Diagnostic, DiagnosticSeverity, WorkflowNode


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


def default_provider_registry() -> ProviderRegistry:
    """Return FreshForge's built-in public-safe provider registry."""
    registry = ProviderRegistry()
    registry.register(ExampleProvider())
    return registry


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


def _find_node_type(
    metadata: ProviderMetadata,
    node_type_id: str,
) -> NodeTypeMetadata | None:
    for node_type in metadata.node_types:
        if node_type.id == node_type_id:
            return node_type
    return None


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
