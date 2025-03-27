"""
Sqirvy-ai: Llama Client Implementation (using OpenAI compatible API)
"""

import os
# Llama models often expose an OpenAI-compatible API, so we use ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Assuming client.py is in the same directory
from .client import Client, Options, query_text_langchain, DefaultTempScale

# Constants specific to Llama if needed, otherwise use defaults
# Llama via OpenAI-compatible API likely uses 0.0-2.0 scale
LLAMA_TEMP_SCALE = DefaultTempScale

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
        return query_text_langchain(self.llm, system, prompts, model, options)


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
        # Model name might be passed during invoke or sometimes needed here depending on provider
        llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        print(f"Using Llama Base URL: {base_url}") # Info message
    except Exception as e:
        # Catch potential initialization errors from LangChain
        raise Exception(f"Failed to create LangChain client for Llama: {e}") from e

    return LlamaClient(llm)

# Example Usage (optional, for testing)
if __name__ == '__main__':
    # Ensure LLAMA_API_KEY and LLAMA_BASE_URL are set
    if not os.getenv("LLAMA_API_KEY") or not os.getenv("LLAMA_BASE_URL"):
        print("Skipping example: LLAMA_API_KEY or LLAMA_BASE_URL not set.")
    else:
        try:
            client = NewLlamaClient()
            print("LlamaClient created successfully.")

            # Example query
            try:
                # Use default temp scale (2.0)
                opts = Options(temperature=70, max_tokens=100)
                # Ensure this model name matches what your Llama endpoint expects
                test_model = "llama3.3-70b"
                response = client.QueryText(
                    "You are a helpful coding assistant.",
                    ["Explain the difference between a list and a tuple in Python."],
                    test_model,
                    opts
                )
                print(f"\nQuery Response from {test_model}:")
                print(response)

                # Test empty prompt error
                print("\nTesting empty prompt error:")
                try:
                    client.QueryText("System", [], test_model, opts)
                except ValueError as e:
                    print(f"Successfully caught expected ValueError: {e}")

            except Exception as e:
                print(f"An unexpected error occurred during query: {e}")


            client.Close()
            print("\nClient closed.")

        except ValueError as e:
            print(f"Configuration Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
