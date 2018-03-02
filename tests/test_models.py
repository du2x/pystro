import unittest

from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError

from api.models.user import User
from api.models.menu import Item
from api.models.order import Order, OrderItem
from api.database import db
from api import create_app
from api.config import TestConfig


class UserModelCase(TestCase):

    TESTING = True

    def create_app(self):
        # pass in test configuration
        app = create_app(TestConfig)
        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(email='susan@gmail.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_users_inserts(self):
        u1 = User(email='john@example.com', name='John')
        u1.set_password('123')
        u2 = User(email='susan@example.com', name='Susan')
        u2.set_password('123')
        u3 = User(email='john@example.com')
        u3.set_password('123')        

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        db.session.add(u3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

    def test_items_inserts(self):
        i1 = Item(title='Acabaxi', description='A great abacaxi. Very big.',
                  price=5, restaurant_id=1)
        i2 = Item(title='Banana', description='A great bannanana. Very big.',
                  price=3, restaurant_id=1)
        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()
        i3 = Item(title='Banana', description='A mini banana.', price=4,
                  restaurant_id=1)
        db.session.add(i3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

    def test_users_find(self):
        self.test_users_inserts()
        u1 = User.find_by_email('john@example.com')
        u2 = User.find_by_email('susan@example.com')
        self.assertEquals(u1.name, 'John')
        self.assertEquals(u2.name, 'Susan')

    def test_orders_inserts(self):
        self.test_users_inserts()
        i1 = Item(title='Acabaxi',
                  description='A great abacaxi. Very big.',
                  price=5,
                  restaurant_id=1)
        i2 = Item(title='Banana',
                  description='A great bannanana. Very big.',
                  price=3,
                  restaurant_id=1)
        db.session.add(i1)
        db.session.add(i2)
        o1 = Order()
        db.session.add(o1)
        db.session.flush()
        db.session.refresh(o1)
        db.session.refresh(i1)
        db.session.refresh(i2)
        o1.orderitems.append(OrderItem(order_id=o1.id,
                                       item_id=i1.id, quantity=2))
        o1.orderitems.append(OrderItem(order_id=o1.id,
                                       item_id=i2.id, quantity=1))
        db.session.commit()
        retrieved = Order.find_by_id(o1.id)
        self.assertEquals(retrieved.total_price(), 2*i1.price + i2.price)


if __name__ == '__main__':
    unittest.main(verbosity=2)
