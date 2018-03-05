import json

from flask_testing import TestCase

from api import create_app, init_api_data
from api.database import db
from api.config import TestConfig
from api.restaurants import register_restaurants_blueprints


class ApiTestCase(TestCase):

    TESTING = True

    def create_app(self):
        # pass in test configuration
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        self.init_data = init_api_data(self.app)
        register_restaurants_blueprints(self.app)

        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_ADMIN_EMAIL'],
                                password=self.init_data['USER_ADMIN_PASSWORD'])
                             ),
                             content_type='application/json').data.decode('utf-8'))
        self.john_token = data['access_token']

        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_COMMON_EMAIL'],
                                password=self.init_data['USER_COMMON_PASSWORD'])
                             ),
                             content_type='application/json').data.decode('utf-8'))
        self.susan_token = data['access_token']

        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username=self.init_data['USER_MANAGER_EMAIL'],
                                password=self.init_data['USER_MANAGER_PASSWORD'])
                             ),
                             content_type='application/json').data.decode('utf-8'))
        self.karl_token = data['access_token']
