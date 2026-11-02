from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.database import list_tickets
from app.logic import submit_ticket


def test_submit_ticket_persists_prediction(tmp_path):
    model = Pipeline(
        [("tfidf", TfidfVectorizer()), ("classifier", LogisticRegression(random_state=1))]
    )
    model.fit(["wifi network", "broken laptop"], ["Access", "Hardware"])
    db = tmp_path / "tickets.db"
    ticket = submit_ticket("Wi-Fi", "Wifi network is unavailable", "Medium", model=model, db_path=str(db))
    saved = list_tickets(path=db)
    assert len(saved) == 1
    assert ticket["category"] == saved[0]["category"]
    assert ticket["confidence"] == saved[0]["confidence"]
