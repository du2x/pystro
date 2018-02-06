import unittest

from flask import json
from flask_testing import TestCase

from application import create_app


class UserModelCase(TestCase):

    TESTING = True

    def create_app(self):
        # pass in test configuration
        app, db = create_app()
        self.db = db
        return app

    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_users_post(self):
        self.assertEquals(
            self.client.post('/users', data=json.dumps(dict(
                email='john@gmail.com',
                username='john',
                password='123')),
                content_type='application/json'
            ).status_code,
            201)
        self.assertEquals(
            self.client.post('/users', data=json.dumps(dict(
                username='suan',
                password='123')),
                content_type='application/json'
            ).status_code,
            400)  # email is required
        self.assertEquals(
            self.client.post('/users', data=json.dumps(dict(
                email='greatjohn@gmail.com',
                username='john',
                password='4321')),
                content_type='application/json'
            ).status_code,
            400)  # username is unique

    def test_authentication(self):
        self.test_users_post()
        self.assertEquals(
            self.client.post('/auth', data=json.dumps(dict(
                username='john',
                password='123')),
                content_type='application/json'
            ).status_code,
            200)
        self.assertEquals(
            self.client.post('/auth', data=json.dumps(dict(
                username='susan',
                password='321')),  # wrong password!
                content_type='application/json'
            ).status_code,
            401)


if __name__ == '__main__':
    unittest.main(verbosity=2)