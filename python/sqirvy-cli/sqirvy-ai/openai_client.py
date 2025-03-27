"""
Sqirvy-ai: OpenAI Client Implementation
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Assuming client.py is in the same directory
from .client import Client, Options, query_text_langchain, DefaultTempScale

# Constants specific to OpenAI if needed, otherwise use defaults from client.py
OPENAI_TEMP_SCALE = DefaultTempScale # OpenAI typically uses 0.0-2.0, matching default

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

    def QueryText(self, system: str, prompts: list[str], options: Options) -> str:
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


    def Close(self):
        """
        Closes resources. For LangChain's OpenAI client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.
        pass

def NewOpenAIClient(model: str) -> OpenAIClient:
    """
    Factory function to create a new OpenAIClient.

    Checks for OPENAI_API_KEY and optionally OPENAI_BASE_URL environment
    variables and initializes the LangChain ChatOpenAI client.

    Returns:
        An instance of OpenAIClient.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
        Exception: If the LangChain client fails to initialize.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    base_url = os.getenv("OPENAI_BASE_URL") # Optional base URL

    try:
        init_args = {"api_key": api_key, "model": model}
        if base_url:
            init_args["base_url"] = base_url
            print(f"Using OpenAI Base URL: {base_url}") # Info message

        # Pass the API key explicitly and base_url if provided
        # Model is specified during the query
        llm = ChatOpenAI(**init_args)
    except Exception as e:
        # Catch potential initialization errors from LangChain
        raise Exception(f"Failed to create LangChain OpenAI client: {e}") from e

    return OpenAIClient(llm)
