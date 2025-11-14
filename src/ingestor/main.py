from fastapi import FastAPI, Request, Response, status

app = FastAPI(
    title="Cambridge Ingestor Service",
    description="Receives webhooks from Frame.io and queues them for processing.",
    version="0.1.0",
)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receives a webhook from Frame.io.

    This is a placeholder implementation.
    """
    # In a future step, this will validate the signature,
    # parse the payload, and publish a message to Pub/Sub.
    payload = await request.json()
    print("Received webhook payload:", payload)

    return Response(status_code=status.HTTP_202_ACCEPTED)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
