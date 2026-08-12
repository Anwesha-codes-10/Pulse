import pickle

from xgboost import XGBRegressor

from src.config.paths import MODELS_DIR


FEATURES = [
    "temperature_c",
    "vibration_hz",
    "structural_strain",
    "corrosion_index",
]


def train_forecaster(df, out_file="forecast_model.pkl"):
    """
    Train an XGBoost regression model to estimate future asset risk.

    """

    X = df[FEATURES]

    y = (df["corrosion_index"] * 40) + (
        df["structural_strain"] * 0.1
    )

    y = y.clip(0, 100)

    model = XGBRegressor(
        n_estimators=80,
        max_depth=4,
        learning_rate=0.08,
        random_state=42,
    )

    model.fit(X, y)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODELS_DIR / out_file

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("Forecasting model trained successfully.")
    print(f"Model saved to: {model_path}")

    return {
        "path": model_path,
    }