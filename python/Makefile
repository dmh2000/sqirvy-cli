.PHONY: release debug test clean pylint

build:
	$(MAKE) -C sqirvy_cli release

debug: pylint
	$(MAKE) -C sqirvy_cli debug

test: pylint
	$(MAKE) -C sqirvy_cli test

clean:
	$(MAKE) -C sqirvy_cli clean

pylint:
	$(MAKE) -C sqirvy_cli pylint

test-unit:
	$(MAKE) -C sqirvy_cli test-unit

test-coverage:
	$(MAKE) -C sqirvy_cli test-coverage