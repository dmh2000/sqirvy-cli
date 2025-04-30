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

// planCmd represents the command to request a plan generation from the LLM.
// It constructs a prompt including an internal system prompt for planning,
// input from stdin, and content from specified files or URLs, then sends it
// to the LLM and prints the generated plan to stdout.
var planCmd = &cobra.Command{
	Use:   "plan",
	Short: "Request the LLM to generate a plan",
	Long: `sqirvy-cli plan:
It will ask the LLM to generate a plan based on the given prompt. 
It will send a request to the LLM and output the results to stdout.
Typical usage would be to generate a plan for an application and send it 
to [sqirvy-cli code] to generate the actual code. 
The prompt is constructed in this order:
	An internal system prompt for general planning 
	Input from stdin
	Any number of filename or url arguments	`,
	Run: func(cmd *cobra.Command, args []string) {
		// get arg/config params
		model := viper.GetString("model")
		temperature := viper.GetFloat64("temperature")

		// Execute the query using the specific planning prompt
		response, err := executeQuery(model, temperature, planPrompt, args)
		if err != nil {
			log.Fatalf("Error executing plan command: %v", err)
		}
		// Print the LLM response to standard output
		fmt.Print(response)
		fmt.Println() // Ensure a newline at the end
	},
}

// planUsage prints the usage instructions for the plan command.
func planUsage(cmd *cobra.Command) error {
	fmt.Println("Usage: stdin | sqirvy-cli plan [flags] [files| urls]")
	fmt.Println("\nFlags:")
	cmd.Flags().PrintDefaults()
	return nil
}

// init registers the plan command with the root command and sets its custom usage function.
func init() {
	rootCmd.AddCommand(planCmd)
	planCmd.SetUsageFunc(planUsage)
}
