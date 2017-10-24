FROM ubuntu:16.04
LABEL maintainer="Aaron Bloomfield aaron@virginia.edu"
ENV DEBIAN_FRONTEND noninteractive

# build this image as either:
# docker build -t pico docker
# docker build --build-arg APT_PROXY=1.2.3.4 -t pico docker

# step 1: allow the use of a apt-cacher-ng proxy defined via
# --build-arg (this is only for the build, and is removed at the end)
ARG APT_PROXY=0.0.0.0
RUN echo $APT_PROXY | grep -v 0.0.0.0 | awk '{print "Acquire::http::Proxy \"http://" $1 ":3142\";"}' > /etc/apt/apt.conf.d/02proxy && \
    apt-get update -y -q

# step 2: update the system and install apt-utils and locales
RUN apt-get dist-upgrade -y -q -q && \
    apt-get install -y -q -q --no-install-recommends \
	    apt-utils \
	    locales && \
    apt-get clean -y

# step 2: fix the locale
RUN locale-gen en_US.UTF-8

# step 3: set up root mysql password as 'password'
RUN echo mysql-server mysql-server/root_password password password > /tmp/debconf && \
    echo mysql-server mysql-server/root_password_again password password >> /tmp/debconf && \
    debconf-set-selections /tmp/debconf && \
    /bin/rm -f /tmp/debconf

# step 4: install necessary packages
RUN apt-get install -y -q -q --no-install-recommends \
        openssh-client \
	git \
	python3 \
	python3-pip \
	mysql-server \
	libmysqlclient-dev \
	supervisor \
	openssh-server \
	apache2 \
	libapache2-mod-wsgi-py3 \
	apt-transport-https \
	ca-certificates \
	curl \
	software-properties-common && \
    apt-get clean -y

# step 5: clone the tools repo
RUN mkdir -p ~/.ssh && \
    ssh-keyscan github.com > ~/.ssh/known_hosts && \
    cd /root; git clone https://github.com/uva-slp/pico

# step 6: upgrade pip and install python packages
RUN pip3 install --upgrade pip && \
    pip3 install setuptools && \
    apt-get install -y -q -q --no-install-recommends gcc libpython3.5-dev && \
    cd /root/pico/docs; pip3 install -r packages.txt && \
    apt-get remove -y gcc libpython3.5-dev && \
    apt-get autoremove -y && \
    apt-get clean -y

# step 7: set up the database to be initialized upon image startup
RUN mkdir /init-db && \
    echo \#\!/bin/bash > /pico-init.sh && \
    echo "if [ -d \"/init-db/\" ]; then" >> /pico-init.sh && \
    echo "    sleep 5" >> /pico-init.sh && \
    echo "    cat /init-db/000-db-init.sql | mysql" >> /pico-init.sh && \
    echo "    cat /init-db/schema.sql | mysql pico" >> /pico-init.sh && \
    echo "    /bin/rm /init-db/*" >> /pico-init.sh && \
    echo "    rmdir /init-db" >> /pico-init.sh && \
    echo "fi" >> /pico-init.sh && \
    chmod 755 /pico-init.sh
COPY 000-db-init.sql /init-db/
COPY schema.sql /init-db/

# step 8: make sure root can log in
RUN echo 'root:password' | chpasswd && \
    sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

# step 9: install docker in docker (adapted from https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository)
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y -q -q  --no-install-recommends docker-ce && \
    apt-get clean -y

# step 10: set up supervisor (adapted from
# https://docs.docker.com/engine/admin/using_supervisord/)
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/log/supervisor /var/run/mysqld/ /var/run/sshd && \
    chown mysql:mysql /var/run/mysqld/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]

# step 11: configure the app's local settings (key generation from
# https://www.howtogeek.com/howto/30184/10-ways-to-generate-a-random-password-from-the-command-line/)
COPY secrets.py /root/pico/app/pico/secrets.py
RUN echo SECRET_KEY = \'`< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-50}`\' >> /root/pico/app/pico/secrets.py && \
    sed -ri 's_pico/static_static_g' /root/pico/app/pico/settings.py

# step 12: configure the web app directory
RUN cd /root/pico; python3 app/manage.py collectstatic --noinput && \
    mv /root/pico /var/www/ && \
    chown -R www-data:www-data /var/www/pico/

# step 13: remove the (possible) apt-cacher-ng repository
RUN /bin/rm -f /etc/apt/apt.conf.d/02proxy

# step 14: configure apache2
COPY django.conf /etc/apache2/conf-available/pico-django.conf
RUN a2enconf pico-django

# step 15: some final configuration
RUN gpasswd -a www-data docker && \
    echo "[client]" > /root/.my.cnf && \
    echo "password=password" >> /root/.my.cnf
EXPOSE 22 80

