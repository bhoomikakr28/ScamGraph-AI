"""Load and use the trained ScamGraph AI TF-IDF + Logistic Regression model."""

from functools import lru_cache
from pathlib import Path

import joblib

from backend.nlp.preprocessing import preprocess_text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "backend" / "models"
MODEL_PATH = MODEL_DIR / "scam_classifier.joblib"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"


@lru_cache(maxsize=1)
def _load_artifacts() -> tuple:
    """Load the saved vectorizer and classifier or raise a clear developer error."""
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        raise FileNotFoundError(
            "Model artifacts are missing. Train the model first using: python -m backend.ml.train"
        )

    vectorizer = joblib.load(VECTORIZER_PATH)
    classifier = joblib.load(MODEL_PATH)
    return vectorizer, classifier


def predict_scam(text: str) -> dict:
    """Return the real prediction payload from the trained artifacts.

    Returns:
        {
            "prediction": "scam" | "legitimate",
            "scam_probability": float,
            "safe_probability": float,
        }
    """
    vectorizer, classifier = _load_artifacts()

    clean_text = preprocess_text(text)
    features = vectorizer.transform([clean_text])
    probabilities = classifier.predict_proba(features)[0]

    # classes_ order is [0, 1] when sklearn uses labels 0 and 1.
    labels = list(classifier.classes_)
    if 1 in labels:
        scam_index = labels.index(1)
    else:
        scam_index = 1

    if 0 in labels:
        safe_index = labels.index(0)
    else:
        safe_index = 0

    scam_probability = float(probabilities[scam_index])
    safe_probability = float(probabilities[safe_index])
    prediction_value = int(classifier.predict(features)[0])
    prediction = "scam" if prediction_value == 1 else "legitimate"

    return {
        "prediction": prediction,
        "scam_probability": scam_probability,
        "safe_probability": safe_probability,
    }
