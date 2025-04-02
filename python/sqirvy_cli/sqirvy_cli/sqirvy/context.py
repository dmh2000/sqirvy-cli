#!/usr/bin/env python3

"""
Sqirvy CLI Context Module.

This module defines the Context dataclass that encapsulates all information needed
for executing a sqirvy command.
"""
import sys
import os
from dataclasses import dataclass
from typing import List, Optional
from sqirvy.models import get_provider_name, get_model_alias
from sqirvy.prompts import code_prompt, plan_prompt, query_prompt, review_prompt

system_prompts = {
    "query": query_prompt,
    "plan": plan_prompt,
    "code": code_prompt,
    "review": review_prompt,
}


SUPPORTED_COMMANDS = [
    "query",
    "plan",
    "code",
    "review",
    "help",
]


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
    prompts: List[str]

    def print(self):
        """Print the contents of the context in a readable format."""
        print(f"Command     : {self.command}")
        print(f"Model       : {self.model}")
        print(f"Provider    : {self.provider}")
        print(f"Temperature : {self.temperature}")
        print(f"Files/URLs  : {self.files}")
        print(f"System      : {self.system}")
        print(f"Messages    : {len(self.prompts)}")


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

    if files is None:
        files = []

    # get the system prompt based on the command provided
    # validate the command
    if command not in SUPPORTED_COMMANDS:
        print(
            f"Invalid command: {command}. Supported commands are: {SUPPORTED_COMMANDS}"
        )
        sys.exit(1)
    system_prompt = system_prompts.get(command)

    # validate the model
    if not model:
        print("Model is required.")
        sys.exit(1)
    model = get_model_alias(model)

    # get the provider based on the model
    provider = get_provider_name(model)

    # validate the temperature
    if temperature <= 0 or temperature > 1.0:
        print("Temperature must be in range (0..1.0]")
        sys.exit(1)
    # validate the prompt
    if not prompt or prompt == "":
        prompt = "hello world"

    # populate the prompts
    prompts = []
    prompts.append(prompt)
    for file in files:
        try:
            # check if file exists and is a file
            if not os.path.isfile(file):
                print(f"File '{file}' does not exist or is not a file.")
                raise FileNotFoundError
            with open(file, "r", encoding="utf-8") as f:
                p = f.read()
                prompts.append(p)
        except FileNotFoundError:
            print(f"File '{file}' not found.")
            raise

    return Context(
        command=command,
        model=model,
        provider=provider,
        temperature=temperature,
        files=files,
        system=system_prompt,
        prompts=prompts,
    )
