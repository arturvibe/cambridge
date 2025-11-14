#!/bin/bash
set -e

echo "--- Starting local development environment ---"
docker-compose up -d

echo "\n--- Setting up Pub/Sub emulator topics and subscriptions ---"
# We need to install the google-cloud-pubsub library to run our setup script.
# Running it in a temporary container is a clean way to do this.
docker run --rm --network="host" \
  -e PUBSUB_EMULATOR_HOST="localhost:8085" \
  -v "$(pwd)/scripts:/scripts" \
  python:3.12-slim \
  bash -c "pip install google-cloud-pubsub && python /scripts/setup_local_pubsub.py"

echo "\n--- Local environment is ready! ---"
echo "Services:"
echo "  - Ingestor: http://localhost:8080"
echo "  - Processor: http://localhost:8081"
echo "  - Pub/Sub Emulator: localhost:8085"

echo "\nView logs with: docker-compose logs -f"
