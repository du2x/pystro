"""
    Tests about users management and authentication
"""
import unittest
import json
import jwt

from flask import current_app

from api.models.user import User

from . import ApiTestCase


class UserModelCase(ApiTestCase):

    def test_users_post(self):
        self.assertEquals(
            self.client.post('/users', data=json.dumps(dict(
                email='joe@gmail.com')),
                content_type='application/json'
            ).status_code,
            201)
        joe_token = jwt.encode(
                {'user_email': 'joe@gmail.com'},
                current_app.config['JWT_SECRET_KEY'],
                current_app.config['JWT_ALG']).decode("utf-8")
        self.assertEquals(
            self.client.put('/users',
                            data=json.dumps(dict(
                                email='joe@gmail.com',
                                name='joe',
                                phone='31 999121722',
                                password='123',
                                is_admin=True,
                                activation_token=joe_token
                                )),
                            content_type='application/json').status_code, 200)
        self.assertEquals(
            self.client.post('/users', data=json.dumps(dict(
                email='juliet@gmail.com')),
                content_type='application/json'
            ).status_code,
            201)
        juliet_token = jwt.encode(
                {'user_email': 'juliet@gmail.com'},
                current_app.config['JWT_SECRET_KEY'],
                current_app.config['JWT_ALG']).decode('utf-8')
        self.assertEquals(
            self.client.put('/users', data=json.dumps(dict(
                email='juliet@gmail.com',
                name='juliet',
                phone='31 989121722',
                password='123',
                activation_token=str(juliet_token))),
                content_type='application/json'
            ).status_code,
            200)
        self.assertEquals(
            self.client.post('/users', data=json.dumps(dict(
                email='joe@gmail.com')),
                content_type='application/json'
            ).status_code,
            203)  # email has to be unique

    def test_authentication(self):
        self.test_users_post()
        self.assertEquals(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username='joe@gmail.com',
                                password='123')),
                             content_type='application/json')
            .status_code, 200)
        self.assertEquals(
            self.client.post('/auth', data=json.dumps(dict(
                username='juliet@gmail.com',
                password='321')),  # wrong password!
                content_type='application/json'
            ).status_code,
            401)

    def test_role_required_endpoint(self):
        self.test_users_post()
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username='joe@gmail.com',
                                password='123')
                             ),
                             content_type='application/json').data.decode('utf-8'))
        joe_token = data['access_token']
        self.assertEquals(
            self.client.get('/users',
                            headers={'Authorization': 'JWT ' + joe_token}
                            ).status_code, 200)  # joe is admin
        data = json.loads(
            self.client.post('/auth',
                             data=json.dumps(dict(
                                username='juliet@gmail.com',
                                password='123')
                             ),
                             content_type='application/json').data.decode('utf-8'))
        juliet_token = data['access_token']
        self.assertEquals(
            self.client.get('/users',
                            headers={'Authorization': 'JWT ' + juliet_token})
            .status_code, 403)  # juliet is not admin
        john = User.find_by_email('joe@gmail.com')
        self.assertEquals(
            self.client.put('/user/' + str(john.id),
                            headers={'Authorization': 'JWT ' + juliet_token},
                            data=json.dumps(dict(name='john')),
                            content_type='application/json')
            .status_code, 403)  # juliet is not admin and is not joe            
        juliet = User.find_by_email('juliet@gmail.com')
        self.assertEquals(
            self.client.put('/user/' + str(juliet.id),
                            headers={'Authorization': 'JWT ' + juliet_token},
                            data=json.dumps(dict(name='julyet')),
                            content_type='application/json')
            .status_code, 200)  # susan can edit herself


if __name__ == '__main__':
    unittest.main(verbosity=2)
