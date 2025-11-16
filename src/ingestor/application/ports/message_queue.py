from abc import ABC, abstractmethod


class MessageQueuePort(ABC):
    @abstractmethod
    async def publish_message(self, message: dict) -> None:
        pass
