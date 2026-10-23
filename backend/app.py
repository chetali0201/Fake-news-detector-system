
"""Flask API for the Fake News Detector.
Loads the trained model at startup and serves predictions.
"""

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

# Allowed frontend origins
DEFAULT_CORS_ORIGINS = [
    "https://fake-news-detector-system-rose.vercel.app",
    "https://fake-news-detector-system-ictp2wexq-chetali202.vercel.app",
    "http://localhost:5173",
]

# Optionally override allowed origins using a comma-separated
# CORS_ORIGINS environment variable on Render.
cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        ",".join(DEFAULT_CORS_ORIGINS),
    ).split(",")
    if origin.strip()
]

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": cors_origins,
        }
    },
)

# Load trained model and evaluation metrics once at startup
try:
    MODEL = joblib.load(MODELS_DIR / "model_pipeline.joblib")
    METRICS = json.loads(
        (MODELS_DIR / "metrics.json").read_text(encoding="utf-8")
    )
    print("Model loaded successfully.")

except FileNotFoundError as exc:
    MODEL = None
    METRICS = None
    print(f"Model or metrics file not found: {exc}")

except Exception as exc:
    MODEL = None
    METRICS = None
    print(f"Could not load model: {exc}")

DISCLAIMER = (
    "This is a machine learning prediction based on writing patterns "
    "in the training data. It is not proof that a claim is true or false."
)


@app.get("/")
def home():
    return jsonify(
        service="Fake News Detector API",
        status="ok",
        health_endpoint="/api/health",
    )


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        model_loaded=MODEL is not None,
    )


@app.post("/api/predict")
def predict():
    if MODEL is None:
        return jsonify(
            error="Model is not loaded. Check the server logs."
        ), 503

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        return jsonify(
            error='Send JSON like {"text": "Your news article here"}.'
        ), 400

    text = data["text"].strip()

    if not text:
        return jsonify(
            error="Please enter a headline or article."
        ), 400

    if len(text) > MAX_CHARS:
        return jsonify(
            error=f"Text is too long (maximum {MAX_CHARS} characters)."
        ), 413

    cleaned = clean_text(text)

    if len(cleaned.split()) < MIN_WORDS:
        return jsonify(
            error=f"Please enter at least {MIN_WORDS} words."
        ), 400

    try:
        probabilities = MODEL.predict_proba([cleaned])[0]
        probs = {
            label: float(probability)
            for label, probability in zip(MODEL.classes_, probabilities)
        }

        label = max(probs, key=probs.get)

        selected_model = (
            METRICS.get("selected_model", "Unknown")
            if METRICS
            else "Unknown"
        )

        return jsonify(
            label=str(label),
            confidence=round(probs[label], 4),
            probabilities={
                key: round(value, 4)
                for key, value in probs.items()
            },
            model=selected_model,
            disclaimer=DISCLAIMER,
        )

    except Exception as exc:
        app.logger.exception("Prediction failed")
        return jsonify(
            error="Prediction failed. Please try again."
        ), 500


@app.get("/api/metrics")
def metrics():
    if METRICS is None:
        return jsonify(
            error="Metrics are unavailable. Check the server logs."
        ), 503

    return jsonify(METRICS)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )
