# CLAUDE.md - Sqirvy CLI Developer Guidelines

## Build/Lint/Test Commands
- **Go**: `make -C go debug` (build), `make -C go test` (all tests)
- **Go Single Test**: `cd go/pkg/sqirvy && go test -run TestAnthropicClient_QueryText`
- **Python**: `make -C python test` (all tests)
- **Python Pytest**: `cd python/sqirvy_cli && python -m pytest`
- **Python Single Test**: `cd python/sqirvy_cli && python -m pytest test/unit/test_cli.py::TestCliArgs::test_parse_arguments_valid -v`
- **TypeScript**: `cd ts && npm run start`

## Code Style Guidelines
- **Imports**: Standard library first, third-party second, local imports last
- **Types**: Use explicit type hints (Python), interface checks (Go)
- **Error Handling**: Return errors with context, raise specific exceptions with clear messages
- **Naming**: camelCase (private), PascalCase (exported) in Go; snake_case in Python
- **Documentation**: Every function has documentation comments/docstrings
- **Testing**: Mock external dependencies when testing

## Note
- Go tests require API keys (will be skipped if not present)
- Python tests use mocking to avoid requiring real API calls