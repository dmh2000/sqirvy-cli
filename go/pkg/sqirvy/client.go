// Package sqirvy provides a unified interface for interacting with various AI language models.
//
// The package supports multiple AI providers including:
// - Anthropic (Claude models)
// - Google (Gemini models)
// - OpenAI (GPT models)
// - Meta (Llama models)
// - DeepSeek (DeepSeek models)
//
// It provides a consistent interface for making text and JSON queries while handling
// provider-specific implementation details internally.
package sqirvy

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/tmc/langchaingo/llms"
)

const (
	// MaxTokensDefault is the default maximum number of tokens in responses
	MaxTokensDefault = 4096

	// Temperature limits for model queries (0-100 scale)
	MinTemperature = 0.0
	MaxTemperature = 100.0

	// request timeout in seconds
	RequestTimeout = time.Second * 15
)

// Provider represents supported AI providers.
// Currently supports Anthropic, DeepSeek, Gemini, and OpenAI.
// Provider identifies which AI service provider to use
type Provider string

// Options combines all provider-specific options into a single structure.
// This allows for provider-specific configuration while maintaining a unified interface.
type Options struct {
	Temperature float32 // Controls the randomness of the output
	MaxTokens   int64   // Maximum number of tokens in the response
}

// Client provides a unified interface for AI operations.
// It abstracts away provider-specific implementations behind a common interface
// for making text and JSON queries to AI models.
type Client interface {
	QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error)
	Close() error
}

// NewClient creates a new AI client for the specified provider
func NewClient(provider string) (Client, error) {
	switch provider {
	case Anthropic:
		client, err := NewAnthropicClient()
		if err != nil {
			return nil, fmt.Errorf("failed to create Anthropic client: %w", err)
		}
		return client, nil
	case DeepSeek:
		client, err := NewDeepSeekClient()
		if err != nil {
			return nil, fmt.Errorf("failed to create DeepSeek client: %w", err)
		}
		return client, nil
	case Gemini:
		client, err := NewGeminiClient()
		if err != nil {
			return nil, fmt.Errorf("failed to create Geminip client: %w", err)
		}
		return client, nil
	case OpenAI:
		client, err := NewOpenAIClient()
		if err != nil {
			return nil, fmt.Errorf("failed to create OpenAI client: %w", err)
		}
		return client, nil
	case Llama:
		client, err := NewLlamaClient()
		if err != nil {
			return nil, fmt.Errorf("failed to create Llama client: %w", err)
		}
		return client, nil
	default:
		return nil, fmt.Errorf("unsupported provider: %s", provider)
	}
}

func QueryTextLangChain(ctx context.Context, llm llms.Model, system string, prompts []string, model string, options Options) (string, error) {
	if ctx.Err() != nil {
		return "", fmt.Errorf("request context error %w", ctx.Err())
	}

	if len(prompts) == 0 {
		return "", fmt.Errorf("prompts cannot be empty for text query")
	}

	// Set default and validate temperature
	if options.Temperature < MinTemperature {
		options.Temperature = MinTemperature
	}
	if options.Temperature > MaxTemperature {
		return "", fmt.Errorf("temperature must be between %.1f and %.1f", MinTemperature, MaxTemperature)
	}
	// Scale temperature for Llama's 0-2 range
	options.Temperature = (options.Temperature * LlamaTempScale) / MaxTemperature

	// system prompt
	content := []llms.MessageContent{
		llms.TextParts(llms.ChatMessageTypeSystem, system),
	}

	// query prompts
	for _, prompt := range prompts {
		content = append(content, llms.TextParts(llms.ChatMessageTypeHuman, prompt))
	}

	// generate completion
	completion, err := llm.GenerateContent(
		ctx, content,
		llms.WithTemperature(float64(options.Temperature)),
		llms.WithModel(model),
	)
	if err != nil {
		return "", fmt.Errorf("failed to generate completion: %w", err)
	}

	var response strings.Builder
	for _, part := range completion.Choices {
		response.WriteString(part.Content)
	}

	return response.String(), nil
}
