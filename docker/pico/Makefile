# get the proxy based on the hostname
ifeq ($(shell hostname),orion)
	PROXY=192.168.14.6
else
	PROXY=libra.cs.virginia.edu
endif

build:
	docker build --build-arg APT_PROXY=$(PROXY) -t pico .

run:
	docker run -v /var/run/docker.sock:/var/run/docker.sock -dP pico

doc:
	@echo nothing to do!

