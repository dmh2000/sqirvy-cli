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

in file python/sqirvy-cli/sqirvy/client.py, create a function named NewClient that takes parameter provider:str as input and returns a client object based on the input string. The  function  is similar to go/pkg/sqirvy/client.go, except using python instead of go. the providers supported include "gemini", "anthropic", "openai", and "llama". you can assume the functions that create the clients will be implemented later.

in file python/sqirvy-cli/sqirvy/anthropic.py, create a function NewAnthropicClient that is similar to the same function in go/pkg/sqirvy/anthropic.go. It will create an instance of interface Client that checks for the anthropic api key from the environment, then creates an insance of the LangChain anthropic object. import the LangChain package for the anthropic llm as weel as any other imports required. 

refactor python/sqirvy-cli/sqirvy/anthropic_client.py to use the native anthropic SDK instead of langchain. change only this file, do not change any other files. in the QuertyText function, do not call QueryTextLangchain, instead use the anthropic sdk to make send the query directly.

- modify python/sqirvy_cli/sqirvy_cli/main.py so it behaves as follows:
  - "sqirvy_cli <command> <flags..> <filenames, urls>
  - where the commands are:
    - "query"
    - "plan"
    - "code"
    - "review"
  - the command name comes first, then the flags (if any) and file/url arguments (if any)
- update python/sqirvy_cli/sqirvy_cli/test_cli.py as needed
  

in python/sqirvy-cli/sqirvy_cli/main.py, update the "parse_arguments" function to accept command line arguments in the following order:
"sqirvy_cli <command> <model> <temperature> [filenames..., urls...]"
- <command> 
   - command is a string that has only one of the following values:
   - query
   - plan
   - code
   - review
- <model>
  - -m "modelname"
  - --mode "modelname"
- <temperature>
  - -t n             (where n is a floating point value in the range (0..1.0]
  - --temperature n  (where n is a floating point value in the range (0..1.0]
- any number of filenames and urls after all other arguments


create a new file, python/sqirvy_cli/sqirvy_cli/test_args.sh. this file will be a bash script. on each   line of the script it will run main.py with various combinations of arguments and print the output. it  does not need to validate the output. include instances where main.py gets input from stdin using "echo  hello from stdin". create as many tests as needed to cover most combinations of arguments.   

create a new file python/sqirvy-cli/sqirvy-cli/context.py. in this file, add a python dataclass 'Context' that has the following fields:
- command (string)
- model (string)
- temperature (float)
- files (list of strings)
- system (string)
- prompt (string)
add a function that constructs an instance of the context dataclass. the function will take parameters for each field and initialize it



