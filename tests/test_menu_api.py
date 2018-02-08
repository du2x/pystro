"""
    Tests about menu management
"""
import unittest

from flask import json
from flask_testing import TestCase

from application import create_app
from application.models.user import User


class ItemModelCase(TestCase):

    TESTING = True

    def create_app(self):
        # pass in test configuration
        app, db = create_app()
        self.db = db
        return app

    def setUp(self):
        self.db.create_all()
        u1 = User(email='john@example.com', is_manager=True)
        u1.set_password('123')
        u2 = User(email='susan@example.com')
        u2.set_password('123')
        self.db.session.add(u1)
        self.db.session.add(u2)
        self.db.session.commit()
        
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_items_post(self):
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username='john@example.com',
                                password='123')
                             ),
                             content_type='application/json').data)
        token = data['access_token']
        self.assertEquals(
            self.client.post('/items',
                             data=json.dumps(dict(
                                title='Delicioso prato de batata',
                                description='Batata rustica com amendoin e \
                                    alecrim e canela')),
                             content_type='application/json',
                             headers={'Authorization': 'JWT ' + token}
                             ).status_code, 201)


if __name__ == '__main__':
    unittest.main(verbosity=2)
