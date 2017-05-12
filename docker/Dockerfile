FROM ubuntu:16.04
MAINTAINER Aaron Bloomfield "aaron@virginia.edu"

# step 1: update the system and install apt-utils and locales
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y -q -q
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q -q apt-utils locales
RUN DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y -q -q

# step 2: fix the locale
RUN locale-gen en_US.UTF-8

# step 3: set up root mysql password as 'password'
RUN echo mysql-server mysql-server/root_password password password > /tmp/debconf
RUN echo mysql-server mysql-server/root_password_again password password >> /tmp/debconf
RUN debconf-set-selections /tmp/debconf
RUN /bin/rm -f /tmp/debconf

# step 4: install necessary packages
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q -q openssh-client git python3 python3-pip mysql-server libmysqlclient-dev supervisor openssh-server apache2 libapache2-mod-wsgi-py3 apt-transport-https ca-certificates curl software-properties-common

# step 5: apt-get clean
RUN DEBIAN_FRONTEND=noninteractive apt-get clean -y -q -q

# step 6: upgrade pip
RUN pip3 install --upgrade pip

# step 7: clone the tools repo
RUN mkdir -p ~/.ssh
RUN ssh-keyscan github.com > ~/.ssh/known_hosts
RUN cd /root; git clone https://github.com/uva-slp/pico

# step 8: install necessary python packages
RUN cd /root/pico/docs; pip3 install -r packages.txt

# step 9: set up the database to be initialized upon image startup
RUN mkdir /init-db
COPY 000-db-init.sql /init-db/
COPY schema.sql /init-db/
COPY pico-init.sh /
RUN chmod 755 /pico-init.sh

# step 10: make sure root can log in
RUN echo 'root:password' | chpasswd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

# step 11: install docker in docker (adapted from https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository)
#RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q -q apt-transport-https ca-certificates curl software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q -q docker-ce

# step 12: set up supervisor (adapted from
# https://docs.docker.com/engine/admin/using_supervisord/)
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/log/supervisor /var/run/mysqld/ /var/run/sshd
RUN chown mysql:mysql /var/run/mysqld/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]

# step 13: configure the app's local settings (key generation from
# https://www.howtogeek.com/howto/30184/10-ways-to-generate-a-random-password-from-the-command-line/)
COPY secrets.py /root/pico/app/pico/secrets.py
RUN echo SECRET_KEY = \'`< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-50}`\' >> /root/pico/app/pico/secrets.py
RUN sed -ri 's_pico/static_static_g' /root/pico/app/pico/settings.py

# step 14: configure the web app directory
RUN cd /root/pico; python3 app/manage.py collectstatic --noinput
RUN mv /root/pico /var/www/
RUN chown -R www-data:www-data /var/www/pico/

# step 15: configure apache2
COPY django.conf /etc/apache2/conf-available/pico-django.conf
RUN a2enconf pico-django

# step 16: some final configuration
RUN gpasswd -a www-data docker
COPY my.cnf /root/.my.cnf
EXPOSE 22 80
