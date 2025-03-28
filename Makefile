.PHONY: test

test:
	$(MAKE) -C python test
	$(MAKE) -C go


#	$(MAKE) -C go test
