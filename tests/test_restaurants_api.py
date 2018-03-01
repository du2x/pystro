"""
    Tests about restaurant management
"""
import unittest

from flask import json
from flask_testing import TestCase

from application import create_app
from application.database import db
from application.config import TestConfig
from application import init_api_data
from application.restaurants import register_restaurants_blueprints


class RestaurantModelCase(TestCase):

    TESTING = True

    def create_app(self):
        # pass in test configuration
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        self.init_data = init_api_data(self.app)
        register_restaurants_blueprints(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restaurants_post(self):
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_ADMIN_EMAIL'],
                                password=self.init_data['USER_ADMIN_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.post('restaurants',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps(dict(
                                name='Gaules',
                                subdomain='gaules',
                                phone='31 99832171')),
                             content_type='application/json').status_code, 201)
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                               username=self.init_data['USER_COMMON_EMAIL'],
                               password=self.init_data['USER_COMMON_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.post('restaurants',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps(dict(
                                name='Familia Paulista',
                                subdomain='familia-paulista',
                                phone='31 99832333')),
                             content_type='application/json').status_code, 403)

    def test_restaurants_put(self):
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_ADMIN_EMAIL'],
                                password=self.init_data['USER_ADMIN_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.put('restaurant/1' + str(self.init_data['RESTAURANT_ID']),
                            headers={'Authorization': 'JWT ' + token},
                            data=json.dumps(dict(
                              name='O Almazén',
                              phone='31 33292052')),
                            content_type='application/json').status_code, 200)
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_COMMON_EMAIL'],
                                password=self.init_data['USER_COMMON_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.put('restaurant/' + str(self.init_data['RESTAURANT_ID']),
                            headers={'Authorization': 'JWT ' + token},
                            data=json.dumps(dict(
                              name='A Almazén',
                              phone='31 33292052')),
                            content_type='application/json').status_code, 403)


if __name__ == '__main__':
    unittest.main(verbosity=2)
