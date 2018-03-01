from datetime import datetime

from application.database import db


class BaseModel(db.Model):
    __abstract__ = True
    _tablename = None

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)

    def serializable(self):
        raise NotImplementedError('Oops!')

    @classmethod
    def find_by_id(cls, uid):
        result = cls.query.filter(cls.id == uid)
        if result.count() == 1:
            return result.first()
        return None

    @classmethod
    def find_all(cls):
        return [obj.serializable() for obj in cls.query.all()]


class ContentModel(BaseModel):
    __abstract__ = True
    _tablename = None    

    title = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.String(140))
    image_url = db.Column(db.String(140))

    def serializable(self):
        return {'id': self.id, 'title': self.title}
