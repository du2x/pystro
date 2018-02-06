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
        with self.app.test_client() as client:     
            self.assertEquals(
                client.post('/users', data=json.dumps(dict(
                    email='john@gmail.com',
                    username='john',
                    password='123')),
                    content_type='application/json'
                ).status_code, 
                201)            
        

if __name__ == '__main__':
    unittest.main(verbosity=2)        