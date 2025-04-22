/*
Copyright © 2025 David Howard  dmh2000@gmail.com
*/
package cmd

import (
	_ "embed"
	"fmt"
	"sort"

	sqirvy "dmh2000/sqirvy-cli/pkg/sqirvy"

	"github.com/spf13/cobra"
)

// modelsCmd represents the command to list supported LLM providers and models.
// It retrieves the list of models and their providers from the sqirvy package
// and prints them to standard output, sorted alphabetically by provider and model.
var modelsCmd = &cobra.Command{
	Use:   "models",
	Short: "List the supported LLM models and providers",
	Long:  `sqirvy-cli models lists all the Large Language Models (LLMs) supported by the tool, grouped by their provider (e.g., OpenAI, Anthropic, Gemini, Llama).`,
	Run: func(cmd *cobra.Command, args []string) {
		// Retrieve the list of models and providers
		mplist := sqirvy.GetModelProviderList()

		// Format the list for printing
		var mptext []string
		for _, v := range mplist {
			// Format as "  Provider  : ModelName"
			mptext = append(mptext, fmt.Sprintf("  %-10s: %s", v.Provider, v.Model))
		}

		// Sort the formatted list alphabetically
		sort.Strings(mptext)

		// Print the header and the sorted list
		fmt.Println("Supported Providers and Models:")
		for _, m := range mptext {
			fmt.Println(m)
		}
		fmt.Println() // Add a trailing newline for cleaner output
	},
}

// modelsUsage prints the usage instructions for the models command.
func modelsUsage(cmd *cobra.Command) error {
	fmt.Println("Usage: sqirvy-cli models")
	// No flags specific to this command, but persistent flags apply.
	fmt.Println("\nFlags:")
	cmd.PersistentFlags().PrintDefaults()
	return nil
}

// init registers the models command with the root command and sets its custom usage function.
func init() {
	rootCmd.AddCommand(modelsCmd)
	modelsCmd.SetUsageFunc(modelsUsage)
}
