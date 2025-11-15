import hashlib
import hmac
import json
import os

from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

# Get the webhook secret from an environment variable
FRAMEIO_WEBHOOK_SECRET = os.environ.get("FRAMEIO_WEBHOOK_SECRET")


@app.post("/api/v1/frameio/webhook")
async def receive_frameio_webhook(
    request: Request,
    x_frameio_signature: str = Header(None),
    x_frameio_timestamp: str = Header(None),
):
    """
    Receives a webhook from Frame.io, verifies its signature,
    and prints the payload.
    """
    if not FRAMEIO_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured.")

    if not x_frameio_signature or not x_frameio_timestamp:
        raise HTTPException(status_code=400, detail="Missing required headers.")

    # Get the raw request body
    body = await request.body()

    # Verify the signature
    expected_signature = hmac.new(
        key=FRAMEIO_WEBHOOK_SECRET.encode(),
        msg=f"{x_frameio_timestamp}:{body.decode()}".encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_frameio_signature):
        raise HTTPException(status_code=401, detail="Invalid signature.")

    # Print the payload to stdout
    print(json.loads(body))

    return {"status": "success"}
