# Example Usage (optional, for testing)
if __name__ == "__main__":
    from .anthropic_client import NewAnthropicClient, Options, ANTHROPIC_TEMP_SCALE
    import os

    # Ensure ANTHROPIC_API_KEY is set in your environment for this to work
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Skipping example: ANTHROPIC_API_KEY not set.")
    else:
        try:
            test_model = "claude-3-haiku-20240307"  # Use a fast model for testing
            client = NewAnthropicClient(test_model)
            print("AnthropicClient created successfully.")

            # Example query
            try:
                # Use temperature 0 for deterministic output in example
                # Explicitly set the correct scale for clarity, though QueryText handles it
                opts = Options(
                    temperature=1.0,
                    max_tokens=2048,
                    temperature_scale=ANTHROPIC_TEMP_SCALE,
                )
                response = client.QueryText(
                    "You are a helpful assistant.",
                    ["Say 'Hello, World!'"],
                    opts,
                )
                print(f"\nQuery Response from {test_model}:")
                print(response)

                # Test empty prompt error
                print("\nTesting empty prompt error:")
                try:
                    client.QueryText("System", [], opts)
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
