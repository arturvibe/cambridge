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

variable "app_name" {
  description = "The name of the application."
  type        = string
  default     = "frameio-webhook-app"
}

resource "google_artifact_registry_repository" "main" {
  location      = var.region
  repository_id = var.app_name
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "main" {
  name     = var.app_name
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.main.repository_id}/${var.app_name}:latest"
    }
  }
}

resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_cloud_run_v2_service.main.service_account}"
}
