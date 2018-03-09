from flask_restful import Resource

from api.auth import  authenticated_user
from api.models.restaurant import Restaurant


class RestaurantAPI(Resource):

    @authenticated_user()
    def get(self, cname):
        restaurant = Restaurant.find_by_cname(cname)
        if not restaurant:
            return 404
        return restaurant.serializable(), 200


class RestaurantsAPI(Resource):

    @authenticated_user()
    def get(self):
        return Restaurant.find_all()