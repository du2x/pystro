"""
    Defines classes for Models for menu management
"""
from api.database import db
from api.models import BaseModel


restaurants_managers = db.Table('restaurants_managers',
                                db.metadata,
                                db.Column('restaurant_id',
                                          db.Integer,
                                          db.ForeignKey('restaurant.id')),
                                db.Column('user_id',
                                          db.Integer,
                                          db.ForeignKey('user.id')))


class Restaurant(BaseModel):
    name = db.Column(db.String(140), index=True, nullable=False)
    subdomain = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(140))
    phone = db.Column(db.String(20))
    image_url = db.Column(db.String(140))
    url = db.Column(db.String(140))
    managers = db.relationship("User",
                               secondary=restaurants_managers,
                               back_populates='manages')

    def serializable(self):
        return {'id': self.id, 'address': self.address,
                'image_url': self.image_url, 'url': self.url,
                'subdomain': self.subdomain, 'name': self.name}

    @classmethod
    def find_by_subdomain(cls, subdomain):
        result = cls.query.filter(cls.subdomain == subdomain)
        if result.count() == 1:
            return result.first()
        return None


    def __repr__(self):
        return '<Restaurant {}>'.format(self.name)
