import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_receive_webhook():
    payload = {"test": "data"}
    body = json.dumps(payload).encode()

    with patch("builtins.print") as mock_print:
        response = client.post("/api/v1/frameio/webhook", content=body)

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    mock_print.assert_called_once_with(payload)
