"""
Tests for the Pulse Asset Registry.

"""

import pytest
from src.config.constants import AssetType 
from src.digital_twin import InfrastructureAsset

def test_asset_registry_creates_asset() -> None:
    """Verify that an infrascture asset can be registered"""
    asset = InfrastructureAsset(
        asset_id="Bridge-12",
        asset_type=AssetType.BRIDGE,
        location="Bhubaneswar",
        metadata={"category": "urban_bridge"},
    )


    assert asset.asset_id == "Bridge-12"
    assert asset.asset_type == AssetType.BRIDGE
    assert asset.location == "Bhubaneswar"
    assert asset.metadata["category"] == "urban_bridge" 

def test_asset_registry_immutable() -> None:
    """Verify that an infrascture asset is immutable"""
    asset = InfrastructureAsset(
        asset_id="Bridge-12",
        asset_type=AssetType.BRIDGE,
        location="Bhubaneswar",
        metadata={"category": "urban_bridge"},
    )

    with pytest.raises(AttributeError):
        asset.asset_id = "Bridge-13"


