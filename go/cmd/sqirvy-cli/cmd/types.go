// Package cmd holds the command-line interface logic for the sqirvy-cli tool.
package cmd

const (
	// MaxInputTotalBytes defines the maximum allowed size in bytes for the combined
	// input from stdin, files, and scraped URLs. This prevents excessively large
	// prompts from being sent to the LLM. Currently set to 256 KiB.
	MaxInputTotalBytes = 262144 // 256 * 1024 bytes
)
