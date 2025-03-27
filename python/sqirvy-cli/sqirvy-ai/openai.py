"""
Sqirvy-ai: OpenAI Client Implementation
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Assuming client.py is in the same directory
from .client import Client, Options

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

    def QueryText(self, system: str, prompts: list[str], model: str, options: Options) -> str:
        """
        Sends a text query to the specified OpenAI model using LangChain.

        Args:
            system: The system prompt.
            prompts: A list of user prompts.
            model: The specific OpenAI model identifier to use.
            options: An Options object containing temperature, max_tokens, etc.

        Returns:
            The text response from the AI model.

        Raises:
            NotImplementedError: Placeholder until fully implemented.
            Exception: Errors from the LangChain API call.
        """
        # TODO: Implement actual query logic using self.llm
        #       - Construct messages (SystemMessage, HumanMessage)
        #       - Handle temperature scaling (OpenAI uses 0.0-2.0)
        #       - Call self.llm.invoke(...)
        print(f"Placeholder: Querying OpenAI model {model} with system prompt and {len(prompts)} user prompts.")
        print(f"Options: {options}")
        raise NotImplementedError("OpenAIClient.QueryText is not yet implemented")

    def Close(self):
        """
        Closes resources. For LangChain's OpenAI client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.
        pass

def NewOpenAIClient() -> OpenAIClient:
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
        init_args = {"api_key": api_key}
        if base_url:
            init_args["base_url"] = base_url
            print(f"Using OpenAI Base URL: {base_url}") # Info message

        # Pass the API key explicitly and base_url if provided
        llm = ChatOpenAI(**init_args)
        # Example: llm = ChatOpenAI(model="gpt-4o", api_key=api_key, base_url=base_url)
    except Exception as e:
        # Catch potential initialization errors from LangChain
        raise Exception(f"Failed to create LangChain OpenAI client: {e}") from e

    return OpenAIClient(llm)

# Example Usage (optional, for testing)
if __name__ == '__main__':
    try:
        # Ensure OPENAI_API_KEY (and optionally OPENAI_BASE_URL) is set
        client = NewOpenAIClient()
        print("OpenAIClient created successfully.")

        # Example of how QueryText *might* be called (will raise NotImplementedError)
        try:
            opts = Options(temperature=70, max_tokens=100) # Example options
            response = client.QueryText(
                "You are a poetic assistant.",
                ["Write a short haiku about clouds."],
                "gpt-4o-mini", # Example model
                opts
            )
            print("Query Response:", response)
        except NotImplementedError as e:
            print(f"Caught expected error: {e}")

        client.Close()
        print("Client closed.")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
