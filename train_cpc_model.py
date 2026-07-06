"""Train a baseline CPC forecasting model on synthetic data."""

from __future__ import annotations

from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_cpc_data.csv"
MODEL_DIR = ROOT / "src" / "models"

NUMERIC_FEATURES = [
    "transit_days",
    "port_dwell_days",
    "base_freight",
    "fuel_surcharge",
    "detention_cost",
    "demurrage_cost",
    "storage_cost",
    "chassis_cost",
    "accessorial_cost",
]
CATEGORICAL_FEATURES = ["origin_port", "destination_port", "carrier", "program", "load_type"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run src/generate_synthetic_data.py first.")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    X = df[FEATURES]
    y = df["total_transportation_cost"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    cpc_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)),
        ]
    )
    cpc_model.fit(X_train, y_train)
    preds = cpc_model.predict(X_test)

    metrics = {
        "mae": round(mean_absolute_error(y_test, preds), 2),
        "r2": round(r2_score(y_test, preds), 4),
    }

    joblib.dump(cpc_model, MODEL_DIR / "cpc_forecast_model.joblib")

    y_cls = df["cpc_escalation_flag"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_cls, test_size=0.2, random_state=42, stratify=y_cls)
    risk_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)),
        ]
    )
    risk_model.fit(X_train, y_train)
    cls_preds = risk_model.predict(X_test)
    joblib.dump(risk_model, MODEL_DIR / "lane_risk_model.joblib")

    with open(MODEL_DIR / "model_metrics.json", "w", encoding="utf-8") as f:
        json.dump({"cpc_forecast": metrics, "risk_model": classification_report(y_test, cls_preds, output_dict=True)}, f, indent=2)

    print("CPC forecast metrics:", metrics)
    print("Saved models to", MODEL_DIR)


if __name__ == "__main__":
    main()
