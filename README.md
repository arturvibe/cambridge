# Frame.io Webhook Handler

A FastAPI application to receive and process webhooks from Frame.io, deployed on Google Cloud Run.

## Configuration

To ensure the security of your webhook endpoint, this application verifies the signature of incoming webhooks. You'll need to configure a secret token in both Frame.io and your Google Cloud Run service.

### 1. Generate a Secret Token

You can generate a strong, random secret token using a password manager or the following command:

```bash
openssl rand -hex 32
```

### 2. Configure the Frame.io Webhook

When you create your webhook in Frame.io, paste the secret token you generated into the "Secret" field.

### 3. Configure the Google Cloud Run Service

In your Google Cloud Run service, you'll need to set the `FRAMEIO_WEBHOOK_SECRET` environment variable to the same secret token you used in Frame.io.

You can do this when you deploy the service for the first time or by updating the service's configuration.

## Viewing Logs

To view the logs for your service and see the payloads of incoming webhooks, you can use the Google Cloud Console or the `gcloud` command-line tool.

### Using the Google Cloud Console

1.  Go to the [Cloud Run](https://console.cloud.google.com/run) section of the Google Cloud Console.
2.  Click on your service in the list.
3.  Go to the "Logs" tab.

### Using the `gcloud` CLI

To view the logs for your service, you can use the following command:

```bash
gcloud logging read "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"<your-service-name>\"" --project=<your-project-id> --limit=100
```

Replace `<your-service-name>` with the name of your Cloud Run service and `<your-project-id>` with your Google Cloud project ID.
