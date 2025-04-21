// Package api provides integration with Meta's Llama models via langchaingo.
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

// LlamaClient implements the Client interface for Meta's Llama models.
// It provides methods for querying Llama language models through
// an OpenAI-compatible interface.
type LlamaClient struct {
	llm              llms.Model // OpenAI-compatible LLM client
	temperatureScale float32
}

// Ensure LlamaClient implements the Client interface
var _ Client = (*LlamaClient)(nil)

// NewLlamaClient creates a new instance of LlamaClient.
// It returns an error if the required environment variables are not set.
func NewLlamaClient() (*LlamaClient, error) {
	apiKey := os.Getenv("LLAMA_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("LLAMA_API_KEY environment variable not set")
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
		temperatureScale: 1.0, // Default temperature scale for Llama
	}, nil
}

// LlamaClient.QueryText implements the QueryText method for the Client interface.
// It sends a text query to Meta's Llama models and returns the generated text response.
func (c *LlamaClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	// scale the temperature
	options.Temperature = options.Temperature * c.temperatureScale
	options.MaxTokens = modelToMaxTokens[model]

	return QueryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
func (c *LlamaClient) Close() error {
	// the langchain llm does not require explicit close
	return nil
}
