"""
Tests for the cli_args.py module using pytest.
"""

import sys
import pytest
from unittest.mock import patch

# Import the parse_arguments function
# Note: We need to use relative imports based on how the package is structured
from sqirvy_cli.sqirvy_cli.cli_args import parse_arguments
from sqirvy_cli.sqirvy_cli.sqirvy.context import SUPPORTED_COMMANDS


class TestCliArgs:
    """Test the CLI argument parsing functionality."""

    @pytest.mark.parametrize(
        "test_args, expected",
        [
            # Basic query command with all parameters
            (
                ["-c", "query", "-m", "test-model", "-t", "0.5", "file1.txt", "http://example.com"],
                {
                    "command": "query",
                    "model": "test-model",
                    "temperature": 0.5,
                    "files_or_urls": ["file1.txt", "http://example.com"],
                },
            ),
            # Plan command with default temperature
            (
                ["-c", "plan", "-m", "claude-model", "file2.md"],
                {
                    "command": "plan",
                    "model": "claude-model",
                    "temperature": 1.0,
                    "files_or_urls": ["file2.md"],
                },
            ),
            # Code command with only files/URLs (using -c flag)
            (
                ["-c", "code", "config.json", "data.csv"],
                {
                    "command": "code",
                    "model": None,
                    "temperature": 1.0,
                    "files_or_urls": ["config.json", "data.csv"],
                },
            ),
            # Review command with only flags and no files/URLs
            (
                ["-c", "review", "-m", "gpt-model", "-t", "0.9"],
                {
                    "command": "review", 
                    "model": "gpt-model", 
                    "temperature": 0.9, 
                    "files_or_urls": []
                },
            ),
            # Default command (query) with no arguments
            (
                [],
                {
                    "command": "query",
                    "model": None,
                    "temperature": 1.0,
                    "files_or_urls": [],
                },
            ),
            # Using long form arguments
            (
                ["--command", "plan", "--model", "test-model", "--temperature", "0.7", "file.txt"],
                {
                    "command": "plan",
                    "model": "test-model",
                    "temperature": 0.7,
                    "files_or_urls": ["file.txt"],
                },
            ),
        ],
    )
    def test_parse_arguments_valid(self, test_args, expected):
        """Test that valid arguments are parsed correctly."""
        with patch("sys.argv", ["sqirvy_cli.py"] + test_args):
            args = parse_arguments()
            assert args.command == expected["command"]
            assert args.model == expected["model"]
            assert args.temperature == expected["temperature"]
            assert args.files_or_urls == expected["files_or_urls"]

    def test_all_commands_exist(self):
        """Test that all supported commands can be parsed."""
        for command in SUPPORTED_COMMANDS:
            with patch("sys.argv", ["sqirvy_cli.py", "-c", command]):
                args = parse_arguments()
                assert args.command == command
                assert args.model is None
                assert args.temperature == 1.0
                assert args.files_or_urls == []

    # Note: The current implementation doesn't validate temperature range in the argument parser
    # It's validated later in create_context, so we can't test it here directly
    # We'll modify this test to check that the parser accepts these values
    @pytest.mark.parametrize(
        "temperature, expected_value",
        [
            ("-0.1", -0.1),   # Negative temperature
            ("0.0", 0.0),     # Zero temperature
            ("1.5", 1.5),     # Temperature too high
        ],
    )
    def test_temperature_parsing(self, temperature, expected_value):
        """Test that temperature values are correctly parsed."""
        with patch("sys.argv", ["sqirvy_cli.py", "-t", temperature]):
            args = parse_arguments()
            assert args.temperature == expected_value

    def test_invalid_temperature_format(self):
        """Test that non-numeric temperature raises error."""
        with patch("sys.argv", ["sqirvy_cli.py", "-t", "abc"]):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_help_flag(self):
        """Test that help flag is properly recognized."""
        with patch("sys.argv", ["sqirvy_cli.py", "--help"]):
            args = parse_arguments()
            assert args.help is True