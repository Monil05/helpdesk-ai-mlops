"""Start metrics independently of the first Streamlit browser session."""

from __future__ import annotations

import sys

from app.metrics import start_metrics_server


def main() -> None:
    start_metrics_server()
    sys.argv = [
        "streamlit",
        "run",
        "app/streamlit_app.py",
        "--server.address=0.0.0.0",
        "--server.port=8501",
        "--server.headless=true",
    ]
    from streamlit.web.cli import main as streamlit_main

    streamlit_main()


if __name__ == "__main__":
    main()
