.PHONY: release debug test clean pylint

build: pylint
	# Utils specific release commands

debug: pylint
	# Debug setup

test: pylint
	python -m pytest

clean:
	rm -rf __pycache__ *.pyc

pylint:
	pylint . || true