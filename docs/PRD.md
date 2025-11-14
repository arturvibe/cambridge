# Product Requirements Document: Cambridge Photo Sync (GCP Edition)

**Author:** Jules (AI Software Engineer)
**Version:** 1.0
**Status:** In Development
**Date:** 2025-11-13

---

## 1. Introduction

Professional and prosumer photographers/videographers increasingly use Frame.io's Camera to Cloud (C2C) service to get files from their cameras to the cloud instantly. However, Frame.io is a collaborative review tool, not a permanent personal archive. Users lack a simple, automated way to sync these valuable assets to their personal, long-term photo storage solutions like Google Photos. This creates a manual, time-consuming gap in their workflow, similar to the problem smartphone users had before automatic camera roll backups became standard.

**Cambridge** is a serverless application that bridges this gap. It provides a reliable, automated pipeline to sync photos from a Frame.io project directly into a user's Google Photos library, creating an effortless "set it and forget it" backup experience. The V2.0 release will introduce a multi-user web interface, allowing users to self-manage their service connections and sync rules.

---

## 2. Project Goals & Objectives

- **Automate Workflow:** To eliminate the manual process of downloading photos from Frame.io and re-uploading them to Google Photos.
- **Provide a User-Friendly Experience:** To deliver a simple web portal where non-technical users can authenticate their services and configure sync rules.
- **Build a Robust & Scalable System:** To create a secure, reliable, and cost-effective solution using a modern, serverless GCP technology stack.
- **Ensure Maintainability:** To build a flexible, platform-agnostic codebase using Hexagonal Architecture, enabling future expansion to other services with minimal effort.

---

## 3. User Personas

- **Priya, the Professional Photographer:** Shoots events and needs to provide clients with proofs via Frame.io. She wants an automatic backup of all final JPGs sent to clients to be archived in her personal Google Photos account for long-term storage without any manual work.
- **Leo, the Hobbyist Filmmaker:** Uses his mirrorless camera with C2C for personal projects. He wants the photos he takes to appear seamlessly in his Google Photos library, just like they do from his smartphone, so he can easily view and share them.
- **Alex, the Small Agency Owner:** Manages several client projects in Frame.io. They need a system where they can set up distinct sync rules for each client, ensuring that assets from different projects are correctly routed and archived, with the ability for team members to manage their own connections.

---

## 4. Features & Requirements

### 4.1. Functional Requirements

#### Epic 1: Core Sync Engine
*The backend pipeline responsible for receiving notifications and transferring photos.*

- **FR1.1: Secure Webhook Ingestion:** The system must expose a secure public endpoint to receive `asset.created` webhooks from Frame.io. All incoming requests must be validated using the HMAC signature provided by Frame.io.
- **FR1.2: Asynchronous Processing:** Upon successful validation, the webhook payload must be placed into a message queue (GCP Pub/Sub) to decouple ingestion from the transfer process, ensuring reliability and scalability.
- **FR1.3: Frame.io Asset Processing:** The processor service must be able to:
    - Parse the webhook message.
    - Use the Frame.io API to retrieve asset metadata.
    - Download the original asset file from the URL provided in the metadata.
- **FR1.4: Google Photos Upload:** The processor service must be able to:
    - Authenticate with the Google Photos Library API using stored credentials.
    - Upload the downloaded photo file to the user's Google Photos library.
- **FR1.5: File Type Filtering:** The system must support configuration to filter assets based on their file type (e.g., only sync JPG, ARW, CR3 files).

#### Epic 2: Multi-User Web Interface (V2.0)
*A web portal for users to manage their accounts and sync rules.*

- **FR2.1: User Authentication:** Users must be able to create an account, sign in, and sign out. The system will be secured using GCP Identity Platform.
- **FR2.2: Service Connection Management:** Authenticated users must have a UI to securely add, view, and remove credentials for external services (initially Frame.io and Google Photos, via API tokens).
- **FR2.3: Sync Rule Management:** Users must have a UI to create, view, and delete sync rules. A rule defines a source (Frame.io project), a destination (Google Photos), and associated filters (file types).

### 4.2. Non-Functional Requirements

