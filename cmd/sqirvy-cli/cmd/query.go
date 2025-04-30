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

// queryCmd represents the command to execute an arbitrary query against the LLM.
// It constructs a prompt using a generic system prompt, input from stdin,
// and content from specified files or URLs, then sends it to the LLM
// and prints the response to stdout. This is the default command if none is specified.
var queryCmd = &cobra.Command{
	Use:   "query",
	Short: "Execute an arbitrary query to the LLM (default command)",
	Long: `sqirvy-cli query will send a request to the LLM to execute an arbitrary query.
It uses a general-purpose system prompt. The full prompt to the LLM will consist of 
this system prompt, any input from stdin, and then any filename or url arguments, 
in the order specified.
`,
	Run: func(cmd *cobra.Command, args []string) {
		// get arg/config params
		model := viper.GetString("model")
		temperature := viper.GetFloat64("temperature")

		// Execute the query using the generic query prompt
		response, err := executeQuery(model, temperature, queryPrompt, args)
		if err != nil {
			log.Fatalf("Error executing query command: %v", err)
		}
		// Print the LLM response to standard output
		fmt.Print(response)
		fmt.Println() // Ensure a newline at the end
	},
}

// queryUsage prints the usage instructions for the query command.
func queryUsage(cmd *cobra.Command) error {
	fmt.Println("Usage: stdin | sqirvy-cli query [flags] [files| urls]")
	fmt.Println("\nFlags:")
	cmd.Flags().PrintDefaults()
	return nil
}

// init registers the query command with the root command and sets its custom usage function.
func init() {
	rootCmd.AddCommand(queryCmd)
	queryCmd.SetUsageFunc(queryUsage)
}
