"""Metric helpers; run `python evaluate_model.py [data_path]` to re-evaluate the saved model."""
import sys
from pathlib import Path

import joblib
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             precision_recall_fscore_support)

LABELS = ["FAKE", "REAL"]  # FAKE is treated as the positive class
MODELS_DIR = Path(__file__).parent / "models"


def evaluate(model, X, y) -> dict:
    pred = model.predict(X)
    p, r, f, _ = precision_recall_fscore_support(
        y, pred, pos_label="FAKE", average="binary", zero_division=0)
    return {"accuracy": float(accuracy_score(y, pred)), "precision": float(p),
            "recall": float(r), "f1": float(f),
            "confusion_matrix": confusion_matrix(y, pred, labels=LABELS).tolist()}


if __name__ == "__main__":
    from preprocess import load_and_clean, prepare_splits
    data = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "data"
    _, _, (X_test, y_test) = prepare_splits(load_and_clean(data))
    model = joblib.load(MODELS_DIR / "model_pipeline.joblib")
    print(classification_report(y_test, model.predict(X_test), zero_division=0))
    print(evaluate(model, X_test, y_test))
