"""
Pulse Data Validator Automation Test Suite.

Verifies structural schema gates, data quality tolerances, type checking loops,
and strict vs non-strict report configurations.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.validator import PulseDataValidator, ValidationReport


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Provides a baseline, healthy dataset mirroring typical production asset parameters."""
    return pd.DataFrame({
        "asset_id": ["Bridge-12", "Road-45"],
        "age_years": [42.0, 5.2],
        "timestamp": pd.to_datetime(["2026-07-29", "2026-07-30"])
    })


def test_validate_empty_dataframe_throws():
    """Confirms empty dataframes cause an immediate structural halt with a clear error message."""
    with pytest.raises(ValueError, match="Dataframe contains zero rows"):
        PulseDataValidator.validate_not_empty(pd.DataFrame())


def test_validate_columns_detects_missing_required_fields(sample_df):
    """Verifies that missing expected columns throw explicit schema validation exceptions."""
    required = ["asset_id", "vibration_sensor_hz"]
    with pytest.raises(ValueError, match="Schema validation failed: Missing fields"):
        PulseDataValidator.validate_columns(sample_df, required)


def test_validate_columns_ignores_empty_or_null_schemas(sample_df):
    """Verifies that passing None or an empty list to column checks returns True immediately."""
    assert PulseDataValidator.validate_columns(sample_df, None) is True
    assert PulseDataValidator.validate_columns(sample_df, []) is True


def test_validate_missing_values_strict_enforcement(sample_df):
    """Confirms that strict missing value checks throw an error when null bounds are breached."""
    corrupt_df = sample_df.copy()
    corrupt_df.loc[0, "age_years"] = np.nan
    
    # 1 row missing out of 2 equals a 50% missing ratio, breaching a 10% threshold limit
    with pytest.raises(ValueError, match="Data quality check failed: Fields exceeded threshold"):
        PulseDataValidator.validate_missing_values(corrupt_df, threshold_percent=0.10, strict=True)


def test_validate_missing_values_non_strict_warning(sample_df):
    """Verifies that non-strict missing checks report failures gracefully via dataclass warnings."""
    corrupt_df = sample_df.copy()
    corrupt_df.loc[0, "age_years"] = np.nan
    
    report = PulseDataValidator.validate_missing_values(corrupt_df, threshold_percent=0.10, strict=False)
    assert isinstance(report, ValidationReport)
    assert report.passed is False
    assert len(report.warnings) == 1
    assert "age_years" in report.metrics["null_breached_fields"]


def test_validate_duplicates_strict_enforcement():
    """Confirms duplicate rows cause an immediate pipeline failure under strict configuration."""
    duplicate_df = pd.DataFrame({
        "asset_id": ["Bridge-12", "Bridge-12"],
        "metric": [10.5, 10.5]
    })
    with pytest.raises(ValueError, match="Data validation failed: Duplicate entries caught"):
        PulseDataValidator.validate_duplicates(duplicate_df, strict=True)


def test_validate_duplicates_non_strict_metrics():
    """Verifies that non-strict mode records duplicate frequencies inside metrics logs cleanly."""
    duplicate_df = pd.DataFrame({
        "asset_id": ["Bridge-12", "Bridge-12"],
        "metric": [10.5, 10.5]
    })
    report = PulseDataValidator.validate_duplicates(duplicate_df, strict=False)
    assert isinstance(report, ValidationReport)
    assert report.passed is False
    assert len(report.errors) == 1
    assert report.metrics["duplicate_statistics"]["duplicate_count"] == 1


def test_validate_datatypes_identifies_type_violations(sample_df):
    """Confirms data type checking catches logical category rule mismatches."""
    rules = {"asset_id": "numeric"}  # asset_id contains string categories
    with pytest.raises(TypeError, match="must match type 'numeric'"):
        PulseDataValidator.validate_datatypes(sample_df, rules)


def test_validate_datatypes_flags_invalid_rules(sample_df):
    """Confirms that providing an unsupported data type token throws a clear parameter exception."""
    invalid_rules = {"age_years": "banana"}
    with pytest.raises(ValueError, match="Invalid validation datatype target rule: 'banana'"):
        PulseDataValidator.validate_datatypes(sample_df, invalid_rules)


def test_comprehensive_validation_happy_path(sample_df):
    """Validates that a healthy dataframe clears the complete integrated validation pipeline seamlessly."""
    rules = {"asset_id": "string", "age_years": "numeric", "timestamp": "datetime"}
    report = PulseDataValidator.validate(
        df=sample_df,
        required_columns=["asset_id", "age_years"],
        expected_types=rules,
        unique_subset=["asset_id"]
    )
    assert isinstance(report, ValidationReport)
    assert report.passed is True
    assert len(report.errors) == 0
    assert len(report.warnings) == 0
    assert "null_breached_fields" in report.metrics
    assert "duplicate_statistics" in report.metrics
