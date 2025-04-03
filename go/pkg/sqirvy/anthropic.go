// Package api provides integration with Anthropic's Claude AI models.
//
// This file implements the Client interface for Anthropic's API, supporting
// both text and JSON queries to Claude models. It handles authentication,
// request formatting, and response parsing specific to Anthropic's requirements.
package sqirvy

import (
	"context"
	"fmt"
	"os"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/anthropic"
)

// AnthropicClient implements the Client interface for Anthropic's API.
// It provides methods for querying Anthropic's language models through
// the langchaingo library.
type AnthropicClient struct {
	llm              llms.Model // langchaingo LLM client
	temperatureScale float32
}

// Ensure AnthropicClient implements the Client interface
var _ Client = (*AnthropicClient)(nil)

// NewAnthropicClient creates a new instance of AnthropicClient using langchaingo.
// It returns an error if the required ANTHROPIC_API_KEY environment variable is not set.
func NewAnthropicClient() (*AnthropicClient, error) {
	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("ANTHROPIC_API_KEY environment variable not set")
	}

	// Note: langchaingo's anthropic client uses the API key from the environment variable by default.
	llm, err := anthropic.New()
	if err != nil {
		return nil, fmt.Errorf("failed to create Anthropic client: %w", err)
	}

	return &AnthropicClient{
		llm:              llm,
		temperatureScale: 1.0, // Default temperature scale for Anthropic
	}, nil
}

// QueryText sends a text query to the specified Anthropic model using langchaingo
// and returns the response.
func (c *AnthropicClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	// scale the temperature
	options.Temperature = options.Temperature * c.temperatureScale
	return QueryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
func (c *AnthropicClient) Close() error {
	// the langchaingo llm does not require explicit close
	return nil
}
