"""
This packages defines implementations that concerns the
restaurants blueprints.
"""

from flask import Blueprint, request
from flask_restful import Api

from api.models.restaurant import Restaurant
from api.database import db

from .menu import ItemAPI, ItemsAPI, MenuAPI, SectionAPI, SectionsAPI
from .orders import OrdersAPI


def _register_restaurant_blueprint(app, restaurant):
    api_bp = Blueprint(restaurant['cname'], 'pystro')
    api = Api(api_bp)
    setup_restaurant_api_routes(api)
    app.register_blueprint(api_bp, url_prefix='/' + restaurant['cname'])


def register_restaurants_blueprints(app):
    for restaurant in Restaurant.find_all():
        _register_restaurant_blueprint(app, restaurant)


def register_restaurant(app, restaurant_dict):
    restaurant = Restaurant(**restaurant_dict)
    db.session.add(restaurant)
    db.session.commit()
    _register_restaurant_blueprint(app, restaurant_dict)


def setup_restaurant_api_routes(api):
    api.add_resource(ItemsAPI, '/items', endpoint='items')
    api.add_resource(ItemAPI, '/item/<int:id>', endpoint='item')
    api.add_resource(SectionAPI, '/section/<int:id>', endpoint='section')
    api.add_resource(SectionsAPI, '/sections', endpoint='sections')
    api.add_resource(OrdersAPI, '/orders', endpoint='orders')
    api.add_resource(MenuAPI, '/menu', endpoint='menu')
