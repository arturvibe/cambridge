import json

from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/api/v1/frameio/webhook")
async def receive_frameio_webhook(request: Request):
    """
    Receives a webhook from Frame.io and prints the payload.
    """
    body = await request.body()
    print(json.loads(body))
    return {"status": "success"}
