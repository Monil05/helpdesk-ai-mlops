from app.database import create_ticket, list_tickets, update_ticket_status


def test_create_list_and_update_ticket(tmp_path):
    db = tmp_path / "tickets.db"
    ticket = create_ticket("Wi-Fi", "Cannot connect", "Access", 0.91, "High", path=db)
    assert ticket["ticket_id"].startswith("HD-")
    assert ticket["status"] == "New"
    assert list_tickets(path=db)[0]["title"] == "Wi-Fi"
    assert update_ticket_status(ticket["ticket_id"], "Resolved", path=db)
    assert list_tickets(path=db)[0]["status"] == "Resolved"


def test_invalid_status_is_rejected(tmp_path):
    try:
        update_ticket_status("missing", "Closed", path=tmp_path / "tickets.db")
    except ValueError as exc:
        assert "Status" in str(exc)
    else:
        raise AssertionError("Expected invalid status to be rejected")
