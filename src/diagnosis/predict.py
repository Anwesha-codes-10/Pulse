import pickle

import pandas as pd

from src.config.constants import HealthStatus
from src.config.paths import MODELS_DIR


FEATURES = [
    "temperature_c",
    "vibration_hz",
    "structural_strain",
    "corrosion_index",
]


def get_asset_health(data, model_file=None):
    """
    Predict the health status of an asset using the trained diagnostic anomaly-detection model.

    """

    if model_file is None:
        model_file = MODELS_DIR / "diag_model.pkl"

    try:
        with open(model_file, "rb") as f:
            clf = pickle.load(f)
    except FileNotFoundError:
        return HealthStatus.HEALTHY, 100.0


    X = pd.DataFrame(
        [
            {
                key: float(data.get(key, 0))
                for key in FEATURES
            }
        ]
    )

    pred = clf.predict(X)[0]
    prob = clf.predict_proba(X)[0][1]
    score = round((1 - prob) * 100, 1)

    
    if pred == 1:
        status = HealthStatus.CRITICAL
    elif score < 75:
        status = HealthStatus.WARNING
    else:
        status = HealthStatus.HEALTHY

    return status, score