# This Dockerfile is part of the uva-slp/pico repository, and will
# create the execution environment used by the contest system

# build this image as either:
# docker build -t pccs .
# docker build --build-arg APT_PROXY=1.2.3.4 -t pccs .

FROM python:3

# step 1: allow the use of a apt-cacher-ng proxy defined via
# --build-arg (this is only for the build, and is removed at the end)
ARG APT_PROXY=0.0.0.0
RUN echo $APT_PROXY | grep -v 0.0.0.0 | awk '{print "Acquire::http::Proxy \"http://" $1 ":3142\";"}' > /etc/apt/apt.conf.d/02proxy

# step 2: install some packages
RUN apt-get update -y -q -q && \
     apt-get -y -y -q install --no-install-recommends \
     g++ \
     default-jdk \
     sudo

# step 3: remove the (possible) apt-cacher-ng repository
RUN /bin/rm -f /etc/apt/apt.conf.d/02proxy
