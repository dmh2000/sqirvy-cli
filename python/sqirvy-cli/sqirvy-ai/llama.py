"""
Sqirvy-ai: Llama Client Implementation (using OpenAI compatible API)
"""

import os
# Llama models often expose an OpenAI-compatible API, so we use ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Assuming client.py is in the same directory
from .client import Client, Options

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

    def QueryText(self, system: str, prompts: list[str], model: str, options: Options) -> str:
        """
        Sends a text query to the specified Llama model using LangChain.

        Args:
            system: The system prompt.
            prompts: A list of user prompts.
            model: The specific Llama model identifier to use.
            options: An Options object containing temperature, max_tokens, etc.

        Returns:
            The text response from the AI model.

        Raises:
            NotImplementedError: Placeholder until fully implemented.
            Exception: Errors from the LangChain API call.
        """
        # TODO: Implement actual query logic using self.llm
        #       - Construct messages (SystemMessage, HumanMessage)
        #       - Handle temperature scaling (Llama often uses 0.0-2.0 like OpenAI)
        #       - Call self.llm.invoke(...)
        print(f"Placeholder: Querying Llama model {model} with system prompt and {len(prompts)} user prompts.")
        print(f"Options: {options}")
        raise NotImplementedError("LlamaClient.QueryText is not yet implemented")

    def Close(self):
        """
        Closes resources. For LangChain's client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.
        pass

def NewLlamaClient() -> LlamaClient:
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
            # You might need to set other specific parameters depending on the Llama API provider
            # e.g., model_name might be passed here or during invoke
        )
        print(f"Using Llama Base URL: {base_url}") # Info message
    except Exception as e:
        # Catch potential initialization errors from LangChain
        raise Exception(f"Failed to create LangChain client for Llama: {e}") from e

    return LlamaClient(llm)

# Example Usage (optional, for testing)
if __name__ == '__main__':
    try:
        # Ensure LLAMA_API_KEY and LLAMA_BASE_URL are set
        client = NewLlamaClient()
        print("LlamaClient created successfully.")

        # Example of how QueryText *might* be called (will raise NotImplementedError)
        try:
            opts = Options(temperature=70, max_tokens=100) # Example options
            response = client.QueryText(
                "You are a helpful coding assistant.",
                ["Explain the difference between a list and a tuple in Python."],
                "llama3.3-70b", # Example model - ensure this matches what the endpoint expects
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
