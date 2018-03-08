"""
This packages defines the resources for the
managing restaurants and users
"""
from .restaurant import RestaurantsAPI, RestaurantAPI

def setup_admin_api_routes(api):
    api.add_resource(RestaurantsAPI, '/restaurants', endpoint='restaurantsapi')
    api.add_resource(RestaurantAPI, '/restaurant/<int:id>',
                     endpoint='restaurantapi')

