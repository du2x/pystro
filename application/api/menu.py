"""
    Defines APIs for menu management.
"""
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

from application.models import Item
from application.database import db
from application.auth import only_manager


titleArg = reqparse.Argument(name='title', type=str,
                             required=True,
                             help='title of item',
                             location='json')
descriptionArg = reqparse.Argument(name='description', type=str,
                                   required=True,
                                   help='description of item',
                                   location='json')
imgArg = reqparse.Argument(name='image_url', type=str,
                           required=False,
                           help='image of item',
                           location='json')


class ItemsAPI(Resource):
    """
    Defines routes for items listing and item adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(titleArg)
        self.reqparse.add_argument(descriptionArg)
        self.reqparse.add_argument(imgArg)
        super(ItemsAPI, self).__init__()

    @only_manager
    def post(self):
        data = self.reqparse.parse_args()
        try:
            item = Item(**data)
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

    def get(self):
        return Item.find_all()


titleNotReqArg = titleArg
titleNotReqArg.required = False
descriptionNotReqArg = descriptionArg
descriptionNotReqArg.required = False


class ItemAPI(Resource):
    """
    Defines routes for item editing and item viewing.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(titleNotReqArg)
        self.reqparse.add_argument(descriptionNotReqArg)
        self.reqparse.add_argument(imgArg)
        super(ItemAPI, self).__init__()

    def get(self, id):
        item = Item.find_by_id(id)
        if not item:
            return "Item not found", 404
        else:
            return item.serializable(), 200

    @only_manager
    def put(self, id):
        item = Item.find_by_id(id)
        if not item:
            return "Item not found", 404
        else:
            data = self.reqparse.parse_args()
            for k, v in data.items():
                setattr(item, k, v)
            db.session.add(item)
            db.session.commit()
            return item.serializable(), 200


