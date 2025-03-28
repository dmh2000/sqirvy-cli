"""
Llama Client Implementation (using OpenAI compatible API)
"""

import os

# Llama models often expose an OpenAI-compatible API, so we use ChatOpenAI
from langchain_openai import ChatOpenAI

from .client import Client, Options
from .query import query_text_langchain


# Constants specific to Llama if needed, otherwise use defaults
# Llama via OpenAI-compatible API likely uses 0.0-2.0 scale
LLAMA_TEMP_SCALE = 1.0


class LlamaClient(Client):
    """
    Client implementation for Llama models via an OpenAI-compatible API using LangChain.
    """

    def __init__(self, llm: ChatOpenAI):
        """
        Initializes the LlamaClient.

        Args:
            llm: An instance of LangChain's ChatOpenAI configured for the Llama endpoint.
        """
        self.llm = llm

    def query_text(self, system: str, prompts: list[str], options: Options) -> str:
        """
        Sends a text query to the specified Llama model using LangChain's OpenAI interface.

        Args:
            system: The system prompt.
            prompts: A list of user prompts.
            model: The specific Llama model identifier to use (must match endpoint expectation).
            options: An Options object containing temperature, max_tokens, etc.
                     Uses the default temperature scale (2.0) if not specified.

        Returns:
            The text response from the AI model.

        Raises:
            ValueError: If prompts list is empty or temperature is out of range.
            Exception: Errors from the LangChain API call.
        """
        # Ensure the correct temperature scale is used (defaults to 2.0 if None)
        if options.temperature_scale is None:
            options.temperature_scale = LLAMA_TEMP_SCALE

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, system, prompts, options)

    def close(self):
        """
        Closes resources. For LangChain's client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.


def new_llama_client(model: str) -> LlamaClient:
    """
    Factory function to create a new LlamaClient.

    Checks for LLAMA_API_KEY and LLAMA_BASE_URL environment variables
    and initializes the LangChain ChatOpenAI client configured for the Llama endpoint.

    Returns:
        An instance of LlamaClient.

    Raises:
        ValueError: If LLAMA_API_KEY or LLAMA_BASE_URL environment variables are not set.
        Exception: If the LangChain client fails to initialize.
    """
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        raise ValueError("LLAMA_API_KEY environment variable not set")

    base_url = os.getenv("LLAMA_BASE_URL")
    if not base_url:
        raise ValueError("LLAMA_BASE_URL environment variable not set")

    try:
        # Use ChatOpenAI but point it to the Llama endpoint
        llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model,
        )
        print(f"Using Llama Base URL: {base_url}")  # Info message
    except ValueError as e:
        # Catch potential initialization errors from LangChain
        raise ValueError(f"Failed to create LangChain client for Llama: {e}") from e

    return LlamaClient(llm)
