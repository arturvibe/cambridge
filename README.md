# Frame.io Webhook Handler

A FastAPI application to receive and process webhooks from Frame.io, deployed on Google Cloud Run.

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
