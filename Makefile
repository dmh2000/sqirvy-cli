.PHONY: build test  clean

SILENT=-s

build:
	$(MAKE) $(SILENT) -C go build

test:
	$(MAKE) $(SILENT) -C go test

clean:
	$(MAKE) $(SILENT) -C go clean