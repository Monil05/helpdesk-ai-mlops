"""Prometheus metrics for inference and ticket activity."""

from __future__ import annotations

import os
import threading
from collections import Counter

from prometheus_client import Counter as PromCounter
from prometheus_client import Gauge, Histogram, start_http_server

PREDICTIONS = PromCounter("helpdesk_predictions_total", "Ticket category predictions")
PREDICTIONS_BY_CATEGORY = PromCounter(
    "helpdesk_predictions_by_category_total",
    "Ticket predictions by predicted category",
    ["category"],
)
PREDICTION_ERRORS = PromCounter("helpdesk_prediction_errors_total", "Failed predictions")
PREDICTION_LATENCY = Histogram(
    "helpdesk_prediction_latency_seconds", "Time spent predicting a ticket category"
)
TICKETS_SUBMITTED = PromCounter("helpdesk_tickets_submitted_total", "Tickets saved")
TICKETS_BY_STATUS = Gauge("helpdesk_tickets_by_status", "Current ticket count by status", ["status"])

_metrics_lock = threading.Lock()
_server_started = False


def start_metrics_server() -> None:
    global _server_started
    with _metrics_lock:
        if not _server_started:
            start_http_server(int(os.getenv("METRICS_PORT", "8000")), addr="0.0.0.0")
            _server_started = True


def refresh_ticket_gauges(tickets: list[dict]) -> None:
    counts = Counter(ticket["status"] for ticket in tickets)
    for status in ("New", "In Progress", "Resolved"):
        TICKETS_BY_STATUS.labels(status=status).set(counts[status])
