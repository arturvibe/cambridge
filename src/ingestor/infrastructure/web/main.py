import os
import json
from fastapi import FastAPI, Request, Response, status, Header
from typing import Optional

from ...application.services.webhook_service import WebhookService
from ..message_queue.pubsub_adapter import PubSubAdapter

app = FastAPI(
    title="Cambridge Ingestor Service",
    description="Receives webhooks from Frame.io and queues them for processing.",
    version="0.1.0",
)

# In a real application, you'd use a more robust dependency injection system
def get_webhook_service():
    project_id = os.environ.get("PROJECT_ID")
    topic_id = os.environ.get("TOPIC_ID")
    webhook_secret = os.environ.get("FRAME_IO_WEBHOOK_SECRET")

    if not all([project_id, topic_id, webhook_secret]):
        raise ValueError("Missing required environment variables")

    message_queue = PubSubAdapter(project_id, topic_id)
    return WebhookService(message_queue, webhook_secret)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/webhook")
async def receive_webhook(
    request: Request,
    x_frameio_request_timestamp: Optional[str] = Header(None),
    x_frameio_signature: Optional[str] = Header(None),
):
    """Receives a webhook from Frame.io."""
    if not x_frameio_request_timestamp or not x_frameio_signature:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Missing required headers",
        )

    body = await request.body()
    service = get_webhook_service()

    if not service.verify_signature(x_frameio_request_timestamp, x_frameio_signature, body):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid signature"
        )

    payload = json.loads(body)
    await service.process_webhook(payload)

    return Response(status_code=status.HTTP_202_ACCEPTED)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
