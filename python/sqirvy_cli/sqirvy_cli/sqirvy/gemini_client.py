"""
Google Gemini Client Implementation
"""

from langchain_google_genai import ChatGoogleGenerativeAI


from .client import Client, Options
from .query import query_text_langchain
from .env import get_api_key

# Constants specific to Gemini if needed
# Gemini's native temperature scale is often 0.0-1.0 or 0.0-2.0.
# Langchain's integration might handle this, but we can specify if needed.
# Let's assume Langchain handles it correctly for now, or use 1.0/2.0 if issues arise.
GEMINI_TEMP_SCALE = 1.0  # Assuming Langchain expects 0.0-1.0 for Gemini


class GeminiClient(Client):
    """
    Client implementation for Google's Gemini API using LangChain.
    """

    def __init__(self, llm: ChatGoogleGenerativeAI):
        """
        Initializes the GeminiClient.

        Args:
            llm: An instance of LangChain's ChatGoogleGenerativeAI.
        """
        self.llm = llm

    def query_text(self, system: str, prompts: list[str], options: Options) -> str:
        """
        Sends a text query to the specified Gemini model using LangChain.

        Args:
            system: The system prompt (Note: Gemini might handle system prompts differently,
                    Langchain's integration might adapt or ignore it).
            prompts: A list of user prompts.
            model: The specific Gemini model identifier to use (e.g., "gemini-1.5-flash").
            options: An Options object containing temperature, max_tokens, etc.
                     Adjust temperature_scale if Langchain's default handling is incorrect.

        Returns:
            The text response from the AI model.

        Raises:
            ValueError: If prompts list is empty or temperature is out of range.
            Exception: Errors from the LangChain API call.
        """
        # Ensure the correct temperature scale is used for Gemini if needed
        if options.temperature_scale is None:
            options.temperature_scale = GEMINI_TEMP_SCALE
        elif options.temperature_scale != GEMINI_TEMP_SCALE:
            print(
                f"Warning: Using provided temperature_scale ({options.temperature_scale}) \
                for Gemini, expected scale might be {GEMINI_TEMP_SCALE}"
            )
            # Allow override but warn

        # Note: System prompt handling varies with Gemini models and Langchain versions.
        # The common helper function includes it, but its effect depends on the underlying implementation.

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, system, prompts, options)

    def close(self):
        """
        Closes resources. For LangChain's Gemini client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.


def new_gemini_client(model: str) -> GeminiClient:
    """
    Factory function to create a new GeminiClient.

    Checks for the GEMINI_API_KEY environment variable and initializes
    the LangChain ChatGoogleGenerativeAI client.

    Args:
        model: The model identifier to use.

    Returns:
        An instance of GeminiClient.

    Raises:
        ValueError: If required environment variables are not set or if client initialization fails.
    """
    # Get required API credentials
    provider = "gemini"
    api_key = get_api_key(provider)

    try:
        # Initialize the LangChain client
        llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
        return GeminiClient(llm)
    except Exception as e:
        # Catch and contextualize initialization errors
        raise ValueError(f"Failed to create LangChain Gemini client: {e}") from e
