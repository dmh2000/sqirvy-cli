import unittest
import os
from unittest.mock import patch

# Add sqirvy_ai to the path if necessary, or adjust imports based on project structure
# Assuming tests are run from a location where 'sqirvy_ai' is discoverable
# (e.g., from the 'python/sqirvy-cli' directory after setting PYTHONPATH,
# or if 'src' is added to sys.path)
try:
    from sqirvy_ai.anthropic import NewAnthropicClient, AnthropicClient, ANTHROPIC_TEMP_SCALE
    from sqirvy_ai.client import Options, MinTemperature, MaxTemperature
except ImportError:
    # If running directly from src or tests directory, adjust path
    import sys
    # Assuming the structure is python/sqirvy-cli/src and python/sqirvy-cli/sqirvy_ai
    # Adjust based on your actual structure and how tests are run
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from sqirvy_ai.anthropic import NewAnthropicClient, AnthropicClient, ANTHROPIC_TEMP_SCALE
    from sqirvy_ai.client import Options, MinTemperature, MaxTemperature


# Check if the API key is available in the environment
ANTHROPIC_API_KEY_AVAILABLE = os.getenv("ANTHROPIC_API_KEY") is not None
ASSISTANT_PROMPT = "you are a helpful assistant"

@unittest.skipIf(not ANTHROPIC_API_KEY_AVAILABLE, "ANTHROPIC_API_KEY environment variable not set")
class TestAnthropicClient(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        try:
            self.client = NewAnthropicClient()
        except ValueError as e:
            self.fail(f"Failed to create Anthropic client in setUp: {e}")
        except Exception as e:
             self.fail(f"Unexpected error creating Anthropic client in setUp: {e}")

        # Use a known, available, and fast model for testing
        self.model = "claude-3-haiku-20240307"
        # Use temperature 0 for deterministic output in tests
        self.options = Options(temperature=0, max_tokens=100, temperature_scale=ANTHROPIC_TEMP_SCALE)

    def test_query_text_basic(self):
        """Test QueryText with a basic prompt."""
        prompt = ["Say 'Hello, World!'"]
        try:
            response = self.client.QueryText(ASSISTANT_PROMPT, prompt, self.model, self.options)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0, "QueryText returned an empty response")
            # Anthropic models might add conversational filler, so check for contains
            self.assertIn("Hello, World!", response, "Response did not contain expected content")
        except Exception as e:
            self.fail(f"QueryText failed unexpectedly: {e}")

    def test_query_text_empty_prompt_list(self):
        """Test QueryText with an empty list of prompts."""
        prompt = []
        # Expect a ValueError because the prompts list is empty
        with self.assertRaisesRegex(ValueError, "Prompts list cannot be empty"):
             self.client.QueryText(ASSISTANT_PROMPT, prompt, self.model, self.options)

    def test_query_text_invalid_temperature_low(self):
        """Test QueryText with temperature below minimum."""
        invalid_temp = MinTemperature - 10
        options_invalid = Options(temperature=invalid_temp, temperature_scale=ANTHROPIC_TEMP_SCALE)
        with self.assertRaisesRegex(ValueError, "Temperature must be between"):
            self.client.QueryText(ASSISTANT_PROMPT, ["Test"], self.model, options_invalid)

    def test_query_text_invalid_temperature_high(self):
        """Test QueryText with temperature above maximum."""
        invalid_temp = MaxTemperature + 10
        options_invalid = Options(temperature=invalid_temp, temperature_scale=ANTHROPIC_TEMP_SCALE)
        with self.assertRaisesRegex(ValueError, "Temperature must be between"):
            self.client.QueryText(ASSISTANT_PROMPT, ["Test"], self.model, options_invalid)

    # Add more tests here as needed
    # e.g., test different temperatures, max_tokens, specific model behaviors, error handling from API

    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'client') and self.client:
            self.client.Close() # Call close, even if it's a no-op

if __name__ == '__main__':
    unittest.main()
