"""
Abstract base class and factory function for AI client implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional  # Added Optional, Union, Dict, List

from .models import get_provider_name
from .context import Context

# Constants matching Go implementation
MAX_TOKENS_DEFAULT = 4096
MIN_TEMPERATURE = 0.0001
MAX_TEMPERATURE = 1.0


class Options:
    """
    Configuration options for AI client queries.

    Attributes:
        temperature: Controls randomness (0-1.0). Defaults to 0.5 if None.
        max_tokens: Maximum response tokens. Defaults to MAX_TOKENS_DEFAULT if None or 0.
    """

    def __init__(
        self,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        # Set default temperature if not provided
        temp_value = temperature if temperature is not None else MAX_TEMPERATURE / 2.0

        # Set validated temperature
        self.temperature = temp_value

        # Set max_tokens with default if needed
        self.max_tokens = (
            max_tokens
            if max_tokens is not None and max_tokens > 0
            else MAX_TOKENS_DEFAULT
        )

    def __repr__(self):
        return f"Options(temperature={self.temperature}, max_tokens={self.max_tokens}"


# --- Client Interface ---


class Client(ABC):
    """
    Abstract Base Class for AI client implementations.
    Defines the common interface for interacting with different AI providers.
    """

    @abstractmethod
    def query_text(self, context) -> str:
        """
        Sends a text query to the specified model and returns the response.

        Args:
            system: The system prompt or context.
            prompts: A list of user prompts.
            model: The specific model identifier to use.
            options: An Options object containing provider-specific settings.

        Returns:
            The text response from the AI model.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
            ValueError: If input parameters are invalid (e.g., empty prompts, bad temperature).
            Exception: Provider-specific errors during the API call.
        """

    @abstractmethod
    def close(self):
        """
        Closes any open connections or resources used by the client.
        May not be necessary for all implementations.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """


# --- Factory Function ---


def new_client(context: Context) -> Optional[Client]:
    """
    Factory function to create a new AI client based on the specified provider.

    Args:
        provider: The name of the AI provider (e.g., "gemini", "anthropic", "openai", "llama").

    Returns:
        An instance of the corresponding Client implementation, or None if creation fails.

    Raises:
        ValueError: If the specified provider is not supported.
        Exception: If client creation fails for other reasons (e.g., missing API key).
    """

    from .gemini_client import new_gemini_client
    from .anthropic_client import new_anthropic_client
    from .openai_client import new_openai_client
    from .llama_client import new_llama_client

    # Import functions here to avoid potential circular dependencies at module level
    # and ensure they are defined before being called.
    context.provider = get_provider_name(context.model)
    try:
        if context.provider == "gemini":
            return new_gemini_client(context)
        if context.provider == "anthropic":
            return new_anthropic_client(context)
        if context.provider == "openai":
            return new_openai_client(context)
        if context.provider == "llama":
            return new_llama_client(context)
        raise ValueError(f"Unsupported provider: {context.provider}")
    except ImportError as e:
        # Handle cases where the specific client module might be missing or has issues
        raise ImportError(
            f"Could not import client module for provider '{context.provider}': {e}"
        ) from e
    except Exception as e:
        # Catch errors during client instantiation (e.g., missing keys handled in specific New*Client funcs)
        # Re-raise the specific error for clarity
        raise e
