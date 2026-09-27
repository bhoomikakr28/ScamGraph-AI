"""Train the Phase 1 baseline TF-IDF + Logistic Regression classifier.

This module intentionally contains only the model training logic and artifact saving.
The API never retrains when /api/analyze is called.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from backend.nlp.preprocessing import preprocess_text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "datasets" / "scam_messages.csv"
MODEL_DIR = PROJECT_ROOT / "backend" / "models"
MODEL_PATH = MODEL_DIR / "scam_classifier.joblib"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"


def validate_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate the existing dataset before training.

    Checks required columns, trims duplicate messages, removes null rows,
    and verifies label values are binary 0/1.
    """
    required_columns = {"text", "label", "scam_type"}
    missing = required_columns.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    frame = frame.dropna(subset=["text", "label", "scam_type"]).copy()
    frame = frame.drop_duplicates(subset=["text"], keep="first")
    frame = frame[frame["text"].astype(str).str.strip().ne("")]

    allowed_labels = {0, 1}
    invalid_labels = sorted(set(frame["label"].dropna().astype(int).unique()).difference(allowed_labels))
    if invalid_labels:
        raise ValueError(f"Dataset contains invalid label values: {invalid_labels}")

    frame = frame[frame["label"].astype(int).isin(allowed_labels)].copy()
    frame["label"] = frame["label"].astype(int)
    return frame


def train_model() -> dict:
    """Load dataset, validate it, preprocess, split, fit, evaluate, and save artifacts."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found: {DATASET_PATH}")

    frame = pd.read_csv(DATASET_PATH)
    print(f"Dataset size before validation: {len(frame)}")
    frame = validate_dataset(frame)
    print(f"Dataset size after validation: {len(frame)}")

    print("Class distribution:")
    print(frame["label"].value_counts().to_string())

    texts = frame["text"].map(preprocess_text)
    labels = frame["label"].astype(int).to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        stratify=labels,
        random_state=42,
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    classifier = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    classifier.fit(X_train_tfidf, y_train)

    predictions = classifier.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    matrix = confusion_matrix(y_test, predictions)

    roc_auc = None
    if len(set(y_test)) == 2:
        roc_auc = roc_auc_score(y_test, classifier.predict_proba(X_test_tfidf)[:, 1])

    print("Accuracy:", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1-score:", round(f1, 4))
    print("Confusion Matrix:")
    print(matrix)
    if roc_auc is not None:
        print("ROC-AUC:", round(roc_auc, 4))
    else:
        print("ROC-AUC: unavailable; both classes are not present in the test set.")

    joblib.dump(classifier, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    result = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": matrix.tolist(),
        "roc_auc": roc_auc,
    }
    print(f"Saved model: {MODEL_PATH}")
    print(f"Saved vectorizer: {VECTORIZER_PATH}")
    return result


if __name__ == "__main__":
    train_model()
