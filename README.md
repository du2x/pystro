
pystro
========

[![Build Status](https://travis-ci.org/du2x/pystro.svg?branch=master)](https://travis-ci.org/du2x/pystro) 

pystro is a **simple** and easy to use and to extend api for restaurant managements apps.

pystro has basic restaurant business functionalities:
- user authentication and authorization (using jwt)
- users management
- menu management (sections, items)
- orders managment
- restaurant units management 


It is written in Flask, tries to follow principles SOLID, KISS and DRY and Flask specific best practices, taking, for example, [miguelgrinberg](https://github.com/miguelgrinberg) as one of the main references. We also follow pep8 style guide.

pystro uses SQLAlchemy as ORM framework. The models of pystro are those on the following class diagram:

![models class diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.github.com/du2x/pystro/master/docs/models_cd.txt)


Usage
--------

pystro runs with python3 (and *possibly* with python2). There are a docker container configuration. You can run pystro with or without docker.



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
**pystro** will be always open source, licensed under GPL3.

Feel free to contribute!
