"""Small SQLite repository for helpdesk tickets."""

from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def database_path() -> Path:
    return Path(os.getenv("TICKET_DB_PATH", "data/tickets.db"))


def get_connection(path: str | Path | None = None) -> sqlite3.Connection:
    db_path = Path(path) if path is not None else database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(path: str | Path | None = None) -> None:
    with closing(get_connection(path)) as connection, connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                confidence REAL NOT NULL,
                priority TEXT NOT NULL CHECK(priority IN ('Low', 'Medium', 'High')),
                status TEXT NOT NULL CHECK(status IN ('New', 'In Progress', 'Resolved')),
                created_at TEXT NOT NULL
            )"""
        )


def create_ticket(
    title: str,
    description: str,
    category: str,
    confidence: float,
    priority: str,
    path: str | Path | None = None,
) -> dict[str, Any]:
    initialize_database(path)
    ticket = {
        "ticket_id": f"HD-{uuid.uuid4().hex[:10].upper()}",
        "title": title.strip(),
        "description": description.strip(),
        "category": category,
        "confidence": float(confidence),
        "priority": priority,
        "status": "New",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with closing(get_connection(path)) as connection, connection:
        connection.execute(
            """INSERT INTO tickets
               (ticket_id, title, description, category, confidence, priority, status, created_at)
               VALUES (:ticket_id, :title, :description, :category, :confidence, :priority,
                       :status, :created_at)""",
            ticket,
        )
    return ticket


def list_tickets(path: str | Path | None = None) -> list[dict[str, Any]]:
    initialize_database(path)
    with closing(get_connection(path)) as connection, connection:
        rows = connection.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC, ticket_id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def update_ticket_status(
    ticket_id: str, status: str, path: str | Path | None = None
) -> bool:
    if status not in {"New", "In Progress", "Resolved"}:
        raise ValueError("Status must be New, In Progress or Resolved.")
    initialize_database(path)
    with closing(get_connection(path)) as connection, connection:
        cursor = connection.execute(
            "UPDATE tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id)
        )
    return cursor.rowcount == 1
