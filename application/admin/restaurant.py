"""
    Defines APIs for restaurants management.
"""
from flask import current_app
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

from application.models.restaurant import Restaurant
from application.database import db
from application.auth import only_admin
from application.restaurants import register_restaurant


nameArg = reqparse.Argument(name='name', type=str,
                            required=True,
                            help='name of restaurant',
                            location='json')
subdomainArg = reqparse.Argument(name='subdomain', type=str,
                                 required=True,
                                 help='subdomain of restaurant',
                                 location='json')                            
phoneArg = reqparse.Argument(name='phone', type=str,
                             required=True,
                             help='phone of restaurant',
                             location='json')
addressArg = reqparse.Argument(name='address', type=str,
                               required=False,
                               help='No email provided',
                               location='json')
imgArg = reqparse.Argument(name='image_url', type=str,
                           required=False,
                           help='img url for restaurant',
                           location='json')
mngArg = reqparse.Argument(name='managers', type=list,
                           required=False,
                           default=[],
                           help='users ids of managers for restaurant',
                           location='json')


class RestaurantsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(RestaurantsAPI, self).__init__()

    def get(self):
        return Restaurant.find_all()

    @only_admin()
    def post(self):
        """ creates a restaurant """
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(subdomainArg)
        self.reqparse.add_argument(phoneArg)
        self.reqparse.add_argument(addressArg)
        self.reqparse.add_argument(imgArg)
        self.reqparse.add_argument(mngArg)
        data = self.reqparse.parse_args()
        try:
            restaurant = Restaurant()
            for key in data.keys():
                setattr(restaurant, key, data[key])
            register_restaurant(current_app, data)
            return restaurant.serializable(), 201
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 500


class RestaurantAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(RestaurantAPI, self).__init__()

    @only_admin()
    def put(self, id):
        """ edits a restaurant """
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(phoneArg)
        self.reqparse.add_argument(addressArg)
        self.reqparse.add_argument(imgArg)
        self.reqparse.add_argument(mngArg)
        data = self.reqparse.parse_args()
        try:
            restaurant = Restaurant.find_by_id(id)
            if not restaurant:
                return 404
            for key in data.keys():
                setattr(restaurant, key, data[key])
            db.session.add(restaurant)
            db.session.commit()
            return restaurant.serializable(), 200
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 500
