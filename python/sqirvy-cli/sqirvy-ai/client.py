from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union # Added Optional, Union, Dict, List

# Constants matching Go implementation
MaxTokensDefault = 4096
MinTemperature = 0.0
MaxTemperature = 100.0
DefaultTempScale = 2.0 # Default scaling factor (like OpenAI, Llama)

class Options:
    """
    Configuration options for AI client queries.

    Attributes:
        temperature: Controls randomness (0-100). Defaults to MinTemperature if None.
        max_tokens: Maximum response tokens. Defaults to MaxTokensDefault if None or 0.
        temperature_scale: Provider-specific scaling factor for temperature (e.g., 1.0 for Anthropic, 2.0 for OpenAI). Defaults to DefaultTempScale if None.
    """
    def __init__(self, temperature: Optional[float] = None, max_tokens: Optional[int] = None, temperature_scale: Optional[float] = None):
        self.temperature = temperature if temperature is not None else MinTemperature
        self.max_tokens = max_tokens if max_tokens is not None and max_tokens > 0 else MaxTokensDefault
        self.temperature_scale = temperature_scale if temperature_scale is not None else DefaultTempScale

    def __repr__(self):
        return f"Options(temperature={self.temperature}, max_tokens={self.max_tokens}, temperature_scale={self.temperature_scale})"


# Import specific client creation functions - these will be implemented in other files
# We need to handle potential circular imports if client.py imports from anthropic.py etc.
# A common pattern is to import within the NewClient function or use deferred imports.
# For simplicity here, we assume the functions exist but might refine imports later.

# --- Client Interface ---

class Client(ABC):
    """
    Abstract Base Class for AI client implementations.
    Defines the common interface for interacting with different AI providers.
    """

    @abstractmethod
    def QueryText(self, system: str, prompts: List[str], model: str, options: Options) -> str:
        """
        Sends a text query to the specified model and returns the response.

        Args:
            system: The system prompt or context.
            prompts: A list of user prompts.
            model: The specific model identifier to use.
            options: An Options object containing provider-specific settings.

        Returns:
            The text response from the AI model.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
            ValueError: If input parameters are invalid (e.g., empty prompts, bad temperature).
            Exception: Provider-specific errors during the API call.
        """
        pass

    @abstractmethod
    def Close(self):
        """
        Closes any open connections or resources used by the client.
        May not be necessary for all implementations.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        pass

# --- Factory Function ---

def NewClient(provider: str) -> Optional[Client]:
    """
    Factory function to create a new AI client based on the specified provider.

    Args:
        provider: The name of the AI provider (e.g., "gemini", "anthropic", "openai", "llama").

    Returns:
        An instance of the corresponding Client implementation, or None if creation fails.

    Raises:
        ValueError: If the specified provider is not supported.
        Exception: If client creation fails for other reasons (e.g., missing API key).
    """
    provider = provider.lower() # Ensure case-insensitivity

    # Import functions here to avoid potential circular dependencies at module level
    # and ensure they are defined before being called.
    try:
        if provider == "gemini":
            from .gemini import NewGeminiClient # Assuming gemini.py exists
            return NewGeminiClient()
        elif provider == "anthropic":
            from .anthropic import NewAnthropicClient
            return NewAnthropicClient()
        elif provider == "openai":
            from .openai import NewOpenAIClient # Assuming openai.py exists
            return NewOpenAIClient()
        elif provider == "llama":
            from .llama import NewLlamaClient # Assuming llama.py exists
            return NewLlamaClient()
        # Add other providers like "deepseek" here if needed
        # elif provider == "deepseek":
        #     from .deepseek import NewDeepSeekClient # Assuming deepseek.py exists
        #     return NewDeepSeekClient()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    except ImportError as e:
        # Handle cases where the specific client module might be missing or has issues
        raise ImportError(f"Could not import client module for provider '{provider}': {e}") from e
    except Exception as e:
        # Catch errors during client instantiation (e.g., missing keys handled in specific New*Client funcs)
        # Re-raise the specific error for clarity
        raise e


# Example Usage (optional, for testing)
if __name__ == '__main__':
    import os # Import os here for the example usage block
    # Note: Set relevant API keys in environment variables before running
    supported_providers = ["anthropic"] # Add others like "gemini", "openai", "llama" as implemented
    unsupported_provider = "unknown_provider"

    print("--- Testing Client Creation ---")
    for prov in supported_providers:
        # Check for API key before attempting creation in example
        key_needed = f"{prov.upper()}_API_KEY"
        if not os.getenv(key_needed):
             print(f"Skipping {prov} client creation test: {key_needed} not set.")
             continue

        try:
            print(f"Attempting to create client for: {prov}")
            # Ensure the corresponding New*Client function exists and API keys are set
            client_instance = NewClient(prov)
            if client_instance:
                print(f"Successfully created client for {prov}: {type(client_instance)}")
                # Placeholder for using the client
                try:
                    # Use temperature 0 for deterministic output in example
                    opts = Options(temperature=0, max_tokens=50)
                    # Use a known model for the provider (adjust if needed)
                    test_model = "claude-3-haiku-20240307" if prov == "anthropic" else "default-model"
                    response = client_instance.QueryText("System prompt", ["Say 'Test'"], test_model, opts)
                    print(f"  Query Response from {test_model}: {response[:100]}...") # Print snippet
                except NotImplementedError:
                     print(f"  QueryText for {prov} not implemented yet.")
                except ValueError as ve:
                     print(f"  Caught ValueError during query test: {ve}")
                except Exception as qe:
                     print(f"  Caught unexpected error during query test: {qe}")

                client_instance.Close()
                print(f"  Client for {prov} closed.")
            else:
                print(f"Failed to create client for {prov} (returned None)")
        except (ValueError, ImportError, Exception) as e:
            print(f"Error creating client for {prov}: {e}")

    print(f"\n--- Testing Unsupported Provider ({unsupported_provider}) ---")
    try:
        unsupported_client = NewClient(unsupported_provider)
    except ValueError as e:
        print(f"Successfully caught expected error for unsupported provider: {e}")
    except Exception as e:
        print(f"Caught unexpected error for unsupported provider: {e}")

    print("\n--- Testing Missing API Key (Example: Anthropic) ---")
    # Temporarily unset API key (if it was set) to test error handling
    original_key = os.environ.get("ANTHROPIC_API_KEY")
    key_was_set = False
    if original_key:
        del os.environ["ANTHROPIC_API_KEY"]
        key_was_set = True
        print("Temporarily unset ANTHROPIC_API_KEY for testing.")

    try:
        # Only run this test if the key was actually set initially
        if key_was_set:
            client_instance = NewClient("anthropic")
        else:
            print("Skipping missing key test for Anthropic as key was not set initially.")
    except ValueError as e:
         print(f"Successfully caught expected ValueError for missing API key: {e}")
    except Exception as e:
         print(f"Caught unexpected error when testing missing API key: {e}")
    finally:
        # Restore the key if it was originally set
        if key_was_set:
            os.environ["ANTHROPIC_API_KEY"] = original_key
            print("Restored ANTHROPIC_API_KEY.")

