"""
    Tests about menu management
"""
import unittest

from flask import json
from flask_testing import TestCase

from application import create_app
from application.database import db
from application.config import TestConfig
from application import init_api_data
from application.restaurants import register_restaurants_blueprints


class ItemModelCase(TestCase):

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

    def test_items_post(self):
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_ADMIN_EMAIL'],
                                password=self.init_data['USER_ADMIN_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.post(self.init_data['RESTAURANT_SUBDOMAIN'] + '/items',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps(dict(
                                title='Delicioso prato de batata',
                                price=10,
                                description='Batata rustica com amendoin e \
                                    alecrim e canela')),
                             content_type='application/json').status_code, 201)
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_MANAGER_EMAIL'],
                                password=self.init_data['USER_MANAGER_PASSWORD'])
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.post(self.init_data['RESTAURANT_SUBDOMAIN'] + '/items',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps(dict(
                                title='Lentilhas com bardana',
                                price=12,
                                description='Lentilha cozida com raiz de bardana')),
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
            self.client.post(self.init_data['RESTAURANT_SUBDOMAIN'] + '/items',
                             headers={'Authorization': 'JWT ' + token},
                             data=json.dumps(dict(
                                title='Shitake',
                                price=13,
                                description='Sopa de cogumelos')),
                             content_type='application/json').status_code, 403)


if __name__ == '__main__':
    unittest.main(verbosity=2)
