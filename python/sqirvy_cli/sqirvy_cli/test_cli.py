"""
test cli arguments
"""

import unittest
from unittest.mock import patch


# Add the parent directory to sys.path to allow importing sqirvy_cli
# This assumes the test script is run from the project root or python/test directory
# import os
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# cli_dir = os.path.join(parent_dir, 'src')
# Ensure the src directory is discoverable if running tests from a different location
# A simpler approach if tests are run relative to the python directory:
# sys.path.insert(0, "src") # No longer needed with relative import

# Use relative import because test_cli.py and main.py are in the same directory
from .main import parse_arguments


class TestSqirvyCliArgs(unittest.TestCase):
    """Test the argument parsing of the sqirvy-cli."""

    def test_parse_arguments_full(self):
        """Test parsing with all arguments."""
        test_args = ["-m", "test-model", "-t", "0.5", "file1.txt", "http://example.com"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.model, "test-model")
            self.assertEqual(args.temperature, 0.5)
            self.assertEqual(args.files_or_urls, ["file1.txt", "http://example.com"])

    def test_parse_arguments_default_temp(self):
        """Test parsing with default temperature."""
        test_args = ["-m", "another-model", "file2.md"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.model, "another-model")
            self.assertEqual(args.temperature, 1.0)  # Default value
            self.assertEqual(args.files_or_urls, ["file2.md"])

    def test_parse_arguments_only_files(self):
        """Test parsing with only files/URLs."""
        test_args = ["config.json", "data.csv"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertIsNone(args.model)
            self.assertEqual(args.temperature, 1.0)  # Default value
            self.assertEqual(args.files_or_urls, ["config.json", "data.csv"])

    def test_parse_arguments_no_extra_args(self):
        """Test parsing with only flags."""
        test_args = ["-m", "flag-model", "-t", "1.9"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.model, "flag-model")
            self.assertEqual(args.temperature, 1.9)
            self.assertEqual(args.files_or_urls, [])

    def test_parse_arguments_temp_edge_cases(self):
        """Test temperature edge cases."""
        # Valid edge case: 0.0
        test_args_zero = ["-t", "0.0"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args_zero):
            args = parse_arguments()
            self.assertEqual(args.temperature, 0.0)

        # Valid edge case: close to 2.0
        test_args_near_two = ["-t", "1.999"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args_near_two):
            args = parse_arguments()
            self.assertEqual(args.temperature, 1.999)

    def test_parse_arguments_invalid_temp_low(self):
        """Test invalid temperature (too low)."""
        test_args = ["-t", "-0.1"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            # Argparse calls sys.exit on error, which raises SystemExit
            with self.assertRaises(SystemExit):
                with patch(
                    "argparse.ArgumentParser._print_message"
                ):  # Suppress error message print
                    parse_arguments()
            # No need to assert on cm.exception message unless specifically required,
            # catching SystemExit confirms argparse's error handling was triggered.

    def test_parse_arguments_invalid_temp_high(self):
        """Test invalid temperature (too high)."""
        test_args = ["-t", "2.0"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            # Argparse calls sys.exit on error, which raises SystemExit
            with self.assertRaises(SystemExit):
                with patch(
                    "argparse.ArgumentParser._print_message"
                ):  # Suppress error message print
                    parse_arguments()

    def test_parse_arguments_invalid_temp_format(self):
        """Test invalid temperature (not a float)."""
        test_args = ["-t", "abc"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            # Argparse calls sys.exit on error, which raises SystemExit
            with self.assertRaises(SystemExit):
                with patch(
                    "argparse.ArgumentParser._print_message"
                ):  # Suppress error message print
                    parse_arguments()


if __name__ == "__main__":
    unittest.main()
