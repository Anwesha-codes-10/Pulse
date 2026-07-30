"""
Unit tests for PulseDataLoader.
"""

import pandas as pd
import pytest

from src.data.loader import PulseDataLoader


def test_save_and_load_csv():
    """Verify a DataFrame can be saved and loaded successfully."""

    df = pd.DataFrame(
        {
            "temperature": [36.5, 37.2],
            "pressure": [101.2, 100.8],
        }
    )

    path = PulseDataLoader.save_csv(
        df,
        "test_loader.csv",
        category="processed",
    )

    loaded_df = PulseDataLoader.load_csv(
        "test_loader.csv",
        category="processed",
    )

    assert loaded_df.shape == df.shape
    assert list(loaded_df.columns) == list(df.columns)

    path.unlink()


def test_invalid_category():
    """Invalid category should raise ValueError."""

    with pytest.raises(ValueError):
        PulseDataLoader.load_csv(
            "test.csv",
            category="invalid",
        )


def test_invalid_filename():
    """Non-CSV filename should raise ValueError."""

    with pytest.raises(ValueError):
        PulseDataLoader.load_csv(
            "dataset.txt",
            category="raw",
        )


def test_missing_file():
    """Missing CSV should raise FileNotFoundError."""

    with pytest.raises(FileNotFoundError):
        PulseDataLoader.load_csv(
            "does_not_exist.csv",
            category="raw",
        )