#!/usr/bin/env python3

"""
Sqirvy-cli: A command-line tool to interact with LLMs.

Receives input from stdin and command-line arguments (flags, filenames, URLs).
Prints the parsed arguments and stdin content to stdout.
"""

import argparse
import sys

SUPPORTED_COMMANDS = ["query", "plan", "code", "review"]

def parse_arguments():
    """Parses command-line arguments with subcommands."""
    parser = argparse.ArgumentParser(
        description="Sqirvy-cli: Interact with LLMs via commands.",
        epilog="Input is read from stdin. Files/URLs are provided after the command and flags."
    )

    # --- Common arguments for all commands ---
    parser.add_argument(
        "-m", "--model",
        type=str,
        # required=True, # Make model mandatory later if needed
        help="Specify the LLM model name (e.g., gpt-4o, claude-3-5-sonnet-latest)."
    )

    def check_temperature(value):
        """Validate temperature range [0.0, 2.0)."""
        try:
            fvalue = float(value)
        except ValueError as e:
            raise argparse.ArgumentTypeError(f"{value} is not a valid float") from e
        if not 0.0 <= fvalue < 2.0:
            raise argparse.ArgumentTypeError(f"{value} is not in the range [0.0, 2.0)")
        return fvalue

    parser.add_argument(
        "-t", "--temperature",
        type=check_temperature,
        default=1.0,
        help="Specify the LLM temperature (float in [0.0, 2.0), default: 1.0)."
    )

    # --- Subcommands ---
    subparsers = parser.add_subparsers(dest="command", required=True,
                                       help="The command to execute.")

    for command_name in SUPPORTED_COMMANDS:
        subparser = subparsers.add_parser(
            command_name,
            help=f"Execute the '{command_name}' command."
            # Add specific help/description for each command later if needed
        )
        # Add arguments specific to each command here, if any
        # For now, all commands accept files/URLs
        subparser.add_argument(
            'files_or_urls',
            nargs='*',
            help='Optional filenames or URLs relevant to the command.'
        )

    args = parser.parse_args()
    return args

def main():
    """Main execution function."""
    args = parse_arguments()

    # Read from stdin only if it's not connected to a TTY (i.e., piped/redirected)
    stdin_content = ""
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read()

    # Print collected information (adjust as needed for actual execution)
    print("--- Arguments ---")
    print(f"Command: {args.command}")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Files/URLs: {args.files_or_urls}") # This now comes from the subparser
    print("--- Stdin Content ---")
    print(stdin_content if stdin_content else "<empty>")
    print("-------------------")

if __name__ == "__main__":
    main()
