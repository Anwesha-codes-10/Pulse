from src.config.constants import AssetType
from src.config.paths import MODELS_DIR
from src.data.synthetic_generator import make_asset_data
from src.forecasting import train_forecaster, get_risk_forecast


def test_forecasting_pipeline():
    """
    Test the complete forecasting pipeline: data generation → model training → risk prediction.
    """

    df = make_asset_data("Bridge-FC-TEST", AssetType.BRIDGE, age=30.0, days=150,)

    result = train_forecaster(df, "test_forecast.pkl",)
    assert result["path"].exists()

    sample = {
        "temperature_c": 28.0,
        "vibration_hz": 13.5,
        "structural_strain": 160.0,
        "corrosion_index": 0.2,
    }

    projections = get_risk_forecast(
        sample,
        MODELS_DIR / "test_forecast.pkl",
    )

    assert isinstance(projections, dict)
    assert 7 in projections
    assert 30 in projections
    assert 90 in projections

    for risk in projections.values():
        assert 0 <= risk <= 100

    result["path"].unlink()