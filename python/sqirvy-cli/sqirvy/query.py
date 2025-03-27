from typing import List, Optional

# Import Langchain components needed for the helper function
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from .models import MODEL_TO_PROVIDER
from .client import MaxTemperature, MaxTokensDefault, MinTemperature, DefaultTempScale


class Options:
    """
    Configuration options for AI client queries.

    Attributes:
        temperature: Controls randomness (0-100). Defaults to MinTemperature if None.
        max_tokens: Maximum response tokens. Defaults to MaxTokensDefault if None or 0.
        temperature_scale: Provider-specific scaling factor for temperature (e.g., 1.0 for Anthropic, 2.0 for OpenAI). Defaults to DefaultTempScale if None.
    """

    def __init__(
        self,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        temperature_scale: Optional[float] = None,
    ):
        self.temperature = temperature if temperature is not None else MinTemperature
        self.max_tokens = (
            max_tokens
            if max_tokens is not None and max_tokens > 0
            else MaxTokensDefault
        )
        self.temperature_scale = (
            temperature_scale if temperature_scale is not None else DefaultTempScale
        )

    def __repr__(self):
        return f"Options(temperature={self.temperature}, max_tokens={self.max_tokens}, temperature_scale={self.temperature_scale})"


# --- LangChain Query Helper Function ---


def query_text_langchain(
    llm: BaseChatModel, system: str, prompts: List[str], options: Options
) -> str:
    """
    Helper function to execute a text query using a LangChain chat model.

    Args:
        llm: An instance of a LangChain BaseChatModel.
        system: The system prompt.
        prompts: A list of user prompts.
        model: The specific model identifier to use.
        options: An Options object containing temperature, max_tokens, etc.

    Returns:
        The text response from the AI model.

    Raises:
        ValueError: If prompts list is empty or temperature is out of range.
        Exception: Errors from the LangChain API call.
    """
    if not prompts:
        raise ValueError("Prompts list cannot be empty for text query.")

    # Validate and scale temperature
    temp = options.temperature
    if not MinTemperature <= temp <= MaxTemperature:
        raise ValueError(
            f"Temperature must be between {MinTemperature} and {MaxTemperature}, got {temp}"
        )

    # Use the provided scale, defaulting if necessary
    temp_scale = options.temperature_scale
    scaled_temperature = (temp * temp_scale) / MaxTemperature

    # Construct messages
    messages = [SystemMessage(content=system)]
    for p in prompts:
        messages.append(HumanMessage(content=p))

    # Prepare LangChain options
    langchain_options = {
        # model": model,
        "temperature": 0.5,
    }
    # # Add max_tokens if provided (LangChain uses 'max_tokens' generally,
    # # though some integrations might have specific names like 'max_tokens_to_sample')
    # if options.max_tokens > 0:
    #     # Use 'max_tokens' as the common parameter name
    #     langchain_options["max_tokens"] = int(options.max_tokens)

    try:
        # Make the API call using the passed llm object
        response = llm.invoke(messages, **langchain_options)

        # Extract content from response
        if hasattr(response, "content"):
            return response.content
        else:
            # Handle unexpected response structure
            raise ValueError("Failed to parse content from LLM response.")

    except Exception as e:
        # Catch and re-raise LangChain or API errors
        raise Exception(f"LangChain API query failed: {e}") from e
