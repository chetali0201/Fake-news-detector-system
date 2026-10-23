"""Flask API: loads the trained model once at startup and serves predictions."""
import json
import os
from pathlib import Path

import joblib
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from preprocess import clean_text

load_dotenv()
MODELS_DIR = Path(__file__).parent / "models"
MAX_CHARS = int(os.getenv("MAX_INPUT_CHARS", "20000"))
MIN_WORDS = 3

app = Flask(__name__)
CORS(app, origins=[o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")])

# Load once, not per request
try:
    MODEL = joblib.load(MODELS_DIR / "model_pipeline.joblib")
    METRICS = json.loads((MODELS_DIR / "metrics.json").read_text())
except FileNotFoundError:
    MODEL, METRICS = None, None

DISCLAIMER = ("This is a machine learning prediction based on writing patterns in the training data. "
              "It is not proof that a claim is true or false.")


@app.get("/api/health")
def health():
    return jsonify(status="ok", model_loaded=MODEL is not None)


@app.post("/api/predict")
def predict():
    if MODEL is None:
        return jsonify(error="Model not trained yet. Run `python train_model.py` first."), 503
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        return jsonify(error="Send JSON like {\"text\": \"...\"}."), 400
    text = data["text"].strip()
    if not text:
        return jsonify(error="Please enter a headline or article."), 400
    if len(text) > MAX_CHARS:
        return jsonify(error=f"Text is too long (max {MAX_CHARS} characters)."), 413
    cleaned = clean_text(text)
    if len(cleaned.split()) < MIN_WORDS:
        return jsonify(error=f"Please enter at least {MIN_WORDS} words."), 400
    proba = MODEL.predict_proba([cleaned])[0]
    probs = dict(zip(MODEL.classes_, (float(p) for p in proba)))
    label = max(probs, key=probs.get)
    return jsonify(label=label, confidence=round(probs[label], 4),
                   probabilities={k: round(v, 4) for k, v in probs.items()},
                   model=METRICS["selected_model"], disclaimer=DISCLAIMER)


@app.get("/api/metrics")
def metrics():
    if METRICS is None:
        return jsonify(error="No metrics found. Train the model first."), 503
    return jsonify(METRICS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
