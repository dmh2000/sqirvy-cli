.PHONY: release debug test clean test-unit test-integration pylint

build: pylint
	python -m build

debug: pylint
	python -m pip install -e .

test: pylint test-unit
	# Runner for the integration tests (uncomment when needed)
	# cd sqirvy_cli && python -m sqirvy.anthropic_test
	# cd sqirvy_cli && python -m sqirvy.gemini_test
	# cd sqirvy_cli && python -m sqirvy.openai_test
	# cd sqirvy_cli && python -m sqirvy.llama_test

test-unit:
	python -m pytest -v

test-coverage:
	python -m pytest --cov=sqirvy_cli --cov-report=term --cov-report=xml:coverage.xml

clean:
	rm -rf build dist *.egg-info
	$(MAKE) -C sqirvy_cli clean

pylint:
	pylint sqirvy_cli || true