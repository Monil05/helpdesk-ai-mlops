from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.classifier import predict


def test_classifier_returns_category_and_probability():
    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("classifier", LogisticRegression(random_state=1)),
        ]
    )
    model.fit(
        ["wifi network connection", "laptop hardware screen", "wifi cannot connect", "broken laptop screen"],
        ["Access", "Hardware", "Access", "Hardware"],
    )
    category, confidence = predict("wifi is not connecting", model=model)
    assert category == "Access"
    assert 0 <= confidence <= 1


def test_empty_description_is_rejected():
    try:
        predict("   ", model=object())
    except ValueError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError("Expected an empty description to be rejected")
