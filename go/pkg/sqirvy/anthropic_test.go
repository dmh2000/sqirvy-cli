package sqirvy

import (
	"context"
	"os"
	"testing"
)

const assistant = "you are a helpful assistant"

func TestAnthropicClient_QueryText(t *testing.T) {
	// Skip test if ANTHROPIC_API_KEY not set
	if os.Getenv("ANTHROPIC_API_KEY") == "" {
		t.Skip("ANTHROPIC_API_KEY not set")
	}

	client, err := NewAnthropicClient()
	if err != nil {
		t.Errorf("new client failed: %v", err)
	}

	tests := []struct {
		name    string
		prompt  []string
		wantErr bool
	}{
		{
			name:    "Basic prompt",
			prompt:  []string{"Say 'Hello, World!'"},
			wantErr: false,
		},
		{
			name:    "Empty prompt",
			prompt:  []string{},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			ctx := context.Background()
			// Use a known model from the list
			model := "claude-3-haiku-20240307"
			options := Options{MaxTokens: GetMaxTokens(model), Temperature: 0.5}
			got, err := client.QueryText(ctx, assistant, tt.prompt, model, options)

			if tt.wantErr {
				if err == nil {
					t.Errorf("AnthropicClient.QueryText() error = nil, wantErr %v", tt.wantErr)
				}
				return // Expected error, test passes
			}

			// If we didn't want an error, but got one
			if err != nil {
				t.Errorf("AnthropicClient.QueryText() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			// If we didn't want an error and didn't get one, check response
			if len(got) == 0 {
				t.Error("AnthropicClient.QueryText() returned empty response")
			}
			// Optional: Add more specific checks for the successful case if needed
			// e.g., if !strings.Contains(got, "Hello") { ... }
		})
	}
}
