/*
Copyright © 2025 David Howard  dmh2000@gmail.com
*/
package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string
var defaultPrompt = "Hello"

const defaultModel = "gemini-2.5-flash-preview-04-17"
const defaultTemperature = 0.5

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "sqirvy-cli [command] [flags] [files| urls]",
	Short: "A command line tool to interact with Large Language Models",
	Long: `Sqirvy-cli is a command line tool to interact with Large Language Models (LLMs).
   - It provides a simple interface to send prompts to the LLM and receive responses
   - Sqirvy-cli commands receive prompt input from stdin, filenames and URLs. Output is sent to stdout.
   - This architecture makes it simple to pipe from stdin -> query -> stdout -> query -> stdout...
   - The output is determined by the command and the input prompt.
   - The "query" command is used to send an arbitrary query to the LLM.
   - The "plan" command is used to send a prompt to the LLM and receive a plan in response.
   - The "code" command is used to send a prompt to the LLM and receive source code in response.
   - The "review" command is used to send a prompt to the LLM and receive a code review in response.
   - Sqirvy-cli is designed to support terminal command pipelines. 
	`,
	// Run defines the behavior when the root command is executed without subcommands.
	// It defaults to executing the 'query' command with the provided arguments.
	Run: func(cmd *cobra.Command, args []string) {
		// If no command is specified, prepend 'query' to the arguments
		// and execute the command again. This makes 'query' the default command.
		queryArgs := append([]string{"query"}, args...)
		cmd.SetArgs(queryArgs)
		if err := cmd.Execute(); err != nil {
			// Error during execution is typically handled by Cobra itself,
			// but we catch it here just in case.
			fmt.Fprintf(os.Stderr, "Error executing default command 'query': %v\n", err)
			os.Exit(1)
		}
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

// init sets up the application's persistent flags and initializes configuration handling.
// It defines flags common to all commands, such as model selection and temperature.
func init() {
	// Register the initConfig function to run when Cobra initializes.
	cobra.OnInitialize(initConfig)

	// Define persistent flags available to the root command and all subcommands.
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.config/sqirvy-cli/config.yaml)") // Example if config file flag was used

	rootCmd.PersistentFlags().StringVar(&defaultPrompt, "default-prompt", "Hello", "Default prompt if no stdin/args provided")
	viper.BindPFlag("default-prompt", rootCmd.PersistentFlags().Lookup("default-prompt")) // Bind flag to Viper config

	rootCmd.PersistentFlags().StringP("model", "m", defaultModel, "LLM model to use (e.g., gpt-4o, claude-3-5-sonnet-latest)")
	viper.BindPFlag("model", rootCmd.PersistentFlags().Lookup("model")) // Bind flag to Viper config

	rootCmd.PersistentFlags().Float32P("temperature", "t", defaultTemperature, "LLM temperature (randomness) to use (0.0 to 1.0)")
	viper.BindPFlag("temperature", rootCmd.PersistentFlags().Lookup("temperature")) // Bind flag to Viper config
}

// configPrinted ensures the config file path is printed only once to stderr.
var configPrinted bool

// initConfig reads in configuration settings from a config file (if found)
// and environment variables. Viper handles the precedence (flags > env > config).
func initConfig() {
	if cfgFile != "" {
		// Use config file from the flag.
		viper.SetConfigFile(cfgFile)
	} else {
		// Find home directory.
		home, err := os.UserHomeDir()
		cobra.CheckErr(err)

		// Search config in home directory with name ".config/sqirvy-cli" (without extension).
		viper.AddConfigPath(home + "/.config/sqirvy-cli")
		viper.SetConfigType("yaml")
		viper.SetConfigName("config")
	}

	viper.AutomaticEnv() // read in environment variables that match

	// If a config file is found, read it in.
	if err := viper.ReadInConfig(); err == nil {
		if !configPrinted {
			configPrinted = true
			fmt.Fprintln(os.Stderr, "Config file :", viper.ConfigFileUsed())
		}
	}
}
