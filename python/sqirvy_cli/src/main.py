#!/usr/bin/env python3

"""
Sqirvy-cli: A command-line tool to interact with LLMs.

Receives input from stdin and command-line arguments (flags, filenames, URLs).
Prints the parsed arguments and stdin content to stdout.
"""

import argparse
import sys

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Sqirvy-cli: Interact with LLMs.",
        epilog="Input is read from stdin. Additional arguments are treated as filenames or URLs."
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        help="Specify the LLM model name."
    )

    def check_temperature(value):
        """Validate temperature range."""
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

    # Capture all remaining arguments as filenames/URLs
    parser.add_argument(
        'files_or_urls',
        nargs='*',
        help='Optional filenames or URLs to include in the prompt.'
    )

    args = parser.parse_args()
    return args

def main():
    """Main execution function."""
    args = parse_arguments()

    # Read from stdin
    stdin_content = sys.stdin.read()

    # Print collected information
    print("--- Arguments ---")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Files/URLs: {args.files_or_urls}")
    print("--- Stdin Content ---")
    print(stdin_content)
    print("-------------------")

if __name__ == "__main__":
    main()
