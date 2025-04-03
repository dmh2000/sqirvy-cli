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
from sqirvy.models import print_providers_with_models


def parse_arguments():
    """Parse command line arguments in the format:
    sqirvy_cli <command> <model> <temperature> [filenames..., urls...]
    """
    parser = argparse.ArgumentParser(
        description="Sqirvy CLI - Interact with LLMs", add_help=False
    )
    
    # Help arguments
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="Show help message and exit",
    )

    # Required command positional argument
    parser.add_argument(
        "-c",
        "--command",
        required=False,
        choices=SUPPORTED_COMMANDS,
        type=str,
        default="query",
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
    print("Usage: sqirvy_cli [options] [filenames... urls...]")
    print("Options:")
    print("  -h, --help        Show this help message and exit")
    print("  -c, --command     Command To Execute")
    for cmd in SUPPORTED_COMMANDS:
        print(f"       {cmd} : {command_help[cmd]}")
    print("  -m, --model       Model name to use (default: None)")
    print("  -t, --temperature Temperature value (0-1.0) (default: 1.0)")
    print("  filenames...      List of files and/or URLs to process")
    print_providers_with_models()


def main():
    """Main execution function."""
    args = parse_arguments()

    # Check for help flag first
    if args.help:
        print_help()
        sys.exit(0)
        
    # Check if model is provided
    if not args.model:
        print_help()
        print("\nError: Model is required")
        sys.exit(1)

    # Read from stdin only if it's not connected to a TTY (i.e., piped/redirected)
    stdin_content = ""
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read()

    try:
        # Create a context object with the parsed arguments
        context = create_context(
            command=args.command,
            model=args.model,
            temperature=args.temperature,
            files=args.files_or_urls,
            prompt=stdin_content,
        )
        
        # Create client and execute the query
        client = new_client(context)
        response = client.query_text(context)
        print(response)
    except ValueError as e:
        print_help()
        print(f"\nError: {str(e)}")
        sys.exit(1)
    except FileNotFoundError as e:
        print_help()
        print(f"\nError: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print_help()
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
