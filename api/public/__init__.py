"""
This packages defines the resources for the
managing restaurants and users
"""
from flask_restful import Api

from .user import UserAPI, UsersAPI, ResetPasswordAPI
from .restaurant import RestaurantAPI, RestaurantsAPI


def setup_public_api_routes(app):
    api = Api(app)    
    api.add_resource(UsersAPI, '/users', endpoint='users')
    api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
    api.add_resource(ResetPasswordAPI, '/resetpassword', endpoint='resetpw')
    api.add_resource(RestaurantAPI, '/restaurant/<string:cname>', endpoint='publicrestaurantapi')
    api.add_resource(RestaurantsAPI, '/restaurants', endpoint='publicrestaurantsapi')
    

