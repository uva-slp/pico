# Installation Instructions

These instructions outline the process of installing PiCO on a clean Linux-based operating system. Note that the process of setting up a server to host the Django site is not elaborated upon. If you would like to host PiCO on your own webserver, consult the [Django documentation](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/), which recommends using Apache. There are also a number of third party hosting options available, such as Heroku.

0. Install Python, Pip, MySQL, Git, and Docker
  - Ensure apt-get is fully up-to-date
    - `sudo apt-get update`
    - `sudo apt-get upgrade`
  - Python
    - `sudo apt-get install python3`
  - Pip
    - `sudo apt-get install python3-pip`
    - `pip3 install --upgrade pip`
  - MySQL
    - `sudo apt-get install mysql-server`
      - You will be prompted for a root password
      - More detailed information on installing MySQL is available [here](https://www.linode.com/docs/databases/mysql/install-mysql-on-ubuntu-14-04)
    - `sudo apt-get install libmysqlclient-dev`
  - Git
    - `sudo apt-get install git`
  - Docker
    - Follow [these instructions](https://docs.docker.com/engine/installation/linux/ubuntu/#install-docker) to install Docker

1. Fork the [PiCO Repository](https://github.com/uva-slp/pico) using [this tutorial](https://help.github.com/articles/fork-a-repo/) and move into the repository directory
  - `git clone https://github.com/uva-slp/pico.git`
  - `cd pico`

2. Install required Python packages
  - `pip3 install -r docs/packages.txt`

3. Setup a MySQL database and user for PiCO to use
  - Open MySQL console using password set during installation
    - `mysql -u root -p`
  - Create database
    - `create database pico;`
  - Ensure database permissions are granted to the host user
    - `grant all privileges on pico.* to 'pico'@'localhost' identified by 'password';`
  - Exit MySQL console
    - `exit`

4. Create an email account to associate with the server

5. Update `app/pico/secrets.py`
  - Set a new Django Secret Key
    - Consider using a generator like [this](http://www.miniwebtool.com/django-secret-key-generator/)
  - Enter the database info from Step 3
  - Enter the server email info from Step 4

6. Set up Docker and download the Docker container
  - Install the Docker container by running `sudo docker pull dmm7aj/pccs`
  - Allow the server to run Docker without sudo by adding them to the docker group. Run:
    - `sudo groupadd docker`
    - `sudo gpasswd -a ${USER} docker`
    - `sudo service docker restart`
    - `newgrp docker`

7. Apply database migrations
  - `python3 app/manage.py migrate`

8. Collect static files
  - `python3 app/manage.py collectstatic`

9. Add superuser
  - `python3 app/manage.py loaddata users_admin`

9. Run the server and enjoy!
  - To run locally, use the `app/runserver.sh` script or `python3 app/manage.py runserver`
  - Credentials
    - Username: admin
    - Password: admin
  - System administrators are strongly urged to change the admin password immediately following successful setup of the system
