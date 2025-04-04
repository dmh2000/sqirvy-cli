#!/usr/bin/env python3

"""
Command-line argument parsing for Sqirvy CLI.
"""

import argparse
from .sqirvy.context import SUPPORTED_COMMANDS


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
