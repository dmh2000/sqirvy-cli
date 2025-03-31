"""
sqirvy: OpenAI Client Implementation
"""

from langchain_openai import ChatOpenAI

# Assuming client.py is in the same directory
from .client import Client, Options, DEFAULT_TEMPERATURE_SCALE
from .query import query_text_langchain
from .env import get_api_key, get_base_url

# Constants specific to OpenAI if needed, otherwise use defaults from client.py
OPENAI_TEMP_SCALE = (
    DEFAULT_TEMPERATURE_SCALE  # OpenAI typically uses 0.0-2.0, matching default
)


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

    def query_text(self, system: str, prompts: list[str], options: Options) -> str:
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
        # Ensure the correct temperature scale is used (defaults to 2.0 if None)
        if options.temperature_scale is None:
            options.temperature_scale = OPENAI_TEMP_SCALE

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, system, prompts, options)

    def close(self):
        """
        Closes resources. For LangChain's OpenAI client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.


def new_openai_client(model: str) -> OpenAIClient:
    """
    Factory function to create a new OpenAIClient.

    Checks for OPENAI_API_KEY and OPENAI_BASE_URL environment
    variables and initializes the LangChain ChatOpenAI client.

    Args:
        model: The model identifier to use.

    Returns:
        An instance of OpenAIClient.

    Raises:
        ValueError: If required environment variables are not set or if client initialization fails.
    """
    # Get required API credentials
    provider = "openai"
    api_key = get_api_key(provider)
    base_url = get_base_url(provider)

    try:
        # Initialize the LangChain client
        init_args = {"api_key": api_key, "model": model, "base_url": base_url}
        llm = ChatOpenAI(**init_args)
        return OpenAIClient(llm)
    except Exception as e:
        # Catch and contextualize initialization errors
        raise ValueError(f"Failed to create LangChain OpenAI client: {e}") from e
