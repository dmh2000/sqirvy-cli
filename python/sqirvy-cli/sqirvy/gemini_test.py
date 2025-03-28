"""
Gemini Client Test
"""

import os
from .gemini_client import new_gemini_client, Options, GEMINI_TEMP_SCALE

# Example Usage (optional, for testing)
if __name__ == "__main__":

    # Ensure GEMINI_API_KEY is set in your environment for this to work
    if not os.getenv("GEMINI_API_KEY"):
        print("Skipping example: GEMINI_API_KEY not set.")
    else:
        try:
            TEST_MODEL = "gemini-1.5-flash"  # Example model
            client = new_gemini_client(TEST_MODEL)
            print("GeminiClient created successfully.")

            # Example query
            try:
                # Use assumed temp scale for Gemini (1.0)
                opts = Options(
                    temperature=1.0, max_tokens=100, temperature_scale=GEMINI_TEMP_SCALE
                )
                response = client.query_text(
                    "You are a helpful assistant.",
                    ["What is the weather like today?"],
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
