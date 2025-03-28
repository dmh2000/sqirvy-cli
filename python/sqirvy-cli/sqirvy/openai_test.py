"""
OpenAI API Client Test
"""

import os
from .openai_client import new_openai_client, Options


# Example Usage (optional, for testing)
if __name__ == "__main__":
    # Ensure OPENAI_API_KEY (and optionally OPENAI_BASE_URL) is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping example: OPENAI_API_KEY not set.")
    else:
        try:
            TEST_MODEL = "gpt-4o-mini"  # Example model
            client = new_openai_client(TEST_MODEL)
            print("OpenAIClient created successfully.")

            # Example query
            try:
                # Use default temp scale (2.0)
                opts = Options(temperature=1.0, max_tokens=100)
                response = client.query_text(
                    "You are a poetic assistant.",
                    ["Write a short haiku about clouds."],
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

            except ValueError as e:
                print(f"An unexpected error occurred during query: {e}")

            client.close()
            print("\nClient closed.")

        except ValueError as e:
            print(f"Configuration Error: {e}")
