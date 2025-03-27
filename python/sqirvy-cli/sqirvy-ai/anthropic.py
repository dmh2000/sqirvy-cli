"""
Sqirvy-ai: Anthropic Client Implementation
"""

import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.exceptions import OutputParserException # For potential future use

# Assuming client.py is in the same directory
from .client import Client, Options, MinTemperature, MaxTemperature

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

        Returns:
            The text response from the AI model.

        Raises:
            ValueError: If prompts list is empty or temperature is out of range.
            Exception: Errors from the LangChain API call.
        """
        if not prompts:
            raise ValueError("Prompts list cannot be empty for text query.")

        # Validate and scale temperature (0-100 -> 0.0-1.0 for Anthropic)
        temp = options.temperature if options.temperature is not None else MinTemperature # Default if None
        if not MinTemperature <= temp <= MaxTemperature:
             raise ValueError(f"Temperature must be between {MinTemperature} and {MaxTemperature}, got {temp}")

        # Use the specific scale for Anthropic if provided, otherwise default
        temp_scale = options.temperature_scale if options.temperature_scale is not None else ANTHROPIC_TEMP_SCALE
        scaled_temperature = (temp * temp_scale) / MaxTemperature

        # Construct messages
        messages = [SystemMessage(content=system)]
        for p in prompts:
            messages.append(HumanMessage(content=p))

        # Prepare LangChain options
        langchain_options = {
            "model": model,
            "temperature": scaled_temperature,
        }
        # Add max_tokens if provided in options (LangChain uses max_tokens)
        if options.max_tokens is not None and options.max_tokens > 0:
            # Anthropic uses 'max_tokens' in Langchain integration
            langchain_options["max_tokens"] = int(options.max_tokens)

        try:
            # Make the API call
            response = self.llm.invoke(messages, **langchain_options)

            # Extract content from response
            if hasattr(response, 'content'):
                return response.content
            else:
                # Handle unexpected response structure
                raise ValueError("Failed to parse content from LLM response.")

        except Exception as e:
            # Catch and re-raise LangChain or API errors
            raise Exception(f"Anthropic API query failed: {e}") from e


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
                with client.QueryText("System", [], test_model, opts) as cm:
                    pass # Should raise ValueError
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

