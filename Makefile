.PHONY: test debug release clean

test:
	$(MAKE) -C python test
	$(MAKE) -C go

debug:
	$(MAKE) -C go debug
	
release:
	$(MAKE) -C go build
	$(MAKE) -C python build
