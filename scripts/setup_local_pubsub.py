import os
import time
from google.cloud import pubsub_v1
from google.api_core import exceptions

# Configuration
PROJECT_ID = "local-project"
TOPIC_ID = "cambridge-ingest"
DLQ_TOPIC_ID = f"{TOPIC_ID}-dlq"
SUBSCRIPTION_ID = "cambridge-processor-subscription"
PROCESSOR_ENDPOINT = "http://processor:8081/"
EMULATOR_HOST = os.getenv("PUBSUB_EMULATOR_HOST", "localhost:8085")


def create_topic_if_not_exists(publisher, project_path, topic_id):
    """Creates a Pub/Sub topic if it doesn't already exist."""
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)
    try:
        publisher.create_topic(request={"name": topic_path})
        print(f"Topic {topic_id} created.")
    except exceptions.AlreadyExists:
        print(f"Topic {topic_id} already exists.")
    return topic_path


def main():
    """
    Sets up the local Pub/Sub environment for Cambridge.
    - Creates the main topic.
    - Creates the Dead Letter Queue (DLQ) topic.
    - Creates a push subscription to the main topic, configured to
      push to the processor service and use the DLQ.
    """
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    project_path = f"projects/{PROJECT_ID}"

    print("Waiting for Pub/Sub emulator to be ready...")
    # Simple wait, in a real scenario a more robust check would be better
    time.sleep(5)

    print("--- Setting up Pub/Sub Topics ---")
    topic_path = create_topic_if_not_exists(publisher, project_path, TOPIC_ID)
    dlq_topic_path = create_topic_if_not_exists(publisher, project_path, DLQ_TOPIC_ID)

    print("\n--- Setting up Pub/Sub Subscription ---")
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=PROCESSOR_ENDPOINT)

    dead_letter_policy = pubsub_v1.types.DeadLetterPolicy(
        dead_letter_topic=dlq_topic_path,
        max_delivery_attempts=5,
    )

    try:
        subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "push_config": push_config,
                "dead_letter_policy": dead_letter_policy,
                "ack_deadline_seconds": 60,
            }
        )
        print(f"Subscription {SUBSCRIPTION_ID} created.")
        print(f"  - Pushing to: {PROCESSOR_ENDPOINT}")
        print(f"  - Dead Letter Topic: {DLQ_TOPIC_ID}")

    except exceptions.AlreadyExists:
        print(f"Subscription {SUBSCRIPTION_ID} already exists.")

    print("\nLocal Pub/Sub setup complete.")


if __name__ == "__main__":
    main()
