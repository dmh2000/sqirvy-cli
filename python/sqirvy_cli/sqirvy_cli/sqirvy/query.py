"""
Helper function to execute a text query using a LangChain chat model.
"""

from typing import List

# Import Langchain components needed for the helper function
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from .client import (
    MAX_TEMPERATURE,
    MAX_TOKENS_DEFAULT,
    MIN_TEMPERATURE,
    Options,
)
from .context import Context

# --- LangChain Query Helper Function ---


def query_text_langchain(llm: BaseChatModel, context: Context) -> str:
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
        ValueError: If prompts list is empty.
        Exception: Errors from the LangChain API call.
    """
    if len(context.prompts) == 0:
        raise ValueError("Prompts list cannot be empty for text query.")

    # Note: Temperature validation is now handled in the Options constructor

    # Construct messages
    messages = [SystemMessage(content=context.system)]
    for p in context.prompts:
        messages.append(HumanMessage(content=p))

    # Prepare LangChain options
    langchain_options = {
        # model": model,
        # "temperature": temperature,
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
        # Handle unexpected response structure
        raise ValueError("Failed to parse content from LLM response.")

    except ValueError as e:
        # Catch and re-raise LangChain or API errors
        raise ValueError(f"LangChain API query failed: {e}") from e
