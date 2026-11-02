"""Application workflows independent of Streamlit."""

from __future__ import annotations

from time import perf_counter
from typing import Any

from app import database, metrics
from app.classifier import predict


def classify_ticket(description: str, model: Any | None = None) -> tuple[str, float]:
    started = perf_counter()
    try:
        category, confidence = predict(description, model=model)
        metrics.PREDICTIONS.inc()
        metrics.PREDICTIONS_BY_CATEGORY.labels(category=category).inc()
        return category, confidence
    except Exception:
        metrics.PREDICTION_ERRORS.inc()
        raise
    finally:
        metrics.PREDICTION_LATENCY.observe(perf_counter() - started)


def submit_ticket(
    title: str,
    description: str,
    priority: str,
    model: Any | None = None,
    db_path: str | None = None,
) -> dict:
    if not title.strip():
        raise ValueError("Ticket title cannot be empty.")
    if not description.strip():
        raise ValueError("Ticket description cannot be empty.")
    if priority not in {"Low", "Medium", "High"}:
        raise ValueError("Priority must be Low, Medium or High.")
    category, confidence = classify_ticket(description, model=model)
    ticket = database.create_ticket(
        title, description, category, confidence, priority, path=db_path
    )
    metrics.TICKETS_SUBMITTED.inc()
    metrics.refresh_ticket_gauges(database.list_tickets(path=db_path))
    return ticket
