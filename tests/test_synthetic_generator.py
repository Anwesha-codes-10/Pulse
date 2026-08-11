"""
Tests for the Data Generator

"""
import pandas as pd
from src.config.constants import AssetType
from src.data.synthetic_generator import make_asset_data

def test_generator_output_schema() -> None:
    df = make_asset_data("Bridge-12", AssetType.BRIDGE, 42.0, 365)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 365

    cols = {"timestamp", "asset_id", "temperature_c", "vibration_hz", "structural_strain", "corrosion_index", "is_anomaly"}
    assert cols.issubset(df.columns)

def test_generator_determinism() -> None:
    df1 = make_asset_data("Road-45", AssetType.ROAD_SEGMENT, 5.0, 100)
    df2 = make_asset_data("Road-45", AssetType.ROAD_SEGMENT, 5.0, 100)
    pd.testing.assert_frame_equal(df1, df2)

def test_trauma_injection() -> None:
    df = make_asset_data("Pipeline-A17", AssetType.PIPELINE, 15.0, 200)
    assert df.loc[180, "is_anomaly"] == 1
    assert df.loc[10, "is_anomaly"] == 0
