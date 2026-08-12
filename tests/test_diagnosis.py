from src.config.constants import AssetType, HealthStatus
from src.config.paths import MODELS_DIR
from src.data.synthetic_generator import make_asset_data
from src.diagnosis import train_diagnostics, get_asset_health


def test_diagnosis_pipeline():
    """
    Test the complete diagnosis pipeline: data generation → model training → prediction.
    """

    df = make_asset_data("Bridge-TEST", AssetType.BRIDGE, age=25.0, days=200,)
    result = train_diagnostics(df, "test_diag.pkl",)

    assert result["accuracy"] >= 0
    assert result["path"].exists()

    sample = {
        "temperature_c": 35.2,
        "vibration_hz": 24.5,
        "structural_strain": 280.4,
        "corrosion_index": 0.45,
    }

    status, score = get_asset_health(
        sample,
        MODELS_DIR / "test_diag.pkl",
    )

    assert isinstance(status, HealthStatus)
    assert 0 <= score <= 100

    result["path"].unlink()