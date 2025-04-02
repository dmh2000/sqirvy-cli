#!/usr/bin/env python3

"""
Sqirvy-cli: A command-line tool to interact with LLMs.

Receives input from stdin and command-line arguments (flags, filenames, URLs).
Prints the parsed arguments and stdin content to stdout.
"""

import argparse
import sys
from sqirvy.context import create_context, SUPPORTED_COMMANDS
from sqirvy.client import new_client


def parse_arguments():
    """Parse command line arguments in the format:
    sqirvy_cli <command> <model> <temperature> [filenames..., urls...]
    """
    parser = argparse.ArgumentParser(
        description="Sqirvy CLI - Interact with LLMs", add_help=False
    )

    # Required command positional argument
    parser.add_argument(
        "-c",
        "--command",
        required=False,
        choices=SUPPORTED_COMMANDS,
        type=str,
        default="help",
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


command_help = {
    "query": "Query the LLM with a prompt",
    "plan": "Plan a task using the LLM",
    "code": "Generate code snippets with the LLM",
    "review": "Review code or text with the LLM",
    "help": "Show this help message",
}


def print_help():
    """Print the help message."""
    print("Sqirvy CLI - Command Line Interface for LLMs")
    print("Usage: sqirvy_cli <command> [options] [filenames... urls...]")
    print("Commands:")
    print("Options:")
    print("  -c | --command    Command To Execute")
    for cmd in SUPPORTED_COMMANDS:
        print(f"       {cmd} : {command_help[cmd]}")
    print("  -m, --model       Model name to use (default: None)")
    print("  -t, --temperature Temperature value (0-1.0) (default: 1.0)")
    print("  filenames...      List of files and/or URLs to process")


def main():
    """Main execution function."""
    args = parse_arguments()

    if args.command == "help":
        print_help()
        sys.exit(0)

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
    # context.print()

    client = new_client(context)

    # execute the query
    response = client.query_text(context)
    print(response)


if __name__ == "__main__":
    main()
