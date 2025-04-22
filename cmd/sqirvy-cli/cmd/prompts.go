// Package cmd implements command-line interface functionality for the sqirvy-cli tool.
// It provides commands for handling various types of prompts and input processing.
package cmd

import (
	util "dmh2000/sqirvy-cli/pkg/util"
	_ "embed"
	"fmt"
	"net"
	"net/url"
)

// queryPrompt contains the embedded content of the query.md file,
// which defines the system prompt for query operations.
//
//go:embed prompts/query.md
var queryPrompt string

// planPrompt contains the embedded content of the plan.md file,
// which defines the system prompt for planning operations.
//
//go:embed prompts/plan.md
var planPrompt string

// codePrompt contains the embedded content of the code.md file,
// which defines the system prompt for code generation operations.
//
//go:embed prompts/code.md
var codePrompt string

// reviewPrompt contains the embedded content of the review.md file,
// which defines the system prompt for code review operations.
//
//go:embed prompts/review.md
var reviewPrompt string

// ReadPrompt processes input from standard input (stdin), URLs, and local files,
// combining them into a slice of strings suitable for use as prompts.
// It ensures the total size of all inputs does not exceed MaxInputTotalBytes.
// Input sources are processed in the order: stdin, then arguments (files/URLs).
// If no input is provided via stdin or arguments, a default prompt is used.
//
// Parameters:
//   - args: A slice of strings, each representing a local file path or a URL.
//
// Returns:
//   - []string: A slice containing the content from stdin and each file/URL,
//     formatted and ready to be used as prompts. Returns a default prompt if
//     no other input is provided.
//   - error: An error if reading stdin, scraping a URL, reading a file fails,
//     or if the total combined size exceeds MaxInputTotalBytes.
func ReadPrompt(args []string) ([]string, error) {

	var prompts []string
	var length int64 // Tracks the cumulative size of the prompts

	// Process standard input and check size limit
	var stdinData string
	stdinData, _, err := util.ReadStdin(MaxInputTotalBytes)
	if err != nil {
		return []string{""}, fmt.Errorf("error: reading from stdin: %w", err)
	}
	prompts = append(prompts, stdinData)
	length += int64(len(stdinData))
	if length > MaxInputTotalBytes {
		return nil, fmt.Errorf("error: total size would exceed limit of %d bytes (stdin)", MaxInputTotalBytes)
	}

	// Process each argument which can be either a URL or a file path
	for _, arg := range args {
		// Attempt to parse argument as URL
		parsedURL, err := url.ParseRequestURI(arg)
		if err == nil && (parsedURL.Scheme == "http" || parsedURL.Scheme == "https") {
			// Basic URL format is valid, now check for potential SSRF
			hostname := parsedURL.Hostname()
			ips, err := net.LookupIP(hostname)
			if err != nil {
				return []string{""}, fmt.Errorf("error: could not resolve hostname for URL %s: %w", arg, err)
			}

			for _, ip := range ips {
				if ip.IsLoopback() || ip.IsPrivate() || ip.IsLinkLocalUnicast() || ip.IsLinkLocalMulticast() {
					return []string{""}, fmt.Errorf("error: URL %s resolves to a non-public IP address %s, potential SSRF detected", arg, ip.String())
				}
			}

			// Hostname resolves to public IPs, proceed with scraping
			content, err := util.ScrapeURL(arg)
			if err != nil {
				return []string{""}, fmt.Errorf("error: failed to scrape URL %s: %w", arg, err)
			}
			content += "\n\n"
			prompts = append(prompts, content)
			length += int64(len(content))
			if length > MaxInputTotalBytes {
				return []string{""}, fmt.Errorf("error: total size would exceed limit of %d bytes (urls)", MaxInputTotalBytes)
			}
			continue
		}

		// Handle file content if not a URL
		fileData, _, err := util.ReadFile(arg, MaxInputTotalBytes)
		if err != nil {
			return []string{""}, fmt.Errorf("error: failed to read file %s: %w", arg, err)
		}
		prompts = append(prompts, string(fileData))
		length += int64(len(fileData))
		if length > MaxInputTotalBytes {
			return []string{""}, fmt.Errorf("error: total size would exceed limit of %d bytes (files)", MaxInputTotalBytes)
		}
	}

	// If no prompts were gathered from stdin or arguments, use the default prompt.
	// This handles cases where stdin is not piped and no file/URL args are given.
	if len(prompts) == 0 || (len(prompts) == 1 && prompts[0] == "") {
		prompts = []string{defaultPrompt}
	}

	return prompts, nil
}
