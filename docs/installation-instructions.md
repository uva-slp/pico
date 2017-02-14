# Installation Instructions

These instructions outline the process of installing PCCS. Note that the process of setting up a server to host the Django site is not elaborated upon. If you would like to host PCCS on your own webserver, consult the [Django documentation](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/), which recommends using Apache. There are also a number of third party hosting options available, such as Heroku.

0. Install Python3 and MySQL

1. Fork the [PCCS Repository](https://github.com/uva-slp/pccs) using [this tutorial](https://help.github.com/articles/fork-a-repo/)

2. Install required Python packages
  - `pip install -r app/docs/packages.txt`

3. Setup a MySQL Database for PCCS to use
  - Ensure that database permissions are granted to the host user

4. Create an email account to associate with the server

5. Update `/app/pccs/secrets.py`
  - Set a new Django Secret Key
  	- Consider using a generator like [this](http://www.miniwebtool.com/django-secret-key-generator/)
  - Enter the database info from Step 3
  - Enter the server email info from Step 4

6. Run the server and enjoy!
  - To run local, use the `/app/runserver` script or `python3 manage.py runserver`
