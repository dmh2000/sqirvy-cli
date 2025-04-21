.PHONY: build test clean review

SUBDIRS = cmd pkg
PKG_SOURCES := $(shell find pkg -type f -name '*.go')
CMD_SOURCES := $(shell find cmd -type f -name '*.go')
SOURCES:= $(PKG_SOURCES) $(CMD_SOURCES)

# silence make output. remove -s to see make output
export SILENT=-s

build:
	@for dir in $(SUBDIRS); do \
		$(MAKE) $(SILENT) -C $$dir build; \
	done

test: 
	@for dir in $(SUBDIRS); do \
		$(MAKE)  $(SILENT) -C $$dir test; \
	done
	@echo "Tests passed"

clean:
	@for dir in $(SUBDIRS); do \
		$(MAKE)  $(SILENT)  -C $$dir clean; \
	done
	-rm -rf bin

review:	build
	bin/sqirvy-review -m claude-3-5-haiku-latest  $(SOURCES) >REVIEW.md

