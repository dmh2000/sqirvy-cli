"""
sqirvy: Anthropic Client Implementation
"""

import os
from langchain_anthropic import ChatAnthropic

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.exceptions import OutputParserException # For potential future use

# Assuming client.py is in the same directory
from .client import (
    Client,
    Options,
    MinTemperature,
    MaxTemperature,
    query_text_langchain,
)

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

    def QueryText(self, system: str, prompts: list[str], options: Options) -> str:
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
                f"Warning: Overriding provided temperature_scale ({options.temperature_scale}) with Anthropic's required scale ({ANTHROPIC_TEMP_SCALE})"
            )
            options.temperature_scale = ANTHROPIC_TEMP_SCALE

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, system, prompts, options)

    def Close(self):
        """
        Closes resources. For LangChain's Anthropic client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.
        pass


def NewAnthropicClient(model: str) -> AnthropicClient:
    """
    Factory function to create a new AnthropicClient.

    Checks for the ANTHROPIC_API_KEY environment variable and initializes
    the LangChain ChatAnthropic client.

    Returns:
        An instance of AnthropicClient.

    Raises:
        ValueError: If the ANTHROPIC_API_KEY environment variable is not set.
        Exception: If the LangChain client fails to initialize.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    if not base_url:
        raise ValueError("ANTHROPIC_BASE_URL environment variable not set")

    try:
        # LangChain's ChatAnthropic automatically picks up the API key
        # from the environment variable if not explicitly passed.
        # We don't specify the model here; it's passed during QueryText.
        llm = ChatAnthropic(model=model, api_key=api_key, base_url=base_url)
    except Exception as e:
        # Catch potential initialization errors from LangChain
        raise Exception(f"Failed to create LangChain Anthropic client: {e}") from e

    return AnthropicClient(llm)
