/*
Copyright © 2025 David Howard  dmh2000@gmail.com
*/
package cmd

import (
	"fmt"
	"log"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

// reviewCmd represents the command to request a code review from the LLM.
// It constructs a prompt including an internal system prompt for code review,
// input from stdin (usually the code to be reviewed), and content from
// specified files or URLs (e.g., related code or context), then sends it
// to the LLM and prints the generated review to stdout.
var reviewCmd = &cobra.Command{
	Use:   "review",
	Short: "Request the LLM to generate a code review",
	Long: `sqirvy-cli review
It will ask the LLM to review input code and will output the results to stdout.
The prompt is constructed in this order:
    An internal system prompt for code review
    Input from stdin
    Any number of filename or url arguments
`,
	Run: func(cmd *cobra.Command, args []string) {
		// get arg/config params
		model := viper.GetString("model")
		temperature := viper.GetFloat64("temperature")

		// Execute the query using the specific code review prompt
		response, err := executeQuery(model, temperature, reviewPrompt, args)
		if err != nil {
			log.Fatalf("Error executing review command: %v", err)
		}
		// Print the LLM response (the review) to standard output
		fmt.Print(response)
		fmt.Println() // Ensure a newline at the end
	},
}

// reviewUsage prints the usage instructions for the review command.
func reviewUsage(cmd *cobra.Command) error {
	fmt.Println("Usage: stdin | sqirvy-cli review [flags] [files| urls]")
	fmt.Println("\nFlags:")
	cmd.Flags().PrintDefaults()
	return nil
}

// init registers the review command with the root command and sets its custom usage function.
func init() {
	rootCmd.AddCommand(reviewCmd)
	reviewCmd.SetUsageFunc(reviewUsage)
}
