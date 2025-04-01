#!/usr/bin/env python3

"""
Sqirvy-cli: A command-line tool to interact with LLMs.

Receives input from stdin and command-line arguments (flags, filenames, URLs).
Prints the parsed arguments and stdin content to stdout.
"""

import argparse
import sys
from .context import create_context

# from .sqirvy.client import new_client


SUPPORTED_COMMANDS = ["query", "plan", "code", "review"]


def parse_arguments():
    """Parse command line arguments in the format:
    sqirvy_cli <command> <model> <temperature> [filenames..., urls...]
    """
    parser = argparse.ArgumentParser(description="Sqirvy CLI - Interact with LLMs")

    # Required command positional argument
    parser.add_argument(
        "command",
        type=str,
        choices=SUPPORTED_COMMANDS,
        help="Command to execute: query, plan, code, or review",
    )

    # Model parameter with short and long form
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=False,
        default=None,
        help="Model name to use",
    )

    # Temperature parameter with short and long form
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        required=False,
        default=1.0,
        help="Temperature value (0-1.0)",
    )

    # Any number of filenames or URLs after the other arguments
    parser.add_argument(
        "files_or_urls", nargs="*", help="List of files and/or URLs to process"
    )

    args = parser.parse_args()

    # Validate temperature is in range (0 < temperature <= 1.0)
    if args.temperature <= 0 or args.temperature > 1.0:
        parser.error("Temperature must be in range (0..1.0]")

    return args


def main():
    """Main execution function."""
    args = parse_arguments()

    # Read from stdin only if it's not connected to a TTY (i.e., piped/redirected)
    stdin_content = ""
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read()

    # Create a context object with the parsed arguments
    # For now, use placeholders for provider, system and prompt
    context = create_context(
        command=args.command,
        model=args.model,
        temperature=args.temperature,
        files=args.files_or_urls,
        prompt=stdin_content,
    )

    # Print the context information
    context.print()

    # client = new_client(context.model)


if __name__ == "__main__":
    main()
