Smartlunch
========

Smartlunch is a **simple** and easy to use and to extend restaurant api and webapp, designed specially for small restaurants that serves **lunch** - there are (will be) two function that stands out in this context: Subscription and pre-ordering a lunch plate (for customers in a hurry). 

It is written in Flask, following the best practices, taking @miguelgrinberg as one of the main references. 


Brief Api Description
----

The api has three main modules:
- Users management and authentication.
    - Models: User, Role.
- Menu management.
    - Models: Item, Special.
- Orders management.
    - Models: Order.
- Subscription.
    - Models: Subscription.


Brief Web app description
-----
The webapp will be a **simple** website, with an administration panel and a front store page, which will consume the Smartlunch api to get the items and specials to show.

There will be also an android client which will consume the Smartlunch api, but these will be on other github repo.

Feel free to contribute!
