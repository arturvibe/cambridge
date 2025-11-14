import hmac
import hashlib
import json
import time
from uuid import uuid4

import click
import requests


def generate_signature(timestamp: int, body: str, secret: str) -> str:
    message = f"v0:{timestamp}:{body}"
    return f"v0={hmac.new(bytes(secret, 'latin-1'), msg=bytes(message, 'latin-1'), digestmod=hashlib.sha256).hexdigest()}"


def generate_asset_created_payload(asset_id: str) -> dict:
    return {
        "type": "asset.created",
        "resource": {
            "type": "asset",
            "id": asset_id,
        },
        "user": {
            "id": f"user-{uuid4()}",
        },
        "team": {
            "id": f"team-{uuid4()}",
        },
    }


@click.group()
def cli():
    pass


@cli.command()
@click.option("--asset-id", default=lambda: f"asset-{uuid4()}", help="The asset ID to include in the webhook payload.")
@click.option("--webhook-url", required=True, help="The URL to send the webhook to.")
@click.option("--webhook-secret", required=True, help="The secret to use for signing the webhook.")
def send_asset_created(asset_id: str, webhook_url: str, webhook_secret: str):
    """Sends an asset.created webhook to the specified URL."""
    payload = generate_asset_created_payload(asset_id)
    body = json.dumps(payload)
    timestamp = int(time.time())
    signature = generate_signature(timestamp, body, webhook_secret)

    headers = {
        "X-Frameio-Request-Timestamp": str(timestamp),
        "X-Frameio-Signature": signature,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(webhook_url, data=body, headers=headers)
        response.raise_for_status()
        click.echo(f"Webhook sent successfully to {webhook_url}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error sending webhook: {e}", err=True)


if __name__ == "__main__":
    cli()
