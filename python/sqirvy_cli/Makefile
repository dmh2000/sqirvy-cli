.PHONY: test test-unit test-integration build

test: test-unit
	# Runner for the integration tests (uncomment when needed)
	# cd sqirvy_cli && python -m sqirvy.anthropic_test
	# cd sqirvy_cli && python -m sqirvy.gemini_test
	# cd sqirvy_cli && python -m sqirvy.openai_test
	# cd sqirvy_cli && python -m sqirvy.llama_test

test-unit:
	python -m pytest -v

test-coverage:
	python -m pytest --cov=sqirvy_cli --cov-report=term --cov-report=xml:coverage.xml

release:
	python -m build
