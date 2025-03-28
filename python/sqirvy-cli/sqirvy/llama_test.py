"""
Llama client test
"""

import os
from .llama_client import new_llama_client, Options

# Example Usage (optional, for testing)
if __name__ == "__main__":
    # Ensure LLAMA_API_KEY and LLAMA_BASE_URL are set
    if not os.getenv("LLAMA_API_KEY") or not os.getenv("LLAMA_BASE_URL"):
        print("Skipping example: LLAMA_API_KEY or LLAMA_BASE_URL not set.")
    else:
        try:
            TEST_MODEL = "llama3.3-70b"
            client = new_llama_client(TEST_MODEL)
            print("LlamaClient created successfully.")

            # Example query
            try:
                # Use default temp scale (2.0)
                opts = Options(temperature=1.0, max_tokens=100)
                # Ensure this model name matches what your Llama endpoint expects
                response = client.query_text(
                    "You are a helpful coding assistant.",
                    ["Explain the difference between a list and a tuple in Python."],
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
