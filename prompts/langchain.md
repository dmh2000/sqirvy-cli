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
