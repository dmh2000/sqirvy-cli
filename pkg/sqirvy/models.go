// Package sqirvy provides model management functionality for AI language models.
//
// This file contains model-to-provider mappings and utility functions for
// working with different AI models across supported providers.
package sqirvy

import "fmt"

var modelAlias = map[string]string{
	"claude-3-7-sonnet": "claude-3-7-sonnet-latest",
	"claude-3-5-sonnet": "claude-3-5-sonnet-latest",
	"claude-3-5-haiku":  "claude-3-5-haiku-latest",
	"claude-3-opus":     "claude-3-opus-latest",
}

// Supported AI providers
const (
	Anthropic string = "anthropic" // Anthropic's Claude models
	Gemini    string = "gemini"    // Google's Gemini models
	OpenAI    string = "openai"    // OpenAI's GPT models
	Llama     string = "llama"     // Meta's Llama models
)

// modelRegistry consolidates provider and token information for each model
// This helps ensure consistency between provider and token information.
// These mappings are essential for the QueryText functions to route requests
// to the appropriate client.

// ModelInfo holds information about a specific model
type ModelInfo struct {
	Provider  string
	MaxTokens int64
}

// modelRegistry is the single source of truth for model information
var modelRegistry = map[string]ModelInfo{
	// anthropic models
	"claude-3-7-sonnet-20250219": {Provider: Anthropic, MaxTokens: 64000},
	"claude-3-5-sonnet-20241022": {Provider: Anthropic, MaxTokens: 8192},
	"claude-3-7-sonnet-latest":   {Provider: Anthropic, MaxTokens: 64000},
	"claude-3-5-sonnet-latest":   {Provider: Anthropic, MaxTokens: 8192},
	"claude-3-5-haiku-latest":    {Provider: Anthropic, MaxTokens: MAX_TOKENS_DEFAULT},
	"claude-3-haiku-20240307":    {Provider: Anthropic, MaxTokens: MAX_TOKENS_DEFAULT},
	// google gemini models
	"gemini-1.5-flash":               {Provider: Gemini, MaxTokens: MAX_TOKENS_DEFAULT},
	"gemini-1.5-pro":                 {Provider: Gemini, MaxTokens: MAX_TOKENS_DEFAULT},
	"gemini-2.0-flash":               {Provider: Gemini, MaxTokens: MAX_TOKENS_DEFAULT},
	"gemini-2.0-flash-thinking-exp":  {Provider: Gemini, MaxTokens: MAX_TOKENS_DEFAULT},
	"gemini-2.5-flash-preview-04-17": {Provider: Gemini, MaxTokens: 65536},
	"gemini-2.5-pro-preview-03-25":   {Provider: Gemini, MaxTokens: 65536},
	// openai models
	"gpt-4o":      {Provider: OpenAI, MaxTokens: MAX_TOKENS_DEFAULT},
	"gpt-4o-mini": {Provider: OpenAI, MaxTokens: MAX_TOKENS_DEFAULT},
	"gpt-4-turbo": {Provider: OpenAI, MaxTokens: MAX_TOKENS_DEFAULT},
	"o4-mini":     {Provider: OpenAI, MaxTokens: MAX_TOKENS_DEFAULT},
	// llama models
	"llama3.3-70b": {Provider: Llama, MaxTokens: MAX_TOKENS_DEFAULT},
}

// ModelToMaxTokens maps model names to their maximum token limits.
// If a model is not in this map, MAX_TOKENS_DEFAULT will be used.
// MAX_TOKENS_DEFAULT is defined in client.go
// This map is maintained for backward compatibility
var modelToMaxTokens = map[string]int64{}

// Initialize modelToMaxTokens from modelRegistry for backward compatibility
func init() {
	for model, info := range modelRegistry {
		modelToMaxTokens[model] = info.MaxTokens
	}
}

// GetModelAlias returns the standardized model name for a given alias.
// This is used in cmd/sqirvy-cli to validate the model command line argument
// The model uses the input value unless there is an alias
func GetModelAlias(model string) string {
	if alias, ok := modelAlias[model]; ok {
		return alias
	}
	return model
}

// GetModelList returns a list of all supported model names
func GetModelList() []string {
	var models []string
	for model := range modelRegistry {
		models = append(models, model)
	}
	return models
}

type ModelProvider struct {
	Model    string
	Provider string
}

func GetModelProviderList() []ModelProvider {
	var mp []ModelProvider
	for model, info := range modelRegistry {
		mp = append(mp, ModelProvider{Model: model, Provider: info.Provider})
	}
	return mp
}

// GetProviderName returns the provider name for a given model identifier.
// Returns an error if the model is not recognized.
func GetProviderName(model string) (string, error) {
	if info, ok := modelRegistry[model]; ok {
		return info.Provider, nil
	}
	return "", fmt.Errorf("unrecognized model: %s", model)
}

// GetMaxTokensWithError returns the maximum token limit for a given model identifier
// along with an error if the model is not recognized.
// This function provides more detailed error reporting compared to GetMaxTokens.
func GetMaxTokensWithError(model string) (int64, error) {
	if info, ok := modelRegistry[model]; ok {
		return info.MaxTokens, nil
	}
	return MAX_TOKENS_DEFAULT, fmt.Errorf("unrecognized model: %s, using default token limit", model)
}

// GetMaxTokens returns the maximum token limit for a given model identifier.
// Returns MAX_TOKENS_DEFAULT if the model is not in ModelToMaxTokens.
// This function maintains backward compatibility with existing code.
func GetMaxTokens(model string) int64 {
	tokens, _ := GetMaxTokensWithError(model)
	return tokens
}
