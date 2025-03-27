from ..gemini_client import NewGeminiClient, Options, GEMINI_TEMP_SCALE
import os

# Example Usage (optional, for testing)
if __name__ == "__main__":

    # Ensure GEMINI_API_KEY is set in your environment for this to work
    if not os.getenv("GEMINI_API_KEY"):
        print("Skipping example: GEMINI_API_KEY not set.")
    else:
        try:
            test_model = "gemini-1.5-flash" # Example model
            client = NewGeminiClient(test_model)
            print("GeminiClient created successfully.")

            # Example query
            try:
                # Use assumed temp scale for Gemini (1.0)
                opts = Options(temperature=70, max_tokens=100, temperature_scale=GEMINI_TEMP_SCALE)
                response = client.QueryText(
                    "You are a helpful assistant.",
                    ["What is the weather like today?"],
                    opts
                )
                print(f"\nQuery Response from {test_model}:")
                print(response)

                # Test empty prompt error
                print("\nTesting empty prompt error:")
                try:
                    client.QueryText("System", [],  opts)
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
