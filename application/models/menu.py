"""
    Defines classes for Models for menu management
"""
from application.database import db
from application.models import ContentModel


class Item(ContentModel):
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    image_url = db.Column(db.String(140))
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Item {}>'.format(self.title)

    @classmethod
    def find_by_section_id(cls, section_id):
        result = cls.query.filter(cls.section_id == section_id)
        if result.count() > 0:
            return result
        return []

    def serializable(self):
        return {'id': self.id, 'title': self.title, 'price': self.price,
                'image_url': self.image_url}


class Section(ContentModel):
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    def __repr__(self):
        return '<Section {}>'.format(self.title)

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id):
        result = cls.query.filter(cls.restaurant_id == restaurant_id)
        if result.count() > 0:
            return result
        return []
