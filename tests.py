from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models.user import User, Role


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_roles(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')

        r1 = Role(name='Admin')
        r2 = Role(name='Operator')
        r3 = Role(name='Client')

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()
        
        u1 = User.find_by_username('john')
        u2 = User.find_by_username('susan')
        self.assertEqual(u1.roles.all(), [])
        self.assertEqual(u2.roles.all(), [])

        u1.add_role(r1)
        u2.add_role(r2)Us
        u2.add_role(r3)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # John has exactly 1 role?
        self.assertEqual(u1.roles.count(), 1) 
        # John has the 'Admin' role?
        self.assertEqual(u1.roles.first().name, 'Admin') 
        # Susan has exactly 2 roles?
        self.assertEqual(u2.roles.count(), 2) 
        # Susan has the role 'Client'?
        self.assertTrue(u2.has_role(r3)) 
        

if __name__ == '__main__':
    unittest.main(verbosity=2)        