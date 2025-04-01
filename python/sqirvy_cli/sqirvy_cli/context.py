#!/usr/bin/env python3

"""
Sqirvy CLI Context Module.

This module defines the Context dataclass that encapsulates all information needed
for executing a sqirvy command.
"""
import sys
from dataclasses import dataclass
from typing import List, Optional
from .sqirvy.models import get_provider_name, get_model_alias

system_prompts = {
    "query": "prompts/query.txt",
    "plan": "prompts/plan.txt",
    "code": "prompts/code.txt",
    "review": "prompts/review.txt",
}


@dataclass
class Context:
    """
    Context for executing a sqirvy command.

    Encapsulates all the information needed for executing a command, including
    the command type, model selection, files/URLs, and prompt information.

    Attributes:
        command: The command to execute (query, plan, code, review).
        model: The AI model to use.
        provider: The AI provider (anthropic, openai, gemini, llama).
        temperature: The temperature setting for the model.
        files: List of file paths and/or URLs to process.
        system: The system message to provide context to the AI.
        prompt: The user prompt to send to the AI.
    """

    command: str
    model: str
    provider: str
    temperature: float
    files: List[str]
    system: str
    prompt: str

    def print(self):
        """Print the contents of the context in a readable format."""
        print(f"Command     : {self.command}")
        print(f"Model       : {self.model}")
        print(f"Provider    : {self.provider}")
        print(f"Temperature : {self.temperature}")
        print(f"Files/URLs  : {self.files}")
        print(f"System      : {self.system}")
        print(f"Prompt      : {self.prompt if self.prompt else '<empty>'}")


def create_context(
    command: str,
    model: str,
    temperature: float,
    files: Optional[List[str]] = None,
    prompt: str = "",
) -> Context:
    """
    Create a new Context instance.

    Args:
        command: The command to execute (query, plan, code, review).
        model: The AI model to use.
        provider: The AI provider (anthropic, openai, gemini, llama).
        temperature: The temperature setting for the model.
        files: List of file paths and/or URLs to process.
        system: The system message to provide context to the AI.
        prompt: The user prompt to send to the AI.

    Returns:
        A new Context instance with the provided values.
    """

    from .main import SUPPORTED_COMMANDS

    if files is None:
        files = []

    # get the system prompt based on the command provided
    system_file = system_prompts.get(command)
    if system_file:
        try:
            with open(system_file, "r", encoding="ascii") as f:
                system_prompt = f.read()
        except FileNotFoundError:
            print(f"System prompt file '{system_file}' not found.")
            sys.exit(1)
    else:
        print(f"Unsupported command: {command}")
        sys.exit(1)

    # validate the command
    if command not in SUPPORTED_COMMANDS:
        print(
            f"Invalid command: {command}. Supported commands are: {SUPPORTED_COMMANDS}"
        )
        sys.exit(1)

    # validate the model
    if not model:
        print("Model is required.")
        sys.exit(1)
    model = get_model_alias(model)

    # validate the temperature
    if temperature <= 0 or temperature > 1.0:
        print("Temperature must be in range (0..1.0]")
        sys.exit(1)
    # validate the prompt
    if not prompt or prompt == "":
        prompt = "hello world"

    # validate the files
    prompts = []
    for file in files:
        try:
            with open(file, "r", encoding="ascii") as f:
                prompts.append(f.read())
        except FileNotFoundError:
            print(f"File '{file}' not found.")
            sys.exit(1)

    # validate the provider
    if not get_provider_name(model):
        print(
            f"Invalid model: {model}. Supported models are: {list(get_provider_name)}"
        )
        sys.exit(1)
    # get the provider based on the model
    provider = get_provider_name(model)

    return Context(
        command=command,
        model=model,
        provider=provider,
        temperature=temperature,
        files=files,
        system=system_prompt,
        prompt=prompt,
    )
