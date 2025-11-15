# Frame.io Webhook Handler

A FastAPI application to receive and process webhooks from Frame.io, deployed on Google Cloud Run.

## Deployment to Google Cloud Platform

This project uses Terraform to manage the infrastructure on Google Cloud Platform. To deploy the application, you will need to have the `gcloud` CLI and Terraform installed and configured.

For instructions on how to install the `gcloud` CLI on macOS, see the [official Google Cloud documentation](https://cloud.google.com/sdk/docs/install#mac).

### 1. Authenticate with Google Cloud

First, you'll need to authenticate with Google Cloud:

```bash
gcloud auth login
gcloud auth application-default login
```

### 2. Set Up Terraform

Navigate to the `terraform` directory and initialize Terraform:

```bash
cd terraform
terraform init
```

### 3. Deploy the Infrastructure

To deploy the infrastructure, you'll need to provide your Google Cloud project ID. You can do this by creating a `terraform.tfvars` file or by passing the variable on the command line.

**Using `terraform.tfvars`:**

Create a file named `terraform.tfvars` in the `terraform` directory with the following content:

```
project_id = "your-gcp-project-id"
```

Then, run the following commands:

```bash
terraform plan
terraform apply
```

**Using the command line:**

```bash
terraform plan -var="project_id=your-gcp-project-id"
terraform apply -var="project_id=your-gcp-project-id"
```

After a successful deployment, the URL of the Cloud Run service will be displayed as an output.

### 4. Continuous Deployment

This project is configured with a GitHub Actions workflow that will automatically build and deploy the application to Google Cloud Run whenever you push to the `main` branch.

You will need to configure the following secrets in your GitHub repository:

*   `GCP_PROJECT_ID`: Your Google Cloud project ID.
*   `GCP_SA_KEY`: A service account key with the necessary permissions to deploy to Cloud Run and Artifact Registry.

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
