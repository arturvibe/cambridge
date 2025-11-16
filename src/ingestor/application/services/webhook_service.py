import hmac
import hashlib
import time

from ..ports.message_queue import MessageQueuePort


class WebhookService:
    def __init__(self, message_queue: MessageQueuePort, webhook_secret: str):
        self.message_queue = message_queue
        self.webhook_secret = webhook_secret

    def verify_signature(self, request_timestamp: str, signature: str, body: bytes) -> bool:
        message = f"v0:{request_timestamp}:{body.decode()}"
        expected_signature = f"v0={hmac.new(bytes(self.webhook_secret, 'latin-1'), msg=bytes(message, 'latin-1'), digestmod=hashlib.sha256).hexdigest()}"

        if not hmac.compare_digest(expected_signature, signature):
            return False

        if abs(time.time() - int(request_timestamp)) > 300:
            return False

        return True

    async def process_webhook(self, payload: dict) -> None:
        await self.message_queue.publish_message(payload)
