"""
Environment variable helper functions for the sqirvy module.

Centralizes environment variable access with consistent error handling and defaults.
"""

import os
from typing import Optional

def get_env_var(name: str, required: bool = True, default: Optional[str] = None) -> Optional[str]:
    """
    Get an environment variable with consistent error handling.

    Args:
        name: The name of the environment variable.
        required: If True, raises ValueError when variable is not set.
        default: Default value if not required and variable is not set.

    Returns:
        The environment variable value, or default if not required and not set.

    Raises:
        ValueError: If the variable is required but not set.
    """
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"{name} environment variable not set")
    return value

def get_api_key(provider: str) -> str:
    """
    Get the API key for a specific provider.

    Args:
        provider: The provider name (anthropic, openai, gemini, llama).

    Returns:
        The API key string.

    Raises:
        ValueError: If the API key is not set.
    """
    env_var_name = f"{provider.upper()}_API_KEY"
    return get_env_var(env_var_name, required=True)

def get_base_url(provider: str, default: Optional[str] = None) -> str:
    """
    Get the base URL for a specific provider.

    Args:
        provider: The provider name (anthropic, openai, gemini, llama).
        default: Default base URL if not set in environment.

    Returns:
        The base URL string.

    Raises:
        ValueError: If the base URL is required but not set.
    """
    env_var_name = f"{provider.upper()}_BASE_URL"
    required = default is None  # Only required if no default is provided
    return get_env_var(env_var_name, required=required, default=default)