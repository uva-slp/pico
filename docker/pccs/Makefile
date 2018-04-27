# get the proxy based on the hostname
ifeq ($(shell hostname),orion)
	PROXY=192.168.14.6
else
	PROXY=libra.cs.virginia.edu
endif

build:
	docker build --build-arg APT_PROXY=$(PROXY) -t pccs .

run:
	@echo This image is not typically run directly...

doc:
	@echo nothing to do!

