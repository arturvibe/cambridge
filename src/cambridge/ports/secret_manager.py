from abc import ABC, abstractmethod


class SecretManager(ABC):
    """
    Defines the interface for a secret management service.
    This is a port in the Hexagonal Architecture.
    """

    @abstractmethod
    async def get_secret(self, secret_name: str) -> str:
        """
        Retrieves a secret value.

        Args:
            secret_name: The identifier of the secret to retrieve.

        Returns:
            The secret value as a string.
        """
        pass
