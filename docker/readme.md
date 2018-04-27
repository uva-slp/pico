Run PICO in Docker
==================

There are two docker images herein:

- pico, which runs the entire contest system
- pccs, which is the execution environment for a single submitted run


### Quickstart

1. Install docker (now sure how? see below)
2. Pull the image for executing submissions: `docker pull dmm7aj/pccs`
3. Build the docker image contained herein; from the pico/ directory, run `docker build -t pico docker/`
4. Run docker via: `docker run -v /var/run/docker.sock:/var/run/docker.sock -dP pico`
5. Run `docker ps -a`, and note the port that 80 is mapped to (something like 32780); browse to that port (http://localhost:32780)
    - You can also ssh in via the other port redirected (`ssh root@localhost -p 32779`)
	- The login to the web page is admin/admin; root's password is 'password', and it can automatically log into mysql (but root's password there is 'password' again)

### Installing docker

One must first install docker;
[https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/)
is a good place to start (install the Stable Docker CE version); the
Ubuntu specific directions are
[here](https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository).
One will likely want to allow non-privileged users to run docker; see
[http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo](http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)
for details.  That link is Ubuntu specific, but will apply to any
Linux system.  Other operating systems are possible, but those links
are not in this document.

### Notes

This is not really running docker-in-docker; it's using the host's docker socket.  This is described at [https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/) (in "The solution" section).  To start the container, run:
