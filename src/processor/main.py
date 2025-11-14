from fastapi import FastAPI, Request, Response, status
import base64
import json

app = FastAPI(
    title="Cambridge Processor Service",
    description="Processes messages from the queue to sync photos.",
    version="0.1.0",
)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/")
async def receive_pubsub_message(request: Request):
    """
    Receives a push message from a Pub/Sub subscription.

    This is a placeholder implementation.
    """
    # Pub/Sub push messages are base64 encoded
    envelope = await request.json()
    if not envelope or "message" not in envelope:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Bad Request: invalid Pub/Sub message format",
        )

    message = envelope["message"]
    data = base64.b64decode(message["data"]).decode("utf-8")

    print("Received Pub/Sub message data:", json.loads(data))

    # In a future step, this will download the asset from Frame.io
    # and upload it to Google Photos.

    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
