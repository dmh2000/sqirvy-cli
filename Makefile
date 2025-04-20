.PHONY: build test  clean

SILENT=-s

build:
	$(MAKE) $(SILENT) -C go build

test:
	$(MAKE) $(SILENT)-C go

clean:
	$(MAKE) $(SILENT) -C go clean