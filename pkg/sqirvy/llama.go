// Package sqirvy provides integration with Meta's Llama models via langchaingo.
//
// This file implements the Client interface for Meta's Llama models using
// langchaingo's OpenAI-compatible interface. It handles model initialization,
// prompt formatting, and response parsing.
package sqirvy

import (
	"context"
	"fmt"
	"os"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/openai"
)

const llama_temperature_scale = 1.0

// LlamaClient implements the Client interface for Meta's Llama models.
// It provides methods for querying Llama language models through
// an OpenAI-compatible interface.
type LlamaClient struct {
	llm              llms.Model // OpenAI-compatible LLM client
	temperatureScale float32
}

// Ensure LlamaClient implements the Client interface
var _ Client = (*LlamaClient)(nil)

// NewLlamaClient creates a new instance of LlamaClient using an OpenAI-compatible interface.
// It returns an error if the required LLAMA_API_KEY or LLAMA_BASE_URL environment variables are not set.
//
// The API key is retrieved from the LLAMA_API_KEY environment variable and
// the base URL is retrieved from the LLAMA_BASE_URL environment variable.
// Ensure these variables are set before calling this function.
func NewLlamaClient() (*LlamaClient, error) {
	apiKey := os.Getenv("LLAMA_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("LLAMA_API_KEY environment variable not set")
	}
	if len(apiKey) < 8 { // Assuming a minimum length for API keys
		return nil, fmt.Errorf("invalid LLAMA_API_KEY: key appears to be too short")
	}

	baseURL := os.Getenv("LLAMA_BASE_URL")
	if baseURL == "" {
		return nil, fmt.Errorf("LLAMA_BASE_URL environment variable not set")
	}

	llm, err := openai.New(
		openai.WithBaseURL(baseURL),
		openai.WithToken(apiKey),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create Llama client: %w", err)
	}

	return &LlamaClient{
		llm:              llm,
		temperatureScale: llama_temperature_scale, // Default temperature scale for Llama
	}, nil
}

// QueryText implements the Client interface method for querying Llama models.
// It sends a text query to Meta's Llama models and returns the generated text response.
// Request timeouts are handled by the input context.
func (c *LlamaClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	provider, err := GetProviderName(model)
	if err != nil || provider != Llama {
		return "", fmt.Errorf("invalid or unsupported Llama model: %s", model)
	}

	// scale the temperature
	options.Temperature = options.Temperature * c.temperatureScale
	options.MaxTokens = GetMaxTokens(model)

	return queryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
//
// For the Llama client, this method does not require any action as the
// underlying langchaingo client does not need to be explicitly closed.
func (c *LlamaClient) Close() error {
	// the langchain llm does not require explicit close
	return nil
}
