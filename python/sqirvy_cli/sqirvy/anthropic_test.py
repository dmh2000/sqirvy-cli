"""
sqirvy: Anthropic Client TEst
"""

from .anthropic_client import new_anthropic_client
from .client import Options

if __name__ == "__main__":
    import os

    # Ensure ANTHROPIC_API_KEY is set in your environment for this to work
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Skipping example: ANTHROPIC_API_KEY not set.")
    else:
        try:
            TEST_MODEL = "claude-3-haiku-20240307"  # Use a fast model for testing
            client = new_anthropic_client(TEST_MODEL)
            print("AnthropicClient created successfully.")

            # Example query
            # Use temperature 0 for deterministic output in example
            # Explicitly set the correct scale for clarity, though query_text handles it
            opts = Options(
                temperature=1.0,
                max_tokens=2048,
                temperature_scale=1.0,
            )
            response = client.query_text(
                "You are a helpful assistant.",
                ["Say 'Hello, World!'"],
                opts,
            )
            print(f"\nQuery Response from {TEST_MODEL}:")
            print(response)

            # Test empty prompt error
            print("\nTesting empty prompt error:")
            try:
                client.query_text("System", [], opts)
            except ValueError as e:
                print(f"Successfully caught expected ValueError: {e}")

            client.close()
            print("\nClient closed.")

        except ValueError as e:
            print(f"Configuration Error: {e}")
