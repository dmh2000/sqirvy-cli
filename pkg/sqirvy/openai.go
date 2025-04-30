// Package sqirvy provides integration with OpenAI models via langchaingo.
//
// This file implements the Client interface for OpenAI models using
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

const openai_temperature_scale = 2.0

// OpenAIClient implements the Client interface for OpenAI models.
// It provides methods for querying OpenAI language models through
// an OpenAI-compatible interface.
type OpenAIClient struct {
	llm              llms.Model // OpenAI-compatible LLM client
	temperatureScale float32
}

// Ensure OpenAIClient implements the Client interface
var _ Client = (*OpenAIClient)(nil)

// NewOpenAIClient creates a new instance of OpenAIClient using langchaingo.
// It returns an error if the required OPENAI_API_KEY or OPENAI_BASE_URL environment variables are not set.
//
// The API key is retrieved from the OPENAI_API_KEY environment variable and
// the base URL is retrieved from the OPENAI_BASE_URL environment variable.
// Ensure these variables are set before calling this function.
func NewOpenAIClient() (*OpenAIClient, error) {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("OPENAI_API_KEY environment variable not set")
	}
	if len(apiKey) < 20 {
		return nil, fmt.Errorf("invalid OPENAI_API_KEY: key appears to be too short")
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
		temperatureScale: openai_temperature_scale, // Default temperature scale for OpenAI
	}, nil
}

// QueryText implements the Client interface method for querying OpenAI models.
// It sends a text query to OpenAI models and returns the generated text response.
// It returns an error if the query fails or the model is invalid.
func (c *OpenAIClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	// validate the model
	provider, err := GetProviderName(model)
	if err != nil || provider != OpenAI {
		return "", fmt.Errorf("invalid or unsupported OpenAI model: %s", model)
	}

	// scale the temperature
	options.Temperature = options.Temperature * c.temperatureScale
	options.MaxTokens = GetMaxTokens(model)

	return queryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
//
// For the OpenAI client, this method does not require any action as the
// underlying langchaingo client does not need to be explicitly closed.
func (c *OpenAIClient) Close() error {
	// the langchain llm does not require explicit close
	return nil
}
