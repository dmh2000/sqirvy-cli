- refactor gemini.go to use langchain similarly to the code in llama.go and openai.go.
- be sure to import tmc/lanchaingo/llms/anthropic 
- the gemini QueryText function should simply call the QueryTextLangChain in client.go and let that function execute the query

/add ./go/pkg/sqirvy/client.go
 ./go/pkg/sqirvy/openai.go
 ./go/pkg/sqirvy/gemini.go
 ./go/pkg/sqirvy/llama.go
 ./go/pkg/sqirvy/llama_test.go
 ./go/pkg/sqirvy/gemini_test.go
 ./go/pkg/sqirvy/anthropic_test.go
 ./go/pkg/sqirvy/deepseek.go
 ./go/pkg/sqirvy/deepseek_test.go
 ./go/pkg/sqirvy/models_test.go
 ./go/pkg/sqirvy/models.go
 ./go/pkg/sqirvy/anthropic.go
 ./go/pkg/sqirvy/openai_test.go

- in the directory "python/sqirvy-cli, create a python main program named sqirvy-cli.py
- sqirvy-cli is a command line tool that  receives  input from stdin, and command line arguments
- command line flags are:
  - "-m  <model name>" or "--model <model name>" which is a string with the name of the llm model to be used
  - "-t <temperature>" or "--temperature <temperature>" which is a floating point value indicating the temperature to use on the llm. it has a default value of 1.0 and is limited to the  interval [0.0, 2.0)
  - the flags are optional
  - the python code should read the arguments and assign them to appropriate variables
- additional arguments following the flags are any number of filenames and urls
- the program will print the stdin input and command line arguments to stdout



Sqirvy-cli is a command line tool to interact with Large Language Models (LLMs).
- It provides a simple interface to send prompts to the LLM and receive responses
  - remaining arguments are any number of filenames and/or urls
  - Output is sent to stdout.
- This architecture makes it simple to pipe from stdin -> query -> stdout -> query -> stdout...
- The output is determined by the command and the input prompt.
- The "query" command is used to send an arbitrary query to the LLM.
- The "plan" command is used to send a prompt to the LLM and receive a plan in response.
- The "code" command is used to send a prompt to the LLM and receive source code in response.
- The "review" command is used to send a prompt to the LLM and receive a code review in response.
- Sqirvy-cli is designed to support terminal command pipelines./

in file python/sqirvy-cli/sqirvy-ai/client.py, create a function named NewClient that takes parameter provider:str as input and returns a client object based on the input string. The  function  is similar to go/pkg/sqirvy/client.go, except using python instead of go. the providers supported include "gemini", "anthropic", "openai", and "llama". you can assume the functions that create the clients will be implemented later.