
pystro
========

[![Build Status](https://travis-ci.org/du2x/pystro.svg?branch=master)](https://travis-ci.org/du2x/pystro) 

Pystro is a **simple** and easy to use and to extend api for restaurant managements apps.

Pystro has basic restaurant business functionalities:
- user authentication and authorization (using jwt)
- users management
- menu management (sections, items)
- orders managment


It is written in Flask, following the principles SOLID, KISS, YAGNI, DRY and Flask specific best practices, taking [miguelgrinberg](https://github.com/miguelgrinberg) as one of the main references. We also follow pep8 style guide.

Usage
--------

Pystro runs with python3 (and *possibly* with python2). There are a docker container configuration. You can run pystro with or without docker.


With docker
------

Simply run docker-compose.

`docker-compose up --build`

Without docker
------

1. First, you need to install mysql 5-6+ and create the pystro database
and user.

    Enter mysql shell (`mysql -uroot -p`) and type the following commands:

    `create database pystro;`

    `create user pystro@localhost;`

    `grant all privileges on pystro.* to pystro@localhost identified by 'devpassword';`

2. Create and activate the python virtualenv.

    `virtualenv -p python3 venv`

    `source venv/bin/activate.sh`

3. export FLASK_APP

    `export FLASK_APP=pystro.py`

4. run it

    `flask run`


We are open!
-----
**Pystro** will be always open source, licensed under GPL3.

Feel free to contribute!
