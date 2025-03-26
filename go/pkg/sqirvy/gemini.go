// Package api provides integration with Google's Gemini AI models.
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

// GeminiClient implements the Client interface for Google's Gemini API.
// It provides methods for querying Google's Gemini language models through
// the langchaingo library.
type GeminiClient struct {
	llm llms.Model // langchaingo LLM client
}

// Ensure GeminiClient implements the Client interface
var _ Client = (*GeminiClient)(nil)

// NewGeminiClient creates a new instance of GeminiClient.
// It returns an error if the required GEMINI_API_KEY environment variable is not set.
func NewGeminiClient() (*GeminiClient, error) {
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("GEMINI_API_KEY environment variable not set")
	}

	// Note: langchaingo's googleai client uses the API key from the environment variable by default.
	llm, err := googleai.New(context.Background(), googleai.WithAPIKey(apiKey))
	if err != nil {
		return nil, fmt.Errorf("failed to create Gemini client: %w", err)
	}

	return &GeminiClient{
		llm: llm,
	}, nil
}

// QueryText sends a text query to the specified Gemini model using langchaingo
// and returns the response.
func (c *GeminiClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	// langchaingo's googleai client expects temperature 0.0-1.0
	// QueryTextLangChain handles the 0-100 to 0-1 scaling
	// Note: Gemini via langchaingo might use a different temp scale (e.g., 0-1), adjust TemperatureScale in Options if needed.
	// For now, rely on the default scaling in QueryTextLangChain.
	return QueryTextLangChain(ctx, c.llm, system, prompts, model, options)
}

// Close implements the Close method for the Client interface.
func (c *GeminiClient) Close() error {
	// the langchaingo llm does not require explicit close
	return nil
}
