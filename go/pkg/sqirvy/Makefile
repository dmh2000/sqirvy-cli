.PHONY: build test clean


build:
	staticcheck ./...
	go vet ./...

test:
	@echo "Testing pkg/sqirvy"
	go test -timeout 2m .

clean:
	@echo "pkg/sqirvy"