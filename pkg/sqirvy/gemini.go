// Package sqirvy provides integration with Google's Gemini AI models.
//
// This file implements the Client interface for Google's Gemini API, supporting
// both text and JSON queries. It handles authentication, request formatting,
// and response parsing specific to the Gemini API requirements.
package sqirvy

import (
	"context"
	"fmt"
	"os"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/googleai"
)

const gemini_temperature_scale = 2.0

// GeminiClient implements the Client interface for Google's Gemini API.
// It provides methods for querying Google's Gemini language models through
// the langchaingo library.
type GeminiClient struct {
	llm              llms.Model // langchaingo LLM client
	temperatureScale float32
}

// Ensure GeminiClient implements the Client interface
var _ Client = (*GeminiClient)(nil)

// NewGeminiClient creates a new instance of GeminiClient using langchaingo.
// It returns an error if the required GEMINI_API_KEY environment variable is not set.
//
// The Google API key is retrieved from the GEMINI_API_KEY environment variable.
// Ensure this variable is set before calling this function.
func NewGeminiClient() (*GeminiClient, error) {
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("GEMINI_API_KEY environment variable not set")
	}
	if len(apiKey) < 20 {
		return nil, fmt.Errorf("invalid GEMINI_API_KEY: key appears to be too short")
	}

	// Note: langchaingo's googleai client uses the API key from the environment variable by default.
	llm, err := googleai.New(context.Background(), googleai.WithAPIKey(apiKey))
	if err != nil {
		return nil, fmt.Errorf("failed to create Gemini client: %w", err)
	}

	return &GeminiClient{
		llm:              llm,
		temperatureScale: gemini_temperature_scale, // Default temperature scale for Gemini
	}, nil
}

// QueryText sends a text query to the specified Gemini model using langchaingo and returns the response.
//
// It takes a context, system prompt, a list of prompts, the model name, and options as input.
// It returns the generated text or an error if the query fails.
// Request timeouts are handled by the input context.
func (c *GeminiClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {

	provider, err := GetProviderName(model)
	if err != nil || provider != Gemini {
		return "", fmt.Errorf("invalid or unsupported Gemini model: %s", model)
	}
	options.Temperature = options.Temperature * c.temperatureScale
	options.MaxTokens = GetMaxTokens(model)
	return queryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
//
// For the Gemini client, this method does not require any action as the
// underlying langchaingo client does not need to be explicitly closed.
func (c *GeminiClient) Close() error {
	// the langchaingo llm does not require explicit close
	return nil
}
