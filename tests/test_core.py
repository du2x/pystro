import unittest

from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError

from application.models.user import User
from application import create_app


class UserModelCase(TestCase):

    TESTING = True

    def create_app(self):
        # pass in test configuration
        app, db = create_app()
        self.db = db
        return app

    def setUp(self):        
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_users_inserts(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('123')
        u2 = User(username='susan', email='susan@example.com')
        u2.set_password('123')
        u3 = User(username='john', email='greatjohn@example.com')
        u3.set_password('123')        

        self.db.session.add(u1)
        self.db.session.add(u2)
        self.db.session.commit()

        self.db.session.add(u3)
        self.assertRaises(IntegrityError, self.db.session.commit)
        self.db.session.rollback()

    def test_users_find(self):
        self.test_users_inserts()
        u1 = User.find_by_username('john')
        u2 = User.find_by_username('susan')
        self.assertEquals(u1.email, 'john@example.com')
        self.assertEquals(u2.email, 'susan@example.com')


if __name__ == '__main__':
    unittest.main(verbosity=2)
