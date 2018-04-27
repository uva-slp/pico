# get the proxy based on the hostname
ifeq ($(shell hostname),orion)
	PROXY=192.168.14.6
else
	PROXY=libra.cs.virginia.edu
endif

build:
	docker build --build-arg APT_PROXY=$(PROXY) -t pccs pccs
	docker build --build-arg APT_PROXY=$(PROXY) -t pico pico

build-no-cache:
	docker build --no-cache --build-arg APT_PROXY=$(PROXY) -t pccs pccs
	docker build --no-cache --build-arg APT_PROXY=$(PROXY) -t pico pico

run:
	echo Try running the pico image in the pico/ sub-directory

doc:
	pandoc -f markdown -c ../markdown.css -t html -o readme.html readme.md
