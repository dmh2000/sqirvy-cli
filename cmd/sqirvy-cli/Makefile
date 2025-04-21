.PHONY: build test clean

PROJECT=sqirvy-cli
BINDIR=../../bin

# detect variants of Windows
ifeq ($(filter Windows%, $(OS)),Windows)
    arch := Windows
else
    arch := $(shell uname -s)
	ifeq ($(arch),Darwin)
		arch := darwin
	else 
		ifeq ($(arch),Linux)
			arch := linux
		else 
			echo "Unsupported OS: $(arch)"
			exit 1
		endif
	endif
endif

build: 
	staticcheck ./...
	go vet ./...
	mkdir -p $(BINDIR)
	GOOS=$(arch) GOARCH=amd64 go build -o $(BINDIR)/$(PROJECT) .
	
# build with compression 
# rm $(BINDIR)/$(PROJECT)
# GOOS=$(arch) GOARCH=amd64 go build . 
# upx -1 -o $(BINDIR)/$(PROJECT) $(PROJECT)

test:
	@./test.sh 
	@echo "Tests passed"
	
clean:
	rm -rf $(PROJECT)
	rm -rf $(BINDIR)
	rm -rf ./test