- **NFR1: Cloud Platform:** The entire solution must be built and deployed on Google Cloud Platform (GCP).
- **NFR2: Architecture:** The Python backend must follow the Hexagonal Architecture (Ports and Adapters) pattern to keep core logic independent of infrastructure.
- **NFR3: Compute:** All backend services (ingestor, processor, user API) must be deployed as containerized applications on GCP Cloud Run, configured to scale to zero.
- **NFR4: Infrastructure as Code:** All GCP resources (Cloud Run, Pub/Sub, Firestore, etc.) must be defined and managed using Terraform.
- **NFR5: Security:** All secrets and credentials (API tokens, webhook secrets) must be stored securely in GCP Secret Manager.
- **NFR6: Reliability:** The system must include a Dead Letter Queue (DLQ) to capture and store messages that fail processing after multiple retries.
- **NFR7: Local Development:** The project must provide a complete, one-step local development environment using Docker Compose and official GCP emulators.
- **NFR8: CI/CD:** The project must have a Continuous Integration pipeline in GitHub Actions that automatically runs linter, formatter checks, and unit tests.

---

## 5. Out of Scope (for V1.0)

- In-app OAuth 2.0 flows for connecting services (users will provide tokens/secrets manually).
- Support for other cloud storage destinations (e.g., Dropbox, OneDrive, iCloud).
- Email or push notifications for sync status or failures.
- A UI-based mechanism for manually re-driving failed jobs from the DLQ.
- Advanced analytics and usage reporting dashboard.

---

## 6. Project Milestones & Plan

*This plan outlines the major development phases to deliver the Cambridge project.*

- **Milestone 1: Core Infrastructure & Scaffolding (✅ Complete)**
    - **Status:** Completed
    - **Description:** Establish the complete foundational structure for the project.
    - **Key Deliverables:**
        - Project directories and files created.
        - Hexagonal architecture core (ports) defined.
        - Containerized skeletons for Ingestor and Processor services.
        - Fully configured local development environment with Docker Compose and Pub/Sub emulator.
        - Terraform scripts for core GCP resources (Pub/Sub, Secret Manager).
        - GitHub Actions CI pipeline for linting, formatting, and testing.

- **Milestone 2: End-to-End Sync Logic**
    - **Status:** Next Up
    - **Description:** Implement the core business logic to make the photo sync functional.
    - **Key Deliverables:**
        - Implement `PubSubAdapter` and integrate it into the Ingestor service to publish messages.
        - Implement `FrameioAdapter` to fetch asset metadata and download files.
        - Implement `GooglePhotosAdapter` to authenticate and upload photos.
        - Integrate adapters into the Processor service to create a complete, working data pipeline.
        - Write comprehensive unit and integration tests for the adapters and services.

- **Milestone 3: Reliability & Configuration**
    - **Status:** Not Started
    - **Description:** Harden the pipeline with robust error handling and configuration.
    - **Key Deliverables:**
        - Implement idempotency checks using Firestore to prevent duplicate processing of assets.
        - Add robust error handling and automatic retry logic within the Processor service.
        - Add environment variable or configuration file support for file type filtering.

- **Milestone 4: V2.0 User API & Authentication**
    - **Status:** Not Started
    - **Description:** Build the backend API to support the multi-user web interface.
    - **Key Deliverables:**
        - Define Firestore data models for Users, Service Connections, and Sync Rules.
        - Create a new Cloud Run service for the User API (FastAPI) with CRUD endpoints for managing connections and rules.
        - Integrate GCP Identity Platform for user signup, login, and JWT-based endpoint protection.
        - Unit and integration tests for the User API.

- **Milestone 5: V2.0 Frontend Application**
    - **Status:** Not Started
    - **Description:** Develop the user-facing web portal.
    - **Key Deliverables:**
        - Set up a React/Vite frontend application with Tailwind CSS.
        - Create pages and components for Login, Dashboard, Service Connections, and Sync Rules.
        - Integrate the frontend with the User API.
        - Configure hosting on GCP Cloud Storage with a Cloud CDN for delivery.

- **Milestone 6: Continuous Deployment (CD)**
    - **Status:** Not Started
    - **Description:** Automate the deployment of the entire application.
    - **Key Deliverables:**
        - Add Terraform code to provision GCP Artifact Registry.
        - Extend the GitHub Actions workflow to build and push Docker images for all services to Artifact Registry.
        - Add Terraform code to deploy the services to Cloud Run, referencing the newly built images.
        - Configure the CD pipeline to automatically deploy to GCP on a merge to the main branch.

---

## 7. Success Metrics

- **Functionality:** An end-to-end test successfully syncs a photo from Frame.io to Google Photos within 5 minutes of upload.
- **Usability:** A new user can sign up, connect their services, and configure a sync rule in under 10 minutes without documentation.
- **Reliability:** The CI pipeline passes consistently, and the pipeline correctly handles transient errors without data loss.
- **Developer Experience:** A new developer can clone the repository and get the full local environment running with a single command.
