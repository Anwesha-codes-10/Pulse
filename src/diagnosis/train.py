import pickle

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from src.config.paths import MODELS_DIR


FEATURES = [
    "temperature_c",
    "vibration_hz",
    "structural_strain",
    "corrosion_index",
]


def train_diagnostics(df, out_file="diag_model.pkl"):
    """
    Train an XGBoost model to detect structural anomalies.

    """

    X = df[FEATURES]
    y = df["is_anomaly"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )


    clf = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.05,
        random_state=42,
        eval_metric="logloss",
    )

    clf.fit(X_tr, y_tr)

    accuracy = clf.score(X_te, y_te)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODELS_DIR / out_file

    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"Model trained successfully | Accuracy: {accuracy:.2%}")
    print(f"Model saved to: {model_path}")

    return {
        "accuracy": accuracy,
        "path": model_path,
    }