"""Load the trained classifier once and return categories with confidence."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib


@lru_cache(maxsize=1)
def load_model(model_path: str | None = None) -> Any:
    path = Path(model_path or os.getenv("MODEL_PATH", "models/ticket_classifier.joblib"))
    if not path.is_file():
        raise FileNotFoundError(
            f"Trained model not found at {path}. Run `python -m ml.train` first."
        )
    return joblib.load(path)


def predict(text: str, model: Any | None = None) -> tuple[str, float]:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Ticket description cannot be empty.")
    pipeline = model if model is not None else load_model()
    category = str(pipeline.predict([cleaned])[0])
    probabilities = pipeline.predict_proba([cleaned])[0]
    confidence = float(max(probabilities))
    return category, confidence
