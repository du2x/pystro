"""
This packages defines the resources for the
managing restaurants and users
"""
from application.admin.user import UserAPI, UsersAPI, ResetPasswordAPI
from application.admin.restaurant import RestaurantsAPI, RestaurantAPI


def set_admin_api_routes(api):
    api.add_resource(UsersAPI, '/users', endpoint='users')
    api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
    api.add_resource(ResetPasswordAPI, '/resetpassword', endpoint='resetpw')
    api.add_resource(RestaurantsAPI, '/restaurants', endpoint='restaurantsapi')
    api.add_resource(RestaurantAPI, '/restaurant/<int:id>',
                     endpoint='restaurantapi')

