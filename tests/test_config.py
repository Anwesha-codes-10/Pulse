from src.config import settings, AssetType


def test_settings():
    assert settings.PROJECT_NAME == "Pulse"


def test_asset_type():
    assert AssetType.BRIDGE.value == "Bridge"


if __name__ == "__main__":
    test_settings()
    test_asset_type()
    print("✅ All configuration tests passed.")