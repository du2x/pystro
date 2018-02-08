Smartlunch
========

[![Join the chat at https://gitter.im/du2x/smartlunch](https://badges.gitter.im/du2x/smartlunch.svg)](https://gitter.im/du2x/smartlunch?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Smartlunch is a **simple** and easy to use and to extend api for restaurant managements apps.

It is written in Flask, following the principles SOLID, KISS, YAGNI, DRY and Flask specific best practices, taking [miguelgrinberg](https://github.com/miguelgrinberg) as one of the main references. We also follow pep8 style guide.

Running it
--------

Smartlunch runs with python3 (and *possibly* with python2)

create virtualenv.

`virtualenv -p python3 venv`


activate virtualenv

`source venv/bin/activate.sh`


export FLASK_APP (this is made automatically if you have `autoenv`)

`export FLASK_APP=smartlunch.py`


run it

`flask run`

Brief Api Description
----

The api has three main modules:
- Users management and authentication.
    - Models: User.
- Menu management.
    - Models: Item, Special.
- Orders management.
    - Models: Order.
- Subscription.
    - Models: Subscription, Payment, CreditCard.


We are open!
-----
**Smartlunch** will be always open source, licensed under GPL3.

Feel free to contribute!
