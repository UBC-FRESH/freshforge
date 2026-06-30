"""Provider registry and metadata tests."""

import pytest

from freshforge.providers import (
    ExampleProvider,
    NodeTypeMetadata,
    ProviderMetadata,
    ProviderRegistry,
    default_provider_registry,
    parse_provider_reference,
)


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
    registry = default_provider_registry()

    resolution = registry.resolve("freshforge.example.load_inventory")

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
    registry = default_provider_registry()

    assert [provider.id for provider in registry.list()] == ["freshforge.example"]
