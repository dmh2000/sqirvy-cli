// Package api provides integration with Meta's OpenAI models via langchaingo.
//
// This file implements the Client interface for Meta's OpenAI models using
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

// OpenAIClient implements the Client interface for Meta's OpenAI models.
// It provides methods for querying OpenAI language models through
// an OpenAI-compatible interface.
type OpenAIClient struct {
	llm              llms.Model // OpenAI-compatible LLM client
	temperatureScale float32
}

// Ensure OpenAIClient implements the Client interface
var _ Client = (*OpenAIClient)(nil)

// NewOpenAIClient creates a new instance of OpenAIClient.
// It returns an error if the required environment variables are not set.
func NewOpenAIClient() (*OpenAIClient, error) {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("OPENAI_API_KEY environment variable not set")
	}

	baseURL := os.Getenv("OPENAI_BASE_URL")
	if baseURL == "" {
		return nil, fmt.Errorf("OPENAI_BASE_URL environment variable not set")
	}

	llm, err := openai.New(
		openai.WithBaseURL(baseURL),
		openai.WithToken(apiKey),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create OpenAI client: %w", err)
	}

	return &OpenAIClient{
		llm:              llm,
		temperatureScale: 2.0, // Default temperature scale for OpenAI
	}, nil
}

// OpenAIClient.QueryText implements the QueryText method for the Client interface.
// It sends a text query to Meta's OpenAI models and returns the generated text response.
func (c *OpenAIClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	// scale the temperature
	options.Temperature = options.Temperature * c.temperatureScale
	return QueryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
func (c *OpenAIClient) Close() error {
	// the langchain llm does not require explicit close
	return nil
}
