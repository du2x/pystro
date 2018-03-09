"""
This packages defines the resources for the
managing restaurants and users
"""
from flask import current_app, Blueprint
from flask_restful import Api

from .restaurant import RestaurantsAPI, RestaurantAPI


def setup_admin_api_routes(app):
    api_bp = Blueprint('admin', 'pystro')
    api = Api(api_bp)
    api.add_resource(RestaurantsAPI, '/restaurants', endpoint='restaurantsapi')
    api.add_resource(RestaurantAPI, '/restaurant/<int:id>',
                     endpoint='restaurantapi')
    app.register_blueprint(api_bp, url_prefix='/admin')
