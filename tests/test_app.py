import hashlib
import hmac
import json
import time
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

WEBHOOK_SECRET = "test_secret"


def test_receive_webhook_with_valid_signature():
    timestamp = str(int(time.time()))
    payload = {"test": "data"}
    body = json.dumps(payload).encode()

    signature = hmac.new(
        key=WEBHOOK_SECRET.encode(),
        msg=f"{timestamp}:{body.decode()}".encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    with patch("src.app.main.FRAMEIO_WEBHOOK_SECRET", WEBHOOK_SECRET):
        with patch("builtins.print") as mock_print:
            response = client.post(
                "/api/v1/frameio/webhook",
                content=body,
                headers={
                    "x-frameio-signature": signature,
                    "x-frameio-timestamp": timestamp,
                },
            )

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    mock_print.assert_called_once_with(payload)


def test_receive_webhook_with_invalid_signature():
    timestamp = str(int(time.time()))
    payload = {"test": "data"}
    body = json.dumps(payload).encode()

    with patch("src.app.main.FRAMEIO_WEBHOOK_SECRET", WEBHOOK_SECRET):
        response = client.post(
            "/api/v1/frameio/webhook",
            content=body,
            headers={
                "x-frameio-signature": "invalid_signature",
                "x-frameio-timestamp": timestamp,
            },
        )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid signature."}


def test_receive_webhook_with_missing_headers():
    payload = {"test": "data"}
    body = json.dumps(payload).encode()

    with patch("src.app.main.FRAMEIO_WEBHOOK_SECRET", WEBHOOK_SECRET):
        response = client.post(
            "/api/v1/frameio/webhook",
            content=body,
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Missing required headers."}


def test_receive_webhook_with_no_secret_configured():
    timestamp = str(int(time.time()))
    payload = {"test": "data"}
    body = json.dumps(payload).encode()
    signature = "any_signature"

    with patch("src.app.main.FRAMEIO_WEBHOOK_SECRET", None):
        response = client.post(
            "/api/v1/frameio/webhook",
            content=body,
            headers={
                "x-frameio-signature": signature,
                "x-frameio-timestamp": timestamp,
            },
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "Webhook secret not configured."}
