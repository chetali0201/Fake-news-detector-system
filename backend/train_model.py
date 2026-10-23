"""Train Logistic Regression and Passive Aggressive models, pick the best, save everything."""
import argparse
import json
from datetime import datetime
from pathlib import Path

import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.pipeline import Pipeline

from evaluate_model import MODELS_DIR, evaluate
from preprocess import load_and_clean, prepare_splits


def build_models(small: bool) -> dict:
    # A Pipeline fits TF-IDF on training data only, so no test/validation leakage.
    def tfidf():
        return TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_df=0.7,
                               min_df=1 if small else 3, sublinear_tf=True, max_features=200000)
    return {
        "Logistic Regression": Pipeline([("tfidf", tfidf()),
                                         ("clf", LogisticRegression(max_iter=1000))]),
        # PAC has no probabilities; calibration makes the confidence score meaningful.
        "Passive Aggressive": Pipeline([("tfidf", tfidf()),
                                        ("clf", CalibratedClassifierCV(
                                            PassiveAggressiveClassifier(max_iter=50, random_state=42), cv=3))]),
    }


def main():
    default = Path(__file__).parents[1] / "data"
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(default), help="CSV file or data folder")
    args = ap.parse_args()

    df = load_and_clean(args.data)
    (X_tr, y_tr), (X_val, y_val), (X_te, y_te) = prepare_splits(df)
    results, fitted = {}, {}
    for name, model in build_models(small=len(df) < 1000).items():
        model.fit(X_tr, y_tr)
        results[name] = {"validation": evaluate(model, X_val, y_val), "test": evaluate(model, X_te, y_te)}
        fitted[name] = model
        print(f"{name}: val F1={results[name]['validation']['f1']:.4f}")

    best = max(results, key=lambda n: results[n]["validation"]["f1"])  # chosen on validation only
    print(f"Selected model: {best}")
    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(fitted[best], MODELS_DIR / "model_pipeline.joblib")
    joblib.dump(fitted[best].named_steps["tfidf"], MODELS_DIR / "tfidf_vectorizer.joblib")
    metrics = {"selected_model": best, "positive_class": "FAKE", "models": results,
               "selected_test": results[best]["test"],
               "dataset": {"rows": len(df), "train": len(X_tr), "validation": len(X_val), "test": len(X_te),
                           "source": Path(args.data).name,
                           "is_sample": "sample" in Path(args.data).name.lower()},
               "trained_at": datetime.now().isoformat(timespec="seconds")}
    (MODELS_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Test metrics:", json.dumps(results[best]["test"], indent=2))


if __name__ == "__main__":
    main()
