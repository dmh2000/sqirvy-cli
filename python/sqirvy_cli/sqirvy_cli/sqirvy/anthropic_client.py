"""
sqirvy: Anthropic Client Implementation
"""

from langchain_anthropic import ChatAnthropic

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.exceptions import OutputParserException # For potential future use

from .client import Client, Options
from .query import query_text_langchain
from .env import get_api_key, get_base_url


# Constants matching Go implementation
ANTHROPIC_TEMP_SCALE = 1.0  # Anthropic uses 0.0-1.0


class AnthropicClient(Client):
    """
    Client implementation for Anthropic's API using LangChain.
    """

    def __init__(self, llm: ChatAnthropic):
        """
        Initializes the AnthropicClient.

        Args:
            llm: An instance of LangChain's ChatAnthropic.
        """
        self.llm = llm

    def query_text(self, system: str, prompts: list[str], options: Options) -> str:
        """
        Sends a text query to the specified Anthropic model using LangChain.

        Args:
            system: The system prompt.
            prompts: A list of user prompts.
            model: The specific Anthropic model identifier to use.
            options: An Options object containing temperature, max_tokens, etc.
                     Note: The temperature_scale specific to Anthropic (1.0)
                     should be set in the Options object before calling.

        Returns:
            The text response from the AI model.

        Raises:
            ValueError: If prompts list is empty or temperature is out of range.
            Exception: Errors from the LangChain API call.
        """
        # Ensure the correct temperature scale is used for Anthropic
        if options.temperature_scale is None:
            options.temperature_scale = ANTHROPIC_TEMP_SCALE
        elif options.temperature_scale != ANTHROPIC_TEMP_SCALE:
            # Optionally warn or raise if a different scale is explicitly provided
            print(
                f"Warning: Overriding anthropic temperature_scale ({options.temperature_scale}) "
            )
            options.temperature_scale = ANTHROPIC_TEMP_SCALE

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, system, prompts, options)

    def close(self):
        """
        Closes resources. For LangChain's Anthropic client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.


def new_anthropic_client(model: str) -> AnthropicClient:
    """
    Factory function to create a new AnthropicClient.

    Checks for the ANTHROPIC_API_KEY environment variable and initializes
    the LangChain ChatAnthropic client.

    Args:
        model: The model identifier to use.

    Returns:
        An instance of AnthropicClient.

    Raises:
        ValueError: If required environment variables are not set or if client initialization fails.
    """
    # Get required API credentials
    provider = "anthropic"
    api_key = get_api_key(provider)
    base_url = get_base_url(provider, default="https://api.anthropic.com")

    try:
        # Initialize the LangChain client
        llm = ChatAnthropic(model=model, api_key=api_key, base_url=base_url)
        return AnthropicClient(llm)
    except Exception as e:
        # Catch and contextualize initialization errors
        raise ValueError(f"Failed to create LangChain Anthropic client: {e}") from e
