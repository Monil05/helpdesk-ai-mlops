"""Train and evaluate the TF-IDF / logistic regression ticket classifier."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "all_tickets_processed_improved_v3.csv"
MODEL_PATH = ROOT / "models" / "ticket_classifier.joblib"
METADATA_PATH = ROOT / "models" / "model_metadata.json"
RANDOM_SEED = 42


def main() -> None:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Training CSV not found: {DATA_PATH}")

    frame = pd.read_csv(DATA_PATH)
    required = {"Document", "Topic_group"}
    if not required.issubset(frame.columns):
        raise ValueError(
            f"Expected columns {sorted(required)}, found {list(frame.columns)}"
        )

    frame = frame[["Document", "Topic_group"]].copy()
    frame["Document"] = frame["Document"].fillna("").astype(str).str.strip()
    frame["Topic_group"] = frame["Topic_group"].fillna("").astype(str).str.strip()
    frame = frame[(frame["Document"] != "") & (frame["Topic_group"] != "")]
    frame = frame.drop_duplicates(subset=["Document", "Topic_group"])
    if frame["Topic_group"].nunique() < 2:
        raise ValueError("At least two categories are required to train a classifier.")
    if frame["Topic_group"].value_counts().min() < 2:
        raise ValueError("Every category needs at least two examples for stratified splitting.")

    x_train, x_test, y_train, y_test = train_test_split(
        frame["Document"],
        frame["Topic_group"],
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=frame["Topic_group"],
    )
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=30000)),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    labels = sorted(frame["Topic_group"].unique().tolist())
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, predictions, average="weighted", zero_division=0
    )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    metadata = {
        "model_name": "HelpDesk AI Ticket Classifier",
        "algorithm": "TF-IDF (unigrams and bigrams) + Logistic Regression",
        "dataset_file": DATA_PATH.name,
        "dataset_source": "Not recorded in the workspace; provenance and license unverified",
        "dataset_license": "Unknown; confirm with the dataset provider before redistribution",
        "rows_in_csv": int(len(pd.read_csv(DATA_PATH, usecols=["Document"]))),
        "rows_used_after_cleaning": int(len(frame)),
        "rows_removed": int(len(pd.read_csv(DATA_PATH, usecols=["Document"])) - len(frame)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "random_seed": RANDOM_SEED,
        "test_size": 0.2,
        "categories": labels,
        "class_distribution": {
            str(label): int(count) for label, count in frame["Topic_group"].value_counts().items()
        },
        "metrics": {
            "accuracy": float(accuracy_score(y_test, predictions)),
            "precision_weighted": float(precision),
            "recall_weighted": float(recall),
            "f1_weighted": float(f1),
        },
        "classification_report": classification_report(
            y_test, predictions, output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=labels).tolist(),
        "confusion_matrix_labels": labels,
        "trained_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps({"model": str(MODEL_PATH), "metadata": str(METADATA_PATH), **metadata["metrics"]}, indent=2))


if __name__ == "__main__":
    main()
