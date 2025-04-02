"""
sqirvy: Model Management

Contains model-to-provider mappings, token limits, and utility functions
for working with different AI models across supported providers.
"""

from typing import List, Dict, NamedTuple

# --- Constants ---

# Supported AI providers
ANTHROPIC = "anthropic"
GEMINI = "gemini"
OPENAI = "openai"
LLAMA = "llama"

# Default max tokens if not specified for a model
MAX_TOKENS_DEFAULT = 4096

# --- Model Mappings ---

MODEL_ALIAS: Dict[str, str] = {
    "claude-3-7-sonnet": "claude-3-7-sonnet-latest",
    "claude-3-5-sonnet": "claude-3-5-sonnet-latest",
    "claude-3-5-haiku": "claude-3-5-haiku-latest",
    "claude-3-opus": "claude-3-opus-latest",
}

# Maps model names (strings) to their respective providers (strings)
MODEL_TO_PROVIDER: Dict[str, str] = {
    # anthropic models
    "claude-3-7-sonnet-20250219": ANTHROPIC,
    "claude-3-5-sonnet-20241022": ANTHROPIC,
    "claude-3-7-sonnet-latest": ANTHROPIC,
    "claude-3-5-sonnet-latest": ANTHROPIC,
    "claude-3-5-haiku-latest": ANTHROPIC,
    "claude-3-haiku-20240307": ANTHROPIC,
    "claude-3-opus-latest": ANTHROPIC,
    "claude-3-opus-20240229": ANTHROPIC,
    # google gemini models
    "gemini-2.0-flash": GEMINI,
    "gemini-1.5-flash": GEMINI,
    "gemini-1.5-pro": GEMINI,
    "gemini-2.0-flash-thinking-exp": GEMINI,
    "gemini-2.5-pro-exp-03-25": GEMINI,
    # openai models
    "gpt-4o": OPENAI,
    "gpt-4o-mini": OPENAI,
    "gpt-4-turbo": OPENAI,
    # llama models
    "llama3.3-70b": LLAMA,
}

# Maps model names (strings) to their maximum token limits (integers)
MODEL_TO_MAX_TOKENS: Dict[str, int] = {
    # anthropic models
    "claude-3-7-sonnet-latest": MAX_TOKENS_DEFAULT,
    "claude-3-5-sonnet-latest": MAX_TOKENS_DEFAULT,
    "claude-3-5-haiku-latest": MAX_TOKENS_DEFAULT,
    "claude-3-opus-latest": 4096,
    # google gemini models
    "gemini-2.0-flash": MAX_TOKENS_DEFAULT,
    "gemini-1.5-flash": MAX_TOKENS_DEFAULT,
    "gemini-1.5-pro": MAX_TOKENS_DEFAULT,
    # openai models
    "gpt-4o": 4096,
    "gpt-4o-mini": 4096,
    "gpt-4-turbo": 4096,
    # llama models
    "llama3.3-70b": MAX_TOKENS_DEFAULT,
}

# --- Utility Functions ---


def get_model_alias(model: str) -> str:
    """Resolves a model name alias if one exists."""
    return MODEL_ALIAS.get(model, model)


def get_model_list() -> List[str]:
    """Returns a list of all supported model names."""
    return list(MODEL_TO_PROVIDER.keys())


class ModelProviderInfo(NamedTuple):
    """Structure to hold model and provider information."""

    model: str
    provider: str


def get_model_provider_list() -> List[ModelProviderInfo]:
    """Returns a list of ModelProviderInfo objects."""
    return [
        ModelProviderInfo(model=model, provider=provider)
        for model, provider in MODEL_TO_PROVIDER.items()
    ]


def get_provider_name(model: str) -> str:
    """
    Returns the provider name for a given model identifier.
    """
    resolved_model = get_model_alias(model)
    provider = MODEL_TO_PROVIDER.get(resolved_model)
    if provider:
        return provider
    raise ValueError(f"Unrecognized provider: {resolved_model}:{provider}")


def get_max_tokens(model: str) -> int:
    """
    Returns the maximum token limit for a given model identifier.

    Args:
        model: The model name (string).

    Returns:
        The maximum token limit (int), defaulting to MAX_TOKENS_DEFAULT
        if the model is not found in the specific mapping.
    """
    resolved_model = get_model_alias(model)
    return MODEL_TO_MAX_TOKENS.get(resolved_model, MAX_TOKENS_DEFAULT)


# --- Example Usage (optional) ---
if __name__ == "__main__":
    print("--- Supported Models ---")
    all_models = get_model_list()
    print(f"Total models: {len(all_models)}")
    # print(all_models)

    print("\n--- Model Providers ---")
    provider_list = get_model_provider_list()
    for info in sorted(provider_list, key=lambda x: (x.provider, x.model)):
        print(f"Model: {info.model:<30} Provider: {info.provider}")

    print("\n--- Max Tokens ---")
    test_models = [
        "gpt-4o",
        "claude-3-opus-latest",
        "gemini-1.5-flash",
        "unknown-model",
        "claude-3-opus",
    ]
    for m in test_models:
        try:
            provider = get_provider_name(m)
            max_t = get_max_tokens(m)
            alias = get_model_alias(m)
            print(
                f"Model: {m:<20} (Alias: {alias:<25}) Provider: {provider:<10} Max Tokens: {max_t}"
            )
        except ValueError as e:
            print(f"Model: {m:<20} Error: {e}")
