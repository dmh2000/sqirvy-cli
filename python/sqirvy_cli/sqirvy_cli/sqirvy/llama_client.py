"""
Llama Client Implementation (using OpenAI compatible API)
"""

# Llama models often expose an OpenAI-compatible API, so we use ChatOpenAI
from langchain_openai import ChatOpenAI

from .client import Client, Options
from .env import get_api_key, get_base_url
from .query import query_text_langchain
from .context import Context


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

    def query_text(self, context: Context) -> str:
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

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, context)

    def close(self):
        """
        Closes resources. For LangChain's client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.


def new_llama_client(context: Context) -> LlamaClient:
    """
    Factory function to create a new LlamaClient.
    """
    # Get required API credentials
    api_key = get_api_key(context.provider)
    base_url = get_base_url(context.provider)

    try:
        # Initialize the LangChain client for Llama
        llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=context.model,
        )
        return LlamaClient(llm)
    except Exception as e:
        # Catch and contextualize initialization errors
        raise ValueError(f"Failed to create LangChain client for Llama: {e}") from e
