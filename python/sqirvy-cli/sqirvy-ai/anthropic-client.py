"""
Sqirvy-ai: Anthropic Client Implementation
"""

import os
from langchain_anthropic import ChatAnthropic

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.exceptions import OutputParserException # For potential future use

# Assuming client.py is in the same directory
from .client import Client, Options, MinTemperature, MaxTemperature, query_text_langchain

# Constants matching Go implementation
ANTHROPIC_TEMP_SCALE = 1.0 # Anthropic uses 0.0-1.0

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

    def QueryText(self, system: str, prompts: list[str], model: str, options: Options) -> str:
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
             print(f"Warning: Overriding provided temperature_scale ({options.temperature_scale}) with Anthropic's required scale ({ANTHROPIC_TEMP_SCALE})")
             options.temperature_scale = ANTHROPIC_TEMP_SCALE

        # Delegate to the common LangChain query function
        return query_text_langchain(self.llm, system, prompts, model, options)


    def Close(self):
        """
        Closes resources. For LangChain's Anthropic client, this is usually a no-op.
        """
        # The LangChain client doesn't typically require explicit closing.
        pass

def NewAnthropicClient() -> AnthropicClient:
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

    try:
        # LangChain's ChatAnthropic automatically picks up the API key
        # from the environment variable if not explicitly passed.
        # We don't specify the model here; it's passed during QueryText.
        llm = ChatAnthropic()
    except Exception as e:
        # Catch potential initialization errors from LangChain
        raise Exception(f"Failed to create LangChain Anthropic client: {e}") from e

    return AnthropicClient(llm)

# Example Usage (optional, for testing)
if __name__ == '__main__':
    # Ensure ANTHROPIC_API_KEY is set in your environment for this to work
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Skipping example: ANTHROPIC_API_KEY not set.")
    else:
        try:
            client = NewAnthropicClient()
            print("AnthropicClient created successfully.")

            # Example query
            try:
                # Use temperature 0 for deterministic output in example
                # Explicitly set the correct scale for clarity, though QueryText handles it
                opts = Options(temperature=0, max_tokens=50, temperature_scale=ANTHROPIC_TEMP_SCALE)
                test_model = "claude-3-haiku-20240307" # Use a fast model for testing
                response = client.QueryText(
                    "You are a helpful assistant.",
                    ["Say 'Hello, World!'"],
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

