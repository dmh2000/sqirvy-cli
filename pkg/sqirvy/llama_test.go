package sqirvy

import (
	"context"
	"os"
	"testing"
)

func TestLlamaClient_QueryText(t *testing.T) {
	if os.Getenv("LLAMA_API_KEY") == "" {
		t.Skip("LLAMA_API_KEY not set")
	}
	if os.Getenv("LLAMA_BASE_URL") == "" {
		t.Skip("LLAMA_BASE_URL not set")
	}

	client, err := NewClient("llama")
	if err != nil {
		t.Fatalf("Failed to create client: %v", err)
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
			got, err := client.QueryText(context.Background(), assistant, tt.prompt, "llama3.3-70b", Options{})
			if tt.wantErr {
				if err == nil {
					t.Errorf("LlamaClient.QueryText() error = %v, wantErr %v", err, tt.wantErr)
				}
				return
			}
			if err != nil {
				t.Errorf("LlamaClient.QueryText() error = %v", err)
				return
			}
			if len(got) == 0 {
				t.Error("LlamaClient.QueryText() returned empty response")
			}
		})
	}
}
