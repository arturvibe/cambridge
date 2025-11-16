import json
import asyncio
from google.cloud.pubsub_v1 import PublisherClient
from ...application.ports.message_queue import MessageQueuePort


class PubSubAdapter(MessageQueuePort):
    def __init__(self, project_id: str, topic_id: str):
        self.publisher = PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    async def publish_message(self, message: dict) -> None:
        data = json.dumps(message).encode("utf-8")
        future = self.publisher.publish(self.topic_path, data)
        await asyncio.to_thread(future.result)
