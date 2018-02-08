"""
    Defines classes for Models for menu management
"""
from datetime import datetime

from application.database import db
from application.models import BaseModel


class Item(BaseModel):
    title = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.String(140))
    image_url = db.Column(db.String(140))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)

    def serializable(self):
        return {'id': self.id, 'title': self.title}

    def __repr__(self):
        return '<Item {}>'.format(self.title)
