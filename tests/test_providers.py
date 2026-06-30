"""Provider registry and metadata tests."""

import pytest

from freshforge.providers import (
    ExampleProvider,
    FixtureProvider,
    NodeTypeMetadata,
    ProviderMetadata,
    ProviderRegistry,
    default_provider_registry,
    discover_entry_point_providers,
    parse_provider_reference,
)
from freshforge.records import WorkflowNode


def test_provider_metadata_to_dict_is_json_serializable_shape() -> None:
    metadata = ProviderMetadata(
        id="freshforge.example",
        version="0.1.0a1",
        name="Example",
        node_types=(NodeTypeMetadata(id="load", inputs=("source",), outputs=("table",)),),
    )

    assert metadata.to_dict() == {
        "id": "freshforge.example",
        "version": "0.1.0a1",
        "name": "Example",
        "node_types": [
            {
                "id": "load",
                "inputs": ["source"],
                "outputs": ["table"],
                "parameters": [],
                "artifacts": [],
            }
        ],
    }


def test_parse_provider_reference_uses_final_dotted_part_as_node_type() -> None:
    reference = parse_provider_reference("freshforge.example.load_inventory")

    assert reference is not None
    assert reference.provider_id == "freshforge.example"
    assert reference.node_type == "load_inventory"
    assert reference.to_dict()["reference"] == "freshforge.example.load_inventory"


def test_parse_provider_reference_rejects_unqualified_references() -> None:
    assert parse_provider_reference("load_inventory") is None
    assert parse_provider_reference("freshforge.example.") is None


def test_provider_registry_registers_and_resolves_provider_references() -> None:
    registry, diagnostics = default_provider_registry(include_entry_points=False)

    resolution = registry.resolve("freshforge.example.load_inventory")

    assert diagnostics == ()
    assert resolution.provider_id == "freshforge.example"
    assert resolution.node_type == "load_inventory"
    assert resolution.provider_available is True
    assert resolution.node_type_available is True


def test_provider_registry_rejects_duplicate_provider_ids() -> None:
    registry = ProviderRegistry()
    registry.register(ExampleProvider())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(ExampleProvider())


def test_provider_registry_lists_providers_deterministically() -> None:
    registry, diagnostics = default_provider_registry(include_entry_points=False)

    assert diagnostics == ()
    assert [provider.id for provider in registry.list()] == ["freshforge.example"]


def test_fixture_provider_metadata_serializes() -> None:
    metadata = FixtureProvider().metadata()

    assert metadata.id == "freshforge.fixture"
    assert [node_type.id for node_type in metadata.node_types] == [
        "inventory_summary",
        "yield_table_check",
        "scenario_report",
    ]


def test_discover_entry_point_providers_registers_valid_provider(monkeypatch) -> None:
    registry = ProviderRegistry()
    entry_points = (_FakeEntryPoint("fixture", lambda: FixtureProvider()),)
    monkeypatch.setattr("freshforge.providers._provider_entry_points", lambda group: entry_points)

    diagnostics = discover_entry_point_providers(registry)

    assert diagnostics == ()
    assert registry.get("freshforge.fixture") is not None


def test_discover_entry_point_providers_reports_duplicate_provider(monkeypatch) -> None:
    registry = ProviderRegistry()
    registry.register(FixtureProvider())
    entry_points = (_FakeEntryPoint("fixture", lambda: FixtureProvider()),)
    monkeypatch.setattr("freshforge.providers._provider_entry_points", lambda group: entry_points)

    diagnostics = discover_entry_point_providers(registry)

    assert {diagnostic.code for diagnostic in diagnostics} == {"provider.discovery.duplicate"}


def test_discover_entry_point_providers_reports_load_failure(monkeypatch) -> None:
    registry = ProviderRegistry()
    entry_points = (_FailingLoadEntryPoint("broken"),)
    monkeypatch.setattr("freshforge.providers._provider_entry_points", lambda group: entry_points)

    diagnostics = discover_entry_point_providers(registry)

    assert {diagnostic.code for diagnostic in diagnostics} == {"provider.discovery.load_failed"}


def test_discover_entry_point_providers_reports_invalid_object(monkeypatch) -> None:
    registry = ProviderRegistry()
    entry_points = (_FakeEntryPoint("invalid", lambda: object()),)
    monkeypatch.setattr("freshforge.providers._provider_entry_points", lambda group: entry_points)

    diagnostics = discover_entry_point_providers(registry)

    assert {diagnostic.code for diagnostic in diagnostics} == {"provider.discovery.invalid"}


def test_fixture_provider_reports_missing_declared_fields() -> None:
    provider = FixtureProvider()
    node_type = provider.metadata().node_types[0]
    node = WorkflowNode(id="summary", provider="freshforge.fixture.inventory_summary")

    diagnostics = provider.validate_node(node, node_type, location="nodes[0]")

    assert {diagnostic.code for diagnostic in diagnostics} == {
        "node.inputs.missing",
        "node.outputs.missing",
        "node.parameters.missing",
    }


class _FakeEntryPoint:
    def __init__(self, name, factory) -> None:
        self.name = name
        self._factory = factory

    def load(self):
        return self._factory


class _FailingLoadEntryPoint:
    name = "broken"

    def __init__(self, name: str) -> None:
        self.name = name

    def load(self):
        raise RuntimeError("load failed")
