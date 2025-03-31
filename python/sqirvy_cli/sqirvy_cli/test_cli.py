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

# Use relative import because test_cli.py and main.py are in the same package
from .main import parse_arguments, SUPPORTED_COMMANDS


class TestSqirvyCliArgs(unittest.TestCase):
    """Test the argument parsing of the sqirvy-cli with subcommands."""

    def test_query_command_full(self):
        """Test 'query' command with all arguments."""
        test_args = [
            "query",
            "-m",
            "test-model",
            "-t",
            "0.5",
            "file1.txt",
            "http://example.com",
        ]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "query")
            self.assertEqual(args.model, "test-model")
            self.assertEqual(args.temperature, 0.5)
            self.assertEqual(args.files_or_urls, ["file1.txt", "http://example.com"])

    def test_plan_command_default_temp(self):
        """Test 'plan' command with default temperature."""
        test_args = ["plan", "-m", "another-model", "file2.md"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "plan")
            self.assertEqual(args.model, "another-model")
            self.assertEqual(args.temperature, 1.0)  # Default value
            self.assertEqual(args.files_or_urls, ["file2.md"])

    def test_code_command_only_files(self):
        """Test 'code' command with only files/URLs (and default flags)."""
        test_args = ["code", "config.json", "data.csv"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "code")
            self.assertIsNone(args.model)  # Model is optional for now
            self.assertEqual(args.temperature, 1.0)  # Default value
            self.assertEqual(args.files_or_urls, ["config.json", "data.csv"])

    def test_review_command_no_files(self):
        """Test 'review' command with only flags and no files/URLs."""
        test_args = ["review", "-m", "flag-model", "-t", "0.9"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "review")
            self.assertEqual(args.model, "flag-model")
            self.assertEqual(args.temperature, 0.9)
            self.assertEqual(args.files_or_urls, [])

    def test_all_commands_exist(self):
        """Test that all supported commands can be parsed without files/flags."""
        for command in SUPPORTED_COMMANDS:
            with self.subTest(command=command):
                test_args = [command]
                with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
                    args = parse_arguments()
                    self.assertEqual(args.command, command)
                    self.assertIsNone(args.model)
                    self.assertEqual(args.temperature, 1.0)
                    self.assertEqual(args.files_or_urls, [])

    def test_missing_command(self):
        """Test error when no command is provided."""
        test_args = ["-m", "some-model"]  # No command
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            with self.assertRaises(SystemExit):
                with patch("argparse.ArgumentParser._print_message"):  # Suppress error
                    parse_arguments()

    def test_invalid_command(self):
        """Test error when an invalid command is provided."""
        test_args = ["invalid_command", "-m", "some-model"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            with self.assertRaises(SystemExit):
                with patch("argparse.ArgumentParser._print_message"):  # Suppress error
                    parse_arguments()

    def test_temp_edge_cases_with_command(self):
        """Test temperature edge cases with a command."""
        # Valid edge case: slightly above zero (valid min is 0 < temp)
        test_args_near_zero = ["query", "-t", "0.001"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args_near_zero):
            args = parse_arguments()
            self.assertEqual(args.command, "query")
            self.assertEqual(args.temperature, 0.001)

        # Valid edge case: exactly 1.0 (valid max is temp <= 1.0)
        test_args_one = ["plan", "-t", "1.0"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args_one):
            args = parse_arguments()
            self.assertEqual(args.command, "plan")
            self.assertEqual(args.temperature, 1.0)

    def test_invalid_temp_low_with_command(self):
        """Test invalid temperature (too low) with a command."""
        # Test negative temperature
        test_args = ["code", "-t", "-0.1"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            with self.assertRaises(SystemExit):
                with patch("argparse.ArgumentParser._print_message"):
                    parse_arguments()
                    
        # Test exactly zero (invalid: requirement is 0 < temp)
        test_args_zero = ["code", "-t", "0.0"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args_zero):
            with self.assertRaises(SystemExit):
                with patch("argparse.ArgumentParser._print_message"):
                    parse_arguments()

    def test_invalid_temp_high_with_command(self):
        """Test invalid temperature (too high) with a command."""
        test_args = ["review", "-t", "2.0"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            with self.assertRaises(SystemExit):
                with patch("argparse.ArgumentParser._print_message"):
                    parse_arguments()

    def test_invalid_temp_format_with_command(self):
        """Test invalid temperature (not a float) with a command."""
        test_args = ["query", "-t", "abc"]
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            with self.assertRaises(SystemExit):
                with patch("argparse.ArgumentParser._print_message"):
                    parse_arguments()


if __name__ == "__main__":
    unittest.main()
