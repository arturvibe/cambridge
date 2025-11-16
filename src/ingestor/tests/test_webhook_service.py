import asyncio
import time
import hmac
import hashlib
from unittest.mock import AsyncMock, MagicMock
import pytest

from src.ingestor.application.ports.message_queue import MessageQueuePort
from src.ingestor.application.services.webhook_service import WebhookService


class MockMessageQueue(MessageQueuePort):
    def __init__(self):
        self.published_messages = []

    async def publish_message(self, message: dict) -> None:
        self.published_messages.append(message)
        await asyncio.sleep(0)


@pytest.fixture
def message_queue() -> MockMessageQueue:
    return MockMessageQueue()


@pytest.fixture
def webhook_service(message_queue: MockMessageQueue) -> WebhookService:
    return WebhookService(message_queue, "test_secret")


def test_verify_signature_valid(webhook_service: WebhookService):
    timestamp = str(int(time.time()))
    body = b'{"test": "body"}'
    message = f"v0:{timestamp}:{body.decode()}"
    secret = "test_secret"
    signature = f"v0={hmac.new(bytes(secret, 'latin-1'), msg=bytes(message, 'latin-1'), digestmod=hashlib.sha256).hexdigest()}"

    assert webhook_service.verify_signature(timestamp, signature, body) is True


def test_verify_signature_invalid(webhook_service: WebhookService):
    timestamp = str(int(time.time()))
    body = b'{"test": "body"}'
    signature = "v0=invalid_signature"

    assert webhook_service.verify_signature(timestamp, signature, body) is False


def test_verify_signature_timestamp_expired(webhook_service: WebhookService):
    timestamp = str(int(time.time()) - 600)
    body = b'{"test": "body"}'
    message = f"v0:{timestamp}:{body.decode()}"
    secret = "test_secret"
    signature = f"v0={hmac.new(bytes(secret, 'latin-1'), msg=bytes(message, 'latin-1'), digestmod=hashlib.sha256).hexdigest()}"

    assert webhook_service.verify_signature(timestamp, signature, body) is False


@pytest.mark.asyncio
async def test_process_webhook(webhook_service: WebhookService, message_queue: MockMessageQueue):
    payload = {"test": "payload"}
    await webhook_service.process_webhook(payload)

    assert len(message_queue.published_messages) == 1
    assert message_queue.published_messages[0] == payload
