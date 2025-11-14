terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "The GCP project ID to deploy resources into."
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources into."
  type        = string
  default     = "us-central1"
}

variable "secret_name" {
  description = "The name of the secret to create in Secret Manager."
  type        = string
  default     = "cambridge-creds"
}

resource "google_pubsub_topic" "ingest" {
  name = "cambridge-ingest"
}

resource "google_pubsub_topic" "ingest_dlq" {
  name = "cambridge-ingest-dlq"
}

resource "google_secret_manager_secret" "cambridge_creds" {
  secret_id = var.secret_name

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "cambridge_creds_initial" {
  secret = google_secret_manager_secret.cambridge_creds.id
  secret_data = jsonencode({
    FRAME_IO_TOKEN"          : "your-frameio-token-here",
    FRAME_IO_WEBHOOK_SECRET" : "generate-a-random-secret-here",
    GOOGLE_CLIENT_ID"        : "your-google-client-id.apps.googleusercontent.com",
    GOOGLE_CLIENT_SECRET"    : "your-google-client-secret",
    GOOGLE_REFRESH_TOKEN"    : "your-google-refresh-token"
  })
}
