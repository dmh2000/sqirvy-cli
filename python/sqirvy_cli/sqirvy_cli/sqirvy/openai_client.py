"""
sqirvy: OpenAI Client Implementation
"""

from langchain_openai import ChatOpenAI

# Assuming client.py is in the same directory
from .client import Client, Options
from .query import query_text_langchain
from .env import get_api_key, get_base_url
from .context import Context


class OpenAIClient(Client):
    """
    Client implementation for OpenAI's API using LangChain.
    """

    def __init__(self, llm: ChatOpenAI):
        """
        Initializes the OpenAIClient.

        Args:
            llm: An instance of LangChain's ChatOpenAI.
        """
        self.llm = llm

    def query_text(self, context: Context) -> str:
        """
        Sends a text query to the specified OpenAI model using LangChain.

        Args:
            system: The system prompt.
            prompts: A list of user prompts.
            model: The specific OpenAI model identifier to use.
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
        Closes resources. For LangChain's OpenAI client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.


def new_openai_client(context: Context) -> OpenAIClient:
    """
    Factory function to create a new OpenAIClient.
    """
    # Get required API credentials
    api_key = get_api_key(context.provider)
    base_url = get_base_url(context.provider)

    try:
        # Initialize the LangChain client
        init_args = {"api_key": api_key, "model": context.model, "base_url": base_url}
        llm = ChatOpenAI(**init_args)
        return OpenAIClient(llm)
    except Exception as e:
        # Catch and contextualize initialization errors
        raise ValueError(f"Failed to create LangChain OpenAI client: {e}") from e
