from application.database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

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
