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
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
)

// AnthropicClient implements the Client interface for Anthropic's API.
// It provides methods for querying Anthropic's language models through
// their official API client.
type AnthropicClient struct {
	client *anthropic.Client // Anthropic API client
}

// Ensure AnthropicClient implements the Client interface
var _ Client = (*AnthropicClient)(nil)

// NewAnthropicClient creates a new instance of AnthropicClient.
// It returns an error if the required ANTHROPIC_API_KEY environment variable is not set.
func NewAnthropicClient() (*AnthropicClient, error) {
	if os.Getenv("ANTHROPIC_API_KEY") == "" {
		return nil, fmt.Errorf("ANTHROPIC_API_KEY environment variable not set")
	}
	return &AnthropicClient{
		client: anthropic.NewClient(),
	}, nil
}

// QueryText sends a text query to the specified Anthropic model and returns the response.
// It accepts a prompt string, model identifier, and query options.
// Returns the model's response as a string or an error if the query fails.
func (c *AnthropicClient) QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error) {
	if ctx.Err() != nil {
		return "", fmt.Errorf("request context error %w", ctx.Err())
	}

	if len(prompts) == 0 {
		return "", fmt.Errorf("prompts cannot be empty for text query")
	}

	// set default and validate temperature
	if options.Temperature < MinTemperature {
		options.Temperature = MinTemperature
	}
	if options.Temperature > MaxTemperature {
		return "", fmt.Errorf("temperature must be between %.1f and %.1f", MinTemperature, MaxTemperature)
	}
	// scale temperature for Claude 0..1.0
	options.Temperature /= MaxTemperature

	// Set default max tokens if not specified
	maxTokens := options.MaxTokens
	if maxTokens == 0 {
		maxTokens = MaxTokensDefault
	}

	// first prompt is system prompt

	systemPrompt := []anthropic.TextBlockParam{
		anthropic.NewTextBlock(system),
	}

	// addtional prompts are user messages
	messages := make([]anthropic.MessageParam, 0, len(prompts))
	for _, p := range prompts {
		messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock(p)))
	}

	// Create new message request with the provided prompt and temperature
	message, err := c.client.Messages.New(ctx, anthropic.MessageNewParams{
		Model:       anthropic.F(model),                        // Specify which model to use
		MaxTokens:   anthropic.F(maxTokens),                    // Limit response length
		Temperature: anthropic.F(float64(options.Temperature)), // Set temperature
		System:      anthropic.F(systemPrompt),
		Messages: anthropic.F(
			messages,
		),
	})
	if err != nil {
		return "", fmt.Errorf("failed to create message: %w", err)
	}

	// Verify we got a non-empty response
	if len(message.Content) == 0 {
		return "", fmt.Errorf("no content in response")
	}

	// Build response using strings.Builder for better performance
	var response strings.Builder
	for _, content := range message.Content {
		response.WriteString(content.Text)
	}
	return response.String(), nil
}

// Close implements the Close method for the Client interface.
func (c *AnthropicClient) Close() error {
	// the anthropic client does not require explicit close
	return nil
}
