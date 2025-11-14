from abc import ABC, abstractmethod
from typing import Dict, Any


class MessageQueue(ABC):
    """
    Defines the interface for a message queue service.
    This is a port in the Hexagonal Architecture.
    """

    @abstractmethod
    async def publish_message(self, topic_name: str, data: Dict[str, Any]) -> str:
        """
        Publishes a message to the specified topic.

        Args:
            topic_name: The name of the topic to publish to.
            data: The message data to publish, as a dictionary.

        Returns:
            The ID of the published message.
        """
        pass
