#!/bin/bash

# Get the list of all supported models
models=(
    # Anthropic models
    "claude-3-7-sonnet-20250219"
    "claude-3-5-sonnet-20241022"
    "claude-3-7-sonnet-latest"
    "claude-3-5-sonnet-latest"
    "claude-3-5-haiku-latest"
    "claude-3-haiku-20240307"
    "claude-3-opus-latest"
    "claude-3-opus-20240229"
    # Google Gemini models
    "gemini-2.0-flash"
    "gemini-1.5-flash"
    "gemini-1.5-pro"
    "gemini-2.0-flash-thinking-exp"
    "gemini-2.5-pro-exp-03-25"
    # OpenAI models
    "gpt-4o"
    "gpt-4o-mini"
    "gpt-4-turbo"
    # Llama models
    "llama3.3-70b"
)

# Simple query to test with
query="hello"

# Test each model
for model in "${models[@]}"; do
    echo "==============================================================="
    echo "Testing model: $model"
    echo "==============================================================="
    echo "$query" | python main.py -c query -m "$model"
    echo "==============================================================="
    echo ""
done

echo "All tests completed"

