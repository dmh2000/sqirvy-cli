// Package sqirvy provides integration with Anthropic's Claude AI models.
package sqirvy

import (
	"context"
	"fmt"
	"os"
	"strings"

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
//
// The Anthropic API key is retrieved from the ANTHROPIC_API_KEY environment variable.
// Ensure this variable is set before calling this function.
func NewAnthropicClient() (*AnthropicClient, error) {
	// require api key
	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("ANTHROPIC_API_KEY environment variable not set")
	}
	if len(apiKey) < 20 || !strings.HasPrefix(apiKey, "sk-") {
		return nil, fmt.Errorf("invalid ANTHROPIC_API_KEY: %s", apiKey)
	}

	// require base url
	baseUrl := os.Getenv("ANTHROPIC_BASE_URL")
	if baseUrl == "" {
		return nil, fmt.Errorf("ANTHROPIC_BASE_URL environment variable not set")
	}

	// Note: langchaingo's anthropic client uses the API key from the environment variable by default.
	llm, err := anthropic.New()
	if err != nil {
		return nil, fmt.Errorf("failed to create Anthropic client (check API key and network): %w", err)
	}

	return &AnthropicClient{
		llm:              llm,
		temperatureScale: 1.0, // Default temperature scale for Anthropic
	}, nil
}

// QueryText sends a text query to the specified Anthropic model using langchaingo and returns the response.
//
// It takes a context, system prompt, a list of prompts, the model name, and options as input.
// It returns the generated text or an error if the query fails or the model is invalid.
// Request timeouts are handled by the input context
func (c *AnthropicClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	// validate the model
	provider, err := GetProviderName(model)
	if err != nil || provider != Anthropic {
		return "", fmt.Errorf("invalid or unsupported Anthropic model: %s", model)
	}

	// scale the temperature
	options.Temperature = options.Temperature * c.temperatureScale
	options.MaxTokens = GetMaxTokens(model)
	return queryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
//
// For the Anthropic client, this method does not require any action as the
// underlying langchaingo client does not need to be explicitly closed.
func (c *AnthropicClient) Close() error {
	// the langchaingo llm does not require explicit close
	return nil
}
