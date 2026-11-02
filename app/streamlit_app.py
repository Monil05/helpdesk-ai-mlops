"""Streamlit user interface for HelpDesk AI."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from app import database, metrics
from app.classifier import load_model
from app.logic import submit_ticket

ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "models" / "model_metadata.json"
STATUSES = ["New", "In Progress", "Resolved"]
PRIORITIES = ["Low", "Medium", "High"]


@st.cache_resource
def application_resources():
    metrics.start_metrics_server()
    return load_model()


def show_submit_page(model) -> None:
    st.title("Submit a support ticket")
    st.write("Describe the issue and HelpDesk AI will suggest a category.")
    with st.form("ticket_form", clear_on_submit=True):
        title = st.text_input("Ticket title", max_chars=160)
        description = st.text_area("Describe the issue", height=160, max_chars=10000)
        priority = st.selectbox("Priority", PRIORITIES, index=1)
        submitted = st.form_submit_button("Submit ticket", type="primary")
    if submitted:
        try:
            ticket = submit_ticket(title, description, priority, model=model)
            st.session_state["last_ticket"] = ticket
            st.success("Ticket submitted.")
        except (ValueError, OSError) as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Could not submit ticket: {exc}")
    ticket = st.session_state.get("last_ticket")
    if ticket:
        st.info(
            f"Ticket **{ticket['ticket_id']}** · Category **{ticket['category']}** · "
            f"Confidence **{ticket['confidence']:.1%}**"
        )


def show_dashboard() -> None:
    st.title("Ticket dashboard")
    tickets = database.list_tickets()
    metrics.refresh_ticket_gauges(tickets)
    counts = {status: sum(t["status"] == status for t in tickets) for status in STATUSES}
    cols = st.columns(4)
    cols[0].metric("Total tickets", len(tickets))
    cols[1].metric("New", counts["New"])
    cols[2].metric("In progress", counts["In Progress"])
    cols[3].metric("Resolved", counts["Resolved"])

    frame = pd.DataFrame(tickets)
    if frame.empty:
        st.caption("No tickets yet. Submit one to get started.")
        return
    categories = sorted(frame["category"].unique().tolist())
    a, b, c = st.columns(3)
    category_filter = a.multiselect("Category", categories)
    priority_filter = b.multiselect("Priority", PRIORITIES)
    status_filter = c.multiselect("Status", STATUSES)
    search = st.text_input("Search tickets", placeholder="Search title or ticket ID")
    filtered = frame.copy()
    if category_filter:
        filtered = filtered[filtered["category"].isin(category_filter)]
    if priority_filter:
        filtered = filtered[filtered["priority"].isin(priority_filter)]
    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]
    if search.strip():
        needle = search.strip().casefold()
        filtered = filtered[
            filtered["title"].str.casefold().str.contains(needle, regex=False)
            | filtered["ticket_id"].str.casefold().str.contains(needle, regex=False)
        ]
    display = filtered[["ticket_id", "title", "category", "priority", "status", "created_at"]].copy()
    display["created_at"] = pd.to_datetime(display["created_at"], utc=True).dt.strftime(
        "%Y-%m-%d %H:%M UTC"
    )
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.subheader("Update ticket status")
    options = {f"{row['ticket_id']} — {row['title']}": row["ticket_id"] for row in tickets}
    with st.form("status_form"):
        selected = st.selectbox("Ticket", list(options))
        new_status = st.selectbox("New status", STATUSES)
        update = st.form_submit_button("Update status")
    if update:
        if database.update_ticket_status(options[selected], new_status):
            st.success(f"{options[selected]} updated to {new_status}.")
            st.rerun()
        st.error("Ticket was not found.")


def show_model_info() -> None:
    st.title("Model information")
    if not METADATA_PATH.is_file():
        st.warning("Model metadata is missing. Train the model with `python -m ml.train`.")
        return
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    st.write(f"**Model:** {metadata['model_name']}")
    st.write(f"**Algorithm:** {metadata['algorithm']}")
    st.write(
        f"**Training data:** {metadata['dataset_file']} · "
        f"{metadata['rows_used_after_cleaning']:,} rows after cleaning"
    )
    st.caption(
        f"Source: {metadata['dataset_source']}. License: {metadata['dataset_license']}."
    )
    st.subheader("Holdout evaluation")
    st.json(metadata["metrics"])
    with st.expander("Confusion matrix"):
        labels = metadata["confusion_matrix_labels"]
        matrix = pd.DataFrame(
            metadata["confusion_matrix"], index=labels, columns=labels
        )
        st.dataframe(matrix, use_container_width=True)
    st.subheader("Training class distribution")
    st.bar_chart(pd.Series(metadata["class_distribution"], name="Tickets"))


def main() -> None:
    st.set_page_config(page_title="HelpDesk AI", page_icon="🎫", layout="wide")
    st.sidebar.title("HelpDesk AI")
    page = st.sidebar.radio("Navigate", ["Submit Ticket", "Ticket Dashboard", "Model Information"])
    try:
        model = application_resources()
    except Exception as exc:
        st.error(f"The trained model could not be loaded: {exc}")
        st.stop()
    if page == "Submit Ticket":
        show_submit_page(model)
    elif page == "Ticket Dashboard":
        show_dashboard()
    else:
        show_model_info()


if __name__ == "__main__":
    main()
