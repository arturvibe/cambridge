import os
import json
import time
from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest

from scripts.frameio_webhook_mock.main import generate_signature, generate_asset_created_payload
from src.ingestor.infrastructure.web.main import app


@pytest.fixture
def client() -> TestClient:
    os.environ["PROJECT_ID"] = "test_project"
    os.environ["TOPIC_ID"] = "test_topic"
    os.environ["FRAME_IO_WEBHOOK_SECRET"] = "test_secret"
    return TestClient(app)


@patch("src.ingestor.infrastructure.message_queue.pubsub_adapter.PublisherClient")
def test_webhook_success(mock_publisher_client, client: TestClient):
    mock_publisher = mock_publisher_client.return_value
    mock_publisher.publish.return_value.result.return_value = "message_id"

    payload = generate_asset_created_payload("asset_123")
    body = json.dumps(payload)
    timestamp = int(time.time())
    signature = generate_signature(timestamp, body, "test_secret")

    headers = {
        "X-Frameio-Request-Timestamp": str(timestamp),
        "X-Frameio-Signature": signature,
    }

    response = client.post("/webhook", content=body, headers=headers)
    assert response.status_code == 202

    # Check that the mocked publish method was called correctly
    topic_path = mock_publisher.topic_path("test_project", "test_topic")
    mock_publisher.publish.assert_called_once_with(topic_path, json.dumps(payload).encode("utf-8"))


def test_webhook_missing_headers(client: TestClient):
    payload = generate_asset_created_payload("asset_123")
    body = json.dumps(payload)

    response = client.post("/webhook", content=body)
    assert response.status_code == 400


@patch("src.ingestor.infrastructure.message_queue.pubsub_adapter.PublisherClient")
def test_webhook_invalid_signature(mock_publisher_client, client: TestClient):
    payload = generate_asset_created_payload("asset_123")
    body = json.dumps(payload)
    timestamp = int(time.time())

    headers = {
        "X-Frameio-Request-Timestamp": str(timestamp),
        "X-Frameio-Signature": "v0=invalid",
    }

    response = client.post("/webhook", content=body, headers=headers)
    assert response.status_code == 401
    mock_publisher_client.return_value.publish.assert_not_called()
