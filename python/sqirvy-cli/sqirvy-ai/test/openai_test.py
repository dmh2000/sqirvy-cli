from ..openai_client import NewOpenAIClient, Options
import os



# Example Usage (optional, for testing)
if __name__ == "__main__":
    # Ensure OPENAI_API_KEY (and optionally OPENAI_BASE_URL) is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping example: OPENAI_API_KEY not set.")
    else:
        try:
            test_model = "gpt-4o-mini" # Example model
            client = NewOpenAIClient(test_model)
            print("OpenAIClient created successfully.")

            # Example query
            try:
                # Use default temp scale (2.0)
                opts = Options(temperature=70, max_tokens=100)
                response = client.QueryText(
                    "You are a poetic assistant.",
                    ["Write a short haiku about clouds."],
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
