"""Utility helpers for model loading, artifact creation, and Phase 1 compatibility."""

from pathlib import Path


MODEL_DIR = Path("backend/models")


def ensure_model_directory() -> Path:
    """Create the model artifact directory if it does not exist."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    return MODEL_DIR
