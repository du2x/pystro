import unittest

from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError

from application.models.user import User
from application.models.menu import Item
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
        u = User(email='susan@gmail.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_users_inserts(self):
        u1 = User(email='john@example.com')
        u1.set_password('123')
        u2 = User(email='susan@example.com')
        u2.set_password('123')
        u3 = User(email='john@example.com')
        u3.set_password('123')        

        self.db.session.add(u1)
        self.db.session.add(u2)
        self.db.session.commit()

        self.db.session.add(u3)
        self.assertRaises(IntegrityError, self.db.session.commit)
        self.db.session.rollback()

    def test_items_inserts(self):
        i1 = Item(title='Acabaxi', description='A great abacaxi. Very big.')
        i2 = Item(title='Banana', description='A great bannanana. Very big.')
        self.db.session.add(i1)
        self.db.session.add(i2)
        self.db.session.commit()
        i3 = Item(title='Banana', description='A mini banana.')
        self.db.session.add(i3)
        self.assertRaises(IntegrityError, self.db.session.commit)
        self.db.session.rollback()


    def test_users_find(self):
        self.test_users_inserts()
        u1 = User.find_by_email('john@example.com')
        u2 = User.find_by_email('susan@example.com')
        self.assertEquals(u1.email, 'john@example.com')
        self.assertEquals(u2.email, 'susan@example.com')


if __name__ == '__main__':
    unittest.main(verbosity=2)
