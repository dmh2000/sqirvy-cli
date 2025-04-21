.PHONY:  build test clean

build:
	staticcheck ./...
	go vet ./...

test:
	@echo "Testing pkg/util"
	go test .

clean:
	@echo "pkg/util"