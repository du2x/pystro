"""
    Tests about orders management
"""
import unittest

from flask import json
from flask_testing import TestCase

from api import create_app
from api.database import db
from api.config import TestConfig
from api import init_api_data
from api.restaurants import register_restaurants_blueprints


class OrdersModelCase(TestCase):

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

    def test_orders(self):
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                               username=self.init_data['USER_COMMON_EMAIL'],
                               password=self.init_data['USER_COMMON_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        post_response = self.client.post(
                self.init_data['RESTAURANT_SUBDOMAIN'] + '/orders',
                    headers={'Authorization': 'JWT ' + token},
                    data=json.dumps(dict(
                    items=[{'id': 1,'quantity': 1},
                           {'id': 2, 'quantity': 1}])),
                    content_type='application/json')
        order_id = json.loads(post_response.data)['id']
        self.assertEquals(post_response.status_code, 201)
        self.assertEquals(
            self.client.put(self.init_data['RESTAURANT_SUBDOMAIN'] + '/orders',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps({'order_id': order_id}),
                             content_type='application/json').status_code, 403)
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                               username=self.init_data['USER_MANAGER_EMAIL'],
                               password=self.init_data['USER_MANAGER_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.put(self.init_data['RESTAURANT_SUBDOMAIN'] + '/orders',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps({'order_id': order_id}),
                             content_type='application/json').status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
