/*
Copyright © 2025 David Howard  dmh2000@gmail.com
*/
package cmd

import (
	_ "embed"
	"fmt"
	"log"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

// codeCmd represents the command to request code generation from the LLM.
// It constructs a prompt including an internal system prompt for code generation,
// input from stdin, and content from specified files or URLs, then sends it
// to the LLM and prints the generated code to stdout.
var codeCmd = &cobra.Command{
	Use:   "code",
	Short: "Request the LLM to generate code",
	Long: `sqirvy-cli code will send a request to generate code 
and will output the results to stdout.
The prompt is constructed in this order:
	An internal system prompt for code generation
	Input from stdin
	Any number of filename or url arguments	
	`,
	Run: func(cmd *cobra.Command, args []string) {
		// get arg/config params
		model := viper.GetString("model")
		temperature := viper.GetFloat64("temperature")

		// Execute the query using the specific code generation prompt
		response, err := executeQuery(model, temperature, codePrompt, args)
		if err != nil {
			log.Fatalf("Error executing code command: %v", err)
		}
		// Print the LLM response to standard output
		fmt.Print(response)
		fmt.Println() // Ensure a newline at the end
	},
}

// codeUsage prints the usage instructions for the code command.
func codeUsage(cmd *cobra.Command) error {
	fmt.Println("Usage: stdin | sqirvy-cli code [flags] [files| urls]")
	fmt.Println("\nFlags:")
	cmd.Flags().PrintDefaults()
	return nil
}

// init registers the code command with the root command and sets its custom usage function.
func init() {
	rootCmd.AddCommand(codeCmd)
	codeCmd.SetUsageFunc(codeUsage)
}
