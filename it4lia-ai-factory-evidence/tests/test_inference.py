import sys
from pathlib import Path

from fastapi.testclient import TestClient

ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARTIFACT_ROOT))

from src.inference_api import SentimentPrediction, create_app


class StubBackend:
    labels = {0: "negative", 1: "positive"}

    def predict(self, texts):
        assert texts == ["Questo servizio funziona bene"]
        return [
            SentimentPrediction(
                label="positive",
                score=0.91,
                class_id=1,
                backend="stub",
                latency_ms=1.2,
            )
        ]


def test_predict_endpoint_uses_injected_backend():
    app = create_app(backend=StubBackend())
    client = TestClient(app)

    response = client.post(
        "/predict",
        json={"texts": ["Questo servizio funziona bene"]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "predictions": [
            {
                "label": "positive",
                "score": 0.91,
                "class_id": 1,
                "backend": "stub",
                "latency_ms": 1.2,
            }
        ]
    }
