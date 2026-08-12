import pickle

import pandas as pd

from src.config.paths import MODELS_DIR


FEATURES = [
    "temperature_c",
    "vibration_hz",
    "structural_strain",
    "corrosion_index",
]


def get_risk_forecast(data, model_file=None):
    """
    Predict the asset's risk for different future time horizons.

    """

    if model_file is None:
        model_file = MODELS_DIR / "forecast_model.pkl"

    try:
        with open(model_file, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        return {7: 5.0, 30: 15.0,90: 30.0,}

    X = pd.DataFrame(
        [
            {
                key: float(data.get(key, 0))
                for key in FEATURES
            }
        ]
    )

    base_risk = float(model.predict(X)[0])
    risk_7 = round(min(100.0, max(0.0, base_risk * 1.05)), 1,)
    risk_30 = round(min(100.0, max(0.0, base_risk * 1.25)),1,)
    risk_90 = round(min(100.0, max(0.0, base_risk * 1.65)),1,)
    return {7: risk_7, 30: risk_30, 90: risk_90,}